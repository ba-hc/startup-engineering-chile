"""Almacenamiento del expediente: escritura atómica, bloqueo entre procesos, CSV con BOM, manifest y 00_estado.md."""
import contextlib
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import tempfile
import time

from .config import SCHEMA_VERSION

LOCK = ".lock"
_TOMADOS = {}


def exp_dir(base):
    return os.path.join(os.path.abspath(base), "expediente")


def reg_path(base, reg):
    return os.path.join(exp_dir(base), "registros", reg.replace(".csv", "") + ".csv")


def escribir_atomico(path, texto, bom=False):
    """Escribe en un temporal y reemplaza: si se corta a la mitad, el archivo original queda intacto."""
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp_", suffix=os.path.splitext(path)[1])
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as fh:
            fh.write(texto)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def escribir_bytes_atomico(path, datos):
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp_", suffix=os.path.splitext(path)[1])
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(datos)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


@contextlib.contextmanager
def bloqueo(base, espera=10.0, vencido=120.0):
    """Bloqueo exclusivo del expediente (archivo expediente/.lock creado con O_EXCL, funciona en Windows y POSIX).

    Evita que dos procesos (dos agentes, o el agente y un script) hagan leer-modificar-escribir a la vez sobre
    el mismo CSV. Un bloqueo más antiguo que `vencido` segundos se considera abandonado y se reemplaza.
    """
    e = exp_dir(base)
    if not os.path.isdir(e):
        yield
        return
    path = os.path.abspath(os.path.join(e, LOCK))
    if _TOMADOS.get(path):  # reentrante dentro del mismo proceso (p. ej. migrar → agregar)
        _TOMADOS[path] += 1
        try:
            yield
        finally:
            _TOMADOS[path] -= 1
        return
    inicio = time.time()
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{os.getpid()} {dt.datetime.now().isoformat(timespec='seconds')}".encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(path) > vencido:
                    os.remove(path)
                    continue
            except OSError:
                pass
            if time.time() - inicio > espera:
                sys.exit(f"El expediente está en uso por otro proceso ({path}). Si no hay otro proceso trabajando, borra ese archivo.")
            time.sleep(0.05)
    _TOMADOS[path] = 1
    try:
        yield
    finally:
        _TOMADOS.pop(path, None)
        try:
            os.remove(path)
        except OSError:
            pass


def csv_texto(header, rows, delimiter=","):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue()


def tiene_bom(path):
    with open(path, "rb") as fh:
        return fh.read(3) == b"\xef\xbb\xbf"


def leer(path):
    """Devuelve (header, filas). Tolera BOM, archivos vacíos y filas en blanco."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return [], []
    return rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]


def leer_seguro(path):
    """Como leer(), pero devuelve (header, filas, error) sin lanzar excepción."""
    try:
        h, r = leer(path)
        return h, r, None
    except (UnicodeDecodeError, csv.Error, OSError) as e:
        return [], [], f"{type(e).__name__}: {e}"


def manifest_path(base):
    return os.path.join(exp_dir(base), "manifest.json")


def leer_manifest(base):
    p = manifest_path(base)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        except (ValueError, OSError):
            return {"schema_version": 0, "corrupto": True}
    return {"schema_version": 1} if os.path.isdir(exp_dir(base)) else None


def escribir_manifest(base, **extra):
    m = leer_manifest(base) or {}
    m.pop("corrupto", None)
    m.update({"schema_version": SCHEMA_VERSION, "actualizado": dt.date.today().isoformat()}, **extra)
    m.setdefault("creado", dt.date.today().isoformat())
    escribir_atomico(manifest_path(base), json.dumps(m, ensure_ascii=False, indent=2) + "\n")


def estado_path(base):
    return os.path.join(exp_dir(base), "00_estado.md")


def leer_estado(base):
    p = estado_path(base)
    if not os.path.exists(p):
        return ""
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def seccion(txt, titulo):
    m = re.search(r"^## " + re.escape(titulo) + r"\s*\n(.*?)(?=^#{2,3} |\Z)", txt, re.M | re.S)
    return m.group(1).strip() if m else ""


def campo(txt, etiqueta):
    """Valor de una línea '- **Etiqueta:** valor' (cadena vacía si no está o está vacía)."""
    m = re.search(r"\*\*" + re.escape(etiqueta) + r"[^*]*:\*\*[ \t]*(.*)", txt)
    return m.group(1).strip() if m else ""


def nombre_proyecto(base):
    m = re.search(r"^# Expediente: (.+)$", leer_estado(base), re.M)
    return m.group(1).strip() if m else ""


def requiere_expediente(base):
    if not os.path.isdir(exp_dir(base)):
        sys.exit("No hay expediente. Ejecuta primero: expediente.py init --dir <carpeta> --proyecto \"Nombre\" "
                 "(o expediente.py onboarding) — solo si el usuario quiere guardar el proyecto.")
