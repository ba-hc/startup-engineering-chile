"""Núcleo del expediente (paquete interno de la skill Startup Engineering Chile).

Módulos:
  config     rutas de la skill, gates y versión de esquema
  storage    lectura/escritura atómica de CSV y JSON, bloqueo del expediente, 00_estado.md
  schemas    esquemas de registros (8 núcleo + rendiciones + bitácora), tipos, monedas y validación
  registros  agregar filas, IDs, bitácora con compatibilidad de registros antiguos, migración
  estado     plantilla de 00_estado.md, acciones, misión de 7 días, onboarding
  gates      umbrales por gate y evaluación determinista contra el expediente
  exporters  informes Markdown, Excel (.xlsx), HTML y ZIP
  busqueda   BM25 sobre manual/flujos/plantillas y catálogo de fuentes
  plantillas catálogo y copia de plantillas

Solo biblioteca estándar (Python 3.8+). Los scripts de `scripts/` lo importan; `expediente.py` es el CLI.
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
