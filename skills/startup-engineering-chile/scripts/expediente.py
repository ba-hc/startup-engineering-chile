#!/usr/bin/env python3
"""Gestiona el expediente de una startup (núcleo de evidencia del pack Startup Engineering Chile).

Uso (--dir es la carpeta del proyecto; el expediente vive en RUTA/expediente/):
  expediente.py init    --dir RUTA --proyecto "Nombre" [--modo empezar|pulir|complementar]
  expediente.py estado  --dir RUTA                 # ruta por gates, campo pendiente, acciones vencidas
  expediente.py add     REGISTRO campo=valor ... --dir RUTA [--confirmado]
                                                   # agrega una fila (ID y fecha automáticos)
  expediente.py ver     REGISTRO --dir RUTA [--ultimos N]   # tabla markdown para mostrar al usuario
  expediente.py doc     TPL-031 --dir RUTA         # copia una plantilla a documentos/ (no sobrescribe)
  expediente.py id      REGISTRO --dir RUTA        # siguiente ID libre (p. ej. EV-004)
  expediente.py exportar [REGISTRO|todos] --dir RUTA   # copia con ';' para Excel en español
  expediente.py modelo  --dir RUTA                 # copia el modelo financiero de ejemplo
  expediente.py buscar  "texto" [--en plantillas|manual|todo]

Solo biblioteca estándar de Python.
"""
import argparse
import csv
import datetime as dt
import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL_DIR, "assets")
REFS = os.path.join(SKILL_DIR, "references")
PLANTILLAS = os.path.join(ASSETS, "plantillas")
REGISTROS = os.path.join(ASSETS, "registros")
REGISTROS_INICIALES = ["hipotesis", "evidencias", "decisiones"]

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

