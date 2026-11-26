# TPL-087 — Economía unitaria (Unit Economics)

> **Para qué sirve:** Saber si cada cliente deja más de lo que cuesta conseguirlo y servirlo, con CAC cargado completo y churn observado.
> **Cuándo NO usarla:** Con menos de 3–6 meses de clientes pagando: sin churn observado el LTV es ficción, y conviene mostrar solo margen de contribución y payback, como rangos.
> **Micro-ejemplo resuelto:** Precio $120.000/mes, costo variable $36.000 y CAC cargado $504.000 → contribución $84.000 y payback de 6 meses; con churn de 4% la vida es 25 meses, el LTV $2.100.000 y LTV/CAC ≈ 4,2.

**Gate:** G4 / G8 · **Alimenta:** `bitacora.csv` (tipo kpi y cohorte), `decisiones.csv`

## Completar
**Unidad de cobro:** [cuenta, sede, camión, usuario activo] · **Moneda:** CLP neto, sin IVA · **Fecha de corte:** [ ]
*Fija los umbrales antes de calcular y regístralos en `decisiones.csv`:* payback ≤ [ ] meses · margen ≥ [ ]% · LTV/CAC ≥ [ ]

| Componente mensual por unidad | Cómo se calcula | CLP | ID o "supuesto" |
|---|---|---|---|
| Ingreso neto | [precio − descuento promedio; sin IVA ni setup] | | |
| Costos variables directos | [infra, datos, hardware amortizado, soporte (h × costo hora), comisiones] | | |

| CAC del período [trimestre] | CLP | ID o "supuesto" |
|---|---|---|
| Publicidad pagada | | |
| Ferias, viajes, demos, material | | |
| Horas comerciales del fundador [h × valor hora] | | |
| Comisiones, vendedores, CRM | | |
| **Total ÷ clientes nuevos del mismo período** | | |

**Churn mensual observado:** [bajas ÷ clientes-mes, desde `bitacora.csv` (tipo cohorte); con < 6 meses o < 20 clientes, usa un rango y dilo]
*No calcules a mano:* `python scripts/finanzas.py unit --precio <ingreso> --costo-variable <CV> --cac <CAC> --churn <tasa>` y pega su tabla.

## Ejemplo bueno (ficticio)
FríoRuta: monitoreo de temperatura para distribuidoras de alimentos refrigerados; unidad = cuenta con flota promedio de 5 camiones. Umbrales (DEC-007, 2026-09-30): payback ≤ 12 · margen ≥ 60% · LTV/CAC ≥ 3.
- Ingreso neto $350.000/mes (+IVA = $416.500), sin descuentos (EV-021, contratos).
- Costos variables $105.000: datos M2M $25.000 · sensores en comodato $37.500 (5 × $180.000 / 24 meses) · nube $15.000 · soporte 1,5 h × $18.000 = $27.000 (EV-024, tickets).
- CAC T3: ads $450.000 + feria $1.100.000 + fundador 80 h × $20.000 (valor hora: supuesto) + demos $350.000 + comisiones $360.000 = $3.860.000 ÷ 3 nuevos = $1.287.000.
- Churn 3,6%: 4 bajas en 110 clientes-mes, cohortes ene–sep (`bitacora.csv` tipo cohorte, EV-030).
- `finanzas.py unit`: contribución $245.000 · margen 70,0% · payback 5,3 meses · vida 27,8 meses · LTV $6.805.556 · LTV/CAC 5,29 → cumple los tres umbrales.
- Límite: solo 3 altas por trimestre; si el churn sube a 5% la vida (20 meses) no alcanza a amortizar los sensores a 24 meses.

## Ejemplo malo y por qué falla
> Precio $350.000. CAC $150.000 (Google Ads ÷ 3 clientes). Churn 1% ("en B2B nadie se va"). LTV = $350.000 × 100 meses = $35.000.000. LTV/CAC = 233.
- CAC solo de ads: omite feria, demos, comisiones y 80 h del fundador; el cargado es 8,6 veces mayor.
- Churn supuesto sin cohortes (el observado es 3,6%); el script además topa la vida en 60 meses.
- LTV sobre ingreso y no sobre contribución: ignora $105.000/mes de costos variables.
- Sin umbral previo: cualquier resultado "se ve bien".

## Criterio de aceptación
- Ingreso neto sin IVA ni setup y unidad de cobro declarada.
- El CAC suma horas del fundador y todo el gasto comercial del mismo período que las altas.
- El churn sale de `bitacora.csv` (tipo cohorte) o se presenta como rango explícito.
- La tabla viene de `finanzas.py unit` y los umbrales están en `decisiones.csv` con fecha anterior al cálculo.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
