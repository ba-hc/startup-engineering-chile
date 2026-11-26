# Scripts, entregables y estructura del expediente

Todos los scripts usan solo la biblioteca estándar de Python 3.8+ (sin `pip install`). En Windows, si `python` falla o abre la Microsoft Store, usa `py -3` y entrecomilla rutas con espacios. Ante cualquier error raro: `expediente.py doctor --dir <carpeta>`. Cada script tiene `--help` con ejemplos.

## Qué script usar
| Script | Para qué | Comandos clave |
|---|---|---|
| `expediente.py` | gestionar el expediente (CLI delgada sobre `scripts/core/`) | `onboarding` (3 preguntas → estado, gate y misión de 7 días), `init`, `doctor`, `estado`, `gate [--gate G4]`, `add`, `ver`, `validar`, `migrar`, `id`, `doc TPL-0XX`, `plantillas --troncales`, `biblioteca`, `buscar-fuente "texto" [--tema publico\|mercado\|legal\|metodos]`, `buscar "texto"` (BM25 sin internet), `umbrales`, `resumen`, `empaquetar`/`restaurar`, `exportar [--xlsx]`, `informe semanal\|onepager\|deck`, `modelo` |
| `finanzas.py` | cálculos deterministas | `unit`, `equilibrio`, `runway`, `escenarios --modelo X.xlsx`, `dilucion` (SAFE con cap y descuento, pool), `salida` (waterfall), `costo-empleado`, `honorarios`, `ley-id --gasto` (crédito tributario I+D) |
| `fondos_matcher.py` | qué instrumentos calzan con el perfil (lee `00_estado.md` o flags) | `--dir RUTA [--tipo juridica --meses-inicio 10 --ventas-12m 0 --trl 4 --mujeres]` |
| `presupuesto_corfo.py` | revisar el presupuesto o la rendición de un fondo | `revisar --csv rendiciones.csv --instrumento semilla_inicia [--recupera-iva si]`, `tabla [--xlsx]` |
| `fondos_lint.py` | revisar una postulación antes de subirla | `instrumentos`, `elegibilidad`, `presupuesto`, `rendiciones`, `coherencia`, `caracteres` |
| `cap_table.py` | tabla de capitalización, vesting, SAFE y rondas | `init --fundadores "Ana:60,Beto:40"`, `emitir`, `safe`, `ver [--fecha]`, `ronda --pre --inversion`, `exportar [--xlsx]` |
| `dataroom.py` | sala de datos para inversionistas | `revisar` (checklist de 9 carpetas y cifras sin EV-), `armar [--zip]` |
| `auditar.py` | contradicciones, sesgos e integridad referencial | `--dir RUTA [--estricto]` |
| `ingestar.py` | anonimizar notas y transcripciones | `anonimizar ARCHIVO --dir RUTA [--nombres "…"]`, `revisar ARCHIVO` |
| `modelo_xlsx.py` | editar `modelo_financiero.xlsx` sin romper fórmulas | `leer`, `set "Precio mensual=250000"`, `verificar` |
| `indicadores_cl.py` | UF, UTM, dólar, IPC con caché y respaldo | `obtener`, `convertir 120 UF CLP` |
| `actualizar_parametros.py` | edad de los datos legales y respaldo de indicadores | `revisar`, `indicadores [--escribir]` |
| `dashboard.py` | expediente → HTML interactivo autocontenido | `--dir RUTA` |
| `cohorte.py` | tablero de varios equipos | `--raiz CARPETA [--html] [--csv] [--xlsx] [--estancado 14]` |
| `firecrawl.py` | conector opcional (ver abajo) | `health`, `scrape`, `competidor`, `lote`, `map` |

## Reglas de uso
- **Registros**: siempre `expediente.py add`, nunca editar CSV a mano (escritura atómica, IDs, validación). Riesgos, indicadores, lecciones y otros eventos van a la bitácora: `add bitacora tipo=riesgo titulo=… responsable=…` (los nombres antiguos, como `add riesgos`, siguen funcionando). Si un CSV se dañó, `validar` dice dónde y `migrar` lo repara (deja `.bak`).
- **Datos con fecha**: `assets/parametros_cl.json`, `assets/fondos/instrumentos.json` y `assets/umbrales_gates.json` llevan `_verificado`. `actualizar_parametros.py revisar` dice cuáles vencieron; si un dato decide algo, dilo y verifica en la fuente.
- **Indicadores**: sin red, `indicadores_cl.py` usa caché o respaldo con su fecha; en un presupuesto cita el valor y la fecha.
- **Excel**: `modelo_xlsx.py set` solo cambia supuestos, deja `.bak` y marca el libro para recalcular. La hoja `Fondos_y_moneda` muestra montos en CLP, UF o USD, el equilibrio y los meses de caja por escenario y el presupuesto del fondo con aporte pecuniario y valorado.
- **Sin terminal**: cálculo a mano mostrando fórmula y supuestos; avisa que no se guardó nada.
- **Sin persistencia** (Claude.ai): `empaquetar` al cerrar y `restaurar` al empezar (`flujos/retomar.md`).

