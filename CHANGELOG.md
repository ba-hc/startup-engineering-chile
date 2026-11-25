# Cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versionado [SemVer](https://semver.org/lang/es/):

- **mayor:** cambios en el formato del expediente que exigen migrar a mano;
- **menor:** flujos, scripts o plantillas nuevas;
- **parche:** correcciones y actualización de cifras.

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
