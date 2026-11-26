# Mapa de enrutamiento: necesidad → módulo → plantillas → registros → gate

Úsalo para saltar directo a lo que el usuario necesita (modo *complementar*) o para decidir qué sigue tras el diagnóstico. Módulos agrupados en 6 guías por etapa en `references/manual/`; plantillas: las 40 troncales están completas en `assets/plantillas/`; las demás IDs del mapa se crean como esqueleto con su criterio (`expediente.py doc TPL-XXX` sirve para ambas). Umbrales por gate y ejemplos de decisiones: `expediente.py umbrales` y `references/ejemplos_y_umbrales.md`, registros en `expediente/registros/`.

| # | Módulo (guía en `references/manual/`) | Cuándo usarlo | Plantillas | Registros | Gate |
|---|---|---|---|---|---|
| 01 | Fundador, equipo y recursos (`manual/G0_oportunidad_y_equipo.md`) | Equipo nuevo, dudas de dedicación (pesos de referencia Semilla Inicia: capacidad 20% + compromiso 10%) | TPL-034, 035, 036, 093 | — | G0 |
| 02 | Oportunidades y contexto (`manual/G0_oportunidad_y_equipo.md`) | Varias ideas, aún sin foco | TPL-001, 002, 003, 004, 008, 009, 010, 056 | bitácora (desafío) | G0 |
| 03 | Definición y cuantificación del problema (`manual/G1-G2_problema_cliente_y_mercado.md`) | Problema difuso o descrito como "falta de mi solución" | TPL-005, 006, 007, 011, 012 | hipotesis, evidencias | G1 |
| 04 | Investigación cualitativa (`manual/G1-G2_problema_cliente_y_mercado.md`) | Preparar o analizar entrevistas | TPL-013, 014, 015, 016, 018, 028 | entrevistas, evidencias | G1 |
| 05 | Investigación cuantitativa (`manual/G1-G2_problema_cliente_y_mercado.md`) | Encuestas, muestras, cifras propias | TPL-017, 029 | evidencias | G1–G2 |
| 06 | Segmentación, ICP y compradores (`manual/G1-G2_problema_cliente_y_mercado.md`) | "Mi cliente es todo el mundo"; B2B con varios decisores | TPL-019, 020, 021, 022, 023, 025 | cuentas_y_pipeline | G2 |
| 07 | Inteligencia de mercado y TAM/SAM/SOM (`manual/G1-G2_problema_cliente_y_mercado.md`) | Tamaño de mercado, estudio de mercado | TPL-030, 032 | bitácora (fuente), evidencias | G2 |
| 08 | Competencia, posicionamiento y estrategia (`manual/G3-G4_propuesta_modelo_y_economia.md`) | Benchmark, "no tenemos competencia", diferenciación | TPL-031, 033, 039, 041, 042, 043, 044 | competencia | G3 |
| 09 | Innovación y diferenciación (`manual/G3-G4_propuesta_modelo_y_economia.md`) | Justificar innovación (CORFO), estado del arte | TPL-010, 045, 096 | bitácora (ip) | G3 |
| 10 | Propuesta de valor, Customer Canvas y JTBD (`manual/G3-G4_propuesta_modelo_y_economia.md`) | Promesa poco clara, beneficios no cuantificados | TPL-024, 026, 027, 049, 055 | evidencias | G3 |
| 11 | Diseño del modelo de negocio (`manual/G3-G4_propuesta_modelo_y_economia.md`) | BMC/Lean Canvas, alternativas de modelo | TPL-040, 047, 048, 050, 051, 052 | — | G4 |
| 12 | Monetización, pricing y packaging (`manual/G3-G4_propuesta_modelo_y_economia.md`) | Definir precio, planes, unidad de cobro | TPL-053, 054, 055 | experimentos | G4 |
| 13 | Experimentación y prototipado (`manual/G5-G6_experimentos_producto_y_piloto.md`) | Priorizar supuestos, diseñar pruebas | TPL-038, 059–066, 075 | hipotesis, experimentos, evidencias | G5 |
| 14 | Producto, UX y estrategia técnica (`manual/G5-G6_experimentos_producto_y_piloto.md`) | MVP, roadmap, TRL | TPL-037, 070–077 | bitácora (kpi) | G5 |
| 15 | Pilotaje, adopción e implementación (`manual/G5-G6_experimentos_producto_y_piloto.md`) | Diseñar o cerrar un piloto | TPL-067, 068, 086 | pilotos | G6 |
| 16 | Go-to-market y distribución (`manual/G7-G9_venta_traccion_y_escala.md`) | Primeras ventas, playbook, pipeline | TPL-081, 082, 083, 084 | cuentas_y_pipeline | G7 |
| 17 | Product-Market Fit, retención y expansión (`manual/G7-G9_venta_traccion_y_escala.md`) | Churn, cohortes, ¿tenemos PMF? | TPL-078, 079, 080, 085 | bitácora (cohorte, kpi) | G8 |
| 18 | Economía unitaria y evaluación de ROI (`manual/G3-G4_propuesta_modelo_y_economia.md`) | CAC, LTV, margen, ROI para el cliente | TPL-058, 087 | bitácora (kpi) | G4/G8 |
| 19 | Finanzas, caja, inversión y escenarios (`manual/G3-G4_propuesta_modelo_y_economia.md`) | Flujo de caja, runway, escenarios | TPL-088 + `entregables/modelo_financiero.xlsx` | — | G4/G9 |
| 20 | Operaciones, administración y organización (`manual/G7-G9_venta_traccion_y_escala.md`) | Procesos, roles, capacidad | TPL-093, 100 | — | G8 |
| 21 | Legalidad, propiedad intelectual y seguridad (`manual/transversal_legal_riesgo_fondos_y_gestion.md`) | Contratos, licencias, datos personales | TPL-096, 097 | bitácora (ip, riesgo) | transversal |
| 22 | Impacto, sostenibilidad y ética (`manual/transversal_legal_riesgo_fondos_y_gestion.md`) | Criterio sostenibilidad CORFO, teoría de cambio | TPL-098 | bitácora (kpi) | transversal |
| 23 | Madurez, riesgo y gobernanza de innovación (`manual/transversal_legal_riesgo_fondos_y_gestion.md`) | TRL/IRL, riesgos, pre-mortem, decisión go/kill | TPL-046, 069, 094, 095, 099 | bitácora (riesgo), decisiones | todos |
| 24 | Ecosistema, mentoría y alianzas (`manual/G0_oportunidad_y_equipo.md`) | Buscar mentores, incubadoras, socios | TPL-057, 101, 102 | bitácora (lección) | transversal |
| 25 | Financiamiento público y formulación (`manual/transversal_legal_riesgo_fondos_y_gestion.md`) | Postular a CORFO/ANID/Start-Up Chile | TPL-103–108 | bitácora (requisito), rendiciones | CORFO |
| 26 | Inversión, due diligence y valorización (`manual/G7-G9_venta_traccion_y_escala.md`) | Levantar capital privado | TPL-089, 090, 091, 092 | — | G9 |
| 27 | Escalamiento e internacionalización (`manual/G7-G9_venta_traccion_y_escala.md`) | Expandir a otro país LATAM | TPL-079, 099 | — | G9 |
| 28 | Gestión continua y aprendizaje (`manual/transversal_legal_riesgo_fondos_y_gestion.md`) | Ritmo semanal, decisiones, revisión | TPL-062, 069, 100 | decisiones | todos |

