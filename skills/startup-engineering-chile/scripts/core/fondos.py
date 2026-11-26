"""Reglas de fondos públicos (assets/fondos/instrumentos.json): elegibilidad y revisión de presupuesto.

Lo usan fondos_lint.py, fondos_matcher.py y presupuesto_corfo.py. Es una revisión previa con reglas versionadas,
no una certificación de admisibilidad: manda la base del llamado vigente.
"""
import datetime as dt
import json
import os
import re
import sys

from .config import ASSETS

REGLAS = os.path.join(ASSETS, "fondos", "instrumentos.json")
NO_FINANCIABLES = ["inmueble", "compra de terreno", "vehículo", "vehiculo", "camioneta", "automóvil", "deuda", "multa", "interés",
                   "intereses", "iva recuperable", "dividendo", "acciones", "garantía", "garantia", "gasto previo", "retiro de socio"]
SOCIO = re.compile(r"\bsoci[oa]s?\b|fundador|cofundador|due[ñn]o|accionista|relacionad|\b(CEO|CTO|COO)\b|gerente general", re.I)
RRHH = re.compile(r"recursos humanos|rr\.?\s?hh|honorario|remuneraci|sueldo|personal", re.I)
ADMIN = re.compile(r"administraci|gastos generales|overhead|contabilidad", re.I)


def reglas():
    with open(REGLAS, encoding="utf-8") as fh:
        r = json.load(fh)
    ver = r.get("_verificado", "?")
    edad = (dt.date.today() - dt.date.fromisoformat(ver)).days if ver != "?" else 999
    aviso = f" — hace {edad} días: revisa la convocatoria vigente" if edad > 90 else ""
    return r, f"Reglas verificadas el {ver}{aviso}. Revisión previa, no certificación: manda la base del llamado."


def instrumento(r, clave):
    inst = r["instrumentos"].get(clave)
    if not inst:
        sys.exit(f"Instrumento desconocido '{clave}'. Disponibles: {', '.join(r['instrumentos'])}")
    return inst


def num(v):
    v = (v or "").strip().replace("$", "").replace(" ", "")
    if not v:
        return 0.0
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", v):
        v = v.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d+,\d+", v):
        v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return float("nan")


def clp(x):
    return "$" + f"{x:,.0f}".replace(",", ".")


def fecha(v):
    try:
        return dt.date.fromisoformat((v or "").strip()[:10])
    except ValueError:
        return None


def condiciones(inst, mujeres=False):
    """(tope, cofinanciamiento) aplicando la variante para empresas lideradas por mujeres si existe."""
    tope, cof = inst.get("tope_subsidio_CLP"), inst.get("cofinanciamiento_max")
    var = inst.get("variante_mujeres") or {}
    if mujeres and var:
        tope, cof = var.get("tope_subsidio_CLP", tope), var.get("cofinanciamiento_max", cof)
    return tope, cof


