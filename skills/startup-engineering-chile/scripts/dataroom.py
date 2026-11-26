#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Sala de datos (data room) desde el expediente: checklist de 9 carpetas, cifras sin evidencia y paquete para compartir.

  dataroom.py revisar --dir RUTA                 # qué hay y qué falta por carpeta + cifras del pitch/one-pager sin EV-
  dataroom.py armar   --dir RUTA [--zip]         # copia a expediente/entregables/dataroom/ con índice (y ZIP opcional)

Carpetas (TPL-092): 1 societario · 2 capital · 3 propiedad intelectual · 4 comercial · 5 financiero y tributario ·
6 laboral · 7 producto y datos · 8 subsidios · 9 contingencias. Reconoce archivos por nombre (p. ej. TPL-034, pacto,
estatutos, cap_table, TPL-110, F29). Nunca copia notas de entrevistas ni registros con datos de personas, y avisa si
algún archivo copiado parece tener correos, teléfonos o RUT. Comparte la carpeta con permisos, no por correo.
"""
import argparse
import os
import re
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.registros import filas  # noqa: E402
from core.schemas import buscar_pii  # noqa: E402
from core.storage import escribir_atomico, exp_dir, nombre_proyecto, requiere_expediente  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# carpeta -> [(documento, patrón de nombre de archivo, acceso sugerido)]
CARPETAS = [
    ("1_societario", [("Estatutos y modificaciones", r"estatut|escritura|constituci", "todos"),
                      ("Pacto de accionistas / acuerdo de socios", r"TPL-034|pacto|acuerdo_de_socios", "todos"),
                      ("Certificado de vigencia y poderes", r"vigencia|poder", "tras term sheet")]),
    ("2_capital", [("Cap table", r"TPL-091|cap_table", "todos"),
                   ("SAFE, notas, opciones o term sheet", r"TPL-109|safe|term_sheet|opcion", "tras term sheet")]),
    ("3_propiedad_intelectual", [("Cesiones de PI de socios y freelancers", r"cesi[oó]n|propiedad_intelectual|TPL-095", "tras term sheet"),
                                 ("Marcas y dominios", r"inapi|marca|dominio", "todos")]),
    ("4_comercial", [("Contratos y órdenes de compra", r"contrato|orden_de_compra|\bOC\b", "solo abogados"),
                     ("Cartas de intención", r"TPL-110|carta_de_intencion|\bLOI\b", "tras term sheet"),
                     ("Pipeline de cuentas", r"cuentas_y_pipeline|TPL-083", "tras term sheet"),
                     ("Pilotos con resultado", r"pilotos|TPL-067", "tras term sheet")]),
    ("5_financiero_tributario", [("Modelo financiero", r"modelo_financiero", "todos"),
                                 ("Economía unitaria y flujo de caja", r"TPL-087|TPL-088|flujo_de_caja|unit", "todos"),
                                 ("Estados financieros y F29", r"balance|estado_financ|eerr|f29|carpeta_tributaria", "tras term sheet")]),
    ("6_laboral", [("Contratos de trabajo y honorarios", r"contrato_de_trabajo|honorario|anexo_laboral", "solo abogados"),
                   ("Certificado de cotizaciones", r"cotizacion|previred", "tras term sheet")]),
    ("7_producto_y_datos", [("Checklist Ley 21.719 / seguridad", r"TPL-097|privacidad|seguridad", "todos"),
                            ("Dashboard y métricas", r"dashboard|TPL-080|cohort", "todos"),
                            ("One-pager y deck", r"one_pager|deck", "todos")]),
    ("8_subsidios", [("Convenios y rendiciones de fondos", r"rendiciones|convenio|TPL-105|TPL-106", "tras term sheet")]),
    ("9_contingencias", [("Juicios, reclamos, deudas y garantías", r"juicio|reclamo|contingencia|garant", "solo abogados")]),
]
EXCLUIR = re.compile(r"(^|[\\/])(investigacion[\\/]notas|\.lock|.*\.bak|.*\.tmp)|entrevistas\.csv$|bitacora\.csv$|dataroom", re.I)
CIFRA = re.compile(r"(\$\s?\d|\d[\d.,]*\s?(%|clientes|usuarios|MRR|ARR|UF|millones|M\b))", re.I)
MARCA = re.compile(r"EV-\d+|\[SIN RESPALDO\]|\[FALTA EVIDENCIA\]|supuesto|hipot", re.I)


def archivos(base):
    e = exp_dir(base)
    out = []
    for dp, dn, fs in os.walk(e):
        dn[:] = [d for d in dn if d not in ("__pycache__",)]
        for f in fs:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, e).replace(os.sep, "/")
            if not EXCLUIR.search(rel):
                out.append((rel, p))
    return sorted(out)


def clasificar(base):
    arch = archivos(base)
    res = []
    for carpeta, docs in CARPETAS:
        for nombre, pat, acceso in docs:
            hits = [(r, p) for r, p in arch if re.search(pat, os.path.basename(r), re.I)]
            res.append((carpeta, nombre, acceso, hits))
    return res


def cifras_sin_respaldo(base):
    """[(archivo, n_línea, línea)] de one-pager, deck y pitch con cifras sin EV- existente ni marca de supuesto."""
    ev = {d.get("evidence_id", "") for d in filas(base, "evidencias")}
    out = []
    for rel, p in archivos(base):
        if not re.search(r"one_pager|deck|pitch|TPL-04[0-9]_.*pitch", os.path.basename(rel), re.I) or not rel.endswith(".md"):
            continue
        with open(p, encoding="utf-8-sig", errors="replace") as fh:
            for i, linea in enumerate(fh, 1):
                if not CIFRA.search(linea) or re.match(r"\s*(>|#|\|?\s*-{3})", linea):
                    continue
                citados = re.findall(r"EV-\d+", linea)
                if any(c not in ev for c in citados):
                    out.append((rel, i, linea.strip()[:140] + f"  ← cita {', '.join(c for c in citados if c not in ev)} que no existe"))
                elif not MARCA.search(linea):
                    out.append((rel, i, linea.strip()[:140]))
    return out


def cmd_revisar(a):
    requiere_expediente(a.dir)
    res = clasificar(a.dir)
    print(f"# Data room — {nombre_proyecto(a.dir)}\n\n| Carpeta | Documento | ¿Está? | Acceso sugerido |\n|---|---|---|---|")
    faltan = 0
    for carpeta, nombre, acceso, hits in res:
        estado = ", ".join(r for r, _ in hits[:2]) if hits else "FALTA"
        faltan += not hits
        print(f"| {carpeta} | {nombre} | {estado} | {acceso} |")
    sin = cifras_sin_respaldo(a.dir)
    print(f"\n{faltan} documento(s) faltante(s) de {len(res)}. Registra cada vacío como riesgo: "
          "expediente.py add bitacora tipo=riesgo titulo=… responsable=… revision=AAAA-MM-DD")
    if sin:
        print("\n## Cifras del material de inversión sin EV- (respáldalas o márcalas como supuesto)")
        for rel, i, l in sin:
            print(f"- {rel}:{i}: {l}")
    else:
        print("\nCifras del one-pager y del deck: todas citan un EV- existente o están marcadas.")
    sys.exit(1 if sin else 0)


def cmd_armar(a):
    requiere_expediente(a.dir)
    destino = os.path.join(exp_dir(a.dir), "entregables", "dataroom")
    if os.path.exists(destino):
        shutil.rmtree(destino)
    indice = [f"# Data room — {nombre_proyecto(a.dir)}\n", "> Generado por dataroom.py desde el expediente. Revisa cada archivo antes de compartir; "
              "da acceso por carpeta según la columna «Acceso».\n", "| Carpeta | Documento | Archivo | Acceso |", "|---|---|---|---|"]
    pii, n = [], 0
    for carpeta, nombre, acceso, hits in clasificar(a.dir):
        os.makedirs(os.path.join(destino, carpeta), exist_ok=True)
        if not hits:
            indice.append(f"| {carpeta} | {nombre} | **FALTA** | {acceso} |")
        for rel, p in hits:
            dst = os.path.join(destino, carpeta, os.path.basename(p))
            shutil.copy2(p, dst)
            n += 1
            indice.append(f"| {carpeta} | {nombre} | {carpeta}/{os.path.basename(p)} | {acceso} |")
            if p.endswith((".md", ".csv", ".txt", ".html")):
                with open(p, encoding="utf-8-sig", errors="replace") as fh:
                    hallado = buscar_pii(fh.read())
                if hallado:
                    pii.append((rel, hallado))
    escribir_atomico(os.path.join(destino, "00_indice.md"), "\n".join(indice) + "\n")
    print(f"Data room armado en {destino} ({n} archivo(s) copiados; índice en 00_indice.md)")
    for rel, h in pii:
        print(f"⚠ {rel} parece contener {', '.join(h)}: quítalo o anonimízalo antes de compartir.")
    if a.zip:
        z = destino + ".zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for dp, _, fs in os.walk(destino):
                for f in sorted(fs):
                    p = os.path.join(dp, f)
                    zf.write(p, os.path.relpath(p, os.path.dirname(destino)).replace(os.sep, "/"))
        print(f"ZIP: {z}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("revisar"); p.add_argument("--dir", default="."); p.set_defaults(f=cmd_revisar)
    p = sp.add_parser("armar"); p.add_argument("--dir", default="."); p.add_argument("--zip", action="store_true"); p.set_defaults(f=cmd_armar)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
