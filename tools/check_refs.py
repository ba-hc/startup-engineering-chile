#!/usr/bin/env python3
"""Integridad del paquete: rutas citadas y enlaces Markdown existen, archivos en UTF-8, nombres ASCII,
versiones sincronizadas, SKILL.md liviano y comandos con descripción.

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
# [texto](destino) fuera de bloques de código; se ignoran URLs, anclas y correos
ENLACE = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\s]+)\)")
SKILL_MAX_LINEAS = 350
SKILL_MAX_CARACTERES = 6500


def enlaces_rotos(p, txt):
    """Enlaces relativos de un .md que no apuntan a un archivo o carpeta existente."""
    sin_codigo = re.sub(r"```.*?```", "", txt, flags=re.S)
    sin_codigo = re.sub(r"`[^`\n]*`", "", sin_codigo)
    malos = []
    for m in ENLACE.finditer(sin_codigo):
        dest = m.group(1)
        if re.match(r"^(https?:|mailto:|#|<)", dest):
            continue
        dest = re.sub(r"[#?].*$", "", dest)
        dest = re.sub(r":\d+$", "", dest)
        if dest and not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), dest))):
            malos.append(dest)
    return malos


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
                if f.endswith(".md"):
                    for dest in enlaces_rotos(p, txt):
                        problemas.append(f"{rel}: enlace a {dest}, que no existe")
                comando = os.path.basename(dp) == "commands" and os.path.dirname(dp) == RAIZ
                if f.endswith(".md") and (p.startswith(SKILL) or comando):
                    base = SKILL
                    for m in RUTA.finditer(txt):
                        ruta = m.group(1).rstrip(".")
                        if "*" in ruta or "NN_" in ruta or "<" in ruta or ruta.endswith("/"):
                            continue
                        if not os.path.exists(os.path.join(base, ruta)):
                            problemas.append(f"{rel}: cita {ruta}, que no existe")
    for cat, col, carpeta in (("assets/plantillas/catalogo_plantillas.csv", "ruta", "assets/plantillas"),):
        with open(os.path.join(SKILL, cat), encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                if not r[col]:
                    if r.get("troncal") == "si":
                        problemas.append(f"{cat}: {r['id']} es troncal y no tiene archivo")
                    continue
                if not os.path.exists(os.path.join(SKILL, carpeta, r[col])):
                    problemas.append(f"{cat}: {r[col]} no existe")
    plugin = json.load(open(os.path.join(RAIZ, ".claude-plugin", "plugin.json"), encoding="utf-8"))
    market = json.load(open(os.path.join(RAIZ, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
    if plugin["name"] not in [p["name"] for p in market["plugins"]]:
        problemas.append("plugin.json y marketplace.json no coinciden en el nombre")
    for m in market["plugins"]:
        if m.get("version") and m["version"] != plugin["version"]:
            problemas.append(f"marketplace.json declara la versión {m['version']} y plugin.json {plugin['version']}")
    pyproject = os.path.join(RAIZ, "pyproject.toml")
    if os.path.exists(pyproject):
        v = re.search(r'^version\s*=\s*"([^"]+)"', open(pyproject, encoding="utf-8").read(), re.M)
        if v and v.group(1) != plugin["version"]:
            problemas.append(f"pyproject.toml declara la versión {v.group(1)} y plugin.json {plugin['version']}")
    cl = open(os.path.join(RAIZ, "CHANGELOG.md"), encoding="utf-8").read()
    if f"## [{plugin['version']}]" not in cl:
        problemas.append(f"CHANGELOG.md no tiene entrada para la versión {plugin['version']} de plugin.json")
    skill_txt = open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read()
    fm = skill_txt.split("---")[1]
    cuerpo = skill_txt.split("---", 2)[2]
    if skill_txt.count("\n") > SKILL_MAX_LINEAS or len(cuerpo) > SKILL_MAX_CARACTERES:
        problemas.append(f"SKILL.md: {skill_txt.count(chr(10))} líneas y {len(cuerpo)} caracteres de cuerpo "
                         f"(máximo {SKILL_MAX_LINEAS} y {SKILL_MAX_CARACTERES}: es un enrutador; el detalle va a references/)")
    cmd_dir = os.path.join(RAIZ, "commands")
    for f in sorted(os.listdir(cmd_dir)) if os.path.isdir(cmd_dir) else []:
        if f.endswith(".md"):
            head = open(os.path.join(cmd_dir, f), encoding="utf-8").read().split("---")
            if len(head) < 3 or not re.search(r"^description:\s*\S", head[1], re.M):
                problemas.append(f"commands/{f}: falta el frontmatter con description")
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