ESTADO_TPL = """# Expediente: {proyecto}

> Núcleo permanente del proyecto. La skill lo actualiza al cerrar cada bloque.
> Las vistas (pitch, dossier, informe) se generan desde aquí; la presentación no crea evidencia.
> Regla: los campos del perfil solo llevan lo que dijo el usuario. Lo propuesto por el agente se marca "(propuesta, por confirmar)".

## Perfil
- **Proyecto:** {proyecto}
- **Modo de trabajo:** {modo}
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


def exp_dir(base):
    return os.path.join(os.path.abspath(base), "expediente")


def reg_path(base, reg):
    return os.path.join(exp_dir(base), "registros", reg.replace(".csv", "") + ".csv")


def asegurar_registro(base, reg):
    """Crea el registro desde el esquema del pack si aún no existe."""
    reg = reg.replace(".csv", "")
    dst = reg_path(base, reg)
    if not os.path.exists(dst):
        src = os.path.join(REGISTROS, reg + ".csv")
        if not os.path.exists(src):
            disponibles = ", ".join(sorted(f[:-4] for f in os.listdir(REGISTROS)))
            sys.exit(f"Registro desconocido '{reg}'. Disponibles: {disponibles}")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    return dst


def leer(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return [], []
    return rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]


def cmd_init(a):
    e = exp_dir(a.dir)
    for sub in ["registros", "documentos", "entregables", "investigacion"]:
        os.makedirs(os.path.join(e, sub), exist_ok=True)
    for r in REGISTROS_INICIALES:
        asegurar_registro(a.dir, r)
    est = os.path.join(e, "00_estado.md")
    if not os.path.exists(est):
        ruta = "\n".join(f"| {g} {n}: {q} | pendiente | 0 | |" for g, n, q in GATES)
        with open(est, "w", encoding="utf-8") as fh:
            fh.write(ESTADO_TPL.format(proyecto=a.proyecto, modo=a.modo, hoy=dt.date.today().isoformat(), ruta=ruta))
        print(f"Creado {est}")
    else:
        print(f"Ya existía {est} (no se tocó)")
    print(f"Expediente listo en {e}. Los demás registros se crean al usarlos (`add`).")


def template_path(tpl_id):
    tpl_id = tpl_id.upper()
    for root, _, files in os.walk(PLANTILLAS):
        for f in files:
            if f.upper().startswith(tpl_id + "_"):
                return os.path.join(root, f)
    return None


def nombre_proyecto(base):
    est = os.path.join(exp_dir(base), "00_estado.md")
    if os.path.exists(est):
        m = re.search(r"^# Expediente: (.+)$", open(est, encoding="utf-8").read(), re.M)
        if m:
            return m.group(1).strip()
    return ""


def cmd_doc(a):
    src = template_path(a.tpl)
    if not src:
        sys.exit(f"No existe la plantilla {a.tpl}. Revisa assets/plantillas/INDICE.md")
    e = exp_dir(a.dir)
    if not os.path.isdir(e):
        sys.exit("No hay expediente. Ejecuta primero: expediente.py init")
    dst = os.path.join(e, "documentos", os.path.basename(src))
    if os.path.exists(dst):
        print(f"Ya existe: {dst} (edítalo, no se sobrescribe)")
        return
    proyecto = nombre_proyecto(a.dir)
    txt = open(src, encoding="utf-8").read()
    txt = txt.replace("**Proyecto:** [ ]", f"**Proyecto:** {proyecto or '[ ]'}", 1)
    txt = txt.replace("**Versión:** [ ]", "**Versión:** v1", 1)
    txt = txt.replace("**Fecha:** [ ]", f"**Fecha:** {dt.date.today().isoformat()}", 1)
    txt = re.sub(r"`[./]*references/biblioteca/FUENTES\.md`", "la biblioteca de fuentes de la skill", txt)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(txt)
    print(f"Creado {dst}")


PREFIJOS = {"evidencias": "EV", "hipotesis": "H", "experimentos": "EXP", "decisiones": "DEC", "riesgos": "R",
            "competencia": "COMP", "entrevistas": "ENT", "pilotos": "PIL", "cuentas_y_pipeline": "CTA",
            "fuentes_nuevas": "SRC", "indicadores": "KPI", "ip_licencias": "IP", "rendiciones": "GAS",
            "lecciones_mentores": "LEC", "desafios_corporativos": "DES", "corfo_elegibilidad": "REQ", "cohortes": "COH"}


def siguiente_id(base, reg):
    reg = reg.replace(".csv", "")
    pref = PREFIJOS.get(reg, reg[:3].upper())
    path = reg_path(base, reg)
    mx = 0
    if os.path.exists(path):
        _, rows = leer(path)
        for row in rows:
            m = re.search(r"(\d+)$", row[0].strip())
            if m:
                mx = max(mx, int(m.group(1)))
    return f"{pref}-{mx + 1:03d}"


def cmd_id(a):
    print(siguiente_id(a.dir, a.registro))


def cmd_add(a):
    if not os.path.isdir(exp_dir(a.dir)):
        sys.exit("No hay expediente. Ejecuta primero: expediente.py init")
    path = asegurar_registro(a.dir, a.registro)
    header, _ = leer(path)
    valores = {}
    for kv in a.campos:
        if "=" not in kv:
            sys.exit(f"Formato inválido '{kv}': usa campo=valor")
        k, v = kv.split("=", 1)
        k = k.strip()
        if k not in header:
            sys.exit(f"Campo '{k}' no existe en {a.registro}. Columnas: {', '.join(header)}")
        valores[k] = v.strip()
    idcol = header[0]
    if not valores.get(idcol) and idcol.endswith("id"):
        valores[idcol] = siguiente_id(a.dir, a.registro)
    hoy = dt.date.today().isoformat()
    for col in ("fecha", "fecha_consulta"):
        if col in header and not valores.get(col):
            valores[col] = hoy
    if "estado" in header and not valores.get("estado"):
        valores["estado"] = "confirmado" if a.confirmado else "propuesta-agente"
    fila = [valores.get(c, "") for c in header]
    with open(path, "a", encoding="utf-8", newline="") as fh:
        csv.writer(fh, quoting=csv.QUOTE_MINIMAL).writerow(fila)
    print(valores[idcol] or "(fila agregada)")
    # Aviso (no bloquea) si la fila referencia IDs que no existen en su registro.
    for col, v in valores.items():
        destino = REFERENCIAS.get(col)
        if not destino or col == idcol or not v:
            continue
        existentes = ids_de(a.dir, destino)
        for ref in re.split(r"[;,\s]+", v):
            if re.fullmatch(r"[A-Z]+-\d+", ref) and ref not in existentes:
                print(f"AVISO: {col}={ref} no existe en {destino}.csv "
                      f"(IDs actuales: {', '.join(sorted(existentes)) or 'ninguno'})", file=sys.stderr)


REFERENCIAS = {"hypothesis_id": "hipotesis", "experiment_id": "experimentos", "evidence_id": "evidencias",
               "evidence_ids": "evidencias"}


def ids_de(base, reg):
    path = reg_path(base, reg)
    if not os.path.exists(path):
        return set()
    _, rows = leer(path)
    return {r[0].strip() for r in rows if r and r[0].strip()}


def cmd_ver(a):
    path = reg_path(a.dir, a.registro)
    if not os.path.exists(path):
        print(f"(sin registro {a.registro} todavía)")
        return
    header, rows = leer(path)
    if a.ultimos:
        rows = rows[-a.ultimos:]
    cols = a.columnas.split(",") if a.columnas else header
    idx = [header.index(c) for c in cols if c in header]
    corta = lambda s: (s[:a.ancho - 1] + "…") if len(s) > a.ancho else s
    print("| " + " | ".join(header[i] for i in idx) + " |")
    print("|" + "---|" * len(idx))
    for r in rows:
        r = r + [""] * (len(header) - len(r))
        print("| " + " | ".join(corta(r[i].replace("|", "/").replace("\n", " ")) for i in idx) + " |")
    print(f"\n{len(rows)} fila(s)")


def cmd_exportar(a):
    rdir = os.path.join(exp_dir(a.dir), "registros")
    out = os.path.join(exp_dir(a.dir), "entregables", "excel")
    os.makedirs(out, exist_ok=True)
    regs = [f[:-4] for f in os.listdir(rdir) if f.endswith(".csv")] if a.registro == "todos" else [a.registro]
    for r in regs:
        header, rows = leer(reg_path(a.dir, r))
        with open(os.path.join(out, r + ".csv"), "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(header)
            w.writerows(rows)
    print(f"Exportado(s) {len(regs)} registro(s) con ';' a {out}")


def cmd_modelo(a):
    dst = os.path.join(exp_dir(a.dir), "entregables", "modelo_financiero.xlsx")
    if os.path.exists(dst):
        print(f"Ya existe {dst}")
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(os.path.join(ASSETS, "modelo_financiero.xlsx"), dst)
    print(f"Copiado {dst} (escenario hipotético: reemplazar con datos propios)")


def seccion(txt, titulo):
    m = re.search(r"^## " + re.escape(titulo) + r"\s*\n(.*?)(?=^#{2,3} |\Z)", txt, re.M | re.S)
    return m.group(1).strip() if m else ""


def cmd_estado(a):
    e = exp_dir(a.dir)
    est = os.path.join(e, "00_estado.md")
    if not os.path.exists(est):
        print("SIN_EXPEDIENTE: no hay expediente en esta carpeta.")
        return
    txt = open(est, encoding="utf-8").read()
    hoy = dt.date.today()
    print(f"# Estado del expediente — {nombre_proyecto(a.dir)} — {hoy.isoformat()}\n")
    ruta = seccion(txt, "Ruta")
    if ruta:
        print("## Ruta\n" + "\n".join(l for l in ruta.splitlines() if l.startswith("|")) + "\n")
    foco = seccion(txt, "Foco actual")
    gate_actual = None
    if foco:
        print("## Foco actual\n" + foco + "\n")
        m = re.search(r"Gate actual:\*\*\s*(G\d)", foco)
        gate_actual = m.group(1) if m else None
    campo = seccion(txt, "Trabajo de campo pendiente")
    if campo and re.search(r":\*\*\s*\S", campo):
        print("## Trabajo de campo pendiente\n" + campo + "\n")
    acciones = seccion(txt, "Próximas acciones")
    pend, vencidas = [], []
    for l in acciones.splitlines():
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
    rdir = os.path.join(e, "registros")
    if os.path.isdir(rdir):
        cuentas = []
        for f in sorted(os.listdir(rdir)):
            if f.endswith(".csv"):
                _, rows = leer(os.path.join(rdir, f))
                prop = 0
                h, _ = leer(os.path.join(rdir, f))
                if "estado" in h:
                    i = h.index("estado")
                    prop = sum(1 for r in rows if len(r) > i and r[i] == "propuesta-agente")
                cuentas.append(f"{f[:-4]}={len(rows)}" + (f" ({prop} por confirmar)" if prop else ""))
        print("## Registros\n" + ", ".join(cuentas) + "\n")
        dec = os.path.join(rdir, "decisiones.csv")
        if os.path.exists(dec):
            h, rows = leer(dec)
            ult = {}
            for r in rows:
                d = dict(zip(h, r))
                ult[d.get("gate", "?")] = d
            if ult:
                print("## Última decisión por gate")
                for g, d in sorted(ult.items()):
                    print(f"- {g}: {d.get('decision','')} ({d.get('fecha','')}) — {d.get('justificacion','')[:120]}")
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


def cmd_buscar(a):
    roots = {"plantillas": [PLANTILLAS], "manual": [REFS], "todo": [PLANTILLAS, REFS]}[a.en]
    pat = re.compile(re.escape(a.texto), re.I)
    hits = 0
    for root in roots:
        for dp, _, fs in os.walk(root):
            for f in fs:
                if not f.endswith((".md", ".csv")):
                    continue
                p = os.path.join(dp, f)
                for i, line in enumerate(open(p, encoding="utf-8-sig", errors="replace"), 1):
                    if pat.search(line):
                        print(f"{os.path.relpath(p, SKILL_DIR)}:{i}: {line.strip()[:200]}")
                        hits += 1
                        if hits >= a.max:
                            return
    if not hits:
        print("Sin resultados.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("--dir", default="."); p.add_argument("--proyecto", required=True)
    p.add_argument("--modo", default="empezar", choices=["empezar", "pulir", "complementar"]); p.set_defaults(f=cmd_init)
    p = sp.add_parser("estado"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_estado)
    p = sp.add_parser("add"); p.add_argument("registro"); p.add_argument("campos", nargs="+")
    p.add_argument("--dir", default="."); p.add_argument("--confirmado", action="store_true"); p.set_defaults(f=cmd_add)
    p = sp.add_parser("ver"); p.add_argument("registro"); p.add_argument("--dir", default=".")
    p.add_argument("--ultimos", type=int); p.add_argument("--columnas"); p.add_argument("--ancho", type=int, default=50)
    p.set_defaults(f=cmd_ver)
    p = sp.add_parser("doc"); p.add_argument("tpl"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_doc)
    p = sp.add_parser("id"); p.add_argument("registro"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_id)
    p = sp.add_parser("exportar"); p.add_argument("registro", nargs="?", default="todos"); p.add_argument("--dir", default=".")
    p.set_defaults(f=cmd_exportar)
    p = sp.add_parser("modelo"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_modelo)
    p = sp.add_parser("buscar"); p.add_argument("texto"); p.add_argument("--en", default="todo", choices=["plantillas", "manual", "todo"])
    p.add_argument("--max", type=int, default=40); p.set_defaults(f=cmd_buscar)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
