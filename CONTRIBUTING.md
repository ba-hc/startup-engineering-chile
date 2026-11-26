# Cómo contribuir

Gracias por ayudar. Lo que más sirve es mantener las cifras y reglas al día y reportar casos que la skill maneja mal. Abre un [issue](https://github.com/ba-hc/startup-engineering-chile/issues) o un pull request.

## Antes de enviar
```powershell
python tools/check_refs.py
```
```powershell
python tools/validar_datos.py
```
```powershell
python -m unittest discover -s tests
```
La CI corre lo mismo en Ubuntu y Windows (Python 3.8 y 3.12), valida el expediente de ejemplo y pasa `ruff check skills/startup-engineering-chile/scripts tests tools`.

## Actualizar una cifra o una regla de fondo
Los datos que caducan viven en tres archivos, cada uno con su esquema en `tools/esquemas/`:

| Archivo | Qué guarda | Umbral de antigüedad |
|---|---|---|
| `assets/parametros_cl.json` | tasas, topes, tramos, UF/UTM de respaldo | 6 meses |
| `assets/fondos/instrumentos.json` | topes, cofinanciamiento y elegibilidad por instrumento | 3 meses |
| `assets/umbrales_gates.json` | umbrales por gate y tipo de startup | 12 meses |

1. Verifica el dato en la **fuente oficial** (ley en BCN, bases del llamado, SII, CORFO, ANID). Un blog o una noticia no basta.
2. Cambia el valor y su `fuente` (URL o norma). En `instrumentos.json`, deja en `verificar` lo que cambia en cada llamado.
3. Actualiza `_verificado` del archivo con la fecha de hoy (AAAA-MM-DD). `expediente.py doctor` y la revisión semanal leen esa fecha; no la escribas a mano en otros archivos.
4. Si el cambio afecta un flujo, actualiza su línea **Última verificación** y el texto.
5. Corre `python tools/validar_datos.py`.

## Fuentes de la biblioteca
Las fuentes están en cuatro archivos por tema (`references/biblioteca/fuentes_publico_corfo.csv`, `fuentes_mercado_latam.csv`, `fuentes_legal_tributario.csv` y `fuentes_saas_metricas.csv`), con `estado` y `fecha_reconsulta` por fila; `expediente.py buscar-fuente` busca en los cuatro. Marca una fila como verificada solo si leíste la página y confirmaste lo que la fila dice. Si el enlace está roto, reemplázalo o deja el estado como "URL rota (fecha)". El workflow semanal (`.github/workflows/mantencion.yml`) revisa los enlaces y abre un issue con lo que falle.

`mentores.csv` describe a personas reales: usa solo su rol profesional público y una URL que lo respalde. No agregues datos personales ni opiniones sobre ellas.

## Agregar o cambiar un flujo
- Un flujo responde a una situación del fundador ("me ofrecen un SAFE"), no a un tema.
- Abre con **Última verificación** si tiene cifras o normas, cita la fuente de cada dato y separa lo verificado de lo inferido.
- Lo legal, tributario o clínico es orientación educativa: indica qué profesional lo confirma.
- Menciónalo en el enrutador de `SKILL.md` (tabla o lista de «Otros temas»; `SKILL.md` debe seguir bajo ~5 KB, lo revisa `check_refs.py`) y en `references/mapa_modulos.md`.

## Plantillas
Las 40 troncales siguen el mismo formato: encabezado pedagógico (Para qué sirve, Cuándo NO usarla, Micro-ejemplo resuelto), Gate / Alimenta, Completar, Ejemplo bueno (ficticio), Ejemplo malo y por qué falla, Criterio de aceptación y Decisión. Los ejemplos son ficticios. Si una plantilla de catálogo merece ser troncal, márcala en `catalogo_plantillas.csv` y escríbela completa con ese formato.

## Scripts
- Solo biblioteca estándar de Python 3.8+, con cabecera PEP 723.
- Escrituras atómicas (archivo temporal + `os.replace`) y CSV con BOM.
- Mensajes de error en español que digan qué hacer.
- Cada comando nuevo lleva un test en `tests/test_scripts.py`.

## Casos de prueba
Sigue [`docs/evals.md`](docs/evals.md): carpeta en `evals/` con `prompt.md`, `case.yaml` y un criterio por archivo en `graders/`, más su fila en `tools/limites_respuesta.json`.

## CHANGELOG y versión
Anota el cambio en `CHANGELOG.md`. Si sube la versión, cámbiala en `.claude-plugin/plugin.json` y `pyproject.toml` (`check_refs.py` revisa que coincidan con el CHANGELOG).

Al contribuir aceptas publicar el código bajo MIT y el contenido bajo CC BY 4.0.
