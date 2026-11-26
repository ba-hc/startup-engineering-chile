"""Vistas generadas desde el expediente: informes Markdown, Excel (.xlsx), HTML (dashboard) y ZIP (empaquetar/restaurar).

La presentación no crea evidencia: lo que no está registrado se marca [SIN RESPALDO] o [FALTA EVIDENCIA].
"""
import datetime as dt
import html
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

from .config import GATES, SCHEMA_VERSION
from .estado import acciones, gate_actual_de, hipotesis_estancadas, mision, numeros_clave
from .gates import evaluar_gate, progreso
from .registros import filas
from .schemas import BITACORA, LEGADO, es_numero, fecha_iso, registros_disponibles, validar
from .storage import (csv_texto, escribir_atomico, escribir_bytes_atomico, escribir_manifest, exp_dir, leer_estado, leer_manifest,
                      leer_seguro, nombre_proyecto, seccion)
from .plantillas import slug

SIN = "[SIN RESPALDO]"
FALTA = "[FALTA EVIDENCIA]"


# ---------------------------------------------------------------- Markdown
def informe_semanal(base, dias=7):
    hoy = dt.date.today()
    txt = leer_estado(base)
    desde = hoy - dt.timedelta(days=dias)
    out = [f"# Reporte semanal — {nombre_proyecto(base)}\n\n{desde.isoformat()} a {hoy.isoformat()} · generado desde el expediente\n"]
    foco = seccion(txt, "Foco actual")
    if foco:
        out.append("## Foco\n" + foco + "\n")
    mi = mision(txt, hoy)
    if mi:
        out.append(f"## Misión de 7 días\n- {mi['mision']} (vence {mi['vence'] or '?'}; {mi['estado'] or 'abierta'})"
                   + (" — **vencida**" if mi["vencida"] else "") + "\n")
    por = {}
    for reg in registros_disponibles():
        for d in filas(base, reg):
            f = d.get("fecha") or d.get("fecha_consulta") or d.get("inicio") or ""
            if fecha_iso(f) and dt.date.fromisoformat(f[:10]) >= desde:
                clave = f"{reg} ({d.get('tipo')})" if reg == BITACORA else reg
                por[clave] = por.get(clave, 0) + 1
    out.append("## Avance de la semana")
    out.append((", ".join(f"{k}: +{v}" for k, v in sorted(por.items())) if por else "Sin registros nuevos esta semana.") + "\n")
    ents, pipe, pils = filas(base, "entrevistas"), filas(base, "cuentas_y_pipeline"), filas(base, "pilotos")
    out.append("## Embudo\n| Entrevistas | Cuentas en pipeline | Pilotos |\n|---|---|---|\n"
               f"| {len(ents)} | {len(pipe)} | {len(pils)} |\n")
    dec = [d for d in filas(base, "decisiones") if fecha_iso(d.get("fecha", "")) and d["fecha"][:10] >= desde.isoformat()]
    if dec:
        out.append("## Decisiones\n" + "\n".join(f"- {d.get('gate')}: **{d.get('decision')}** — {d.get('justificacion', '')[:140]}" for d in dec) + "\n")
    pend, venc = acciones(txt, hoy)
    est = hipotesis_estancadas(base, hoy)
    riesgos = [d for d in filas(base, "riesgos") if d.get("estado", "").lower() not in ("cerrado", "mitigado")]
    out.append("## Semáforo")
    out.append(f"- {'🔴' if venc else '🟢'} Acciones vencidas: {len(venc)}")
    out.append(f"- {'🟡' if est else '🟢'} Hipótesis estancadas (>14 días): {len(est)}")
    out.append(f"- {'🟡' if riesgos else '🟢'} Riesgos abiertos: {len(riesgos)}")
    kpis = filas(base, "indicadores")
    if kpis:
        out.append("\n## Indicadores\n| KPI | Línea base | Meta |\n|---|---|---|")
        out += [f"| {k.get('nombre')} | {k.get('baseline')} | {k.get('meta')} |" for k in kpis]
    out.append("\n## Próxima semana")
    out += [f"- {acc} · {resp} · {f}" for acc, resp, f in (venc + pend)[:6]] or ["- (sin acciones registradas)"]
    return f"reporte_semanal_{hoy.isoformat()}.md", "\n".join(out) + "\n"


