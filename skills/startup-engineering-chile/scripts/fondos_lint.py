#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Revisa una postulación a fondos públicos antes de subirla (reglas versionadas, solo biblioteca estándar).

  fondos_lint.py instrumentos                                   # lista instrumentos y fecha de verificación
  fondos_lint.py elegibilidad --instrumento semilla_inicia --tipo juridica|natural
                              [--meses-inicio N] [--ventas-12m CLP] [--ventas-solucion CLP]
  fondos_lint.py presupuesto  --instrumento X (--dir RUTA | --csv rendiciones.csv)
  fondos_lint.py rendiciones  (--dir RUTA | --csv rendiciones.csv) --inicio AAAA-MM-DD --fin AAAA-MM-DD
  fondos_lint.py coherencia   --marco documentos/TPL-106_marco_logico_y_gantt.md (--dir RUTA | --csv ...)
  fondos_lint.py caracteres   respuestas.md [--max-defecto N]

Límites de caracteres: anótalos en cada título de respuestas.md, p. ej.
  "## Problema [máx 1500]"  o una línea "<!-- max: 1500 -->" bajo el título.
Las reglas están en assets/fondos/instrumentos.json con fecha de verificación y fuente. Cambian por
convocatoria: el resultado es una revisión previa, no una certificación de admisibilidad. Contrasta
siempre con las bases del llamado vigente.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGLAS = os.path.join(SKILL_DIR, "assets", "fondos", "instrumentos.json")
NO_FINANCIABLES = ["inmueble", "compra de terreno", "vehículo", "vehiculo", "camioneta", "automóvil", "deuda", "multa", "interés", "intereses", "iva recuperable",
                   "dividendo", "acciones", "garantía", "garantia", "gasto previo", "retiro de socio"]


def reglas():
    r = json.load(open(REGLAS, encoding="utf-8"))
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


def filas_rendicion(a):
    path = a.csv or os.path.join(os.path.abspath(a.dir or "."), "expediente", "registros", "rendiciones.csv")
    if not os.path.exists(path):
        sys.exit(f"No encontré {path}. Registra el presupuesto con: expediente.py add rendiciones actividad=… presupuesto_CLP=…")
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [r for r in csv.DictReader(fh) if any((v or "").strip() for v in r.values())]


def salida(resultados, nota):
    simbolo = {"CUMPLE": "✅", "NO CUMPLE": "❌", "FALTA DATO": "❔", "VERIFICAR": "🔎", "OK": "✅", "PROBLEMA": "❌", "AVISO": "⚠"}
    for est, txt in resultados:
        print(f"{simbolo.get(est, '·')} {est}: {txt}")
    print(f"\n{nota}")
    sys.exit(1 if any(e in ("NO CUMPLE", "PROBLEMA") for e, _ in resultados) else 0)


def cmd_instrumentos(a):
    r, nota = reglas()
    print("| Clave | Instrumento | Tope subsidio | Cofinanciamiento máx. | Fuente |\n|---|---|---|---|---|")
    for k, i in r["instrumentos"].items():
        tope = clp(i["tope_subsidio_CLP"]) if i.get("tope_subsidio_CLP") else "según bases"
        cof = f"{i['cofinanciamiento_max'] * 100:.0f}%" if i.get("cofinanciamiento_max") else "según bases"
        print(f"| {k} | {i['nombre']} | {tope} | {cof} | {i.get('fuente', '')} |")
    print(f"\n{nota}")


