"""Pruebas de los scripts de la skill (unittest; también corre con pytest). No usan la red."""
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, "skills", "startup-engineering-chile")
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
os.environ.setdefault("SEC_CACHE", os.path.join(tempfile.gettempdir(), "sec_test_cache.json"))

import dashboard  # noqa: E402
import expediente as ex  # noqa: E402
import finanzas  # noqa: E402
import fondos_lint  # noqa: E402
import ingestar as ingesta  # noqa: E402
import modelo_xlsx  # noqa: E402


def correr(mod, *args):
    """Ejecuta main() de un script y devuelve (código, salida+errores)."""
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with redirect_stdout(out), redirect_stderr(err):
        try:
            mod.main(list(args))
        except SystemExit as e:
            if isinstance(e.code, str):
                err.write(e.code)
                code = 1
            else:
                code = e.code or 0
    return code, out.getvalue() + err.getvalue()


class ConExpediente(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        correr(ex, "init", "--dir", self.dir, "--proyecto", "Prueba")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def reg(self, nombre):
        return os.path.join(self.dir, "expediente", "registros", nombre + ".csv")


class TestExpediente(ConExpediente):
    def test_init_crea_estado_manifest_y_gitignore(self):
        e = os.path.join(self.dir, "expediente")
        self.assertTrue(os.path.exists(os.path.join(e, "00_estado.md")))
        self.assertEqual(json.load(open(os.path.join(e, "manifest.json")))["schema_version"], ex.SCHEMA_VERSION)
        self.assertTrue(os.path.exists(os.path.join(e, ".gitignore")))

    def test_add_asigna_id_y_estado(self):
        code, out = correr(ex, "add", "hipotesis", "enunciado_refutable=X", "--dir", self.dir)
        self.assertEqual(code, 0)
        self.assertIn("H-001", out)
        h, rows = ex.leer(self.reg("hipotesis"))
        self.assertEqual(dict(zip(h, rows[0]))["estado"], "propuesta-agente")

    def test_add_exige_obligatorios(self):
        code, out = correr(ex, "add", "experimentos", "metodo=entrevistas", "--dir", self.dir)
        self.assertNotEqual(code, 0)
        self.assertIn("hypothesis_id", out)

    def test_add_rechaza_fecha_y_decision_invalidas(self):
        code, _ = correr(ex, "add", "evidencias", "afirmacion=a", "fuente_url_o_ruta=b", "fecha=25/11/2026", "--dir", self.dir)
        self.assertNotEqual(code, 0)
        code, _ = correr(ex, "add", "decisiones", "gate=G1", "decision=Quizás", "justificacion=x", "--dir", self.dir)
        self.assertNotEqual(code, 0)

    def test_add_avisa_referencia_inexistente_y_pii(self):
        _, out = correr(ex, "add", "evidencias", "hypothesis_id=H-099", "afirmacion=llamar a ana@x.cl",
                        "fuente_url_o_ruta=nota", "--dir", self.dir)
        self.assertIn("H-099 no existe", out)
        self.assertIn("privacidad", out)

    def test_validar_detecta_problemas(self):
        with open(self.reg("hipotesis"), "a", encoding="utf-8") as fh:
            fh.write("H-001,,,,,,,,,,,raro\nH-001,,,,,,,,,,,confirmado\n")
        with open(self.reg("evidencias"), "a", encoding="utf-8") as fh:
            fh.write("EV-001,H-777,primaria,a,b,ayer,,,diez,,,,,confirmado\n")
        errores, _ = ex.validar(self.dir)
        texto = "\n".join(errores)
        self.assertIn("ID duplicado", texto)
        self.assertIn("no es AAAA-MM-DD", texto)
        self.assertIn("no es un número", texto)
        self.assertIn("H-777 no existe", texto)

    def test_registro_vacio_y_migrar(self):
        open(self.reg("decisiones"), "w").close()
        errores, _ = ex.validar(self.dir)
        self.assertTrue(any("vacío" in e for e in errores))
        h, _ = ex.leer(self.reg("hipotesis"))
        with open(self.reg("hipotesis"), "w", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerow(h[:-1])
        os.remove(os.path.join(self.dir, "expediente", "manifest.json"))
        code, _ = correr(ex, "migrar", "--dir", self.dir)
        self.assertEqual(code, 0)
        self.assertEqual(ex.validar(self.dir)[0], [])
        m = json.load(open(os.path.join(self.dir, "expediente", "manifest.json")))
        self.assertEqual(m["schema_version"], ex.SCHEMA_VERSION)

    def test_estado_no_se_cae_con_csv_ilegible(self):
        with open(self.reg("evidencias"), "wb") as fh:
            fh.write(b"\xff\xfe\x00basura")
        code, out = correr(ex, "estado", "--dir", self.dir)
        self.assertEqual(code, 0)
        self.assertIn("ILEGIBLE", out)

    def test_exportar_con_bom_y_punto_y_coma(self):
        correr(ex, "add", "hipotesis", "enunciado_refutable=Ñandú, sí", "--dir", self.dir)
        correr(ex, "exportar", "--dir", self.dir)
        raw = open(os.path.join(self.dir, "expediente", "entregables", "excel", "hipotesis.csv"), "rb").read()
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
        self.assertIn(";", raw.decode("utf-8-sig").splitlines()[0])

    def test_doc_acepta_id_corto_y_no_sobrescribe(self):
        code, out = correr(ex, "doc", "tpl-31", "--dir", self.dir)
        self.assertEqual(code, 0, out)
        _, out = correr(ex, "doc", "TPL-031", "--dir", self.dir)
        self.assertIn("Ya existe", out)

    def test_informes_y_dashboard(self):
        correr(ex, "add", "hipotesis", "enunciado_refutable=X", "--dir", self.dir)
        for tipo in ("semanal", "onepager"):
            code, out = correr(ex, "informe", tipo, "--dir", self.dir)
            self.assertEqual(code, 0, out)
        code, out = correr(dashboard, "--dir", self.dir)
        self.assertEqual(code, 0, out)
        html = open(os.path.join(self.dir, "expediente", "entregables", "dashboard.html"), encoding="utf-8").read()
        self.assertIn("<!doctype html>", html)
        self.assertNotIn("<script src", html)
        self.assertNotIn("<link", html)


class TestCatalogos(unittest.TestCase):
    def test_nombres_de_archivo_ascii(self):
        for _, _, fs in os.walk(SKILL):
            for f in fs:
                self.assertTrue(f.isascii(), f"nombre no ASCII: {f}")

    def test_catalogos_apuntan_a_archivos_existentes(self):
        h, rows = ex.leer(os.path.join(ex.PLANTILLAS, "catalogo_plantillas.csv"))
        for r in rows:
            d = dict(zip(h, r))
            if d["troncal"] == "si":
                self.assertTrue(d["ruta"] and os.path.exists(os.path.join(ex.PLANTILLAS, d["ruta"])), d["id"])
            else:
                self.assertEqual(d["ruta"], "", d["id"])
        self.assertEqual(sum(1 for r in rows if dict(zip(h, r))["troncal"] == "si"), ex.MIN_TRONCALES)
        guias = sorted(f for f in os.listdir(os.path.join(ex.REFS, "manual")) if f.endswith(".md"))
        self.assertEqual(len(guias), 6, guias)
        self.assertFalse(os.path.exists(os.path.join(ex.REFS, "manual", "indice_modulos.csv")))

    def test_troncales_con_encabezado_pedagogico(self):
        h, rows = ex.leer(os.path.join(ex.PLANTILLAS, "catalogo_plantillas.csv"))
        for r in rows:
            d = dict(zip(h, r))
            if d["troncal"] != "si":
                continue
            with open(os.path.join(ex.PLANTILLAS, d["ruta"]), encoding="utf-8") as fh:
                txt = fh.read()
            for campo in ("Para qué sirve", "Cuándo NO usarla", "Micro-ejemplo"):
                self.assertIn(campo, txt, f"{d['id']} sin «{campo}»")

    def test_biblioteca(self):
        code, out = correr(ex, "biblioteca", "Semilla", "--tipo", "fuentes", "--max", "2")
        self.assertEqual(code, 0)
        self.assertIn("CORFO", out)


class TestFinanzas(unittest.TestCase):
    def test_unit_economics(self):
        _, out = correr(finanzas, "unit", "--precio", "150000", "--costo-variable", "50000", "--cac", "300000", "--churn", "0.03")
        self.assertIn("$3.333.333", out)
        self.assertIn("LTV sobre ingreso", out)

    def test_contribucion_negativa(self):
        _, out = correr(finanzas, "unit", "--precio", "100", "--costo-variable", "200", "--cac", "10", "--churn", "0.05")
        self.assertIn("pierde plata", out)

    def test_equilibrio_redondea_arriba(self):
        _, out = correr(finanzas, "equilibrio", "--costos-fijos", "1000", "--precio", "300", "--costo-variable", "0")
        self.assertIn("4 clientes", out)

    def test_dilucion(self):
        _, out = correr(finanzas, "dilucion", "--fundadores", "A:50,B:50", "--pre", "800", "--inversion", "200")
        self.assertIn("20,0%", out)
        self.assertIn("40,0%", out)

    def test_costo_empleado(self):
        code, out = correr(finanzas, "costo-empleado", "--bruto", "1000000", "--uf", "40000", "--utm", "70000")
        self.assertEqual(code, 0, out)
        self.assertIn("Costo empresa mensual", out)
        self.assertNotIn("SIS (invalidez", out)

    def test_liquido_a_bruto_es_inverso(self):
        p = finanzas.params()

        class A:
            contrato, gratificacion, mutual_adicional, provision_indemnizacion = "indefinido", False, 0, False
        liq = finanzas.calcular_empleado(1200000, A, p, 40000, 70000)[4]
        _, out = correr(finanzas, "costo-empleado", "--liquido", str(round(liq)), "--uf", "40000", "--utm", "70000")
        self.assertIn("$1.200.000", out)

    def test_honorarios(self):
        _, out = correr(finanzas, "honorarios", "--bruto", "100000")
        self.assertIn("$15.250", out)


class TestFondos(ConExpediente):
    def test_elegibilidad_inicia(self):
        code, out = correr(fondos_lint, "elegibilidad", "--instrumento", "semilla_inicia", "--tipo", "juridica",
                           "--meses-inicio", "24", "--ventas-12m", "0")
        self.assertEqual(code, 1)
        self.assertIn("NO CUMPLE", out)

    def test_presupuesto_cofinanciamiento(self):
        correr(ex, "add", "rendiciones", "actividad=Dev", "resultado=MVP", "presupuesto_CLP=10000000",
               "subsidio_CLP=9000000", "aporte_CLP=1000000", "--dir", self.dir)
        code, out = correr(fondos_lint, "presupuesto", "--instrumento", "semilla_inicia", "--dir", self.dir)
        self.assertEqual(code, 1)
        self.assertIn("90.0%", out)

    def test_caracteres(self):
        p = os.path.join(self.dir, "r.md")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("## A [máx 10]\n" + "x" * 20 + "\n\n## B\n<!-- max: 100 -->\n" + "y" * 60 + "\n")
        code, out = correr(fondos_lint, "caracteres", p)
        self.assertEqual(code, 1)
        self.assertIn("EXCEDE por 10", out)


class TestIngesta(unittest.TestCase):
    def test_anonimiza(self):
        txt = ("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n<v Ana Pérez>Hola Luis\n\n"
               "00:00:03.000 --> 00:00:04.000\n<v Luis Soto>Mi mail es luis@x.cl, fono +56 9 1234 5678, RUT 12.345.678-5\n")
        anon, _ = ingesta.anonimizar(txt, entrevistador="Ana Pérez")
        for dato in ("luis@x.cl", "1234 5678", "12.345.678-5", "Luis", "Ana", "-->"):
            self.assertNotIn(dato, anon)
        self.assertIn("Entrevistado/a:", anon)


class TestModeloXlsx(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.x = os.path.join(self.dir, "m.xlsx")
        shutil.copy(os.path.join(SKILL, "assets", "modelo_financiero.xlsx"), self.x)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_set_por_etiqueta_y_proteccion_de_formulas(self):
        code, out = correr(modelo_xlsx, "set", self.x, "Precio mensual=250000")
        self.assertEqual(code, 0, out)
        vals = {f["variable"]: f["valor"] for f in modelo_xlsx.supuestos(self.x)}
        self.assertEqual(vals["Precio mensual"], "250000")
        code, out = correr(modelo_xlsx, "set", self.x, "Mercado!B5=1")
        self.assertNotEqual(code, 0)
        self.assertIn("fórmula", out)
        with zipfile.ZipFile(self.x) as z:
            self.assertIsNone(z.testzip())
            self.assertIn("fullCalcOnLoad", z.read("xl/workbook.xml").decode())
        code, out = correr(modelo_xlsx, "verificar", self.x)
        self.assertEqual(code, 0, out)

    def test_escenarios_desde_modelo(self):
        code, out = correr(finanzas, "escenarios", "--modelo", self.x)
        self.assertEqual(code, 0, out)
        self.assertIn("pesimista", out)


class TestFondosRendicionCoherencia(ConExpediente):
    def test_rendiciones_detecta_fecha_documento_y_sobrepago(self):
        correr(ex, "add", "rendiciones", "actividad=Dev", "resultado=MVP", "presupuesto_CLP=1000000", "comprometido_CLP=1000000",
               "pagado_CLP=1200000", "fecha=2027-08-01", "--dir", self.dir)
        correr(ex, "add", "rendiciones", "actividad=Piloto", "resultado=Informe", "presupuesto_CLP=500000", "pagado_CLP=500000",
               "documento=F-1", "medio_verificacion=transferencia", "fecha=2027-03-01", "--dir", self.dir)
        correr(ex, "add", "rendiciones", "actividad=Ventas", "resultado=OC", "presupuesto_CLP=500000", "pagado_CLP=100000",
               "documento=f-1", "medio_verificacion=transferencia", "fecha=2027-04-01", "--dir", self.dir)
        code, out = correr(fondos_lint, "rendiciones", "--dir", self.dir, "--inicio", "2027-02-01", "--fin", "2027-06-30")
        self.assertEqual(code, 1)
        self.assertIn("fuera del período", out)
        self.assertIn("pagado $1.200.000 > comprometido", out)
        self.assertIn("pagado sin documento", out)
        self.assertIn("repetido", out)

    def test_rendiciones_ok(self):
        correr(ex, "add", "rendiciones", "actividad=Dev", "resultado=MVP", "presupuesto_CLP=1000000", "pagado_CLP=0",
               "fecha=2027-03-01", "--dir", self.dir)
        code, out = correr(fondos_lint, "rendiciones", "--dir", self.dir, "--inicio", "2027-02-01", "--fin", "2027-06-30")
        self.assertEqual(code, 0, out)
        self.assertIn("OK", out)

    def test_coherencia_marco_y_presupuesto(self):
        correr(ex, "add", "rendiciones", "actividad=Desarrollo del módulo de reportes", "resultado=MVP", "presupuesto_CLP=1000000",
               "--dir", self.dir)
        correr(ex, "add", "rendiciones", "actividad=Compra de camioneta", "resultado=Logística", "presupuesto_CLP=9000000",
               "--dir", self.dir)
        marco = os.path.join(self.dir, "marco.md")
        with open(marco, "w", encoding="utf-8") as fh:
            fh.write("| Componente | Actividad | Indicador |\n|---|---|---|\n| C1 | Desarrollo del módulo de reportes | MVP |\n"
                     "| C2 | Prueba de usabilidad con 5 usuarios | Informe |\n")
        code, out = correr(fondos_lint, "coherencia", "--dir", self.dir, "--marco", marco)
        self.assertEqual(code, 1)
        self.assertIn("actividad sin presupuesto: 'Prueba de usabilidad", out)
        self.assertIn("no corresponde a una actividad", out)


class TestContinuidad(ConExpediente):
    def test_empaquetar_y_restaurar(self):
        correr(ex, "add", "hipotesis", "enunciado_refutable=Las clínicas pagan", "--dir", self.dir)
        salida = os.path.join(self.dir, "zips")
        code, out = correr(ex, "empaquetar", "--dir", self.dir, "--salida", salida)
        self.assertEqual(code, 0, out)
        z = [f for f in os.listdir(salida) if f.endswith(".zip")][0]
        nombres = zipfile.ZipFile(os.path.join(salida, z)).namelist()
        self.assertIn("expediente/00_estado.md", nombres)
        self.assertIn("LEEME.txt", nombres)
        otro = tempfile.mkdtemp()
        try:
            code, out = correr(ex, "restaurar", os.path.join(salida, z), "--dir", otro)
            self.assertEqual(code, 0, out)
            self.assertTrue(os.path.exists(os.path.join(otro, "expediente", "registros", "hipotesis.csv")))
            code, out = correr(ex, "restaurar", os.path.join(salida, z), "--dir", otro)
            self.assertEqual(code, 1)
            self.assertIn("--forzar", out)
            code, out = correr(ex, "restaurar", os.path.join(salida, z), "--dir", otro, "--forzar")
            self.assertEqual(code, 0, out)
            self.assertTrue(any(d.startswith("expediente.bak-") for d in os.listdir(otro)))
        finally:
            shutil.rmtree(otro, ignore_errors=True)

    def test_restaurar_rechaza_rutas_inseguras(self):
        malo = os.path.join(self.dir, "malo.zip")
        with zipfile.ZipFile(malo, "w") as z:
            z.writestr("expediente/../../fuera.txt", "x")
        otro = tempfile.mkdtemp()
        try:
            code, out = correr(ex, "restaurar", malo, "--dir", otro)
            self.assertEqual(code, 1)
            self.assertIn("insegura", out)
        finally:
            shutil.rmtree(otro, ignore_errors=True)

    def test_resumen_es_compacto(self):
        code, out = correr(ex, "resumen", "--dir", self.dir)
        self.assertEqual(code, 0, out)
        self.assertIn("Resumen para retomar", out)
        self.assertLess(len(out), 2700)

    def test_umbrales_por_track(self):
        code, out = correr(ex, "umbrales", "--gate", "G4", "--track", "hardware", "--dir", self.dir)
        self.assertEqual(code, 0, out)
        self.assertIn("BOM", out)
        code, out = correr(ex, "umbrales", "--gate", "G4", "--track", "saas_b2b", "--dir", self.dir)
        self.assertIn("LTV/CAC", out)
        self.assertNotIn("BOM", out)

    def test_doc_no_troncal_genera_esqueleto(self):
        code, out = correr(ex, "doc", "TPL-002", "--dir", self.dir)
        self.assertEqual(code, 0, out)
        self.assertIn("esqueleto", out)
        docs = os.listdir(os.path.join(self.dir, "expediente", "documentos"))
        self.assertTrue(any(d.startswith("TPL-002_") for d in docs))

    def test_deck_marca_faltantes(self):
        code, out = correr(ex, "informe", "deck", "--dir", self.dir)
        self.assertEqual(code, 0, out)
        deck = [f for f in os.listdir(os.path.join(self.dir, "expediente", "entregables")) if f.startswith("deck_")][0]
        texto = open(os.path.join(self.dir, "expediente", "entregables", deck), encoding="utf-8").read()
        self.assertIn("marp: true", texto)
        self.assertIn("[FALTA EVIDENCIA]", texto)

    def test_buscar_rankea_archivos(self):
        code, out = correr(ex, "buscar", "vesting cliff socios", "--max", "3")
        self.assertEqual(code, 0, out)
        titulos = [x for x in out.splitlines() if x.strip() and not x.startswith(" ")][:3]
        self.assertIn("socios_equity.md", "\n".join(titulos))


class TestAuditar(ConExpediente):
    def test_detecta_go_bajo_umbral_y_entrevistas_complacientes(self):
        import auditar
        correr(ex, "add", "hipotesis", "enunciado_refutable=Pagan 100 mil", "--dir", self.dir)
        correr(ex, "add", "experimentos", "hypothesis_id=H-001", "metrica=preventas", "umbral=30%", "resultado=12%",
               "decision=Go", "--dir", self.dir, "--forzar")
        for i in range(4):
            correr(ex, "add", "entrevistas", "segmento=clínicas", f"hecho_o_cita_breve=Me interesa mucho, lo compraría {i}",
                   "situacion=turnos", "--dir", self.dir, "--forzar")
        hs = auditar.auditar(self.dir)
        textos = " ".join(h[2] for h in hs)
        self.assertIn("bajo el umbral", textos)
        self.assertIn("ninguna un compromiso", textos)

    def test_expediente_demo_sin_alertas(self):
        import datetime as dt

        import auditar
        # fecha fija: la demo tiene fechas reales y con el tiempo sus experimentos "vencerían"
        hs = auditar.auditar(os.path.join(RAIZ, "examples", "expediente_demo"), hoy=dt.date(2026, 12, 15))
        self.assertFalse([h for h in hs if h[0] == "ALERTA"], hs)


class TestFinanzasCapital(unittest.TestCase):
    def test_safe_post_money_con_cap(self):
        _, out = correr(finanzas, "dilucion", "--fundadores", "A:50,B:50", "--safe", "100:1000")
        self.assertIn("10,0%", out)

    def test_safe_con_descuento_en_ronda(self):
        code, out = correr(finanzas, "dilucion", "--fundadores", "A:100", "--safe", "100:0:20", "--pre", "1000", "--inversion", "250")
        self.assertEqual(code, 0, out)
        self.assertIn("aplica: descuento 20%", out)
        self.assertIn("20,0%", out)  # el inversionista de la ronda: 250 / 1250 post

    def test_salida_con_preferencia_y_opciones(self):
        pago, precio = finanzas.reparto_salida(2e9, [("F", 8e6)], [("Seed", 1e9, 2e6)], [("Yo", 1e5, 200)])
        self.assertAlmostEqual(pago["Seed"], 1e9)
        self.assertAlmostEqual(precio, 125)
        self.assertEqual(pago["Yo"], 0)
        pago, precio = finanzas.reparto_salida(1e10, [("F", 8e6)], [("Seed", 1e9, 2e6)], [("Yo", 1e5, 200)])
        self.assertGreater(pago["Seed"], 1e9)  # convierte
        self.assertAlmostEqual(sum(pago.values()) + 1e5 * 200, 1e10 + 1e5 * 200, delta=1)


class TestIndicadores(unittest.TestCase):
    def test_respaldo_futuro_no_es_desactualizado(self):
        import datetime as dt
        import indicadores_cl
        hoy = dt.date(2026, 11, 25)
        self.assertIn("ya publicado", indicadores_cl.estado_respaldo("uf", "2026-11-30", hoy))
        self.assertIn("vigente este mes", indicadores_cl.estado_respaldo("utm", "2026-11-01", hoy))
        self.assertIn("desactualizado", indicadores_cl.estado_respaldo("uf", "2026-06-01", hoy))


class TestEvalsYMedicion(unittest.TestCase):
    def test_medir_respuesta(self):
        sys.path.insert(0, os.path.join(RAIZ, "tools"))
        import medir_respuesta as mr
        texto = "\n".join(["Hola. Tu idea es buena.", "", "¿Quién paga? ¿Cuánto??", "",
                           "> Hola, ¿tienes 15 minutos?", "", "```", "x = '¿y?'", "```", ""])
        self.assertEqual(mr.medir(texto), (8, 2))
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "r.md")
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(texto)
            self.assertEqual(mr.main([f, "--max-preguntas", "1"]), 1)
            self.assertEqual(mr.main([f, "--caso", "retomar-sin-campo"]), 0)

    def test_casos_de_eval_completos(self):
        evals = os.path.join(SKILL, "evals")
        with open(os.path.join(RAIZ, "tools", "limites_respuesta.json"), encoding="utf-8") as fh:
            lim = json.load(fh)
        for caso in sorted(os.listdir(evals)):
            d = os.path.join(evals, caso)
            if not os.path.isdir(d) or caso.startswith("_"):
                continue  # _bases/: expedientes compartidos por varios fixtures, no son casos
            with self.subTest(caso=caso):
                self.assertTrue(os.path.isfile(os.path.join(d, "prompt.md")))
                with open(os.path.join(d, "case.yaml"), encoding="utf-8") as fh:
                    y = fh.read()
                self.assertIn(f"name: {caso}", y)
                self.assertTrue(os.listdir(os.path.join(d, "graders")))
                if "scaffold_script" in y:
                    self.assertTrue(os.path.isfile(os.path.join(d, "place-files.sh")))
                    self.assertTrue(os.path.isdir(os.path.join(d, "files")) or os.path.isfile(os.path.join(d, "fixture.json")))
                self.assertIn(caso, lim, "agrega el caso a tools/limites_respuesta.json")


class TestCLI(unittest.TestCase):
    def test_todos_los_scripts_tienen_help(self):
        for f in sorted(os.listdir(SCRIPTS)):
            if f.endswith(".py"):
                r = subprocess.run([sys.executable, os.path.join(SCRIPTS, f), "--help"], capture_output=True,
                                   text=True, encoding="utf-8", timeout=60)
                self.assertEqual(r.returncode, 0, f + r.stderr)


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------------------------------------
# v2: onboarding, gates, fuentes, exportación, fondos, cap table, data room, parámetros, fixtures
# ---------------------------------------------------------------------------------------------
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import armar_fixture  # noqa: E402
import cap_table  # noqa: E402
import cohorte  # noqa: E402
import dataroom  # noqa: E402
import fondos_matcher  # noqa: E402
import presupuesto_corfo  # noqa: E402

EVALS = os.path.join(SKILL, "evals")
DEMO = os.path.join(RAIZ, "examples", "expediente_demo")


def hojas_xlsx(path):
    """Nombres de hoja de un .xlsx (y verifica que cada XML esté bien formado)."""
    import re
    import xml.etree.ElementTree as ET
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.endswith((".xml", ".rels")):
                ET.fromstring(z.read(n))
        wb = z.read("xl/workbook.xml").decode("utf-8")
    return re.findall(r'<(?:\w+:)?sheet [^>]*name="([^"]+)"', wb)


class TestOnboarding(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_tres_preguntas_crean_estado_gate_y_mision(self):
        code, out = correr(ex, "onboarding", "--dir", self.dir, "--proyecto", "Turnos",
                           "--problema", "Supervisoras pierden 2 días al mes armando turnos",
                           "--evidencia", "ninguna todavía", "--situacion", "persona natural, sin empresa",
                           "--objetivo", "Semilla Inicia 2027")
        self.assertEqual(code, 0, out)
        self.assertIn("Gate asignado: G0", out)
        self.assertIn("Misión de 7 días", out)
        txt = ex.leer_estado(self.dir)
        self.assertIn("ninguna todavía", txt)
        self.assertIn("## Misión de 7 días", txt)
        self.assertEqual(ex.gate_actual_de(self.dir), "G0")
        self.assertEqual(ex.validar(self.dir)[0], [])

    def test_evidencia_de_pago_sube_el_gate_y_no_sobrescribe(self):
        correr(ex, "onboarding", "--dir", self.dir, "--proyecto", "X", "--problema", "a",
               "--evidencia", "3 clientes pagando hace 4 meses", "--situacion", "SpA", "--objetivo", "ninguno")
        self.assertNotEqual(ex.gate_actual_de(self.dir), "G0")
        code, out = correr(ex, "onboarding", "--dir", self.dir, "--proyecto", "Y", "--problema", "b",
                           "--evidencia", "c", "--situacion", "d", "--objetivo", "e")
        self.assertEqual(code, 1)
        self.assertIn("no se sobrescribe", out)


class TestGateFuentesExportar(ConExpediente):
    def test_gate_lista_chequeos(self):
        code, out = correr(ex, "gate", "--gate", "G0", "--dir", self.dir)
        self.assertEqual(code, 0, out)
        self.assertIn("G0", out)
        self.assertIn("Chequeo", out)

    def test_buscar_fuente_por_tema(self):
        code, out = correr(ex, "buscar-fuente", "Semilla", "--tema", "publico", "--max", "3")
        self.assertEqual(code, 0, out)
        self.assertIn("CORFO", out)
        self.assertIn("publico_corfo", out)

    def test_bitacora_y_nombres_antiguos(self):
        code, out = correr(ex, "add", "riesgos", "riesgo=Sin cliente ancla", "responsable=Ana", "revision=2027-01-10",
                           "--dir", self.dir)
        self.assertEqual(code, 0, out)
        filas = ex.filas(self.dir, "riesgos")
        self.assertEqual(filas[0]["riesgo"], "Sin cliente ancla")
        bit = ex.filas(self.dir, "bitacora")
        self.assertEqual(bit[0]["tipo"], "riesgo")

    def test_exportar_xlsx_una_hoja_por_registro(self):
        correr(ex, "add", "hipotesis", "enunciado_refutable=Pagan 100 mil", "--dir", self.dir)
        code, out = correr(ex, "exportar", "todos", "--dir", self.dir, "--xlsx")
        self.assertEqual(code, 0, out)
        xl = [os.path.join(dp, f) for dp, _, fs in os.walk(self.dir) for f in fs if f.endswith(".xlsx")]
        self.assertTrue(xl, out)
        self.assertIn("hipotesis", hojas_xlsx(xl[0]))


class TestFondosV2(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_matcher_perfil_temprano(self):
        code, out = correr(fondos_matcher, "--tipo", "juridica", "--meses-inicio", "10", "--ventas-12m", "0", "--trl", "4")
        self.assertEqual(code, 0, out)
        fila = [x for x in out.splitlines() if "`semilla_inicia`" in x][0]
        self.assertIn("CALZA", fila)
        fila = [x for x in out.splitlines() if "`crea_y_valida`" in x][0]
        self.assertIn("NO CALZA", fila)

    def test_matcher_negocio_tradicional_va_a_sercotec(self):
        code, out = correr(fondos_matcher, "--tipo", "natural", "--meses-inicio", "0", "--ventas-12m", "0", "--tradicional")
        fila = [x for x in out.splitlines() if "`sercotec_semilla_emprende`" in x][0]
        self.assertNotIn("NO CALZA", fila)

    def test_presupuesto_detecta_trampas_del_eval(self):
        armar_fixture.armar(os.path.join(EVALS, "trampa-presupuesto-corfo"), self.dir)
        code, out = correr(presupuesto_corfo, "revisar", "--dir", self.dir, "--instrumento", "semilla_inicia")
        self.assertEqual(code, 1, out)
        self.assertIn("IVA", out)
        self.assertIn("PROBLEMA", out)
        socio = [x for x in out.splitlines() if "remuneración de socio" in x]
        self.assertTrue(socio and "PROBLEMA" in socio[0] and "$7.000.000" in socio[0], out)

    def test_presupuesto_tope_y_numero_de_socios(self):
        import datetime as dt
        from core import fondos
        with open(os.path.join(SKILL, "assets", "fondos", "instrumentos.json"), encoding="utf-8") as fh:
            inst = json.load(fh)["instrumentos"]["semilla_inicia"]
        fila = {"cuenta_presupuestaria": "Recursos humanos", "subsidio_CLP": "0", "aporte_CLP": "0"}
        filas = [dict(fila, gasto_id=f"GAS-00{i}", actividad="Sueldo socio", proveedor=quien, presupuesto_CLP=monto)
                 for i, (quien, monto) in enumerate([("Ana", "2800000"), ("Ana", "2800000"), ("Beto", "5000000"),
                                                     ("Carla", "1000000")], 1)]
        res, _, _ = fondos.revisar_presupuesto(filas, inst, dt.date(2027, 3, 1), dt.date(2027, 10, 31))
        textos = {e: [t for est, t in res if est == e] for e in ("OK", "PROBLEMA", "AVISO")}
        self.assertTrue(any("(ana; GAS-001, GAS-002) $5.600.000" in t and "8 meses" in t for t in textos["OK"]), res)
        self.assertTrue(any("(beto; GAS-003)" in t for t in textos["OK"]), res)
        self.assertTrue(any("3 socios" in t for t in textos["AVISO"]), res)
        filas[2]["presupuesto_CLP"] = "5700000"
        res, _, _ = fondos.revisar_presupuesto(filas, inst, dt.date(2027, 3, 1), dt.date(2027, 10, 31))
        self.assertTrue(any("(beto; GAS-003)" in t for est, t in res if est == "PROBLEMA"), res)

    def test_presupuesto_plantilla_buena_sin_problemas(self):
        import re
        with open(os.path.join(SKILL, "assets", "plantillas", "corfo", "TPL-105_presupuesto_y_rendicion.md"), encoding="utf-8") as fh:
            bloque = re.search(r"## Ejemplo bueno.*?```\n(.*?)```", fh.read(), re.S).group(1)
        csvp = os.path.join(self.dir, "r.csv")
        with open(csvp, "w", encoding="utf-8-sig") as fh:
            fh.write(bloque)
        code, out = correr(presupuesto_corfo, "revisar", "--csv", csvp, "--instrumento", "semilla_inicia",
                           "--inicio", "2027-03-01", "--fin", "2027-10-31", "--recupera-iva", "si")
        self.assertEqual(code, 0, out)
        self.assertIn("0 problema(s)", out)

    def test_ley_id_credito_y_tope(self):
        _, out = correr(finanzas, "ley-id", "--gasto", "100000000", "--utm", "70000")
        self.assertIn("$35.000.000", out)
        self.assertIn("$65.000.000", out)
        _, out = correr(finanzas, "ley-id", "--gasto", "5000000000", "--utm", "70000")
        self.assertIn("topado", out)
        self.assertIn("$1.050.000.000", out)


class TestCapTableYDataroom(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_cap_table_vesting_safe_y_ronda(self):
        os.makedirs(os.path.join(self.dir, "expediente", "documentos"))
        code, out = correr(cap_table, "init", "--dir", self.dir, "--fundadores", "Ana:60,Beto:40", "--pool", "10",
                           "--vesting", "48", "--cliff", "12", "--inicio-vesting", "2026-01-01")
        self.assertEqual(code, 0, out)
        self.assertIn("5.400.000", out)
        _, out = correr(cap_table, "ver", "--dir", self.dir, "--fecha", "2026-06-01")
        self.assertIn("| Ana | comun | 5.400.000 | 60,0% | 54,0% | 0 |", out)  # antes del cliff
        _, out = correr(cap_table, "ver", "--dir", self.dir, "--fecha", "2027-06-01")
        self.assertIn("1.912.500", out)  # 17/48 de 5,4 M
        code, out = correr(cap_table, "safe", "--dir", self.dir, "--titular", "Ángel", "--monto", "50000000",
                           "--cap", "1500000000")
        self.assertEqual(code, 0, out)
        code, out = correr(cap_table, "ronda", "--dir", self.dir, "--pre", "3000000000", "--inversion", "500000000")
        self.assertEqual(code, 0, out)
        self.assertIn("SAFE 1", out)
        self.assertIn("Inversionista ronda", out)

    def test_dataroom_revisa_y_arma_sin_entrevistas(self):
        dst = os.path.join(self.dir, "demo")
        shutil.copytree(DEMO, dst)
        code, out = correr(dataroom, "revisar", "--dir", dst)
        self.assertIn("1_societario", out)
        code, out = correr(dataroom, "armar", "--dir", dst, "--zip")
        self.assertEqual(code, 0, out)
        sala = os.path.join(dst, "expediente", "entregables", "dataroom")
        self.assertTrue(os.path.isfile(os.path.join(sala, "00_indice.md")))
        copiados = [f for _, _, fs in os.walk(sala) for f in fs]
        self.assertNotIn("entrevistas.csv", copiados)
        self.assertFalse([f for f in copiados if f.endswith("_anon.md")])


class TestIngestarYAuditar(ConExpediente):
    def test_nombres_por_contexto(self):
        anon, _ = ingesta.anonimizar("Hablé con la Sra. Pérez y después con Rodrigo Soto sobre los turnos.")
        self.assertNotIn("Pérez", anon)
        self.assertNotIn("Rodrigo Soto", anon)
        self.assertIn("[NOMBRE]", anon)

    def test_integridad_referencial(self):
        import auditar
        correr(ex, "add", "decisiones", "gate=G1", "decision=Go", "evidence_ids=EV-999", "justificacion=porque sí",
               "--dir", self.dir, "--forzar")
        notas = os.path.join(self.dir, "expediente", "investigacion", "notas")
        os.makedirs(notas, exist_ok=True)
        with open(os.path.join(notas, "ENT-001.md"), "w", encoding="utf-8") as fh:
            fh.write("Contacto: juana.perez@clinica.cl, +56 9 8765 4321\n")
        hs = auditar.auditar(self.dir)
        alertas = " ".join(h[2] for h in hs if h[0] == "ALERTA")
        self.assertIn("EV-999", alertas)
        self.assertIn("ENT-001.md", alertas)

    def test_demo_sin_alertas_con_fecha_fija(self):
        import datetime as dt

        import auditar
        hs = auditar.auditar(DEMO, hoy=dt.date(2026, 11, 25))
        self.assertFalse([h for h in hs if h[0] == "ALERTA"], hs)


class TestModeloYCohorte(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_modelo_tiene_hoja_de_fondos_y_monedas(self):
        modelo = os.path.join(SKILL, "assets", "modelo_financiero.xlsx")
        self.assertIn("Fondos_y_moneda", hojas_xlsx(modelo))
        c = modelo_xlsx.celdas(modelo, "Fondos_y_moneda")
        self.assertEqual(c["B4"]["valor"], "CLP")
        self.assertIn("Escenarios!", c["B12"]["formula"])
        self.assertEqual(c["D37"]["valor"], "OK")
        code, out = correr(modelo_xlsx, "verificar", modelo)
        self.assertEqual(code, 0, out)

    def test_cohorte_exporta_csv_y_xlsx(self):
        armar_fixture.armar(os.path.join(EVALS, "cohorte-incubadora-dos-equipos"), self.dir)
        xl, cs = os.path.join(self.dir, "c.xlsx"), os.path.join(self.dir, "c.csv")
        code, out = correr(cohorte, "--raiz", self.dir, "--xlsx", xl, "--csv", cs)
        self.assertEqual(code, 0, out)
        self.assertIn("TRL", out)
        hs = hojas_xlsx(xl)
        self.assertIn("Equipos", hs)
        self.assertIn("hipotesis", hs)
        with open(cs, encoding="utf-8-sig") as fh:
            self.assertIn(";", fh.readline())


class TestFixturesDeEvals(unittest.TestCase):
    def test_todos_los_fixtures_se_arman(self):
        for caso in sorted(os.listdir(EVALS)):
            d = os.path.join(EVALS, caso)
            if caso.startswith("_") or not os.path.isfile(os.path.join(d, "place-files.sh")):
                continue
            with self.subTest(caso=caso):
                with open(os.path.join(d, "place-files.sh"), encoding="utf-8") as fh:
                    self.assertIn("armar_fixture.py", fh.read())
                tmp = tempfile.mkdtemp()
                try:
                    armar_fixture.armar(d, tmp)
                    self.assertTrue(os.listdir(tmp))
                    conf = {}
                    if os.path.isfile(os.path.join(d, "fixture.json")):
                        with open(os.path.join(d, "fixture.json"), encoding="utf-8") as fh:
                            conf = json.load(fh)
                    for capa in conf.get("capas", []):
                        if capa["base"] in ("demo", "vacio") and not conf.get("empaquetar"):
                            base = os.path.join(tmp, capa.get("destino", "."))
                            self.assertEqual(ex.validar(base)[0], [], (caso, capa))
                    if conf.get("empaquetar"):
                        self.assertTrue(os.path.isfile(os.path.join(tmp, conf["empaquetar"]["salida"])))
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)


class TestComandos(unittest.TestCase):
    def test_atajos_del_plugin(self):
        for nombre in ("estado", "destrozar", "fondos", "entrevista", "numeros", "exportar"):
            with self.subTest(atajo=nombre):
                with open(os.path.join(RAIZ, "commands", nombre + ".md"), encoding="utf-8") as fh:
                    txt = fh.read()
                self.assertTrue(txt.startswith("---\ndescription:"))
                self.assertIn("startup-engineering-chile", txt)

    def test_skill_md_es_enrutador_liviano(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as fh:
            txt = fh.read()
        self.assertLess(txt.count("\n"), 350)
        self.assertLess(len(txt.split("---", 2)[2]), 6500)
        for clave in ("Express", "1-3-1", "onboarding", "/estado"):
            self.assertIn(clave, txt)
