#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Anonimiza notas o transcripciones de entrevistas antes de analizarlas o guardarlas en el expediente.

  ingesta.py anonimizar ARCHIVO [ARCHIVO ...] --dir RUTA [--nombres "Ana Pérez,Clínica Sur"] [--id ENT-004]
  ingesta.py revisar    ARCHIVO                 # solo informa datos personales, no escribe nada

Acepta .txt, .md y .vtt/.srt (quita marcas de tiempo). Reemplaza correos, teléfonos chilenos, RUT,
URLs de perfiles personales y los nombres que indiques; los hablantes ("Juan:", "<v Juan>") pasan a
Entrevistado/a, Entrevistador/a o Participante N. Guarda el texto en expediente/investigacion/notas/
como <ID>_anon.md, sin el original. Luego el agente propone las filas de entrevistas/evidencias y el
fundador las confirma: el script no inventa contenido ni decide qué es evidencia.

Los nombres propios sueltos no siempre se detectan: el informe final lista palabras con mayúscula
que conviene revisar a mano.
"""
import argparse
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PATRONES = [
    ("[CORREO]", re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")),
    ("[RUT]", re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}\s?-\s?[\dkK]\b")),
    ("[TELÉFONO]", re.compile(r"(\+?56[\s.-]?)?(\(?\d{1,2}\)?[\s.-]?)?9[\s.-]?\d{4}[\s.-]?\d{4}\b|\+?56[\s.-]?\d{1,2}[\s.-]?\d{3,4}[\s.-]?\d{4}\b")),
    ("[PERFIL]", re.compile(r"https?://(www\.)?(linkedin\.com/in|instagram\.com|facebook\.com|x\.com|twitter\.com|wa\.me)/[\w./?=-]+", re.I)),
    ("[DIRECCIÓN]", re.compile(r"\b(calle|av\.?|avenida|pasaje|psje\.?)\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+(\s+[A-ZÁÉÍÓÚÑ]?[\wáéíóúñ]+)*\s+\d{1,5}\b", re.I)),
]
TIEMPO = re.compile(r"^\s*(\d+\s*$|\d{2}:\d{2}(:\d{2})?[.,]\d{3}\s*-->.*$|WEBVTT.*$|NOTE\b.*$)", re.M)
HABLANTE_VTT = re.compile(r"<v\s+([^>]+)>")
HABLANTE = re.compile(r"^([A-ZÁÉÍÓÚÑ][\wáéíóúñ]+(?:\s[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+){0,2})\s*:", re.M)
COMUNES = {"El", "La", "Los", "Las", "Un", "Una", "Yo", "Sí", "Si", "No", "Pero", "Entonces", "Bueno", "Ya", "Y", "O",
           "Que", "Qué", "Cómo", "Como", "Cuando", "Cuándo", "Dónde", "Por", "Para", "Con", "En", "De", "Del", "Al",
           "Eso", "Esto", "Esta", "Este", "Hay", "Es", "Lo", "Le", "Se", "Me", "Mi", "Nos", "Nosotros", "Ellos",
           "Chile", "Santiago", "Excel", "WhatsApp", "Google", "CORFO", "SII", "Entrevistado", "Entrevistada",
           "Entrevistador", "Entrevistadora", "Participante", "Hola", "Gracias", "Ok", "Okay", "También", "Después",
           "Antes", "Ahora", "Hoy", "Ayer", "Mañana", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado",
           "Domingo", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre",
           "Octubre", "Noviembre", "Diciembre", "Nota", "Notas", "Pregunta", "Respuesta", "Hecho", "Cita"}


def limpiar_tiempos(txt):
    txt = TIEMPO.sub("", txt)
    return re.sub(r"\n{3,}", "\n\n", txt)


def anonimizar(txt, nombres=(), entrevistador=None):
    conteo = {}
    txt = limpiar_tiempos(txt)
    txt = HABLANTE_VTT.sub(lambda m: m.group(1) + ": ", txt)
    hablantes = []
    for m in HABLANTE.finditer(txt):
        h = m.group(1)
        if h not in hablantes and h not in COMUNES:
            hablantes.append(h)
    reemplazo_h = {}
    for n, h in enumerate(hablantes):
        if entrevistador and h.lower() == entrevistador.lower():
            reemplazo_h[h] = "Entrevistador/a"
        elif len(hablantes) == 2 and entrevistador:
            reemplazo_h[h] = "Entrevistado/a"
        elif len(hablantes) == 2:
            reemplazo_h[h] = "Entrevistador/a" if n == 0 else "Entrevistado/a"
        else:
            reemplazo_h[h] = f"Participante {n + 1}"
    for h, r in reemplazo_h.items():
        txt = re.sub(r"^" + re.escape(h) + r"\s*:", r + ":", txt, flags=re.M)
        txt, k = re.subn(r"\b" + re.escape(h) + r"\b", r, txt)
        for parte in [x for x in h.split() if len(x) > 2]:  # nombre o apellido suelto
            txt, k2 = re.subn(r"\b" + re.escape(parte) + r"\b", "[NOMBRE]", txt)
            k += k2
        conteo["hablantes"] = conteo.get("hablantes", 0) + 1 + k
    for etiqueta, pat in PATRONES:
        txt, k = pat.subn(etiqueta, txt)
        if k:
            conteo[etiqueta] = k
    for n in [x.strip() for x in nombres if x.strip()]:
        partes = [n] + [p for p in n.split() if len(p) > 2]
        for p in partes:
            txt, k = re.subn(r"\b" + re.escape(p) + r"\b", "[NOMBRE]", txt, flags=re.I)
            if k:
                conteo["[NOMBRE]"] = conteo.get("[NOMBRE]", 0) + k
    return txt, conteo


def sospechosos(txt):
    """Palabras con mayúscula no al inicio de oración, que podrían ser nombres."""
    cand = {}
    for m in re.finditer(r"(?<![.!?:\n]\s)(?<!^)\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,})\b", txt, re.M):
        w = m.group(1)
        if w not in COMUNES:
            cand[w] = cand.get(w, 0) + 1
    return sorted(cand, key=lambda w: -cand[w])[:15]


def cmd_anonimizar(a):
    import expediente as ex
    ex.requiere_expediente(a.dir)
    nombres = a.nombres.split(",") if a.nombres else []
    for i, arch in enumerate(a.archivos):
        txt = open(arch, encoding="utf-8-sig", errors="replace").read()
        anon, conteo = anonimizar(txt, nombres, a.entrevistador)
        eid = a.id if (a.id and len(a.archivos) == 1) else ex.siguiente_id(a.dir, "entrevistas")
        if a.id and len(a.archivos) > 1:
            n = int(a.id.split("-")[-1]) + i
            eid = f"ENT-{n:03d}"
        dst = os.path.join(ex.exp_dir(a.dir), "investigacion", "notas", f"{eid}_anon.md")
        if os.path.exists(dst):
            sys.exit(f"Ya existe {dst}; usa otro --id.")
        cab = (f"# {eid} — notas anonimizadas\n\n> Origen: {os.path.basename(arch)} (el original no se guarda en el expediente). "
               f"Reemplazos: {', '.join(f'{k}×{v}' for k, v in conteo.items()) or 'ninguno'}.\n\n")
        ex.escribir_atomico(dst, cab + anon.strip() + "\n")
        print(f"Creado {dst}")
        resto = ex.buscar_pii(anon)
        if resto:
            print(f"  ⚠ aún parece haber {', '.join(resto)}: revisa a mano.")
        sos = sospechosos(anon)
        if sos:
            print(f"  Revisa si son nombres de personas u organizaciones identificables: {', '.join(sos)}")
            print("  (si lo son, vuelve a correr con --nombres \"...\" sobre el original)")
    print("\nSiguiente: lee las notas anonimizadas, propone filas (expediente.py add entrevistas …) y pide confirmación.")


def cmd_revisar(a):
    import expediente as ex
    txt = open(a.archivo, encoding="utf-8-sig", errors="replace").read()
    _, conteo = anonimizar(txt)
    print("Datos personales detectados: " + (", ".join(f"{k}×{v}" for k, v in conteo.items()) or "ninguno"))
    pii = ex.buscar_pii(txt)
    if pii:
        print("Contiene " + ", ".join(pii) + ": anonimiza antes de guardarlo o compartirlo.")
    sos = sospechosos(limpiar_tiempos(txt))
    if sos:
        print("Posibles nombres: " + ", ".join(sos))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("anonimizar"); p.add_argument("archivos", nargs="+"); p.add_argument("--dir", default=".")
    p.add_argument("--nombres"); p.add_argument("--id"); p.add_argument("--entrevistador"); p.set_defaults(f=cmd_anonimizar)
    p = sp.add_parser("revisar"); p.add_argument("archivo"); p.set_defaults(f=cmd_revisar)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
