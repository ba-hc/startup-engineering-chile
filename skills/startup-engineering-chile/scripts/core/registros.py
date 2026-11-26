"""Registros del expediente: crear, leer (con compatibilidad de nombres antiguos), agregar filas y migrar el esquema."""
import datetime as dt
import json
import os
import re
import shutil
import sys

from .schemas import (BITACORA, LEGADO, OBLIGATORIOS, PREFIJOS, PREFIJOS_BITACORA, REFERENCIAS, TIPO_A_LEGADO, DECISIONES_VALIDAS,
                      buscar_pii, datos_json, esquema, registros_disponibles, validar_valor)
from .storage import (exp_dir, bloqueo, csv_texto, escribir_atomico, escribir_manifest, leer_manifest,
                      leer_seguro, reg_path, tiene_bom)
from .config import SCHEMA_VERSION

GITIGNORE_EXPEDIENTE = """# El expediente puede contener entrevistas, precios de clientes y datos personales.
# Por defecto no se sube a git. Si lo quieres versionar en un repositorio PRIVADO, borra este archivo.
*
!.gitignore
"""


def asegurar_registro(base, reg):
    """Crea el registro desde el esquema del pack si aún no existe (o si quedó vacío)."""
    reg = reg.replace(".csv", "")
    dst = reg_path(base, reg)
    if not os.path.exists(dst) or os.path.getsize(dst) == 0:
        cols = esquema(reg)
        if cols is None:
            sys.exit(f"Registro desconocido '{reg}'. Disponibles: {', '.join(registros_disponibles())} "
                     f"(y los antiguos {', '.join(sorted(LEGADO))}, que van a la bitácora)")
        escribir_atomico(dst, csv_texto(cols, []), bom=True)
    return dst


def _filas_crudas(base, reg):
    p = reg_path(base, reg)
    if not os.path.exists(p):
        return [], []
    h, rows, err = leer_seguro(p)
    if err:
        return [], []
    return h, [dict(zip(h, r + [""] * (len(h) - len(r)))) for r in rows]


def bitacora_a_legado(fila, reg):
    """Reconstruye una fila de un registro antiguo (p. ej. riesgos) desde una entrada de bitácora."""
    _, cols, mapa = LEGADO[reg]
    extra, _ = datos_json(fila.get("datos", ""))
    inv = {v: k for k, v in mapa.items()}
    d = {}
    for c in cols:
        if c in mapa:
            d[c] = fila.get(mapa[c], "")
        else:
            d[c] = extra.get(c, "")
    for c, v in extra.items():
        d.setdefault(c, v)
    for bc, c in inv.items():
        if not d.get(c):
            d[c] = fila.get(bc, "")
    d["_entrada_id"] = fila.get("entrada_id", "")
    return d


def filas(base, reg):
    """Filas de un registro como lista de dicts. Para nombres antiguos lee la bitácora (y el CSV antiguo si aún existe)."""
    reg = reg.replace(".csv", "")
    if reg in LEGADO:
        tipo = LEGADO[reg][0]
        _, viejas = _filas_crudas(base, reg)
        _, bit = _filas_crudas(base, BITACORA)
        return viejas + [bitacora_a_legado(f, reg) for f in bit if f.get("tipo", "").lower() == tipo]
    return _filas_crudas(base, reg)[1]


def bitacora(base, tipo=None):
    _, bit = _filas_crudas(base, BITACORA)
    return [f for f in bit if tipo is None or f.get("tipo", "").lower() == tipo]


def ids_de(base, reg):
    return {list(d.values())[0].strip() for d in filas(base, reg) if d and list(d.values())[0].strip()}


def siguiente_id(base, reg, tipo=None):
    reg = reg.replace(".csv", "")
    if reg in LEGADO:
        tipo, reg = LEGADO[reg][0], BITACORA
    if reg == BITACORA:
        pref = PREFIJOS_BITACORA.get((tipo or "nota").lower(), "BIT")
        existentes = [f.get("entrada_id", "") for f in bitacora(base)]
    else:
        pref = PREFIJOS.get(reg, reg[:3].upper())
        h, rows = _filas_crudas(base, reg)
        existentes = [list(r.values())[0] if r else "" for r in rows]
    mx = 0
    for rid in existentes:
        m = re.fullmatch(re.escape(pref) + r"-(\d+)", (rid or "").strip())
        if m:
            mx = max(mx, int(m.group(1)))
    return f"{pref}-{mx + 1:03d}"