## Etapa → por dónde empezar 
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

## Las 6 guías
| Guía | Etapa | Módulos |
|---|---|---|
| `manual/G0_oportunidad_y_equipo.md` | G0 · Oportunidad y equipo | 01, 02, 24 |
| `manual/G1-G2_problema_cliente_y_mercado.md` | G1–G2 · Problema, cliente y mercado | 03, 04, 05, 06, 07 |
| `manual/G3-G4_propuesta_modelo_y_economia.md` | G3–G4 · Propuesta, modelo de negocio y economía | 08, 09, 10, 11, 12, 18, 19 |
| `manual/G5-G6_experimentos_producto_y_piloto.md` | G5–G6 · Experimentos, producto y piloto | 13, 14, 15 |
| `manual/G7-G9_venta_traccion_y_escala.md` | G7–G9 · Venta, tracción y escala | 16, 17, 20, 26, 27 |
| `manual/transversal_legal_riesgo_fondos_y_gestion.md` | Transversal · Legal, riesgo, fondos y gestión | 21, 22, 23, 25, 28 |

## Criterios del sistema

### Arquitectura
El expediente de una startup debe organizar conocimiento de manera coherente. Un núcleo permanente registra oportunidades, segmentos, compradores, problemas, hipótesis, experimentos, evidencia, alternativas, decisiones, costos, riesgos y resultados. Las vistas de salida —Canvas, pitch, estudio de mercado, modelo financiero, dossier comercial y postulación— se generan desde ese núcleo. La presentación no crea evidencia.