def onepager(base):
    hoy = dt.date.today()
    txt = leer_estado(base)
    perfil = seccion(txt, "Perfil")
    frase = re.search(r"Una frase[^:]*:\*\*\s*(.+)", perfil)
    out = [f"# {nombre_proyecto(base)} — one-pager\n\n> Borrador generado desde el expediente el {hoy.isoformat()}. "
           f"Lo marcado {SIN} no tiene evidencia registrada: respáldalo o quítalo antes de compartir.\n"]
    out.append("## Problema\n" + (frase.group(1).strip() if frase and "[segmento]" not in frase.group(1) else SIN) + "\n")
    evs = [d for d in filas(base, "evidencias") if d.get("estado") == "confirmado"]
    out.append("## Evidencia confirmada")
    out += [f"- {d.get('afirmacion')} ({d.get('tipo')}, n={d.get('n') or '?'}; {d.get('evidence_id')})" for d in evs[:8]] or [f"- {SIN} aún no hay evidencia confirmada"]
    comp = filas(base, "competencia")
    out.append("\n## Alternativas y competencia")
    out += [f"- {c.get('alternativa')} ({c.get('tipo')}): {c.get('limitacion')}" + (f" ({c['evidence_id']})" if c.get("evidence_id") else "")
            for c in comp[:5]] or [f"- {SIN} sin benchmark registrado"]
    ents, pils = filas(base, "entrevistas"), filas(base, "pilotos")
    out.append(f"\n## Tracción\n- Entrevistas registradas: {len(ents)}\n- Pilotos: {len(pils)}")
    kpis = filas(base, "indicadores")
    out += [f"- {k.get('nombre')}: {k.get('baseline')} (meta {k.get('meta')})" for k in kpis[:5]]
    dec = filas(base, "decisiones")
    out.append("\n## Dónde estamos")
    out += [f"- {d.get('gate')}: {d.get('decision')} — {d.get('justificacion', '')[:120]}" for d in dec[-3:]] or ["- Sin decisiones de gate registradas"]
    equipo = re.search(r"Equipo y dedicación:\*\*\s*(.*)", perfil)
    out.append("\n## Equipo\n" + ((equipo.group(1).strip() or SIN) if equipo else SIN))
    objetivo = re.search(r"Objetivo próximo y fecha límite:\*\*\s*(.*)", perfil)
    out.append("\n## Qué pedimos / próximo hito\n" + ((objetivo.group(1).strip() or "[completar]") if objetivo else "[completar]"))
    return f"one_pager_{hoy.isoformat()}.md", "\n".join(out) + "\n"


