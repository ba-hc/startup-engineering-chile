#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Gestiona el expediente de una startup (núcleo de evidencia del pack Startup Engineering Chile).

Uso (--dir es la carpeta del proyecto; el expediente vive en RUTA/expediente/):
  expediente.py doctor   [--dir RUTA]              # verifica Python, permisos, skill, Firecrawl e internet
  expediente.py init     --dir RUTA --proyecto "Nombre" [--modo empezar|pulir|complementar]
                         [--nivel sprint|completo] [--track saas_b2b|b2c|marketplace|deeptech|hardware|servicios]
  expediente.py estado   --dir RUTA                # ruta por gates, campo pendiente, acciones vencidas
  expediente.py add      REGISTRO campo=valor ... --dir RUTA [--confirmado] [--forzar]
  expediente.py ver      REGISTRO --dir RUTA [--ultimos N] [--columnas a,b]
  expediente.py validar  --dir RUTA                # esquema, fechas ISO, números, IDs y referencias
  expediente.py migrar   --dir RUTA                # actualiza registros y manifest al esquema actual
  expediente.py doc      TPL-031 --dir RUTA        # copia una plantilla a documentos/ (no sobrescribe)
  expediente.py plantillas [--troncales] [--dominio D] [--buscar texto]
  expediente.py biblioteca "texto" [--tipo fuentes|libros|mentores|charlas|casos|workshops|curriculo|cifras]
  expediente.py id       REGISTRO --dir RUTA       # siguiente ID libre (p. ej. EV-004)
  expediente.py exportar [REGISTRO|todos] --dir RUTA   # CSV con ';' y BOM para Excel en español
  expediente.py informe  semanal|onepager|deck --dir RUTA   # Markdown en entregables/ (deck: Marp)
  expediente.py modelo   --dir RUTA                # copia el modelo financiero de ejemplo
  expediente.py buscar   "texto" [--gate G4] [--en plantillas|manual|todo]   # ranking BM25: qué archivos leer
  expediente.py umbrales [--gate G4] [--track saas_b2b] --dir RUTA     # criterios de referencia del gate
  expediente.py resumen  --dir RUTA [--guardar]     # ~600 tokens para retomar en otra conversación
  expediente.py empaquetar --dir RUTA [--salida CARPETA]   # ZIP del expediente para descargar
  expediente.py restaurar  PAQUETE.zip --dir RUTA [--forzar]  # vuelve a abrir un ZIP empaquetado

Solo biblioteca estándar de Python (3.8+).
"""
import argparse
import csv
import datetime as dt
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import urllib.request
import zipfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL_DIR, "assets")
REFS = os.path.join(SKILL_DIR, "references")
PLANTILLAS = os.path.join(ASSETS, "plantillas")
REGISTROS = os.path.join(ASSETS, "registros")
SCHEMA_VERSION = 2
NIVELES = {"sprint": ["hipotesis", "evidencias"], "completo": ["hipotesis", "evidencias", "decisiones"]}

GATES = [
    ("G0", "Oportunidad", "¿vale la pena investigar?"),
    ("G1", "Problema", "¿qué necesidad existe?"),
    ("G2", "Mercado", "¿a quién vender?"),
    ("G3", "Propuesta", "¿por qué elegirnos?"),
    ("G4", "Economía", "¿se puede cobrar rentablemente?"),
    ("G5", "Factibilidad", "¿funciona técnicamente?"),
    ("G6", "Piloto", "¿entrega valor en contexto?"),
    ("G7", "Venta/adopción", "¿compra y usa el cliente?"),
    ("G8", "Repetibilidad", "¿se repite venta e implementación?"),
    ("G9", "Escala", "¿conviene invertir más?"),
]
# Siguiente paso orientativo por gate (de references/operacion/01_plan_90_dias.md)
SIGUIENTE = {
    "G0": "Semanas 1–2: comparar 2–3 oportunidades, recursos y pérdida aceptable; investigación secundaria y competencia rápida.",
    "G1": "Semana 3: entrevistas exploratorias y observación del proceso; registrar también casos negativos.",
    "G2": "Semana 4: ICP, unidad de decisión (DMU) y compradores; mercado inicial bottom-up.",
    "G3": "Semanas 5–6: alternativas y benchmark, propuesta de valor con valor cuantificado (VPC, ROI).",
    "G4": "Semanas 7 y 11: prueba de precio y condiciones; costos, caja y escenarios.",
    "G5": "Semana 8: prototipo o PoC que ataque el riesgo técnico/usabilidad principal.",
    "G6": "Semanas 9–10: sponsor y comprador, pilot charter con criterio de éxito; medición.",
    "G7": "Semana 12: compromiso verificable, IRL/ARL/PMF y riesgos.",
    "G8": "Cohortes, capacidad y márgenes; estandarizar venta e implementación.",
    "G9": "Caja, capacidad, retención y riesgo antes de invertir en escala.",
}

PREFIJOS = {"evidencias": "EV", "hipotesis": "H", "experimentos": "EXP", "decisiones": "DEC", "riesgos": "R",
            "competencia": "COMP", "entrevistas": "ENT", "pilotos": "PIL", "cuentas_y_pipeline": "CTA",
            "fuentes_nuevas": "SRC", "indicadores": "KPI", "ip_licencias": "IP", "rendiciones": "GAS",
            "lecciones_mentores": "LEC", "desafios_corporativos": "DES", "corfo_elegibilidad": "REQ", "cohortes": "COH"}
# columna -> registro al que apunta
REFERENCIAS = {"hypothesis_id": "hipotesis", "experiment_id": "experimentos", "evidence_id": "evidencias",
               "evidence_ids": "evidencias", "cuenta_id": "cuentas_y_pipeline"}
# campos que `add` exige (se puede saltar con --forzar)
OBLIGATORIOS = {"experimentos": ["hypothesis_id", "metrica", "umbral"],
                "evidencias": ["afirmacion", "fuente_url_o_ruta"],
                "decisiones": ["gate", "decision", "justificacion"],
                "entrevistas": ["segmento", "hecho_o_cita_breve"]}
COLS_FECHA = {"fecha", "fecha_consulta", "fecha_publicacion", "fecha_estimada", "inicio", "fin", "vencimiento", "revision"}
DECISIONES_VALIDAS = {"go", "hold", "recycle", "kill", "no aplica"}
ESTADOS_DATO = {"propuesta-agente", "confirmado", "descartado", "en revisión", "en revision", "vigente", "obsoleto"}

ESTADO_TPL = """# Expediente: {proyecto}

> Núcleo permanente del proyecto. La skill lo actualiza al cerrar cada bloque.
> Las vistas (pitch, dossier, informe) se generan desde aquí; la presentación no crea evidencia.
> Regla: los campos del perfil solo llevan lo que dijo el usuario. Lo propuesto por el agente se marca "(propuesta, por confirmar)".
> Privacidad: sin nombres, correos ni teléfonos de entrevistados (usa ENT-001, rol y segmento).

