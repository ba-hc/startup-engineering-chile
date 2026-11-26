#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Cap table simple del expediente (expediente/documentos/cap_table.csv), con vesting, SAFE y simulación de ronda.

  cap_table.py init    --dir RUTA --fundadores "Ana:60,Beto:40" [--acciones 10000000] [--pool 10]
                       [--vesting 48 --cliff 12 --inicio-vesting AAAA-MM-DD]
  cap_table.py emitir  --dir RUTA --titular "Ángel 1" --acciones 250000 [--clase comun|preferente|pool] [--monto CLP]
  cap_table.py safe    --dir RUTA --titular "Fondo X" --monto 50000000 [--cap 1500000000] [--descuento 20]
  cap_table.py ver     --dir RUTA [--fecha AAAA-MM-DD]      # % emitido y fully diluted, acciones consolidadas (vesting)
  cap_table.py ronda   --dir RUTA --pre 2000000000 --inversion 500000000 [--pool-post 10]
                       # convierte los SAFE y muestra la tabla post-ronda (misma lógica que finanzas.py dilucion)
  cap_table.py exportar --dir RUTA [--xlsx]                 # CSV ';' para Excel o .xlsx en entregables/

La tabla es una vista de trabajo para conversar con socios e inversionistas: el registro de accionistas legal
de la SpA, el pacto y los contratos mandan. Plantillas: TPL-034 (acuerdo de socios), TPL-091 (cap table),
TPL-109 (SAFE y term sheet). Orientación educativa, no asesoría legal.
"""
import argparse
import datetime as dt
import io
import os
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.storage import csv_texto, escribir_atomico, exp_dir, leer, requiere_expediente  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

COLS = ["titular", "clase", "acciones", "monto_CLP", "cap_CLP", "descuento_pct", "fecha", "vesting_meses", "cliff_meses",
        "inicio_vesting", "nota"]
CLASES = ("comun", "preferente", "pool", "safe")


def ruta(base):
    return os.path.join(exp_dir(base), "documentos", "cap_table.csv")


def cargar(base):
    p = ruta(base)
    if not os.path.exists(p):
        sys.exit(f"No hay cap table en {p}. Créala con: cap_table.py init --dir {base} --fundadores \"Ana:60,Beto:40\"")
    h, rows = leer(p)
    return [dict(zip(h, r + [""] * (len(h) - len(r)))) for r in rows]


def guardar(base, filas):
    escribir_atomico(ruta(base), csv_texto(COLS, [[f.get(c, "") for c in COLS] for f in filas]), bom=True)


def n(v):
    try:
        return float(str(v).replace(".", "").replace(",", ".")) if v not in ("", None) else 0.0
    except ValueError:
        return 0.0


def miles(x):
    return f"{x:,.0f}".replace(",", ".")


def pct(x):
    return f"{x * 100:.1f}%".replace(".", ",")


def consolidadas(f, hoy):
    """Acciones consolidadas (vested) a la fecha según vesting y cliff."""
    acc, vest, cliff = n(f["acciones"]), int(n(f.get("vesting_meses"))), int(n(f.get("cliff_meses")))
    if not vest or f.get("clase") != "comun":
        return acc
    try:
        ini = dt.date.fromisoformat(f.get("inicio_vesting", "")[:10])
    except ValueError:
        return acc
    meses = (hoy.year - ini.year) * 12 + hoy.month - ini.month - (1 if hoy.day < ini.day else 0)
    if meses < cliff:
        return 0.0
    return acc * min(1.0, meses / vest)


def cmd_init(a):
    requiere_expediente(a.dir)
    if os.path.exists(ruta(a.dir)) and not a.forzar:
        sys.exit(f"Ya existe {ruta(a.dir)} (usa --forzar para reemplazarla).")
    pares = []
    for parte in a.fundadores.split(","):
        nombre, _, v = parte.partition(":")
        pares.append((nombre.strip(), float(v)))
    total = sum(v for _, v in pares)
    hoy = dt.date.today().isoformat()
    emitidas = a.acciones * (1 - a.pool / 100)
    filas = [{"titular": nom, "clase": "comun", "acciones": f"{emitidas * v / total:.0f}", "fecha": hoy,
              "vesting_meses": str(a.vesting or ""), "cliff_meses": str(a.cliff or ""),
              "inicio_vesting": a.inicio_vesting or (hoy if a.vesting else ""), "nota": "fundador/a"} for nom, v in pares]
    if a.pool:
        filas.append({"titular": "Pool de opciones (sin asignar)", "clase": "pool", "acciones": f"{a.acciones * a.pool / 100:.0f}",
                      "fecha": hoy, "nota": "reservado para equipo"})
    guardar(a.dir, filas)
    print(f"Creado {ruta(a.dir)}")
    if not a.vesting:
        print("Aviso: fundadores sin vesting. Sin vesting ni cliff, un socio que se va a los 3 meses se queda con todo su porcentaje "
              "(ver TPL-034).")
    cmd_ver(a)


def cmd_emitir(a):
    filas = cargar(a.dir)
    filas.append({"titular": a.titular, "clase": a.clase, "acciones": f"{a.acciones:.0f}", "monto_CLP": f"{a.monto or ''}",
                  "fecha": dt.date.today().isoformat(), "nota": a.nota or ""})
    guardar(a.dir, filas)
    cmd_ver(a)


def cmd_safe(a):
    filas = cargar(a.dir)
    filas.append({"titular": a.titular, "clase": "safe", "acciones": "0", "monto_CLP": f"{a.monto:.0f}",
                  "cap_CLP": f"{a.cap:.0f}" if a.cap else "", "descuento_pct": f"{a.descuento:g}" if a.descuento else "",
                  "fecha": dt.date.today().isoformat(), "nota": "SAFE post-money: convierte en la próxima ronda con precio"})
    guardar(a.dir, filas)
    print(f"SAFE registrado: {a.titular} por ${miles(a.monto)}" + (f", cap ${miles(a.cap)}" if a.cap else ", sin cap")
          + (f", descuento {a.descuento:g}%" if a.descuento else "") + ". Simula su conversión con `cap_table.py ronda`.")


def cmd_ver(a):
    filas = cargar(a.dir)
    hoy = dt.date.fromisoformat(a.fecha) if getattr(a, "fecha", None) else dt.date.today()
    acc = [f for f in filas if f["clase"] != "safe"]
    emitidas = sum(n(f["acciones"]) for f in acc if f["clase"] != "pool")
    fd = sum(n(f["acciones"]) for f in acc)
    print(f"### Cap table al {hoy.isoformat()}\n| Titular | Clase | Acciones | % emitido | % fully diluted | Consolidadas (vesting) |")
    print("|---|---|---|---|---|---|")
    for f in acc:
        v = n(f["acciones"])
        emi = pct(v / emitidas) if f["clase"] != "pool" and emitidas else "—"
        print(f"| {f['titular']} | {f['clase']} | {miles(v)} | {emi} | {pct(v / fd) if fd else '—'} | {miles(consolidadas(f, hoy))} |")
    print(f"| **Total** | | **{miles(fd)}** | | 100% | |")
    safes = [f for f in filas if f["clase"] == "safe"]
    if safes:
        tot = sum(n(f["monto_CLP"]) for f in safes)
        print(f"\nSAFE pendientes de conversión: {len(safes)} por ${miles(tot)} en total (no son acciones todavía; "
              "con cap post-money, cada uno ≈ monto / cap del post-money).")
        for f in safes:
            if n(f["cap_CLP"]):
                print(f"- {f['titular']}: ${miles(n(f['monto_CLP']))} / cap ${miles(n(f['cap_CLP']))} ≈ {pct(n(f['monto_CLP']) / n(f['cap_CLP']))} post-money")
            else:
                print(f"- {f['titular']}: ${miles(n(f['monto_CLP']))} sin cap: su % depende del precio de la ronda")
    print("\nVista de trabajo: el registro de accionistas de la SpA y el pacto mandan.")


def cmd_ronda(a):
    import finanzas
    filas = cargar(a.dir)
    comunes = [f for f in filas if f["clase"] in ("comun", "preferente")]
    pool = sum(n(f["acciones"]) for f in filas if f["clase"] == "pool")
    tot = sum(n(f["acciones"]) for f in comunes) + pool
    if not comunes:
        sys.exit("La cap table no tiene accionistas.")
    args = ["dilucion", "--fundadores", ",".join(f"{f['titular'].replace(',', ' ').replace(':', ' ')}:{n(f['acciones']):.0f}" for f in comunes),
            "--pool", f"{100 * pool / tot:.6f}", "--pre", str(a.pre), "--inversion", str(a.inversion), "--pool-post", str(a.pool_post)]
    for f in filas:
        if f["clase"] == "safe":
            args += ["--safe", f"{n(f['monto_CLP']):.0f}:{n(f['cap_CLP']):.0f}:{n(f['descuento_pct']):g}"]
    buf = io.StringIO()
    with redirect_stdout(buf):
        finanzas.main(args)
    print(buf.getvalue().replace("Antes de convertir instrumentos", "Hoy (cap table del expediente)"))
    print("Simulación: no modifica cap_table.csv. Registra la ronda con `emitir` cuando se firme.")


def cmd_exportar(a):
    filas = cargar(a.dir)
    out = os.path.join(exp_dir(a.dir), "entregables")
    if a.xlsx:
        from core.exporters import escribir_xlsx
        dst = os.path.join(out, "cap_table.xlsx")
        escribir_xlsx(dst, [("Cap table", COLS, [[f.get(c, "") for c in COLS] for f in filas])])
    else:
        dst = os.path.join(out, "cap_table.csv")
        escribir_atomico(dst, csv_texto(COLS, [[f.get(c, "") for c in COLS] for f in filas], delimiter=";"), bom=True)
    print(f"Creado {dst}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("--dir", default="."); p.add_argument("--fundadores", required=True)
    p.add_argument("--acciones", type=float, default=10_000_000); p.add_argument("--pool", type=float, default=0)
    p.add_argument("--vesting", type=int); p.add_argument("--cliff", type=int); p.add_argument("--inicio-vesting")
    p.add_argument("--forzar", action="store_true"); p.set_defaults(f=cmd_init)
    p = sp.add_parser("emitir"); p.add_argument("--dir", default="."); p.add_argument("--titular", required=True)
    p.add_argument("--acciones", type=float, required=True); p.add_argument("--clase", default="comun", choices=["comun", "preferente", "pool"])
    p.add_argument("--monto", type=float); p.add_argument("--nota"); p.set_defaults(f=cmd_emitir)
    p = sp.add_parser("safe"); p.add_argument("--dir", default="."); p.add_argument("--titular", required=True)
    p.add_argument("--monto", type=float, required=True); p.add_argument("--cap", type=float); p.add_argument("--descuento", type=float)
    p.set_defaults(f=cmd_safe)
    p = sp.add_parser("ver"); p.add_argument("--dir", default="."); p.add_argument("--fecha"); p.set_defaults(f=cmd_ver)
    p = sp.add_parser("ronda"); p.add_argument("--dir", default="."); p.add_argument("--pre", type=float, required=True)
    p.add_argument("--inversion", type=float, required=True); p.add_argument("--pool-post", type=float, default=0)
    p.set_defaults(f=cmd_ronda)
    p = sp.add_parser("exportar"); p.add_argument("--dir", default="."); p.add_argument("--xlsx", action="store_true")
    p.set_defaults(f=cmd_exportar)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
