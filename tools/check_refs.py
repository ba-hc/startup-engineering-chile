#!/usr/bin/env python3
"""Integridad del paquete: rutas citadas existen, archivos en UTF-8, nombres ASCII, versiones sincronizadas.

  python tools/check_refs.py        # sale con código 1 si encuentra problemas (lo usa la CI)
"""
import csv
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, "skills", "startup-engineering-chile")
TEXTO = (".md", ".csv", ".py", ".json", ".yaml", ".yml", ".txt")
# `references/x.md`, `assets/...`, `scripts/x.py` dentro de backticks o enlaces markdown
RUTA = re.compile(r"[`(]((?:references|assets|scripts)/[\w./*-]+?)[`)\s:]")


def main():
    problemas = []
    for dp, dn, fs in os.walk(RAIZ):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", ".venv", "node_modules")]
        for f in fs:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, RAIZ)
            if p.startswith(SKILL) and not f.isascii():
                problemas.append(f"nombre no ASCII: {rel}")
            if f.endswith(TEXTO):
                try:
                    txt = open(p, encoding="utf-8-sig").read()
                except UnicodeDecodeError as e:
                    problemas.append(f"no es UTF-8: {rel} ({e})")
                    continue
                if p.startswith(SKILL) and f.endswith(".md"):
                    base = SKILL
                    for m in RUTA.finditer(txt):
                        ruta = m.group(1).rstrip(".")
                        if "*" in ruta or "NN_" in ruta or "<" in ruta or ruta.endswith("/"):
                            continue
                        if not os.path.exists(os.path.join(base, ruta)):
                            problemas.append(f"{rel}: cita {ruta}, que no existe")
    for cat, col, carpeta in (("assets/plantillas/catalogo_plantillas.csv", "ruta", "assets/plantillas"),
                              ("references/manual/indice_modulos.csv", "archivo", "references/manual")):
        with open(os.path.join(SKILL, cat), encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                if not os.path.exists(os.path.join(SKILL, carpeta, r[col])):
                    problemas.append(f"{cat}: {r[col]} no existe")
    plugin = json.load(open(os.path.join(RAIZ, ".claude-plugin", "plugin.json"), encoding="utf-8"))
    market = json.load(open(os.path.join(RAIZ, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
    if plugin["name"] not in [p["name"] for p in market["plugins"]]:
        problemas.append("plugin.json y marketplace.json no coinciden en el nombre")
    cl = open(os.path.join(RAIZ, "CHANGELOG.md"), encoding="utf-8").read()
    if f"## [{plugin['version']}]" not in cl:
        problemas.append(f"CHANGELOG.md no tiene entrada para la versión {plugin['version']} de plugin.json")
    fm = open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read().split("---")[1]
    if "name: startup-engineering-chile" not in fm or "description:" not in fm:
        problemas.append("SKILL.md: frontmatter sin name/description")
    desc = re.search(r"description:\s*(.+)", fm).group(1)
    if len(desc) > 1024:
        problemas.append(f"SKILL.md: description de {len(desc)} caracteres (máximo 1024)")
    for p in problemas:
        print("PROBLEMA  " + p)
    print(f"{len(problemas)} problema(s).")
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
