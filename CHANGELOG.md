# Cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versionado [SemVer](https://semver.org/lang/es/):

- **mayor:** cambios en el formato del expediente que exigen migrar a mano;
- **menor:** flujos, scripts o plantillas nuevas;
- **parche:** correcciones y actualización de cifras.

## [2.0.0] - 2026-11-25

Versión mayor: el expediente pasa al esquema v3. `expediente.py migrar` convierte uno v1/v2 sin perder datos (deja respaldo `.bak`) y los nombres antiguos de registros siguen funcionando en `add`, `ver` y los scripts.

### Agregado
- **Modos Express y Expediente.** Una consulta puntual o exploratoria se responde sin crear archivos; el expediente se crea solo si el usuario quiere guardar el proyecto.
- **Onboarding de 3 preguntas** (`expediente.py onboarding`): problema, evidencia de calle y situación societaria/objetivo de financiamiento → `00_estado.md`, gate inferido y **misión de 7 días** con criterio de éxito. No sobrescribe un expediente existente.
- **Formato de respuesta 1-3-1** (un diagnóstico, hasta tres hallazgos/opciones/preguntas, un próximo paso).
- **Atajos** en `commands/`: `/estado`, `/destrozar`, `/fondos`, `/entrevista`, `/numeros`, `/exportar`.
- **Scripts:**
  - `fondos_matcher.py`: calce de todos los instrumentos con el perfil (tipo de persona, meses de inicio, ventas, TRL, mujeres, negocio tradicional);
  - `presupuesto_corfo.py`: revisa presupuesto y rendición (tope, cofinanciamiento, aporte pecuniario mínimo, IVA recuperable, fechas fuera del convenio, plazo del instrumento, RR.HH., pagos a socios con el tope de $700.000 mensuales y máximo 2 personas en Semilla Inicia, ítems no financiables) y arma la tabla por cuenta en Excel;
  - `cap_table.py`: cap table con vesting y cliff, SAFE, emisiones, ronda y export a Excel;
  - `dataroom.py`: checklist de 9 carpetas, cifras del pitch sin EV- y paquete sin datos personales;
  - `actualizar_parametros.py`: antigüedad de los datos legales y actualización de UF/UTM de respaldo;
  - `finanzas.py ley-id`: crédito tributario de la Ley 20.241 (35%, tope 15.000 UTM, 65% deducible, remanente, arancel);
  - `expediente.py gate` (chequeos deterministas por gate desde `umbrales_gates.json`), `buscar-fuente`, `id` y `exportar --xlsx`.
- **Modelo financiero:** hoja `Fondos_y_moneda` con selector CLP/UF/USD, equilibrio y meses de caja en los 3 escenarios, presupuesto del fondo con aporte pecuniario y valorado y chequeos de tasa, tope, aporte mínimo, RR.HH. y administración.
- **Referencias:** `glosario_sin_humo.md`, `conectores_y_apis.md` y los flujos `ley_id.md`, `sercotec_vs_corfo.md`, `prochile_aterrizaje.md`, `flip_societario.md` y `fintech_cmf.md`; 31 fuentes legales verificadas nuevas.
- **Evals:** 5 casos nuevos (29 en total): modo Express sin archivos, red team, flip prematuro, Ley 21.719 y derivación a Sercotec.
- `tools/armar_fixture.py`: arma los fixtures de los evals desde el demo, una base vacía o una base compartida, más las diferencias de cada caso.

