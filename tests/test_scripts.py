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
import ingesta  # noqa: E402
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
        self.assertEqual(sum(1 for r in rows if dict(zip(h, r))["troncal"] == "si"), 25)
        h, rows = ex.leer(os.path.join(ex.REFS, "manual", "indice_modulos.csv"))
        for r in rows:
            self.assertTrue(os.path.exists(os.path.join(ex.REFS, "manual", dict(zip(h, r))["archivo"])))

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
        self.assertIn("socios_equity.md", out.splitlines()[0])


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
        import auditar
        hs = auditar.auditar(os.path.join(RAIZ, "examples", "expediente_demo"))
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
            if not os.path.isdir(d):
                continue
            with self.subTest(caso=caso):
                self.assertTrue(os.path.isfile(os.path.join(d, "prompt.md")))
                with open(os.path.join(d, "case.yaml"), encoding="utf-8") as fh:
                    y = fh.read()
                self.assertIn(f"name: {caso}", y)
                self.assertTrue(os.listdir(os.path.join(d, "graders")))
                if "scaffold_script" in y:
                    self.assertTrue(os.path.isdir(os.path.join(d, "files")))
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
