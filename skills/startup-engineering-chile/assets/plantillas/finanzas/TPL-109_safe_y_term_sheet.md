# TPL-109 — SAFE y hoja de términos (SAFE / Term Sheet)

> **Para qué sirve:** Entender, antes de firmar, cuánto de la SpA entrega un SAFE post-money o una ronda con precio, y qué derechos y obligaciones agrega cada cláusula.
> **Cuándo NO usarla:** Si todavía no sabes para qué hito es la plata o una alternativa no dilutiva alcanza (ventas, subsidio); tampoco como contrato: el texto final lo redacta y revisa un abogado.
> **Micro-ejemplo resuelto:** Un SAFE post-money de $120 M con cap de $1.200 M entrega 10% de la SpA antes de la ronda con precio (120 ÷ 1.200); un segundo SAFE igual diluye solo a fundadores y pool, no al primero.

**Gate:** G9 (o antes, si se levanta pre-seed) · **Alimenta:** `decisiones.csv`, `cuentas_y_pipeline.csv` (segmento=inversionista), `bitacora.csv` (tipo riesgo)

## Completar
*Orientación educativa. En Chile no hay un SAFE oficial: se adaptan modelos (YC, Platanus) al derecho chileno; su tratamiento tributario depende del texto exacto (ver `references/flujos/capital_privado.md`). Cálculos con `scripts/cap_table.py`; texto final revisado por abogado.*

### 1. Para qué es la plata
Hito verificable [ ] · costo y meses para llegar [TPL-088] · alternativa no dilutiva evaluada [ ]

### 2. Términos del SAFE
| Término | Propuesto | Habitual en seed | Comentario o riesgo |
|---|---|---|---|
| Monto | | | |
| Cap post-money | | coherente con tracción y comparables | |
| Descuento | | 0–20% | |
| MFN (nación más favorecida) | | frecuente | |
| Pro rata / carta paralela | | | |
| Conversión y evento de liquidez | | ronda con precio; venta o disolución | |
| Ley y resolución de conflictos | | ley chilena si la SpA es chilena | |

**% al convertir (post-money):** monto ÷ cap = [ ]% · **Dilución acumulada con todos los SAFE:** [salida de `scripts/cap_table.py`]

### 3. Term sheet de ronda con precio (si aplica)
| Cláusula | Propuesta | Habitual en seed | Alerta |
|---|---|---|---|
| Pre-money / inversión / post-money | | | |
| Pool exigido y cuándo se crea | | 5–10% | pool grande creado antes de la ronda |
| Preferencia de liquidación | | 1x no participativa | > 1x o participativa |
| Vesting de fundadores | | 4 años, cliff 1 año | sin aceleración ante despido sin causa |
| Directorio y vetos | | | vetos amplios por un ticket chico |
| Anti-dilución | | promedio ponderado amplio | full ratchet |
| Tag / drag along, preferencia | | | |
| Exclusividad y gastos legales | | 30–60 días | |

*La ronda con precio es un aumento de capital acordado por los accionistas: se modifican estatutos y registro de accionistas.*

## Ejemplo bueno (ficticio)
TallerOK SpA: agenda y cobro para talleres mecánicos; 38 talleres pagando, MRR $3,4 M (EV-071). Hito: 150 talleres y caja en equilibrio en 14 meses; costo $160 M (TPL-088).
- SAFE post-money: $160 M, cap $1.600 M, sin descuento, con MFN, sin pro rata, ley chilena, arbitraje en Santiago.
- `scripts/cap_table.py`: el SAFE convierte en 10,0%; fundadores de 45% a 40,5% c/u; pool de 10% a 9%.
- Escenario de ronda futura: pre-money $4.000 M e inversión $1.000 M → nuevo inversionista 20%; fundadores 32,4% c/u.
- Abogado revisó el texto el 2027-03-10 y el contador, su tratamiento tributario (DEC-021).

## Ejemplo malo y por qué falla
> Un ángel ofrece $80 M por un SAFE con cap de $400 M y descuento de 30%, más un asiento en el directorio y veto sobre contrataciones. Firmamos hoy porque se acaba la caja; el contrato lo bajamos de internet, en inglés.
- Cap bajo y descuento alto: entrega 20% o más por $80 M y complica la ronda siguiente.
- Derechos de control por un ticket chico no son habituales en un SAFE.
- Firma por urgencia, sin simulación, sin abogado y con un texto pensado para otra jurisdicción.

## Criterio de aceptación
- El monto está conectado con un hito y con el flujo de caja.
- El % entregado y la dilución acumulada salen de `scripts/cap_table.py` y la tabla suma 100%.
- Cada término se comparó con lo habitual y cada alerta tiene respuesta escrita.
- Un abogado revisó el texto final y la decisión está en `decisiones.csv` con fecha.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