### Cambiado
- **`SKILL.md`** es un enrutador de ~5 KB (antes 14 KB). El detalle de conversación, primer turno y onboarding pasa a `references/diagnostico.md`; scripts, entregables y estructura a `references/herramientas.md`. `check_refs.py` controla el tamaño.
- **`expediente.py`** se dividió en `scripts/core/` (`storage`, `schemas`, `registros`, `estado`, `gates`, `exporters`, `busqueda`, `plantillas`) y queda como CLI delgada. El bloqueo del expediente es reentrante.
- **Registros:** de 17 CSV a 8 tablas núcleo (hipótesis, evidencias, experimentos, decisiones, entrevistas, competencia, cuentas y pipeline, pilotos) + `rendiciones` (con `tipo_aporte` e `iva_incluido`) + `bitacora` (riesgos, KPI, fuentes, lecciones, desafíos, PI, requisitos de fondos, cohortes y notas).
- **Manual:** 28 archivos y un índice duplicado pasan a 6 guías por etapa (G0, G1–G2, G3–G4, G5–G6, G7–G9 y transversal).
- **Biblioteca:** `fuentes.csv` se partió en 4 archivos por tema (público/CORFO, mercado LATAM, legal-tributario, SaaS y métricas).
- **Plantillas:** 40 troncales (antes 25), cada una con encabezado pedagógico (para qué sirve, cuándo no usarla, micro-ejemplo resuelto). TPL-105 usa las columnas nuevas de rendiciones.
- **`auditar.py`:** integridad referencial (decisiones que citan evidencia inexistente, Kill/Hold/Recycle sin evidencia, experimentos vencidos sin decisión o sin resultado, notas y entrevistas con datos personales) y cifras de `00_estado.md` contra el modelo.
- **Dashboard** interactivo: progreso G0–G9 con detalle de chequeos, semáforo de runway, embudo de validación y comercial, misión, filtro y tablas ordenables; sigue siendo un solo HTML sin dependencias.
- **`cohorte.py`:** alerta de estancamiento (más de 14 días sin actividad), días en el gate, misión vencida, matriz TRL × CRL y export `--csv`/`--xlsx` consolidado.
- **`ingesta.py` → `ingestar.py`**, que además detecta nombres por contexto ("la Sra. Pérez", "hablé con Rodrigo Soto").
- **Normativa:** `privacidad.md` (Ley 21.719 vigente desde el 15-10-2027 por la Ley 21.855), `compras_publicas.md` (Compra Ágil y Contratos para la Innovación), guía CORFO con fichas de Semilla Inicia y ANID Startup CTCI 2027, `instrumentos.json` con plazo, prórroga, tipo de aporte, TRL y variante mujeres verificados, y Ley I+D en `parametros_cl.json`.
- **Firecrawl** deja de ser una guía aparte y queda como conector opcional en `references/herramientas.md`.
- **Mantención:** la CI revisa enlaces Markdown internos y valida los JSON contra sus esquemas; el workflow de mantención revisa enlaces y vigencia cada semana y una vez al mes abre un PR con los indicadores de respaldo.

### Eliminado
- `docs/proceso/` (proceso de construcción del pack): se conserva en la rama `dev/proceso`, fuera del paquete distribuible.
- Copias duplicadas del expediente, del modelo y del ZIP en los evals (ahora se generan al vuelo).
- `references/firecrawl.md`, `references/manual/indice_modulos.csv` y los 28 módulos sueltos del manual.

## [1.2.0] - 2026-11-25

### Agregado
- **8 flujos nuevos** en `references/flujos/`, con fecha de verificación y fuentes:
  - `capital_privado.md`: ángeles, aceleradoras, SAFE y nota convertible en Chile, term sheet y VC;
  - `sumarse_a_startup.md`: evaluar una oferta de opciones o equity;
  - `pivote_y_cierre.md`: pivote, pausa o cierre; obligaciones con un proyecto CORFO vigente (BAG), trabajadores, término de giro y Ley 20.720;
  - `venta_corporativa.md`: registros de proveedores (SICEP, REGIC, Ariba), piloto pagado y pago a 30 días;
  - `caja_y_cobro.md`: IVA y caja, medios de pago y cobro recurrente;
  - `ebct_transferencia.md`: spin-offs universitarias, TRL, licencias e instrumentos ANID;
  - `verticales_reguladas.md`: salud (dispositivo médico, datos de pacientes, telemedicina) y puntos de control de otras verticales;
  - `mvp_e_ia.md`: validar un producto con IA, costo de inferencia y Ley Fintec.
