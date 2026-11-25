#!/usr/bin/env python3
"""Cliente mínimo para Firecrawl self-hosted (API v2). Solo biblioteca estándar.

Configuración (variables de entorno):
  FIRECRAWL_API_URL   base de la API (por defecto http://localhost:3002)
  FIRECRAWL_API_KEY   opcional; solo si tu instancia exige autenticación

Comandos:
  health [--deep] [--guardar ARCHIVO.json]
        ¿está corriendo? --deep prueba de verdad scrape, map y search y guarda las capacidades
  scrape URL [--out DIR] [--nombre X] [--full] [--timeout SEG]
        una página (o un PDF público) -> markdown con URL y fecha. Para PDFs largos: --timeout 180
  map URL [--search TXT] [--limit N]                lista URLs de un sitio
  crawl URL --out DIR [--limit N] [--include REGEX ...] [--exclude REGEX ...]
  search "consulta" [--limit N] [--scrape] [--out DIR] [--country CL]
  competidor URL --nombre "X" --out DIR [--max-paginas 8] [--extra URL ...]
        mapea el sitio, elige páginas clave (precios, producto, clientes, integraciones,
        nosotros, seguridad) y guarda una instantánea fechada en DIR/<nombre>/<AAAA-MM-DD>/.
        Crea DIR/<nombre>/ficha.md solo la primera vez (nunca la sobrescribe) y, si hay una
        instantánea anterior, informa los cambios de precios detectados.
  lote ARCHIVO --out DIR [--paralelo 3]
        varios competidores; ARCHIVO tiene una línea por competidor: "Nombre | https://url"

Códigos de salida: 0 ok · 2 Firecrawl no responde (conexión rechazada) · 3 función no
disponible en esta instancia (p. ej. search) · 1 otro error.
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.environ.get("FIRECRAWL_API_URL", "http://localhost:3002").rstrip("/")
KEY = os.environ.get("FIRECRAWL_API_KEY", "")

AYUDA_SETUP = (
    f"Firecrawl no responde en {BASE}.\n"
    "- ¿Está levantado? Docker: `docker compose ps` en la carpeta de firecrawl; binario: `firecrawl-local serve`.\n"
    "- ¿Otra URL/puerto? Define FIRECRAWL_API_URL.\n"
    "- Guía: references/firecrawl.md de la skill.\n"
    "Mientras tanto, el agente puede seguir con sus herramientas web y anotar la fuente igual."
)


class NoDisponible(Exception):
    """La instancia responde pero no ofrece esta función (p. ej. search sin backend)."""


class FirecrawlCaido(Exception):
    """No hay servidor escuchando (conexión rechazada / host inexistente)."""


def _es_caido(reason):
    if isinstance(reason, ConnectionRefusedError):
        return True
    errno = getattr(reason, "errno", None)
    if errno in (111, 10061, 61):  # ECONNREFUSED en Linux / Windows / macOS
        return True
    return type(reason).__name__ == "gaierror"


def req(method, path, body=None, timeout=90):
    url = BASE + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if KEY:
        headers["Authorization"] = f"Bearer {KEY}"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="replace")[:800]
        low = txt.lower()
        if e.code in (404, 501) or "not supported" in low or ("cloud" in low and e.code in (401, 402, 403)):
            raise NoDisponible(f"HTTP {e.code} en {path}: {txt}")
        raise RuntimeError(f"HTTP {e.code} en {path}: {txt}")
    except urllib.error.URLError as e:
        if _es_caido(e.reason):
            raise FirecrawlCaido(str(e.reason))
        raise RuntimeError(f"error de red en {path}: {e.reason}")
    except (TimeoutError, ConnectionError, OSError) as e:
        # timeouts y conexiones cortadas a mitad de respuesta: falla de esta página, no del servicio
        raise RuntimeError(f"{type(e).__name__} en {path}: {e}")


def slug(texto, n=60):
    t = re.sub(r"^https?://", "", texto.lower())
    t = re.sub(r"[^a-z0-9áéíóúñ]+", "-", t).strip("-")
    return (t[:n] or "pagina").strip("-")


def hoy():
    return dt.date.today().isoformat()


def guardar_md(out, nombre, url, md, meta, extra=None):
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, slug(nombre) + ".md")
    fm = {"url": url, "fecha_consulta": hoy(), "titulo": (meta or {}).get("title", ""),
          "status": (meta or {}).get("statusCode", ""), "fuente": "firecrawl-local"}
    if extra:
        fm.update(extra)
    head = "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()) + "\n---\n\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + (md or ""))
    return path


def scrape(url, full=False, formats=("markdown", "links"), timeout_s=60):
    body = {"url": url, "formats": list(formats), "onlyMainContent": not full, "timeout": int(timeout_s * 1000)}
    res = req("POST", "/v2/scrape", body, timeout=timeout_s + 20)
    if not res.get("success", True) and "data" not in res:
        raise RuntimeError(f"scrape falló: {json.dumps(res)[:500]}")
    return res.get("data", res)


def site_map(url, search=None, limit=500):
    body = {"url": url, "limit": limit}
    if search:
        body["search"] = search
    res = req("POST", "/v2/map", body, timeout=120)
    return [l if isinstance(l, dict) else {"url": l} for l in res.get("links", [])]


# ---------- health ----------

def c_health(a):
    vivo = None
    for path in ("/health/readiness", "/health"):
        try:
            r = urllib.request.urlopen(BASE + path, timeout=5)
            vivo = f"{BASE}{path} (HTTP {r.status})"
            break
        except Exception:
            continue
    if not vivo:
        print(AYUDA_SETUP, file=sys.stderr)
        sys.exit(2)
    if not a.deep:
        print(f"OK Firecrawl responde en {vivo}. (Usa --deep para probar scrape/search de verdad.)")
        return
    cap = {"fecha": hoy(), "base": BASE}
    pruebas = [
        ("scrape", lambda: bool(scrape("https://example.com").get("markdown"))),
        ("map", lambda: len(site_map("https://example.com", limit=5)) >= 0),
        ("search", lambda: bool(req("POST", "/v2/search", {"query": "example domain", "limit": 1}, timeout=60))),
    ]
    for nombre, f in pruebas:
        try:
            cap[nombre] = "ok" if f() else "vacio"
        except FirecrawlCaido:
            cap[nombre] = "caido"
        except NoDisponible as e:
            cap[nombre] = "no disponible"
        except Exception as e:
            cap[nombre] = ("no disponible" if nombre == "search" else "error") + f" ({str(e)[:100]})"
    for k in ("scrape", "map", "search"):
        print(f"{k:7} {cap[k]}")
    if a.guardar:
        os.makedirs(os.path.dirname(os.path.abspath(a.guardar)), exist_ok=True)
        with open(a.guardar, "w", encoding="utf-8") as fh:
            json.dump(cap, fh, ensure_ascii=False, indent=2)
        print(f"Capacidades guardadas en {a.guardar}")
    if cap["scrape"] != "ok":
        sys.exit(1)


# ---------- comandos simples ----------

def c_scrape(a):
    d = scrape(a.url, full=a.full, timeout_s=a.timeout)
    md, meta = d.get("markdown", ""), d.get("metadata", {})
    if a.out:
        p = guardar_md(a.out, a.nombre or a.url, a.url, md, meta)
        print(f"Guardado {p} ({len(md)} caracteres)")
    else:
        print(md)


def c_map(a):
    links = site_map(a.url, a.search, a.limit)
    for l in links:
        print(l.get("url", ""), ("· " + l.get("title", "")) if l.get("title") else "")
    print(f"\n{len(links)} URLs", file=sys.stderr)


def c_crawl(a):
    body = {"url": a.url, "limit": a.limit, "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True}}
    if a.include:
        body["includePaths"] = a.include
    if a.exclude:
        body["excludePaths"] = a.exclude
    res = req("POST", "/v2/crawl", body)
    jid = res.get("id")
    if not jid:
        raise RuntimeError(f"crawl no devolvió id: {res}")
    print(f"crawl {jid} iniciado; consultando estado…", file=sys.stderr)
    t0, data = time.time(), []
    while True:
        st = req("GET", f"/v2/crawl/{jid}")
        status = st.get("status", "")
        data = st.get("data", []) or data
        print(f"  {status} {st.get('completed', len(data))}/{st.get('total', '?')}", file=sys.stderr)
        if status in ("completed", "failed", "cancelled"):
            break
        if time.time() - t0 > a.max_segundos:
            print("  tiempo máximo alcanzado; se guarda lo obtenido", file=sys.stderr)
            break
        time.sleep(3)
    for n, item in enumerate(data):
        meta = item.get("metadata", {})
        url = meta.get("sourceURL") or meta.get("url") or ""
        guardar_md(a.out, url or f"pagina-{n}", url, item.get("markdown", ""), meta)
    print(f"{len(data)} páginas guardadas en {a.out}")


def c_search(a):
    body = {"query": a.query, "limit": a.limit}
    if a.country:
        body["country"] = a.country.upper()
    if a.scrape:
        body["scrapeOptions"] = {"formats": ["markdown"], "onlyMainContent": True}
    try:
        res = req("POST", "/v2/search", body, timeout=120)
    except (NoDisponible, RuntimeError) as e:
        print(f"SEARCH_NO_DISPONIBLE: {e}\n"
              "La búsqueda no funciona en esta instancia (en self-host requiere un backend como SearXNG; "
              "en firecrawl-local se delega a la nube). Usa la búsqueda web del agente para descubrir URLs "
              "y luego `scrape`/`competidor` para leerlas y archivarlas.", file=sys.stderr)
        sys.exit(3)
    data = res.get("data", {})
    items = data.get("web", data) if isinstance(data, dict) else data
    for i, it in enumerate(items or [], 1):
        print(f"{i}. {it.get('title','')}\n   {it.get('url','')}\n   {(it.get('description') or '')[:200]}")
        if a.out and it.get("markdown"):
            guardar_md(a.out, it.get("url", f"res-{i}"), it.get("url", ""), it["markdown"], it.get("metadata", {}),
                       {"consulta": a.query})
    if not items:
        print("Sin resultados.")


# ---------- competidor ----------

CATEGORIAS = {
    "precios": ["pricing", "precio", "precios", "planes", "plans", "plan", "tarifa", "tarifas", "preco", "cotiz", "cotizar", "suscripcion"],
    "producto": ["product", "producto", "productos", "solucion", "soluciones", "solution", "features", "funcionalidad",
                 "caracteristica", "plataforma", "platform", "como-funciona", "how-it-works", "modulos", "servicios"],
    "clientes": ["customers", "clientes", "casos", "case-stud", "caso-de-exito", "casos-de-exito", "testimonio", "historias", "success"],
    "integraciones": ["integration", "integraciones", "integracion", "api", "developers", "partners", "socios", "marketplace"],
    "nosotros": ["about", "nosotros", "quienes-somos", "empresa", "equipo", "team", "company", "historia"],
    "seguridad": ["security", "seguridad", "privacidad", "privacy", "compliance", "trust", "certificacion"],
}
_PERIODO = r"(?:\s?\+\s?IVA)?(?:\s?(?:/\s?(?:mes|año|usuario|user|month|year)|por\s+(?:mes|año|usuario)|mensual(?:es)?|anual(?:es)?))?"
PRECIO_RE = re.compile(
    r"(?:(?:US\$|USD|CLP|UF|R\$|MXN|COP|PEN|€|\$)\s?\d[\d\.,]*" + _PERIODO + r")"
    r"|(?:\b\d[\d\.,]*\s?(?:UF|USD|CLP|dólares|pesos)\b" + _PERIODO + r")",
    re.I)


def puntuar(url, cat):
    path = urllib.parse.urlparse(url).path.lower()
    path_n = path.translate(str.maketrans("áéíóú", "aeiou"))
    if any(x in path_n for x in ("/blog", "/tag", "/author", "/wp-", ".pdf", ".jpg", ".png", "/feed", "/category")):
        return 0
    score = 0
    for kw in CATEGORIAS[cat]:
        if re.search(r"(^|[/\-_])" + re.escape(kw), path_n):
            score += 3 if path_n.rstrip("/").endswith(kw) else 2
    if score:
        score -= path_n.count("/") * 0.3
    return score


def _ficha_inicial(nombre, raiz, fecha, resumen, precios):
    ficha = [f"# Ficha competidor: {nombre}", "",
             f"- URL: {raiz}", f"- Primera consulta: {fecha}", "- Fuente: sitio público (Firecrawl local)",
             f"- Instantáneas: carpetas con fecha junto a este archivo", "",
             "> Completar leyendo las páginas guardadas. Distinguir lo que el sitio *declara* de lo verificado.",
             "> Cada afirmación cita archivo/URL. Si un dato no aparece, escribir 'no publicado'.",
             "> Este archivo no se sobrescribe en consultas posteriores.", "",
             "| Campo (competencia.csv) | Valor | Fuente (archivo/URL) |", "|---|---|---|"]
    for campo in ["alternativa", "tipo (directo/indirecto/in-house/servicio/no hacer nada)", "segmento",
                  "precio (moneda original, unidad, IVA, fecha)", "resultado que promete", "integracion",
                  "ventaja (declarada)", "limitacion (observada o inferida — marcar cuál)", "canal de venta",
                  "clientes/logos citados", "señales de tracción"]:
        ficha.append(f"| {campo} |  |  |")
    ficha += ["", f"## Precios detectados automáticamente ({fecha}; verificar en contexto)"]
    ficha += [f"- {u}: {', '.join(h)}" for u, h in precios] or ["- ninguno detectado (puede ser 'cotizar' o precio oculto)"]
    ficha += ["", f"## Páginas guardadas ({fecha})"] + [
        f"- [{p['categoria']}] {p['url']} → {fecha}/{p.get('archivo', 'ERROR: ' + p.get('error', ''))}" for p in resumen["paginas"]]
    return "\n".join(ficha) + "\n"


def competidor(url, nombre, out, max_paginas=8, limit_map=300, extra=None, pausa=1.0, log=None):
    log = log or (lambda m: print(m, file=sys.stderr))
    raiz = url if url.startswith("http") else "https://" + url
    base_dir = os.path.join(out, slug(nombre))
    fecha = hoy()
    snap = os.path.join(base_dir, fecha)
    log(f"[{nombre}] mapeando {raiz} …")
    caido = False
    try:
        links = [l["url"] for l in site_map(raiz, limit=limit_map) if l.get("url")]
    except FirecrawlCaido:
        raise
    except Exception as e:
        log(f"[{nombre}]   map falló ({str(e)[:100]}); sigo con portada y --extra")
        links = []
    os.makedirs(snap, exist_ok=True)
    elegidas = [("portada", raiz)]
    for cat in CATEGORIAS:
        cands = [u for s, u in sorted(((puntuar(u, cat), u) for u in links), reverse=True) if s > 0]
        for u in cands[:2 if cat in ("precios", "producto") else 1]:
            if u not in [x[1] for x in elegidas]:
                elegidas.append((cat, u))
    elegidas = elegidas[:max_paginas] + [("extra", u) for u in (extra or [])]
    resumen = {"competidor": nombre, "url": raiz, "fecha_consulta": fecha, "urls_en_mapa": len(links), "paginas": []}
    precios = []

    def guardar_resumen():
        with open(os.path.join(snap, "resumen.json"), "w", encoding="utf-8") as fh:
            json.dump(resumen, fh, ensure_ascii=False, indent=2)

    for cat, u in elegidas:
        try:
            d = scrape(u)
            md, meta = d.get("markdown", ""), d.get("metadata", {})
            p = guardar_md(snap, f"{cat}-{urllib.parse.urlparse(u).path or 'inicio'}", u, md, meta, {"categoria": cat})
            hall = sorted(set(m.group(0).strip() for m in PRECIO_RE.finditer(md)))[:15]
            if hall:
                precios.append((u, hall))
            resumen["paginas"].append({"categoria": cat, "url": u, "archivo": os.path.basename(p), "titulo": meta.get("title", ""),
                                       "status": meta.get("statusCode"), "caracteres": len(md), "precios_detectados": hall})
            log(f"[{nombre}]   ✓ {cat:13} {u}")
        except FirecrawlCaido as e:
            resumen["paginas"].append({"categoria": cat, "url": u, "error": "Firecrawl dejó de responder"})
            log(f"[{nombre}]   ✗ Firecrawl dejó de responder; se guarda lo obtenido")
            caido = True
            break
        except Exception as e:
            resumen["paginas"].append({"categoria": cat, "url": u, "error": str(e)[:300]})
            log(f"[{nombre}]   ✗ {cat:13} {u}: {str(e)[:120]}")
        guardar_resumen()
        time.sleep(pausa)
    guardar_resumen()

    # comparar con la instantánea anterior
    previas = sorted(d for d in os.listdir(base_dir)
                     if re.match(r"\d{4}-\d{2}-\d{2}$", d) and d < fecha and os.path.exists(os.path.join(base_dir, d, "resumen.json")))
    cambios = []
    if previas:
        ant = json.load(open(os.path.join(base_dir, previas[-1], "resumen.json"), encoding="utf-8"))
        prev = {p["url"]: set(p.get("precios_detectados") or []) for p in ant.get("paginas", []) if "archivo" in p}
        for p in resumen["paginas"]:
            if "archivo" in p and p["url"] in prev:
                nuevo, viejo = set(p["precios_detectados"]), prev[p["url"]]
                if nuevo != viejo:
                    cambios.append(f"- {p['url']}: antes {sorted(viejo) or '—'} → ahora {sorted(nuevo) or '—'}")
        with open(os.path.join(snap, "cambios.md"), "w", encoding="utf-8") as fh:
            fh.write(f"# Cambios vs {previas[-1]}\n\n" + ("\n".join(cambios) if cambios else "Sin cambios en precios detectados.") + "\n")

    ficha_path = os.path.join(base_dir, "ficha.md")
    if not os.path.exists(ficha_path):
        with open(ficha_path, "w", encoding="utf-8") as fh:
            fh.write(_ficha_inicial(nombre, raiz, fecha, resumen, precios))
        ficha_msg = "ficha.md creada"
    else:
        ficha_msg = "ficha.md existente NO modificada"
    ok = sum(1 for p in resumen["paginas"] if "archivo" in p)
    log(f"[{nombre}] {ok}/{len(resumen['paginas'])} páginas en {snap} · {ficha_msg}"
        + (f" · {len(cambios)} cambio(s) de precio vs {previas[-1]} (ver cambios.md)" if previas else ""))
    return {"nombre": nombre, "ok": ok, "total": len(resumen["paginas"]), "dir": snap, "cambios": cambios, "caido": caido}


def c_competidor(a):
    r = competidor(a.url, a.nombre, a.out, a.max_paginas, a.limit_map, a.extra, a.pausa)
    for c in r["cambios"]:
        print(c)
    if r["caido"]:
        sys.exit(2)


def c_lote(a):
    items = []
    for line in open(a.archivo, encoding="utf-8-sig"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            n, u = [x.strip() for x in line.split("|", 1)]
        else:
            u = line
            n = urllib.parse.urlparse(u if u.startswith("http") else "https://" + u).netloc
        items.append((n, u))
    if not items:
        sys.exit("El archivo no tiene competidores.")
    resultados = []
    with cf.ThreadPoolExecutor(max_workers=max(1, a.paralelo)) as ex:
        futs = {ex.submit(competidor, u, n, a.out, a.max_paginas, 300, None, a.pausa): n for n, u in items}
        for f in cf.as_completed(futs):
            try:
                resultados.append(f.result())
            except FirecrawlCaido:
                print(AYUDA_SETUP, file=sys.stderr)
                sys.exit(2)
            except Exception as e:
                resultados.append({"nombre": futs[f], "ok": 0, "total": 0, "error": str(e)[:200], "cambios": []})
    print("\nResumen del lote:")
    for r in sorted(resultados, key=lambda r: r["nombre"]):
        print(f"- {r['nombre']}: {r['ok']}/{r['total']} páginas" + (f" · ERROR {r['error']}" if r.get("error") else "")
              + (f" · {len(r['cambios'])} cambio(s) de precio" if r.get("cambios") else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("health"); p.add_argument("--deep", action="store_true"); p.add_argument("--guardar")
    p.set_defaults(f=c_health)
    p = sp.add_parser("scrape"); p.add_argument("url"); p.add_argument("--out"); p.add_argument("--nombre")
    p.add_argument("--full", action="store_true", help="incluye menú/pie (onlyMainContent=false)")
    p.add_argument("--timeout", type=int, default=60, help="segundos (PDFs largos: 180)"); p.set_defaults(f=c_scrape)
    p = sp.add_parser("map"); p.add_argument("url"); p.add_argument("--search"); p.add_argument("--limit", type=int, default=500)
    p.set_defaults(f=c_map)
    p = sp.add_parser("crawl"); p.add_argument("url"); p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int, default=20); p.add_argument("--include", nargs="*"); p.add_argument("--exclude", nargs="*")
    p.add_argument("--max-segundos", type=int, default=300); p.set_defaults(f=c_crawl)
    p = sp.add_parser("search"); p.add_argument("query"); p.add_argument("--limit", type=int, default=10)
    p.add_argument("--scrape", action="store_true"); p.add_argument("--out"); p.add_argument("--country", default="CL")
    p.set_defaults(f=c_search)
    p = sp.add_parser("competidor"); p.add_argument("url"); p.add_argument("--nombre", required=True)
    p.add_argument("--out", required=True); p.add_argument("--max-paginas", type=int, default=8)
    p.add_argument("--limit-map", type=int, default=300); p.add_argument("--extra", nargs="*")
    p.add_argument("--pausa", type=float, default=1.0, help="segundos entre páginas del mismo sitio"); p.set_defaults(f=c_competidor)
    p = sp.add_parser("lote"); p.add_argument("archivo"); p.add_argument("--out", required=True)
    p.add_argument("--paralelo", type=int, default=3); p.add_argument("--max-paginas", type=int, default=8)
    p.add_argument("--pausa", type=float, default=1.0); p.set_defaults(f=c_lote)
    a = ap.parse_args()
    try:
        a.f(a)
    except FirecrawlCaido:
        print(AYUDA_SETUP, file=sys.stderr); sys.exit(2)
    except NoDisponible as e:
        print(f"NO_DISPONIBLE: {e}", file=sys.stderr); sys.exit(3)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr); sys.exit(1)


if __name__ == "__main__":
    main()