def _a_bitacora(reg, valores):
    """Convierte campos de un registro antiguo en una entrada de bitácora."""
    tipo, cols, mapa = LEGADO[reg]
    fila = {"tipo": tipo}
    extra = {}
    for k, v in valores.items():
        if k in mapa:
            fila[mapa[k]] = v
        elif v != "":
            extra[k] = v
    if extra:
        fila["datos"] = json.dumps(extra, ensure_ascii=False, sort_keys=True)
    return fila


def agregar(base, reg, valores, confirmado=False, forzar=False, avisar=print):
    """Agrega una fila validada. Devuelve el ID asignado. Sale con mensaje claro si algo no cuadra."""
    reg = reg.replace(".csv", "")
    legado = reg if reg in LEGADO else None
    if legado:
        cols_legado = LEGADO[reg][1]
        malos = [k for k in valores if k not in cols_legado]
        if malos:
            sys.exit(f"Campo(s) {', '.join(malos)} no existen en {reg}. Columnas: {', '.join(cols_legado)}")
        valores = _a_bitacora(reg, valores)
        reg = BITACORA
    with bloqueo(base):
        path = asegurar_registro(base, reg)
        header, rows, err = leer_seguro(path)
        if err:
            sys.exit(f"No pude leer {path} ({err}). Corre `expediente.py validar` y repáralo antes de agregar filas.")
        if reg == BITACORA:
            extra = {k: v for k, v in valores.items() if k not in header}
            if extra:
                previos, e_ = datos_json(valores.get("datos", ""))
                if e_:
                    sys.exit(f"bitacora: {e_}")
                previos.update(extra)
                valores = {k: v for k, v in valores.items() if k in header}
                valores["datos"] = json.dumps(previos, ensure_ascii=False, sort_keys=True)
            valores["tipo"] = (valores.get("tipo") or "nota").lower()
        for k in valores:
            if k not in header:
                sys.exit(f"Campo '{k}' no existe en {reg}. Columnas: {', '.join(header)}")
        faltan = [c for c in OBLIGATORIOS.get(reg, []) if c in header and not valores.get(c)]
        if faltan and not forzar:
            sys.exit(f"Faltan campos obligatorios en {legado or reg}: {', '.join(faltan)}. "
                     "Complétalos (o usa --forzar si de verdad no aplica).")
        for col in header:
            e_, a_ = validar_valor(reg, col, valores.get(col, ""))
            if e_:
                sys.exit(e_ + ".")
            if a_:
                avisar("AVISO: " + a_, file=sys.stderr)
        if reg == "decisiones" and valores.get("decision") and valores["decision"].lower() not in DECISIONES_VALIDAS:
            sys.exit(f"decision='{valores['decision']}' no es válida. Usa Go, Hold, Recycle, Kill o no aplica.")
        if reg == BITACORA and valores.get("datos"):
            _, e_ = datos_json(valores["datos"])
            if e_:
                sys.exit(f"bitacora: {e_}")
        idcol = header[0]
        if not valores.get(idcol) and (idcol.endswith("id") or reg == BITACORA):
            valores[idcol] = siguiente_id(base, reg, valores.get("tipo"))
        if valores.get(idcol) and valores[idcol] in {r[0] for r in rows if r}:
            sys.exit(f"{idcol}={valores[idcol]} ya existe en {reg}.")
        hoy = dt.date.today().isoformat()
        for col in ("fecha", "fecha_consulta"):
            if col in header and not valores.get(col):
                valores[col] = hoy
        if "estado" in header and not valores.get("estado"):
            valores["estado"] = "confirmado" if confirmado else "propuesta-agente"
        fila = [valores.get(c, "") for c in header]
        escribir_atomico(path, csv_texto(header, rows + [fila]), bom=tiene_bom(path))
    for col, v in valores.items():
        destino = REFERENCIAS.get(col)
        if not destino or col == idcol or not v:
            continue
        existentes = ids_de(base, destino)
        for ref in re.split(r"[;,\s]+", v):
            if re.fullmatch(r"[A-Z]+-\d+", ref) and ref not in existentes:
                avisar(f"AVISO: {col}={ref} no existe en {destino}.csv "
                       f"(IDs actuales: {', '.join(sorted(existentes)) or 'ninguno'})", file=sys.stderr)
    pii = buscar_pii(list(valores.values()))
    if pii:
        avisar(f"AVISO privacidad: la fila parece contener {', '.join(pii)}. Anonimiza (ENT-00X, rol) "
               "o usa ingestar.py antes de guardar notas.", file=sys.stderr)
    return valores.get(idcol, "")