- **Plan de opciones (ESOP)** en `socios_equity.md`.
- **Umbrales por gate y tipo de startup** (`assets/umbrales_gates.json`, `expediente.py umbrales`, `init --track`) y `references/ejemplos_y_umbrales.md` con decisiones de gate bien y mal tomadas.
- **`auditar.py`:** contradicciones y sesgos del expediente (Go sin evidencia, resultados bajo el umbral, experimentos vencidos, hipótesis estancadas, costo hundido, entrevistas complacientes, feature creep, precio contra pipeline).
- **Continuidad fuera de Claude Code:** `expediente.py empaquetar` (ZIP descargable), `restaurar` (con protección contra rutas maliciosas y respaldo) y `resumen` (~600 tokens para otra conversación o modelo). `SKILL.md` y `retomar.md` los usan al cerrar y al empezar.
- **`expediente.py buscar`** con ranking BM25 sin internet sobre manual, flujos, plantillas y catálogo (`--gate`).
- **`expediente.py informe deck`:** borrador de pitch en Markdown (Marp) que marca cada vacío como [FALTA EVIDENCIA].
- **`finanzas.py`:** SAFE con descuento (`MONTO:CAP:DESC%`), aumento de pool antes de la ronda, y `salida` para el reparto en una venta con preferencia de liquidación no participativa y opciones.
- **Mantenimiento:**
  - `tools/validar_datos.py` y esquemas JSON (`tools/esquemas/`) para instrumentos, parámetros y umbrales, en la CI;
  - `tools/revisar_enlaces.py` y `tools/revisar_vigencia.py`, y un workflow semanal que abre un issue si algo venció o se rompió;
  - `expediente.py doctor` muestra la fecha de verificación de cada archivo de datos y avisa si venció.
- **Evals:** 13 casos nuevos (24 en total): socios, capital privado, compras públicas, internacionalización, red team, antisesgo, privacidad, cohorte, persistencia con ZIP, multi-turno simulado y 3 activaciones negativas más. `tools/medir_respuesta.py` mide palabras y preguntas contra `tools/limites_respuesta.json`. Guía en `docs/evals.md`.
- `CONTRIBUTING.md`.

### Cambiado
- **Plantillas:** quedan 25 troncales reescritas, cada una con estructura propia, un ejemplo bueno, uno malo y su criterio de aceptación. Las otras 83 viven solo en el catálogo y `expediente.py doc` genera su esqueleto.
- **Manual:** sin el "Propósito" genérico ni las secciones repetidas; cada capítulo abre con cuándo usarlo, su gate y sus plantillas (de 73 KB a 52 KB).
- **`SKILL.md`:** descripción reescrita con frases que diría el usuario (982 caracteres); el principio 6 remite a la fecha `_verificado` de los datos en vez de una fecha escrita a mano; enrutador con los flujos nuevos; Firecrawl queda como opción para quien ya lo tiene.
- **Evals:** los límites de palabras y preguntas salen de los graders LLM y pasan al script.
- **`mentores.csv`:** columnas `estado` y `fecha_consulta` por fila; `biblioteca` recuerda que los perfiles no están reverificados.
- **`instrumentos.json`:** cofinanciamiento de Start-Up Chile Build (90%) e Ignite (80%), nuevo `startup_chile_growth` y nota de TRL en ANID Startup CTCI.
- Prefijo de evidencias unificado como `EV-` en plantillas y referencias.

### Corregido
- El respaldo de UF con fecha futura (ya publicada) ya no aparece como "desactualizado".
- `fondos_lint.py coherencia` encuentra el marco lógico también relativo a `--dir`.
- Tres enlaces rotos de la biblioteca y de `parametros_cl.json`.
- Tests para `fondos_lint.py rendiciones` y `coherencia`.

### Fuera de alcance (por ahora)
- Asesoría tributaria (elección de régimen) y datos de mercado del SII: requieren un profesional o datos que no se pueden verificar sin conexión.
- Sincronización con CRM o calendario, servidor MCP, asistente de instalación, empaquetado para otros clientes y separación por país.

## [1.1.0] - 2026-11-25

