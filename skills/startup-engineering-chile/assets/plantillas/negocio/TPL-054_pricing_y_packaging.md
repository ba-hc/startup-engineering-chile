# TPL-054 — Precio y empaquetado (Pricing & Packaging)

**Para qué:** fijar métrica de cobro, niveles y precio anclados al valor frente a la alternativa, y probarlos con un compromiso real. · **Gate:** G4 (–G7) · **Alimenta:** `experimentos.csv`, `evidencias.csv`, `decisiones.csv`

## Completar
### 1. Ancla de valor
| Elemento | Valor | ID o supuesto |
|---|---|---|
| Segmento y comprador (quién firma) | [ ] | |
| Mejor alternativa y su costo anual | [lo que paga hoy, incluido "hacerlo a mano"] | |
| Beneficio realizable por cliente/año | [baseline × mejora × factor realizable] | |
| Piso (costo directo + margen mínimo) / techo (beneficio realizable) | [ ] | |

*Horas ahorradas no son caja salvo que se reasignen o se dejen de pagar.*

### 2. Métrica de cobro
[usuario / sitio / vehículo / transacción / resultado] — *debe crecer con el valor que recibe el cliente y ser fácil de contar para ambas partes.*

### 3. Niveles
| Nivel | Para quién | Incluye / límite | Neto/mes | Con IVA 19% | Setup | Costo directo | Margen de contribución |
|---|---|---|---|---|---|---|---|

Moneda (CLP o UF) y si el precio publicado incluye IVA: [ ] · Descuentos y meses gratis (precio efectivo vs. lista): [ ]

### 4. Prueba de precio con compromiso real
[Oferta concreta a N compradores con poder de firma; compromiso = pago anticipado, OC o contrato, nunca "¿pagarías X?"] · Umbral y reglas fijadas antes: [ ] · EXP-ID: [ ]

## Ejemplo bueno (ficticio)
"FríoRuta", sensores y alertas de temperatura para distribuidoras de alimentos refrigerados con 5–30 camiones, RM. Firma: gerente de operaciones.
- Alternativa: termógrafo desechable + revisión manual; mermas por quiebre de frío ≈ $30 M/año en una flota de 10 camiones (EV-011, 4 distribuidoras). Factor realizable 40% → beneficio $12 M/año (supuesto H-008).
- Métrica: vehículo monitoreado/mes (crece con la flota y es auditable).

| Nivel | Para | Límite | Neto/mes | IVA incl. | Setup | Costo dir. | Margen |
|---|---|---|---|---|---|---|---|
| Base | ≤10 camiones | alertas + reporte mensual | 1,0 UF/vehículo | 1,19 UF | 3 UF | 0,35 UF | 65% |
| Pro | 11–30 | + API a ERP, histórico 2 años | 0,85 UF/vehículo | 1,01 UF | 6 UF | 0,35 UF | 59% |

10 camiones en Base = 120 UF/año ≈ $5,0 M neto: ~42% del beneficio realizable (costo directo EV-012).
- Prueba EXP-006: a 8 gerentes de operaciones, 3 meses de Base a 0,8 UF/vehículo pagados por adelantado. ≥3 de 8 pagan → Go; 1–2 → revisar métrica y nivel; 0 → Recycle.

## Ejemplo malo y por qué falla
"Plan Básico $29.990, Pro $59.990, Enterprise a cotizar. Precios similares a competidores de EE.UU. En la encuesta, 70% dijo que pagaría el Pro."
- Sin ancla: no hay alternativa ni beneficio; el precio sale de copiar listas extranjeras.
- Sin métrica de cobro ni límites por nivel, y no dice si incluye IVA.
- "Pagaría" es intención declarada, no compromiso; no hubo umbral previo ni cálculo de margen.

## Criterio de aceptación
- La alternativa y el beneficio realizable están cuantificados con ID o marcados supuesto.
- La métrica de cobro está escrita y crece con el valor del cliente.
- Cada nivel tiene límite, precio neto, precio con IVA, setup y margen de contribución.
- La prueba exige pago, OC o contrato a quien firma, con umbral registrado en `experimentos.csv` antes de ofrecer.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
