# Mapa de enrutamiento: necesidad → módulo → plantillas → registros → gate

Úsalo para saltar directo a lo que el usuario necesita (modo *complementar*) o para decidir qué sigue tras el diagnóstico. Módulos en `references/manual/`, plantillas: las 25 troncales están completas en `assets/plantillas/`; las demás IDs del mapa se crean como esqueleto con su criterio (`expediente.py doc TPL-XXX` sirve para ambas). Umbrales por gate y ejemplos de decisiones: `expediente.py umbrales` y `references/ejemplos_y_umbrales.md`, registros en `expediente/registros/`.

| # | Módulo (archivo en manual/) | Cuándo usarlo | Plantillas | Registros | Gate |
|---|---|---|---|---|---|
| 01 | Fundador, equipo y recursos (`01_…`) | Equipo nuevo, dudas de dedicación (pesos de referencia Semilla Inicia: capacidad 20% + compromiso 10%) | TPL-034, 035, 036, 093 | — | G0 |
| 02 | Oportunidades y contexto (`02_…`) | Varias ideas, aún sin foco | TPL-001, 002, 003, 004, 008, 009, 010, 056 | desafios_corporativos | G0 |
| 03 | Definición y cuantificación del problema (`03_…`) | Problema difuso o descrito como "falta de mi solución" | TPL-005, 006, 007, 011, 012 | hipotesis, evidencias | G1 |
| 04 | Investigación cualitativa (`04_…`) | Preparar o analizar entrevistas | TPL-013, 014, 015, 016, 018, 028 | entrevistas, evidencias | G1 |
| 05 | Investigación cuantitativa (`05_…`) | Encuestas, muestras, cifras propias | TPL-017, 029 | evidencias | G1–G2 |
| 06 | Segmentación, ICP y compradores (`06_…`) | "Mi cliente es todo el mundo"; B2B con varios decisores | TPL-019, 020, 021, 022, 023, 025 | cuentas_y_pipeline | G2 |
| 07 | Mercado y TAM/SAM/SOM (`07_…`) | Tamaño de mercado, estudio de mercado | TPL-030, 032 | fuentes_nuevas, evidencias | G2 |
| 08 | Competencia, posicionamiento y estrategia (`08_…`) | Benchmark, "no tenemos competencia", diferenciación | TPL-031, 033, 039, 041, 042, 043, 044 | competencia | G3 |
| 09 | Innovación y diferenciación (`09_…`) | Justificar innovación (CORFO), estado del arte | TPL-010, 045, 096 | ip_licencias | G3 |
| 10 | Propuesta de valor, VPC y JTBD (`10_…`) | Promesa poco clara, beneficios no cuantificados | TPL-024, 026, 027, 049, 055 | evidencias | G3 |
| 11 | Modelo de negocio (`11_…`) | BMC/Lean Canvas, alternativas de modelo | TPL-040, 047, 048, 050, 051, 052 | — | G4 |
| 12 | Monetización, pricing y packaging (`12_…`) | Definir precio, planes, unidad de cobro | TPL-053, 054, 055 | experimentos | G4 |
| 13 | Experimentación y prototipado (`13_…`) | Priorizar supuestos, diseñar pruebas | TPL-038, 059–066, 075 | hipotesis, experimentos, evidencias | G5 |
| 14 | Producto, UX y estrategia técnica (`14_…`) | MVP, roadmap, TRL | TPL-037, 070–077 | indicadores | G5 |
| 15 | Pilotaje, adopción e implementación (`15_…`) | Diseñar o cerrar un piloto | TPL-067, 068, 086 | pilotos | G6 |
| 16 | Go-to-market y distribución (`16_…`) | Primeras ventas, playbook, pipeline | TPL-081, 082, 083, 084 | cuentas_y_pipeline | G7 |
| 17 | PMF, retención y expansión (`17_…`) | Churn, cohortes, ¿tenemos PMF? | TPL-078, 079, 080, 085 | cohortes, indicadores | G8 |
| 18 | Economía unitaria y ROI (`18_…`) | CAC, LTV, margen, ROI para el cliente | TPL-058, 087 | indicadores | G4/G8 |
| 19 | Finanzas, caja y escenarios (`19_…`) | Flujo de caja, runway, escenarios | TPL-088 + `entregables/modelo_financiero.xlsx` | — | G4/G9 |
| 20 | Operaciones y organización (`20_…`) | Procesos, roles, capacidad | TPL-093, 100 | — | G8 |
| 21 | Legal, PI y seguridad (`21_…`) | Contratos, licencias, datos personales | TPL-096, 097 | ip_licencias, riesgos | transversal |
| 22 | Impacto, sostenibilidad y ética (`22_…`) | Criterio sostenibilidad CORFO, teoría de cambio | TPL-098 | indicadores | transversal |
| 23 | Madurez, riesgo y gobernanza (`23_…`) | TRL/IRL, riesgos, pre-mortem, decisión go/kill | TPL-046, 069, 094, 095, 099 | riesgos, decisiones | todos |
| 24 | Ecosistema, mentoría y alianzas (`24_…`) | Buscar mentores, incubadoras, socios | TPL-057, 101, 102 | lecciones_mentores | transversal |
| 25 | Financiamiento público y formulación (`25_…`) + `references/corfo/` | Postular a CORFO/ANID/Start-Up Chile | TPL-103–108 | corfo_elegibilidad, rendiciones | CORFO |
| 26 | Inversión, due diligence y valorización (`26_…`) | Levantar capital privado | TPL-089, 090, 091, 092 | — | G9 |
| 27 | Escalamiento e internacionalización (`27_…`) | Expandir a otro país LATAM | TPL-079, 099 | — | G9 |
| 28 | Gestión continua y aprendizaje (`28_…`) | Ritmo semanal, decisiones, revisión | TPL-062, 069, 100 | decisiones | todos |