def deck_md(base):
    """Pitch deck en Markdown compatible con Marp, desde el expediente; marca vacíos con [FALTA EVIDENCIA]."""
    F = FALTA
    txt = leer_estado(base)
    perfil = seccion(txt, "Perfil")

    def campo(et):
        mm = re.search(re.escape(et) + r"[^:]*:\*\*\s*(.*)", perfil)
        v = (mm.group(1).strip() if mm else "")
        return F if not v or "[segmento]" in v else v
    evs = [d for d in filas(base, "evidencias") if d.get("estado") == "confirmado"]
    ents, comp, pils = filas(base, "entrevistas"), filas(base, "competencia"), filas(base, "pilotos")
    pipe, kpis = filas(base, "cuentas_y_pipeline"), filas(base, "indicadores")
    precio = ""
    for d in filas(base, "experimentos"):
        if re.search(r"precio|pago|preventa|carta", d.get("metrica", "") + d.get("metodo", ""), re.I) and d.get("resultado"):
            precio = f"{d.get('metrica')}: {d.get('resultado')} (umbral {d.get('umbral')}; {d.get('experiment_id')})"
    sup = supuestos_modelo(base)
    sl = ["---", "marp: true", "paginate: true", "---", "",
          f"# {nombre_proyecto(base)}", f"{campo('Una frase')}", "",
          "> Borrador generado desde el expediente el " + dt.date.today().isoformat() + ". Todo lo marcado " + F + " debe respaldarse o quitarse.",
          "", "---", "", "## El problema", campo("Una frase"), ""]
    sl += [f"- {d.get('afirmacion')} (n={d.get('n') or '?'}; {d.get('evidence_id')})" for d in evs[:3]] or [f"- {F} sin evidencia confirmada del problema"]
    sl += ["", "---", "", "## A quién le pasa", f"- Entrevistas registradas: {len(ents)}"]
    segs = sorted({d.get("segmento", "") for d in ents if d.get("segmento")})
    sl += [f"- Segmentos entrevistados: {', '.join(segs[:4])}" if segs else f"- {F} segmento del cliente"]
    sl += ["", "---", "", "## Cómo lo resuelven hoy"]
    sl += [f"- {c.get('alternativa')} ({c.get('tipo')}): {c.get('limitacion') or F}" for c in comp[:4]] or [f"- {F} alternativas y competencia"]
    sl += ["", "---", "", "## Nuestra propuesta", f"- {F} propuesta de valor con la diferencia demostrada (TPL-049, TPL-031)", "",
           "---", "", "## Modelo de negocio y precio", f"- {precio or F + ' prueba de precio con compromiso'}"]
    if sup.get("Precio mensual"):
        sl.append(f"- Precio supuesto en el modelo: {sup['Precio mensual']} CLP/mes (supuesto, no evidencia)")
    sl += ["", "---", "", "## Tracción", f"- Pilotos: {len(pils)} · Cuentas en pipeline: {len(pipe)}"]
    sl += [f"- {k.get('nombre')}: {k.get('baseline') or F} → meta {k.get('meta') or F}" for k in kpis[:3]] or [f"- {F} indicadores de uso o venta"]
    sl += ["", "---", "", "## Economía unitaria"]
    if sup:
        for et in ("CAC", "Churn mensual", "Infraestructura variable"):
            if et in sup:
                sl.append(f"- {et}: {sup[et]} (supuesto del modelo; respáldalo con `finanzas.py unit`)")
    else:
        sl.append(f"- {F} unit economics (`finanzas.py unit`)")
    sl += ["", "---", "", "## Equipo", f"- {campo('Equipo y dedicación')}", "", "---", "", "## Qué pedimos",
           f"- {campo('Objetivo próximo y fecha límite')}", f"- {F} monto, uso de fondos e hito que se alcanza", ""]
    return "\n".join(sl) + "\n"


def supuestos_modelo(base):
    """{variable: valor} de la hoja Supuestos del modelo del expediente ({} si no hay modelo o no se puede leer)."""
    modelo = os.path.join(exp_dir(base), "entregables", "modelo_financiero.xlsx")
    if not os.path.exists(modelo):
        return {}
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import modelo_xlsx
        return {s["variable"]: s["valor"] for s in modelo_xlsx.supuestos(modelo, "Supuestos")}
    except (Exception, SystemExit):
        return {}


# ---------------------------------------------------------------- CSV y Excel
def todas_las_tablas(base):
    """[(nombre, header, filas)] de los registros presentes; la bitácora se expande en una hoja por tipo."""
    rdir = os.path.join(exp_dir(base), "registros")
    out = []
    if not os.path.isdir(rdir):
        return out
    for f in sorted(os.listdir(rdir)):
        if not f.endswith(".csv"):
            continue
        reg = f[:-4]
        h, rows, err = leer_seguro(os.path.join(rdir, f))
        if err:
            continue
        if reg == BITACORA:
            for legado, (tipo, cols, _) in sorted(LEGADO.items()):
                fs = filas(base, legado)
                if fs:
                    out.append((legado, cols, [[d.get(c, "") for c in cols] for d in fs]))
            continue
        out.append((reg, h, rows))
    return out


def exportar_csv(base, destino, registro="todos"):
    tablas = todas_las_tablas(base)
    if registro != "todos":
        tablas = [t for t in tablas if t[0] == registro]
    for nombre, h, rows in tablas:
        escribir_atomico(os.path.join(destino, nombre + ".csv"), csv_texto(h, rows, delimiter=";"), bom=True)
    return [t[0] for t in tablas]


