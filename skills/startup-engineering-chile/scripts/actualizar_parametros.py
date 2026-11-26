#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Actualiza los valores de respaldo (UF, UTM, dólar) de assets/parametros_cl.json y revisa qué datos están vencidos.

  actualizar_parametros.py revisar                      # edad de parametros_cl.json, instrumentos.json y umbrales (sin red)
  actualizar_parametros.py indicadores [--escribir]     # consulta mindicador.cl y muestra/escribe el respaldo nuevo
  actualizar_parametros.py indicadores --uf 41500 --utm 72500 --fecha 2026-12-01 --escribir   # a mano, sin red

Solo toca `respaldo_indicadores` (valores con fecha y fuente). Las tasas, topes y reglas legales (IVA, cotizaciones,
fondos) NO se actualizan solas: cambian por ley o por bases y hay que verificarlas en la fuente oficial; `revisar`
dice cuáles están vencidas. Lo usa el workflow mensual de mantención (.github/workflows/mantencion.yml), que abre un
PR para revisión humana. Escritura atómica; deja el JSON con la misma estructura.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.config import ASSETS  # noqa: E402
from core.storage import escribir_atomico  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PARAMS = os.path.join(ASSETS, "parametros_cl.json")
ARCHIVOS = [("parametros_cl.json", "Parámetros legales (tasas, topes, tramos)", 6),
            (os.path.join("fondos", "instrumentos.json"), "Reglas de fondos", 3),
            ("umbrales_gates.json", "Umbrales por gate", 12)]


def cargar(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def cmd_revisar(a):
    hoy = dt.date.today()
    vencidos = 0
    for rel, nombre, meses in ARCHIVOS:
        d = cargar(os.path.join(ASSETS, rel))
        ver = d.get("_verificado", "")
        try:
            dias = (hoy - dt.date.fromisoformat(ver)).days
        except ValueError:
            print(f"⚠ {nombre}: sin _verificado legible ({rel})")
            vencidos += 1
            continue
        if dias > meses * 30:
            vencidos += 1
            print(f"⚠ {nombre}: verificado el {ver} (hace {dias} días; plazo {meses} meses) → revisar en la fuente oficial")
        else:
            print(f"✓ {nombre}: verificado el {ver} (hace {dias} días)")
    for k, r in cargar(PARAMS).get("respaldo_indicadores", {}).items():
        try:
            dias = (hoy - dt.date.fromisoformat(r["fecha"])).days
        except (KeyError, ValueError):
            continue
        print(f"{'⚠' if dias > 35 else '✓'} Respaldo {k.upper()}: {r['valor']} al {r['fecha']} ({r.get('fuente', '')})"
              + (" → corre `actualizar_parametros.py indicadores --escribir`" if dias > 35 else ""))
    sys.exit(1 if vencidos and a.estricto else 0)


def cmd_indicadores(a):
    hoy = dt.date.today().isoformat()
    nuevos = {}
    if a.uf or a.utm or a.dolar:
        fecha = a.fecha or hoy
        for k, v in (("uf", a.uf), ("utm", a.utm), ("dolar", a.dolar)):
            if v:
                nuevos[k] = {"valor": v, "fecha": fecha, "fuente": a.fuente or "ingresado a mano"}
    else:
        import indicadores_cl
        try:
            api = indicadores_cl.consultar_api()
        except Exception as e:
            sys.exit(f"No pude consultar {indicadores_cl.API} ({type(e).__name__}). Pasa los valores con --uf/--utm/--dolar y --fecha.")
        for k in ("uf", "utm", "dolar"):
            if k in api:
                nuevos[k] = {"valor": api[k]["valor"], "fecha": api[k]["fecha"][:10], "fuente": f"mindicador.cl ({hoy})"}
    if not nuevos:
        sys.exit("No hay valores nuevos.")
    d = cargar(PARAMS)
    resp = d.setdefault("respaldo_indicadores", {})
    for k, v in nuevos.items():
        antes = resp.get(k, {})
        print(f"{k.upper()}: {antes.get('valor', '—')} ({antes.get('fecha', '—')}) → {v['valor']} ({v['fecha']})")
    if not a.escribir:
        print("\n(simulación: agrega --escribir para guardar en assets/parametros_cl.json)")
        return
    resp.update(nuevos)
    with open(PARAMS, encoding="utf-8") as fh:
        raw = fh.read()
    bloque = ('  "respaldo_indicadores": {\n'
              + ",\n".join(f"    {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in resp.items()) + "\n  }")
    nuevo, n = re.subn(r'^  "respaldo_indicadores": \{.*?^  \}', lambda _: bloque, raw, count=1, flags=re.M | re.S)
    if not n:
        nuevo = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    json.loads(nuevo)
    escribir_atomico(PARAMS, nuevo)
    print(f"\nActualizado {PARAMS}. No cambia _verificado: las tasas y topes legales se revisan a mano en la fuente.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("revisar"); p.add_argument("--estricto", action="store_true", help="código 1 si algo está vencido")
    p.set_defaults(f=cmd_revisar)
    p = sp.add_parser("indicadores"); p.add_argument("--escribir", action="store_true")
    p.add_argument("--uf", type=float); p.add_argument("--utm", type=float); p.add_argument("--dolar", type=float)
    p.add_argument("--fecha"); p.add_argument("--fuente"); p.set_defaults(f=cmd_indicadores)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