def cmd_elegibilidad(a):
    r, nota = reglas()
    i = instrumento(r, a.instrumento)
    res = []
    tipos = i.get("beneficiarios", [])
    if tipos:
        res.append(("CUMPLE" if a.tipo in tipos else "NO CUMPLE", f"tipo de postulante '{a.tipo}' (admite: {', '.join(tipos)})"))
    reglas_tipo = i.get("por_tipo", {}).get(a.tipo, {})
    mmax, mmin = reglas_tipo.get("meses_inicio_max"), reglas_tipo.get("meses_inicio_min")
    if mmax is not None or mmin is not None:
        if a.meses_inicio is None:
            res.append(("FALTA DATO", "meses desde el inicio de actividades en el SII"))
        else:
            ok = (mmax is None or a.meses_inicio < mmax) and (mmin is None or a.meses_inicio >= mmin)
            rango = (f"< {mmax}" if mmax is not None else "") + (f" y ≥ {mmin}" if mmin is not None else "")
            res.append(("CUMPLE" if ok else "NO CUMPLE", f"antigüedad {a.meses_inicio} meses (regla: {rango.strip(' y')})"))
    vmax, vmin = reglas_tipo.get("ventas_12m_max_CLP"), reglas_tipo.get("ventas_12m_min_CLP")
    if vmax is not None or vmin is not None:
        if a.ventas_12m is None:
            res.append(("FALTA DATO", "ventas netas de los últimos 12 meses"))
        else:
            ok = (vmax is None or a.ventas_12m <= vmax) and (vmin is None or a.ventas_12m >= vmin)
            res.append(("CUMPLE" if ok else "NO CUMPLE",
                        f"ventas 12 meses {clp(a.ventas_12m)} (regla: {('≥ ' + clp(vmin)) if vmin is not None else ''}"
                        f"{' y ' if vmin is not None and vmax is not None else ''}{('≤ ' + clp(vmax)) if vmax is not None else ''})"))
    smin = reglas_tipo.get("ventas_solucion_min_CLP")
    if smin is not None:
        if a.ventas_solucion is None:
            res.append(("FALTA DATO", "ventas de la solución postulada"))
        else:
            res.append(("CUMPLE" if a.ventas_solucion >= smin else "NO CUMPLE",
                        f"ventas de la solución {clp(a.ventas_solucion)} (mínimo {clp(smin)})"))
    if reglas_tipo.get("sin_ventas") and a.ventas_12m:
        res.append(("NO CUMPLE", "la regla de referencia exige no tener ventas para este tipo de postulante"))
    for v in i.get("verificar", []):
        res.append(("VERIFICAR", v))
    print(f"## {i['nombre']} — fuente: {i.get('fuente', '')}\n")
    salida(res, nota)


def cmd_presupuesto(a):
    r, nota = reglas()
    i = instrumento(r, a.instrumento)
    filas = filas_rendicion(a)
    res = []
    tot = {"presupuesto": 0.0, "subsidio": 0.0, "aporte": 0.0}
    por_cuenta = {}
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
        texto = (f.get("actividad", "") + " " + f.get("cuenta_presupuestaria", "") + " " + f.get("proveedor", "")).lower()
        hit = [k for k in NO_FINANCIABLES if k in texto]
        if hit:
            res.append(("AVISO", f"{gid}: '{hit[0]}' suele ser no financiable; confirma en las bases"))
        if not f.get("actividad", "").strip() or not f.get("resultado", "").strip():
            res.append(("AVISO", f"{gid}: falta actividad o resultado (cada gasto debe servir a un resultado)"))
        tot["presupuesto"] += p
        tot["subsidio"] += s
        tot["aporte"] += ap
        c = f.get("cuenta_presupuestaria", "") or "(sin cuenta)"
        por_cuenta[c] = por_cuenta.get(c, 0.0) + p
    if not filas:
        sys.exit("rendiciones.csv no tiene filas.")
    tope = i.get("tope_subsidio_CLP")
    if tope:
        res.append(("OK" if tot["subsidio"] <= tope else "PROBLEMA", f"subsidio total {clp(tot['subsidio'])} vs tope {clp(tope)}"))
    cof = i.get("cofinanciamiento_max")
    if cof and tot["presupuesto"]:
        share = tot["subsidio"] / tot["presupuesto"]
        res.append(("OK" if share <= cof + 1e-9 else "PROBLEMA",
                    f"subsidio = {share * 100:.1f}% del costo total (máximo {cof * 100:.0f}%); aporte mínimo {clp(tot['presupuesto'] * (1 - cof))}, tienes {clp(tot['aporte'])}"))
    for c, lim in (i.get("topes_por_cuenta_pct") or {}).items():
        v = sum(x for k, x in por_cuenta.items() if c.lower() in k.lower())
        if tot["presupuesto"] and v / tot["presupuesto"] > lim:
            res.append(("PROBLEMA", f"cuenta '{c}' = {v / tot['presupuesto'] * 100:.0f}% (tope de referencia {lim * 100:.0f}%)"))
    print(f"## Presupuesto vs {i['nombre']}\n")
    print("| Cuenta | Monto | % |\n|---|---|---|")
    for c, v in sorted(por_cuenta.items(), key=lambda x: -x[1]):
        print(f"| {c} | {clp(v)} | {v / tot['presupuesto'] * 100:.0f}% |")
    print(f"| **Total** | **{clp(tot['presupuesto'])}** | subsidio {clp(tot['subsidio'])} · aporte {clp(tot['aporte'])} |\n")
    salida(res, nota)