## Perfil
- **Proyecto:** {proyecto}
- **Modo de trabajo:** {modo}
- **Nivel:** {nivel}
- **Creado:** {hoy}
- **Etapa declarada:**
- **Una frase (sin nombrar la solución):** [segmento] necesita [trabajo] y hoy enfrenta [problema] usando [alternativa].
- **Equipo y dedicación:**
- **Recursos y pérdida aceptable:**
- **Objetivo próximo y fecha límite:**
- **Materiales / sitio web:**

## Ruta
| Gate | Estado | Evidencia (0–4) | Qué lo movería |
|---|---|---|---|
{ruta}
| CORFO u otro fondo | no aplica | — | |

Estados: pendiente · en curso · Go · Hold · Recycle · Kill · no aplica. Evidencia: 0 sin evidencia · 1 hipótesis · 2 secundaria · 3 primaria parcial · 4 pertinente y comprobable.

## Foco actual
- **Gate actual:** G0
- **Hipótesis más riesgosa:**
- **Único cuello de botella:**

## Trabajo de campo pendiente
- **Tarea:**
- **Plazo:**
- **Criterio fijado antes (EXP-…):**
- **Qué traer de vuelta:**

## Próximas acciones
| # | Acción | Responsable | Vence | Criterio de éxito | Estado |
|---|---|---|---|---|---|

## Herramientas
- **Firecrawl local:** sin verificar

## Bitácora de sesiones
| Fecha | Qué se hizo | Evidencia nueva | Decisión | Para la próxima |
|---|---|---|---|---|
| {hoy} | Expediente creado | — | — | — |
"""

GITIGNORE_EXPEDIENTE = """# El expediente puede contener entrevistas, precios de clientes y datos personales.
# Por defecto no se sube a git. Si lo quieres versionar en un repositorio PRIVADO, borra este archivo.
*
!.gitignore
"""


# ---------------------------------------------------------------- utilidades
def exp_dir(base):
    return os.path.join(os.path.abspath(base), "expediente")


def reg_path(base, reg):
    return os.path.join(exp_dir(base), "registros", reg.replace(".csv", "") + ".csv")


def escribir_atomico(path, texto, bom=False):
    """Escribe en un temporal y reemplaza: si se corta a la mitad, el archivo original queda intacto."""
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp_", suffix=os.path.splitext(path)[1])
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as fh:
            fh.write(texto)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def csv_texto(header, rows, delimiter=","):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue()


def tiene_bom(path):
    with open(path, "rb") as fh:
        return fh.read(3) == b"\xef\xbb\xbf"


def leer(path):
    """Devuelve (header, filas). Tolera BOM, archivos vacíos y filas en blanco."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return [], []
    return rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]


def leer_seguro(path):
    """Como leer(), pero devuelve (header, filas, error) sin lanzar excepción."""
    try:
        h, r = leer(path)
        return h, r, None
    except (UnicodeDecodeError, csv.Error, OSError) as e:
        return [], [], f"{type(e).__name__}: {e}"


def esquema(reg):
    src = os.path.join(REGISTROS, reg + ".csv")
    return leer(src)[0] if os.path.exists(src) else None


def registros_disponibles():
    return sorted(f[:-4] for f in os.listdir(REGISTROS) if f.endswith(".csv"))


def asegurar_registro(base, reg):
    """Crea el registro desde el esquema del pack si aún no existe (o si quedó vacío)."""
    reg = reg.replace(".csv", "")
    dst = reg_path(base, reg)
    if not os.path.exists(dst) or os.path.getsize(dst) == 0:
        cols = esquema(reg)
        if cols is None:
            sys.exit(f"Registro desconocido '{reg}'. Disponibles: {', '.join(registros_disponibles())}")
        escribir_atomico(dst, csv_texto(cols, []), bom=True)
    return dst


def manifest_path(base):
    return os.path.join(exp_dir(base), "manifest.json")


def leer_manifest(base):
    p = manifest_path(base)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except (ValueError, OSError):
            return {"schema_version": 0, "corrupto": True}
    return {"schema_version": 1} if os.path.isdir(exp_dir(base)) else None


def escribir_manifest(base, **extra):
    m = leer_manifest(base) or {}
    m.pop("corrupto", None)
    m.update({"schema_version": SCHEMA_VERSION, "actualizado": dt.date.today().isoformat()}, **extra)
    m.setdefault("creado", dt.date.today().isoformat())
    escribir_atomico(manifest_path(base), json.dumps(m, ensure_ascii=False, indent=2) + "\n")


def nombre_proyecto(base):
    est = os.path.join(exp_dir(base), "00_estado.md")
    if os.path.exists(est):
        m = re.search(r"^# Expediente: (.+)$", open(est, encoding="utf-8").read(), re.M)
        if m:
            return m.group(1).strip()
    return ""


def requiere_expediente(base):
    if not os.path.isdir(exp_dir(base)):
        sys.exit("No hay expediente. Ejecuta primero: expediente.py init --dir <carpeta> --proyecto \"Nombre\"")


def fecha_iso(v):
    try:
        dt.date.fromisoformat(v.strip()[:10])
        return len(v.strip()) >= 10
    except ValueError:
        return False


def es_numero(v):
    v = v.strip().replace("$", "").replace(" ", "")
    if not v:
        return True
    # acepta 1200000, 1.200.000, 1200000.5, 0,25 y 25%
    v = v.rstrip("%")
    return bool(re.fullmatch(r"-?(\d{1,3}(\.\d{3})+|\d+)([.,]\d+)?", v))


def seccion(txt, titulo):
    m = re.search(r"^## " + re.escape(titulo) + r"\s*\n(.*?)(?=^#{2,3} |\Z)", txt, re.M | re.S)
    return m.group(1).strip() if m else ""


def ids_de(base, reg):
    path = reg_path(base, reg)
    if not os.path.exists(path):
        return set()
    _, rows, err = leer_seguro(path)
    return {r[0].strip() for r in rows if r and r[0].strip()} if not err else set()


# ---------------------------------------------------------------- comandos
def cmd_doctor(a):
    ok = True

    def linea(nivel, texto, arreglo=""):
        nonlocal ok
        if nivel == "ERROR":
            ok = False
        print(f"[{nivel}] {texto}" + (f"\n        → {arreglo}" if arreglo else ""))

    v = sys.version_info
    if v >= (3, 8):
        linea("OK", f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        linea("ERROR", f"Python {v.major}.{v.minor} es muy antiguo", "instala Python 3.8 o superior (python.org) y usa `py -3` en Windows")
    nreg = len(registros_disponibles())
    npl = sum(1 for _, _, fs in os.walk(PLANTILLAS) for f in fs if re.match(r"TPL-\d{3}_.*\.md$", f))
    if nreg >= 17 and npl >= 25 and os.path.exists(os.path.join(ASSETS, "modelo_financiero.xlsx")):
        linea("OK", f"Skill completa: {nreg} registros, {npl} plantillas, modelo financiero")
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
                  "dilo al usuario y verifica en la fuente antes de afirmar cifras o reglas")
        else:
            linea("OK", f"{nombre}: verificado el {ver}")
    url = os.environ.get("FIRECRAWL_API_URL", "http://localhost:3002").rstrip("/")
    try:
        urllib.request.urlopen(url + "/", timeout=2)
        linea("OK", f"Firecrawl responde en {url}")
    except Exception:
        linea("INFO", f"Firecrawl no está activo en {url} (opcional; no hace falta)")
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
        linea("INFO", "No hay expediente en esta carpeta (se crea con `init` cuando haga falta)")
    sys.exit(0 if ok else 1)


