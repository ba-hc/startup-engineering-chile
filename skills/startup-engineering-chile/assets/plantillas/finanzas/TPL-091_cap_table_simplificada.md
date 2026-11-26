# TPL-091 — Tabla de capitalización (Cap Table)

> **Para qué sirve:** Saber quién es dueño de qué porcentaje de la SpA hoy, totalmente diluido, y cómo cambia con el pool de opciones, los SAFE y la próxima ronda.
> **Cuándo NO usarla:** Como sustituto del registro de accionistas o para fijar una valorización; la propiedad legal está en el registro y los estatutos, y el precio sale de la negociación, no de esta tabla.
> **Micro-ejemplo resuelto:** Dos fundadores con 5.000.000 de acciones cada uno crean un pool de 1.111.111 acciones (10% totalmente diluido) y quedan en 45% cada uno; un SAFE post-money de $150 M con cap de $1.500 M se lleva 10% y los deja en 40,5% cada uno antes de la ronda.

**Gate:** G0 (al constituir) y G9 (antes de cada ronda) · **Alimenta:** `decisiones.csv`, `bitacora.csv` (tipo riesgo)

## Completar
*Orientación educativa: la SpA lleva su registro de accionistas y sus estatutos se pactan con libertad (Código de Comercio, arts. 424 y siguientes). Esta tabla es un modelo para decidir; los cálculos se hacen con `scripts/cap_table.py`, no a mano, y se revisan con abogado y contador antes de firmar.*
**Fecha de corte:** [ ] · **Respaldo:** registro de accionistas al [fecha] · **Acciones emitidas:** [ ]

### 1. Tabla actual
| Titular | Tipo [ordinaria / preferente / opción / SAFE / nota] | Acciones o equivalente | % básico | % totalmente diluido | Consolidadas / total (vesting) | Documento |
|---|---|---|---|---|---|---|
| [ ] | | | | | | [registro, pacto, contrato] |
| Pool asignado | opción | | | | | |
| Pool sin asignar | opción | | | | | |
| **Total** | | | 100% | 100% | | |

### 2. Instrumentos que convertirán
| Instrumento | Monto CLP | Cap [pre / post-money] | Descuento | Interés y vencimiento (si es nota) | % estimado al convertir |
|---|---|---|---|---|---|

### 3. Simulación de la próxima ronda
Pre-money [ ] · inversión [ ] · pool exigido post-ronda [ ]% · ¿se amplía antes de la ronda? [sí/no]
| Titular | % hoy | % post-ronda | Dilución (puntos) |
|---|---|---|---|

*Todo suma 100%. Los SAFE se muestran convertidos. Un pool que el inversionista pide ampliar "antes de la ronda" diluye solo a los accionistas actuales.*

## Ejemplo bueno (ficticio)
BodegaViva SpA: inventario para almacenes de barrio. Corte 2027-02-28; registro de accionistas EV-060.
| Titular | Tipo | Acciones | % TD | Vesting |
|---|---|---|---|---|
| Fundadora A | ordinaria | 5.000.000 | 40,5% | 14/48 meses |
| Fundador B | ordinaria | 5.000.000 | 40,5% | 14/48 meses |
| Pool (300.000 asignadas a dev senior; 811.111 libres) | opción | 1.111.111 | 9,0% | 24 meses |
| SAFE ángel, post-money, cap $1.500 M, $150 M | SAFE | ≈ 1.234.568 | 10,0% | — |
| **Total** | | 12.345.679 | 100% | |

- Simulación con `scripts/cap_table.py`: ronda de $600 M a pre-money de $2.400 M sin ampliar el pool → inversionista 20%; fundadores 32,4% c/u; pool 7,2%; SAFE 8,0%.
- Si el inversionista exige pool de 10% post-ronda creado antes, la dilución extra recae en fundadores, pool y SAFE: se corre ese escenario antes de responder el term sheet (TPL-109).
- Revisado con abogado el 2027-03-05 (DEC-019).

## Ejemplo malo y por qué falla
> Juan 50%, María 50%. Un ángel nos pasó $100 M por un SAFE; después vemos cuánto es. Al desarrollador le prometimos 5% por WhatsApp.
- Omite el SAFE: los fundadores creen tener 50% y tienen menos.
- Promesa de 5% sin documento, vesting ni pool: conflicto seguro en la due diligence.
- Sin fecha de corte ni registro de accionistas que la respalde.

## Criterio de aceptación
- Suma 100% en básico y totalmente diluido, con fecha de corte y respaldo en el registro de accionistas.
- Cada SAFE o nota tiene monto, cap (pre o post-money), descuento y documento.
- Pool asignado y sin asignar están separados; toda promesa de acciones u opciones tiene documento.
- La simulación de ronda sale de `scripts/cap_table.py` y fue revisada con abogado antes de firmar.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
