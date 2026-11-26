# TPL-030 — Tamaño de mercado bottom-up (TAM / SAM / SOM)

> **Para qué sirve:** Dimensionar el mercado contando cuentas reales × precio anual, con fuente de cada conteo y un SOM limitado por capacidad.
> **Cuándo NO usarla:** Para decidir si el problema existe o si alguien pagará: el tamaño de mercado no reemplaza la evidencia de G1, y en G0 basta un orden de magnitud.
> **Micro-ejemplo resuelto:** 1.200 ópticas en Chile (conteo por rubro, supuesto) × 24 UF/año = 28.800 UF de TAM; el SAM son 480 ópticas independientes de la RM y Valparaíso = 11.520 UF; con un vendedor que cierra 4 al mes, el SOM a 18 meses es ~70 ópticas ≈ 1.680 UF/año.

**Gate:** G2 · **Alimenta:** `evidencias.csv`, `bitacora.csv` (tipo fuente), `hipotesis.csv`

## Completar
**Unidad económica:** [empresa (RUT) / local / faena / hogar] · **Precio anual neto de referencia:** [CLP sin IVA, de qué sale: alternativa actual, entrevistas, prueba de precio] · **Año y moneda:** [ ]
*Desduplica: una empresa con 3 locales que compra centralizado es 1 cuenta, no 3.*

| Nivel | Definición / filtro aplicado | N° cuentas | Fuente del conteo (ID, año) | Precio anual neto | Valor anual |
|---|---|---|---|---|---|
| TAM | todas las unidades que podrían tener el problema | | | | |
| SAM | filtro 1: [ ] | | | | |
| | filtro 2: [ ] | | | | |
| SOM [horizonte] | mín(capacidad comercial, capacidad operacional, SAM) | | cálculo abajo | | |

**Capacidad comercial:** [personas] × [reuniones/mes] × [tasa de cierre] × [meses] = [ ]
**Capacidad operacional:** [implementaciones/mes] × [meses] = [ ]
**Sensibilidad:** tasa de cierre baja / base / alta → SOM [ ] / [ ] / [ ]
**Control top-down (solo para contrastar, nunca como cálculo):** [ ]

## Ejemplo bueno (ficticio — conteos ilustrativos, no son datos oficiales)
Proyecto "Repón" — reposición de stock para ferreterías independientes. Unidad: empresa con 1–3 locales. Precio: $45.000 + IVA/mes = $540.000 neto/año (H-007, prueba de precio con 10 dueños, EV-022).

| Nivel | Filtro | Cuentas | Fuente | Valor anual neto |
|---|---|---|---|---|
| TAM | empresas con giro de venta minorista de ferretería | 5.800 | EV-020, estadísticas de empresas por rubro del SII, último año disponible | $3.132 M |
| SAM | solo tramos pequeña y mediana | 2.100 | EV-021, mismo dataset por tramo de ventas | — |
| | con punto de venta que exporta ventas (6 de 10 entrevistados) | 1.260 | EV-023, nivel 3, supuesto 60% | $680,4 M |
| SOM 24 meses | mín(72; 144; 1.260) | 72 | cálculo | $38,9 M |

- Comercial: 1 fundador × 20 demos/mes × 15% cierre (supuesto) × 24 meses = 72 cuentas.
- Operacional: 6 implementaciones/mes × 24 = 144.
- Sensibilidad: cierre 10% / 15% / 20% → 48 / 72 / 96 cuentas → $25,9 M / $38,9 M / $51,8 M.
- Control: 72 cuentas = 5,7% del SAM en 2 años; plausible solo si el canal de distribuidores funciona.

## Ejemplo malo y por qué falla
> "El retail en Chile vende miles de millones de dólares al año (TAM). El software para retail en LATAM vale US$ 5.000 millones (SAM, informe global). Si capturamos solo el 1%, son US$ 50 millones (SOM)."
- Top-down: confunde facturación del sector con gasto en tu producto.
- Sin unidad, número de cuentas ni precio: no se puede reproducir.
- Un informe de LATAM no prueba nada sobre el mercado chileno servible.
- El 1% es arbitrario: el SOM no sale de la capacidad comercial ni operacional.

## Criterio de aceptación
- Cada nivel = N° de cuentas × precio anual neto, con IVA tratado explícitamente.
- Cada conteo y cada filtro tiene fuente con ID y año, o está marcado "supuesto".
- El SOM es el mínimo de capacidad comercial, operacional y SAM, con horizonte.
- Hay sensibilidad con al menos tres escenarios del supuesto más débil.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
