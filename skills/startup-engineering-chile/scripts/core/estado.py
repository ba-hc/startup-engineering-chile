"""00_estado.md: plantilla, acciones, hipótesis estancadas, números clave, misión de 7 días y onboarding de 3 preguntas."""
import datetime as dt
import re

from .config import GATES
from .registros import filas
from .schemas import fecha_iso, parse_monto
from .storage import leer_estado, leer_manifest, seccion

ESTADO_TPL = """# Expediente: {proyecto}

> Núcleo permanente del proyecto. La skill lo actualiza al cerrar cada bloque.
> Las vistas (pitch, dossier, informe) se generan desde aquí; la presentación no crea evidencia.
> Regla: los campos del perfil solo llevan lo que dijo el usuario. Lo propuesto por el agente se marca "(propuesta, por confirmar)".
> Privacidad: sin nombres, correos ni teléfonos de entrevistados (usa ENT-001, rol y segmento).

## Perfil
- **Proyecto:** {proyecto}
- **Modo de trabajo:** {modo}
- **Nivel:** {nivel}
- **Creado:** {hoy}
- **Etapa declarada:**
- **Una frase (sin nombrar la solución):** {frase}
- **Evidencia de calle o ventas hoy:** {evidencia}
- **Situación societaria en Chile:** {situacion}
- **Objetivo de financiamiento:** {objetivo}
- **Madurez (TRL / CRL):**
- **Equipo y dedicación:**
- **Recursos y pérdida aceptable:**
- **Objetivo próximo y fecha límite:**
- **Materiales / sitio web:**

## Números clave
> Solo cifras que el usuario dio o que salen de un script; en CLP. `auditar.py` las compara con el modelo financiero.
- **Precio mensual:**
- **CAC:**
- **Churn mensual:**
- **Caja actual (CLP):**
- **Gasto mensual neto (CLP):**
- **Ventas últimos 12 meses (CLP):**

## Ruta
| Gate | Estado | Evidencia (0–4) | Qué lo movería |
|---|---|---|---|
{ruta}
| CORFO u otro fondo | no aplica | — | |

Estados: pendiente · en curso · Go · Hold · Recycle · Kill · no aplica. Evidencia: 0 sin evidencia · 1 hipótesis · 2 secundaria · 3 primaria parcial · 4 pertinente y comprobable.

## Foco actual
- **Gate actual:** {gate}
- **Hipótesis más riesgosa:**
- **Único cuello de botella:**

## Misión de 7 días
- **Misión:** {mision}
- **Vence:** {vence}
- **Cómo sabremos que se cumplió:** {criterio}
- **Estado:** {estado_mision}

## Trabajo de campo pendiente
- **Tarea:**
- **Plazo:**
- **Criterio fijado antes (EXP-…):**
- **Qué traer de vuelta:**

## Próximas acciones
| # | Acción | Responsable | Vence | Criterio de éxito | Estado |
|---|---|---|---|---|---|

## Bitácora de sesiones
| Fecha | Qué se hizo | Evidencia nueva | Decisión | Para la próxima |
|---|---|---|---|---|
| {hoy} | {primera} | — | — | — |
"""

# palabra clave en la evidencia declarada -> gate sugerido (el primero que calza, de más a menos avanzado)
GATE_POR_EVIDENCIA = [
    (r"factur|vend(o|emos|imos)|ventas|clientes? pagando|MRR|ingresos", "G7"),
    (r"piloto", "G6"),
    (r"preventa|dep[oó]sito|carta de intenci[oó]n|\bLOI\b|orden de compra|\bOC\b", "G4"),
    (r"encuesta|entrevist|convers[eé]|convers", "G1"),
]


def texto_estado(proyecto, modo="empezar", nivel="completo", frase="", evidencia="", situacion="", objetivo="", gate="G0",
                 mision="", vence="", criterio="", hoy=None, primera="Expediente creado"):
    hoy = hoy or dt.date.today().isoformat()
    ruta = "\n".join(f"| {g} {n}: {q} | {'en curso' if g == gate else 'pendiente'} | 0 | |" for g, n, q in GATES)
    return ESTADO_TPL.format(
        proyecto=proyecto, modo=modo, nivel=nivel, hoy=hoy, ruta=ruta, gate=gate,
        frase=frase or "[segmento] necesita [trabajo] y hoy enfrenta [problema] usando [alternativa].",
        evidencia=evidencia, situacion=situacion, objetivo=objetivo, mision=mision, vence=vence, criterio=criterio,
        estado_mision="abierta" if mision else "", primera=primera)