def fecha(v):
    try:
        return dt.date.fromisoformat((v or "").strip()[:10])
    except ValueError:
        return None


def cmd_rendiciones(a):
    filas = filas_rendicion(a)
    ini, fin = fecha(a.inicio), fecha(a.fin)
    if not ini or not fin:
        sys.exit("--inicio y --fin deben ser AAAA-MM-DD (fechas del convenio).")
    res, docs = [], {}
    for f in filas:
        gid = f.get("gasto_id", "?")
        p, c, pg = num(f.get("presupuesto_CLP")), num(f.get("comprometido_CLP")), num(f.get("pagado_CLP"))
        d = fecha(f.get("fecha"))
        if not d:
            res.append(("PROBLEMA", f"{gid}: fecha vacía o no AAAA-MM-DD"))
        elif not ini <= d <= fin:
            res.append(("PROBLEMA", f"{gid}: fecha {d} fuera del período del proyecto ({ini} a {fin})"))
        if pg > c + 1 and c:
            res.append(("PROBLEMA", f"{gid}: pagado {clp(pg)} > comprometido {clp(c)}"))
        if c > p + 1 and p:
            res.append(("AVISO", f"{gid}: comprometido {clp(c)} > presupuesto {clp(p)} (requiere reitemización autorizada)"))
        if pg > 0:
            if not f.get("documento", "").strip():
                res.append(("PROBLEMA", f"{gid}: pagado sin documento (factura/boleta)"))
            if not f.get("medio_verificacion", "").strip():
                res.append(("AVISO", f"{gid}: sin medio de verificación (transferencia, contrato, entregable)"))
        doc = f.get("documento", "").strip().lower()
        if doc:
            if doc in docs:
                res.append(("PROBLEMA", f"{gid}: documento '{f['documento']}' repetido (también en {docs[doc]})"))
            docs[doc] = gid
    if not res:
        res.append(("OK", f"{len(filas)} gasto(s) sin problemas de forma"))
    salida(res, "Revisión de forma. La aceptación de cada gasto depende del manual de rendición vigente y del ejecutivo.")


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


def parecido(a_, b_):
    A, B = set(norm(a_)), set(norm(b_))
    return len(A & B) / max(1, min(len(A), len(B)))


def cmd_coherencia(a):
    txt = open(a.marco, encoding="utf-8-sig").read()
    actividades = []
    for tabla in re.findall(r"((?:^\|.*\|\s*\n)+)", txt, re.M):
        lineas = [l for l in tabla.strip().splitlines() if not re.match(r"^\|\s*-", l)]
        if not lineas:
            continue
        cab = [c.strip().lower() for c in lineas[0].strip("|").split("|")]
        col = next((k for k, c in enumerate(cab) if "actividad" in c), None)
        if col is None:
            # tabla de dos columnas Campo | Contenido: filas cuyo campo dice "Actividad"
            for l in lineas[1:]:
                cs = [c.strip() for c in l.strip("|").split("|")]
                if len(cs) > 1 and "actividad" in cs[0].lower() and cs[1]:
                    actividades.append(cs[1])
            continue
        for l in lineas[1:]:
            cs = [c.strip() for c in l.strip("|").split("|")]
            if len(cs) > col and cs[col] and not cs[col].startswith("["):
                actividades.append(cs[col])
    filas = filas_rendicion(a)
    res = []
    if not actividades:
        sys.exit("No encontré actividades en el marco lógico (busco una columna o fila llamada 'Actividad').")
    for act in actividades:
        if not any(parecido(act, f.get("actividad", "")) >= 0.6 for f in filas):
            res.append(("PROBLEMA", f"actividad sin presupuesto: '{act[:80]}'"))
    for f in filas:
        if not any(parecido(f.get("actividad", ""), act) >= 0.6 for act in actividades):
            res.append(("AVISO", f"{f.get('gasto_id', '?')}: gasto '{f.get('actividad', '')[:60]}' no corresponde a una actividad del marco lógico"))
    if not res:
        res.append(("OK", f"{len(actividades)} actividades y {len(filas)} gastos coinciden"))
    salida(res, "Coincidencia por palabras (≥60%). Revisa los avisos a mano: puede ser un nombre distinto para lo mismo.")


