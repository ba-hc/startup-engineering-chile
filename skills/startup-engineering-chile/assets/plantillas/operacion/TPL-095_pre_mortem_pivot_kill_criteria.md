# TPL-095 — Pre-mortem y criterios de pivote o cierre (Pre-mortem / Pivot-Kill Criteria)

**Para qué:** fijar, antes de un gasto significativo, por qué podría fracasar y qué cifra concreta obliga a perseverar, pivotar o detenerse. · **Gate:** transversal (antes de un gasto que cambia de etapa, típ. G5–G7) · **Alimenta:** `riesgos.csv`, `decisiones.csv`, `experimentos.csv`

## Completar
**Decisión en juego:** [qué, monto CLP, meses, ¿reversible?] · **Pérdida aceptable:** [TPL-036]
**Ejercicio:** "Es [fecha + 12 meses] y esto fracasó. ¿Por qué?" Cada persona escribe sola 5 min antes de compartir.
*Causas específicas de este proyecto, no categorías ("competencia", "financiamiento").*

| Causa del fracaso | Tipo [demanda / venta / técnica / economía / equipo / legal] | Prob. (B/M/A) | Impacto (B/M/A) | Señal temprana medible | Umbral de alarma | Mitigación que empieza hoy | risk_id |
|---|---|---|---|---|---|---|---|
| [ ] | | | | | | | |

| Métrica decisiva | Persevera si | Pivota si [hacia qué] | Detiene si | Fecha de corte | Fuente |
|---|---|---|---|---|---|
| [ ] | | | | | |

*Fija estos criterios y su fecha en `decisiones.csv` antes del gasto; no los muevas al ver los datos. Un "detiene si" sin fecha no detiene nada.*

## Ejemplo bueno (ficticio)
InspectaCinta: inspección térmica con visión artificial de correas transportadoras en faenas mineras. Decisión: contratar 2 ingenieros y comprar 3 equipos ($38.000.000, 9 meses, parcialmente reversible) para pasar de 1 a 4 faenas. Pérdida aceptable: $45.000.000 (TPL-036).

| Causa | Tipo | P | I | Señal | Umbral | Mitigación | ID |
|---|---|---|---|---|---|---|---|
| La faena no renueva: el ahorro no se atribuye al sistema | demanda | A | A | línea base de detenciones firmada | sin firma a la semana 2 | usar registro de 6 meses de la faena (EV-041) | R-004 |
| Compras exige homologación de proveedor (6+ meses) | venta | M | A | fecha de homologación | sin fecha al mes 1 | iniciar homologación hoy con el piloto actual | R-005 |
| Falsas alarmas: operadores ignoran alertas | técnica | M | A | % falsos positivos semanal | > 15% dos semanas | revisión humana de alertas en el piloto | R-006 |

| Métrica | Persevera | Pivota | Detiene | Corte |
|---|---|---|---|---|
| Faenas con OC firmada | ≥ 2 | 1 → vender a contratistas de mantención | 0 | 2027-06-30 |
| Falsos positivos | ≤ 10% | 10–25% → solo rodillos | > 25% | semana 8 |

Fijado el 2026-12-01 por ambos socios (DEC-012), antes de firmar contratos.

## Ejemplo malo y por qué falla
> Riesgos: competencia, que la tecnología no funcione, falta de financiamiento. Mitigación: trabajar duro y buscar inversionistas. Si no resulta en un tiempo razonable, evaluaremos pivotear.
- Riesgos genéricos: no nombran una causa propia ni quién la observa.
- Sin señal ni umbral: nadie sabrá cuándo encender la alarma.
- "Tiempo razonable" sin fecha ni cifra: el criterio se acomodará después.
- La mitigación no es una acción con responsable.

## Criterio de aceptación
- Cada causa tiene señal medible, umbral y mitigación registrada en `riesgos.csv`.
- Cada métrica decisiva tiene los tres umbrales y una fecha de corte.
- `decisiones.csv` registra los criterios con fecha anterior al gasto.
- El monto en juego está dentro de la pérdida aceptable o se achicó.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