def evaluar_elegibilidad(inst, tipo=None, meses_inicio=None, ventas_12m=None, ventas_solucion=None, trl=None, uf=None):
    """[(estado, texto)] con estado CUMPLE / NO CUMPLE / FALTA DATO / VERIFICAR. Solo filtros duros versionados."""
    res = []
    tipos = inst.get("beneficiarios", [])
    if tipos:
        if tipo is None:
            res.append(("FALTA DATO", f"tipo de postulante (admite: {', '.join(tipos)})"))
        else:
            res.append(("CUMPLE" if tipo in tipos else "NO CUMPLE", f"tipo de postulante '{tipo}' (admite: {', '.join(tipos)})"))
    reglas_tipo = inst.get("por_tipo", {}).get(tipo or "", {})
    mmax, mmin = reglas_tipo.get("meses_inicio_max"), reglas_tipo.get("meses_inicio_min")
    if mmax is not None or mmin is not None:
        if meses_inicio is None:
            res.append(("FALTA DATO", "meses desde el inicio de actividades en el SII"))
        else:
            ok = (mmax is None or meses_inicio < mmax) and (mmin is None or meses_inicio >= mmin)
            rango = (f"< {mmax}" if mmax is not None else "") + (f" y ≥ {mmin}" if mmin is not None else "")
            res.append(("CUMPLE" if ok else "NO CUMPLE", f"antigüedad {meses_inicio:g} meses (regla: {rango.strip(' y')})"))
    vmax, vmin = reglas_tipo.get("ventas_12m_max_CLP"), reglas_tipo.get("ventas_12m_min_CLP")
    vmax_uf = reglas_tipo.get("ventas_12m_max_UF")
    if vmax_uf is not None and uf:
        vmax = min(vmax, vmax_uf * uf) if vmax is not None else vmax_uf * uf
    elif vmax_uf is not None:
        res.append(("VERIFICAR", f"ventas anuales de hasta {vmax_uf:,.0f} UF (pasa --uf para convertir)".replace(",", ".")))
    if vmax is not None or vmin is not None:
        if ventas_12m is None:
            res.append(("FALTA DATO", "ventas netas de los últimos 12 meses"))
        else:
            ok = (vmax is None or ventas_12m <= vmax) and (vmin is None or ventas_12m >= vmin)
            res.append(("CUMPLE" if ok else "NO CUMPLE",
                        f"ventas 12 meses {clp(ventas_12m)} (regla: {('≥ ' + clp(vmin)) if vmin is not None else ''}"
                        f"{' y ' if vmin is not None and vmax is not None else ''}{('≤ ' + clp(vmax)) if vmax is not None else ''})"))
    smin = reglas_tipo.get("ventas_solucion_min_CLP")
    if smin is not None:
        if ventas_solucion is None:
            res.append(("FALTA DATO", "ventas de la solución postulada"))
        else:
            res.append(("CUMPLE" if ventas_solucion >= smin else "NO CUMPLE",
                        f"ventas de la solución {clp(ventas_solucion)} (mínimo {clp(smin)})"))
    if reglas_tipo.get("sin_ventas"):
        if ventas_12m is None:
            res.append(("FALTA DATO", "¿tiene ventas? (la regla exige cero ventas para este tipo de postulante)"))
        elif ventas_12m:
            res.append(("NO CUMPLE", "la regla exige no tener ventas para este tipo de postulante"))
        else:
            res.append(("CUMPLE", "sin ventas"))
    tmin, tmax = inst.get("trl_min"), inst.get("trl_max")
    if tmin is not None or tmax is not None:
        if trl is None:
            res.append(("FALTA DATO", f"TRL de entrada (regla: {tmin}–{tmax})"))
        else:
            ok = (tmin is None or trl >= tmin) and (tmax is None or trl <= tmax)
            res.append(("CUMPLE" if ok else "NO CUMPLE", f"TRL {trl} (regla: {tmin}–{tmax})"))
    for v in inst.get("verificar", []):
        res.append(("VERIFICAR", v))
    return res


def meses_entre(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month) + (1 if b.day >= a.day else 0)


