# Transversal · Legal, riesgo, fondos y gestión

> Lo que acompaña a todos los gates: legalidad y PI, impacto, riesgo y gobernanza, fondos públicos y ritmo de gestión. Guía consolidada del manual: un archivo por etapa en vez de un capítulo por archivo. Índice general, criterios de los gates y taxonomía de evidencia: `references/mapa_modulos.md`.

## Contenido
- [Módulo 21 · Legalidad, propiedad intelectual y seguridad](#módulo-21--legalidad-propiedad-intelectual-y-seguridad)
- [Módulo 22 · Impacto, sostenibilidad y ética](#módulo-22--impacto-sostenibilidad-y-ética)
- [Módulo 23 · Madurez, riesgo y gobernanza de innovación](#módulo-23--madurez-riesgo-y-gobernanza-de-innovación)
- [Módulo 25 · Financiamiento público y formulación](#módulo-25--financiamiento-público-y-formulación)
- [Módulo 28 · Gestión continua y aprendizaje](#módulo-28--gestión-continua-y-aprendizaje)

## Módulo 21 · Legalidad, propiedad intelectual y seguridad

**Úsalo cuando:** Contratos, licencias, datos personales · **Gate:** transversal · **Plantillas:** TPL-096, 097 (troncales en `assets/plantillas/catalogo_plantillas.csv`)

#### Métodos de referencia
WIPO IP; INAPI; NIST CSF; régimen chileno; contratos.

#### Procedimiento operativo
1. Identificar titulares de código, modelos, datos, marca, contratos y licencias (incluido open source).
2. Revisar derechos de explotación universitaria/laboral/cliente.
3. Elegir marca, secreto, derechos, patente cuando proceda.
4. Definir contratos, condiciones, DPA, confidencialidad, SLA y responsabilidad según sector.
5. Inventariar datos, finalidad, acceso, retención, proveedores, incidentes y recuperación.
6. Consultar normativa y experto para actividades reguladas.
7. Ley 21.855 cambió vigencia principal de Ley 21.719 al 15 oct 2027; no suspender cumplimiento actual.

#### Entregables
Inventario IP; matriz legal; Security Overview; riesgos.

#### Criterio de salida
Los activos y licencias tienen titular; riesgos legales bloqueantes y responsabilidades identificados; controles demostrables.

#### Errores y alertas
Usar datos sin derecho; asumir software no regulado por defecto; afirmar certificaciones inexistentes; entregar código sin acuerdo.

#### Fuentes y materiales
- [METODO-061 · WIPO IP Strategy Checklist](https://www.wipo.int/en/web/business/checklist)
- [CHILE-022 · INAPI](https://www.inapi.cl/)
- [CHILE-024 · Ley 21.719 protección de datos](https://www.bcn.cl/leychile/navegar?i=1209272)
- [CHILE-025 · Ley 21.855 — publicada 23 nov 2026](https://www.bcn.cl/leychile/navegar?idNorma=1230520&idVersion=2026-11-23)
- [METODO-062 · NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Módulo 22 · Impacto, sostenibilidad y ética

**Úsalo cuando:** Criterio sostenibilidad CORFO, teoría de cambio · **Gate:** transversal · **Plantillas:** TPL-098 (troncales en `assets/plantillas/catalogo_plantillas.csv`)

#### Métodos de referencia
Theory of Change; Nesta; marco lógico; evaluación de impacto; ODS.

#### Procedimiento operativo
1. Definir recursos, actividades, resultados, efectos y supuestos de causalidad.
2. Identificar impactos positivos y negativos, materiales para la actividad.
3. Priorizar por severidad/probabilidad, asignar acción, responsable y plazo.
4. Medir línea base, indicador, fuente y frecuencia.
5. Diferenciar actividad, resultado e impacto; evitar convertir correlación en causalidad.
6. En IA considerar energía, calidad, sesgos, seguridad y privacidad.
7. Elegir ODS pertinentes sin hacer greenwashing.

#### Entregables
Mapa impactos; indicadores; plan acción; evaluación.

#### Criterio de salida
El plan contiene indicadores y medios de verificación, resultados razonables y riesgos mitigados.

#### Errores y alertas
Afirmar carbono neutro sin medición; seleccionar ODS por decoración; considerar horas de taller como impacto; omitir efectos adversos.

#### Fuentes y materiales
- [METODO-047 · Standards of Evidence](https://www.nesta.org.uk/)
- [METODO-045 · DIY Toolkit](https://www.nesta.org.uk/toolkit/diy-toolkit/)
- [METODO-068 · CEPAL](https://repositorio.cepal.org/)
- [METODO-067 · World Bank — publicaciones](https://openknowledge.worldbank.org/)
- [CORFO-025 · Manual FIA–Gearbox](https://rebrota.fia.cl/wp-content/uploads/2025/06/Guia_metodologica_formulacion_de_proyectos.pdf)

## Módulo 23 · Madurez, riesgo y gobernanza de innovación

**Úsalo cuando:** TRL/IRL, riesgos, pre-mortem, decisión go/kill · **Gate:** todos · **Plantillas:** TPL-046, 069, 094, 095, 099 (troncales en `assets/plantillas/catalogo_plantillas.csv`)

#### Métodos de referencia
TRL; KTH IRL; DOE ARL; ISO 56000; Stage-Gate; pre-mortem.

#### Procedimiento operativo
1. Evaluar madurez por dimensión independiente.
2. TRL 1–9 describe desarrollo desde principios hasta operación probada según marco aplicable; adjuntar evidencia.
3. KTH IRL: cliente, tecnología, negocio, equipo, IP, financiamiento.
4. ARL: propuesta de valor, aceptación, recursos, licencia para operar.
5. Hacer pre-mortem, asignar probabilidad/impacto, señales tempranas, mitigación y responsable.
6. Usar gates con decisiones Go/Hold/Recycle/Kill y presupuesto incremental.
7. Gestionar incertidumbre, no solo avance de tareas.

#### Entregables
Readiness report; risk register; portafolio; decisión.

#### Criterio de salida
Cada puntuación se justifica; los bloqueos críticos no se promedian; el siguiente gasto elimina una brecha.

#### Errores y alertas
Inflar TRL por demo; mezclar IRL de KTH y Steve Blank; aplicar rúbricas internas como oficiales; certificar ISO sin auditoría.

#### Fuentes y materiales
- [METODO-048 · KTH Innovation Readiness Levels](https://kthinnovationreadinesslevel.com/)
- [METODO-049 · Adoption Readiness Levels](https://www.energy.gov/technologycommercialization/adoption-readiness-levels-arl-framework)
- [CHILE-035 · Calculadora IRL Chile](https://www.calculadorairl.cl/)
- [METODO-056 · Stage-Gate](https://www.stage-gate.com/)
- [METODO-059 · ISO/TC 279](https://www.iso.org/committee/4587737.html)

## Módulo 25 · Financiamiento público y formulación

**Úsalo cuando:** Postular a CORFO/ANID/Start-Up Chile · **Gate:** CORFO · **Plantillas:** TPL-103–108 (troncales en `assets/plantillas/catalogo_plantillas.csv`)

#### Métodos de referencia
CORFO; ANID; FIA–Gearbox; marco lógico; Five Case Model.

#### Procedimiento operativo
1. Determinar etapa, ventas, constitución, territorio, innovación e incompatibilidades.
2. Versionar bases, focalización, formulario, FAQ, convenio y manual rendición.
3. Separar negocio de intervención financiable; justificar adicionalidad, objetivos, actividades, recursos, indicadores, medios de verificación y riesgos.
4. Probar coherencia con caja y aportes.
5. Red team por criterio y admisibilidad.
6. No inventar cartas ni comprometer resultados desproporcionados.

#### Entregables
Funding Dossier; bases; matriz elegibilidad; objetivos/hitos.

#### Criterio de salida
Cada requisito tiene estado y evidencia, presupuesto reconciliado y cronograma; envío dentro de plazo por canal oficial.

#### Errores y alertas
Postular a fondo incorrecto; confundir carta de intención con factura; no leer focalización; asumir subsidio sin aporte o aprobación de gastos.

#### Fuentes y materiales
- [CORFO-001 · Semilla Inicia — ficha y convocatorias](https://www.corfo.gob.cl/sites/cpp/programa/semilla-inicia/)
- [CORFO-002 · Semilla Inicia — Resolución 1498, 2025](https://www.bcn.cl/leychile/Navegar?idNorma=1218656&idVersion=2025-11-19)
- [CORFO-005 · Semilla Expande 2026](https://www.corfo.gob.cl/sites/cpp/convocatoria/semilla-expande-2026/)
- [CORFO-018 · Startup CTCI 2027](https://anid.cl/concursos/startup-ctci-2027/)
- [CORFO-025 · Manual FIA–Gearbox](https://rebrota.fia.cl/wp-content/uploads/2025/06/Guia_metodologica_formulacion_de_proyectos.pdf)

## Módulo 28 · Gestión continua y aprendizaje

**Úsalo cuando:** Ritmo semanal, decisiones, revisión · **Gate:** todos · **Plantillas:** TPL-062, 069, 100 (troncales en `assets/plantillas/catalogo_plantillas.csv`)

#### Métodos de referencia
ISO 56000; Sercotec; scientific approach; Stage-Gate; mentor reviews.

#### Procedimiento operativo
1. Revisar semanalmente evidencias, ventas, caja, aprendizaje, riesgos, capacidad y decisiones.
2. Registrar resultado real versus meta, causa y siguiente acción.
3. Mantener backlog de incertidumbres con dueño, coste y criterio de éxito.
4. Limitar iniciativas activas mediante potencial/evidencia, no sunk cost.
5. Evaluar mentoría y programas por acciones y resultados.
6. Actualizar documentación generada a partir de la evidencia; archivar versiones.
7. Celebrar aprendizaje negativo útil sin confundirlo con éxito comercial.

#### Entregables
Weekly Operating Review; decision journal; scorecard.

#### Criterio de salida
Se puede explicar qué cambió esta semana, qué evidencia motivó la decisión y qué riesgo se resolverá después.

#### Errores y alertas
Actividades sin impacto; métricas de vanidad; insistir por inversión hundida; acumular canvas contradictorios.

#### Fuentes y materiales
- [CORFO-027 · Manual Centros de Negocios 2020](https://www.sercotec.cl/wp-content/uploads/2022/10/Anexo-13-Manual-de-Gesti%C3%B3n-y-Operaci%C3%B3n-Centros-de-Negocios-SERCOTEC-2020.pdf)
- [ACADEMIA-005 · Beyond Demo Day 2026](https://www.nber.org/papers/w35063)
- [ACADEMIA-001 · Método científico en decisiones emprendedoras](https://doi.org/10.1002/smj.3580)
- [METODO-056 · Stage-Gate](https://www.stage-gate.com/)