def _col(n):
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _celda(ref, v, encabezado=False):
    v = "" if v is None else str(v)
    estilo = ' s="1"' if encabezado else ""
    plano = v.strip().replace(" ", "")
    if not encabezado and plano and es_numero(plano) and not re.match(r"^0\d", plano) and "%" not in plano:
        num = plano.replace("$", "")
        if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", num):
            num = num.replace(".", "").replace(",", ".")
        else:
            num = num.replace(",", ".")
        try:
            float(num)
            return f'<c r="{ref}"><v>{num}</v></c>'
        except ValueError:
            pass
    return f'<c r="{ref}" t="inlineStr"{estilo}><is><t xml:space="preserve">{escape(v)}</t></is></c>'


def escribir_xlsx(path, hojas):
    """Escribe un .xlsx mínimo (sin dependencias): hojas = [(nombre, header, filas)]. Encabezado en negrita y fijado."""
    hojas = hojas or [("Vacio", ["(sin registros)"], [])]
    usados = set()
    nombres = []
    for nombre, _, _ in hojas:
        n = re.sub(r"[\[\]:*?/\\]", "_", nombre)[:31] or "Hoja"
        base_n, i = n, 2
        while n.lower() in usados:
            n = f"{base_n[:28]}_{i}"
            i += 1
        usados.add(n.lower())
        nombres.append(n)
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>']
    ct += [f'<Override PartName="/xl/worksheets/sheet{i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
           for i in range(len(hojas))]
    ct.append("</Types>")
    wb = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>']
    wb += [f'<sheet name="{escape(n)}" sheetId="{i + 1}" r:id="rId{i + 1}"/>' for i, n in enumerate(nombres)]
    wb.append("</sheets></workbook>")
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    rels += [f'<Relationship Id="rId{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
             f'Target="worksheets/sheet{i + 1}.xml"/>' for i in range(len(hojas))]
    rels.append(f'<Relationship Id="rId{len(hojas) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
    rels.append("</Relationships>")
    estilos = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
               '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
               '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
               '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
               '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
               '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
               '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>'
               '</styleSheet>')
    hojas_xml = []
    for nombre, header, rows in hojas:
        filas_xml = []
        for ri, fila in enumerate([header] + list(rows)):
            celdas = "".join(_celda(f"{_col(ci)}{ri + 1}", v, encabezado=(ri == 0)) for ci, v in enumerate(fila))
            filas_xml.append(f'<row r="{ri + 1}">{celdas}</row>')
        anchos = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{min(60, max(10, len(str(h)) + 4))}" customWidth="1"/>'
                         for i, h in enumerate(header))
        hojas_xml.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                         '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                         '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
                         '</sheetView></sheetViews>'
                         + (f"<cols>{anchos}</cols>" if header else "")
                         + f'<sheetData>{"".join(filas_xml)}</sheetData></worksheet>')
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(path)) or ".", suffix=".tmp")
    os.close(fd)
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", "".join(ct))
            z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
                       'Target="xl/workbook.xml"/></Relationships>')
            z.writestr("xl/workbook.xml", "".join(wb))
            z.writestr("xl/_rels/workbook.xml.rels", "".join(rels))
            z.writestr("xl/styles.xml", estilos)
            for i, x in enumerate(hojas_xml):
                z.writestr(f"xl/worksheets/sheet{i + 1}.xml", x)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return path


# ---------------------------------------------------------------- ZIP
LEEME_ZIP = """Expediente de {proyecto} empaquetado el {fecha} con la skill startup-engineering-chile.

Para retomar en otra sesión (por ejemplo en Claude.ai, donde los archivos se borran entre conversaciones):
1. Sube este ZIP al iniciar la conversación.
2. Pide: "retomemos mi proyecto con este expediente".
   La skill corre: expediente.py restaurar <zip> --dir <carpeta>

Contiene entrevistas y datos del proyecto: guárdalo en un lugar privado.
"""
MAX_ZIP_BYTES = 200 * 1024 * 1024


def _excluir(f):
    return ".bak" in f or f.endswith(".tmp") or f.startswith(".tmp_") or f == ".lock"


