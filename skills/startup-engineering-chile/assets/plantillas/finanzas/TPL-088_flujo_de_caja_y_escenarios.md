# TPL-088 — Flujo de caja y escenarios (Cash Flow & Scenarios)

**Para qué:** saber en qué mes se acaba la caja con cobros reales, IVA y desfase de pago, y cuánto capital falta para el próximo hito. · **Gate:** G4 / G9 · **Alimenta:** `indicadores.csv`, `decisiones.csv`, `riesgos.csv`

## Completar
**Caja inicial:** [ ] al [fecha] · **Plazo de cobro:** [días, según contratos] · **Hito que la caja debe alcanzar:** [ ]
*Facturar ≠ cobrar. El IVA débito se devenga al facturar, aunque el cliente no haya pagado.*

| Mes | Clientes | Facturado neto | Cobrado (con IVA) | Pagos operativos (con IVA) | IVA F29 (débito − crédito del mes anterior) | Capital / deuda / subsidio | Caja final |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |

*El subsidio y el capital van en su columna, nunca como venta. Incluye la remuneración de los fundadores aunque hoy no la cobren.*

**Runway:** `python scripts/finanzas.py runway --caja C --gasto G --ingreso <cobrado, no facturado>`
**Escenarios:** `python scripts/finanzas.py escenarios --modelo expediente/entregables/modelo_financiero.xlsx` (o flags `--precio --fijos --altas --churn --caja --diferido`); pesimista y optimista son factores fijos, no probabilidades.
*El script trabaja en neto y con 1 mes de desfase: si cobras a 60+ días o el IVA pesa, manda la tabla mensual y se usa el peor de ambos.*
**Capital requerido:** [caja mínima del peor caso + colchón de [ ] meses de gasto]

## Ejemplo bueno (ficticio)
Refuerza: reforzamiento de matemáticas para colegios particulares subvencionados; $900.000 neto/mes por colegio (+IVA), cobro a 60 días (EV-044, 3 contratos), +1 colegio por mes (supuesto). Caja $18.000.000 (aporte de socios, EV-040). Pagos: $5.352.000 fijos (incluye $152.000 de IVA crédito) + $150.000 por colegio.

| Mes | Clientes | Facturado neto | Cobrado | Pagos | IVA F29 | Caja final |
|---|---|---|---|---|---|---|
| 1 | 4 | 3.600.000 | 0 | 5.952.000 | 0 | 12.048.000 |
| 2 | 5 | 4.500.000 | 0 | 6.102.000 | 532.000 | 5.414.000 |
| 3 | 6 | 5.400.000 | 4.284.000 | 6.252.000 | 703.000 | 2.743.000 |
| 4 | 7 | 6.300.000 | 5.355.000 | 6.402.000 | 874.000 | 822.000 |
| 5 | 8 | 7.200.000 | 6.426.000 | 6.552.000 | 1.045.000 | −349.000 |

- `escenarios` (neto, 1 mes de desfase, churn 2%): base sin quiebre en 12 meses; pesimista negativo en el mes 7. La tabla, con IVA y 60 días, quiebra en el mes 5: manda la tabla.
- Capital requerido: ≥ $14.000.000 antes del mes 4 (déficit del mes 6, $770.000, + 2 meses de gasto) o factoring (cotizar).

## Ejemplo malo y por qué falla
> Ingresos mes 1: $3.600.000; gastos: $5.952.000. Burn $2.352.000. Runway = $18.000.000 / $2.352.000 = 7,7 meses. Con el fondo CORFO de mes 6 llegamos al equilibrio.
- Usa lo facturado como cobrado: ignora 60 días sin caja.
- El IVA no aparece; desde el mes 2 sale caja todos los meses por F29.
- Cuenta un subsidio no adjudicado como ingreso que "llega al equilibrio".
- Un solo escenario, sin caja mínima ni capital requerido.

## Criterio de aceptación
- Cobrado y facturado van en columnas separadas, con el plazo de cobro de los contratos.
- El IVA débito y el crédito están modelados y se pagan el mes siguiente.
- Subsidio y capital están separados de las ventas y solo aparecen si están adjudicados o firmados.
- Hay tres escenarios del script y un capital requerido ligado a un hito con fecha.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
