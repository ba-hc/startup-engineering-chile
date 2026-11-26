#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Revisa el presupuesto de una postulación CORFO/ANID/Sercotec antes de subirla (registros/rendiciones.csv).

  presupuesto_corfo.py revisar --dir RUTA [--instrumento semilla_inicia] [--inicio AAAA-MM-DD] [--fin AAAA-MM-DD]
                               [--recupera-iva si|no|auto] [--tope-rrhh 0.5] [--tope-admin 0.1] [--mujeres]
  presupuesto_corfo.py tabla   --dir RUTA [--instrumento X] [--xlsx salida.xlsx]   # cuadro por cuenta para el formulario

Revisa, gasto por gasto y en total:
  - cofinanciamiento y tope del instrumento (con la variante para empresas lideradas por mujeres);
  - aporte pecuniario vs valorado (y mínimo pecuniario cuando la regla existe, p. ej. ANID 15%);
  - IVA incluido en una empresa que lo recupera como crédito fiscal (no financiable);
  - gastos con fecha anterior al inicio o posterior al término, ya pagados o comprometidos antes de postular;
  - duración contra el plazo de ejecución del instrumento;
  - concentración en RR.HH. y honorarios a socios o fundadores pagados con subsidio;
  - partidas que suelen ser no financiables (vehículos, inmuebles, deudas, gasto previo...).

Sin --instrumento, --inicio, --fin ni --recupera-iva, los lee de expediente/00_estado.md (objetivo, «Proyecto
postulado» y «Situación societaria»). Los montos van en CLP. Reglas en assets/fondos/instrumentos.json: es una
revisión previa, no una certificación de admisibilidad; manda la base del llamado vigente. Código de salida 1 si hay
PROBLEMA. No modifica el CSV: el fundador decide qué corregir.
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.fondos import clp, condiciones, fecha, instrumento, perfil_desde_estado, reglas, revisar_presupuesto  # noqa: E402
from core.storage import leer_estado  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SIMBOLO = {"OK": "✅", "PROBLEMA": "❌", "AVISO": "⚠", "VERIFICAR": "🔎"}


def filas(a):
    path = a.csv or os.path.join(os.path.abspath(a.dir), "expediente", "registros", "rendiciones.csv")
    if not os.path.exists(path):
        sys.exit(f"No encontré {path}. Registra el presupuesto con: expediente.py add rendiciones actividad=… presupuesto_CLP=…")
    with open(path, encoding="utf-8-sig", newline="") as fh:
        out = [r for r in csv.DictReader(fh) if any((v or "").strip() for v in r.values())]
    if not out:
        sys.exit("rendiciones.csv no tiene filas.")
    return out


def contexto(a):
    perfil = perfil_desde_estado(leer_estado(a.dir)) if a.dir else {}
    clave = a.instrumento or perfil.get("instrumento")
    if not clave:
        r, _ = reglas()
        sys.exit("No sé a qué instrumento postula: usa --instrumento (" + ", ".join(r["instrumentos"]) + ").")
    inicio = fecha(a.inicio) if a.inicio else perfil.get("inicio")
    fin = fecha(a.fin) if a.fin else perfil.get("fin")
    if a.recupera_iva == "auto":
        recupera = perfil.get("recupera_iva", perfil.get("tipo") == "juridica")
        origen = "00_estado.md" if "recupera_iva" in perfil else ("supuesto: persona jurídica" if recupera else "supuesto: no recupera")
    else:
        recupera, origen = a.recupera_iva == "si", "--recupera-iva"
    mujeres = a.mujeres or perfil.get("mujeres", False)
    return clave, inicio, fin, recupera, origen, mujeres


def cuadro(tot, por_cuenta):
    print("| Cuenta | Total | Subsidio | Aporte pecuniario | Aporte valorado | % del total |\n|---|---|---|---|---|---|")
    for c, v in sorted(por_cuenta.items(), key=lambda x: -x[1]["total"]):
        print(f"| {c} | {clp(v['total'])} | {clp(v['subsidio'])} | {clp(v['pecuniario'])} | {clp(v['valorado'])} | "
              f"{v['total'] / tot['presupuesto'] * 100:.0f}% |")
    print(f"| **Total** | **{clp(tot['presupuesto'])}** | {clp(tot['subsidio'])} | {clp(tot['pecuniario'])} | {clp(tot['valorado'])} | 100% |\n")