def cmd_init(a):
    e = exp_dir(a.dir)
    for sub in ["registros", "documentos", "entregables", "investigacion"]:
        os.makedirs(os.path.join(e, sub), exist_ok=True)
    for r in NIVELES[a.nivel]:
        asegurar_registro(a.dir, r)
    est = os.path.join(e, "00_estado.md")
    if not os.path.exists(est):
        ruta = "\n".join(f"| {g} {n}: {q} | pendiente | 0 | |" for g, n, q in GATES)
        escribir_atomico(est, ESTADO_TPL.format(proyecto=a.proyecto, modo=a.modo, nivel=a.nivel,
                                                 hoy=dt.date.today().isoformat(), ruta=ruta))
        print(f"Creado {est}")
    else:
        print(f"Ya existía {est} (no se tocó)")
    gi = os.path.join(e, ".gitignore")
    if not os.path.exists(gi):
        escribir_atomico(gi, GITIGNORE_EXPEDIENTE)
    escribir_manifest(a.dir, nivel=a.nivel, **({"track": a.track} if a.track else {}))
    print(f"Expediente listo en {e} (nivel {a.nivel}). Los demás registros se crean al usarlos (`add`).")
    print("Por privacidad, expediente/.gitignore evita que se suba a git; bórralo si usas un repo privado.")


def normalizar_tpl(tpl_id):
    tpl_id = tpl_id.upper()
    if re.fullmatch(r"TPL-?\d{1,3}", tpl_id):
        tpl_id = "TPL-" + tpl_id.split("-")[-1].replace("TPL", "").zfill(3)
    return tpl_id


def template_path(tpl_id):
    tpl_id = normalizar_tpl(tpl_id)
    for root, _, files in os.walk(PLANTILLAS):
        for f in files:
            if f.upper().startswith(tpl_id + "_"):
                return os.path.join(root, f)
    return None


def catalogo_fila(tpl_id):
    tpl_id = normalizar_tpl(tpl_id)
    h, rows = leer(os.path.join(PLANTILLAS, "catalogo_plantillas.csv"))
    for r in rows:
        d = dict(zip(h, r))
        if d.get("id") == tpl_id:
            return d
    return None


def slug(texto):
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")[:60]


def esqueleto_plantilla(d):
    """Las plantillas no troncales viven solo en el catálogo: se genera un esqueleto breve."""
    return "\n".join([
        f"# {d['id']} — {d['nombre']}", "",
        f"**Para qué:** {d['uso']}", "",
        f"*Plantilla no troncal: estructúrala según el capítulo del manual del dominio «{d['dominio']}» y los "
        "ejemplos de `references/ejemplos_y_umbrales.md`. Cada afirmación con su ID de evidencia o marcada como supuesto.*", "",
        "## Completar", "[ ]", "",
        "## Criterio de aceptación", f"- {d['criterio_aceptacion']}", "",
        "## Decisión",
        "Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]",
        ""])


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
    txt = open(src, encoding="utf-8-sig").read() if src else esqueleto_plantilla(fila)
    cabecera = f"**Proyecto:** {proyecto} · **Versión:** v1 · **Fecha:** {dt.date.today().isoformat()} · **Responsable:** [ ]"
    if "**Proyecto:** [ ]" in txt:
        txt = re.sub(r"^\*\*Proyecto:\*\* \[ \].*$", cabecera, txt, count=1, flags=re.M)
    else:
        primera, _, resto = txt.partition("\n")
        txt = f"{primera}\n\n{cabecera}\n{resto}"
    escribir_atomico(dst, txt)
    print(f"Creado {dst}" + ("" if src else " (esqueleto desde el catálogo)"))


def siguiente_id(base, reg):
    reg = reg.replace(".csv", "")
    pref = PREFIJOS.get(reg, reg[:3].upper())
    path = reg_path(base, reg)
    mx = 0
    if os.path.exists(path):
        _, rows, _ = leer_seguro(path)
        for row in rows:
            m = re.search(r"(\d+)$", row[0].strip()) if row else None
            if m:
                mx = max(mx, int(m.group(1)))
    return f"{pref}-{mx + 1:03d}"


def cmd_id(a):
    print(siguiente_id(a.dir, a.registro))


def cmd_add(a):
    requiere_expediente(a.dir)
    reg = a.registro.replace(".csv", "")
    path = asegurar_registro(a.dir, reg)
    header, rows, err = leer_seguro(path)
    if err:
        sys.exit(f"No pude leer {path} ({err}). Corre `expediente.py validar` y repáralo antes de agregar filas.")
    valores = {}
    for kv in a.campos:
        if "=" not in kv:
            sys.exit(f"Formato inválido '{kv}': usa campo=valor")
        k, v = kv.split("=", 1)
        k = k.strip()
        if k not in header:
            sys.exit(f"Campo '{k}' no existe en {reg}. Columnas: {', '.join(header)}")
        valores[k] = v.strip()
    faltan = [c for c in OBLIGATORIOS.get(reg, []) if c in header and not valores.get(c)]
    if faltan and not a.forzar:
        sys.exit(f"Faltan campos obligatorios en {reg}: {', '.join(faltan)}. "
                 "Complétalos (o usa --forzar si de verdad no aplica).")
    for col in header:
        if col in COLS_FECHA and valores.get(col) and not fecha_iso(valores[col]):
            sys.exit(f"{col}='{valores[col]}' no es una fecha AAAA-MM-DD.")
    if reg == "decisiones" and valores.get("decision") and valores["decision"].lower() not in DECISIONES_VALIDAS:
        sys.exit(f"decision='{valores['decision']}' no es válida. Usa Go, Hold, Recycle, Kill o no aplica.")
    idcol = header[0]
    if not valores.get(idcol) and idcol.endswith("id"):
        valores[idcol] = siguiente_id(a.dir, reg)
    if valores.get(idcol) and valores[idcol] in {r[0] for r in rows if r}:
        sys.exit(f"{idcol}={valores[idcol]} ya existe en {reg}.")
    hoy = dt.date.today().isoformat()
    for col in ("fecha", "fecha_consulta"):
        if col in header and not valores.get(col):
            valores[col] = hoy
    if "estado" in header and not valores.get("estado"):
        valores["estado"] = "confirmado" if a.confirmado else "propuesta-agente"
    fila = [valores.get(c, "") for c in header]
    escribir_atomico(path, csv_texto(header, rows + [fila]), bom=tiene_bom(path))
    print(valores.get(idcol) or "(fila agregada)")
    for col, v in valores.items():
        destino = REFERENCIAS.get(col)
        if not destino or col == idcol or not v:
            continue
        existentes = ids_de(a.dir, destino)
        for ref in re.split(r"[;,\s]+", v):
            if re.fullmatch(r"[A-Z]+-\d+", ref) and ref not in existentes:
                print(f"AVISO: {col}={ref} no existe en {destino}.csv "
                      f"(IDs actuales: {', '.join(sorted(existentes)) or 'ninguno'})", file=sys.stderr)
    pii = buscar_pii(list(valores.values()))
    if pii:
        print(f"AVISO privacidad: la fila parece contener {', '.join(pii)}. Anonimiza (ENT-00X, rol) "
              "o usa ingesta.py antes de guardar notas.", file=sys.stderr)