NEGACION = re.compile(r"\b(sin|no|nada de|cero|0|ning[uú]n[ao]?|a[uú]n no|todav[ií]a no)\s+(\w+\s+){0,3}?"
                      r"(ventas|vend\w*|clientes|factur\w*|ingresos|pilotos?|preventas?|entrevistas?|conversaciones|encuestas?)\b", re.I)


def inferir_gate(evidencia):
    """Gate sugerido según la evidencia declarada en el onboarding ("sin ventas" no cuenta como ventas)."""
    texto = NEGACION.sub(" ", evidencia or "")
    for pat, g in GATE_POR_EVIDENCIA:
        if re.search(pat, texto, re.I):
            return g
    return "G0"


def acciones(txt, hoy):
    pend, vencidas = [], []
    for l in seccion(txt, "Próximas acciones").splitlines():
        if not l.startswith("|") or re.match(r"^\|\s*(#|-)", l):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) < 4 or not cells[1]:
            continue
        estado = cells[5].lower() if len(cells) > 5 else ""
        if estado in ("hecho", "hecha", "cerrada", "cerrado", "ok", "✓"):
            continue
        m = re.search(r"\d{4}-\d{2}-\d{2}", cells[3])
        venc = dt.date.fromisoformat(m.group(0)) if m else None
        (vencidas if venc and venc < hoy else pend).append((cells[1], cells[2], cells[3]))
    return pend, vencidas


def mision(txt, hoy=None):
    """Devuelve {'mision','vence','criterio','estado','vencida'} o None si no hay misión."""
    s = seccion(txt, "Misión de 7 días")
    if not s:
        return None

    def c(et):
        m = re.search(r"\*\*" + re.escape(et) + r":\*\*[ \t]*(.*)", s)
        return m.group(1).strip() if m else ""
    d = {"mision": c("Misión"), "vence": c("Vence"), "criterio": c("Cómo sabremos que se cumplió"), "estado": c("Estado")}
    if not d["mision"]:
        return None
    hoy = hoy or dt.date.today()
    m = re.search(r"\d{4}-\d{2}-\d{2}", d["vence"])
    d["vencida"] = bool(m and dt.date.fromisoformat(m.group(0)) < hoy and d["estado"].lower() not in ("cumplida", "hecha", "cerrada"))
    return d


def numeros_clave(txt):
    """{etiqueta: valor numérico en CLP o fracción} desde la sección 'Números clave' (ignora vacíos y montos no CLP)."""
    out = {}
    for l in seccion(txt, "Números clave").splitlines():
        m = re.match(r"-\s*\*\*(.+?):\*\*\s*(.*)", l.strip())
        if not m or not m.group(2).strip():
            continue
        et, v = m.group(1).strip(), m.group(2).strip()
        if "%" in v:
            num, _ = parse_monto(v.replace("%", ""))
            if num is not None:
                out[et] = num / 100
            continue
        num, moneda = parse_monto(v)
        if num is not None and moneda == "CLP":
            out[et] = num
    return out


def hipotesis_estancadas(base, hoy, dias=14):
    """Hipótesis no descartadas sin experimento asociado y con más de `dias` desde su evidencia o creación."""
    hips = filas(base, "hipotesis")
    if not hips:
        return []
    con_exp = {d.get("hypothesis_id", "") for d in filas(base, "experimentos")}
    ev_fecha = {}
    for d in filas(base, "evidencias"):
        if fecha_iso(d.get("fecha", "")):
            f = dt.date.fromisoformat(d["fecha"][:10])
            hid = d.get("hypothesis_id", "")
            ev_fecha[hid] = max(ev_fecha.get(hid, f), f)
    creado = (leer_manifest(base) or {}).get("creado")
    base_fecha = dt.date.fromisoformat(creado) if creado and fecha_iso(creado) else hoy
    out = []
    for d in hips:
        hid = d.get("hypothesis_id", "")
        if d.get("estado", "").lower() in ("descartado", "obsoleto") or hid in con_exp or d.get("experiment_id"):
            continue
        ref = ev_fecha.get(hid, base_fecha)
        if (hoy - ref).days > dias:
            out.append((hid, d.get("enunciado_refutable", "")[:90], (hoy - ref).days))
    return out


def gate_actual_de(base):
    mm = re.search(r"Gate actual:\*\*\s*(G\d)", seccion(leer_estado(base), "Foco actual"))
    return mm.group(1) if mm else None
