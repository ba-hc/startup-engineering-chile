# TPL-034 — Acuerdo de socios y team charter (Team Charter Canvas)

> **Para qué sirve:** Dejar por escrito, antes de constituir la SpA o recibir capital, quién hace qué, cuánto dedica, qué porcentaje recibe, cómo consolida (vesting), de quién es la PI y qué pasa si alguien se va.
> **Cuándo NO usarla:** Con un fundador solo y sin socios en conversación, o como reemplazo del pacto de accionistas firmado; esto ordena la conversación y el encargo al abogado, no tiene fuerza legal por sí mismo.
> **Micro-ejemplo resuelto:** Dos socios que partieron 50/50, con dedicación de 45 h y 10 h por semana, acuerdan 60/40 con vesting de 4 años y cliff de 1 año; si uno sale antes del mes 12, pierde todas sus acciones, que se recompran a valor nominal.

**Gate:** G0 (antes de constituir o levantar capital; se revisa en G9) · **Alimenta:** `decisiones.csv`, `bitacora.csv` (tipo ip y riesgo)

## Completar
*Orientación educativa: el pacto de accionistas y las cesiones de PI los redacta y revisa un abogado. En Chile el vesting no opera por ley: se pacta (opción de compra o recompra sobre acciones no consolidadas) en el pacto de accionistas o en los estatutos de la SpA.*

### 1. Roles, dedicación y aportes
| Socio | Rol y decisiones que le tocan | Horas/semana reales y desde cuándo | Sueldo hoy | Aporte (dinero, código, clientes, PI previa) | ¿Valorizado en acciones o compensado aparte? |
|---|---|---|---|---|---|
| [ ] | | | | | |

### 2. Reparto y vesting
| Socio | % acciones | Vesting [meses] | Cliff [meses] | Inicio del conteo | Aceleración [ninguna / ante venta / doble gatillo] |
|---|---|---|---|---|---|
| Pool de opciones | [ ]% | | | | |

*El reparto incluye el pool y suma 100%; simúlalo con `scripts/cap_table.py` (TPL-091). Partes iguales con dedicaciones distintas es la fuente clásica de conflicto.*

### 3. Salida y conflictos
- **Good leaver** (enfermedad, despido sin causa, mutuo acuerdo): [qué conserva y a qué precio se recompra lo no consolidado]
- **Bad leaver** (renuncia antes de [ ] meses, incumplimiento grave, competencia): [ ]
- **Empates y conflictos:** [mediación → arbitraje, plazo] · **Decisiones que requieren unanimidad:** [ ]
- **No competencia y confidencialidad:** [plazo y alcance razonables]

### 4. Propiedad intelectual
| Activo (código, marca, dominio, datos, diseños) | Titular hoy | ¿Cedido a la SpA? | Documento | ID |
|---|---|---|---|---|

Contratos laborales previos de cada socio revisados (cláusulas de PI o no competencia): [sí/no, quién]

### 5. Lista para el pacto de accionistas
[ ] vesting y recompra · [ ] derecho de preferencia · [ ] tag along / drag along · [ ] administración o directorio · [ ] no competencia · [ ] resolución de conflictos · [ ] socio que deja de trabajar · [ ] fecha de reunión con abogado

## Ejemplo bueno (ficticio)
MuelleSur SpA: coordinación de carga para pymes exportadoras de San Antonio.
| Socio | Rol | Dedicación | % | Vesting / cliff | Inicio |
|---|---|---|---|---|---|
| Ana | CEO, ventas y finanzas | 45 h desde 2026-09 | 45% | 48 / 12 | 2026-09-01 |
| Bruno | CTO, producto | 45 h desde 2027-01 (hoy empleado) | 45% | 48 / 12 | 2027-01-01 |
| Pool | asesora portuaria (1%) y primeros empleados | — | 10% | 24 / 6 | al asignar |
- PI: el prototipo que Bruno escribió en 2026 se cede a la SpA (IP-001, contrato de cesión); su contrato laboral solo protege trabajos del empleador (EV-004).
- Good leaver: conserva lo consolidado; bad leaver (renuncia antes de 24 meses): recompra de todo a valor nominal.
- Empate: mediación de 30 días y luego arbitraje. Unanimidad para: nuevos socios, deuda > 500 UF, venta de la PI.
- Acordado el 2026-12-05 (DEC-003); reunión con abogado para el pacto: 2027-01-15.

## Ejemplo malo y por qué falla
> Somos 3 amigos, 33/33/33, todos igual de comprometidos; no necesitamos papeles. El código está en el GitHub personal de Pedro. Lo formalizamos cuando llegue un inversionista.
- Partes iguales sin vesting: si uno se va en el mes 4, se lleva un tercio sin seguir trabajando.
- La PI no es de la SpA: un inversionista lo detecta en la due diligence (TPL-092) y frena la ronda.
- Sin reglas de salida, el conflicto se negocia cuando ya hay desconfianza.

## Criterio de aceptación
- Cada socio tiene rol, dedicación en horas y fecha de inicio.
- El reparto suma 100% con el pool incluido y está simulado con `scripts/cap_table.py`.
- Vesting, cliff, good/bad leaver y precio de recompra están escritos.
- Toda PI está cedida a la SpA o registrada en `bitacora.csv` (tipo ip) con fecha de regularización.
- `decisiones.csv` registra el acuerdo y la fecha de revisión del pacto con abogado.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