def migrar(base, avisar=print):
    """Lleva el expediente al esquema vigente. Devuelve el número de cambios.

    v1/v2 → v3: agrega columnas faltantes a los registros (con respaldo .bak), pasa los 8 registros secundarios
    a bitacora.csv conservando sus IDs y crea el .gitignore de privacidad.
    """
    e = exp_dir(base)
    rdir = os.path.join(e, "registros")
    os.makedirs(rdir, exist_ok=True)
    cambios = 0
    hoy = dt.date.today().isoformat()
    with bloqueo(base):
        for f in sorted(os.listdir(rdir)):
            if not f.endswith(".csv"):
                continue
            reg, path = f[:-4], os.path.join(rdir, f)
            esq = esquema(reg)
            if esq is None:
                continue
            if os.path.getsize(path) == 0:
                escribir_atomico(path, csv_texto(esq, []), bom=True)
                avisar(f"{reg}: encabezado restaurado")
                cambios += 1
                continue
            h, rows, err = leer_seguro(path)
            if err:
                avisar(f"{reg}: no se pudo leer ({err}); no se tocó. Revisa la codificación a mano.")
                continue
            faltan = [c for c in esq if c not in h]
            if not faltan:
                continue
            shutil.copy2(path, path + f".bak-{hoy}")
            nuevo_h = esq + [c for c in h if c not in esq]
            nuevas = []
            for r in rows:
                d = dict(zip(h, r + [""] * (len(h) - len(r))))
                nuevas.append([d.get(c, "") for c in nuevo_h])
            escribir_atomico(path, csv_texto(nuevo_h, nuevas), bom=True)
            avisar(f"{reg}: agregadas columnas {', '.join(faltan)} (respaldo .bak)")
            cambios += 1
        # registros antiguos → bitácora
        antiguos = [r for r in sorted(LEGADO) if os.path.exists(reg_path(base, r))]
        if antiguos:
            bpath = reg_path(base, BITACORA)
            if not os.path.exists(bpath) or os.path.getsize(bpath) == 0:
                escribir_atomico(bpath, csv_texto(esquema(BITACORA), []), bom=True)
            bh, brows, err = leer_seguro(bpath)
            if err:
                avisar(f"bitacora: no se pudo leer ({err}); no se migraron {', '.join(antiguos)}.")
                antiguos = []
            usados = {r[0] for r in brows if r}
            for reg in antiguos:
                path = reg_path(base, reg)
                h, rows, err = leer_seguro(path)
                if err:
                    avisar(f"{reg}: no se pudo leer ({err}); quedó como estaba.")
                    continue
                tipo, cols, mapa = LEGADO[reg]
                n = 0
                for r in rows:
                    d = dict(zip(h, r + [""] * (len(h) - len(r))))
                    entrada = _a_bitacora(reg, {k: v for k, v in d.items() if k in cols or v})
                    rid = entrada.get("entrada_id", "").strip()
                    if not rid or rid in usados:
                        pref = PREFIJOS_BITACORA[tipo]
                        mx = max([int(m.group(1)) for m in (re.fullmatch(re.escape(pref) + r"-(\d+)", u) for u in usados) if m] + [0])
                        rid = f"{pref}-{mx + 1:03d}"
                    entrada["entrada_id"] = rid
                    usados.add(rid)
                    brows.append([entrada.get(c, "") for c in bh])
                    n += 1
                shutil.move(path, path + f".bak-{hoy}")
                avisar(f"{reg}: {n} fila(s) pasadas a bitacora.csv (tipo {tipo}); original en {os.path.basename(path)}.bak-{hoy}")
                cambios += 1
            escribir_atomico(bpath, csv_texto(bh, brows), bom=True)
        gi = os.path.join(e, ".gitignore")
        if not os.path.exists(gi):
            escribir_atomico(gi, GITIGNORE_EXPEDIENTE)
            avisar("Agregado expediente/.gitignore (privacidad)")
            cambios += 1
        antes = (leer_manifest(base) or {}).get("schema_version", 1)
        escribir_manifest(base)
    avisar(f"Esquema v{antes} → v{SCHEMA_VERSION}. {cambios} cambio(s).")
    return cambios


def nombre_legible(reg):
    return f"{reg} (en bitácora, tipo {LEGADO[reg][0]})" if reg in LEGADO else reg


__all__ = ["GITIGNORE_EXPEDIENTE", "asegurar_registro", "filas", "bitacora", "bitacora_a_legado", "ids_de", "siguiente_id",
           "agregar", "migrar", "TIPO_A_LEGADO", "nombre_legible"]
