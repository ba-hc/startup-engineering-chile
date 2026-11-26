#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""¿A qué fondos públicos calza este proyecto hoy? Cruza el perfil con los filtros duros de cada instrumento.

  fondos_matcher.py --dir RUTA                       # lee 00_estado.md (situación societaria, ventas, TRL, objetivo)
  fondos_matcher.py --tipo juridica --meses-inicio 10 --ventas-12m 0 [--trl 4] [--mujeres] [--tradicional] [--uf 39000]

Por instrumento muestra: CALZA (pasa todos los filtros duros), NO CALZA (con el filtro que falla) o FALTA DATO,
el tope de subsidio y el cofinanciamiento (con la variante para empresas lideradas por mujeres) y lo que hay que
verificar en las bases. Si el negocio es tradicional (sin innovación escalable: panadería, minimarket, servicios de
barrio), prioriza Sercotec y deriva a references/flujos/sercotec_vs_corfo.md.

Reglas en assets/fondos/instrumentos.json (fecha de verificación incluida). Calzar con los filtros no significa ganar:
la evaluación pondera equipo, mercado e innovación. Siguiente paso para el elegido: presupuesto_corfo.py revisar.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.fondos import clp, condiciones, evaluar_elegibilidad, perfil_desde_estado, reglas  # noqa: E402
from core.storage import leer_estado  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def clasificar(res):
    if any(e == "NO CUMPLE" for e, _ in res):
        return "NO CALZA"
    if any(e == "FALTA DATO" for e, _ in res):
        return "FALTA DATO"
    return "CALZA"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir")
    ap.add_argument("--tipo", choices=["natural", "juridica"])
    ap.add_argument("--meses-inicio", type=float, help="meses desde el inicio de actividades en el SII")
    ap.add_argument("--ventas-12m", type=float, help="ventas netas de los últimos 12 meses en CLP")
    ap.add_argument("--ventas-solucion", type=float)
    ap.add_argument("--trl", type=int)
    ap.add_argument("--uf", type=float, help="valor de la UF para reglas en UF (indicadores_cl.py uf)")
    ap.add_argument("--mujeres", action="store_true", help="empresa liderada por mujeres")
    ap.add_argument("--tradicional", action="store_true", help="negocio sin innovación escalable (deriva a Sercotec)")
    ap.add_argument("--todos", action="store_true", help="muestra también los que no calzan con el detalle completo")
    a = ap.parse_args(argv)
    perfil = perfil_desde_estado(leer_estado(a.dir)) if a.dir else {}
    tipo = a.tipo or perfil.get("tipo")
    meses = a.meses_inicio if a.meses_inicio is not None else perfil.get("meses_inicio")
    ventas = a.ventas_12m if a.ventas_12m is not None else perfil.get("ventas_12m")
    trl = a.trl if a.trl is not None else perfil.get("trl")
    mujeres = a.mujeres or perfil.get("mujeres", False)
    tradicional = a.tradicional or perfil.get("tradicional", False)
    r, nota = reglas()
    print("## Perfil usado\n" + " · ".join([
        f"postulante: {tipo or '¿?'}", f"meses desde inicio de actividades: {meses if meses is not None else '¿?'}",
        f"ventas 12 meses: {clp(ventas) if ventas is not None else '¿?'}", f"TRL: {trl if trl is not None else '¿?'}",
        f"liderada por mujeres: {'sí' if mujeres else 'no/¿?'}", f"negocio tradicional: {'sí' if tradicional else 'no'}"]))
    if a.dir and not perfil:
        print("(00_estado.md no tiene situación societaria, ventas ni TRL legibles: completa el perfil o pasa los datos con flags)")
    filas = []
    for clave, inst in r["instrumentos"].items():
        res = evaluar_elegibilidad(inst, tipo, meses, ventas, a.ventas_solucion, trl, a.uf)
        if "mujeres" in clave and not mujeres:
            res.append(("NO CUMPLE", "solo para empresas lideradas por mujeres (usa --mujeres si aplica)"))
        if tradicional and "tradicional" not in inst.get("perfil", []):
            res.append(("NO CUMPLE", "pide innovación escalable; para un negocio tradicional calza mejor Sercotec"))
        estado = clasificar(res)
        tope, cof = condiciones(inst, mujeres)
        filas.append((estado, clave, inst, tope, cof, res))
    orden = {"CALZA": 0, "FALTA DATO": 1, "NO CALZA": 2}
    filas.sort(key=lambda f: (orden[f[0]], -(f[3] or 0)))
    print("\n| Instrumento | Estado | Tope subsidio | Cofinanciamiento | Motivo / dato faltante |\n|---|---|---|---|---|")
    for estado, clave, inst, tope, cof, res in filas:
        motivo = "; ".join(t for e, t in res if e in ("NO CUMPLE", "FALTA DATO"))[:140] or "pasa los filtros duros"
        print(f"| {inst['nombre']} (`{clave}`) | {estado} | {clp(tope) if tope else 'según bases'} | "
              f"{f'{cof * 100:.0f}%' if cof else 'según bases'} | {motivo} |")
    calzan = [f for f in filas if f[0] == "CALZA"]
    for estado, clave, inst, tope, cof, res in (filas if a.todos else calzan):
        ver = [t for e, t in res if e == "VERIFICAR"]
        if ver:
            print(f"\n### {inst['nombre']} — verificar en las bases\n" + "\n".join(f"- {v}" for v in ver) + f"\n- Fuente: {inst.get('fuente')}")
    if tradicional:
        print("\nNegocio tradicional: revisa references/flujos/sercotec_vs_corfo.md antes de gastar semanas en una postulación CORFO.")
    if calzan:
        print(f"\nSiguiente paso: presupuesto_corfo.py revisar --dir <carpeta> --instrumento {calzan[0][1]}")
    elif not any(f[0] == "FALTA DATO" for f in filas):
        print("\nNingún instrumento calza hoy con los filtros duros. Mejor: financiar con ventas o preventas y volver a mirar en 3 meses.")
    print(f"\n{nota} Calzar con los filtros no es ganar: la evaluación pondera equipo, mercado e innovación.")


if __name__ == "__main__":
    main()
