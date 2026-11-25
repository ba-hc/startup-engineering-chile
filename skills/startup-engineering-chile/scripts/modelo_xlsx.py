#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Lee y edita los supuestos de modelo_financiero.xlsx sin romper fórmulas (solo biblioteca estándar).

  modelo_xlsx.py leer      ARCHIVO [--hoja Supuestos] [--json]   # variable, valor, unidad, celda
  modelo_xlsx.py set       ARCHIVO "Precio mensual=250000" ["Churn mensual=0.03" ...]
                                   [--hoja Supuestos]             # por etiqueta de la columna A
  modelo_xlsx.py set       ARCHIVO Supuestos!B4=250000            # o por celda
  modelo_xlsx.py verificar ARCHIVO                                # fórmulas, hojas referidas, entradas

Reglas: solo cambia celdas con valor constante (nunca una con fórmula), deja un respaldo .bak,
escribe de forma atómica y marca el libro para que Excel/LibreOffice recalculen al abrir.
Los valores calculados guardados en el archivo quedan desactualizados hasta abrirlo: para cifras
inmediatas usa finanzas.py escenarios --modelo ARCHIVO.
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

CELDA = re.compile(r'<(?P<p>\w+:)?c r="(?P<ref>[A-Z]+\d+)"(?P<attr>[^>]*?)(?:/>|>(?P<inner>.*?)</(?P=p)?c>)', re.S)


def _hojas(z):
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    rmap = {}
    for m in re.finditer(r"<(?:\w+:)?Relationship\b([^>]*)/?>", rels):
        at = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        rmap[at.get("Id")] = at.get("Target", "").lstrip("/")
    out = {}
    for m in re.finditer(r"<(?:\w+:)?sheet\b([^>]*)/?>", wb):
        at = dict(re.findall(r'([\w:]+)="([^"]*)"', m.group(1)))
        tgt = rmap.get(at.get("r:id"), "")
        out[at["name"]] = tgt if tgt.startswith("xl/") else "xl/" + tgt
    return out


