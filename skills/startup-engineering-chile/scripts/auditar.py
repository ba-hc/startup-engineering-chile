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
  - señales de sesgo: entrevistas complacientes, costo hundido, funciones agregadas antes de validar.

Uso:
  auditar.py --dir RUTA [--dias-hipotesis 30] [--estricto]

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


def gate_num(g):
    m = re.match(r"G(\d)", g or "")
    return int(m.group(1)) if m else None


def auditar(base, dias_hip=30):
    hallazgos = []

    def h(nivel, tema, texto, accion):
        hallazgos.append((nivel, tema, texto, accion))
    txt = ex.leer_estado(base)
    hoy = dt.date.today()
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
        if x.get("fin") and ex.fecha_iso(x["fin"]) and dt.date.fromisoformat(x["fin"][:10]) < hoy - dt.timedelta(days=7) and not x.get("resultado", "").strip():
            h("aviso", "experimento", f"{x.get('experiment_id')} terminó el {x['fin'][:10]} y no tiene resultado.", "Registra el resultado o extiende la fecha con una razón.")
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
        h("info", "fondos", "Hay marco lógico y presupuesto.", f"Corre `fondos_lint.py coherencia --dir {base} --marco expediente/documentos/{marco[0]}` antes de postular.")
    return hallazgos


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=".")
    ap.add_argument("--dias-hipotesis", type=int, default=30)
    ap.add_argument("--estricto", action="store_true", help="código de salida 1 si hay alertas")
    a = ap.parse_args(argv)
    ex.requiere_expediente(a.dir)
    hs = auditar(a.dir, a.dias_hipotesis)
    orden = {"ALERTA": 0, "aviso": 1, "info": 2}
    print(f"# Auditoría de coherencia — {ex.nombre_proyecto(a.dir)} — {dt.date.today().isoformat()}\n")
    if not hs:
        print("Sin contradicciones ni señales de sesgo detectadas por las reglas automáticas.")
    for nivel, tema, texto, accion in sorted(hs, key=lambda x: orden[x[0]]):
        print(f"- **{nivel}** [{tema}] {texto}\n  → {accion}")
    n = sum(1 for x in hs if x[0] == "ALERTA")
    print(f"\n{n} alerta(s), {sum(1 for x in hs if x[0] == 'aviso')} aviso(s). Son preguntas para el fundador, no veredictos.")
    sys.exit(1 if a.estricto and n else 0)


if __name__ == "__main__":
    main()
