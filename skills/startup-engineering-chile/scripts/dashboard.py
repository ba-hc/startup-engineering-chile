#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Compila el expediente en un solo dashboard.html autocontenido (sin servidor ni internet).

  dashboard.py --dir RUTA [--salida expediente/entregables/dashboard.html]

Muestra: ruta por gates, semáforo (acciones vencidas, hipótesis estancadas, riesgos), embudo
entrevistas → cuentas → pilotos, hipótesis y su evidencia, experimentos con criterio y resultado,
últimas decisiones y próximas acciones. Se puede abrir con doble clic, imprimir a PDF o enviar.
Ojo: incluye lo que hay en el expediente; revisa que no tenga datos confidenciales antes de compartir.
"""
import argparse
import datetime as dt
import html
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expediente as ex  # noqa: E402

CSS = """
:root{--bg:#f7f7f5;--card:#fff;--tx:#1d1d1b;--mut:#6b6b66;--bd:#e3e2dc;--ok:#2f7d4f;--warn:#b7791f;--bad:#c0392b;--acc:#2d5bd7}
@media (prefers-color-scheme:dark){:root{--bg:#161615;--card:#1f1f1d;--tx:#ecebe6;--mut:#a3a29b;--bd:#33332f;--ok:#5cc28a;--warn:#e0a84a;--bad:#ef6f5f;--acc:#7b9cff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1100px;margin:0 auto;padding:24px 16px 48px}h1{font-size:26px;margin:0 0 4px}h2{font-size:16px;margin:0 0 12px}
.sub{color:var(--mut);margin-bottom:20px}.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px;overflow-x:auto}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:16px}
.kpi{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px}.kpi b{display:block;font-size:24px}
.kpi span{color:var(--mut);font-size:13px}table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--bd);vertical-align:top}th{color:var(--mut);font-weight:600}
.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;border:1px solid var(--bd)}
.go{color:var(--ok);border-color:var(--ok)}.hold,.encurso{color:var(--warn);border-color:var(--warn)}.kill,.recycle{color:var(--bad);border-color:var(--bad)}
.bar{height:22px;background:var(--acc);border-radius:4px;opacity:.85;min-width:2px}.row{display:grid;grid-template-columns:110px 1fr 40px;gap:8px;align-items:center;margin:6px 0}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}.dot.ok{background:var(--ok)}.dot.warn{background:var(--warn)}.dot.bad{background:var(--bad)}
footer{color:var(--mut);font-size:12px;margin-top:24px}
"""


def e(s):
    return html.escape(str(s or ""))


def pill(estado):
    k = re.sub(r"[^a-z]", "", (estado or "").lower())
    return f'<span class="pill {k}">{e(estado or "—")}</span>'


def tabla(cab, filas):
    if not filas:
        return '<p class="sub">Sin registros todavía.</p>'
    h = "".join(f"<th>{e(c)}</th>" for c in cab)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"


def construir(base):
    hoy = dt.date.today()
    txt = ex.leer_estado(base)
    if not txt:
        sys.exit("No hay expediente en esa carpeta.")
    proyecto = ex.nombre_proyecto(base)
    ruta = []
    for l in ex.seccion(txt, "Ruta").splitlines():
        cs = [c.strip() for c in l.strip().strip("|").split("|")]
        if l.startswith("|") and len(cs) >= 3 and not cs[0].startswith(("Gate", "-")):
            ruta.append([e(cs[0]), pill(cs[1]), e(cs[2]), e(cs[3] if len(cs) > 3 else "")])
    foco = ex.seccion(txt, "Foco actual")
    gate = re.search(r"Gate actual:\*\*\s*(G\d)", foco)
    pend, venc = ex.acciones(txt, hoy)
    est = ex.hipotesis_estancadas(base, hoy)
    ents, ctas, pils = ex.filas(base, "entrevistas"), ex.filas(base, "cuentas_y_pipeline"), ex.filas(base, "pilotos")
    hips, evs, exps = ex.filas(base, "hipotesis"), ex.filas(base, "evidencias"), ex.filas(base, "experimentos")
    decs, riesgos = ex.filas(base, "decisiones"), ex.filas(base, "riesgos")
    abiertos = [r for r in riesgos if r.get("estado", "").lower() not in ("cerrado", "mitigado")]
    errores, _ = ex.validar(base)

    def sem(n, malo=1):
        return "ok" if n == 0 else ("bad" if n >= malo * 3 else "warn")
    semaf = [("Acciones vencidas", len(venc), sem(len(venc))), ("Hipótesis estancadas", len(est), sem(len(est))),
             ("Riesgos abiertos", len(abiertos), sem(len(abiertos))), ("Errores del expediente", len(errores), sem(len(errores)))]
    embudo = [("Entrevistas", len(ents)), ("Cuentas", len(ctas)), ("Pilotos", len(pils)),
              ("Pilotos con decisión", sum(1 for p in pils if p.get("decision_comercial")))]
    mx = max([v for _, v in embudo] + [1])
    ev_por_h = {}
    for v in evs:
        ev_por_h[v.get("hypothesis_id", "")] = ev_por_h.get(v.get("hypothesis_id", ""), 0) + 1
    partes = [f"<h1>{e(proyecto)}</h1><div class='sub'>Dashboard del expediente · {hoy.isoformat()} · gate actual {e(gate.group(1) if gate else '—')}</div>"]
    partes.append("<div class='kpis'>" + "".join(
        f"<div class='kpi'><b>{v}</b><span>{e(k)}</span></div>" for k, v in
        [("Entrevistas", len(ents)), ("Hipótesis", len(hips)), ("Evidencias", len(evs)), ("Experimentos", len(exps)), ("Decisiones", len(decs))]) + "</div>")
    partes.append("<div class='grid'>")
    partes.append("<div class='card'><h2>Semáforo</h2>" + "".join(
        f"<div><span class='dot {c}'></span>{e(k)}: <b>{v}</b></div>" for k, v, c in semaf) + "</div>")
    partes.append("<div class='card'><h2>Embudo</h2>" + "".join(
        f"<div class='row'><span>{e(k)}</span><div class='bar' style='width:{100 * v / mx:.0f}%'></div><b>{v}</b></div>" for k, v in embudo) + "</div>")
    partes.append("</div><div class='card' style='margin-top:16px'><h2>Ruta por gates</h2>" + tabla(["Gate", "Estado", "Evidencia (0–4)", "Qué lo movería"], ruta) + "</div>")
    partes.append("<div class='grid' style='margin-top:16px'>")
    partes.append("<div class='card'><h2>Hipótesis</h2>" + tabla(["ID", "Enunciado", "Evidencias", "Estado"], [
        [e(h.get("hypothesis_id")), e(h.get("enunciado_refutable", "")[:140]), str(ev_por_h.get(h.get("hypothesis_id"), 0)), pill(h.get("estado"))] for h in hips]) + "</div>")
    partes.append("<div class='card'><h2>Experimentos</h2>" + tabla(["ID", "Métrica / umbral", "Resultado", "Decisión"], [
        [e(x.get("experiment_id")), e(f"{x.get('metrica', '')} · {x.get('umbral', '')}"), e(x.get("resultado")), pill(x.get("decision"))] for x in exps]) + "</div>")
    partes.append("</div><div class='grid' style='margin-top:16px'>")
    partes.append("<div class='card'><h2>Últimas decisiones</h2>" + tabla(["Fecha", "Gate", "Decisión", "Justificación"], [
        [e(d.get("fecha")), e(d.get("gate")), pill(d.get("decision")), e(d.get("justificacion", "")[:160])] for d in decs[-6:][::-1]]) + "</div>")
    partes.append("<div class='card'><h2>Próximas acciones</h2>" + tabla(["Acción", "Responsable", "Vence"], [
        [e(x) for x in t] + [] for t in venc] + [[e(x) for x in t] for t in pend]) + "</div>")
    partes.append("</div>")
    if abiertos:
        partes.append("<div class='card' style='margin-top:16px'><h2>Riesgos abiertos</h2>" + tabla(["ID", "Riesgo", "Prob.", "Impacto", "Mitigación"], [
            [e(r.get("risk_id")), e(r.get("riesgo")), e(r.get("probabilidad")), e(r.get("impacto")), e(r.get("mitigacion"))] for r in abiertos]) + "</div>")
    partes.append("<footer>Generado por la skill Startup Engineering Chile desde expediente/. Lo que no está registrado no aparece: "
                  "la presentación no crea evidencia.</footer>")
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{e(proyecto)} · dashboard</title><style>{CSS}</style></head><body><main>{''.join(partes)}</main></body></html>")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=".")
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    dst = a.salida or os.path.join(ex.exp_dir(a.dir), "entregables", "dashboard.html")
    ex.escribir_atomico(dst, construir(a.dir))
    print(f"Creado {dst}")


if __name__ == "__main__":
    main()