def _shared(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    x = z.read("xl/sharedStrings.xml").decode("utf-8")
    return [re.sub(r"<[^>]+>", "", s) for s in re.findall(r"<(?:\w+:)?si>(.*?)</(?:\w+:)?si>", x, re.S)]


def _texto(m, shared):
    inner, attr = m.group("inner") or "", m.group("attr")
    t = re.search(r"<(?:\w+:)?t[^>]*>(.*?)</(?:\w+:)?t>", inner, re.S)
    if t:
        return t.group(1)
    v = re.search(r"<(?:\w+:)?v>(.*?)</(?:\w+:)?v>", inner)
    if v and 't="s"' in attr:
        return shared[int(v.group(1))]
    return v.group(1) if v else ""


def celdas(path, hoja):
    with zipfile.ZipFile(path) as z:
        hs = _hojas(z)
        if hoja not in hs:
            sys.exit(f"No existe la hoja '{hoja}'. Hojas: {', '.join(hs)}")
        x = z.read(hs[hoja]).decode("utf-8")
        shared = _shared(z)
    out = {}
    for m in CELDA.finditer(x):
        f = re.search(r"<(?:\w+:)?f>(.*?)</(?:\w+:)?f>", m.group("inner") or "", re.S)
        out[m.group("ref")] = {"valor": _texto(m, shared), "formula": f.group(1) if f else None}
    return out


def supuestos(path, hoja="Supuestos"):
    """Lista de dicts {variable, valor, unidad, celda, formula} leyendo columnas A-B-C."""
    c = celdas(path, hoja)
    filas = sorted({int(re.sub(r"[A-Z]", "", r)) for r in c})
    out = []
    for n in filas:
        a, b = c.get(f"A{n}"), c.get(f"B{n}")
        if not a or not b or n <= 3:
            continue
        out.append({"variable": a["valor"], "valor": b["valor"], "unidad": (c.get(f"C{n}") or {}).get("valor", ""),
                    "celda": f"B{n}", "formula": b["formula"]})
    return out


def numero(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def cmd_leer(a):
    filas = supuestos(a.archivo, a.hoja)
    if a.json:
        print(json.dumps(filas, ensure_ascii=False, indent=2))
        return
    print("| Variable | Valor | Unidad | Celda |\n|---|---|---|---|")
    for f in filas:
        val = ("=" + f["formula"]) if f["formula"] else f["valor"]
        print(f"| {f['variable']} | {val} | {f['unidad']} | {a.hoja}!{f['celda']} |")


def _normaliza(s):
    import unicodedata
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def cmd_set(a):
    cambios = {}  # (hoja, celda) -> valor
    for asig in a.asignaciones:
        if "=" not in asig:
            sys.exit(f"Formato inválido '{asig}': usa \"Etiqueta=valor\" o Hoja!B4=valor")
        izq, val = asig.rsplit("=", 1)
        izq, val = izq.strip(), val.strip().replace(",", ".") if re.fullmatch(r"-?\d+,\d+", val.strip()) else val.strip()
        if numero(val) is None:
            sys.exit(f"'{val}' no es un número (usa punto o coma decimal, sin separador de miles).")
        m = re.fullmatch(r"(?:(?P<h>[^!]+)!)?(?P<c>[A-Z]+\d+)", izq)
        if m:
            cambios[(m.group("h") or a.hoja, m.group("c"))] = val
            continue
        cand = [f for f in supuestos(a.archivo, a.hoja) if _normaliza(f["variable"]) == _normaliza(izq)]
        if not cand:
            nombres = ", ".join(f["variable"] for f in supuestos(a.archivo, a.hoja))
            sys.exit(f"No encontré la variable '{izq}' en {a.hoja}. Disponibles: {nombres}")
        cambios[(a.hoja, cand[0]["celda"])] = val
    with zipfile.ZipFile(a.archivo) as z:
        hs = _hojas(z)
        contenido = {n: z.read(n) for n in z.namelist()}
        infos = {i.filename: i for i in z.infolist()}
    por_hoja = {}
    for (h, c), v in cambios.items():
        if h not in hs:
            sys.exit(f"No existe la hoja '{h}'.")
        por_hoja.setdefault(hs[h], []).append((h, c, v))
    for parte, lista in por_hoja.items():
        x = contenido[parte].decode("utf-8")
        for h, c, v in lista:
            m = next((m for m in CELDA.finditer(x) if m.group("ref") == c), None)
            if not m:
                sys.exit(f"{h}!{c} no existe o está vacía; solo edito celdas de entrada existentes.")
            inner = m.group("inner") or ""
            if re.search(r"<(?:\w+:)?f>", inner):
                sys.exit(f"{h}!{c} tiene una fórmula: no se edita. Cambia el supuesto que la alimenta.")
            p = m.group("p") or ""
            attr = re.sub(r'\s*t="[^"]*"', "", m.group("attr"))
            nueva = f'<{p}c r="{c}"{attr} t="n"><{p}v>{escape(v)}</{p}v></{p}c>'
            x = x[:m.start()] + nueva + x[m.end():]
            print(f"{h}!{c} = {v}")
        contenido[parte] = x.encode("utf-8")
    wb = contenido["xl/workbook.xml"].decode("utf-8")
    if "fullCalcOnLoad" not in wb:
        pref = re.match(r"<\?xml[^>]*\?>\s*<(\w+:)?workbook", wb)
        p = (pref.group(1) or "") if pref else ""
        if re.search(r"<(?:\w+:)?calcPr\b", wb):
            wb = re.sub(r"<((?:\w+:)?calcPr)\b", r'<\1 fullCalcOnLoad="1"', wb, count=1)
        else:
            wb = re.sub(r"(</(?:\w+:)?sheets>)", r'\1<' + p + 'calcPr fullCalcOnLoad="1"/>', wb, count=1)
        contenido["xl/workbook.xml"] = wb.encode("utf-8")
    shutil.copy2(a.archivo, a.archivo + ".bak")
    d = os.path.dirname(os.path.abspath(a.archivo))
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".xlsx")
    os.close(fd)
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for n, data in contenido.items():
                z.writestr(infos[n], data)
        os.replace(tmp, a.archivo)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    print(f"Guardado {a.archivo} (respaldo .bak). Excel recalculará al abrir; cifras inmediatas: finanzas.py escenarios --modelo")


def cmd_verificar(a):
    problemas, n_f, entradas = [], 0, 0
    with zipfile.ZipFile(a.archivo) as z:
        bad = z.testzip()
        if bad:
            sys.exit(f"Archivo dañado: {bad}")
        hs = _hojas(z)
    for h in hs:
        for ref, c in celdas(a.archivo, h).items():
            if c["formula"]:
                n_f += 1
                for hoja_ref in re.findall(r"(?:'([^']+)'|([A-Za-z_]\w*))!\$?[A-Z]+\$?\d+", c["formula"]):
                    nombre = hoja_ref[0] or hoja_ref[1]
                    if nombre not in hs:
                        problemas.append(f"{h}!{ref}: referencia a hoja inexistente '{nombre}'")
                if re.search(r"#REF!|#NAME\?|#DIV/0!", c["formula"] + (c["valor"] or "")):
                    problemas.append(f"{h}!{ref}: error ({c['valor'] or c['formula']})")
            elif h == "Supuestos" and numero(c["valor"]) is not None:
                entradas += 1
    for f in supuestos(a.archivo):
        v = numero(f["valor"])
        u = f["unidad"].lower()
        if v is not None and ("fracción" in u or "fraccion" in u) and not 0 <= v <= 1:
            problemas.append(f"Supuestos!{f['celda']} {f['variable']}={v}: una fracción debe estar entre 0 y 1")
        if v is not None and v < 0:
            problemas.append(f"Supuestos!{f['celda']} {f['variable']}={v}: valor negativo")
    print(f"Hojas: {', '.join(hs)}\nFórmulas: {n_f} · entradas numéricas en Supuestos: {entradas}")
    for p in problemas:
        print("PROBLEMA  " + p)
    print("Sin problemas." if not problemas else f"{len(problemas)} problema(s).")
    sys.exit(1 if problemas else 0)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("leer"); p.add_argument("archivo"); p.add_argument("--hoja", default="Supuestos")
    p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_leer)
    p = sp.add_parser("set"); p.add_argument("archivo"); p.add_argument("asignaciones", nargs="+")
    p.add_argument("--hoja", default="Supuestos"); p.set_defaults(f=cmd_set)
    p = sp.add_parser("verificar"); p.add_argument("archivo"); p.set_defaults(f=cmd_verificar)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
