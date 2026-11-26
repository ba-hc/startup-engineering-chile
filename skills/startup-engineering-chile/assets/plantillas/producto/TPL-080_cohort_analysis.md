# TPL-080 — Análisis de cohortes de clientes (Cohort Analysis)

> **Para qué sirve:** Medir la retención de clientes y de ingresos por grupo que empezó a pagar el mismo mes, para ver si el producto retiene mejor con el tiempo y alimentar el churn y el LTV con datos observados.
> **Cuándo NO usarla:** Con menos de 3 cohortes o cohortes de 1–3 clientes, donde un solo caso mueve 30 puntos; ahí lista cliente por cliente y explica cada baja.
> **Micro-ejemplo resuelto:** La cohorte de enero (20 clientes) retiene 70% al mes 3 y la de abril (25 clientes), con onboarding guiado, 84%; la retención neta de ingresos de enero es 82% porque 4 de los 14 que siguen subieron de plan.

**Gate:** G8 (también G4 con los primeros clientes) · **Alimenta:** `bitacora.csv` (tipo cohorte y kpi), `decisiones.csv`

## Completar
**Definiciones (fíjalas antes de mirar):** cohorte = [mes del primer pago] · cliente activo = [pagó en el mes / usó X veces] · ingreso = [neto, sin IVA ni setup] · fuente = [facturación, pasarela de pago, CRM] · fecha de corte [ ]
*Cada cohorte es una entrada de `bitacora.csv` (tipo cohorte, COH-001…) con sus valores en `datos`.*

### 1. Retención de clientes (% de la cohorte que sigue activa)
| Cohorte | N inicial | M1 | M2 | M3 | M6 | M12 |
|---|---|---|---|---|---|---|

### 2. Retención neta de ingresos (NRR: ingreso del mes ÷ ingreso inicial de la cohorte)
| Cohorte | MRR inicial | M1 | M3 | M6 | M12 |
|---|---|---|---|---|---|

### 3. Lectura
¿Las cohortes nuevas retienen mejor que las antiguas? [ ] · ¿La curva se aplana? ¿En qué mes y nivel? [ ] · Bajas y motivo por cliente [ ] · Churn mensual para TPL-087: [rango y meses usados]
*Cohortes con N < 10: marca "indicativa". No mezcles segmentos con comportamientos distintos en la misma fila.*

## Ejemplo bueno (ficticio)
ClaseViva SpA: reservas y cobro para estudios de yoga y pilates; plan $45.000/mes neto. Activo = pagó el mes. Fuente: pasarela de pago (EV-101). Corte 2027-09-30.
| Cohorte | N | M1 | M2 | M3 | M6 |
|---|---|---|---|---|---|
| Ene | 12 | 83% | 75% | 75% | 67% |
| Feb | 9 (indicativa) | 89% | 78% | 67% | 67% |
| Mar | 15 | 87% | 80% | 73% | 73% |
| Abr (onboarding guiado) | 18 | 94% | 89% | 83% | — |
| May | 21 | 95% | 90% | 86% | — |

- La curva se aplana desde M3 en ~67–75%; las cohortes con onboarding retienen 9–15 puntos más en M2.
- 17 bajas: 9 por cierre del estudio (no controlable), 6 por precio, 2 por falta de app.
- Churn mensual M3–M6: 1 baja en 78 clientes-mes (1,3%), con solo 3 cohortes → TPL-087 usa un rango de 1–4%.

## Ejemplo malo y por qué falla
> Churn 2% mensual (bajas del mes ÷ clientes totales). Tenemos 200 usuarios registrados y 90% de retención.
- Mezcla clientes nuevos y antiguos: una base que crece esconde la fuga de las primeras cohortes.
- "Usuarios registrados" no son clientes activos ni pagadores, y no hay definición de activo.
- Sin tabla por cohorte no se ve si la curva se aplana ni si los cambios al producto ayudaron.

## Criterio de aceptación
- Las definiciones de cohorte, activo e ingreso se fijaron antes y tienen fuente.
- Cada cohorte muestra su N inicial; las de N < 10 están marcadas como indicativas.
- Retención de clientes e ingresos van por separado y cada baja tiene motivo.
- El churn que usa TPL-087 sale de esta tabla y está en `bitacora.csv` (tipo cohorte).

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