## Entregables
Se generan **desde el expediente** en `expediente/entregables/`:
- `expediente.py informe onepager|semanal|deck` (deck: Markdown para Marp con cada vacío marcado `[FALTA EVIDENCIA]`).
- `dashboard.py`: HTML autocontenido con progreso por gate, runway, embudo de validación, misión y tablas filtrables (imprimible a PDF).
- `expediente.py exportar --xlsx`: un Excel con una hoja por registro; `dataroom.py armar`: carpeta para inversionistas.

Una afirmación sin respaldo se marca `[SIN RESPALDO]` o se quita: la presentación no crea evidencia. Antes de compartir, revisa que no lleve datos personales ni confidenciales.

## Plantillas
40 **troncales** en `assets/plantillas/`, cada una con encabezado pedagógico (para qué sirve, cuándo no usarla y un micro-ejemplo resuelto) (`expediente.py plantillas --troncales`). Las demás viven en el catálogo con su uso y criterio. `expediente.py doc TPL-0XX` copia una troncal o crea el esqueleto de las otras.

## Estructura del expediente (esquema v3)
```
expediente/
├── 00_estado.md      perfil, ruta por gates, misión de 7 días, números clave, acciones
├── manifest.json     versión del esquema, nivel y track (migrar la actualiza)
├── .gitignore        evita subirlo a git por accidente
├── registros/        8 tablas núcleo (hipotesis, evidencias, experimentos, decisiones, entrevistas,
│                     competencia, cuentas_y_pipeline, pilotos) + rendiciones + bitacora
├── documentos/       plantillas trabajadas
├── investigacion/    páginas con URL y fecha; notas/ con entrevistas anonimizadas (*_anon.md)
└── entregables/      one-pager, reporte semanal, deck, dashboard, modelo financiero, dataroom/
```
En modo Express no se crea nada de esto.

## Conector opcional: Firecrawl local
Firecrawl convierte páginas web en markdown limpio y corre en la máquina del usuario. **No es necesario**: sin él, usa la búsqueda y lectura web del cliente y guarda cada página con URL y fecha en `investigacion/`. No propongas instalarlo a un fundador no técnico (requiere Docker o Rust) salvo que lo pida. Otras fuentes con API pública: `references/conectores_y_apis.md`.

**Detectarlo**: `python scripts/firecrawl.py health --deep --guardar <proyecto>/expediente/.herramientas.json` (también lo revisa `expediente.py doctor`). Código 2 = no responde: sigue con las herramientas web del agente. URL distinta de `http://localhost:3002`: `FIRECRAWL_API_URL`; con clave: `FIRECRAWL_API_KEY` (la nube de Firecrawl saca los datos del computador: avísalo).

**Instalar** (solo si lo pide; confirma antes de cada comando que instala software; los pasos cambian entre versiones, revisa https://docs.firecrawl.dev/contributing/self-host):
- Docker Compose: `git clone https://github.com/firecrawl/firecrawl.git`, un `.env` con `USE_DB_AUTHENTICATION=false` y credenciales de Postgres, `docker compose up --build -d`, luego `firecrawl.py health --deep` y un `scrape https://example.com` de prueba.
- Sin Docker: `cargo install firecrawl-local` y `firecrawl-local serve` (`FIRECRAWL_CLOUD=off` para que nada salga a la nube).
- MCP: `npx -y firecrawl-mcp` con `FIRECRAWL_API_URL=http://localhost:3002`.

**Usar** (siempre con `--out` dentro del expediente; cada archivo lleva URL y fecha):
| Objetivo | Comando |
|---|---|
| Ficha de un competidor (precios, producto, clientes) | `firecrawl.py competidor https://competidor.cl --nombre "X" --out expediente/investigacion/competencia` |
| Varios competidores | `firecrawl.py lote competidores.txt --out …` (una línea `Nombre \| https://url`) |
| Bases de un fondo en PDF | `firecrawl.py scrape https://…/bases.pdf --timeout 180 --out expediente/investigacion/fuentes` |
| Estructura de un sitio | `firecrawl.py map https://sitio.cl --search precios` |

`competidor` guarda instantáneas por fecha y escribe `cambios.md` con las diferencias de precio respecto de la consulta anterior.

**Uso responsable**: solo páginas públicas; nada de logins, muros de pago ni CAPTCHAs; sin datos personales de empleados; crawls chicos (límite 20 páginas). Lo que dice un sitio es **declaración del competidor**: regístralo así en evidencias.

## Dependencias y pruebas
Sin dependencias externas. Pruebas: `python -m unittest discover -s tests`; integridad de referencias y enlaces: `python tools/check_refs.py`; esquemas de datos: `python tools/validar_datos.py`. Corren en la CI.