### Agregado
- **Scripts nuevos**, todos solo con biblioteca estándar y cabecera PEP 723:
  - `finanzas.py`: unit economics, punto de equilibrio, runway, escenarios desde el modelo, dilución con SAFE y pool, costo empleado y boletas de honorarios con parámetros chilenos 2026.
  - `indicadores_cl.py`: UF, UTM, dólar y euro desde mindicador.cl, con caché y respaldo.
  - `modelo_xlsx.py`: lee y edita los supuestos del modelo financiero sin tocar las fórmulas.
  - `fondos_lint.py`: elegibilidad por instrumento, presupuesto, rendiciones, coherencia con el marco lógico y límites de caracteres.
  - `ingesta.py`: anonimiza transcripciones (.txt, .vtt, .srt) antes de guardarlas.
  - `dashboard.py`: tablero HTML autocontenido del expediente.
  - `cohorte.py`: tablero para incubadoras y cursos que siguen varios equipos.
- **`expediente.py`:**
  - `doctor` revisa el entorno;
  - `validar` revisa columnas, IDs, claves foráneas, fechas, decisiones y datos personales;
  - `migrar` actualiza expedientes antiguos;
  - `init --nivel sprint|completo`;
  - `informe semanal|onepager`, `modelo`, `buscar`;
  - filtros en `plantillas` y `biblioteca`.
- **Esquema del expediente versionado** (`manifest.json` con `schema_version` 2). Escrituras atómicas y CSV con BOM para Excel.
- **Privacidad:**
  - aviso si una fila parece contener correo, teléfono o RUT;
  - `.gitignore` dentro del expediente;
  - flujo `privacidad.md` con la Ley 19.628 vigente y la Ley 21.719 (vigencia 15-oct-2027).
- **Flujos en `references/flujos/`:** retomar (con vuelco semanal), ciclo de bloque, finanzas, router de fondos no dilutivos, red team con tres evaluadores, compuerta antisesgo, compras públicas, socios / equity / vesting, trampas chilenas, internacionalización, privacidad y modo cohorte.
- **Tres niveles de profundidad** (consulta, sprint, completo) y modo degradado sin terminal o sin internet.
- **Datos versionados:**
  - `assets/parametros_cl.json`: tasas, topes y tramos con fecha de verificación;
  - `assets/fondos/instrumentos.json`: reglas de 9 instrumentos.
- **25 plantillas troncales** marcadas en el catálogo (`plantillas --troncales`).
- **Receta R7** de investigación web: Mercado Público, INAPI y convocatorias.
- **Expediente de demostración** ficticio en `examples/expediente_demo/`.
- **4 casos de prueba nuevos:** unit economics inflados, coherencia de presupuesto CORFO, expediente dañado y activación negativa.
- **Calidad del repositorio:**
  - tests (`tests/`);
  - verificador de referencias (`tools/check_refs.py`);
  - CI en GitHub Actions (Ubuntu y Windows, Python 3.8 y 3.12);
  - este CHANGELOG.

### Cambiado
- `SKILL.md` reescrito como enrutador: 11,6 KB, antes 15,5 KB. El detalle pasa a los flujos.
- Nombres de archivo sin tildes ni eñes (5 plantillas y 22 capítulos del manual).
- Las guías CORFO llevan fecha de última verificación. Se actualizaron Crea y Valida, ANID, Ley I+D y Start-Up Chile.
- Firecrawl documentado como opcional: una instancia local no necesita clave.

### Corregido
- En 1.0.0 no se habían publicado los expedientes de prueba de los casos `retomar-*`: el `.gitignore` excluía cualquier carpeta `expediente/`. Ahora solo excluye la de la raíz.

### Eliminado
- Catálogos duplicados en Markdown (`FUENTES.md`, `LIBROS.md`, `MENTORES.md`, `CHARLAS_Y_CURSOS.md`, `CASOS.md`, `INDICE.md`, `02_workshops.md`, `fuentes.json`): los CSV son la única fuente.
- Documentos internos del proceso: se movieron a `docs/proceso/` y ya no van en el ZIP.

## [1.0.0] - 2026-11-25

### Agregado
- Primera versión pública de la skill:
  - 28 módulos del manual;
  - 108 plantillas;
  - 17 registros;
  - guía CORFO;
  - biblioteca de 268 fuentes;
  - casos y plan de 90 días.
- `expediente.py` y `firecrawl.py`.
- Instalación como plugin de Claude Code y como ZIP para Claude.ai.
- 6 casos de prueba.

[1.1.0]: https://github.com/ba-hc/startup-engineering-chile/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ba-hc/startup-engineering-chile/releases/tag/v1.0.0
