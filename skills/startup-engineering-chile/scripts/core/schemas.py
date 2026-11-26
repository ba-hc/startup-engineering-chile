"""Esquemas de los registros, tipos de columna (fechas, números, montos en CLP/UF/USD, enumeraciones) y validación.

Esquema v3:
  - 8 tablas núcleo: hipotesis, experimentos, evidencias, decisiones, entrevistas, competencia, cuentas_y_pipeline, pilotos
  - rendiciones: solo si el proyecto postula a un fondo
  - bitacora: todo lo secundario (riesgos, KPI, fuentes, lecciones, desafíos, PI, requisitos de fondos, cohortes, notas),
    con una columna `tipo` y una columna `datos` (JSON) para los campos propios de cada tipo.
Los nombres antiguos (riesgos, indicadores, …) siguen funcionando en `add`, `ver` y `filas()`: se leen y escriben en la bitácora.
"""
import datetime as dt
import json
import os
import re

from .config import REGISTROS
from .storage import exp_dir, leer, leer_seguro

NUCLEO = ["hipotesis", "experimentos", "evidencias", "decisiones", "entrevistas", "competencia", "cuentas_y_pipeline", "pilotos"]
FONDOS = ["rendiciones"]
BITACORA = "bitacora"

PREFIJOS = {"evidencias": "EV", "hipotesis": "H", "experimentos": "EXP", "decisiones": "DEC", "competencia": "COMP",
            "entrevistas": "ENT", "pilotos": "PIL", "cuentas_y_pipeline": "CTA", "rendiciones": "GAS"}
PREFIJOS_BITACORA = {"riesgo": "R", "kpi": "KPI", "fuente": "SRC", "leccion": "LEC", "desafio": "DES", "ip": "IP",
                     "requisito": "REQ", "cohorte": "COH", "nota": "BIT"}

# registro antiguo -> (tipo en bitácora, columnas antiguas, {columna antigua: columna de bitácora})
LEGADO = {
    "riesgos": ("riesgo", "risk_id,dominio,riesgo,probabilidad,impacto,senal,mitigacion,contingencia,responsable,revision,estado",
                {"risk_id": "entrada_id", "riesgo": "titulo", "mitigacion": "detalle", "responsable": "responsable",
                 "revision": "revision", "estado": "estado"}),
    "indicadores": ("kpi", "kpi_id,nombre,tipo,formula,unidad,denominador,baseline,meta,frecuencia,fuente,guardrail,responsable",
                    {"kpi_id": "entrada_id", "nombre": "titulo", "formula": "detalle", "baseline": "valor", "meta": "meta",
                     "responsable": "responsable"}),
    "fuentes_nuevas": ("fuente", "source_id,titulo,autor,url,fecha_publicacion,fecha_consulta,version,tipo,hallazgo,limite,licencia,estado",
                       {"source_id": "entrada_id", "titulo": "titulo", "hallazgo": "detalle", "url": "url",
                        "fecha_consulta": "fecha", "estado": "estado"}),
    "lecciones_mentores": ("leccion", "lesson_id,referente,fuente,url,fecha,timestamp_capitulo,contexto,tipo_evidencia,"
                           "ensenanza_parafraseada,limitacion,aplicacion,experimento,entregable",
                           {"lesson_id": "entrada_id", "referente": "titulo", "ensenanza_parafraseada": "detalle", "url": "url",
                            "fecha": "fecha"}),
    "desafios_corporativos": ("desafio", "challenge_id,organizacion,sector,problema,fecha,url,requisitos,TRL,presupuesto_publicado,"
                              "condicion_piloto,decision_compra,estado",
                              {"challenge_id": "entrada_id", "problema": "titulo", "requisitos": "detalle", "fecha": "fecha",
                               "url": "url", "estado": "estado"}),
    "ip_licencias": ("ip", "asset_id,activo,titular,origen,licencia,restriccion,derechos,evidence_id,proteccion,riesgo,accion,responsable",
                     {"asset_id": "entrada_id", "activo": "titulo", "accion": "detalle", "evidence_id": "evidence_id",
                      "responsable": "responsable"}),
    "corfo_elegibilidad": ("requisito", "convocatoria,version,requisito,articulo_pagina,url,evidence_id,estado,responsable,vencimiento,observacion",
                           {"requisito": "titulo", "observacion": "detalle", "url": "url", "evidence_id": "evidence_id",
                            "estado": "estado", "responsable": "responsable", "vencimiento": "revision"}),
    "cohortes": ("cohorte", "cohorte,segmento,mes_relativo,clientes_iniciales,clientes_retenidos,MRR_inicial_CLP,MRR_retenido_CLP,"
                 "expansion_CLP,contraccion_CLP,churn_CLP,fuente",
                 {"cohorte": "titulo", "segmento": "detalle", "fuente": "url"}),
}
LEGADO = {k: (t, cols.split(","), m) for k, (t, cols, m) in LEGADO.items()}
TIPO_A_LEGADO = {t: k for k, (t, _, _) in LEGADO.items()}