def empaquetar(base, salida=None, nombre=None):
    e = exp_dir(base)
    hoy = dt.date.today().isoformat()
    proyecto = nombre_proyecto(base) or "proyecto"
    salida = os.path.abspath(salida or base)
    os.makedirs(salida, exist_ok=True)
    dst = os.path.join(salida, nombre or f"expediente_{slug(proyecto) or 'proyecto'}_{hoy}.zip")
    escribir_manifest(base, empaquetado=hoy)
    fd, tmp = tempfile.mkstemp(dir=salida, suffix=".tmp")
    os.close(fd)
    n = 0
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(e):
                dirs[:] = sorted(d for d in dirs if d != "__pycache__")
                for f in sorted(files):
                    if _excluir(f):
                        continue
                    p = os.path.join(root, f)
                    z.write(p, os.path.relpath(p, os.path.dirname(e)).replace(os.sep, "/"))
                    n += 1
            z.writestr("LEEME.txt", LEEME_ZIP.format(proyecto=proyecto, fecha=hoy))
        os.replace(tmp, dst)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return dst, n


def restaurar(zip_path, base, forzar=False, avisar=print):
    if not zipfile.is_zipfile(zip_path):
        sys.exit(f"{zip_path} no es un ZIP válido.")
    destino = os.path.abspath(base)
    e = exp_dir(base)
    with zipfile.ZipFile(zip_path) as z:
        miembros = [i for i in z.infolist() if i.filename.startswith("expediente/") and not i.is_dir()]
        if not miembros:
            sys.exit("El ZIP no contiene una carpeta expediente/. ¿Es un paquete de `expediente.py empaquetar`?")
        if sum(i.file_size for i in miembros) > MAX_ZIP_BYTES:
            sys.exit("El ZIP descomprimido supera 200 MB; no se restaura.")
        for i in miembros:
            objetivo = os.path.abspath(os.path.join(destino, i.filename))
            if not objetivo.startswith(destino + os.sep):
                sys.exit(f"Ruta insegura en el ZIP: {i.filename}; no se restaura.")
        if os.path.isdir(e):
            if not forzar:
                actual = (leer_manifest(base) or {}).get("actualizado", "?")
                sys.exit(f"Ya hay un expediente en {e} (actualizado {actual}). Usa --forzar para reemplazarlo; "
                         "el actual se respalda como expediente.bak-<fecha-hora>.")
            respaldo = e + ".bak-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            shutil.move(e, respaldo)
            avisar(f"Respaldo del expediente anterior: {respaldo}")
        for i in miembros:
            objetivo = os.path.join(destino, *i.filename.split("/"))
            os.makedirs(os.path.dirname(objetivo), exist_ok=True)
            with z.open(i) as src, open(objetivo, "wb") as out:
                shutil.copyfileobj(src, out)
    return len(miembros)


# ---------------------------------------------------------------- HTML (dashboard interactivo)
CSS = """
:root{--bg:#f7f7f5;--card:#fff;--tx:#1d1d1b;--mut:#6b6b66;--bd:#e3e2dc;--ok:#2f7d4f;--warn:#b7791f;--bad:#c0392b;--acc:#2d5bd7;--track:#ecebe5}
@media (prefers-color-scheme:dark){:root{--bg:#161615;--card:#1f1f1d;--tx:#ecebe6;--mut:#a3a29b;--bd:#33332f;--ok:#5cc28a;--warn:#e0a84a;--bad:#ef6f5f;--acc:#7b9cff;--track:#2a2a27}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1100px;margin:0 auto;padding:24px 16px 48px}h1{font-size:26px;margin:0 0 4px}h2{font-size:16px;margin:0 0 12px}
.sub{color:var(--mut);margin-bottom:20px}.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));margin-top:16px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px;overflow-x:auto}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:16px}
.kpi{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px}.kpi b{display:block;font-size:24px}
.kpi span{color:var(--mut);font-size:13px}table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--bd);vertical-align:top}th{color:var(--mut);font-weight:600;cursor:pointer;user-select:none}
th:hover{color:var(--tx)}.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;border:1px solid var(--bd)}
.go{color:var(--ok);border-color:var(--ok)}.hold,.encurso{color:var(--warn);border-color:var(--warn)}.kill,.recycle{color:var(--bad);border-color:var(--bad)}
.bar{height:22px;background:var(--acc);border-radius:4px;opacity:.85;min-width:2px}.row{display:grid;grid-template-columns:110px 1fr 40px;gap:8px;align-items:center;margin:6px 0}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}.dot.ok{background:var(--ok)}.dot.warn{background:var(--warn)}.dot.bad{background:var(--bad)}
.gates{display:grid;grid-template-columns:repeat(10,1fr);gap:4px;margin:8px 0 4px}
.gate{border-radius:6px;padding:6px 4px;text-align:center;font-size:12px;background:var(--track);border:2px solid transparent;cursor:pointer}
.gate.listo{background:var(--ok);color:#fff}.gate.parcial{background:var(--warn);color:#fff}.gate.actual{border-color:var(--acc)}
.gate small{display:block;opacity:.85}.det{display:none;margin-top:8px}.det.on{display:block}
.funnel .row{grid-template-columns:120px 1fr 40px}.runway{font-size:28px;font-weight:700}
input[type=search]{width:100%;padding:8px 10px;border-radius:8px;border:1px solid var(--bd);background:var(--card);color:var(--tx);font:inherit;margin:8px 0 0}
footer{color:var(--mut);font-size:12px;margin-top:24px}@media (max-width:640px){.gates{grid-template-columns:repeat(5,1fr)}}
@media print{input[type=search]{display:none}.det{display:block}}
"""

