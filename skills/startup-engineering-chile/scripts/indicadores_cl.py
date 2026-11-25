#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Indicadores económicos de Chile (UF, UTM, dólar, euro, IPC, IMACEC, TPM) con caché y respaldo sin internet.

  indicadores_cl.py obtener [uf utm dolar ...] [--json] [--sin-red]
  indicadores_cl.py convertir 120 UF CLP          # también CLP→UF, USD→CLP, UTM→CLP, etc.

Fuente: API pública de mindicador.cl (datos del Banco Central y SII). Orden de uso:
1) consulta en línea (si hay internet) y guarda caché; 2) caché local con su fecha;
3) valores de respaldo de assets/parametros_cl.json (con fecha, desactualizados).
La salida siempre dice de dónde salió cada valor y su fecha: cítala en presupuestos y postulaciones.
Caché: $SEC_CACHE o ~/.cache/startup-engineering-chile/indicadores.json
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

API = os.environ.get("MINDICADOR_URL", "https://mindicador.cl/api")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARAMS = os.path.join(SKILL_DIR, "assets", "parametros_cl.json")
CACHE = os.environ.get("SEC_CACHE") or os.path.join(os.path.expanduser("~"), ".cache", "startup-engineering-chile", "indicadores.json")
ALIAS = {"usd": "dolar", "dólar": "dolar", "eur": "euro", "clp": "clp"}
TODOS = ["uf", "utm", "dolar", "euro", "ipc", "imacec", "tpm"]


def _leer_cache():
    try:
        return json.load(open(CACHE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _guardar_cache(c):
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        tmp = CACHE + ".tmp"
        json.dump(c, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, CACHE)
    except OSError:
        pass


def consultar_api(timeout=6):
    req = urllib.request.Request(API, headers={"User-Agent": "startup-engineering-chile/1.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    out = {}
    for k in TODOS:
        d = data.get(k)
        if isinstance(d, dict) and d.get("valor") is not None:
            out[k] = {"valor": float(d["valor"]), "fecha": (d.get("fecha") or "")[:10],
                      "unidad": d.get("unidad_medida", ""), "nombre": d.get("nombre", k)}
    return out


def obtener(nombres, red=True):
    """Devuelve {nombre: {valor, fecha, origen, ...}}."""
    cache = _leer_cache()
    res = {}
    if red:
        try:
            nuevos = consultar_api()
            if nuevos:
                cache.update(nuevos)
                cache["_consultado"] = dt.datetime.now().isoformat(timespec="seconds")
                _guardar_cache(cache)
                for n in nombres:
                    if n in nuevos:
                        res[n] = dict(nuevos[n], origen="mindicador.cl")
        except Exception as e:  # sin internet, API caída, JSON inválido
            print(f"(sin conexión a {API}: {type(e).__name__}; uso caché o respaldo)", file=sys.stderr)
    for n in nombres:
        if n in res:
            continue
        if n in cache:
            res[n] = dict(cache[n], origen="caché")
            continue
        try:
            r = json.load(open(PARAMS, encoding="utf-8")).get("respaldo_indicadores", {}).get(n)
        except (OSError, ValueError):
            r = None
        if r:
            res[n] = {"valor": float(r["valor"]), "fecha": r["fecha"], "origen": "respaldo (desactualizado)"}
    return res


def valor(nombre, red=True):
    d = obtener([nombre], red=red).get(nombre)
    return (d["valor"], d["fecha"], d["origen"]) if d else (None, None, None)


def cmd_obtener(a):
    nombres = [ALIAS.get(n.lower(), n.lower()) for n in (a.nombres or TODOS)]
    res = obtener(nombres, red=not a.sin_red)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print("| Indicador | Valor | Fecha | Origen |\n|---|---|---|---|")
    for n in nombres:
        d = res.get(n)
        if not d:
            print(f"| {n} | — | — | no disponible |")
            continue
        v = d["valor"]
        txt = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"| {n.upper()} | {txt} | {d['fecha']} | {d['origen']} |")
    if any(d.get("origen") != "mindicador.cl" for d in res.values()):
        print("\nAlgún valor no viene de la consulta en línea: verifica la fecha antes de usarlo.")


def cmd_convertir(a):
    de, a_ = ALIAS.get(a.de.lower(), a.de.lower()), ALIAS.get(a.a.lower(), a.a.lower())
    necesarios = [x for x in (de, a_) if x != "clp"]
    res = obtener(necesarios, red=not a.sin_red)
    for x in necesarios:
        if x not in res:
            sys.exit(f"No tengo el valor de {x.upper()} (ni caché ni respaldo).")
    en_clp = a.monto * (res[de]["valor"] if de != "clp" else 1)
    final = en_clp / (res[a_]["valor"] if a_ != "clp" else 1)
    fuentes = "; ".join(f"{x.upper()} {res[x]['valor']:,.2f} al {res[x]['fecha']} ({res[x]['origen']})" for x in necesarios)
    print(f"{a.monto:,.2f} {de.upper()} = {final:,.2f} {a_.upper()}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"Valores usados: {fuentes}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("obtener"); p.add_argument("nombres", nargs="*"); p.add_argument("--json", action="store_true")
    p.add_argument("--sin-red", action="store_true"); p.set_defaults(f=cmd_obtener)
    p = sp.add_parser("convertir"); p.add_argument("monto", type=float); p.add_argument("de"); p.add_argument("a")
    p.add_argument("--sin-red", action="store_true"); p.set_defaults(f=cmd_convertir)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
