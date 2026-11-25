# Formulación del proyecto financiable y control financiero
> **Última verificación:** 2026-11-25 · **Revisar:** antes de cada convocatoria. Regla: si una condición de elegibilidad o un monto decide algo, contrástalo con las bases del llamado vigente (resumen actualizable en `assets/fondos/instrumentos.json`; revisión con `scripts/fondos_lint.py`).

## 1. Separar dos expedientes
**Venture dossier:** oportunidad, mercado, producto, modelo de negocio, riesgos, equipo, caja, resultados. Es permanente.
**Funding dossier:** convocatoria, elegibilidad, propósito del subsidio, brechas, actividades, plazos, costos elegibles, aportes, indicadores y resultados comprometidos. Se versiona por llamado. No todo el gasto de una empresa es financiable; no todo lo financiable corresponde a una buena decisión de negocio.

## 2. Lógica vertical y horizontal
| Nivel | Ejemplo hipotético de automatización documental | Evidencia |
|---|---|---|
| Fin | Mejorar productividad de organizaciones | Seguimiento posterior |
| Propósito | Validar solución técnica y comercial en segmento | Informe y ventas/compromisos según bases |
| Resultado 1 | Prototipo integrado | Pruebas predefinidas |
| Resultado 2 | Evaluación en entorno relevante | Registros piloto, guardrails |
| Resultado 3 | Modelo comercial validado | Ofertas, resultados de adquisición |
| Actividades | Entrevistas, desarrollo, integración, pilotaje, ventas | Entregables y comprobantes |
| Supuestos | Acceso a datos, disponibilidad del cliente, recursos | Acuerdos, mitigaciones |

El objetivo general describe una transformación verificable. Los objetivos específicos no son una lista de tareas: identifican resultados parciales. Cada objetivo requiere indicador, línea base, meta, fecha y medio de verificación. Evitar verbos vagos (potenciar, revolucionar, aumentar sin magnitud).

## 3. Additionality: con y sin subsidio
| Variable | Sin subsidio | Con subsidio | Diferencia verificable |
|---|---|---|---|
| Desarrollo | Capacidad financiable por equipo | Nuevos recursos elegibles | Riesgo técnico eliminado |
| Validación | Pruebas limitadas | Más condiciones y clientes | Incertidumbre comercial reducida |
| Comercialización | Canal actual | Acceso a mercado o test específico | Evidencia comercial |
| Tiempo/costos | Plan realista | Hito anticipado o ampliado | Magnitud y limitación |

No afirmar que el proyecto es imposible sin fondos si no es cierto. El subsidio debe justificar su adicionalidad y una ruta comercial sostenible una vez terminado.

## 4. Presupuesto modelo de referencia (hipotético, CLP netos)
Para un subsidio general de hasta $15M y cofinanciamiento de 75%, un proyecto de $20M tendría $15M subsidio y $5M de aportes, **solo si todos los gastos son elegibles y se aprueban**. La siguiente distribución es ejemplo, no lista de gastos permitidos.
| Actividad | Resultado | Total | Subsidio (supuesto) | Aporte |
|---|---|---:|---:|---:|
| Investigación y validación | Segmento y demanda | 2.000.000 | 1.500.000 | 500.000 |
| Desarrollo técnico | PoC/MVP integrado | 7.000.000 | 5.250.000 | 1.750.000 |
| Pruebas e integración | Evidencia técnica | 3.000.000 | 2.250.000 | 750.000 |
| Pilotaje y medición | Resultados operacionales | 4.000.000 | 3.000.000 | 1.000.000 |
| Comercialización | Evidencia de compra | 2.000.000 | 1.500.000 | 500.000 |
| Apoyo y costos autorizados | Ejecución y seguimiento | 2.000.000 | 1.500.000 | 500.000 |
| Total | | 20.000.000 | 15.000.000 | 5.000.000 |

Revisar topes por cuenta, restricciones, gastos previos, overhead, valorización, IVA recuperable/no recuperable, remuneraciones de socios, contratación y garantías. El 75% no es necesariamente el porcentaje aplicable a cada ítem; se presenta como distribución ilustrativa. Debe quedar coherente con categorías oficiales y modalidad de aporte. No usar este ejemplo directamente como presupuesto presentado.

## 5. Gantt e hitos
| Mes | Trabajo | Resultado | Gate |
|---|---|---|---|
| 1 | Diagnóstico y protocolo | Baseline, clientes y pruebas definidas | Diseño autorizado |
| 2–3 | Desarrollo y pruebas controladas | Capacidad mínima y registro técnico | Go/Hold |
| 4–5 | Integración y validación | Piloto medido | Go/Recycle |
| 6 | Oferta, economía y cierre | Decisión y plan comercial | Continuidad |

Duración ilustrativa; reemplazar según bases y convenio. Vincular dependencia, fecha, responsable, recursos, riesgo y medios de verificación. El cambio de actividad, plazo o gasto puede requerir autorización.

## 6. Rendición: cadena documental
Cada gasto lleva ID, actividad, resultado, cuenta presupuestaria, proveedor, cotización cuando corresponda, orden/contrato, documento tributario, comprobante de pago, evidencia de entrega, fecha, fuente (subsidio/aporte), autorización de cambio y revisión. Conciliar total presupuestado, comprometido, pagado y rendido. Separar gastos no elegibles y aporte valorizado; conservar documentación según convenio. Mantener información sensible de proveedores bajo acceso restringido.

## 7. Indicadores y evidencia
- Proceso: reuniones, tareas, prototipos realizados. No demuestran impacto.
- Resultado: cambio operacional, prueba técnica, adquisición comercial, madurez demostrada.
- Impacto: efecto sostenible posterior (productividad, empleo, impacto ambiental) con método apropiado.
Registrar fórmula, unidad, numerador/denominador, frecuencia, línea base, meta, fuente, guardrails y responsable. Si no se alcanza el objetivo, explicar con evidencia y seguir procedimiento formal, no ocultarlo.

## 8. Revisión previa a enviar
Contrastar cada respuesta con criterio oficial. Verificar totales, cohorte/mercado, período de ventas, fechas y elegibilidad. Revisar legibilidad del pitch y consistencia de cifras entre formulario y modelo. Confirmar anexos exigidos, permisos y canal de presentación. Guardar versión final, recibo de postulación y calendario. No enviar si hay una barrera de admisibilidad sin resolver.

Fuentes: FIA–Gearbox (capítulos de objetivos, indicadores, secuencia, comercialización y evaluación); resolución 1498; bases de cada instrumento; [Consolida y Expande 2026](https://www.corfo.gob.cl/sites/cpp/convocatoria/consolida-y-expande-innovacion-2026/) enlaza manuales normativos. Consultar `../biblioteca/fuentes.csv`.