def revisar_presupuesto(filas, inst, inicio=None, fin=None, recupera_iva=False, tope_rrhh=None, tope_admin=None, mujeres=False):
    """Revisa el presupuesto (filas de rendiciones.csv) contra el instrumento.

    Devuelve (resultados, totales, por_cuenta). resultados = [(estado, texto)] con OK / PROBLEMA / AVISO / VERIFICAR.
    """
    res = []
    tot = {"presupuesto": 0.0, "subsidio": 0.0, "aporte": 0.0, "pecuniario": 0.0, "valorado": 0.0, "rrhh": 0.0, "admin": 0.0}
    por_cuenta = {}
    socios = []  # (gasto_id, presupuesto, quién) de filas de RR.HH. que parecen pagar a un socio
    for f in filas:
        gid = f.get("gasto_id", "?")
        p, s, ap = num(f.get("presupuesto_CLP")), num(f.get("subsidio_CLP")), num(f.get("aporte_CLP"))
        if any(x != x for x in (p, s, ap)):
            res.append(("PROBLEMA", f"{gid}: monto no numérico"))
            continue
        if abs(p - (s + ap)) > 1:
            res.append(("PROBLEMA", f"{gid}: presupuesto {clp(p)} ≠ subsidio {clp(s)} + aporte {clp(ap)}"))
        if min(p, s, ap) < 0:
            res.append(("PROBLEMA", f"{gid}: monto negativo"))
        texto = " ".join(f.get(k, "") for k in ("actividad", "cuenta_presupuestaria", "proveedor", "documento")).lower()
        hit = [k for k in NO_FINANCIABLES if k in texto]
        if hit:
            res.append(("AVISO", f"{gid}: '{hit[0]}' suele ser no financiable; confirma en las bases"))
        if not f.get("actividad", "").strip() or not f.get("resultado", "").strip():
            res.append(("AVISO", f"{gid}: falta actividad o resultado (cada gasto debe servir a un resultado)"))
        tipo_ap = (f.get("tipo_aporte") or "").strip().lower()
        if ap > 0:
            if tipo_ap not in ("pecuniario", "valorado"):
                res.append(("AVISO", f"{gid}: aporte {clp(ap)} sin tipo_aporte (pecuniario o valorado)"))
            tot["valorado" if tipo_ap == "valorado" else "pecuniario"] += ap
            if tipo_ap == "valorado" and "valorado" not in (inst.get("aporte_tipos") or ["pecuniario", "valorado"]):
                res.append(("PROBLEMA", f"{gid}: este instrumento no acepta aporte valorado"))
        iva = (f.get("iva_incluido") or "").strip().lower() in ("si", "sí")
        if iva and recupera_iva:
            res.append(("PROBLEMA", f"{gid}: monto con IVA incluido y la empresa recupera IVA como crédito fiscal. El IVA recuperable "
                        f"no es financiable: presupuesta el monto neto ({clp(p / 1.19)} si el 19% está incluido)."))
        elif iva:
            res.append(("VERIFICAR", f"{gid}: monto con IVA; solo es financiable si la empresa no lo recupera (confírmalo con el contador)"))
        d = fecha(f.get("fecha"))
        if inicio and d and d < inicio:
            res.append(("PROBLEMA", f"{gid}: fecha {d} anterior al inicio del proyecto ({inicio}). Un gasto previo al inicio "
                        "(aunque esté pagado o comprometido) no se puede imputar al proyecto."))
        if fin and d and d > fin:
            res.append(("PROBLEMA", f"{gid}: fecha {d} posterior al término del proyecto ({fin})"))
        if inicio and d and d < inicio and (num(f.get("pagado_CLP")) or num(f.get("comprometido_CLP"))):
            res.append(("AVISO", f"{gid}: ya está pagado o comprometido antes de postular: sácalo del presupuesto o muévelo a aporte "
                        "fuera del proyecto"))
        if RRHH.search(f.get("cuenta_presupuestaria", "") + " " + f.get("actividad", "")):
            tot["rrhh"] += p
            if SOCIO.search(f.get("actividad", "") + " " + f.get("proveedor", "")):
                socios.append((gid, p, (f.get("proveedor") or f.get("actividad") or gid).strip().lower()))
                if s > 0 and not inst.get("remuneracion_socio_max_mensual_CLP"):
                    res.append(("AVISO", f"{gid}: honorarios o sueldo a un socio/fundador pagado con subsidio ({clp(s)}). Muchas bases lo "
                                "restringen, le ponen tope o lo aceptan solo como aporte; verifica la regla del llamado antes de postular."))
        if ADMIN.search(f.get("cuenta_presupuestaria", "") + " " + f.get("actividad", "")):
            tot["admin"] += p
        tot["presupuesto"] += p
        tot["subsidio"] += s
        tot["aporte"] += ap
        c = f.get("cuenta_presupuestaria", "") or "(sin cuenta)"
        por_cuenta.setdefault(c, {"total": 0.0, "subsidio": 0.0, "pecuniario": 0.0, "valorado": 0.0})
        por_cuenta[c]["total"] += p
        por_cuenta[c]["subsidio"] += s
        por_cuenta[c]["valorado" if tipo_ap == "valorado" else "pecuniario"] += ap
    tope, cof = condiciones(inst, mujeres)
    if tope:
        res.append(("OK" if tot["subsidio"] <= tope else "PROBLEMA", f"subsidio total {clp(tot['subsidio'])} vs tope {clp(tope)}"))
    if cof and tot["presupuesto"]:
        share = tot["subsidio"] / tot["presupuesto"]
        res.append(("OK" if share <= cof + 1e-9 else "PROBLEMA",
                    f"subsidio = {share * 100:.1f}% del costo total (máximo {cof * 100:.0f}%); aporte mínimo "
                    f"{clp(tot['presupuesto'] * (1 - cof))}, tienes {clp(tot['aporte'])}"))
    pmin = inst.get("aporte_pecuniario_min")
    if pmin and tot["presupuesto"]:
        req = tot["presupuesto"] * pmin
        res.append(("OK" if tot["pecuniario"] + 1 >= req else "PROBLEMA",
                    f"aporte pecuniario {clp(tot['pecuniario'])} vs mínimo {pmin * 100:.0f}% del costo ({clp(req)})"))
    for c, lim in (inst.get("topes_por_cuenta_pct") or {}).items():
        v = sum(x["total"] for k, x in por_cuenta.items() if c.lower() in k.lower())
        if tot["presupuesto"] and v / tot["presupuesto"] > lim:
            res.append(("PROBLEMA", f"cuenta '{c}' = {v / tot['presupuesto'] * 100:.0f}% (tope de referencia {lim * 100:.0f}%)"))
    if tot["presupuesto"]:
        prr, pad = tot["rrhh"] / tot["presupuesto"], tot["admin"] / tot["presupuesto"]
        if tope_rrhh is not None:
            res.append(("OK" if prr <= tope_rrhh + 1e-9 else "PROBLEMA", f"RR.HH. = {prr * 100:.0f}% (tope indicado {tope_rrhh * 100:.0f}%)"))
        elif prr > 0.5:
            res.append(("AVISO", f"RR.HH. concentra el {prr * 100:.0f}% del presupuesto: revisa el tope de la convocatoria "
                        "(pásalo con --tope-rrhh) y si el equipo fundador puede cobrar con cargo al subsidio"))
        if tope_admin is not None and pad > tope_admin + 1e-9:
            res.append(("PROBLEMA", f"administración = {pad * 100:.0f}% (tope indicado {tope_admin * 100:.0f}%)"))
    tope_socio = inst.get("remuneracion_socio_max_mensual_CLP")
    if tope_socio and socios:
        # Agrupa por persona: una misma persona puede aparecer en varias filas (por mes o por actividad).
        por_persona = {}
        for gid, p, q in socios:
            ids, monto = por_persona.get(q, ([], 0.0))
            por_persona[q] = (ids + [gid], monto + p)
        max_socios = inst.get("socios_remunerados_max")
        if max_socios and len(por_persona) > max_socios:
            res.append(("AVISO", f"parece haber remuneraciones a {len(por_persona)} socios ({', '.join(sorted(por_persona))}); "
                        f"las bases admiten hasta {max_socios}. Si son la misma persona, usa el mismo nombre en proveedor"))
        meses, base = inst.get("plazo_meses"), "meses de plazo máximo"
        if inicio and fin and (not meses or meses_entre(inicio, fin) <= meses):
            meses, base = meses_entre(inicio, fin), "meses de ejecución"
        for q, (ids, monto) in sorted(por_persona.items()):
            filas_q = ", ".join(ids)
            if meses:
                lim = tope_socio * meses
                res.append(("OK" if monto <= lim + 1 else "PROBLEMA",
                            f"remuneración de socio ({q}; {filas_q}) {clp(monto)} vs tope {clp(tope_socio)}/mes × {meses} {base} = {clp(lim)}"))
            else:
                res.append(("AVISO", f"remuneración de socio ({q}; {filas_q}): las bases la topan en {clp(tope_socio)} mensuales"))
    plazo = inst.get("plazo_meses")
    if plazo and inicio and fin:
        m = meses_entre(inicio, fin)
        if m > plazo:
            pr = inst.get("prorroga_meses")
            res.append(("PROBLEMA", f"duración {m} meses ({inicio} a {fin}) supera el plazo de ejecución de {plazo} meses"
                        + (f" (la prórroga de hasta {pr} meses es excepcional, no se planifica)" if pr else "")))
        else:
            res.append(("OK", f"duración {m} meses dentro del plazo de {plazo}"))
    return res, tot, por_cuenta


