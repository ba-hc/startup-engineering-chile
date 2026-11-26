"""Rutas de la skill, versión del esquema y gates."""
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = os.path.join(SKILL_DIR, "assets")
REFS = os.path.join(SKILL_DIR, "references")
PLANTILLAS = os.path.join(ASSETS, "plantillas")
REGISTROS = os.path.join(ASSETS, "registros")
SCHEMA_VERSION = 3
NIVELES = {"sprint": ["hipotesis", "evidencias"], "completo": ["hipotesis", "evidencias", "decisiones"]}

GATES = [
    ("G0", "Oportunidad", "¿vale la pena investigar?"),
    ("G1", "Problema", "¿qué necesidad existe?"),
    ("G2", "Mercado", "¿a quién vender?"),
    ("G3", "Propuesta", "¿por qué elegirnos?"),
    ("G4", "Economía", "¿se puede cobrar rentablemente?"),
    ("G5", "Factibilidad", "¿funciona técnicamente?"),
    ("G6", "Piloto", "¿entrega valor en contexto?"),
    ("G7", "Venta/adopción", "¿compra y usa el cliente?"),
    ("G8", "Repetibilidad", "¿se repite venta e implementación?"),
    ("G9", "Escala", "¿conviene invertir más?"),
]
# Siguiente paso orientativo por gate (de references/operacion/01_plan_90_dias.md)
SIGUIENTE = {
    "G0": "Semanas 1–2: comparar 2–3 oportunidades, recursos y pérdida aceptable; investigación secundaria y competencia rápida.",
    "G1": "Semana 3: entrevistas exploratorias y observación del proceso; registrar también casos negativos.",
    "G2": "Semana 4: ICP, unidad de decisión (DMU) y compradores; mercado inicial bottom-up.",
    "G3": "Semanas 5–6: alternativas y benchmark, propuesta de valor con valor cuantificado (VPC, ROI).",
    "G4": "Semanas 7 y 11: prueba de precio y condiciones; costos, caja y escenarios.",
    "G5": "Semana 8: prototipo o PoC que ataque el riesgo técnico/usabilidad principal.",
    "G6": "Semanas 9–10: sponsor y comprador, pilot charter con criterio de éxito; medición.",
    "G7": "Semana 12: compromiso verificable, IRL/ARL/PMF y riesgos.",
    "G8": "Cohortes, capacidad y márgenes; estandarizar venta e implementación.",
    "G9": "Caja, capacidad, retención y riesgo antes de invertir en escala.",
}
