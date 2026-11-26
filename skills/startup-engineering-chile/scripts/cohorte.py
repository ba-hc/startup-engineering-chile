#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Tablero de cohorte: resume muchos expedientes (equipos de una incubadora, curso o aceleradora).

  cohorte.py --raiz CARPETA [--html tablero.html] [--xlsx cohorte.xlsx] [--csv cohorte.csv] [--estancado 14]

Busca CARPETA/*/expediente/ (hasta 3 niveles) y, por equipo, muestra gate actual, chequeos del gate cumplidos,
entrevistas, evidencia confirmada, hipótesis estancadas, acciones vencidas, días sin actividad, días en el gate,
misión de 7 días, TRL/CRL, última decisión y errores del expediente.
Alertas: sin terreno (0 entrevistas), estancado (más de N días sin actividad), misión vencida, acciones vencidas,
fondo en preparación sin requisitos verificados. Al final: bloqueos que se repiten, distribución por gate y la
matriz TRL x CRL de la cohorte. --xlsx exporta un libro consolidado (una hoja de equipos y una por registro con la
columna «equipo»). Solo lee: no modifica los expedientes de los equipos.
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
from core import exporters  # noqa: E402
from core.gates import evaluar_gate  # noqa: E402
from core.schemas import NUCLEO  # noqa: E402

MADUREZ = re.compile(r"TRL\s*(\d)\D+CRL\s*(\d)", re.I)


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


def madurez(txt):
    """(TRL, CRL) declarados en el perfil («Madurez (TRL / CRL): TRL 4 / CRL 3») o (None, None)."""
    m = MADUREZ.search(ex.campo(txt, "Madurez"))
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def dias_en_gate(base, hoy):
    """Días desde la última decisión registrada (o desde la creación del expediente)."""
    fechas = [d.get("fecha", "")[:10] for d in ex.filas(base, "decisiones") if ex.fecha_iso(d.get("fecha", ""))]
    ref = max(fechas) if fechas else (ex.leer_manifest(base) or {}).get("creado", "")
    return (hoy - dt.date.fromisoformat(ref)).days if ref and ex.fecha_iso(ref) else None


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
    g = gate.group(1) if gate else None
    chequeos = evaluar_gate(base, g) if g else []
    mi = ex.mision(txt, hoy)
    trl, crl = madurez(txt)
    alertas = []
    if not ents:
        alertas.append("sin terreno")
    if dias is None or dias > inactivo:
        alertas.append(f"estancado (>{inactivo} días)")
    if mi and mi["vencida"]:
        alertas.append("misión vencida")
    if venc:
        alertas.append("acciones vencidas")
    if est:
        alertas.append("hipótesis estancadas")
    if req and any(r.get("estado", "").lower() not in ("cumple", "verificado", "confirmado") for r in req):
        alertas.append("fondo: requisitos sin verificar")
    if errores:
        alertas.append("expediente con errores")
    return {"equipo": ex.nombre_proyecto(base) or os.path.basename(base), "carpeta": base,
            "gate": g or "—", "chequeos": f"{sum(1 for c in chequeos if c['cumple'])}/{len(chequeos)}" if chequeos else "—",
            "entrevistas": len(ents), "evidencia": len(evs),
            "estancadas": len(est), "vencidas": len(venc), "dias": dias, "dias_gate": dias_en_gate(base, hoy) if g else None,
            "mision": (mi["mision"][:60] + (" (vencida)" if mi["vencida"] else "")) if mi else "—", "trl": trl, "crl": crl,
            "decision": (f"{decs[-1].get('gate')} {decs[-1].get('decision')}" if decs else "—"),
            "errores": len(errores), "alertas": alertas}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--html")
    ap.add_argument("--xlsx", help="libro consolidado: hoja Equipos + una hoja por registro con la columna equipo")
    ap.add_argument("--csv", help="tabla de equipos en CSV (';' y BOM, para Excel en español)")
    ap.add_argument("--estancado", "--inactivo", dest="inactivo", type=int, default=14, help="días sin actividad para marcar estancado")
    a = ap.parse_args(argv)
    hoy = dt.date.today()
    bases = encontrar(a.raiz)
    if not bases:
        sys.exit(f"No encontré expedientes bajo {a.raiz} (busco */expediente/00_estado.md).")
    filas = [resumen(b, hoy, a.inactivo) for b in bases]
    filas.sort(key=lambda f: (-len(f["alertas"]), f["equipo"]))
    cab = ["Equipo", "Gate", "Chequeos", "Entrevistas", "Evidencia confirmada", "Hip. estancadas", "Acciones vencidas",
           "Días sin actividad", "Días en el gate", "TRL/CRL", "Misión de 7 días", "Última decisión", "Alertas"]

    def nd(v):
        return v if v is not None else "—"

    def celdas(f):
        return [f["equipo"], f["gate"], f["chequeos"], f["entrevistas"], f["evidencia"], f["estancadas"], f["vencidas"],
                nd(f["dias"]), nd(f["dias_gate"]), f"{nd(f['trl'])}/{nd(f['crl'])}", f["mision"], f["decision"],
                ", ".join(f["alertas"]) or "ok"]
    print(f"# Cohorte — {len(filas)} equipos — {hoy.isoformat()}\n")
    print("| " + " | ".join(cab) + " |\n|" + "---|" * len(cab))
    for f in filas:
        print("| " + " | ".join(str(c) for c in celdas(f)) + " |")
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
    con_madurez = [f for f in filas if f["trl"] and f["crl"]]
    if con_madurez:
        print("\n## Matriz TRL × CRL (madurez técnica vs. comercial declarada)")
        print("| TRL / CRL | " + " | ".join(str(c) for c in range(1, 10)) + " |\n|---|" + "---|" * 9)
        for t in range(9, 0, -1):
            fila = [", ".join(f["equipo"][:14] for f in con_madurez if f["trl"] == t and f["crl"] == c) for c in range(1, 10)]
            if any(fila):
                print(f"| {t} | " + " | ".join(fila) + " |")
        desfase = [f["equipo"] for f in con_madurez if f["trl"] - f["crl"] >= 3]
        if desfase:
            print(f"\nTecnología muy por delante del mercado (TRL − CRL ≥ 3): {', '.join(desfase)}. Prioriza validación comercial.")
    sin = len(filas) - len(con_madurez)
    if sin:
        print(f"\n{sin} equipo(s) sin «Madurez (TRL / CRL)» en 00_estado.md.")
    if a.csv:
        ex.escribir_atomico(a.csv, ex.csv_texto(cab, [[str(c) for c in celdas(f)] for f in filas], delimiter=";"), bom=True)
        print(f"\nCreado {a.csv}")
    if a.xlsx:
        hojas = [("Equipos", cab, [celdas(f) for f in filas])]
        for reg in NUCLEO + ["rendiciones", "riesgos", "indicadores"]:
            rows, h = [], None
            for f in filas:
                for d in ex.filas(f["carpeta"], reg):
                    h = h or [k for k in d if not k.startswith("_")]
                    rows.append([f["equipo"]] + [d.get(k, "") for k in h])
            if rows:
                hojas.append((reg, ["equipo"] + h, rows))
        exporters.escribir_xlsx(a.xlsx, hojas)
        print(f"\nCreado {a.xlsx} ({len(hojas)} hojas)")
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
