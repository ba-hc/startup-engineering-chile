"""Catálogo de plantillas: troncales completas en assets/plantillas/ y el resto como esqueleto desde el catálogo."""
import os
import re
import unicodedata

from .config import PLANTILLAS
from .storage import leer

CATALOGO = os.path.join(PLANTILLAS, "catalogo_plantillas.csv")


def normalizar_tpl(tpl_id):
    tpl_id = tpl_id.upper()
    if re.fullmatch(r"TPL-?\d{1,3}", tpl_id):
        tpl_id = "TPL-" + tpl_id.split("-")[-1].replace("TPL", "").zfill(3)
    return tpl_id


def template_path(tpl_id):
    tpl_id = normalizar_tpl(tpl_id)
    for root, _, files in os.walk(PLANTILLAS):
        for f in files:
            if f.upper().startswith(tpl_id + "_"):
                return os.path.join(root, f)
    return None


def catalogo():
    h, rows = leer(CATALOGO)
    return [dict(zip(h, r)) for r in rows]


def catalogo_fila(tpl_id):
    tpl_id = normalizar_tpl(tpl_id)
    for d in catalogo():
        if d.get("id") == tpl_id:
            return d
    return None


def contar_troncales():
    return sum(1 for _, _, fs in os.walk(PLANTILLAS) for f in fs if re.match(r"TPL-\d{3}_.*\.md$", f))


def slug(texto):
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")[:60]


def esqueleto_plantilla(d):
    """Las plantillas no troncales viven solo en el catálogo: se genera un esqueleto breve con el mismo encabezado pedagógico."""
    return "\n".join([
        f"# {d['id']} — {d['nombre']}", "",
        f"> **Para qué sirve:** {d['uso']}",
        "> **Cuándo NO usarla:** [completa: en qué situación esta plantilla sería una pérdida de tiempo]",
        "> **Micro-ejemplo resuelto:** [un ejemplo ficticio de dos líneas con cifras]", "",
        f"*Plantilla no troncal: estructúrala según la guía del dominio «{d['dominio']}» en `references/manual/` y los "
        "ejemplos de `references/ejemplos_y_umbrales.md`. Cada afirmación con su ID de evidencia o marcada como supuesto.*", "",
        "## Completar", "[ ]", "",
        "## Criterio de aceptación", f"- {d['criterio_aceptacion']}", "",
        "## Decisión",
        "Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]",
        ""])
