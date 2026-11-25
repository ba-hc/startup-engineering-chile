# TPL-106 — Marco lógico y Gantt (Logical Framework)

**Para qué:** encadenar fin, propósito, componentes y actividades con indicador, verificación, plazo y cuenta, de modo que cada actividad tenga gasto y cada gasto una actividad. · **Gate:** transversal (fondos: formulación) · **Alimenta:** `rendiciones.csv`, `indicadores.csv`, `riesgos.csv`

## Completar
**Lógica vertical** (componente = resultado, no tarea)
| Nivel | Resumen narrativo | Indicador (línea base → meta) | Medio de verificación | Supuesto |
|---|---|---|---|---|
| Fin | [ ] | | | |
| Propósito | [ ] | | | |
| C1 | [ ] | | | |

**Actividades y Gantt** (esta tabla la lee `fondos_lint.py coherencia`)
| Actividad | Componente | Indicador | Medio de verificación | Supuesto | Mes inicio | Mes fin | Cuenta presupuestaria |
|---|---|---|---|---|---|---|---|
| [A1.1 …] | [C1] | | | | | | [según bases vigentes] |

*No cambies el encabezado `Actividad` y escribe cada una con el mismo texto que su fila en `rendiciones.csv` (el script exige ≥ 60% de palabras en común). Una actividad por fila.*
*Ninguna actividad termina después del plazo del convenio; "gestión" o "difusión" también necesitan gasto o se eliminan.*
*Al copiar la plantilla, borra los ejemplos.*
Revisión: `python scripts/fondos_lint.py coherencia --marco expediente/documentos/TPL-106_marco_logico_y_gantt.md --dir .`

## Ejemplo bueno (ficticio)
OxiMar: boyas de oxígeno disuelto con alertas para centros de cultivo de mejillón en Chiloé; 8 meses.

| Nivel | Resumen narrativo | Indicador | Verificación | Supuesto |
|---|---|---|---|---|
| Fin | Menor mortalidad por eventos de bajo oxígeno | mortalidad por evento (seguimiento posterior) | informes de centros | — |
| Propósito | Alertas validadas técnica y comercialmente | 3 centros las usan; ≥ 1 compra | informe final y OC | sin cierre sanitario en la temporada |
| C1 | Boya prototipo validada | datos válidos ≥ 95% del tiempo, 60 días | registro de datos | acceso a balsas |
| C2 | Piloto de alertas | reacción 6 h (EV-071) → ≤ 1 h | bitácora del centro | el jefe de centro responde |

| Cód. | Qué se hace | Comp. | Indicador | Verificación | Meses | Cuenta | Gasto |
|---|---|---|---|---|---|---|---|
| A1.1 | Fabricación de 3 boyas prototipo | C1 | 3 boyas operando | acta de prueba | 1–3 | Operación | GAS-001 |
| A1.2 | Calibración de sensores en laboratorio | C1 | error ≤ 0,3 mg/L | informe | 2–3 | Operación | GAS-002 |
| A2.1 | Piloto de alertas en 3 centros de cultivo | C2 | 3 centros, 60 días | bitácoras | 4–7 | Operación | GAS-003 |

*Aquí la columna se llama "Qué se hace" para que el script no lea el ejemplo; en tu tabla va `Actividad`.*

## Ejemplo malo y por qué falla
> Actividades: desarrollo, marketing, gestión del proyecto y ventas. Plazo: 8 meses. Indicador: 100% de avance.
- Tareas genéricas sin componente, resultado ni medio de verificación.
- "Gestión del proyecto" no tiene gasto (`coherencia` → actividad sin presupuesto).
- Sin mes de inicio y fin: no hay cronograma ejecutable.
- "100% de avance" mide proceso, no resultado, y no hay supuestos.

## Criterio de aceptación
- Cada componente tiene indicador con línea base y meta, verificación y supuesto.
- Toda actividad tiene componente, mes de inicio y fin dentro del convenio y cuenta.
- `fondos_lint.py coherencia` termina sin PROBLEMA y los AVISO están revisados.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
