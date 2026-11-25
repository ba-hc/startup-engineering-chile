#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Mide el largo de la respuesta al usuario contra los límites de tools/limites_respuesta.json.

Uso:
  medir_respuesta.py ARCHIVO.md [--caso NOMBRE] [--max-palabras N] [--max-preguntas N]
  medir_respuesta.py --iteracion CARPETA      # estructura de skill-creator:
                                              # CARPETA/<caso>/<config>/[run-N/]outputs/respuesta_al_usuario.md

Cuenta palabras y preguntas fuera de bloques de código (``` ... ```) y de citas (líneas que
empiezan con >), donde van los mensajes de contacto redactados para terceros. Una pregunta es
cada signo "?" (los "??" seguidos cuentan como uno). Sale con código 1 si algo excede el límite.
"""
import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMITES = os.path.join(RAIZ, "tools", "limites_respuesta.json")
NOMBRE_RESPUESTA = "respuesta_al_usuario.md"


def prosa(texto):
    """Devuelve el texto sin bloques de código ni citas."""
    salida, en_codigo = [], False
    for linea in texto.splitlines():
        if linea.lstrip().startswith("```") or linea.lstrip().startswith("~~~"):
            en_codigo = not en_codigo
            continue
        if en_codigo or linea.lstrip().startswith(">"):
            continue
        salida.append(linea)
    return "\n".join(salida)


def medir(texto):
    p = prosa(texto)
    palabras = len(re.findall(r"[^\W_]+(?:[-'][^\W_]+)*", p))
    preguntas = len(re.findall(r"\?+", p))
    return palabras, preguntas


def limites(caso):
    try:
        with open(LIMITES, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {"max_palabras": None, "max_preguntas": None}
    base = dict(data.get("_por_defecto", {}))
    base.update(data.get(caso, {}) if caso else {})
    return base


def evaluar(ruta, caso=None, max_p=None, max_q=None):
    with open(ruta, encoding="utf-8-sig") as f:
        palabras, preguntas = medir(f.read())
    lim = limites(caso)
    mp = max_p if max_p is not None else lim.get("max_palabras")
    mq = max_q if max_q is not None else lim.get("max_preguntas")
    ok = (mp is None or palabras <= mp) and (mq is None or preguntas <= mq)
    return {"archivo": ruta, "caso": caso, "palabras": palabras, "max_palabras": mp,
            "preguntas": preguntas, "max_preguntas": mq, "ok": ok}


def recorrer_iteracion(carpeta):
    for caso in sorted(os.listdir(carpeta)):
        dcaso = os.path.join(carpeta, caso)
        if not os.path.isdir(dcaso):
            continue
        for raiz, _, archivos in os.walk(dcaso):
            if NOMBRE_RESPUESTA in archivos and os.path.basename(raiz) == "outputs":
                yield caso, os.path.join(raiz, NOMBRE_RESPUESTA)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archivo", nargs="?")
    ap.add_argument("--caso")
    ap.add_argument("--max-palabras", type=int)
    ap.add_argument("--max-preguntas", type=int)
    ap.add_argument("--iteracion", help="carpeta de una iteración de skill-creator")
    ap.add_argument("--json", action="store_true", help="salida en JSON")
    a = ap.parse_args(argv)
    if a.iteracion:
        res = [evaluar(r, c, a.max_palabras, a.max_preguntas) for c, r in recorrer_iteracion(a.iteracion)]
    elif a.archivo:
        res = [evaluar(a.archivo, a.caso, a.max_palabras, a.max_preguntas)]
    else:
        ap.error("indica un ARCHIVO o --iteracion CARPETA")
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        for r in res:
            estado = "OK " if r["ok"] else "EXCEDE"
            rel = os.path.relpath(r["archivo"], a.iteracion) if a.iteracion else r["archivo"]
            print(f"[{estado}] {rel}: {r['palabras']}/{r['max_palabras']} palabras, "
                  f"{r['preguntas']}/{r['max_preguntas']} preguntas")
        if not res:
            print(f"No se encontró ningún {NOMBRE_RESPUESTA}.")
    return 0 if res and all(r["ok"] for r in res) else 1


if __name__ == "__main__":
    sys.exit(main())