PII = {"un correo": r"[\w.+-]+@[\w-]+\.[\w.]+",
       "un teléfono": r"(?<![\d-])(\+?56[\s.-]?)?9[\s.-]?\d{4}[\s.-]?\d{4}(?![\d-])",
       "un RUT": r"(?<![\d-])\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b"}


def buscar_pii(textos):
    """Revisa cada campo por separado (unir campos produce falsos positivos)."""
    if isinstance(textos, str):
        textos = [textos]
    return [k for k, p in PII.items() if any(re.search(p, t or "") for t in textos)]


def validar(base):
    """Devuelve (errores, avisos) sobre los registros del expediente."""
    errores, avisos = [], []
    rdir = os.path.join(exp_dir(base), "registros")
    if not os.path.isdir(rdir):
        return errores, avisos
    ids = {}
    datos = {}
    for f in sorted(os.listdir(rdir)):
        if not f.endswith(".csv"):
            continue
        reg = f[:-4]
        path = os.path.join(rdir, f)
        if os.path.getsize(path) == 0:
            errores.append(f"{reg}: archivo vacío (sin encabezado) → expediente.py migrar lo repara")
            continue
        h, rows, err = leer_seguro(path)
        if err:
            errores.append(f"{reg}: ilegible ({err}); revisa la codificación (debe ser UTF-8)")
            continue
        esq = esquema(reg)
        if esq is None:
            avisos.append(f"{reg}: no es un registro del pack (se ignora)")
            continue
        faltan = [c for c in esq if c not in h]
        sobran = [c for c in h if c not in esq]
        if faltan:
            errores.append(f"{reg}: faltan columnas {', '.join(faltan)} → expediente.py migrar")
        if sobran:
            avisos.append(f"{reg}: columnas extra {', '.join(sobran)} (se conservan)")
        vistos = set()
        for n, r in enumerate(rows, start=2):
            if len(r) != len(h):
                errores.append(f"{reg} línea {n}: {len(r)} celdas, se esperaban {len(h)} (¿coma sin comillas?)")
            d = dict(zip(h, r + [""] * (len(h) - len(r))))
            rid = r[0].strip() if r else ""
            if not rid:
                errores.append(f"{reg} línea {n}: sin ID")
            elif rid in vistos:
                errores.append(f"{reg} línea {n}: ID duplicado {rid}")
            vistos.add(rid)
            for c, v in d.items():
                if not v.strip():
                    continue
                if c in COLS_FECHA and not fecha_iso(v):
                    errores.append(f"{reg} {rid}: {c}='{v}' no es AAAA-MM-DD")
                if (c.endswith("_CLP") or c in ("n", "probabilidad_interna") or c.startswith("clientes_")) and not es_numero(v):
                    errores.append(f"{reg} {rid}: {c}='{v}' no es un número")
            if reg in ("evidencias", "hipotesis") and d.get("estado") and d["estado"].lower() not in ESTADOS_DATO:
                avisos.append(f"{reg} {rid}: estado '{d['estado']}' no es estándar (propuesta-agente, confirmado, descartado…)")
            if reg == "decisiones" and d.get("decision") and d["decision"].lower() not in DECISIONES_VALIDAS:
                errores.append(f"decisiones {rid}: decision '{d['decision']}' no es Go/Hold/Recycle/Kill/no aplica")
            for c in OBLIGATORIOS.get(reg, []):
                if c in d and not d[c].strip():
                    avisos.append(f"{reg} {rid}: falta {c}")
            pii = buscar_pii(list(d.values()))
            if pii:
                avisos.append(f"{reg} {rid}: posible dato personal ({', '.join(pii)})")
        ids[reg] = vistos
        datos[reg] = (h, rows)
    for reg, (h, rows) in datos.items():
        for r in rows:
            d = dict(zip(h, r))
            for c, destino in REFERENCIAS.items():
                if c not in d or c == h[0] or not d[c].strip():
                    continue
                for ref in re.split(r"[;,\s]+", d[c]):
                    if re.fullmatch(r"[A-Z]+-\d+", ref) and ref not in ids.get(destino, set()):
                        errores.append(f"{reg} {r[0]}: {c}={ref} no existe en {destino}")
    return errores, avisos


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
    rdir = os.path.join(exp_dir(a.dir), "registros")
    os.makedirs(rdir, exist_ok=True)
    cambios = 0
    for f in sorted(os.listdir(rdir)):
        if not f.endswith(".csv"):
            continue
        reg, path = f[:-4], os.path.join(rdir, f)
        esq = esquema(reg)
        if esq is None:
            continue
        if os.path.getsize(path) == 0:
            escribir_atomico(path, csv_texto(esq, []), bom=True)
            print(f"{reg}: encabezado restaurado")
            cambios += 1
            continue
        h, rows, err = leer_seguro(path)
        if err:
            print(f"{reg}: no se pudo leer ({err}); no se tocó. Revisa la codificación a mano.")
            continue
        faltan = [c for c in esq if c not in h]
        if not faltan:
            continue
        shutil.copy2(path, path + f".bak-{dt.date.today().isoformat()}")
        nuevo_h = esq + [c for c in h if c not in esq]
        nuevas = []
        for r in rows:
            d = dict(zip(h, r + [""] * (len(h) - len(r))))
            nuevas.append([d.get(c, "") for c in nuevo_h])
        escribir_atomico(path, csv_texto(nuevo_h, nuevas), bom=True)
        print(f"{reg}: agregadas columnas {', '.join(faltan)} (respaldo .bak)")
        cambios += 1
    gi = os.path.join(exp_dir(a.dir), ".gitignore")
    if not os.path.exists(gi):
        escribir_atomico(gi, GITIGNORE_EXPEDIENTE)
        print("Agregado expediente/.gitignore (privacidad)")
        cambios += 1
    antes = (leer_manifest(a.dir) or {}).get("schema_version", 1)
    escribir_manifest(a.dir)
    print(f"Esquema v{antes} → v{SCHEMA_VERSION}. {cambios} cambio(s).")


def cmd_ver(a):
    path = reg_path(a.dir, a.registro)
    if not os.path.exists(path):
        print(f"(sin registro {a.registro} todavía)")
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
        r = r + [""] * (len(header) - len(r))
        print("| " + " | ".join(corta(r[i].replace("|", "/").replace("\n", " ")) for i in idx) + " |")
    print(f"\n{len(rows)} fila(s)")