| Capa | Entradas | Salidas |
|---|---|---|
| Opportunity Intelligence | Datos, señales de compra, capacidades | Opportunity Brief y mercados candidatos |
| Customer Intelligence | Observaciones, entrevistas, compras | Problemas, ICP, JTBD, DMU, mercado |
| Business Design | Alternativas, necesidades, costos | VPC, BMC, pricing y posicionamiento |
| Experimentation | Hipótesis, riesgos | Pruebas, criterios, evidencia y decisiones |
| Product & Adoption | Prototipos, pruebas, integraciones | Roadmap, TRL, piloto e implementación |
| Commercial Engine | Leads, propuestas, contratos | Funnel, retención, PMF y expansión |
| Financial Engine | Precios, costos, caja | Unit economics, ROI, escenarios y capital |
| Governance & Funding | Equipo, riesgos, cumplimiento | Plan operativo, IRL/ARL y Funding Dossier |

### Gates: adaptación propia, no rúbrica CORFO
| Gate | Pregunta | Evidencia mínima orientativa | Si falla |
|---|---|---|---|
| G0 oportunidad | ¿Vale la pena investigar? | problema plausible, ventaja/recursos, pérdida máxima | descartar o limitar |
| G1 problema | ¿Qué necesidad existe? | evidencia directa, gravedad, frecuencia, alternativa actual | reformular |
| G2 mercado | ¿A quién vender? | segmento observable, comprador, acceso, tamaño | segmentar de nuevo |
| G3 propuesta | ¿Por qué elegirnos? | alternativas y beneficio diferenciado | cambiar promesa |
| G4 economía | ¿Se puede cobrar rentablemente? | precio defendible, costos y escenarios | modificar modelo |
| G5 factibilidad | ¿Funciona técnicamente? | prueba mínima y riesgos críticos | experimentar o detener |
| G6 piloto | ¿Entrega valor en contexto? | línea base, éxito predefinido, observación | iterar |
| G7 venta/adopción | ¿Compra y usa el cliente? | compromiso y comportamiento adecuados a etapa | resolver barrera |
| G8 repetibilidad | ¿Se repite la venta e implementación? | cohortes, capacidad, márgenes | estandarizar |
| G9 escala | ¿Conviene invertir más? | caja, capacidad, retención, riesgo | posponer escala |

Las puertas no son secuenciales en sentido rígido: factibilidad técnica, comercial y legal pueden investigarse en paralelo. Para Semilla Inicia es normal que parte de la validación ocurra durante el proyecto. No exigir ventas a un instrumento diseñado para proyectos sin ventas. Decisiones posibles: Go, Hold, Recycle, Kill. Ningún puntaje compensa una barrera crítica de seguridad, legalidad o inexistencia de demanda.

### Taxonomía de evidencia
- Declaración sin fuente: no comprobada.
- Hipótesis refutable: redactada como creencia y condición de rechazo.
- Investigación secundaria: documento, estadística, artículo; verificar población, período, metodología y fecha.
- Investigación primaria declarativa: entrevista o encuesta real; documentar selección, consentimiento y limitaciones.
- Comportamiento observado: proceso, uso, aceptación de oferta, prueba registrada.
- Compromiso verificable: carta de intención, tiempo del cliente, recursos asignados, orden o contrato según el caso. No todos equivalen a ingreso.
- Resultado documentado: medición técnica/económica, factura, cobro, ensayo, retención.
- Replicación: resultado consistente en distintos clientes o condiciones.

Esta clasificación no es una escala universal de madurez. Una factura prueba una compra, no necesariamente eficacia; un benchmark prueba una capacidad en las condiciones del ensayo, no necesariamente demanda. Para impacto aplicar diseños apropiados y separar observación de causalidad.

### Cuatro sistemas de preparación
EntreComp evalúa competencias individuales; KTH IRL madurez de cliente, tecnología, negocio, equipo, IP y financiamiento; DOE ARL barreras de adopción; First Round PMF demanda, satisfacción y eficiencia. La evaluación oficial CORFO verifica elegibilidad y mérito. Conservar cada resultado por separado. Las escalas y gates internos de este paquete son adaptaciones originales.

### Qué usar por etapa
| Etapa | Herramientas prioritarias | Evitar |
|---|---|---|
| Idea | Opportunity brief, DEFI2, entrevista, ICP, hipótesis, TAM preliminar | proyecciones arbitrarias a 5 años |
| Pre-MVP | VPC, alternativas, experimentos, pricing inicial, PoC | desarrollar suite completa |
| MVP | piloto, ROI, prueba técnica, plan implementación, caja | confundir descargas con uso |
| Primeras ventas | funnel, unit economics, retención, pricing, onboarding | contratar equipo comercial sin proceso |
| Escalamiento | PMF, NRR, capacidad, expansión, escenarios, gobernanza | crecer con margen o caja insuficientes |

### Lecturas de referencia
FIA–Gearbox, MIT Disciplined Entrepreneurship, Strategyzer, KTH IRL, DOE ARL, First Round, Stage-Gate, Sercotec. Enlaces e identificadores en `references/biblioteca/`.
