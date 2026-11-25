#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Valida los JSON de datos de la skill contra sus esquemas en tools/esquemas/.

Uso: python tools/validar_datos.py

Los esquemas son JSON Schema (draft 2020-12) y sirven en cualquier editor. Este validador usa solo
la biblioteca estándar y entiende el subconjunto que usan: type, required, properties,
patternProperties, additionalProperties, items, enum, pattern, minimum, maximum, minItems,
minLength y minProperties. Sale con código 1 si hay errores.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "skills", "startup-engineering-chile", "assets")
ESQUEMAS = os.path.join(RAIZ, "tools", "esquemas")
PARES = [
    (os.path.join(ASSETS, "fondos", "instrumentos.json"), "instrumentos.schema.json"),
    (os.path.join(ASSETS, "parametros_cl.json"), "parametros_cl.schema.json"),
    (os.path.join(ASSETS, "umbrales_gates.json"), "umbrales_gates.schema.json"),
]
TIPOS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def validar(valor, esq, ruta="$"):
    errores = []
    tipos = esq.get("type")
    if tipos is not None:
        tipos = tipos if isinstance(tipos, list) else [tipos]
        if not any(TIPOS[t](valor) for t in tipos):
            return [f"{ruta}: se esperaba {'/'.join(tipos)}, hay {type(valor).__name__}"]
    if "enum" in esq and valor not in esq["enum"]:
        errores.append(f"{ruta}: {valor!r} no está en {esq['enum']}")
    if isinstance(valor, str):
        if "pattern" in esq and not re.search(esq["pattern"], valor):
            errores.append(f"{ruta}: {valor!r} no cumple el patrón {esq['pattern']}")
        if len(valor) < esq.get("minLength", 0):
            errores.append(f"{ruta}: texto demasiado corto")
    if TIPOS["number"](valor):
        if "minimum" in esq and valor < esq["minimum"]:
            errores.append(f"{ruta}: {valor} es menor que {esq['minimum']}")
        if "maximum" in esq and valor > esq["maximum"]:
            errores.append(f"{ruta}: {valor} es mayor que {esq['maximum']}")
    if isinstance(valor, list):
        if len(valor) < esq.get("minItems", 0):
            errores.append(f"{ruta}: se esperaban al menos {esq['minItems']} elementos")
        if "items" in esq:
            for i, v in enumerate(valor):
                errores += validar(v, esq["items"], f"{ruta}[{i}]")
    if isinstance(valor, dict):
        if len(valor) < esq.get("minProperties", 0):
            errores.append(f"{ruta}: se esperaban al menos {esq['minProperties']} claves")
        for r in esq.get("required", []):
            if r not in valor:
                errores.append(f"{ruta}: falta la clave obligatoria '{r}'")
        props = esq.get("properties", {})
        patrones = esq.get("patternProperties", {})
        for k, v in valor.items():
            cubierta = False
            if k in props:
                cubierta = True
                errores += validar(v, props[k], f"{ruta}.{k}")
            for pat, sub in patrones.items():
                if re.search(pat, k):
                    cubierta = True
                    errores += validar(v, sub, f"{ruta}.{k}")
            extra = esq.get("additionalProperties", True)
            if not cubierta:
                if extra is False:
                    errores.append(f"{ruta}: clave no permitida '{k}'")
                elif isinstance(extra, dict):
                    errores += validar(v, extra, f"{ruta}.{k}")
    return errores


def main():
    total = 0
    for datos, esquema in PARES:
        nombre = os.path.relpath(datos, RAIZ)
        try:
            with open(datos, encoding="utf-8") as f:
                valor = json.load(f)
            with open(os.path.join(ESQUEMAS, esquema), encoding="utf-8") as f:
                esq = json.load(f)
        except (OSError, ValueError) as e:
            print(f"[ERROR] {nombre}: {e}")
            total += 1
            continue
        errores = validar(valor, esq)
        total += len(errores)
        print(f"[{'OK' if not errores else 'ERROR'}] {nombre}" + "".join(f"\n  - {e}" for e in errores))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