def cmd_exportar(a):
    requiere_expediente(a.dir)
    rdir = os.path.join(exp_dir(a.dir), "registros")
    out = os.path.join(exp_dir(a.dir), "entregables", "excel")
    regs = sorted(f[:-4] for f in os.listdir(rdir) if f.endswith(".csv")) if a.registro == "todos" else [a.registro]
    for r in regs:
        header, rows, err = leer_seguro(reg_path(a.dir, r))
        if err:
            print(f"Saltado {r}: {err}")
            continue
        escribir_atomico(os.path.join(out, r + ".csv"), csv_texto(header, rows, delimiter=";"), bom=True)
    print(f"Exportado(s) {len(regs)} registro(s) con ';' y UTF-8 con BOM a {out} (se abren bien en Excel en español)")


def cmd_modelo(a):
    requiere_expediente(a.dir)
    dst = os.path.join(exp_dir(a.dir), "entregables", "modelo_financiero.xlsx")
    if os.path.exists(dst):
        print(f"Ya existe {dst}")
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(os.path.join(ASSETS, "modelo_financiero.xlsx"), dst)
    print(f"Copiado {dst} (escenario hipotético: reemplaza los supuestos con `modelo_xlsx.py set`)")


def leer_estado(base):
    est = os.path.join(exp_dir(base), "00_estado.md")
    return open(est, encoding="utf-8").read() if os.path.exists(est) else ""


def acciones(txt, hoy):
    pend, vencidas = [], []
    for l in seccion(txt, "Próximas acciones").splitlines():
        if not l.startswith("|") or re.match(r"^\|\s*(#|-)", l):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) < 4 or not cells[1]:
            continue
        estado = cells[5].lower() if len(cells) > 5 else ""
        if estado in ("hecho", "hecha", "cerrada", "cerrado", "ok", "✓"):
            continue
        m = re.search(r"\d{4}-\d{2}-\d{2}", cells[3])
        venc = dt.date.fromisoformat(m.group(0)) if m else None
        (vencidas if venc and venc < hoy else pend).append((cells[1], cells[2], cells[3]))
    return pend, vencidas


def hipotesis_estancadas(base, hoy, dias=14):
    """Hipótesis no descartadas sin experimento asociado y con más de `dias` desde su evidencia o creación."""
    h_path, x_path = reg_path(base, "hipotesis"), reg_path(base, "experimentos")
    if not os.path.exists(h_path):
        return []
    h, rows, err = leer_seguro(h_path)
    if err:
        return []
    con_exp = set()
    if os.path.exists(x_path):
        xh, xr, _ = leer_seguro(x_path)
        con_exp = {dict(zip(xh, r)).get("hypothesis_id", "") for r in xr}
    ev_fecha = {}
    ep = reg_path(base, "evidencias")
    if os.path.exists(ep):
        eh, er, _ = leer_seguro(ep)
        for r in er:
            d = dict(zip(eh, r))
            if fecha_iso(d.get("fecha", "")):
                f = dt.date.fromisoformat(d["fecha"][:10])
                ev_fecha[d.get("hypothesis_id", "")] = max(ev_fecha.get(d.get("hypothesis_id", ""), f), f)
    creado = (leer_manifest(base) or {}).get("creado")
    base_fecha = dt.date.fromisoformat(creado) if creado and fecha_iso(creado) else hoy
    out = []
    for r in rows:
        d = dict(zip(h, r))
        hid = d.get(h[0], "")
        if d.get("estado", "").lower() in ("descartado", "obsoleto") or hid in con_exp or d.get("experiment_id"):
            continue
        ref = ev_fecha.get(hid, base_fecha)
        if (hoy - ref).days > dias:
            out.append((hid, d.get("enunciado_refutable", "")[:90], (hoy - ref).days))
    return out


def cmd_estado(a):
    e = exp_dir(a.dir)
    txt = leer_estado(a.dir)
    if not txt:
        print("SIN_EXPEDIENTE: no hay expediente en esta carpeta.")
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
    gate_actual = None
    if foco:
        print("## Foco actual\n" + foco + "\n")
        mm = re.search(r"Gate actual:\*\*\s*(G\d)", foco)
        gate_actual = mm.group(1) if mm else None
    campo = seccion(txt, "Trabajo de campo pendiente")
    if campo and re.search(r":\*\*\s*\S", campo):
        print("## Trabajo de campo pendiente\n" + campo + "\n")
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
    rdir = os.path.join(e, "registros")
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
            cuentas.append(f"{f[:-4]}={len(rows)}" + (f" ({prop} por confirmar)" if prop else ""))
        print("## Registros\n" + ", ".join(cuentas) + "\n")
        dec = os.path.join(rdir, "decisiones.csv")
        if os.path.exists(dec):
            h, rows, err = leer_seguro(dec)
            ult = {}
            for r in rows if not err else []:
                d = dict(zip(h, r))
                ult[d.get("gate", "?")] = d
            if ult:
                print("## Última decisión por gate")
                for g, d in sorted(ult.items()):
                    print(f"- {g}: {d.get('decision', '')} ({d.get('fecha', '')}) — {d.get('justificacion', '')[:120]}")
                print()
    ddir = os.path.join(e, "documentos")
    if os.path.isdir(ddir) and os.listdir(ddir):
        print("## Documentos\n" + ", ".join(sorted(os.listdir(ddir))) + "\n")
    inv = os.path.join(e, "investigacion")
    if os.path.isdir(inv):
        n = sum(len([f for f in fs if f.endswith(".md")]) for _, _, fs in os.walk(inv))
        if n:
            print(f"## Investigación guardada\n{n} archivos .md en investigacion/\n")
    herr = seccion(txt, "Herramientas")
    if herr:
        print("## Herramientas\n" + herr + "\n")
    if gate_actual in SIGUIENTE:
        print(f"## Siguiente paso orientativo (plan 90 días, {gate_actual})\n{SIGUIENTE[gate_actual]}")


def filas(base, reg):
    p = reg_path(base, reg)
    if not os.path.exists(p):
        return []
    h, rows, err = leer_seguro(p)
    return [] if err else [dict(zip(h, r + [""] * (len(h) - len(r)))) for r in rows]


