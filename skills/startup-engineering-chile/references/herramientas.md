# Scripts de la skill

Todos usan solo la biblioteca estándar de Python 3.8+ (sin `pip install`). En Windows, si `python` falla, usa `py -3`. Ante cualquier error raro: `expediente.py doctor --dir <carpeta>`.

| Script | Para qué | Comandos clave |
|---|---|---|
| `expediente.py` | gestionar el expediente | `doctor` (incluye fecha de verificación de los datos), `init --nivel sprint/completo --track X`, `estado`, `add`, `ver`, `validar`, `migrar`, `doc` (troncal o esqueleto), `plantillas --troncales`, `biblioteca "texto"`, `buscar "texto" [--gate G3]` (búsqueda BM25 sin internet sobre manual, flujos, plantillas y catálogo), `umbrales [--gate G4]`, `resumen [--guardar]` (≈600 tokens para otra conversación), `empaquetar`/`restaurar` (ZIP del expediente), `exportar`, `informe semanal/onepager/deck`, `modelo` |
| `finanzas.py` | cálculos deterministas | `unit`, `equilibrio`, `runway`, `escenarios --modelo X.xlsx`, `dilucion` (SAFE con cap y descuento, pool shuffle), `salida` (waterfall: preferencia de liquidación, opciones), `costo-empleado`, `honorarios` |
| `auditar.py` | contradicciones y sesgos del expediente | `--dir RUTA [--dias-hipotesis 30] [--estricto]` |
| `modelo_xlsx.py` | editar `modelo_financiero.xlsx` sin romper fórmulas | `leer`, `set "Precio mensual=250000"`, `verificar` |
| `indicadores_cl.py` | UF, UTM, dólar, euro, IPC, IMACEC, TPM con caché y respaldo | `obtener`, `convertir 120 UF CLP` |
| `fondos_lint.py` | revisar una postulación antes de subirla | `instrumentos`, `elegibilidad`, `presupuesto`, `rendiciones`, `coherencia`, `caracteres` |
| `ingesta.py` | anonimizar notas y transcripciones | `anonimizar ARCHIVO --dir`, `revisar ARCHIVO` |
| `dashboard.py` | expediente → HTML autocontenido | `--dir RUTA` |
| `cohorte.py` | tablero de muchos equipos | `--raiz CARPETA [--html]` |
| `firecrawl.py` | opcional: archivar páginas si el usuario ya tiene Firecrawl local | `health`, `scrape`, `lote`, `competidor`, `map`, `search` |

## Reglas de uso
- **Registros**: siempre `expediente.py add`, nunca editar CSV a mano (escritura atómica, IDs, validación). Si un CSV se dañó, `validar` dice dónde y `migrar` repara encabezados vacíos o columnas faltantes (deja respaldo `.bak`).
- **Parámetros legales** (`assets/parametros_cl.json`) y **reglas de fondos** (`assets/fondos/instrumentos.json`) llevan fecha de verificación (`_verificado`); `expediente.py doctor` la muestra y avisa si venció. Si tiene más de 6 meses (fondos: 3), dilo al usuario y verifica antes de afirmar.
- **Indicadores**: si `indicadores_cl.py` no tiene red usa la caché o el respaldo con su fecha; en un presupuesto o postulación cita el valor y la fecha usados.
- **Excel**: `modelo_xlsx.py set` solo cambia supuestos (celdas sin fórmula), deja `.bak` y marca el libro para recalcular al abrir; para cifras inmediatas, `finanzas.py escenarios --modelo`.
- **Sin terminal**: haz el cálculo a mano mostrando fórmula y supuestos, y avisa que no se guardó nada.
- **Sin persistencia** (Claude.ai): `empaquetar` al cerrar y `restaurar` al empezar; ver `flujos/retomar.md`.

## Dependencias y pruebas
No hay dependencias externas. El repositorio trae pruebas (`python -m unittest discover -s tests`) y una verificación de integridad (`python tools/check_refs.py`) que corren en la CI.
