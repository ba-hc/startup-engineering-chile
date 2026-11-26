#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Gestiona el expediente de una startup (modo Expediente de la skill Startup Engineering Chile).

El modo Express (consultas rápidas) no crea archivos. El expediente se crea solo cuando el usuario quiere guardar el
proyecto: `onboarding` (3 preguntas) o `init`.

Uso (--dir es la carpeta del proyecto; el expediente vive en RUTA/expediente/):
  expediente.py onboarding --dir RUTA --proyecto "Nombre" --problema "..." --evidencia "..." --situacion "..." --objetivo "..."
                          # crea 00_estado.md, asigna gate y propone una misión de 7 días
  expediente.py init     --dir RUTA --proyecto "Nombre" [--modo empezar|pulir|complementar] [--nivel sprint|completo] [--track T]
  expediente.py doctor   [--dir RUTA]              # Python, permisos, skill, datos vigentes, internet
  expediente.py estado   --dir RUTA                # ruta, misión, acciones vencidas, hipótesis estancadas
  expediente.py gate     [--gate G1] --dir RUTA    # chequeos deterministas del gate contra los registros
  expediente.py add      REGISTRO campo=valor ... --dir RUTA [--confirmado] [--forzar]
                          # REGISTRO: núcleo, rendiciones, bitacora o un nombre antiguo (riesgos, indicadores, ...)
  expediente.py ver      REGISTRO --dir RUTA [--ultimos N] [--columnas a,b]
  expediente.py validar  --dir RUTA                # esquema, tipos (fechas, CLP/UF/USD), IDs y referencias
  expediente.py migrar   --dir RUTA                # pasa un expediente v1/v2 al esquema v3 (bitácora)
  expediente.py doc      TPL-031 --dir RUTA        # copia una plantilla a documentos/ (no sobrescribe)
  expediente.py plantillas [--troncales] [--dominio D] [--buscar texto]
  expediente.py biblioteca "texto" [--tipo fuentes|libros|mentores|charlas|casos|workshops|curriculo|cifras]
  expediente.py buscar-fuente "texto" [--tema publico|mercado|legal|metodos] [--verificadas]
  expediente.py id       REGISTRO --dir RUTA       # siguiente ID libre (p. ej. EV-004)
  expediente.py exportar [REGISTRO|todos] --dir RUTA [--xlsx]   # CSV ';' con BOM o un .xlsx con una hoja por registro
  expediente.py informe  semanal|onepager|deck --dir RUTA       # Markdown en entregables/ (deck: Marp)
  expediente.py modelo   --dir RUTA                # copia el modelo financiero de ejemplo
  expediente.py buscar   "texto" [--gate G4] [--en plantillas|manual|todo]   # ranking BM25: qué archivos leer
  expediente.py umbrales [--gate G4] [--track saas_b2b] --dir RUTA
  expediente.py resumen  --dir RUTA [--guardar]    # ~600 tokens para retomar en otra conversación
  expediente.py empaquetar --dir RUTA [--salida CARPETA]       # ZIP del expediente para descargar
  expediente.py restaurar  PAQUETE.zip --dir RUTA [--forzar]   # vuelve a abrir un ZIP empaquetado

La lógica vive en scripts/core/ (storage, schemas, registros, estado, gates, exporters, busqueda, plantillas).
Solo biblioteca estándar de Python (3.8+).
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import ASSETS, GATES, NIVELES, PLANTILLAS, REFS, REGISTROS, SCHEMA_VERSION, SIGUIENTE, SKILL_DIR  # noqa: E402,F401
from core.storage import (bloqueo, campo, csv_texto, escribir_atomico, escribir_manifest, estado_path, exp_dir, leer,  # noqa: E402,F401
                          leer_estado, leer_manifest, leer_seguro, nombre_proyecto, reg_path, requiere_expediente, seccion,
                          tiene_bom)
from core.schemas import (BITACORA, LEGADO, NUCLEO, PREFIJOS, buscar_pii, es_numero, esquema, fecha_iso,  # noqa: E402,F401
                          parse_monto, registros_disponibles, validar)
from core.registros import (GITIGNORE_EXPEDIENTE, agregar, asegurar_registro, bitacora, filas, ids_de, migrar,  # noqa: E402,F401
                            siguiente_id)
from core.estado import (acciones, gate_actual_de, hipotesis_estancadas, inferir_gate, mision, numeros_clave,  # noqa: E402,F401
                         texto_estado)
from core.gates import evaluar_gate, lineas_umbral, progreso, umbrales_data  # noqa: E402,F401
from core.plantillas import catalogo, catalogo_fila, contar_troncales, esqueleto_plantilla, slug, template_path  # noqa: E402,F401
from core.busqueda import CATALOGOS, buscar, buscar_fuente, filas_catalogo  # noqa: E402,F401
from core import exporters  # noqa: E402

MIN_TRONCALES = 40