def cmd_informe(a):
    requiere_expediente(a.dir)
    hoy = dt.date.today()
    txt = leer_estado(a.dir)
    proyecto = nombre_proyecto(a.dir)
    out = []
    if a.tipo == "semanal":
        desde = hoy - dt.timedelta(days=a.dias)
        out.append(f"# Reporte semanal — {proyecto}\n\n{desde.isoformat()} a {hoy.isoformat()} · generado desde el expediente\n")
        foco = seccion(txt, "Foco actual")
        if foco:
            out.append("## Foco\n" + foco + "\n")
        nuevos = []
        for reg in registros_disponibles():
            for d in filas(a.dir, reg):
                f = d.get("fecha") or d.get("fecha_consulta") or d.get("inicio") or ""
                if fecha_iso(f) and dt.date.fromisoformat(f[:10]) >= desde:
                    nuevos.append((reg, list(d.values())[0], f[:10]))
        out.append("## Avance de la semana")
        if nuevos:
            por = {}
            for reg, _, _ in nuevos:
                por[reg] = por.get(reg, 0) + 1
            out.append(", ".join(f"{k}: +{v}" for k, v in sorted(por.items())) + "\n")
        else:
            out.append("Sin registros nuevos esta semana.\n")
        ents = filas(a.dir, "entrevistas")
        pipe = filas(a.dir, "cuentas_y_pipeline")
        pils = filas(a.dir, "pilotos")
        out.append("## Embudo\n| Entrevistas | Cuentas en pipeline | Pilotos |\n|---|---|---|\n"
                   f"| {len(ents)} | {len(pipe)} | {len(pils)} |\n")
        dec = [d for d in filas(a.dir, "decisiones") if fecha_iso(d.get("fecha", "")) and d["fecha"][:10] >= desde.isoformat()]
        if dec:
            out.append("## Decisiones\n" + "\n".join(f"- {d.get('gate')}: **{d.get('decision')}** — {d.get('justificacion', '')[:140]}" for d in dec) + "\n")
        pend, venc = acciones(txt, hoy)
        est = hipotesis_estancadas(a.dir, hoy)
        riesgos = [d for d in filas(a.dir, "riesgos") if d.get("estado", "").lower() not in ("cerrado", "mitigado")]
        out.append("## Semáforo")
        out.append(f"- {'🔴' if venc else '🟢'} Acciones vencidas: {len(venc)}")
        out.append(f"- {'🟡' if est else '🟢'} Hipótesis estancadas (>14 días): {len(est)}")
        out.append(f"- {'🟡' if riesgos else '🟢'} Riesgos abiertos: {len(riesgos)}")
        kpis = filas(a.dir, "indicadores")
        if kpis:
            out.append("\n## Indicadores\n| KPI | Línea base | Meta |\n|---|---|---|")
            out += [f"| {k.get('nombre')} | {k.get('baseline')} | {k.get('meta')} |" for k in kpis]
        out.append("\n## Próxima semana")
        out += [f"- {acc} · {resp} · {f}" for acc, resp, f in (venc + pend)[:6]] or ["- (sin acciones registradas)"]
        nombre = f"reporte_semanal_{hoy.isoformat()}.md"
    elif a.tipo == "onepager":
        perfil = seccion(txt, "Perfil")
        frase = re.search(r"Una frase[^:]*:\*\*\s*(.+)", perfil)
        out.append(f"# {proyecto} — one-pager\n\n> Borrador generado desde el expediente el {hoy.isoformat()}. "
                   "Lo marcado [SIN RESPALDO] no tiene evidencia registrada: respáldalo o quítalo antes de compartir.\n")
        out.append("## Problema\n" + (frase.group(1).strip() if frase else "[SIN RESPALDO]") + "\n")
        evs = [d for d in filas(a.dir, "evidencias") if d.get("estado") == "confirmado"]
        out.append("## Evidencia confirmada")
        out += [f"- {d.get('afirmacion')} ({d.get('tipo')}, n={d.get('n') or '?'}; {d.get('evidence_id')})" for d in evs[:8]] or ["- [SIN RESPALDO] aún no hay evidencia confirmada"]
        comp = filas(a.dir, "competencia")
        out.append("\n## Alternativas y competencia")
        out += [f"- {c.get('alternativa')} ({c.get('tipo')}): {c.get('limitacion')}" for c in comp[:5]] or ["- [SIN RESPALDO] sin benchmark registrado"]
        ents, pils = filas(a.dir, "entrevistas"), filas(a.dir, "pilotos")
        out.append(f"\n## Tracción\n- Entrevistas registradas: {len(ents)}\n- Pilotos: {len(pils)}")
        kpis = filas(a.dir, "indicadores")
        out += [f"- {k.get('nombre')}: {k.get('baseline')} (meta {k.get('meta')})" for k in kpis[:5]]
        dec = filas(a.dir, "decisiones")
        out.append("\n## Dónde estamos")
        out += [f"- {d.get('gate')}: {d.get('decision')} — {d.get('justificacion', '')[:120]}" for d in dec[-3:]] or ["- Sin decisiones de gate registradas"]
        equipo = re.search(r"Equipo y dedicación:\*\*\s*(.*)", perfil)
        out.append("\n## Equipo\n" + ((equipo.group(1).strip() or "[SIN RESPALDO]") if equipo else "[SIN RESPALDO]"))
        objetivo = re.search(r"Objetivo próximo y fecha límite:\*\*\s*(.*)", perfil)
        out.append("\n## Qué pedimos / próximo hito\n" + ((objetivo.group(1).strip() or "[completar]") if objetivo else "[completar]"))
        nombre = f"one_pager_{hoy.isoformat()}.md"
    if a.tipo == "deck":
        dst = os.path.join(exp_dir(a.dir), "entregables", f"deck_{hoy.isoformat()}.md")
        escribir_atomico(dst, deck_md(a.dir))
        print(f"Creado {dst} (Markdown para Marp: marp {os.path.basename(dst)} --pptx). Revisa cada [FALTA EVIDENCIA].")
        return
    dst = os.path.join(exp_dir(a.dir), "entregables", nombre)
    escribir_atomico(dst, "\n".join(out) + "\n")
    print(f"Creado {dst}")


CATALOGOS = {"fuentes": "biblioteca/fuentes.csv", "libros": "biblioteca/libros.csv", "mentores": "biblioteca/mentores.csv",
             "charlas": "biblioteca/charlas_y_cursos.csv", "casos": "casos/casos.csv", "workshops": "operacion/workshops.csv",
             "curriculo": "operacion/curriculo_360h.csv", "cifras": "investigaciones/afirmaciones_y_cifras.csv"}


def cmd_biblioteca(a):
    tipos = [a.tipo] if a.tipo else list(CATALOGOS)
    pat = re.compile(re.escape(a.texto), re.I) if a.texto else None
    n = 0
    for t in tipos:
        p = os.path.join(REFS, CATALOGOS[t])
        if not os.path.exists(p):
            continue
        h, rows = leer(p)
        for r in rows:
            linea = " · ".join(c for c in r if c)
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


def cmd_plantillas(a):
    h, rows = leer(os.path.join(PLANTILLAS, "catalogo_plantillas.csv"))
    pat = re.compile(re.escape(a.buscar), re.I) if a.buscar else None
    n = 0
    for r in rows:
        d = dict(zip(h, r))
        if a.troncales and d.get("troncal") != "si":
            continue
        if a.dominio and d.get("dominio") != a.dominio:
            continue
        if pat and not pat.search(" ".join(r)):
            continue
        marca = "★ " if d.get("troncal") == "si" else "  "
        print(f"{marca}{d['id']} [{d['dominio']}] {d['nombre']} — {d['uso'][:110]}")
        n += 1
    print(f"\n{n} plantilla(s). ★ = troncal, con estructura y ejemplos; las demás se crean como esqueleto con `doc`.")


def tokens(texto):
    s = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return [t for t in re.findall(r"[a-z0-9]{3,}", s) if t not in STOP]


STOP = set("que los las del con por para una uno como mas pero sus este esta son ser hay sin sobre entre cuando donde cual "
           "the and for you".split())


def corpus(en):
    roots = {"plantillas": [PLANTILLAS], "manual": [REFS], "todo": [PLANTILLAS, REFS]}[en]
    for root in roots:
        for dp, _, fs in os.walk(root):
            for f in sorted(fs):
                if f.endswith((".md", ".csv")):
                    p = os.path.join(dp, f)
                    yield p, open(p, encoding="utf-8-sig", errors="replace").read()