# referencias entre registros: columna -> registro destino
REFERENCIAS = {"hypothesis_id": "hipotesis", "experiment_id": "experimentos", "evidence_id": "evidencias",
               "evidence_ids": "evidencias", "cuenta_id": "cuentas_y_pipeline"}
# campos que `add` exige (se puede saltar con --forzar)
OBLIGATORIOS = {"experimentos": ["hypothesis_id", "metrica", "umbral"],
                "evidencias": ["afirmacion", "fuente_url_o_ruta"],
                "decisiones": ["gate", "decision", "justificacion"],
                "entrevistas": ["segmento", "hecho_o_cita_breve"],
                "bitacora": ["tipo", "titulo"]}
COLS_FECHA = {"fecha", "fecha_consulta", "fecha_publicacion", "fecha_estimada", "inicio", "fin", "vencimiento", "revision"}
COLS_NUMERO = {"n", "probabilidad_interna"}
COLS_MONTO_LIBRE = {"presupuesto_declarado", "presupuesto_publicado", "valor", "meta"}  # aceptan CLP, UF o USD
DECISIONES_VALIDAS = {"go", "hold", "recycle", "kill", "no aplica"}
ESTADOS_DATO = {"propuesta-agente", "confirmado", "descartado", "en revisión", "en revision", "vigente", "obsoleto"}
ENUMS = {("rendiciones", "tipo_aporte"): {"pecuniario", "valorado"},
         ("rendiciones", "iva_incluido"): {"si", "sí", "no"},
         ("bitacora", "tipo"): set(PREFIJOS_BITACORA)}

MONEDAS = {"CLP": ("clp", "$", "pesos", "peso"), "UF": ("uf",), "USD": ("usd", "us$", "u$s", "dólares", "dolares", "dólar", "dolar")}


def esquema(reg):
    """Columnas de un registro (núcleo, rendiciones, bitácora o antiguo). None si no existe."""
    reg = reg.replace(".csv", "")
    if reg in LEGADO:
        return list(LEGADO[reg][1])
    src = os.path.join(REGISTROS, reg + ".csv")
    return leer(src)[0] if os.path.exists(src) else None


def registros_disponibles():
    """Registros vigentes (v3): los 8 núcleo, rendiciones y bitácora."""
    return sorted(f[:-4] for f in os.listdir(REGISTROS) if f.endswith(".csv"))


def fecha_iso(v):
    try:
        dt.date.fromisoformat(v.strip()[:10])
        return len(v.strip()) >= 10
    except ValueError:
        return False


def _num(texto):
    """'1.200.000' -> 1200000.0; '0,25' -> 0.25; '3,5' -> 3.5; '1200000.5' -> 1200000.5."""
    s = texto.strip().replace(" ", "")
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", s):
        s = s.replace(",", "")
    elif re.fullmatch(r"-?\d+,\d+", s):
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def es_numero(v):
    v = v.strip().replace("$", "").replace(" ", "")
    if not v:
        return True
    v = v.rstrip("%")
    return bool(re.fullmatch(r"-?(\d{1,3}(\.\d{3})+|\d+)([.,]\d+)?", v))


