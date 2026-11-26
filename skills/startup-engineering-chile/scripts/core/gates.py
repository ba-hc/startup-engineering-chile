"""Umbrales por gate (assets/umbrales_gates.json) y evaluación determinista contra el expediente.

Cada gate tiene criterios de referencia en texto (`comun`, `por_track`) y `chequeos` que se pueden contar en los registros
(p. ej. "≥8 entrevistas en un mismo segmento"). `evaluar_gate` devuelve, por chequeo, el mínimo, el valor actual y si
cumple. Que todos los chequeos pasen significa "listo para decidir", no Go automático: la decisión la toma el fundador
contra el criterio fijado antes.
"""
import json
import os
import re

from .config import ASSETS
from .registros import filas
from .storage import campo, exp_dir, leer_estado

COMPROMISO = re.compile(r"preventa|dep[oó]sito|orden de compra|\bOC\b|carta de intenci[oó]n firmada|\bLOI\b firmad|pag[oó]|firm[oó]|"
                        r"contrato|anticipo", re.I)
GANADA = re.compile(r"gan|cliente|cerrad|firmad", re.I)
CONVERTIDO = re.compile(r"contrato|pagad|orden de compra|\bOC\b|convirti|firm", re.I)
PLACEHOLDER = re.compile(r"\[segmento\]|\[ \]|^$")


def umbrales_data():
    with open(os.path.join(ASSETS, "umbrales_gates.json"), encoding="utf-8") as fh:
        return json.load(fh)


def lineas_umbral(gate, track):
    g = umbrales_data()["gates"].get(gate)
    if not g:
        return []
    return list(g.get("comun", [])) + list(g.get("por_track", {}).get(track or "", []))


def _segmento_max(ents):
    cuenta = {}
    for e in ents:
        s = e.get("segmento", "").strip().lower()
        if s:
            cuenta[s] = cuenta.get(s, 0) + 1
    return max(cuenta.values()) if cuenta else 0


def _lleno(*valores):
    return all(v and v.strip() for v in valores)


# regla -> función(base) -> número
REGLAS = {
    "perfil_frase": lambda b: 0 if PLACEHOLDER.search(campo(leer_estado(b), "Una frase")) else 1,
    "perdida_aceptable": lambda b: 1 if campo(leer_estado(b), "Recursos y pérdida aceptable") else 0,
    "hipotesis": lambda b: len(filas(b, "hipotesis")),
    "competencia": lambda b: len(filas(b, "competencia")),
    "competencia_con_limitacion": lambda b: sum(1 for c in filas(b, "competencia") if _lleno(c.get("limitacion", ""))),
    "entrevistas": lambda b: len(filas(b, "entrevistas")),
    "entrevistas_mismo_segmento": lambda b: _segmento_max(filas(b, "entrevistas")),
    "entrevistas_con_hecho": lambda b: sum(1 for e in filas(b, "entrevistas") if _lleno(e.get("situacion", ""), e.get("hecho_o_cita_breve", ""))),
    "evidencias_confirmadas": lambda b: sum(1 for v in filas(b, "evidencias") if v.get("estado", "").lower() == "confirmado"),
    "evidencias_secundarias_con_fuente": lambda b: sum(1 for v in filas(b, "evidencias")
                                                       if re.search(r"secundari", v.get("tipo", ""), re.I) and _lleno(v.get("fuente_url_o_ruta", ""))),
    "experimentos_con_umbral": lambda b: sum(1 for x in filas(b, "experimentos") if _lleno(x.get("umbral", ""))),
    "experimentos_cerrados": lambda b: sum(1 for x in filas(b, "experimentos") if _lleno(x.get("resultado", ""), x.get("decision", ""))),
    "compromisos": lambda b: (sum(1 for v in filas(b, "evidencias") if COMPROMISO.search(v.get("tipo", "") + " " + v.get("afirmacion", "")))
                              + sum(1 for c in filas(b, "cuentas_y_pipeline") if COMPROMISO.search(c.get("etapa", "") + " " + c.get("senal_compra", "")))),
    "cuentas": lambda b: len(filas(b, "cuentas_y_pipeline")),
    "cuentas_ganadas": lambda b: sum(1 for c in filas(b, "cuentas_y_pipeline") if GANADA.search(c.get("etapa", ""))),
    "pilotos_definidos": lambda b: sum(1 for p in filas(b, "pilotos") if _lleno(p.get("baseline", ""), p.get("metrica", ""), p.get("meta", ""))),
    "pilotos_con_resultado": lambda b: sum(1 for p in filas(b, "pilotos") if _lleno(p.get("resultado", ""))),
    "pilotos_convertidos": lambda b: sum(1 for p in filas(b, "pilotos") if CONVERTIDO.search(p.get("decision_comercial", ""))),
    "kpis_con_valor": lambda b: sum(1 for k in filas(b, "indicadores") if _lleno(k.get("baseline", ""))),
    "riesgos": lambda b: len(filas(b, "riesgos")),
    "modelo_financiero": lambda b: 1 if os.path.exists(os.path.join(exp_dir(b), "entregables", "modelo_financiero.xlsx")) else 0,
}


def evaluar_gate(base, gate):
    """Lista de dicts {id, texto, regla, min, actual, cumple} para los chequeos del gate."""
    g = umbrales_data()["gates"].get(gate, {})
    out = []
    for ch in g.get("chequeos", []):
        f = REGLAS.get(ch["regla"])
        actual = f(base) if f else None
        out.append({"id": ch["id"], "texto": ch["texto"], "regla": ch["regla"], "min": ch["min"], "actual": actual,
                    "cumple": actual is not None and actual >= ch["min"]})
    return out


def progreso(base):
    """{gate: (cumplidos, total)} para todos los gates con chequeos."""
    res = {}
    for g in umbrales_data()["gates"]:
        ev = evaluar_gate(base, g)
        res[g] = (sum(1 for c in ev if c["cumple"]), len(ev))
    return res