JS = """
document.querySelectorAll('.gate').forEach(function(g){g.addEventListener('click',function(){
  document.querySelectorAll('.det').forEach(function(d){d.classList.toggle('on',d.id==='det-'+g.dataset.g&&!d.classList.contains('on'));});});});
var q=document.getElementById('filtro');if(q){q.addEventListener('input',function(){var t=q.value.toLowerCase();
  document.querySelectorAll('tbody tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(t)>=0?'':'none';});});}
document.querySelectorAll('th').forEach(function(th){th.addEventListener('click',function(){var tb=th.closest('table').querySelector('tbody');
  if(!tb)return;var i=Array.prototype.indexOf.call(th.parentNode.children,th);var asc=th.dataset.o!=='a';th.dataset.o=asc?'a':'d';
  var rs=Array.prototype.slice.call(tb.rows);rs.sort(function(a,b){var x=a.cells[i].textContent,y=b.cells[i].textContent;
  var nx=parseFloat(x.replace(/[^0-9,.-]/g,'').replace(',','.')),ny=parseFloat(y.replace(/[^0-9,.-]/g,'').replace(',','.'));
  var c=(!isNaN(nx)&&!isNaN(ny))?nx-ny:x.localeCompare(y,'es');return asc?c:-c;});rs.forEach(function(r){tb.appendChild(r);});});});
"""


def _e(s):
    return html.escape(str(s if s is not None else ""))


def _pill(estado):
    k = re.sub(r"[^a-z]", "", (estado or "").lower())
    return f'<span class="pill {k}">{_e(estado or "—")}</span>'


def _tabla(cab, filas_):
    if not filas_:
        return '<p class="sub">Sin registros todavía.</p>'
    h = "".join(f"<th>{_e(c)}</th>" for c in cab)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas_)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"


def runway_meses(base):
    """(meses, fuente) desde Números clave (caja / gasto neto) o, en su defecto, del modelo (caja inicial / costos fijos)."""
    nc = numeros_clave(leer_estado(base))
    caja, gasto = nc.get("Caja actual (CLP)"), nc.get("Gasto mensual neto (CLP)")
    if caja is not None and gasto:
        return caja / gasto, "00_estado.md (caja actual / gasto mensual neto)"
    sup = supuestos_modelo(base)
    try:
        caja, fijos = float(sup.get("Caja inicial", "")), float(sup.get("Costos fijos", ""))
        if fijos > 0:
            return caja / fijos, "modelo financiero (caja inicial / costos fijos, sin ingresos)"
    except ValueError:
        pass
    return None, ""


