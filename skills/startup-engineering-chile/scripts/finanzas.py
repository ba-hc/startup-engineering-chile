#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Cálculos financieros deterministas para startups en Chile (no los hagas "a ojo" en el chat).

  finanzas.py unit         --precio P --costo-variable CV --cac CAC --churn 0.03 [--meses-max 60]
  finanzas.py equilibrio   --costos-fijos CF --precio P --costo-variable CV
  finanzas.py runway       --caja C --gasto G [--ingreso I] [--crecimiento-ingreso 0.05]
  finanzas.py escenarios   --modelo modelo_financiero.xlsx [--meses 24]   # o con flags (ver --help)
  finanzas.py dilucion     --fundadores "Ana:60,Beto:40" [--pool 0] [--safe MONTO:CAP_POST[:DESC%] ...]
                           [--pre VALOR_PRE --inversion MONTO --pool-post 10]
  finanzas.py salida       --comunes "Ana:6000000,Beto:4000000" [--preferentes "Seed:MONTO:ACCIONES"]
                           [--opciones "Yo:CANTIDAD:PRECIO_EJERCICIO"] --valores 1e9,5e9 [--multiplo 1]
  finanzas.py costo-empleado (--bruto B | --liquido L) [--contrato indefinido|plazo-fijo]
                           [--mutual-adicional 0] [--gratificacion] [--provision-indemnizacion]
                           [--uf V] [--utm V]
  finanzas.py honorarios   (--bruto B | --liquido L)

