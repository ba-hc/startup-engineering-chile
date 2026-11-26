#!/usr/bin/env python3
"""Arma el fixture de un caso de eval en una carpeta de trabajo, sin copias duplicadas del expediente en el repo.

  python tools/armar_fixture.py CASO DESTINO        # lo llama evals/<caso>/place-files.sh

Lee CASO/fixture.json (opcional) y aplica, en orden:
  1. capas: cada una arma un expediente en DESTINO/<destino>/expediente desde una base:
       "demo"          → examples/expediente_demo/expediente (el demo vigente, esquema actual)
       "vacio"         → 00_estado.md + manifest.json + registros solo con encabezado
                          (claves: "proyecto", "nivel", "registros", "fecha", "modo")
       "_bases/<name>" → evals/_bases/<name>/expediente (compartida por varios casos)
  2. CASO/files/ se copia encima (solo las diferencias de cada caso);
  3. "eliminar": rutas relativas a DESTINO que se borran (p. ej. para simular un expediente dañado);
  4. "empaquetar": {"salida": "x.zip", "origen": ".", "conservar": false} empaqueta <origen>/expediente en un ZIP
     como lo hace `expediente.py empaquetar` y, salvo "conservar", borra la carpeta.

Sin fixture.json solo copia CASO/files/. Solo biblioteca estándar.
"""
import json
import os
import shutil
import sys
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, "skills", "startup-engineering-chile")
sys.path.insert(0, os.path.join(SKILL, "scripts"))

from core.config import REGISTROS, SCHEMA_VERSION  # noqa: E402
from core.estado import texto_estado  # noqa: E402
from core.storage import csv_texto, escribir_atomico, leer  # noqa: E402

FECHA = "2026-11-25"


def copiar_arbol(src, dst):
    for dp, _, fs in os.walk(src):
        rel = os.path.relpath(dp, src)
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in fs:
            shutil.copy2(os.path.join(dp, f), os.path.join(dst, rel, f))


def base_vacia(dst, capa):
    e = os.path.join(dst, "expediente")
    for sub in ("registros", "documentos", "entregables", "investigacion"):
        os.makedirs(os.path.join(e, sub), exist_ok=True)
    fecha = capa.get("fecha", FECHA)
    nivel = capa.get("nivel", "sprint")
    escribir_atomico(os.path.join(e, "00_estado.md"),
                     texto_estado(capa.get("proyecto", "Proyecto"), capa.get("modo", "empezar"), nivel, hoy=fecha))
    escribir_atomico(os.path.join(e, "manifest.json"), json.dumps(
        {"schema_version": SCHEMA_VERSION, "actualizado": fecha, "nivel": nivel, "creado": fecha}, indent=2) + "\n")
    for reg in capa.get("registros", ["hipotesis", "evidencias"]):
        h, _ = leer(os.path.join(REGISTROS, reg + ".csv"))
        escribir_atomico(os.path.join(e, "registros", reg + ".csv"), csv_texto(h, []), bom=True)


def aplicar_capa(capa, caso, destino):
    dst = os.path.normpath(os.path.join(destino, capa.get("destino", ".")))
    base = capa["base"]
    if base == "demo":
        copiar_arbol(os.path.join(RAIZ, "examples", "expediente_demo", "expediente"), os.path.join(dst, "expediente"))
    elif base == "vacio":
        base_vacia(dst, capa)
    elif base.startswith("_bases/"):
        src = os.path.join(os.path.dirname(caso), base, "expediente")
        if not os.path.isdir(src):
            sys.exit(f"No existe la base {src}")
        copiar_arbol(src, os.path.join(dst, "expediente"))
    else:
        sys.exit(f"Base desconocida: {base} (usa demo, vacio o _bases/<nombre>)")


def empaquetar(conf, destino):
    origen = os.path.normpath(os.path.join(destino, conf.get("origen", ".")))
    e = os.path.join(origen, "expediente")
    salida = os.path.join(destino, conf["salida"])
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fs in os.walk(e):
            dn.sort()
            for f in sorted(fs):
                p = os.path.join(dp, f)
                z.write(p, os.path.relpath(p, origen).replace(os.sep, "/"))
        z.writestr("LEEME.txt", "Expediente empaquetado para una prueba de la skill startup-engineering-chile.\n"
                                "Para retomar: expediente.py restaurar <zip> --dir <carpeta>\n")
    if not conf.get("conservar"):
        shutil.rmtree(e)


def armar(caso, destino):
    caso, destino = os.path.abspath(caso), os.path.abspath(destino)
    os.makedirs(destino, exist_ok=True)
    conf = {}
    fj = os.path.join(caso, "fixture.json")
    if os.path.exists(fj):
        with open(fj, encoding="utf-8") as fh:
            conf = json.load(fh)
    for capa in conf.get("capas", []):
        aplicar_capa(capa, caso, destino)
    files = os.path.join(caso, "files")
    if os.path.isdir(files):
        copiar_arbol(files, destino)
    for rel in conf.get("eliminar", []):
        p = os.path.join(destino, rel)
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)
    if conf.get("empaquetar"):
        empaquetar(conf["empaquetar"], destino)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        sys.exit(__doc__)
    armar(argv[0], argv[1])


if __name__ == "__main__":
    main()