def cmd_buscar(a):
    """Ranking BM25 de archivos de la skill para una consulta; muestra las líneas más pertinentes."""
    q = tokens(a.texto + (" " + a.gate if a.gate else ""))
    if not q:
        sys.exit("Consulta vacía: usa palabras de 3 letras o más.")
    docs = [(p, t, tokens(t)) for p, t in corpus(a.en)]
    N = len(docs)
    avg = sum(len(d[2]) for d in docs) / max(N, 1)
    df = {t: sum(1 for d in docs if t in set(d[2])) for t in set(q)}
    k1, b = 1.4, 0.75
    puntajes = []
    for p, t, toks in docs:
        tf = {}
        for x in toks:
            if x in df:
                tf[x] = tf.get(x, 0) + 1
        s = 0.0
        for term in set(q):
            if term in tf:
                idf = math.log(1 + (N - df[term] + 0.5) / (df[term] + 0.5))
                s += idf * tf[term] * (k1 + 1) / (tf[term] + k1 * (1 - b + b * len(toks) / avg))
        if s > 0:
            puntajes.append((s, p, t))
    puntajes.sort(reverse=True)
    if not puntajes:
        print("Sin resultados.")
        return
    for s, p, t in puntajes[:a.max]:
        mejores = sorted(((sum(1 for x in tokens(l) if x in df), i, l.strip()) for i, l in enumerate(t.splitlines(), 1) if l.strip()),
                         reverse=True)[:2]
        print(f"{os.path.relpath(p, SKILL_DIR).replace(os.sep, '/')}  (puntaje {s:.1f})")
        for c, i, l in mejores:
            if c:
                print(f"    {i}: {l[:180]}")


# ---------------------------------------------------------------- continuidad entre sesiones
def umbrales_data():
    return json.load(open(os.path.join(ASSETS, "umbrales_gates.json"), encoding="utf-8"))


def gate_actual_de(base):
    mm = re.search(r"Gate actual:\*\*\s*(G\d)", seccion(leer_estado(base), "Foco actual"))
    return mm.group(1) if mm else None


def lineas_umbral(gate, track):
    g = umbrales_data()["gates"].get(gate)
    if not g:
        return []
    return list(g.get("comun", [])) + list(g.get("por_track", {}).get(track or "", []))


def cmd_umbrales(a):
    data = umbrales_data()
    track = a.track or ((leer_manifest(a.dir) or {}).get("track") if os.path.isdir(exp_dir(a.dir)) else None)
    gates = [a.gate.upper()] if a.gate else ([gate_actual_de(a.dir)] if os.path.isdir(exp_dir(a.dir)) and gate_actual_de(a.dir) else list(data["gates"]))
    print(f"Track: {track or 'sin definir (usa --track o init --track)'} · referencia verificada {data.get('_verificado')}\n")
    for g in gates:
        if g not in data["gates"]:
            sys.exit(f"Gate desconocido {g}. Usa G0–G9.")
        print(f"## {g} — {data['gates'][g]['pregunta']}")
        for linea in lineas_umbral(g, track):
            print(f"- {linea}")
        print()
    print("Son umbrales de referencia para fijar el criterio ANTES de salir a terreno; otro umbral vale si se justifica antes de ver los datos.")


def cmd_resumen(a):
    """Resumen compacto (≈600 tokens) para retomar en otra conversación o en otro cliente."""
    requiere_expediente(a.dir)
    hoy = dt.date.today()
    txt = leer_estado(a.dir)
    m = leer_manifest(a.dir) or {}
    foco = seccion(txt, "Foco actual")

    def campo(et):
        mm = re.search(re.escape(et) + r":\*\*\s*(.*)", txt)
        return mm.group(1).strip() if mm else ""
    gate = gate_actual_de(a.dir) or "?"
    out = [f"# Resumen para retomar — {nombre_proyecto(a.dir)} — {hoy.isoformat()}",
           f"Modo {campo('Modo de trabajo') or '?'} · nivel {m.get('nivel', '?')} · track {m.get('track') or '?'} · gate actual {gate}",
           f"Problema: {campo('Una frase (sin nombrar la solución)')[:220] or '[sin definir]'}",
           f"Objetivo: {campo('Objetivo próximo y fecha límite')[:160] or '[sin definir]'}"]
    hr = re.search(r"Hipótesis más riesgosa:\*\*\s*(.*)", foco)
    if hr and hr.group(1).strip():
        out.append(f"Hipótesis más riesgosa: {hr.group(1).strip()[:160]}")
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


LEEME_ZIP = """Expediente de {proyecto} empaquetado el {fecha} con la skill startup-engineering-chile.

Para retomar en otra sesión (por ejemplo en Claude.ai, donde los archivos se borran entre conversaciones):
1. Sube este ZIP al iniciar la conversación.
2. Pide: "retomemos mi proyecto con este expediente".
   La skill corre: expediente.py restaurar <zip> --dir <carpeta>

Contiene entrevistas y datos del proyecto: guárdalo en un lugar privado.
"""


def cmd_empaquetar(a):
    requiere_expediente(a.dir)
    e = exp_dir(a.dir)
    hoy = dt.date.today().isoformat()
    proyecto = nombre_proyecto(a.dir) or "proyecto"
    salida = os.path.abspath(a.salida or a.dir)
    os.makedirs(salida, exist_ok=True)
    dst = os.path.join(salida, f"expediente_{slug(proyecto) or 'proyecto'}_{hoy}.zip")
    escribir_manifest(a.dir, empaquetado=hoy)
    fd, tmp = tempfile.mkstemp(dir=salida, suffix=".tmp")
    os.close(fd)
    n = 0
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(e):
                dirs[:] = sorted(d for d in dirs if d != "__pycache__")
                for f in sorted(files):
                    if ".bak" in f or f.endswith(".tmp"):
                        continue
                    p = os.path.join(root, f)
                    z.write(p, os.path.relpath(p, os.path.dirname(e)).replace(os.sep, "/"))
                    n += 1
            z.writestr("LEEME.txt", LEEME_ZIP.format(proyecto=proyecto, fecha=hoy))
        os.replace(tmp, dst)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    print(f"Empaquetado {n} archivo(s) en {dst} ({os.path.getsize(dst) // 1024 + 1} KB)")
    print("Entrégaselo al usuario para que lo descargue y lo vuelva a subir en la próxima sesión. Contiene datos privados.")


MAX_ZIP_BYTES = 200 * 1024 * 1024