Todo en CLP salvo que se indique. Los parámetros legales (tasas, topes, tramos) vienen de
assets/parametros_cl.json con su fecha de verificación: el script la muestra y avisa si tiene más
de 6 meses. Es orientación educativa, no asesoría contable, laboral ni tributaria.
"""
import argparse
import datetime as dt
import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARAMS = os.path.join(SKILL_DIR, "assets", "parametros_cl.json")


def clp(x):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "—"
    s = f"{abs(x):,.0f}".replace(",", ".")
    return ("-$" if x < 0 else "$") + s


def miles(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(x):
    return "—" if x is None else f"{x * 100:.1f}%".replace(".", ",")


def params():
    p = json.load(open(PARAMS, encoding="utf-8"))
    ver = p.get("_verificado")
    if ver:
        edad = (dt.date.today() - dt.date.fromisoformat(ver)).days
        nota = f"Parámetros verificados el {ver}"
        if edad > 183:
            nota += f" (hace {edad} días: VERIFICA tasas y topes antes de usarlos)"
        print(nota + ".\n")
    return p


def valor(p, clave):
    v = p[clave]
    return v["valor"] if isinstance(v, dict) else v


def indicador(nombre, explicito):
    """UF/UTM: argumento explícito > caché de indicadores_cl.py > respaldo en parametros_cl.json."""
    if explicito:
        return float(explicito), "argumento"
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import indicadores_cl
        v, fecha, origen = indicadores_cl.valor(nombre, red=False)
        if v:
            return v, f"{origen} {fecha}"
    except Exception:
        pass
    r = params().get("respaldo_indicadores", {}).get(nombre)
    if r:
        return float(r["valor"]), f"respaldo {r['fecha']} (pasa --{nombre} con el valor del día si necesitas precisión)"
    sys.exit(f"Falta el valor de {nombre.upper()}: pásalo con --{nombre} o ejecuta indicadores_cl.py obtener")


# ---------------------------------------------------------------- unit economics
def cmd_unit(a):
    contrib = a.precio - a.costo_variable
    margen = contrib / a.precio if a.precio else None
    print("| Métrica | Valor | Fórmula |\n|---|---|---|")
    print(f"| Contribución mensual por cliente | {clp(contrib)} | precio − costo variable |")
    print(f"| Margen de contribución | {pct(margen)} | contribución / precio |")
    alertas = []
    if contrib <= 0:
        alertas.append("Contribución ≤ 0: cada cliente pierde plata; LTV, payback y equilibrio no tienen sentido.")
    else:
        payback = a.cac / contrib
        print(f"| Payback del CAC | {payback:.1f} meses | CAC / contribución |")
        if a.churn and a.churn > 0:
            vida = min(1 / a.churn, a.meses_max)
            ltv = contrib * vida
            print(f"| Vida esperada | {vida:.1f} meses | 1 / churn (tope {a.meses_max}) |")
            print(f"| LTV (sobre contribución) | {clp(ltv)} | contribución × vida |")
            print(f"| LTV / CAC | {ltv / a.cac:.2f} | |" if a.cac else "| LTV / CAC | — | CAC = 0 |")
            ltv_mal = a.precio * vida
            print(f"| (Error común) LTV sobre ingreso | {clp(ltv_mal)} | precio × vida: infla {ltv_mal / ltv:.1f}× |")
            if 1 / a.churn > a.meses_max:
                alertas.append(f"Churn {pct(a.churn)} implica vida > {a.meses_max} meses: se topó. Sin cohortes reales, no lo uses en un pitch.")
            if a.churn < 0.01:
                alertas.append("Churn mensual < 1% es raro en etapa temprana; exige datos de cohortes (cohortes.csv).")
            if a.cac and ltv / a.cac < 3:
                alertas.append("LTV/CAC < 3: el modelo de adquisición es frágil (referencia común de SaaS, no una regla).")
        else:
            alertas.append("Sin churn (> 0) no hay LTV: no uses churn cero.")
        if payback > 18:
            alertas.append("Payback > 18 meses: necesitas mucha caja para crecer.")
    if margen is not None and margen < 0.5:
        alertas.append("Margen < 50%: revisa costos variables (infraestructura, soporte, implementación) antes de escalar.")
    for x in alertas:
        print(f"\n⚠ {x}")


def cmd_equilibrio(a):
    contrib = a.precio - a.costo_variable
    if contrib <= 0:
        sys.exit("Contribución ≤ 0: no hay punto de equilibrio con este precio y costo variable.")
    n = math.ceil(a.costos_fijos / contrib)
    print(f"Punto de equilibrio: {n} clientes activos ({clp(a.costos_fijos)} / {clp(contrib)} de contribución, redondeado hacia arriba).")
    print(f"Ingreso mensual en equilibrio: {clp(n * a.precio)}.")


def cmd_runway(a):
    burn = a.gasto - a.ingreso
    if burn <= 0:
        print(f"Sin quema neta (ingreso {clp(a.ingreso)} ≥ gasto {clp(a.gasto)}): runway indefinido mientras se mantenga.")
        return
    simple = a.caja / burn
    print(f"Burn neto mensual: {clp(burn)}\nRunway simple: {simple:.1f} meses (caja / burn)")
    if a.crecimiento_ingreso:
        caja, ing, mes = a.caja, a.ingreso, 0
        while caja > 0 and mes < 120:
            mes += 1
            caja -= a.gasto - ing
            ing *= 1 + a.crecimiento_ingreso
            if ing >= a.gasto:
                print(f"Con ingreso creciendo {pct(a.crecimiento_ingreso)} mensual llegas a equilibrio en el mes {mes} con caja {clp(caja)}.")
                return
        print(f"Con ingreso creciendo {pct(a.crecimiento_ingreso)} mensual, la caja se acaba en el mes {mes}.")
    print("Recuerda: subsidio ≠ venta, y facturar ≠ cobrar (usa escenarios con cobro diferido).")


# ---------------------------------------------------------------- escenarios
CLAVES_MODELO = {"precio": "Precio mensual", "infra": "Infraestructura variable", "soporte": "Soporte directo",
                 "fijos": "Costos fijos", "cac": "CAC", "altas": "Altas objetivo por mes", "churn": "Churn mensual",
                 "caja": "Caja inicial", "impl_precio": "Precio implementación", "impl_costo": "Costo implementación",
                 "capex": "CAPEX inicial", "diferido": "Cobro diferido", "capital": "Capital externo",
                 "subsidio": "Subsidio cobrado", "mes_subsidio": "Mes de desembolso", "capacidad": "Capacidad de onboarding",
                 "clientes0": "Clientes iniciales"}
FACTORES = {"pesimista": {"altas": 0.5, "churn": 1.5, "cac": 1.3, "precio": 0.9},
            "base": {},
            "optimista": {"altas": 1.5, "churn": 0.7, "cac": 0.8, "precio": 1.0}}


def simular(s, meses):
    clientes, caja, cobro_pend = s["clientes0"], s["caja"], 0.0
    minimo, mes_min, mes_quiebre = caja, 0, None
    for m in range(1, meses + 1):
        altas = min(s["altas"], s["capacidad"]) if s["capacidad"] else s["altas"]
        bajas = clientes * s["churn"]
        facturado = clientes * s["precio"] + altas * s["impl_precio"]
        cobrado = cobro_pend + facturado * (1 - s["diferido"])
        cobro_pend = facturado * s["diferido"]
        costos = s["fijos"] + clientes * (s["infra"] + s["soporte"]) + altas * (s["cac"] + s["impl_costo"])
        otros = (s["capital"] - s["capex"]) if m == 1 else 0
        otros += s["subsidio"] if m == int(s["mes_subsidio"] or 1) else 0
        caja += cobrado - costos + otros
        clientes = clientes + altas - bajas
        if caja < minimo:
            minimo, mes_min = caja, m
        if caja < 0 and mes_quiebre is None:
            mes_quiebre = m
    return {"clientes": clientes, "caja": caja, "minimo": minimo, "mes_min": mes_min, "quiebre": mes_quiebre}


def cmd_escenarios(a):
    s = {k: 0.0 for k in CLAVES_MODELO}
    if a.modelo:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import modelo_xlsx
        vals = {f["variable"]: f["valor"] for f in modelo_xlsx.supuestos(a.modelo)}
        for k, etiqueta in CLAVES_MODELO.items():
            if etiqueta in vals and modelo_xlsx.numero(vals[etiqueta]) is not None:
                s[k] = float(vals[etiqueta])
    for k in CLAVES_MODELO:
        v = getattr(a, k, None)
        if v is not None:
            s[k] = v
    if not s["precio"]:
        sys.exit("Faltan supuestos: usa --modelo ARCHIVO.xlsx o pasa al menos --precio, --fijos, --altas, --churn y --caja.")
    print(f"Simulación mensual independiente ({a.meses} meses) con los supuestos del modelo; no reemplaza la planilla.\n")
    print("| Escenario | Clientes al final | Caja al final | Caja mínima (mes) | Mes en que la caja queda negativa |")
    print("|---|---|---|---|---|")
    for nombre, fac in FACTORES.items():
        e = dict(s)
        for k, f in fac.items():
            e[k] = e[k] * f
        r = simular(e, a.meses)
        print(f"| {nombre} | {r['clientes']:.1f} | {clp(r['caja'])} | {clp(r['minimo'])} (mes {r['mes_min']}) | {r['quiebre'] or 'no ocurre'} |")
    print("\nPesimista: altas ×0,5, churn ×1,5, CAC ×1,3, precio ×0,9. Optimista: altas ×1,5, churn ×0,7, CAC ×0,8.")
    print("Son supuestos de sensibilidad, no probabilidades. Subsidio y capital no son ingresos comerciales.")


# ---------------------------------------------------------------- dilución
def parse_pares(texto):
    out = []
    for parte in texto.split(","):
        nombre, _, v = parte.partition(":")
        out.append((nombre.strip(), float(v)))
    return out


def parse_safe(s):
    partes = [x.strip().rstrip("%") for x in s.split(":")]
    monto = float(partes[0])
    cap = float(partes[1]) if len(partes) > 1 and partes[1] not in ("", "0") else None
    desc = float(partes[2]) / 100 if len(partes) > 2 and partes[2] else 0.0
    if desc >= 1:
        sys.exit("El descuento va en porcentaje (p. ej. 20), no como fracción mayor a 1.")
    return monto, cap, desc


def cmd_dilucion(a):
    fundadores = parse_pares(a.fundadores)
    total_f = sum(v for _, v in fundadores)
    BASE = 10_000_000
    acciones = {n: BASE * v / total_f * (1 - a.pool / 100) for n, v in fundadores}
    if a.pool:
        acciones["Pool de opciones"] = BASE * a.pool / 100
    T0 = sum(acciones.values())
    P0 = acciones.get("Pool de opciones", 0.0)
    safes = [parse_safe(s) for s in a.safe or []]
    tabla = [("Antes de convertir instrumentos", dict(acciones))]
    ronda = bool(a.pre and a.inversion)
    if safes and not ronda:
        if any(c is None for _, c, _ in safes):
            sys.exit("Un SAFE sin cap solo convierte en una ronda con precio: agrega --pre y --inversion.")
        s_total = sum(m / c for m, c, _ in safes)
        if s_total >= 1:
            sys.exit("Los SAFE suman ≥ 100% de propiedad: revisa montos y caps.")
        X = s_total * T0 / (1 - s_total)
        for i, (m, c, _) in enumerate(safes, 1):
            acciones[f"SAFE {i} ({clp(m)} cap {clp(c)})"] = X * (m / c) / s_total
        tabla.append(("Con los SAFE convertidos al cap (post-money)", dict(acciones)))
    if ronda:
        p = a.pool_post / 100
        S, Padd, detalle = 0.0, 0.0, []
        for _ in range(500):
            cap_base = T0 + S                       # capitalización del SAFE post-money (sin el aumento de pool de la ronda)
            precio = a.pre / (T0 + S + Padd)        # el pre-money incluye SAFE convertidos y aumento de pool
            nuevos, detalle = [], []
            for m, cap, d in safes:
                opciones = {"precio de la ronda": precio}
                if cap:
                    opciones["cap"] = cap / cap_base
                if d:
                    opciones[f"descuento {d * 100:.0f}%"] = precio * (1 - d)
                via = min(opciones, key=opciones.get)
                nuevos.append(m / opciones[via])
                detalle.append((m, cap, d, opciones[via], via))
            S_n = sum(nuevos)
            N = T0 + S_n + Padd + a.inversion / precio
            Padd_n = max(0.0, p * N - P0) if p else 0.0
            if abs(S_n - S) < 1e-6 and abs(Padd_n - Padd) < 1e-6:
                break
            S, Padd = S_n, Padd_n
        else:
            sys.exit("El cálculo no converge: revisa caps, descuentos y valorización.")
        for i, (m, cap, d, pr, via) in enumerate(detalle, 1):
            etiqueta = f"SAFE {i} ({clp(m)}" + (f", cap {clp(cap)}" if cap else "") + (f", desc. {d * 100:.0f}%" if d else "") + ")"
            acciones[etiqueta] = m / pr
        if Padd:
            acciones["Pool de opciones"] = P0 + Padd
        acciones["Inversionista ronda"] = a.inversion / precio
        tabla.append((f"Después de la ronda (pre {clp(a.pre)}, inversión {clp(a.inversion)})", dict(acciones)))
        print(f"Precio por acción de la ronda: {miles(precio, 2)} CLP.")
        for i, (m, cap, d, pr, via) in enumerate(detalle, 1):
            print(f"SAFE {i} convierte a {miles(pr, 2)} CLP por acción (aplica: {via}).")
        if Padd:
            print(f"Aumento de pool antes de la ronda: {miles(Padd)} acciones (lo pagan los accionistas previos).")
        print()
    for titulo, acc in tabla:
        tot = sum(acc.values())
        print(f"### {titulo}\n| Titular | Acciones | % |\n|---|---|---|")
        for n, v in acc.items():
            print(f"| {n} | {miles(v)} | {pct(v / tot)} |")
        print()
    print("Supuestos: SAFE post-money estilo YC (cap sobre la capitalización sin el aumento de pool de la ronda; convierte al menor")
    print("entre precio con cap, precio con descuento y precio de la ronda); el pre-money incluye SAFE y aumento de pool.")
    print("El texto exacto de tu SAFE, nota o pacto manda: revísalo con un abogado.")


def parse_lista(texto, campos):
    out = []
    for parte in (texto or "").split(","):
        if not parte.strip():
            continue
        valores = parte.split(":")
        if len(valores) != campos + 1:
            sys.exit(f"Formato inválido en «{parte}»: se esperan {campos + 1} valores separados por ':'.")
        out.append((valores[0].strip(), *[float(v) for v in valores[1:]]))
    return out


def reparto_salida(V, comunes, preferentes, opciones, multiplo=1.0):
    """Cascada con preferencia de liquidación no participativa (pari passu). Devuelve {titular: monto} y precio por acción común."""
    pref = {n: m * multiplo for n, m, _ in preferentes}
    convierte = {n: False for n, _, _ in preferentes}
    ejerce = {n: False for n, _, _ in opciones}
    precio = 0.0
    for _ in range(100):
        caja = V + sum(q * k for n, q, k in opciones if ejerce[n])
        reservado = sum(pref[n] for n in pref if not convierte[n])
        if caja <= reservado:
            total = sum(pref[n] for n in pref if not convierte[n]) or 1
            pago = {n: caja * pref[n] / total if not convierte[n] else 0.0 for n in pref}
            pago.update({n: 0.0 for n, _ in comunes})
            pago.update({n: 0.0 for n, _, _ in opciones})
            return pago, 0.0
        acciones = sum(s for _, s in comunes) + sum(s for n, _, s in preferentes if convierte[n]) + sum(q for n, q, _ in opciones if ejerce[n])
        precio = (caja - reservado) / acciones
        nuevo_c = {n: precio * s > pref[n] for n, _, s in preferentes}
        nuevo_e = {n: precio > k for n, _, k in opciones}
        if nuevo_c == convierte and nuevo_e == ejerce:
            break
        convierte, ejerce = nuevo_c, nuevo_e
    pago = {n: (precio * s if convierte[n] else pref[n]) for n, _, s in preferentes}
    pago.update({n: precio * s for n, s in comunes})
    pago.update({n: (precio - k) * q if ejerce[n] else 0.0 for n, q, k in opciones})
    return pago, precio


def cmd_salida(a):
    comunes = parse_pares(a.comunes)
    preferentes = parse_lista(a.preferentes, 2)
    opciones = parse_lista(a.opciones, 2)
    valores = [float(v) for v in a.valores.split(",")]
    titulares = [n for n, _, _ in preferentes] + [n for n, _ in comunes] + [n for n, _, _ in opciones]
    res = [reparto_salida(V, comunes, preferentes, opciones, a.multiplo) for V in valores]
    print("| Titular | " + " | ".join(f"Salida {clp(V)}" for V in valores) + " |")
    print("|---|" + "---|" * len(valores))
    for n in titulares:
        print(f"| {n} | " + " | ".join(f"{clp(r[0][n])} ({pct(r[0][n] / V if V else 0)})" for r, V in zip(res, valores)) + " |")
    print("| Precio por acción común | " + " | ".join(miles(r[1], 2) for r in res) + " |")
    print(f"\nSupuestos: preferencia {a.multiplo:g}x no participativa y pari passu entre preferentes; cada preferente elige el mayor entre")
    print("su preferencia y convertir a común; las opciones se ejercen si el precio supera su precio de ejercicio (monto neto del")
    print("ejercicio, antes de impuestos). Sin deuda, costos de transacción ni retenciones. Revisa el pacto real con un abogado.")


# ---------------------------------------------------------------- costo empleado (Chile)
def impuesto_unico(base_clp, utm, tramos):
    base_utm = base_clp / utm
    for t in tramos:
        if t["hasta_utm"] is None or base_utm <= t["hasta_utm"]:
            return max(0.0, base_clp * t["tasa"] - t["rebaja_utm"] * utm)
    return 0.0


def calcular_empleado(bruto, a, p, uf, utm):
    tope_afp = valor(p, "tope_imponible_afp_uf") * uf
    tope_afc = valor(p, "tope_imponible_afc_uf") * uf
    grat = 0.0
    if a.gratificacion:
        grat = min(bruto * 0.25, valor(p, "ingreso_minimo_mensual") * 4.75 / 12)
    imponible = bruto + grat
    base_afp = min(imponible, tope_afp)
    base_afc = min(imponible, tope_afc)
    indef = a.contrato == "indefinido"
    emp = {
        "Seguro de cesantía (empleador)": base_afc * valor(p, "afc_empleador_indefinido" if indef else "afc_empleador_plazo_fijo"),
        "Mutual / Ley 16.744": base_afp * (valor(p, "mutual_basica") + a.mutual_adicional),
        "Aporte empleador reforma de pensiones (incluye SIS)": base_afp * valor(p, "aporte_empleador_reforma"),
    }
    if a.provision_indemnizacion and indef:
        emp["Provisión indemnización años de servicio"] = min(imponible, 90 * uf) / 12
    trab = {
        "AFP (10% + comisión)": base_afp * (0.10 + valor(p, "comision_afp_referencia")),
        "Salud (7%)": base_afp * 0.07,
        "Seguro de cesantía (trabajador)": base_afc * (valor(p, "afc_trabajador_indefinido") if indef else 0.0),
    }
    tributable = imponible - sum(trab.values())
    trab["Impuesto único"] = impuesto_unico(tributable, utm, p["impuesto_unico_tramos"]["valor"])
    liquido = imponible - sum(trab.values())
    return grat, imponible, emp, trab, liquido


def cmd_costo_empleado(a):
    p = params()
    uf, uf_o = indicador("uf", a.uf)
    utm, utm_o = indicador("utm", a.utm)
    if a.liquido:
        lo, hi = a.liquido, a.liquido * 2.5
        for _ in range(80):
            mid = (lo + hi) / 2
            if calcular_empleado(mid, a, p, uf, utm)[4] < a.liquido:
                lo = mid
            else:
                hi = mid
        bruto = hi
    else:
        bruto = a.bruto
    grat, imponible, emp, trab, liquido = calcular_empleado(bruto, a, p, uf, utm)
    costo = imponible + sum(emp.values())
    print(f"UF {clp(uf)} ({uf_o}) · UTM {clp(utm)} ({utm_o}) · contrato {a.contrato}\n")
    print("| Concepto | Monto mensual |\n|---|---|")
    print(f"| Sueldo base bruto | {clp(bruto)} |")
    if grat:
        print(f"| Gratificación legal (25%, tope 4,75 IMM/año) | {clp(grat)} |")
    print(f"| **Total imponible** | **{clp(imponible)}** |")
    for k, v in trab.items():
        print(f"| − {k} | {clp(v)} |")
    print(f"| **Líquido estimado** | **{clp(liquido)}** |")
    for k, v in emp.items():
        print(f"| + {k} | {clp(v)} |")
    print(f"| **Costo empresa mensual** | **{clp(costo)}** |")
    print(f"| Costo empresa anual (×12) | {clp(costo * 12)} |")
    print(f"\nEl costo empresa es {pct(costo / liquido - 1)} más que el líquido y {pct(costo / imponible - 1)} sobre el imponible.")
    print("No incluye: horas extra, bonos, colación/movilización (no imponibles), vacaciones de reemplazo ni beneficios.")
    print("Comisión AFP y mutual adicional varían por AFP y empresa. Confirma con tu contador o la liquidación real.")


def cmd_honorarios(a):
    p = params()
    tasa = valor(p, "retencion_honorarios")
    if a.liquido:
        bruto = a.liquido / (1 - tasa)
    else:
        bruto = a.bruto
    ret = bruto * tasa
    print(f"Retención de boleta de honorarios {pct(tasa)} ({p['retencion_honorarios'].get('nota', '')})\n")
    print(f"| Bruto de la boleta | {clp(bruto)} |\n|---|---|\n| Retención (la paga quien recibe la boleta, si es empresa) | {clp(ret)} |\n| Líquido para quien emite | {clp(bruto - ret)} |")
    print("\nPara la empresa el costo es el bruto. Ojo en rendiciones de fondos: revisa si las bases admiten honorarios de socios.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("unit"); p.add_argument("--precio", type=float, required=True)
    p.add_argument("--costo-variable", type=float, required=True); p.add_argument("--cac", type=float, default=0)
    p.add_argument("--churn", type=float, default=0); p.add_argument("--meses-max", type=float, default=60); p.set_defaults(f=cmd_unit)
    p = sp.add_parser("equilibrio"); p.add_argument("--costos-fijos", type=float, required=True)
    p.add_argument("--precio", type=float, required=True); p.add_argument("--costo-variable", type=float, required=True)
    p.set_defaults(f=cmd_equilibrio)
    p = sp.add_parser("runway"); p.add_argument("--caja", type=float, required=True); p.add_argument("--gasto", type=float, required=True)
    p.add_argument("--ingreso", type=float, default=0); p.add_argument("--crecimiento-ingreso", type=float, default=0)
    p.set_defaults(f=cmd_runway)
    p = sp.add_parser("escenarios"); p.add_argument("--modelo"); p.add_argument("--meses", type=int, default=24)
    for k in CLAVES_MODELO:
        p.add_argument("--" + k.replace("_", "-"), dest=k, type=float)
    p.set_defaults(f=cmd_escenarios)
    p = sp.add_parser("dilucion"); p.add_argument("--fundadores", required=True); p.add_argument("--pool", type=float, default=0)
    p.add_argument("--safe", action="append"); p.add_argument("--pre", type=float); p.add_argument("--inversion", type=float)
    p.add_argument("--pool-post", type=float, default=0); p.set_defaults(f=cmd_dilucion)
    p = sp.add_parser("salida"); p.add_argument("--comunes", required=True); p.add_argument("--preferentes", default="")
    p.add_argument("--opciones", default=""); p.add_argument("--valores", required=True); p.add_argument("--multiplo", type=float, default=1.0)
    p.set_defaults(f=cmd_salida)
    p = sp.add_parser("costo-empleado"); g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--bruto", type=float); g.add_argument("--liquido", type=float)
    p.add_argument("--contrato", default="indefinido", choices=["indefinido", "plazo-fijo"])
    p.add_argument("--mutual-adicional", type=float, default=0); p.add_argument("--gratificacion", action="store_true")
    p.add_argument("--provision-indemnizacion", action="store_true"); p.add_argument("--uf"); p.add_argument("--utm")
    p.set_defaults(f=cmd_costo_empleado)
    p = sp.add_parser("honorarios"); g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--bruto", type=float); g.add_argument("--liquido", type=float); p.set_defaults(f=cmd_honorarios)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
