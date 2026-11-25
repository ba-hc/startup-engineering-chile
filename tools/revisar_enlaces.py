#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Revisa que respondan las URL de la biblioteca (fuentes, libros, charlas, mentores) y de los JSON de datos.

Uso: python tools/revisar_enlaces.py [--salida informe.md] [--hilos 8] [--timeout 20] [--estricto]

Clasifica cada URL:
- ok: responde 2xx/3xx;
- bloqueado: 401/403/429 o similar (el sitio rechaza clientes automáticos; revisar a mano);
- roto: 404/410 o el dominio no existe;
- error: tiempo agotado, SSL u otro error de red (puede ser transitorio).
Que un enlace responda no verifica su contenido: las fuentes "por revalidar" siguen así hasta que
alguien lea la página y actualice la fila. Sale con código 1 si hay rotos (con --estricto, también errores).
"""
import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import json
import os
import re
import socket
import ssl
import sys
import urllib.error
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, "skills", "startup-engineering-chile")
CSVS = ["fuentes.csv", "libros.csv", "charlas_y_cursos.csv", "mentores.csv"]
JSONS = ["assets/parametros_cl.json", "assets/fondos/instrumentos.json"]
UA = "Mozilla/5.0 (compatible; revisor-enlaces-skill/1.0; +https://github.com/)"


def recolectar():
    urls = {}
    for nombre in CSVS:
        ruta = os.path.join(SKILL, "references", "biblioteca", nombre)
        with open(ruta, encoding="utf-8-sig", newline="") as fh:
            for i, fila in enumerate(csv.DictReader(fh), 2):
                for u in re.findall(r"https?://[^\s;,\"<>]+", fila.get("url", "") or ""):
                    urls.setdefault(u.rstrip(".)"), []).append(f"{nombre}:{fila.get('id') or i}")
    for rel in JSONS:
        with open(os.path.join(SKILL, rel), encoding="utf-8") as fh:
            texto = json.dumps(json.load(fh), ensure_ascii=False)
        for u in re.findall(r"https?://[^\s;,\"<>]+", texto):
            urls.setdefault(u.rstrip(".)"), []).append(rel)
    return urls


def probar(url, timeout):
    ctx = ssl.create_default_context()
    for metodo in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=metodo, headers={"User-Agent": UA, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                return "ok", str(r.status)
        except urllib.error.HTTPError as e:
            if metodo == "HEAD" and e.code in (400, 403, 405, 501):
                continue  # muchos sitios no aceptan HEAD
            if e.code in (404, 410):
                return "roto", str(e.code)
            if e.code in (401, 403, 406, 429, 451, 999):
                return "bloqueado", str(e.code)
            return "error", str(e.code)
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.gaierror):
                return "roto", "dominio no resuelve"
            return "error", str(e.reason)[:80]
        except (socket.timeout, TimeoutError):
            return "error", "tiempo agotado"
        except Exception as e:  # noqa: BLE001 - cualquier fallo de red se informa, no se cae
            return "error", type(e).__name__
    return "error", "sin respuesta"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida")
    ap.add_argument("--hilos", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=20)
    ap.add_argument("--estricto", action="store_true")
    a = ap.parse_args(argv)
    urls = recolectar()
    res = {}
    with cf.ThreadPoolExecutor(max_workers=a.hilos) as ex:
        futuros = {ex.submit(probar, u, a.timeout): u for u in urls}
        for f in cf.as_completed(futuros):
            res[futuros[f]] = f.result()
    cuenta = {k: sum(1 for v in res.values() if v[0] == k) for k in ("ok", "bloqueado", "roto", "error")}
    lineas = [f"## Enlaces de la biblioteca ({dt.date.today().isoformat()})", "",
              f"{len(urls)} URL únicas: {cuenta['ok']} ok · {cuenta['bloqueado']} bloqueadas · "
              f"{cuenta['roto']} rotas · {cuenta['error']} con error", ""]
    for clase, titulo in (("roto", "Rotas (reemplazar o marcar en la fila)"),
                          ("error", "Con error (reintentar; si persiste, revisar)"),
                          ("bloqueado", "Bloqueadas para clientes automáticos (revisar a mano si importa)")):
        filas = sorted(u for u, v in res.items() if v[0] == clase)
        if filas:
            lineas += [f"### {titulo}", ""] + [f"- {u} ({res[u][1]}) — {', '.join(urls[u][:3])}" for u in filas] + [""]
    texto = "\n".join(lineas) + "\n"
    print(texto)
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(texto)
    malo = cuenta["roto"] + (cuenta["error"] if a.estricto else 0)
    return 1 if malo else 0


if __name__ == "__main__":
    sys.exit(main())