# Misión de 7 días sugerida según el gate asignado en el onboarding: (misión, cómo sabremos que se cumplió)
MISIONES = {
    "G0": ("Escribir el problema en una frase sin nombrar la solución y conseguir 8 conversaciones agendadas con personas del segmento",
           "Frase en 00_estado.md y 8 conversaciones con fecha (sin datos personales en el expediente)"),
    "G1": ("Hacer 5 entrevistas de problema en un mismo segmento preguntando por la última vez que les pasó",
           "5 filas en entrevistas con situación y hecho o cita breve"),
    "G4": ("Pedir un compromiso concreto (preventa, depósito, carta firmada u OC) a 3 cuentas con el precio fijado antes",
           "Al menos 1 compromiso registrado en evidencias o en el pipeline"),
    "G6": ("Acordar con el sponsor del piloto la línea base, la métrica, la meta y la fecha de decisión comercial",
           "Piloto con baseline, métrica, meta y fecha de conversión escritos y aceptados por el cliente"),
    "G7": ("Medir CAC, churn y ciclo de venta con las ventas reales de los últimos 3 meses",
           "Números clave de 00_estado.md completos desde datos, no supuestos"),
}
FONDO = re.compile(r"corfo|semilla|anid|startup ciencia|startup ctci|sercotec|fondo|subsidio|capital abeja|start-?up chile", re.I)


def _linea_doctor():
    estado = {"ok": True}

    def linea(nivel, texto, arreglo=""):
        if nivel == "ERROR":
            estado["ok"] = False
        print(f"[{nivel}] {texto}" + (f"\n        → {arreglo}" if arreglo else ""))
    return linea, estado