def parse_monto(v):
    """Interpreta un monto con su moneda: '$1.200.000', '1200000 CLP', '3,5 UF', 'UF 3,5', 'USD 120', 'US$120'.

    Devuelve (valor, moneda) con moneda en {CLP, UF, USD}; sin moneda explícita se asume CLP. (None, None) si no se entiende.
    """
    s = (v or "").strip()
    if not s:
        return None, None
    bajo = s.lower()
    moneda = None
    for m, claves in MONEDAS.items():
        for k in claves:
            if k == "$":
                continue
            if re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])", bajo):
                moneda = m
                break
        if moneda:
            break
    if moneda is None:
        moneda = "CLP"
    m = re.search(r"-?\d[\d.,]*", s.replace(" ", ""))
    if not m:
        return None, None
    num = _num(m.group(0).rstrip(".,"))
    if num is None:
        return None, None
    if re.search(r"\b(mil|k)\b", bajo) and moneda == "CLP" and num < 100000:
        num *= 1000
    if re.search(r"\b(millones|mm|m)\b", bajo) and moneda == "CLP" and num < 100000:
        num *= 1_000_000
    return num, moneda


def validar_valor(reg, col, v):
    """Devuelve (error, aviso) para una celda; cada uno es None o un texto."""
    v = (v or "").strip()
    if not v:
        return None, None
    if col in COLS_FECHA and not fecha_iso(v):
        return f"{col}='{v}' no es AAAA-MM-DD", None
    if col.endswith("_CLP"):
        if re.search(r"\b(uf|usd|us\$|d[oó]lar)", v.lower()):
            return (f"{col}='{v}' no está en pesos: conviértelo con `indicadores_cl.py convertir {v.split()[0] if v.split() else v} "
                    "UF CLP` (cita valor y fecha) o anótalo en una columna sin _CLP"), None
        if not es_numero(v):
            return f"{col}='{v}' no es un número", None
    if (col in COLS_NUMERO or col.startswith("clientes_")) and not es_numero(v):
        return f"{col}='{v}' no es un número", None
    if col in COLS_MONTO_LIBRE and re.search(r"\d", v) and parse_monto(v)[0] is None:
        return None, f"{col}='{v}' no se entiende como monto (usa p. ej. '$150.000', '3,5 UF' o 'USD 200')"
    permitidos = ENUMS.get((reg, col))
    if permitidos and v.lower() not in permitidos:
        return f"{col}='{v}' no es válido (usa {', '.join(sorted(permitidos))})", None
    return None, None


PII = {"un correo": r"[\w.+-]+@[\w-]+\.[\w.]+",
       "un teléfono": r"(?<![\d-])(\+?56[\s.-]?)?9[\s.-]?\d{4}[\s.-]?\d{4}(?![\d-])",
       "un RUT": r"(?<![\d-])\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b"}


def buscar_pii(textos):
    """Revisa cada campo por separado (unir campos produce falsos positivos)."""
    if isinstance(textos, str):
        textos = [textos]
    return [k for k, p in PII.items() if any(re.search(p, t or "") for t in textos)]


def datos_json(texto):
    """Parsea la columna `datos` de la bitácora. Devuelve (dict, error)."""
    texto = (texto or "").strip()
    if not texto:
        return {}, None
    try:
        d = json.loads(texto)
    except ValueError as e:
        return {}, f"datos no es JSON válido ({e.msg})"
    if not isinstance(d, dict):
        return {}, "datos debe ser un objeto JSON {…}"
    return {str(k): ("" if v is None else str(v)) for k, v in d.items()}, None