def cmd_restaurar(a):
    if not zipfile.is_zipfile(a.zip):
        sys.exit(f"{a.zip} no es un ZIP válido.")
    destino = os.path.abspath(a.dir)
    e = exp_dir(a.dir)
    with zipfile.ZipFile(a.zip) as z:
        miembros = [i for i in z.infolist() if i.filename.startswith("expediente/") and not i.is_dir()]
        if not miembros:
            sys.exit("El ZIP no contiene una carpeta expediente/. ¿Es un paquete de `expediente.py empaquetar`?")
        if sum(i.file_size for i in miembros) > MAX_ZIP_BYTES:
            sys.exit("El ZIP descomprimido supera 200 MB; no se restaura.")
        for i in miembros:
            objetivo = os.path.abspath(os.path.join(destino, i.filename))
            if not objetivo.startswith(destino + os.sep):
                sys.exit(f"Ruta insegura en el ZIP: {i.filename}; no se restaura.")
        if os.path.isdir(e):
            if not a.forzar:
                actual = (leer_manifest(a.dir) or {}).get("actualizado", "?")
                sys.exit(f"Ya hay un expediente en {e} (actualizado {actual}). Usa --forzar para reemplazarlo; "
                         "el actual se respalda como expediente.bak-<fecha-hora>.")
            respaldo = e + ".bak-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            shutil.move(e, respaldo)
            print(f"Respaldo del expediente anterior: {respaldo}")
        for i in miembros:
            objetivo = os.path.join(destino, *i.filename.split("/"))
            os.makedirs(os.path.dirname(objetivo), exist_ok=True)
            with z.open(i) as src, open(objetivo, "wb") as out:
                shutil.copyfileobj(src, out)
    m = leer_manifest(a.dir) or {}
    print(f"Restaurado {len(miembros)} archivo(s) en {e} (empaquetado {m.get('empaquetado', '?')}).")
    if m.get("schema_version", 1) < SCHEMA_VERSION:
        print("Esquema antiguo: corre `expediente.py migrar`.")
    errores, avisos = validar(a.dir)
    print(f"Validación: {len(errores)} error(es), {len(avisos)} aviso(s). Sigue con `expediente.py estado`.")


def deck_md(base):
    """Pitch deck en Markdown compatible con Marp, desde el expediente; marca vacíos con [FALTA EVIDENCIA]."""
    F = "[FALTA EVIDENCIA]"
    txt = leer_estado(base)
    perfil = seccion(txt, "Perfil")

    def campo(et):
        mm = re.search(re.escape(et) + r"[^:]*:\*\*\s*(.*)", perfil)
        return (mm.group(1).strip() if mm else "") or F
    evs = [d for d in filas(base, "evidencias") if d.get("estado") == "confirmado"]
    ents = filas(base, "entrevistas")
    comp = filas(base, "competencia")
    pils = filas(base, "pilotos")
    pipe = filas(base, "cuentas_y_pipeline")
    kpis = filas(base, "indicadores")
    precio = ""
    for d in filas(base, "experimentos"):
        if re.search(r"precio|pago|preventa|carta", d.get("metrica", "") + d.get("metodo", ""), re.I) and d.get("resultado"):
            precio = f"{d.get('metrica')}: {d.get('resultado')} (umbral {d.get('umbral')}; {d.get('experiment_id')})"
    modelo = os.path.join(exp_dir(base), "entregables", "modelo_financiero.xlsx")
    sup = {}
    if os.path.exists(modelo):
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import modelo_xlsx
            sup = {s["variable"]: s["valor"] for s in modelo_xlsx.supuestos(modelo, "Supuestos")}
        except Exception:
            sup = {}
    sl = ["---", "marp: true", "paginate: true", "---", "",
          f"# {nombre_proyecto(base)}", f"{campo('Una frase')}", "",
          "> Borrador generado desde el expediente el " + dt.date.today().isoformat() + ". Todo lo marcado " + F + " debe respaldarse o quitarse.",
          "", "---", "", "## El problema", campo("Una frase"), ""]
    sl += [f"- {d.get('afirmacion')} (n={d.get('n') or '?'}; {d.get('evidence_id')})" for d in evs[:3]] or [f"- {F} sin evidencia confirmada del problema"]
    sl += ["", "---", "", "## A quién le pasa", f"- Entrevistas registradas: {len(ents)}"]
    segs = sorted({d.get("segmento", "") for d in ents if d.get("segmento")})
    sl += [f"- Segmentos entrevistados: {', '.join(segs[:4])}" if segs else f"- {F} segmento del cliente"]
    sl += ["", "---", "", "## Cómo lo resuelven hoy"]
    sl += [f"- {c.get('alternativa')} ({c.get('tipo')}): {c.get('limitacion') or F}" for c in comp[:4]] or [f"- {F} alternativas y competencia"]
    sl += ["", "---", "", "## Nuestra propuesta", f"- {F} propuesta de valor con la diferencia demostrada (TPL-049, TPL-031)", "",
           "---", "", "## Modelo de negocio y precio", f"- {precio or F + ' prueba de precio con compromiso'}"]
    if sup.get("Precio mensual"):
        sl.append(f"- Precio supuesto en el modelo: {sup['Precio mensual']} CLP/mes (supuesto, no evidencia)")
    sl += ["", "---", "", "## Tracción", f"- Pilotos: {len(pils)} · Cuentas en pipeline: {len(pipe)}"]
    sl += [f"- {k.get('nombre')}: {k.get('baseline') or F} → meta {k.get('meta') or F}" for k in kpis[:3]] or [f"- {F} indicadores de uso o venta"]
    sl += ["", "---", "", "## Economía unitaria"]
    if sup:
        for et in ("CAC", "Churn mensual", "Infraestructura variable"):
            if et in sup:
                sl.append(f"- {et}: {sup[et]} (supuesto del modelo; respáldalo con `finanzas.py unit`)")
    else:
        sl.append(f"- {F} unit economics (`finanzas.py unit`)")
    sl += ["", "---", "", "## Equipo", f"- {campo('Equipo y dedicación')}", "", "---", "", "## Qué pedimos",
           f"- {campo('Objetivo próximo y fecha límite')}", f"- {F} monto, uso de fondos e hito que se alcanza", ""]
    return "\n".join(sl) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("doctor"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_doctor)
    p = sp.add_parser("init"); p.add_argument("--dir", default="."); p.add_argument("--proyecto", required=True)
    p.add_argument("--modo", default="empezar", choices=["empezar", "pulir", "complementar"])
    p.add_argument("--nivel", default="completo", choices=list(NIVELES))
    p.add_argument("--track", choices=list(umbrales_data()["tracks"])); p.set_defaults(f=cmd_init)
    p = sp.add_parser("estado"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_estado)
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
    p = sp.add_parser("id"); p.add_argument("registro"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_id)
    p = sp.add_parser("exportar"); p.add_argument("registro", nargs="?", default="todos"); p.add_argument("--dir", default=".")
    p.set_defaults(f=cmd_exportar)
    p = sp.add_parser("informe"); p.add_argument("tipo", choices=["semanal", "onepager", "deck"]); p.add_argument("--dir", default=".")
    p.add_argument("--dias", type=int, default=7); p.set_defaults(f=cmd_informe)
    p = sp.add_parser("modelo"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_modelo)
    p = sp.add_parser("buscar"); p.add_argument("texto"); p.add_argument("--en", default="todo", choices=["plantillas", "manual", "todo"])
    p.add_argument("--gate"); p.add_argument("--max", type=int, default=5); p.set_defaults(f=cmd_buscar)
    p = sp.add_parser("umbrales"); p.add_argument("--dir", default="."); p.add_argument("--gate")
    p.add_argument("--track", choices=list(umbrales_data()["tracks"])); p.set_defaults(f=cmd_umbrales)
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
