"""Búsqueda sin internet: BM25 sobre manual, flujos y plantillas, y catálogo de fuentes particionado por tema."""
import math
import os
import re
import unicodedata

from .config import PLANTILLAS, REFS, SKILL_DIR
from .storage import leer

FUENTES = {"publico": "biblioteca/fuentes_publico_corfo.csv", "mercado": "biblioteca/fuentes_mercado_latam.csv",
           "legal": "biblioteca/fuentes_legal_tributario.csv", "metodos": "biblioteca/fuentes_saas_metricas.csv"}
CATALOGOS = {"fuentes": list(FUENTES.values()), "libros": ["biblioteca/libros.csv"], "mentores": ["biblioteca/mentores.csv"],
             "charlas": ["biblioteca/charlas_y_cursos.csv"], "casos": ["casos/casos.csv"], "workshops": ["operacion/workshops.csv"],
             "curriculo": ["operacion/curriculo_360h.csv"], "cifras": ["investigaciones/afirmaciones_y_cifras.csv"]}

STOP = set("que los las del con por para una uno como mas pero sus este esta son ser hay sin sobre entre cuando donde cual "
           "the and for you".split())


def tokens(texto):
    s = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return [t for t in re.findall(r"[a-z0-9]{3,}", s) if t not in STOP]


def bm25(consulta, docs, k1=1.4, b=0.75):
    """docs: lista de (clave, texto). Devuelve [(puntaje, clave, texto)] ordenado, solo con puntaje > 0."""
    q = set(tokens(consulta))
    tok = [(k, t, tokens(t)) for k, t in docs]
    N = len(tok)
    avg = sum(len(d[2]) for d in tok) / max(N, 1)
    df = {t: sum(1 for d in tok if t in set(d[2])) for t in q}
    out = []
    for k, t, toks in tok:
        tf = {}
        for x in toks:
            if x in df:
                tf[x] = tf.get(x, 0) + 1
        s = 0.0
        for term in q:
            if term in tf:
                idf = math.log(1 + (N - df[term] + 0.5) / (df[term] + 0.5))
                s += idf * tf[term] * (k1 + 1) / (tf[term] + k1 * (1 - b + b * len(toks) / max(avg, 1)))
        if s > 0:
            out.append((s, k, t))
    out.sort(key=lambda x: -x[0])
    return out


def corpus(en):
    roots = {"plantillas": [PLANTILLAS], "manual": [REFS], "todo": [PLANTILLAS, REFS]}[en]
    for root in roots:
        for dp, _, fs in os.walk(root):
            for f in sorted(fs):
                if f.endswith((".md", ".csv")):
                    p = os.path.join(dp, f)
                    with open(p, encoding="utf-8-sig", errors="replace") as fh:
                        yield p, fh.read()


def buscar(texto, en="todo", maximo=5):
    """[(puntaje, ruta relativa, [(n_línea, línea)])] con las 2 líneas más pertinentes de cada archivo."""
    res = bm25(texto, list(corpus(en)))
    q = set(tokens(texto))
    out = []
    for s, p, t in res[:maximo]:
        mejores = sorted(((sum(1 for x in tokens(l) if x in q), i, l.strip()) for i, l in enumerate(t.splitlines(), 1) if l.strip()),
                         key=lambda x: (-x[0], x[1]))[:2]
        out.append((s, os.path.relpath(p, SKILL_DIR).replace(os.sep, "/"), [(i, l) for c, i, l in mejores if c]))
    return out


def filas_catalogo(tipo):
    out = []
    for rel in CATALOGOS[tipo]:
        p = os.path.join(REFS, rel)
        if os.path.exists(p):
            h, rows = leer(p)
            out += [dict(zip(h, r)) for r in rows]
    return out


def buscar_fuente(texto, tema=None, maximo=8, solo_verificadas=False):
    """Ranking BM25 sobre las fuentes (una línea por fuente, para no saturar el contexto)."""
    rutas = [FUENTES[tema]] if tema else list(FUENTES.values())
    docs = []
    for rel in rutas:
        p = os.path.join(REFS, rel)
        if not os.path.exists(p):
            continue
        h, rows = leer(p)
        for r in rows:
            d = dict(zip(h, r))
            if solo_verificadas and not d.get("fecha_reconsulta"):
                continue
            d["_archivo"] = os.path.basename(rel)
            docs.append((d, " ".join([d.get("titulo", ""), d.get("autor_institucion", ""), d.get("categoria", ""),
                                      d.get("uso_y_limites", ""), d.get("id", "")])))
    keyed = [(i, t) for i, (_, t) in enumerate(docs)]
    res = bm25(texto, keyed)
    return [(s, docs[i][0]) for s, i, _ in res[:maximo]]