def dashboard_html(base):
    hoy = dt.date.today()
    txt = leer_estado(base)
    if not txt:
        sys.exit("No hay expediente en esa carpeta.")
    proyecto = nombre_proyecto(base)
    gate = gate_actual_de(base)
    pend, venc = acciones(txt, hoy)
    est = hipotesis_estancadas(base, hoy)
    ents, ctas, pils = filas(base, "entrevistas"), filas(base, "cuentas_y_pipeline"), filas(base, "pilotos")
    hips, evs, exps = filas(base, "hipotesis"), filas(base, "evidencias"), filas(base, "experimentos")
    decs, riesgos = filas(base, "decisiones"), filas(base, "riesgos")
    abiertos = [r for r in riesgos if r.get("estado", "").lower() not in ("cerrado", "mitigado")]
    errores, _ = validar(base)
    mi = mision(txt, hoy)
    meses, fuente_rw = runway_meses(base)

    def sem(n):
        return "ok" if n == 0 else ("bad" if n >= 3 else "warn")
    semaf = [("Acciones vencidas", len(venc), sem(len(venc))), ("Hipótesis estancadas", len(est), sem(len(est))),
             ("Riesgos abiertos", len(abiertos), sem(len(abiertos))), ("Errores del expediente", len(errores), sem(len(errores)))]
    if mi:
        semaf.insert(0, ("Misión de 7 días vencida", 1 if mi["vencida"] else 0, "bad" if mi["vencida"] else "ok"))
    prog = progreso(base)
    celdas_g, detalles = [], []
    for g, nombre, _ in GATES:
        ok, tot = prog.get(g, (0, 0))
        clase = "listo" if tot and ok == tot else ("parcial" if ok else "")
        clase += " actual" if g == gate else ""
        celdas_g.append(f"<div class='gate {clase}' data-g='{g}' title='{_e(nombre)}'>{g}<small>{ok}/{tot}</small></div>")
        filas_ch = [[("✓" if c["cumple"] else "✗"), _e(c["texto"]), _e(c["min"]), _e(c["actual"])] for c in evaluar_gate(base, g)]
        detalles.append(f"<div class='det' id='det-{g}'><b>{g} · {_e(nombre)}</b>"
                        + _tabla(["", "Chequeo", "Mínimo", "Actual"], filas_ch) + "</div>")
    embudo = [("Hipótesis", len(hips)), ("Experimentos", len(exps)), ("Evidencias", len(evs)), ("Decisiones", len(decs))]
    mx = max([v for _, v in embudo] + [1])
    comercial = [("Entrevistas", len(ents)), ("Cuentas", len(ctas)), ("Pilotos", len(pils)),
                 ("Pilotos con decisión", sum(1 for p in pils if p.get("decision_comercial")))]
    mx2 = max([v for _, v in comercial] + [1])
    ev_por_h = {}
    for v in evs:
        ev_por_h[v.get("hypothesis_id", "")] = ev_por_h.get(v.get("hypothesis_id", ""), 0) + 1
    if meses is None:
        rw = "<div class='runway'>—</div><p class='sub'>Anota «Caja actual» y «Gasto mensual neto» en Números clave de 00_estado.md.</p>"
    else:
        c = "ok" if meses >= 12 else ("warn" if meses >= 6 else "bad")
        rw = (f"<div class='runway'><span class='dot {c}'></span>{meses:.1f} meses</div>"
              f"<p class='sub'>Fuente: {_e(fuente_rw)}. Verde ≥ 12, amarillo 6–12, rojo &lt; 6. Detalle con `finanzas.py runway`.</p>")
    partes = [f"<h1>{_e(proyecto)}</h1><div class='sub'>Dashboard del expediente · {hoy.isoformat()} · gate actual {_e(gate or '—')}</div>"]
    partes.append("<div class='kpis'>" + "".join(
        f"<div class='kpi'><b>{v}</b><span>{_e(k)}</span></div>" for k, v in
        [("Entrevistas", len(ents)), ("Hipótesis", len(hips)), ("Evidencias", len(evs)), ("Experimentos", len(exps)), ("Decisiones", len(decs))]) + "</div>")
    partes.append("<div class='card'><h2>Progreso por gate</h2><div class='gates'>" + "".join(celdas_g) + "</div>"
                  "<p class='sub'>Chequeos verificables en el expediente (expediente.py gate). Verde: listo para decidir; no es un Go automático. "
                  "Toca un gate para ver el detalle.</p>" + "".join(detalles) + "</div>")
    partes.append("<div class='grid'>")
    partes.append("<div class='card'><h2>Runway</h2>" + rw + "</div>")
    partes.append("<div class='card'><h2>Semáforo</h2>" + "".join(
        f"<div><span class='dot {c}'></span>{_e(k)}: <b>{v}</b></div>" for k, v, c in semaf) + "</div>")
    if mi:
        partes.append(f"<div class='card'><h2>Misión de 7 días</h2><p>{_e(mi['mision'])}</p><p class='sub'>Vence {_e(mi['vence'] or '?')} · "
                      f"{_e(mi['criterio'])} · {_pill(mi['estado'] or 'abierta')}</p></div>")
    partes.append("</div><div class='grid'>")
    partes.append("<div class='card funnel'><h2>Embudo de validación</h2>" + "".join(
        f"<div class='row'><span>{_e(k)}</span><div class='bar' style='width:{100 * v / mx:.0f}%'></div><b>{v}</b></div>" for k, v in embudo)
        + "<p class='sub'>Hipótesis → experimentos → evidencias → decisiones. Si se angosta mucho, hay supuestos sin probar.</p></div>")
    partes.append("<div class='card funnel'><h2>Embudo comercial</h2>" + "".join(
        f"<div class='row'><span>{_e(k)}</span><div class='bar' style='width:{100 * v / mx2:.0f}%'></div><b>{v}</b></div>" for k, v in comercial) + "</div>")
    partes.append("</div><div class='card' style='margin-top:16px'><h2>Buscar en las tablas</h2>"
                  "<input type='search' id='filtro' placeholder='Filtra por ID, texto o estado (p. ej. H-002, Go, piloto)'></div>")
    partes.append("<div class='grid'>")
    partes.append("<div class='card'><h2>Hipótesis</h2>" + _tabla(["ID", "Enunciado", "Evidencias", "Estado"], [
        [_e(h.get("hypothesis_id")), _e(h.get("enunciado_refutable", "")[:140]), str(ev_por_h.get(h.get("hypothesis_id"), 0)), _pill(h.get("estado"))] for h in hips]) + "</div>")
    partes.append("<div class='card'><h2>Experimentos</h2>" + _tabla(["ID", "Métrica / umbral", "Resultado", "Decisión"], [
        [_e(x.get("experiment_id")), _e(f"{x.get('metrica', '')} · {x.get('umbral', '')}"), _e(x.get("resultado")), _pill(x.get("decision"))] for x in exps]) + "</div>")
    partes.append("</div><div class='grid'>")
    partes.append("<div class='card'><h2>Últimas decisiones</h2>" + _tabla(["Fecha", "Gate", "Decisión", "Justificación"], [
        [_e(d.get("fecha")), _e(d.get("gate")), _pill(d.get("decision")), _e(d.get("justificacion", "")[:160])] for d in decs[-6:][::-1]]) + "</div>")
    partes.append("<div class='card'><h2>Próximas acciones</h2>" + _tabla(["Acción", "Responsable", "Vence"], [
        [_e(x) for x in t] for t in venc + pend]) + "</div>")
    partes.append("</div>")
    if abiertos:
        partes.append("<div class='card' style='margin-top:16px'><h2>Riesgos abiertos</h2>" + _tabla(["ID", "Riesgo", "Prob.", "Impacto", "Mitigación"], [
            [_e(r.get("risk_id")), _e(r.get("riesgo")), _e(r.get("probabilidad")), _e(r.get("impacto")), _e(r.get("mitigacion"))] for r in abiertos]) + "</div>")
    partes.append("<footer>Generado por la skill Startup Engineering Chile desde expediente/ (esquema v" + str(SCHEMA_VERSION)
                  + "). Lo que no está registrado no aparece: la presentación no crea evidencia. Revisa que no tenga datos confidenciales "
                  "antes de compartirlo.</footer>")
    datos = json.dumps({"proyecto": proyecto, "fecha": hoy.isoformat(), "gate": gate, "progreso": prog}, ensure_ascii=False)
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{_e(proyecto)} · dashboard</title><style>{CSS}</style></head><body><main>{''.join(partes)}</main>"
            f"<script type='application/json' id='datos'>{_e(datos)}</script><script>{JS}</script></body></html>")


def escribir_html(path, texto):
    escribir_atomico(path, texto)


__all__ = ["informe_semanal", "onepager", "deck_md", "supuestos_modelo", "todas_las_tablas", "exportar_csv", "escribir_xlsx",
           "empaquetar", "restaurar", "dashboard_html", "runway_meses", "escribir_bytes_atomico", "MAX_ZIP_BYTES"]