def cmd_caracteres(a):
    txt = open(a.archivo, encoding="utf-8-sig").read()
    partes = re.split(r"^(#{1,3} .+)$", txt, flags=re.M)
    res = []
    print("| Respuesta | Caracteres (con espacios) | Sin espacios | Máximo | Estado |\n|---|---|---|---|---|")
    for k in range(1, len(partes), 2):
        titulo, cuerpo = partes[k], partes[k + 1]
        m = re.search(r"\[m[aá]x\.?\s*([\d.]+)\]|\(m[aá]x\.?\s*([\d.]+)\s*caracteres\)", titulo, re.I) or \
            re.search(r"<!--\s*max:\s*([\d.]+)\s*-->", cuerpo)
        limite = int((next(g for g in m.groups() if g)).replace(".", "")) if m else a.max_defecto
        limpio = re.sub(r"<!--.*?-->", "", cuerpo, flags=re.S).strip()
        con, sin = len(limpio), len(re.sub(r"\s", "", limpio))
        nombre = re.sub(r"\s*(\[m[aá]x.*?\]|\(m[aá]x.*?\))", "", titulo.lstrip("# ")).strip()
        if not con and not m:
            continue
        if limite:
            estado = "OK" if con <= limite else f"EXCEDE por {con - limite}"
            if con > limite:
                res.append(("PROBLEMA", f"'{nombre}' excede {con - limite} caracteres"))
            elif con < 0.5 * limite:
                res.append(("AVISO", f"'{nombre}' usa menos de la mitad del espacio ({con}/{limite}); ¿falta evidencia?"))
        else:
            estado = "sin límite anotado"
        print(f"| {nombre[:50]} | {con} | {sin} | {limite or '—'} | {estado} |")
    print()
    if not res:
        res.append(("OK", "todas las respuestas dentro del límite"))
    salida(res, "El portal puede contar distinto (saltos de línea, tildes): deja un margen de ~3%.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("instrumentos"); p.set_defaults(f=cmd_instrumentos)
    p = sp.add_parser("elegibilidad"); p.add_argument("--instrumento", required=True)
    p.add_argument("--tipo", required=True, choices=["natural", "juridica"]); p.add_argument("--meses-inicio", type=float)
    p.add_argument("--ventas-12m", type=float); p.add_argument("--ventas-solucion", type=float); p.set_defaults(f=cmd_elegibilidad)
    for nombre, fn in (("presupuesto", cmd_presupuesto), ("rendiciones", cmd_rendiciones), ("coherencia", cmd_coherencia)):
        p = sp.add_parser(nombre); p.add_argument("--dir"); p.add_argument("--csv")
        if nombre == "presupuesto":
            p.add_argument("--instrumento", required=True)
        if nombre == "rendiciones":
            p.add_argument("--inicio", required=True); p.add_argument("--fin", required=True)
        if nombre == "coherencia":
            p.add_argument("--marco", required=True)
        p.set_defaults(f=fn)
    p = sp.add_parser("caracteres"); p.add_argument("archivo"); p.add_argument("--max-defecto", type=int, default=0)
    p.set_defaults(f=cmd_caracteres)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