def cmd_revisar(a):
    r, nota = reglas()
    clave, inicio, fin, recupera, origen, mujeres = contexto(a)
    inst = instrumento(r, clave)
    fs = filas(a)
    res, tot, por_cuenta = revisar_presupuesto(fs, inst, inicio, fin, recupera, a.tope_rrhh, a.tope_admin, mujeres)
    tope, cof = condiciones(inst, mujeres)
    print(f"## Presupuesto vs {inst['nombre']}" + (" (variante mujeres)" if mujeres and inst.get("variante_mujeres") else ""))
    print(f"Período: {inicio or '[sin --inicio]'} a {fin or '[sin --fin]'} · IVA recuperable: {'sí' if recupera else 'no'} ({origen}) · "
          f"tope {clp(tope) if tope else 'según bases'} · cofinanciamiento máx. {f'{cof * 100:.0f}%' if cof else 'según bases'}\n")
    cuadro(tot, por_cuenta)
    if not inicio:
        res.append(("VERIFICAR", "sin fecha de inicio del proyecto: no pude revisar gastos previos (pasa --inicio)"))
    orden = {"PROBLEMA": 0, "AVISO": 1, "VERIFICAR": 2, "OK": 3}
    for est, txt in sorted(res, key=lambda x: orden.get(x[0], 9)):
        print(f"{SIMBOLO.get(est, '·')} {est}: {txt}")
    n = sum(1 for e, _ in res if e == "PROBLEMA")
    print(f"\n{n} problema(s), {sum(1 for e, _ in res if e == 'AVISO')} aviso(s). {nota}")
    if n:
        print("No «pulas» un presupuesto con problemas: corrige montos, fechas o partidas antes de subirlo.")
    sys.exit(1 if n else 0)


def cmd_tabla(a):
    r, _ = reglas()
    clave, inicio, fin, recupera, _, mujeres = contexto(a)
    inst = instrumento(r, clave)
    _, tot, por_cuenta = revisar_presupuesto(filas(a), inst, inicio, fin, recupera, mujeres=mujeres)
    print(f"## Cuadro de presupuesto — {inst['nombre']}\n")
    cuadro(tot, por_cuenta)
    if a.xlsx:
        from core.exporters import escribir_xlsx
        cab = ["Cuenta", "Total CLP", "Subsidio CLP", "Aporte pecuniario CLP", "Aporte valorado CLP", "% del total"]
        rows = [[c, round(v["total"]), round(v["subsidio"]), round(v["pecuniario"]), round(v["valorado"]),
                 f"{v['total'] / tot['presupuesto'] * 100:.0f}%"] for c, v in sorted(por_cuenta.items(), key=lambda x: -x[1]["total"])]
        rows.append(["Total", round(tot["presupuesto"]), round(tot["subsidio"]), round(tot["pecuniario"]), round(tot["valorado"]), "100%"])
        escribir_xlsx(a.xlsx, [("Presupuesto", cab, rows)])
        print(f"Creado {a.xlsx}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    for nombre, fn in (("revisar", cmd_revisar), ("tabla", cmd_tabla)):
        p = sp.add_parser(nombre)
        p.add_argument("--dir", default=".")
        p.add_argument("--csv", help="otro rendiciones.csv (por defecto, el del expediente)")
        p.add_argument("--instrumento")
        p.add_argument("--inicio")
        p.add_argument("--fin")
        p.add_argument("--recupera-iva", choices=["si", "no", "auto"], default="auto")
        p.add_argument("--mujeres", action="store_true", help="aplica la variante para empresas lideradas por mujeres")
        if nombre == "revisar":
            p.add_argument("--tope-rrhh", type=float, help="tope de RR.HH. del llamado como fracción (0.5 = 50%%)")
            p.add_argument("--tope-admin", type=float, help="tope de administración del llamado como fracción")
        else:
            p.add_argument("--xlsx")
        p.set_defaults(f=fn)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
