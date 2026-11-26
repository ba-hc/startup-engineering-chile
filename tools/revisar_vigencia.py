#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Avisa cuando los datos fechados de la skill superan su umbral de antigüedad.

Uso: python tools/revisar_vigencia.py [--hoy AAAA-MM-DD] [--salida informe.md]

Revisa:
- `_verificado` de parametros_cl.json (6 meses), fondos/instrumentos.json (3) y umbrales_gates.json (12);
- "Última verificación: AAAA-MM-DD" de los flujos en references/flujos/ (6 meses);
- fecha de reconsulta de las fuentes (references/biblioteca/fuentes_*.csv) marcadas como verificadas (12 meses).
Sale con código 1 si algo venció.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, "skills", "startup-engineering-chile")
JSONS = [("assets/parametros_cl.json", 6), ("assets/fondos/instrumentos.json", 3), ("assets/umbrales_gates.json", 12)]
MESES_FLUJOS = 6
MESES_FUENTES = 12


def fecha(texto):
    try:
        return dt.date.fromisoformat(texto.strip()[:10])
    except (ValueError, AttributeError):
        return None


def revisar(hoy):
    vencidos, sin_fecha = [], []

    def evaluar(nombre, f, meses):
        if f is None:
            sin_fecha.append(nombre)
        elif (hoy - f).days > meses * 30:
            vencidos.append(f"{nombre}: verificado el {f.isoformat()} ({(hoy - f).days} días; umbral {meses} meses)")

    for rel, meses in JSONS:
        try:
            with open(os.path.join(SKILL, rel), encoding="utf-8") as fh:
                evaluar(rel, fecha(json.load(fh).get("_verificado", "")), meses)
        except (OSError, ValueError):
            sin_fecha.append(rel)
    dflujos = os.path.join(SKILL, "references", "flujos")
    for nombre in sorted(os.listdir(dflujos)):
        if not nombre.endswith(".md"):
            continue
        with open(os.path.join(dflujos, nombre), encoding="utf-8") as fh:
            m = re.search(r"Última verificación:\**\s*(\d{4}-\d{2}-\d{2})", fh.read())
        if m:  # los flujos de método (sin datos que caduquen) no llevan fecha
            evaluar(f"references/flujos/{nombre}", fecha(m.group(1)), MESES_FLUJOS)
    dbib = os.path.join(SKILL, "references", "biblioteca")
    for nombre in sorted(n for n in os.listdir(dbib) if n.startswith("fuentes_") and n.endswith(".csv")):
        with open(os.path.join(dbib, nombre), encoding="utf-8-sig", newline="") as fh:
            for fila in csv.DictReader(fh):
                if fila.get("estado", "").strip().lower().startswith("verificad"):
                    evaluar(f"{nombre} {fila['id']}", fecha(fila.get("fecha_reconsulta", "")), MESES_FUENTES)
    return vencidos, sin_fecha


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hoy", help="fecha de referencia (por defecto, hoy)")
    ap.add_argument("--salida", help="escribe el informe en Markdown")
    a = ap.parse_args(argv)
    hoy = fecha(a.hoy) if a.hoy else dt.date.today()
    vencidos, sin_fecha = revisar(hoy)
    lineas = [f"## Vigencia de datos ({hoy.isoformat()})", ""]
    if not vencidos and not sin_fecha:
        lineas.append("Todo dentro de su umbral de antigüedad.")
    if vencidos:
        lineas += ["**Vencidos** (verifica en la fuente y actualiza la fecha):", ""] + [f"- {v}" for v in vencidos] + [""]
    if sin_fecha:
        lineas += ["**Sin fecha legible:**", ""] + [f"- {s}" for s in sin_fecha]
    texto = "\n".join(lineas) + "\n"
    print(texto)
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(texto)
    return 1 if vencidos or sin_fecha else 0


if __name__ == "__main__":
    sys.exit(main())