## Etapa → por dónde empezar (del manual, `00_mapa_y_criterios.md`)
| Etapa | Prioridad | Evitar |
|---|---|---|
| Idea | 02, 03, 04, 06, 13 (hipótesis), 07 preliminar | proyecciones a 5 años |
| Pre-MVP | 10, 08, 13, 12 inicial, 14 (PoC) | construir la suite completa |
| MVP | 15, 18, 14, 19 | confundir descargas con uso |
| Primeras ventas | 16, 18, 17, 12 | contratar equipo comercial sin proceso |
| Escalamiento | 17, 19, 20, 26, 27 | crecer sin margen o caja |

## Otros recursos
- Fórmulas y advertencias de métricas: `references/formulas_y_registros.md`.
- Workshops (dinámicas de 90–120 min por tema): `references/operacion/workshops.csv` (taller, duración, entradas, dinámica, salida, criterio).
- Plan de 90 días por semana y gate: `references/operacion/01_plan_90_dias.md`.
- Casos y ejemplo integral (datos pedagógicos, no reales): `references/casos/`.
- Fuentes con URL (268), libros, charlas, mentores: `references/biblioteca/*.csv` (consulta con `expediente.py biblioteca "texto"`).
- Cifras y afirmaciones verificables con su estado: `references/investigaciones/afirmaciones_y_cifras.csv`.
- Flujos de trabajo paso a paso (retomar, ciclo de bloque, finanzas, fondos, red team, compuerta antisesgo, compras públicas, socios y equity, trampas chilenas, internacionalización, privacidad, cohorte, capital privado, sumarse a una startup, pivote y cierre, venta corporativa, caja y cobro, spin-off/EBCT, verticales reguladas, MVP con IA): `references/flujos/`.
- Qué script usar para cada cálculo o revisión: `references/herramientas.md`.
- Parámetros chilenos verificados (UF/UTM de respaldo, tasas, tramos): `assets/parametros_cl.json`; reglas de instrumentos de fondos: `assets/fondos/instrumentos.json`.