# ---------------------------------------------------------------- comandos
def cmd_doctor(a):
    linea, st = _linea_doctor()
    v = sys.version_info
    if v >= (3, 8):
        linea("OK", f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        linea("ERROR", f"Python {v.major}.{v.minor} es muy antiguo", "instala Python 3.8 o superior (python.org) y usa `py -3` en Windows")
    nreg, npl = len(registros_disponibles()), contar_troncales()
    if nreg >= 10 and npl >= MIN_TRONCALES and os.path.exists(os.path.join(ASSETS, "modelo_financiero.xlsx")):
        linea("OK", f"Skill completa: {nreg} registros, {npl} plantillas troncales, modelo financiero")
    else:
        linea("ERROR", f"Skill incompleta ({nreg} registros, {npl} plantillas)", "reinstala la skill desde el repositorio o el ZIP del release")
    destino = os.path.abspath(a.dir)
    try:
        fd, tmp = tempfile.mkstemp(dir=destino if os.path.isdir(destino) else None)
        os.close(fd)
        os.remove(tmp)
        linea("OK", f"Se puede escribir en {destino}")
    except OSError as e:
        linea("ERROR", f"No se puede escribir en {destino} ({e.strerror})", "elige otra carpeta del proyecto con --dir")
    if os.name == "nt" and len(destino) > 200:
        linea("AVISO", "Ruta muy larga para Windows", "ejecuta desde una carpeta corta y pasa rutas absolutas")
    for rel, nombre, meses in (("parametros_cl.json", "Parámetros legales", 6),
                               (os.path.join("fondos", "instrumentos.json"), "Reglas de fondos", 3),
                               ("umbrales_gates.json", "Umbrales por gate", 12)):
        try:
            with open(os.path.join(ASSETS, rel), encoding="utf-8") as f:
                ver = json.load(f).get("_verificado", "")
            dias = (dt.date.today() - dt.date.fromisoformat(ver)).days
        except (OSError, ValueError, TypeError):
            linea("AVISO", f"{nombre}: sin fecha de verificación legible ({rel})")
            continue
        if dias > meses * 30:
            linea("AVISO", f"{nombre}: verificado el {ver} (hace {dias} días; más de {meses} meses)",
                  "dilo al usuario, corre actualizar_parametros.py y verifica en la fuente antes de afirmar cifras o reglas")
        else:
            linea("OK", f"{nombre}: verificado el {ver}")
    try:
        urllib.request.urlopen(urllib.request.Request("https://mindicador.cl/api", headers={"User-Agent": "sec-doctor"}), timeout=4).read(64)
        linea("OK", "API de indicadores (mindicador.cl) responde")
    except Exception:
        linea("INFO", "Sin internet o mindicador.cl no responde (opcional)",
              "indicadores_cl.py usará la caché o los valores de respaldo con su fecha; o pasa --uf/--utm a finanzas.py")
    if os.path.isdir(exp_dir(a.dir)):
        m = leer_manifest(a.dir) or {}
        sv = m.get("schema_version", 1)
        if m.get("corrupto"):
            linea("ERROR", "manifest.json del expediente está dañado", "expediente.py migrar --dir <carpeta>")
        elif sv < SCHEMA_VERSION:
            linea("AVISO", f"Expediente con esquema v{sv} (actual v{SCHEMA_VERSION})", "expediente.py migrar --dir <carpeta>")
        else:
            linea("OK", f"Expediente encontrado (esquema v{sv})")
        errores, avisos = validar(a.dir)
        if errores:
            linea("AVISO", f"Validación: {len(errores)} error(es), {len(avisos)} aviso(s)", "expediente.py validar --dir <carpeta>")
        else:
            linea("OK", f"Validación sin errores ({len(avisos)} aviso(s))")
    else:
        linea("INFO", "No hay expediente en esta carpeta: modo Express (se crea con `onboarding` solo si el usuario quiere guardar)")
    sys.exit(0 if st["ok"] else 1)


def _crear(base, estado_txt, nivel, track=None):
    e = exp_dir(base)
    for sub in ["registros", "documentos", "entregables", "investigacion"]:
        os.makedirs(os.path.join(e, sub), exist_ok=True)
    for r in NIVELES[nivel]:
        asegurar_registro(base, r)
    est = estado_path(base)
    creado = not os.path.exists(est)
    if creado:
        escribir_atomico(est, estado_txt)
    gi = os.path.join(e, ".gitignore")
    if not os.path.exists(gi):
        escribir_atomico(gi, GITIGNORE_EXPEDIENTE)
    escribir_manifest(base, nivel=nivel, **({"track": track} if track else {}))
    return est, creado


def cmd_init(a):
    est, creado = _crear(a.dir, texto_estado(a.proyecto, a.modo, a.nivel), a.nivel, a.track)
    print(f"Creado {est}" if creado else f"Ya existía {est} (no se tocó)")
    print(f"Expediente listo en {exp_dir(a.dir)} (nivel {a.nivel}). Los demás registros se crean al usarlos (`add`).")
    print("Por privacidad, expediente/.gitignore evita que se suba a git; bórralo si usas un repo privado.")


def cmd_onboarding(a):
    """Wizard de 3 preguntas → 00_estado.md con gate asignado y una misión de 7 días."""
    gate = (a.gate or inferir_gate(a.evidencia)).upper()
    mis, criterio = MISIONES.get(gate, MISIONES["G0"])
    vence = (dt.date.today() + dt.timedelta(days=7)).isoformat()
    txt = texto_estado(a.proyecto, a.modo, a.nivel, frase=a.problema, evidencia=a.evidencia, situacion=a.situacion,
                       objetivo=a.objetivo, gate=gate, mision=mis, vence=vence, criterio=criterio,
                       primera="Onboarding (3 preguntas): gate y misión asignados")
    est, creado = _crear(a.dir, txt, a.nivel, a.track)
    if not creado:
        sys.exit(f"Ya existe {est}: no se sobrescribe. Usa `estado` para retomar o edita el perfil a mano.")
    print(f"Creado {est}")
    print(f"Gate asignado: {gate} ({dict((g, n) for g, n, _ in GATES)[gate]}) — según la evidencia declarada; ajústalo si no calza.")
    print(f"Misión de 7 días (vence {vence}): {mis}")
    print(f"Cómo sabremos que se cumplió: {criterio}")
    if FONDO.search(a.objetivo or ""):
        print("Objetivo con fondos: corre `fondos_matcher.py --dir <carpeta>` para ver a qué instrumentos calza y qué filtros duros no cumple.")
    if re.search(r"extranjer|delaware|cayman|sin empresa|sin constituir|persona natural", a.situacion or "", re.I):
        print("Situación societaria a revisar: ver references/flujos/flip_societario.md y el filtro de persona jurídica del fondo.")


def cmd_estado(a):
    txt = leer_estado(a.dir)
    if not txt:
        print("SIN_EXPEDIENTE: no hay expediente en esta carpeta (modo Express).")
        return
    hoy = dt.date.today()
    print(f"# Estado del expediente — {nombre_proyecto(a.dir)} — {hoy.isoformat()}\n")
    m = leer_manifest(a.dir) or {}
    if m.get("schema_version", 1) < SCHEMA_VERSION or m.get("corrupto"):
        print(f"> Esquema antiguo o manifest dañado: corre `expediente.py migrar --dir {a.dir}`.\n")
    ruta = seccion(txt, "Ruta")
    if ruta:
        print("## Ruta\n" + "\n".join(l for l in ruta.splitlines() if l.startswith("|")) + "\n")
    foco = seccion(txt, "Foco actual")
    gate = gate_actual_de(a.dir)
    if foco:
        print("## Foco actual\n" + foco + "\n")
    if gate:
        ev = evaluar_gate(a.dir, gate)
        if ev:
            ok = sum(1 for c in ev if c["cumple"])
            print(f"## Chequeos de {gate}: {ok}/{len(ev)}")
            for c in ev:
                print(f"- {'✓' if c['cumple'] else '✗'} {c['texto']} (actual {c['actual']}, mínimo {c['min']})")
            print()
    mi = mision(txt, hoy)
    if mi:
        print("## Misión de 7 días" + (" — ⚠ VENCIDA" if mi["vencida"] else ""))
        print(f"- {mi['mision']}\n- Vence: {mi['vence'] or '?'} · Estado: {mi['estado'] or 'abierta'}\n- Criterio: {mi['criterio']}\n")
    trabajo = seccion(txt, "Trabajo de campo pendiente")
    if trabajo and re.search(r":\*\*\s*\S", trabajo):
        print("## Trabajo de campo pendiente\n" + trabajo + "\n")
    pend, vencidas = acciones(txt, hoy)
    if vencidas:
        print("## ⚠ Acciones vencidas")
        for acc, resp, f in vencidas:
            print(f"- {acc} · {resp} · venció {f}")
        print()
    if pend:
        print("## Acciones abiertas")
        for acc, resp, f in pend:
            print(f"- {acc} · {resp} · {f}")
        print()
    est = hipotesis_estancadas(a.dir, hoy)
    if est:
        print("## Hipótesis estancadas (>14 días sin experimento ni evidencia nueva)")
        for hid, txt_h, dias in est:
            print(f"- {hid} ({dias} días): {txt_h}")
        print()
    rdir = os.path.join(exp_dir(a.dir), "registros")
    if os.path.isdir(rdir):
        cuentas = []
        for f in sorted(os.listdir(rdir)):
            if not f.endswith(".csv"):
                continue
            h, rows, err = leer_seguro(os.path.join(rdir, f))
            if err:
                cuentas.append(f"{f[:-4]}=ILEGIBLE (corre validar)")
                continue
            prop = 0
            if "estado" in h:
                i = h.index("estado")
                prop = sum(1 for r in rows if len(r) > i and r[i] == "propuesta-agente")
            det = ""
            if f[:-4] == BITACORA and rows and "tipo" in h:
                i = h.index("tipo")
                por = {}
                for r in rows:
                    t = r[i] if len(r) > i else "?"
                    por[t] = por.get(t, 0) + 1
                det = " [" + ", ".join(f"{k}:{v}" for k, v in sorted(por.items())) + "]"
            cuentas.append(f"{f[:-4]}={len(rows)}{det}" + (f" ({prop} por confirmar)" if prop else ""))
        print("## Registros\n" + ", ".join(cuentas) + "\n")
        ult = {}
        for d in filas(a.dir, "decisiones"):
            ult[d.get("gate", "?")] = d
        if ult:
            print("## Última decisión por gate")
            for g, d in sorted(ult.items()):
                print(f"- {g}: {d.get('decision', '')} ({d.get('fecha', '')}) — {d.get('justificacion', '')[:120]}")
            print()
    ddir = os.path.join(exp_dir(a.dir), "documentos")
    if os.path.isdir(ddir) and os.listdir(ddir):
        print("## Documentos\n" + ", ".join(sorted(os.listdir(ddir))) + "\n")
    inv = os.path.join(exp_dir(a.dir), "investigacion")
    if os.path.isdir(inv):
        n = sum(len([f for f in fs if f.endswith(".md")]) for _, _, fs in os.walk(inv))
        if n:
            print(f"## Investigación guardada\n{n} archivos .md en investigacion/\n")
    if gate in SIGUIENTE:
        print(f"## Siguiente paso orientativo (plan 90 días, {gate})\n{SIGUIENTE[gate]}")


def cmd_gate(a):
    requiere_expediente(a.dir)
    g = (a.gate or gate_actual_de(a.dir) or "G0").upper()
    data = umbrales_data()["gates"]
    if g not in data:
        sys.exit(f"Gate desconocido {g}. Usa G0–G9.")
    ev = evaluar_gate(a.dir, g)
    ok = sum(1 for c in ev if c["cumple"])
    print(f"## {g} — {data[g]['pregunta']}\n")
    print("| | Chequeo | Mínimo | Actual |\n|---|---|---|---|")
    for c in ev:
        print(f"| {'✓' if c['cumple'] else '✗'} | {c['texto']} | {c['min']} | {c['actual']} |")
    print(f"\n{ok}/{len(ev)} chequeos cumplidos.")
    if ev and ok == len(ev):
        print("LISTO PARA DECIDIR: hay base para comparar contra el criterio fijado antes. No es un Go automático; registra la decisión "
              "con `add decisiones`.")
    else:
        print("FALTA: no decidas Go todavía; lo que falta es el trabajo de la próxima semana.")
    track = (leer_manifest(a.dir) or {}).get("track")
    lu = lineas_umbral(g, track)
    if lu:
        print("\nCriterios de referencia (no se cuentan solos): " + "; ".join(lu[:4]))


def cmd_add(a):
    requiere_expediente(a.dir)
    valores = {}
    for kv in a.campos:
        if "=" not in kv:
            sys.exit(f"Formato inválido '{kv}': usa campo=valor")
        k, v = kv.split("=", 1)
        valores[k.strip()] = v.strip()
    rid = agregar(a.dir, a.registro, valores, confirmado=a.confirmado, forzar=a.forzar)
    print(rid or "(fila agregada)")


def cmd_ver(a):
    reg = a.registro.replace(".csv", "")
    if reg in LEGADO:
        header = list(LEGADO[reg][1])
        rows = [[d.get(c, "") for c in header] for d in filas(a.dir, reg)]
    else:
        path = reg_path(a.dir, reg)
        if not os.path.exists(path):
            print(f"(sin registro {reg} todavía)")
            return
        header, rows, err = leer_seguro(path)
        if err:
            sys.exit(f"No pude leer {path}: {err}")
    if a.ultimos:
        rows = rows[-a.ultimos:]
    cols = a.columnas.split(",") if a.columnas else header
    idx = [header.index(c) for c in cols if c in header]

    def corta(s):
        return (s[:a.ancho - 1] + "…") if len(s) > a.ancho else s
    print("| " + " | ".join(header[i] for i in idx) + " |")
    print("|" + "---|" * len(idx))
    for r in rows:
        r = list(r) + [""] * (len(header) - len(r))
        print("| " + " | ".join(corta(r[i].replace("|", "/").replace("\n", " ")) for i in idx) + " |")
    print(f"\n{len(rows)} fila(s)")


def cmd_validar(a):
    requiere_expediente(a.dir)
    m = leer_manifest(a.dir) or {}
    if m.get("schema_version", 1) < SCHEMA_VERSION:
        print(f"AVISO: esquema v{m.get('schema_version', 1)}; corre `expediente.py migrar`.")
    errores, avisos = validar(a.dir)
    for e in errores:
        print("ERROR  " + e)
    for w in avisos:
        print("aviso  " + w)
    print(f"\n{len(errores)} error(es), {len(avisos)} aviso(s).")
    sys.exit(1 if errores else 0)


def cmd_migrar(a):
    requiere_expediente(a.dir)
    with bloqueo(a.dir):
        migrar(a.dir)


def cmd_doc(a):
    src = template_path(a.tpl)
    fila = None if src else catalogo_fila(a.tpl)
    if not src and not fila:
        sys.exit(f"No existe la plantilla {a.tpl}. Lista: expediente.py plantillas")
    requiere_expediente(a.dir)
    nombre = os.path.basename(src) if src else f"{fila['id']}_{slug(fila['nombre'])}.md"
    dst = os.path.join(exp_dir(a.dir), "documentos", nombre)
    if os.path.exists(dst):
        print(f"Ya existe: {dst} (edítalo, no se sobrescribe)")
        return
    proyecto = nombre_proyecto(a.dir) or "[ ]"
    if src:
        with open(src, encoding="utf-8-sig") as fh:
            txt = fh.read()
    else:
        txt = esqueleto_plantilla(fila)
    cabecera = f"**Proyecto:** {proyecto} · **Versión:** v1 · **Fecha:** {dt.date.today().isoformat()} · **Responsable:** [ ]"
    if "**Proyecto:** [ ]" in txt:
        txt = re.sub(r"^\*\*Proyecto:\*\* \[ \].*$", cabecera, txt, count=1, flags=re.M)
    else:
        primera, _, resto = txt.partition("\n")
        txt = f"{primera}\n\n{cabecera}\n{resto}"
    escribir_atomico(dst, txt)
    print(f"Creado {dst}" + ("" if src else " (esqueleto desde el catálogo)"))


def cmd_id(a):
    print(siguiente_id(a.dir, a.registro, a.tipo))


def cmd_exportar(a):
    requiere_expediente(a.dir)
    out = os.path.join(exp_dir(a.dir), "entregables", "excel")
    if a.xlsx:
        tablas = exporters.todas_las_tablas(a.dir)
        if a.registro != "todos":
            tablas = [t for t in tablas if t[0] == a.registro]
        os.makedirs(out, exist_ok=True)
        dst = os.path.join(out, f"expediente_{slug(nombre_proyecto(a.dir)) or 'proyecto'}.xlsx")
        exporters.escribir_xlsx(dst, tablas)
        print(f"Exportado {dst} ({len(tablas)} hoja(s); encabezado fijo, números como números)")
        return
    hechos = exporters.exportar_csv(a.dir, out, a.registro)
    print(f"Exportado(s) {len(hechos)} registro(s) con ';' y UTF-8 con BOM a {out} (se abren bien en Excel en español)")


def cmd_informe(a):
    requiere_expediente(a.dir)
    hoy = dt.date.today()
    if a.tipo == "deck":
        dst = os.path.join(exp_dir(a.dir), "entregables", f"deck_{hoy.isoformat()}.md")
        escribir_atomico(dst, exporters.deck_md(a.dir))
        print(f"Creado {dst} (Markdown para Marp: marp {os.path.basename(dst)} --pptx). Revisa cada [FALTA EVIDENCIA].")
        return
    nombre, texto = exporters.informe_semanal(a.dir, a.dias) if a.tipo == "semanal" else exporters.onepager(a.dir)
    dst = os.path.join(exp_dir(a.dir), "entregables", nombre)
    escribir_atomico(dst, texto)
    print(f"Creado {dst}")


def cmd_modelo(a):
    requiere_expediente(a.dir)
    dst = os.path.join(exp_dir(a.dir), "entregables", "modelo_financiero.xlsx")
    if os.path.exists(dst):
        print(f"Ya existe {dst}")
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(os.path.join(ASSETS, "modelo_financiero.xlsx"), dst)
    print(f"Copiado {dst} (escenario hipotético: reemplaza los supuestos con `modelo_xlsx.py set`)")


def cmd_biblioteca(a):
    tipos = [a.tipo] if a.tipo else list(CATALOGOS)
    pat = re.compile(re.escape(a.texto), re.I) if a.texto else None
    n = 0
    for t in tipos:
        for d in filas_catalogo(t):
            linea = " · ".join(v for v in d.values() if v)
            if pat and not pat.search(linea):
                continue
            print(f"[{t}] {linea[:300]}")
            n += 1
            if n >= a.max:
                print(f"(se muestran {a.max}; afina la búsqueda o usa --max)")
                return
    if not n:
        print("Sin resultados.")
    elif "mentores" in tipos:
        print("Nota: los perfiles de mentores son resúmenes de fuentes públicas sin reverificar (ver columnas estado y "
              "fecha_consulta). Antes de citar a una persona, abre su URL; no la contactes en nombre del usuario.")


def cmd_buscar_fuente(a):
    res = buscar_fuente(a.texto, a.tema, a.max, a.verificadas)
    if not res:
        print("Sin resultados. Prueba otras palabras o quita --tema.")
        return
    for s, d in res:
        print(f"{d.get('id')} [{d['_archivo'].replace('fuentes_', '').replace('.csv', '')}] {d.get('titulo', '')[:110]} — "
              f"{d.get('autor_institucion', '')[:50]} · {d.get('url', '')} · {d.get('estado', '')} {d.get('fecha_reconsulta', '')}"
              f" (puntaje {s:.1f})")
    print("\nAntes de citar una cifra o regla, abre la URL y verifica la fecha; si no hay fecha_reconsulta, dilo.")


def cmd_plantillas(a):
    pat = re.compile(re.escape(a.buscar), re.I) if a.buscar else None
    n = 0
    for d in catalogo():
        if a.troncales and d.get("troncal") != "si":
            continue
        if a.dominio and d.get("dominio") != a.dominio:
            continue
        if pat and not pat.search(" ".join(d.values())):
            continue
        marca = "★ " if d.get("troncal") == "si" else "  "
        print(f"{marca}{d['id']} [{d['dominio']}] {d['nombre']} — {d['uso'][:110]}")
        n += 1
    print(f"\n{n} plantilla(s). ★ = troncal, con estructura y ejemplos; las demás se crean como esqueleto con `doc`.")


def cmd_buscar(a):
    """Ranking BM25 de archivos de la skill para una consulta; muestra las líneas más pertinentes."""
    texto = a.texto + (" " + a.gate if a.gate else "")
    from core.busqueda import tokens
    if not tokens(texto):
        sys.exit("Consulta vacía: usa palabras de 3 letras o más.")
    res = buscar(texto, a.en, a.max)
    if not res:
        print("Sin resultados.")
        return
    for s, rel, lineas in res:
        print(f"{rel}  (puntaje {s:.1f})")
        for i, l in lineas:
            print(f"    {i}: {l[:180]}")


def cmd_umbrales(a):
    data = umbrales_data()
    hay = os.path.isdir(exp_dir(a.dir))
    track = a.track or ((leer_manifest(a.dir) or {}).get("track") if hay else None)
    gates = [a.gate.upper()] if a.gate else ([gate_actual_de(a.dir)] if hay and gate_actual_de(a.dir) else list(data["gates"]))
    print(f"Track: {track or 'sin definir (usa --track o init --track)'} · referencia verificada {data.get('_verificado')}\n")
    for g in gates:
        if g not in data["gates"]:
            sys.exit(f"Gate desconocido {g}. Usa G0–G9.")
        print(f"## {g} — {data['gates'][g]['pregunta']}")
        for linea in lineas_umbral(g, track):
            print(f"- {linea}")
        for ch in data["gates"][g].get("chequeos", []):
            print(f"- [chequeo {ch['id']}] {ch['texto']} (mínimo {ch['min']})")
        print()
    print("Son umbrales de referencia para fijar el criterio ANTES de salir a terreno; otro umbral vale si se justifica antes de ver los datos.")


def cmd_resumen(a):
    """Resumen compacto (≈600 tokens) para retomar en otra conversación o en otro cliente."""
    requiere_expediente(a.dir)
    hoy = dt.date.today()
    txt = leer_estado(a.dir)
    m = leer_manifest(a.dir) or {}
    foco = seccion(txt, "Foco actual")
    gate = gate_actual_de(a.dir) or "?"
    out = [f"# Resumen para retomar — {nombre_proyecto(a.dir)} — {hoy.isoformat()}",
           f"Modo {campo(txt, 'Modo de trabajo') or '?'} · nivel {m.get('nivel', '?')} · track {m.get('track') or '?'} · gate actual {gate}",
           f"Problema: {campo(txt, 'Una frase')[:220] or '[sin definir]'}",
           f"Objetivo: {campo(txt, 'Objetivo próximo y fecha límite')[:160] or campo(txt, 'Objetivo de financiamiento')[:160] or '[sin definir]'}"]
    hr = campo(foco, "Hipótesis más riesgosa")
    if hr:
        out.append(f"Hipótesis más riesgosa: {hr[:160]}")
    mi = mision(txt, hoy)
    if mi:
        out.append(f"Misión de 7 días: {mi['mision'][:150]} (vence {mi['vence']}; {mi['estado'] or 'abierta'}"
                   + ("; VENCIDA" if mi["vencida"] else "") + ")")
    if gate in [g for g, _, _ in GATES]:
        ev = evaluar_gate(a.dir, gate)
        if ev:
            faltan = [c["texto"] for c in ev if not c["cumple"]]
            out.append(f"Chequeos {gate}: {len(ev) - len(faltan)}/{len(ev)}" + (" · falta: " + "; ".join(faltan[:3]) if faltan else ""))
    dec = filas(a.dir, "decisiones")[-3:]
    if dec:
        out.append("Últimas decisiones: " + " | ".join(f"{d.get('gate')} {d.get('decision')} {d.get('fecha', '')[:10]}: {d.get('justificacion', '')[:70]}" for d in dec))
    abiertos = [d for d in filas(a.dir, "experimentos") if not d.get("resultado", "").strip()]
    if abiertos:
        out.append("Experimentos abiertos: " + " | ".join(
            f"{d.get('experiment_id')} ({d.get('hypothesis_id')}): {d.get('metrica', '')[:50]} umbral {d.get('umbral', '')[:30]} hasta {d.get('fin', '') or '?'}"
            for d in abiertos[:3]))
    pend, venc = acciones(txt, hoy)
    est = hipotesis_estancadas(a.dir, hoy)
    errores, _ = validar(a.dir)
    alertas = []
    if venc:
        alertas.append(f"{len(venc)} acción(es) vencida(s)")
    if est:
        alertas.append(f"{len(est)} hipótesis estancada(s): " + ", ".join(h for h, _, _ in est[:4]))
    if errores:
        alertas.append(f"{len(errores)} error(es) de validación")
    out.append("Alertas: " + ("; ".join(alertas) if alertas else "ninguna"))
    if venc or pend:
        out.append("Próximas acciones: " + " | ".join(f"{acc} ({resp}, {f})" for acc, resp, f in (venc + pend)[:3]))
    cuentas = []
    for reg in ("entrevistas", "evidencias", "experimentos", "cuentas_y_pipeline", "pilotos"):
        n = len(filas(a.dir, reg))
        if n:
            cuentas.append(f"{reg}={n}")
    out.append("Registros: " + (", ".join(cuentas) or "vacíos"))
    lu = lineas_umbral(gate, m.get("track"))
    if lu:
        out.append(f"Para pasar {gate}: " + "; ".join(lu[:3]))
    texto = "\n".join(out)
    if len(texto) > 2600:
        texto = texto[:2580].rsplit("\n", 1)[0] + "\n[recortado]"
    print(texto)
    if a.guardar:
        dst = os.path.join(exp_dir(a.dir), "entregables", f"resumen_{hoy.isoformat()}.md")
        escribir_atomico(dst, texto + "\n")
        print(f"\nGuardado en {dst}")


def cmd_empaquetar(a):
    requiere_expediente(a.dir)
    with bloqueo(a.dir):
        dst, n = exporters.empaquetar(a.dir, a.salida)
    print(f"Empaquetado {n} archivo(s) en {dst} ({os.path.getsize(dst) // 1024 + 1} KB)")
    print("Entrégaselo al usuario para que lo descargue y lo vuelva a subir en la próxima sesión. Contiene datos privados.")


def cmd_restaurar(a):
    n = exporters.restaurar(a.zip, a.dir, a.forzar)
    e = exp_dir(a.dir)
    print(f"Restaurado {n} archivo(s) en {e}")
    m = leer_manifest(a.dir) or {}
    if m.get("schema_version", 1) < SCHEMA_VERSION:
        print(f"El paquete usa el esquema v{m.get('schema_version', 1)}: corre `expediente.py migrar --dir {a.dir}`.")
    print(f"Siguiente: expediente.py estado --dir {a.dir}")


def main(argv=None):
    tracks = list(umbrales_data()["tracks"])
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("doctor"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_doctor)
    for nombre, fn in (("init", cmd_init), ("onboarding", cmd_onboarding)):
        p = sp.add_parser(nombre); p.add_argument("--dir", default="."); p.add_argument("--proyecto", required=True)
        p.add_argument("--modo", default="empezar", choices=["empezar", "pulir", "complementar"])
        p.add_argument("--nivel", default="completo", choices=list(NIVELES))
        p.add_argument("--track", choices=tracks); p.set_defaults(f=fn)
        if nombre == "onboarding":
            p.add_argument("--problema", default="", help="1) qué problema, a quién le pasa (sin nombrar la solución)")
            p.add_argument("--evidencia", default="", help="2) evidencia de calle o ventas hasta hoy")
            p.add_argument("--situacion", default="", help="3a) situación societaria en Chile")
            p.add_argument("--objetivo", default="", help="3b) objetivo de financiamiento")
            p.add_argument("--gate", help="fuerza el gate en vez de inferirlo")
    p = sp.add_parser("estado"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_estado)
    p = sp.add_parser("gate"); p.add_argument("--dir", default="."); p.add_argument("--gate"); p.set_defaults(f=cmd_gate)
    p = sp.add_parser("add"); p.add_argument("registro"); p.add_argument("campos", nargs="+")
    p.add_argument("--dir", default="."); p.add_argument("--confirmado", action="store_true")
    p.add_argument("--forzar", action="store_true"); p.set_defaults(f=cmd_add)
    p = sp.add_parser("ver"); p.add_argument("registro"); p.add_argument("--dir", default=".")
    p.add_argument("--ultimos", type=int); p.add_argument("--columnas"); p.add_argument("--ancho", type=int, default=50)
    p.set_defaults(f=cmd_ver)
    p = sp.add_parser("validar"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_validar)
    p = sp.add_parser("migrar"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_migrar)
    p = sp.add_parser("doc"); p.add_argument("tpl"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_doc)
    p = sp.add_parser("plantillas"); p.add_argument("--troncales", action="store_true"); p.add_argument("--dominio")
    p.add_argument("--buscar"); p.set_defaults(f=cmd_plantillas)
    p = sp.add_parser("biblioteca"); p.add_argument("texto", nargs="?", default="")
    p.add_argument("--tipo", choices=list(CATALOGOS)); p.add_argument("--max", type=int, default=25); p.set_defaults(f=cmd_biblioteca)
    p = sp.add_parser("buscar-fuente"); p.add_argument("texto"); p.add_argument("--tema", choices=["publico", "mercado", "legal", "metodos"])
    p.add_argument("--max", type=int, default=8); p.add_argument("--verificadas", action="store_true"); p.set_defaults(f=cmd_buscar_fuente)
    p = sp.add_parser("id"); p.add_argument("registro"); p.add_argument("--tipo", help="para la bitácora: riesgo, kpi, fuente, ...")
    p.add_argument("--dir", default="."); p.set_defaults(f=cmd_id)
    p = sp.add_parser("exportar"); p.add_argument("registro", nargs="?", default="todos"); p.add_argument("--dir", default=".")
    p.add_argument("--xlsx", action="store_true", help="un .xlsx con una hoja por registro en vez de CSV"); p.set_defaults(f=cmd_exportar)
    p = sp.add_parser("informe"); p.add_argument("tipo", choices=["semanal", "onepager", "deck"]); p.add_argument("--dir", default=".")
    p.add_argument("--dias", type=int, default=7); p.set_defaults(f=cmd_informe)
    p = sp.add_parser("modelo"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_modelo)
    p = sp.add_parser("buscar"); p.add_argument("texto"); p.add_argument("--en", default="todo", choices=["plantillas", "manual", "todo"])
    p.add_argument("--gate"); p.add_argument("--max", type=int, default=5); p.set_defaults(f=cmd_buscar)
    p = sp.add_parser("umbrales"); p.add_argument("--dir", default="."); p.add_argument("--gate")
    p.add_argument("--track", choices=tracks); p.set_defaults(f=cmd_umbrales)
    p = sp.add_parser("resumen"); p.add_argument("--dir", default="."); p.add_argument("--guardar", action="store_true")
    p.set_defaults(f=cmd_resumen)
    p = sp.add_parser("empaquetar"); p.add_argument("--dir", default="."); p.add_argument("--salida")
    p.set_defaults(f=cmd_empaquetar)
    p = sp.add_parser("restaurar"); p.add_argument("zip"); p.add_argument("--dir", default=".")
    p.add_argument("--forzar", action="store_true"); p.set_defaults(f=cmd_restaurar)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
