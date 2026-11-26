#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Auditoría de coherencia del expediente: contradicciones entre registros y señales de sesgo.

`expediente.py validar` revisa forma (columnas, IDs, fechas). Este script revisa el fondo:
  - lo que dice 00_estado.md contra lo que hay en los registros;
  - decisiones Go sin respaldo o con resultados bajo el umbral;
  - precio del modelo financiero contra el pipeline;
  - hipótesis que llevan semanas abiertas sin experimento;
  - integridad referencial: decisiones sin evidencia (o con IDs que no existen), experimentos vencidos sin cierre,
    entrevistas sin nota anonimizada o con datos personales;
  - números clave de 00_estado.md contra los supuestos de modelo_financiero.xlsx;
  - señales de sesgo: entrevistas complacientes, costo hundido, funciones agregadas antes de validar.

Uso:
  auditar.py --dir RUTA [--dias-hipotesis 30] [--estricto] [--hoy AAAA-MM-DD]

Cada hallazgo es una pregunta para el fundador, no un veredicto. Solo biblioteca estándar (3.8+).
"""
import argparse
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expediente as ex  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

INTENCION = re.compile(r"me interesa|lo comprar[ií]a|pagar[ií]a|lo usar[ií]a|buena idea|me gusta|me encanta|av[ií]same|suena bien|lo recomendar[ií]a", re.I)
COMPROMISO = re.compile(r"preventa|dep[oó]sito|orden de compra|\bOC\b|carta de intenci[oó]n firmada|pag[oó]|firm[oó]|contrato|piloto con datos|reuni[oó]n con (el|la) (gerente|aprobador|jef)", re.I)
FUNCION = re.compile(r"agregar (una )?(funci[oó]n|m[oó]dulo|feature)|nueva funcionalidad|integraci[oó]n con|desarrollar (el|un) m[oó]dulo|app m[oó]vil", re.I)
TRACCION = re.compile(r"clientes?|ventas|tracci[oó]n|MRR|factur", re.I)


def numero(texto):
    """Primer número del texto, con su unidad (%, o vacío). Acepta 1.200.000, 0,25 y 25%."""
    m = re.search(r"(-?\d{1,3}(?:\.\d{3})+|-?\d+(?:[.,]\d+)?)\s*(%?)", texto or "")
    if not m:
        return None, ""
    s = m.group(1)
    s = s.replace(".", "") if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s) else s.replace(",", ".")
    try:
        return float(s), m.group(2)
    except ValueError:
        return None, ""


def fecha_ok(v):
    return bool(v) and ex.fecha_iso(v)


def fmt(v):
    return f"{v:.0%}".replace(".", ",") if 0 < abs(v) < 1 else f"{v:,.0f}".replace(",", ".")


# etiqueta en Números clave de 00_estado.md -> variable en la hoja Supuestos del modelo
PAREJAS = [("Precio mensual", "Precio mensual"), ("CAC", "CAC"), ("Churn mensual", "Churn mensual"), ("Caja actual (CLP)", "Caja inicial")]


def comparar_modelo(base, txt, tolerancia=0.10):
    """[(etiqueta, valor en 00_estado, valor en el modelo)] cuando difieren más que la tolerancia."""
    modelo = os.path.join(ex.exp_dir(base), "entregables", "modelo_financiero.xlsx")
    nc = ex.numeros_clave(txt)
    if not nc or not os.path.exists(modelo):
        return []
    try:
        import modelo_xlsx
        sup = {s["variable"]: modelo_xlsx.numero(s["valor"]) for s in modelo_xlsx.supuestos(modelo, "Supuestos")}
    except (Exception, SystemExit):
        return []
    out = []
    for et, var in PAREJAS:
        a, b = nc.get(et), sup.get(var)
        if a is None or b is None:
            continue
        if b > 1 and a < 1 and "%" not in et:  # churn guardado como 5 (por ciento) vs 0,05
            b = b / 100 if et == "Churn mensual" else b
        if max(abs(a), abs(b)) and abs(a - b) / max(abs(a), abs(b)) > tolerancia:
            out.append((et, a, b))
    return out


def gate_num(g):
    m = re.match(r"G(\d)", g or "")
    return int(m.group(1)) if m else None


def auditar(base, dias_hip=30, hoy=None):
    hallazgos = []

    def h(nivel, tema, texto, accion):
        hallazgos.append((nivel, tema, texto, accion))
    txt = ex.leer_estado(base)
    hoy = hoy or dt.date.today()
    gate = ex.gate_actual_de(base)
    gn = gate_num(gate)
    dec = ex.filas(base, "decisiones")
    exps = ex.filas(base, "experimentos")
    ents = ex.filas(base, "entrevistas")
    evs = ex.filas(base, "evidencias")
    pils = ex.filas(base, "pilotos")
    pipe = ex.filas(base, "cuentas_y_pipeline")
    hips = ex.filas(base, "hipotesis")

    # 1. Ruta del estado vs decisiones registradas
    for linea in ex.seccion(txt, "Ruta").splitlines():
        m = re.match(r"\|\s*(G\d)[^|]*\|\s*Go\s*\|", linea)
        if m and not any(d.get("gate", "").startswith(m.group(1)) and d.get("decision", "").lower() == "go" for d in dec):
            h("ALERTA", "estado", f"La ruta marca {m.group(1)} en Go, pero no hay una decisión Go de {m.group(1)} en decisiones.csv.",
              "Registra la decisión con su criterio y evidencia, o corrige la ruta.")
    # 2. Gate declarado vs registros
    if gn is not None and gn >= 6 and not pils:
        h("ALERTA", "estado", f"El gate actual es {gate}, pero pilotos.csv está vacío.", "Registra el piloto (TPL-067) o revisa el gate actual.")
    if gn is not None and gn >= 7 and not any(re.search(r"gan|cliente|cerrad", d.get("etapa", ""), re.I) for d in pipe):
        h("ALERTA", "estado", f"El gate actual es {gate}, pero ninguna cuenta del pipeline está ganada.", "Registra las ventas o revisa el gate actual.")
    etapa = re.search(r"Etapa declarada:\*\*\s*(.*)", txt)
    if etapa and TRACCION.search(etapa.group(1)) and not pils and not any(re.search(r"gan|cliente", d.get("etapa", ""), re.I) for d in pipe) \
            and not ex.filas(base, "indicadores"):
        h("aviso", "estado", f"La etapa declarada menciona tracción («{etapa.group(1).strip()[:60]}»), pero no hay pilotos, ventas ni indicadores registrados.",
          "Pide los datos (contratos, facturas, uso) y regístralos; mientras tanto trátalo como declaración.")
    # 3. Decisiones Go sin respaldo o bajo el umbral
    for d in dec:
        if d.get("decision", "").lower() != "go":
            continue
        if not d.get("evidence_ids", "").strip():
            h("ALERTA", "decisión", f"{d.get('decision_id')} ({d.get('gate')}) es Go sin evidence_ids.", "Cita la evidencia o cambia la decisión a Hold.")
        if not d.get("criterio", "").strip():
            h("aviso", "decisión", f"{d.get('decision_id')} ({d.get('gate')}) no registra el criterio que se fijó antes.", "Anota el criterio y su fecha.")
    for x in exps:
        dx = x.get("decision", "").lower()
        if dx == "go" and not x.get("resultado", "").strip():
            h("ALERTA", "experimento", f"{x.get('experiment_id')} tiene decisión Go sin resultado.", "Registra el resultado medido.")
        if not x.get("umbral", "").strip():
            h("aviso", "experimento", f"{x.get('experiment_id')} no tiene umbral.", "Fija el umbral antes de mirar los datos.")
        u, uu = numero(x.get("umbral", ""))
        r, ru = numero(x.get("resultado", ""))
        if dx == "go" and u is not None and r is not None and uu == ru and r < u and not re.search(r"≤|<=|menos|máximo|max", x.get("umbral", ""), re.I):
            h("ALERTA", "sesgo", f"{x.get('experiment_id')}: decisión Go con resultado {x.get('resultado')} bajo el umbral {x.get('umbral')}.",
              "Un resultado bajo el umbral es Hold o Recycle; bajar la meta después de ver los datos es sesgo de confirmación.")
        if fecha_ok(x.get("fin")) and hoy - dt.timedelta(days=14) <= dt.date.fromisoformat(x["fin"][:10]) < hoy - dt.timedelta(days=7)                 and not x.get("resultado", "").strip():
            h("aviso", "experimento", f"{x.get('experiment_id')} terminó el {x['fin'][:10]} y no tiene resultado.", "Registra el resultado o extiende la fecha con una razón.")
    # 3b. Integridad referencial: decisiones ↔ evidencias, experimentos vencidos, entrevistas ↔ notas
    ev_ids = {v.get("evidence_id", "").strip() for v in evs}
    for d in dec:
        refs = [r for r in re.split(r"[;,\s]+", d.get("evidence_ids", "")) if r]
        malos = [r for r in refs if re.fullmatch(r"EV-\d+", r) and r not in ev_ids]
        if malos:
            h("ALERTA", "integridad", f"{d.get('decision_id')} cita {', '.join(malos)}, que no existe(n) en evidencias.",
              "Corrige el ID o registra la evidencia antes de sostener la decisión.")
        if not refs and d.get("decision", "").lower() in ("kill", "hold", "recycle"):
            h("aviso", "integridad", f"{d.get('decision_id')} ({d.get('gate')}) es {d.get('decision')} sin evidence_ids.",
              "También un Kill o un Hold necesitan su evidencia: cítala para poder revisarla después.")
    for x in exps:
        fin = x.get("fin", "")
        if not fecha_ok(fin) or dt.date.fromisoformat(fin[:10]) >= hoy:
            continue
        dias = (hoy - dt.date.fromisoformat(fin[:10])).days
        if x.get("resultado", "").strip() and not x.get("decision", "").strip():
            h("aviso", "integridad", f"{x.get('experiment_id')} terminó hace {dias} días con resultado pero sin decisión.",
              "Cierra el experimento: Go, Hold, Recycle o Kill contra el umbral fijado antes.")
        elif not x.get("resultado", "").strip() and dias > 14:
            h("ALERTA", "integridad", f"{x.get('experiment_id')} venció hace {dias} días sin resultado ni cierre.",
              "Registra lo que se midió (aunque sea parcial) o cierra con Kill; un experimento abierto para siempre no enseña nada.")
    notas_dir = os.path.join(ex.exp_dir(base), "investigacion", "notas")
    notas = sorted(os.listdir(notas_dir)) if os.path.isdir(notas_dir) else []
    for f in notas:
        if not f.endswith((".md", ".txt")):
            continue
        try:
            with open(os.path.join(notas_dir, f), encoding="utf-8-sig", errors="replace") as fh:
                pii = ex.buscar_pii(fh.read())
        except OSError:
            continue
        if pii:
            h("ALERTA", "privacidad", f"investigacion/notas/{f} contiene {', '.join(pii)}.",
              "Pásala por `ingestar.py anonimizar` y borra la versión con datos personales.")
        elif not f.endswith("_anon.md"):
            h("aviso", "privacidad", f"investigacion/notas/{f} no pasó por ingestar.py (no termina en _anon.md).",
              "Revísala con `ingestar.py revisar` antes de usarla como evidencia.")
    for e in ents:
        eid = e.get("entrevista_id", "")
        pii = ex.buscar_pii([v for k, v in e.items() if k != "entrevista_id"])
        if pii:
            h("ALERTA", "privacidad", f"{eid} tiene {', '.join(pii)} en el registro.", "Reemplaza por rol y segmento; el registro no lleva datos personales.")
        if notas and not any(n.startswith(eid + "_") for n in notas) and not e.get("hecho_o_cita_breve", "").strip():
            h("aviso", "integridad", f"{eid} no tiene nota anonimizada ni hecho registrado.",
              f"Anonimiza la nota con `ingestar.py anonimizar … --id {eid}` o registra el hecho concreto.")
    # 3c. Números clave de 00_estado.md vs modelo financiero
    for et, valor_estado, valor_modelo in comparar_modelo(base, txt):
        h("ALERTA", "coherencia", f"«{et}»: 00_estado.md dice {fmt(valor_estado)} y el modelo financiero usa {fmt(valor_modelo)}.",
          "Una de las dos cifras está desactualizada: corrígela (modelo_xlsx.py set o Números clave) antes de mostrar el modelo.")
    # 4. Hipótesis abiertas sin experimento
    for hid, enun, dias in ex.hipotesis_estancadas(base, hoy, dias=dias_hip):
        h("aviso", "hipótesis", f"{hid} lleva {dias} días sin experimento ni evidencia nueva: {enun}", "Diseña la prueba más barata (TPL-061) o descártala.")
    # 5. Costo hundido: trabajo sobre hipótesis descartadas
    descartadas = {d.get("hypothesis_id"): d for d in hips if re.search(r"descart|refut|kill", d.get("estado", ""), re.I)}
    for x in exps:
        if x.get("hypothesis_id") in descartadas and not x.get("resultado", "").strip():
            h("ALERTA", "sesgo", f"{x.get('experiment_id')} sigue abierto sobre {x.get('hypothesis_id')}, que está descartada.",
              "¿Costo hundido? Cierra el experimento o reabre la hipótesis con evidencia nueva.")
    # 6. Entrevistas complacientes
    if ents:
        intencion = [e for e in ents if INTENCION.search(" ".join([e.get("hecho_o_cita_breve", ""), e.get("necesidad", "")]))]
        compromisos = [e for e in ents if COMPROMISO.search(" ".join(e.values()))] + \
                      [v for v in evs if COMPROMISO.search(v.get("tipo", "") + " " + v.get("afirmacion", ""))]
        if len(intencion) >= max(3, len(ents) // 2) and not compromisos:
            h("ALERTA", "sesgo", f"{len(intencion)} de {len(ents)} entrevistas registran intención («me interesa», «lo compraría») y ninguna un compromiso de tiempo, acceso o dinero.",
              "Intención declarada es evidencia nivel 1. Pide un compromiso concreto (piloto con datos, reunión con el aprobador, preventa).")
        sin_hecho = [e for e in ents if not e.get("hecho_o_cita_breve", "").strip() or not e.get("situacion", "").strip()]
        if len(sin_hecho) > len(ents) // 2:
            h("aviso", "sesgo", f"{len(sin_hecho)} de {len(ents)} entrevistas no registran situación ni un hecho concreto.",
              "Registra la última vez que ocurrió el problema (hechos del pasado, no opiniones).")
        segs = {e.get("segmento", "").strip().lower() for e in ents if e.get("segmento")}
        if len(ents) >= 6 and len(segs) >= len(ents) * 0.7:
            h("aviso", "muestra", f"{len(ents)} entrevistas repartidas en {len(segs)} segmentos: ninguno tiene suficientes para concluir.",
              "Concentra las próximas entrevistas en un segmento (≥8).")
    # 7. Funciones antes de validar
    if gn is not None and gn <= 3:
        fx = [d for d in dec + exps if FUNCION.search(" ".join(d.values()))]
        if len(fx) >= 2:
            h("aviso", "sesgo", f"{len(fx)} decisiones o experimentos hablan de agregar funciones mientras el proyecto está en {gate}.",
              "¿Feature creep? Antes de construir más, confirma problema y propuesta (G1–G3).")
    # 8. Precio del modelo vs pipeline
    modelo = os.path.join(ex.exp_dir(base), "entregables", "modelo_financiero.xlsx")
    valores = [numero(d.get("valor_estimado_CLP", ""))[0] for d in pipe]
    valores = [v for v in valores if v]
    if os.path.exists(modelo) and valores:
        try:
            import modelo_xlsx
            sup = {s["variable"]: modelo_xlsx.numero(s["valor"]) for s in modelo_xlsx.supuestos(modelo, "Supuestos")}
            precio = sup.get("Precio mensual")
        except Exception:
            precio = None
        if precio:
            prom = sum(valores) / len(valores)
            cerca = [k for k in (1, 12) if 0.5 <= (prom / k) / precio <= 2]
            if not cerca:
                h("ALERTA", "coherencia", f"Precio mensual del modelo: {precio:,.0f} CLP; valor promedio en el pipeline: {prom:,.0f} CLP "
                  "(ni mensual ni anual calza dentro de 0,5–2×).".replace(",", "."),
                  "Alinea el modelo con lo que los clientes están aceptando, o explica la diferencia (descuento piloto, plan distinto).")
    # 9. Presupuesto vs Gantt (si hay marco lógico)
    docs = os.path.join(ex.exp_dir(base), "documentos")
    marco = [f for f in os.listdir(docs) if f.startswith("TPL-106")] if os.path.isdir(docs) else []
    if marco and ex.filas(base, "rendiciones"):
        h("info", "fondos", "Hay marco lógico y presupuesto.", f"Corre `fondos_lint.py coherencia --dir {base} --marco expediente/documentos/{marco[0]}` y `presupuesto_corfo.py revisar --dir {base}` antes de postular.")
    return hallazgos


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=".")
    ap.add_argument("--dias-hipotesis", type=int, default=30)
    ap.add_argument("--estricto", action="store_true", help="código de salida 1 si hay alertas")
    ap.add_argument("--hoy", help="fecha de referencia AAAA-MM-DD (por defecto, hoy; útil para un expediente de ejemplo)")
    a = ap.parse_args(argv)
    ex.requiere_expediente(a.dir)
    hoy = dt.date.fromisoformat(a.hoy) if a.hoy else dt.date.today()
    hs = auditar(a.dir, a.dias_hipotesis, hoy)
    orden = {"ALERTA": 0, "aviso": 1, "info": 2}
    print(f"# Auditoría de coherencia — {ex.nombre_proyecto(a.dir)} — {hoy.isoformat()}\n")
    if not hs:
        print("Sin contradicciones ni señales de sesgo detectadas por las reglas automáticas.")
    for nivel, tema, texto, accion in sorted(hs, key=lambda x: orden[x[0]]):
        print(f"- **{nivel}** [{tema}] {texto}\n  → {accion}")
    n = sum(1 for x in hs if x[0] == "ALERTA")
    print(f"\n{n} alerta(s), {sum(1 for x in hs if x[0] == 'aviso')} aviso(s). Son preguntas para el fundador, no veredictos.")
    sys.exit(1 if a.estricto and n else 0)


if __name__ == "__main__":
    main()
