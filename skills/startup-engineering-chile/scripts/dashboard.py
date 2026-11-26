#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Compila el expediente en un solo dashboard.html interactivo y autocontenido (sin servidor, sin internet, sin librerías externas).

  dashboard.py --dir RUTA [--salida expediente/entregables/dashboard.html]

Muestra: barra de progreso por gate (chequeos de `expediente.py gate`, clic para ver el detalle), runway en meses con
semáforo, embudo de validación Hipótesis → Experimentos → Evidencias → Decisiones, embudo comercial, misión de 7 días,
semáforo de alertas, tablas ordenables y un filtro de texto. Se abre con doble clic, se imprime a PDF o se envía.
Ojo: incluye lo que hay en el expediente; revisa que no tenga datos confidenciales antes de compartir.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import exporters  # noqa: E402
from core.storage import escribir_atomico, exp_dir  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def construir(base):
    """HTML completo del dashboard (compatibilidad con la v1)."""
    return exporters.dashboard_html(base)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=".")
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    dst = a.salida or os.path.join(exp_dir(a.dir), "entregables", "dashboard.html")
    escribir_atomico(dst, construir(a.dir))
    print(f"Creado {dst}")


if __name__ == "__main__":
    main()
