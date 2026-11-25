# TPL-083 — Pipeline y análisis de ganadas/perdidas (Pipeline & Win/Loss)

**Para qué:** registrar solo oportunidades reales, avanzarlas solo con evidencia verificable y aprender por qué se gana o pierde. · **Gate:** G7–G8 · **Alimenta:** `cuentas_y_pipeline.csv`, `decisiones.csv`

## Completar
### 1. Etapas y criterio de salida
*Defínelas una vez; no las cambies a mitad de trimestre.*

| Etapa | Sale cuando… (verificable) | Prob. interna |
|---|---|---|
| 0 Cuenta objetivo | calza con el ICP y tiene señal de compra registrada | – |
| 1 Descubrimiento | reunión con quien tiene el problema; dolor y alternativa documentados (ENT-ID) | 10% |
| 2 Calificada | se conocen comprador, presupuesto o proceso de compra y fecha de decisión | 25% |
| 3 Propuesta | propuesta con precio revisada con el comprador en reunión | 50% |
| 4 Compromiso | OC, contrato o acta de piloto pagado firmada | 90% |
| Ganada / Perdida | factura emitida / "no" explícito o 60 días sin respuesta | 100% / 0% |

*Un lead no es oportunidad: sin comprador ni fecha de decisión, no pasa de etapa 1.*

### 2. Oportunidades
| cuenta_id | segmento | senal_compra | rol_comprador | etapa | necesidad | valor_estimado_CLP (neto) | fecha_estimada | proxima_accion | causa_perdida | evidence_id |
|---|---|---|---|---|---|---|---|---|---|---|

### 3. Win/Loss (mensual o cada 10 cierres)
| Causa | Ganadas | Perdidas | Ejemplo (CTA-ID) | Acción |
|---|---|---|---|---|

Causas estándar de pérdida: precio · sin presupuesto · eligió competidor (cuál) · eligió no hacer nada · sin comprador · producto incompleto · momento. *"No respondió" no es causa: pregunta.*
**Forecast** = Σ (valor × probabilidad de la etapa), solo etapas ≥2: [ ]

## Ejemplo bueno (ficticio)
"PlanObra", control de avance físico para constructoras medianas (50–300 trabajadores), RM y Valparaíso. Precio: 18 UF + IVA por obra/mes.

| cuenta_id | etapa | rol_comprador | necesidad | valor neto/año | fecha_estimada | proxima_accion | evidence_id |
|---|---|---|---|---|---|---|---|
| CTA-004 | 3 Propuesta | gerente de proyectos | estados de pago atrasados 2 semanas | $26,9 M (3 obras) | 15-12-2026 | revisión 2-12 | ENT-011 |
| CTA-006 | 2 Calificada | gerente general | informes de avance al mandante | $9,0 M (1 obra) | 20-01-2027 | demo con jefe de obra 4-12 | ENT-014 |
| CTA-002 | Perdida | gerente de finanzas | causa: eligió no hacer nada ("seguimos con planilla") | — | — | — | ENT-009 |

Forecast: 26,9 × 0,5 + 9,0 × 0,25 ≈ $15,7 M.
Win/Loss oct–nov: 2 ganadas (informe para mandante), 4 perdidas (2 no hacer nada, 1 precio vs. planilla, 1 sin comprador) → DEC-015: calificar presupuesto antes de la demo.

## Ejemplo malo y por qué falla
"Pipeline: 85 oportunidades por $1.200 M. Etapas: contactado, interesado, caliente. Forecast Q1: 30% del pipeline. Perdidas: no respondieron."
- Cuenta leads como oportunidades; etapas por sensación ("caliente"), sin criterio verificable.
- El forecast es un % arbitrario del total, no valor × probabilidad por etapa.
- Pérdidas sin causa: nada que aprender.

## Criterio de aceptación
- Cada etapa tiene un criterio de salida observable (documento, reunión o firma).
- Toda oportunidad en etapa ≥2 tiene rol_comprador, fecha_estimada y evidence_id.
- Cada perdida tiene causa de la lista estándar.
- Forecast por etapa con las probabilidades definidas, en CLP neto.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