def validar(base):
    """Devuelve (errores, avisos) sobre los registros del expediente."""
    errores, avisos = [], []
    rdir = os.path.join(exp_dir(base), "registros")
    if not os.path.isdir(rdir):
        return errores, avisos
    ids = {}
    datos = {}
    for f in sorted(os.listdir(rdir)):
        if not f.endswith(".csv"):
            continue
        reg = f[:-4]
        path = os.path.join(rdir, f)
        if os.path.getsize(path) == 0:
            errores.append(f"{reg}: archivo vacío (sin encabezado) → expediente.py migrar lo repara")
            continue
        h, rows, err = leer_seguro(path)
        if err:
            errores.append(f"{reg}: ilegible ({err}); revisa la codificación (debe ser UTF-8)")
            continue
        esq = esquema(reg)
        if esq is None:
            avisos.append(f"{reg}: no es un registro del pack (se ignora)")
            continue
        if reg in LEGADO:
            avisos.append(f"{reg}: registro antiguo (v2); `expediente.py migrar` lo pasa a bitacora.csv")
        faltan = [c for c in esq if c not in h]
        sobran = [c for c in h if c not in esq]
        if faltan:
            errores.append(f"{reg}: faltan columnas {', '.join(faltan)} → expediente.py migrar")
        if sobran:
            avisos.append(f"{reg}: columnas extra {', '.join(sobran)} (se conservan)")
        vistos = set()
        for n, r in enumerate(rows, start=2):
            if len(r) != len(h):
                errores.append(f"{reg} línea {n}: {len(r)} celdas, se esperaban {len(h)} (¿coma sin comillas?)")
            d = dict(zip(h, r + [""] * (len(h) - len(r))))
            rid = r[0].strip() if r else ""
            if not rid:
                errores.append(f"{reg} línea {n}: sin ID")
            elif rid in vistos:
                errores.append(f"{reg} línea {n}: ID duplicado {rid}")
            vistos.add(rid)
            for c, v in d.items():
                e_, a_ = validar_valor(reg, c, v)
                if e_:
                    errores.append(f"{reg} {rid}: {e_}")
                if a_:
                    avisos.append(f"{reg} {rid}: {a_}")
            if reg == BITACORA:
                _, e_ = datos_json(d.get("datos", ""))
                if e_:
                    errores.append(f"bitacora {rid}: {e_}")
                pref = PREFIJOS_BITACORA.get(d.get("tipo", "").lower())
                if pref and rid and not rid.startswith(pref + "-"):
                    avisos.append(f"bitacora {rid}: el ID no usa el prefijo {pref}- del tipo {d.get('tipo')}")
            if reg in ("evidencias", "hipotesis") and d.get("estado") and d["estado"].lower() not in ESTADOS_DATO:
                avisos.append(f"{reg} {rid}: estado '{d['estado']}' no es estándar (propuesta-agente, confirmado, descartado…)")
            if reg == "decisiones" and d.get("decision") and d["decision"].lower() not in DECISIONES_VALIDAS:
                errores.append(f"decisiones {rid}: decision '{d['decision']}' no es Go/Hold/Recycle/Kill/no aplica")
            for c in OBLIGATORIOS.get(reg, []):
                if c in d and not d[c].strip():
                    avisos.append(f"{reg} {rid}: falta {c}")
            pii = buscar_pii(list(d.values()))
            if pii:
                avisos.append(f"{reg} {rid}: posible dato personal ({', '.join(pii)})")
        ids[reg] = vistos
        datos[reg] = (h, rows)
    for reg, (h, rows) in datos.items():
        for r in rows:
            d = dict(zip(h, r))
            for c, destino in REFERENCIAS.items():
                if c not in d or c == h[0] or not d[c].strip():
                    continue
                for ref in re.split(r"[;,\s]+", d[c]):
                    if re.fullmatch(r"[A-Z]+-\d+", ref) and ref not in ids.get(destino, set()):
                        errores.append(f"{reg} {r[0]}: {c}={ref} no existe en {destino}")
    return errores, avisos