# ---------------------------------------------------------------- perfil desde 00_estado.md
JURIDICA = re.compile(r"\bSpA\b|\bLtda\b|\bS\.?A\.?\b|\bEIRL\b|sociedad|persona jur[ií]dica|empresa constituida", re.I)
NATURAL = re.compile(r"persona natural|sin (empresa|sociedad)|sin constituir|no (tenemos|tengo) empresa", re.I)
TRADICIONAL = re.compile(r"panader|minimarket|almac[eé]n|peluquer|restaur|cafeter|amasander|ferreter|botiller|negocio de barrio|"
                         r"emprendimiento tradicional|kiosco|food ?truck|taller mec", re.I)


def perfil_desde_estado(txt, hoy=None):
    """dict con tipo, meses_inicio, ventas_12m, trl, mujeres, tradicional e inicio/fin del proyecto inferidos de 00_estado.md."""
    hoy = hoy or dt.date.today()
    socied = " ".join(re.findall(r"\*\*Situaci[oó]n societaria[^:]*:\*\*\s*(.*)", txt))
    perfil = {}
    if NATURAL.search(socied):
        perfil["tipo"] = "natural"
    elif JURIDICA.search(socied):
        perfil["tipo"] = "juridica"
    m = re.search(r"inicio de actividades[^0-9]{0,40}(\d{4}-\d{2}-\d{2})", txt, re.I)
    if m:
        ini = dt.date.fromisoformat(m.group(1))
        perfil["meses_inicio"] = max(0, (hoy.year - ini.year) * 12 + hoy.month - ini.month - (1 if hoy.day < ini.day else 0))
    v = re.search(r"\*\*Ventas últimos 12 meses \(CLP\):\*\*\s*([\d.,]+)", txt)
    if v:
        perfil["ventas_12m"] = num(v.group(1))
    elif re.search(r"\bsin ventas\b|cero ventas|no (tenemos|tiene|hay) ventas", txt, re.I):
        perfil["ventas_12m"] = 0.0
    t = re.search(r"TRL\s*(\d)", txt)
    if t:
        perfil["trl"] = int(t.group(1))
    perfil["mujeres"] = bool(re.search(r"liderad[ao] por mujer|fundadoras?\b|socias\b", txt, re.I))
    perfil["tradicional"] = bool(TRADICIONAL.search(txt))
    proy = " ".join(re.findall(r"\*\*Proyecto postulado:\*\*\s*(.*)", txt)) or " ".join(re.findall(r"inicio del proyecto[^\n]*", txt, re.I))
    fechas = re.findall(r"\d{4}-\d{2}-\d{2}", proy)
    if fechas:
        perfil["inicio"] = dt.date.fromisoformat(fechas[0])
        if len(fechas) > 1:
            perfil["fin"] = dt.date.fromisoformat(fechas[1])
    if re.search(r"recupera (el )?IVA|cr[eé]dito fiscal", txt, re.I):
        perfil["recupera_iva"] = True
    obj = " ".join(re.findall(r"\*\*Objetivo[^:]*:\*\*\s*(.*)", txt))
    for clave, pat in (("semilla_inicia", r"semilla inicia"), ("semilla_expande", r"semilla expande"), ("anid_startup_ctci", r"startup (ciencia|ctci)"),
                       ("crea_y_valida", r"crea y valida"), ("escalamiento", r"escalamiento"), ("sercotec_semilla_emprende", r"sercotec|capital semilla")):
        if re.search(pat, obj, re.I):
            perfil["instrumento"] = clave
            break
    return perfil
