#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Tablero de cohorte: resume muchos expedientes (equipos de una incubadora, curso o aceleradora).

  cohorte.py --raiz CARPETA [--html tablero.html] [--inactivo 14]

Busca CARPETA/*/expediente/ (hasta 3 niveles) y, por equipo, muestra gate actual, entrevistas,
evidencia confirmada, hipótesis estancadas, acciones vencidas, días sin actividad, última decisión
y errores del expediente. Marca alertas: sin terreno (0 entrevistas), inactivo, vencidas, fondo en
preparación sin requisitos verificados. Al final, los bloqueos que se repiten en la cohorte.
Solo lee: no modifica los expedientes de los equipos.
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


def encontrar(raiz, prof=3):
    out = []
    raiz = os.path.abspath(raiz)
    for dp, dn, _ in os.walk(raiz):
        if dp[len(raiz):].count(os.sep) >= prof:
            dn[:] = []
            continue
        if os.path.exists(os.path.join(dp, "expediente", "00_estado.md")):
            out.append(dp)
            dn[:] = [d for d in dn if d != "expediente"]
    return sorted(out)


def ultima_actividad(base):
    fechas = []
    for reg in ex.registros_disponibles():
        for d in ex.filas(base, reg):
            for c in ("fecha", "fecha_consulta", "inicio"):
                v = d.get(c, "")
                if ex.fecha_iso(v):
                    fechas.append(dt.date.fromisoformat(v[:10]))
    for l in ex.seccion(ex.leer_estado(base), "Bitácora de sesiones").splitlines():
        m = re.search(r"\d{4}-\d{2}-\d{2}", l)
        if m:
            fechas.append(dt.date.fromisoformat(m.group(0)))
    fechas = [f for f in fechas if f <= dt.date.today()]  # ignora fechas planificadas a futuro
    return max(fechas) if fechas else None


def resumen(base, hoy, inactivo):
    txt = ex.leer_estado(base)
    gate = re.search(r"Gate actual:\*\*\s*(G\d)", ex.seccion(txt, "Foco actual"))
    _, venc = ex.acciones(txt, hoy)
    est = ex.hipotesis_estancadas(base, hoy)
    ents = ex.filas(base, "entrevistas")
    evs = [v for v in ex.filas(base, "evidencias") if v.get("estado") == "confirmado"]
    decs = ex.filas(base, "decisiones")
    req = ex.filas(base, "corfo_elegibilidad")
    errores, _ = ex.validar(base)
    ult = ultima_actividad(base)
    dias = (hoy - ult).days if ult else None
    alertas = []
    if not ents:
        alertas.append("sin terreno")
    if dias is None or dias > inactivo:
        alertas.append("inactivo")
    if venc:
        alertas.append("acciones vencidas")
    if est:
        alertas.append("hipótesis estancadas")
    if req and any(r.get("estado", "").lower() not in ("cumple", "verificado", "confirmado") for r in req):
        alertas.append("fondo: requisitos sin verificar")
    if errores:
        alertas.append("expediente con errores")
    return {"equipo": ex.nombre_proyecto(base) or os.path.basename(base), "carpeta": base,
            "gate": gate.group(1) if gate else "—", "entrevistas": len(ents), "evidencia": len(evs),
            "estancadas": len(est), "vencidas": len(venc), "dias": dias,
            "decision": (f"{decs[-1].get('gate')} {decs[-1].get('decision')}" if decs else "—"),
            "errores": len(errores), "alertas": alertas}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--html")
    ap.add_argument("--inactivo", type=int, default=14)
    a = ap.parse_args(argv)
    hoy = dt.date.today()
    bases = encontrar(a.raiz)
    if not bases:
        sys.exit(f"No encontré expedientes bajo {a.raiz} (busco */expediente/00_estado.md).")
    filas = [resumen(b, hoy, a.inactivo) for b in bases]
    filas.sort(key=lambda f: (-len(f["alertas"]), f["equipo"]))
    cab = ["Equipo", "Gate", "Entrevistas", "Evidencia confirmada", "Hip. estancadas", "Acciones vencidas",
           "Días sin actividad", "Última decisión", "Alertas"]
    print(f"# Cohorte — {len(filas)} equipos — {hoy.isoformat()}\n")
    print("| " + " | ".join(cab) + " |\n|" + "---|" * len(cab))
    for f in filas:
        print(f"| {f['equipo']} | {f['gate']} | {f['entrevistas']} | {f['evidencia']} | {f['estancadas']} | {f['vencidas']} | "
              f"{f['dias'] if f['dias'] is not None else '—'} | {f['decision']} | {', '.join(f['alertas']) or 'ok'} |")
    conteo = {}
    for f in filas:
        for al in f["alertas"]:
            conteo[al] = conteo.get(al, 0) + 1
    gates = {}
    for f in filas:
        gates[f["gate"]] = gates.get(f["gate"], 0) + 1
    print("\n## Bloqueos que se repiten")
    for al, n in sorted(conteo.items(), key=lambda x: -x[1]):
        print(f"- {al}: {n} de {len(filas)} equipos")
    print("\n## Distribución por gate\n" + ", ".join(f"{g}: {n}" for g, n in sorted(gates.items())))
    if a.html:
        e = html.escape
        filas_html = "".join("<tr>" + "".join(f"<td>{e(str(x))}</td>" for x in [
            f["equipo"], f["gate"], f["entrevistas"], f["evidencia"], f["estancadas"], f["vencidas"],
            f["dias"] if f["dias"] is not None else "—", f["decision"], ", ".join(f["alertas"]) or "ok"]) + "</tr>" for f in filas)
        doc = (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
               f"<title>Cohorte {hoy.isoformat()}</title><style>body{{font:14px system-ui,sans-serif;margin:0;padding:16px;background:#fafaf8;color:#1d1d1b}}"
               f"@media(prefers-color-scheme:dark){{body{{background:#171716;color:#ecebe6}}}}table{{border-collapse:collapse;width:100%}}"
               f"th,td{{padding:6px 8px;border-bottom:1px solid #8884;text-align:left}}div{{overflow-x:auto}}</style></head><body>"
               f"<h1>Cohorte · {len(filas)} equipos · {hoy.isoformat()}</h1><div><table><tr>{''.join(f'<th>{e(c)}</th>' for c in cab)}</tr>{filas_html}</table></div>"
               f"<h2>Bloqueos que se repiten</h2><ul>{''.join(f'<li>{e(k)}: {v} de {len(filas)}</li>' for k, v in sorted(conteo.items(), key=lambda x: -x[1]))}</ul></body></html>")
        ex.escribir_atomico(a.html, doc)
        print(f"\nCreado {a.html}")


if __name__ == "__main__":
    main()
