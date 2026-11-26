# TPL-031 — Benchmark competitivo (Competitive Benchmark)

> **Para qué sirve:** Comparar la oferta con las alternativas reales del cliente en la misma tarea, separando lo demostrado de lo declarado.
> **Cuándo NO usarla:** Como lista de logos para el pitch, o antes de saber qué tarea quiere resolver el cliente; sin tarea definida, cualquier comparación es arbitraria.
> **Micro-ejemplo resuelto:** Para "cuadrar la caja diaria de un minimarket", la planilla actual toma 25 min/día y cuesta $0; un software extranjero toma 8 min pero cuesta $45.000/mes y no emite boleta electrónica chilena; el prototipo propio toma 10 min (medido en 3 locales) a $19.990/mes.

**Gate:** G3 · **Alimenta:** `competencia.csv`, `evidencias.csv`

## Completar
**Tarea de referencia** (la misma para todas las alternativas, p. ej. "cuadrar el stock de 3 tiendas al cierre de mes"): [ ]

*Incluye siempre "no hacer nada" o "in-house": suele ser el competidor más fuerte. Guarda cada página consultada con URL y fecha (`firecrawl.py` o `investigacion/`).*

| Dimensión | Nuestra oferta | Alternativa 1 | Alternativa 2 | No hacer nada / in-house |
|---|---|---|---|---|
| Nombre, URL y fecha de consulta | | | | |
| Tipo (directo / indirecto / servicio / in-house) | | | | |
| Segmento al que apunta | | | | |
| Precio (moneda, unidad, IVA) | | | | |
| Capacidad para la tarea de referencia | | | | |
| Integración / costo de cambio | | | | |
| Canal de venta | | | | |
| Ventaja (declarada / verificada) | | | | |
| Limitación (observada / inferida) | | | | |
| Evidencia (COMP-ID / EV-ID / URL) | | | | |

**Lectura**
- Condiciones mínimas (lo que todos tienen y el cliente da por hecho): [ ]
- Diferencias demostrables (con evidencia): [ ]
- Diferencias por demostrar (hipótesis H-ID y cómo probarlas): [ ]

## Ejemplo bueno (ficticio)
"StockSimple", inventario para minimarkets con 2–4 locales, Gran Concepción. Tarea: cuadrar el stock semanal de 3 locales.
| Dimensión | StockSimple | ERP genérico pyme | Planilla compartida (in-house) |
|---|---|---|---|
| Precio | $39.000 + IVA/mes (supuesto, H-004) | $89.000 + IVA/mes, sitio consultado 12-11-2026 (COMP-002) | $0 + 5 h/semana del dueño (ENT-003, ENT-006) |
| Capacidad para la tarea | Prototipo: 40 min en piloto con 1 local (EV-008, n=1) | Lo hace, con 2 días de configuración (ENT-004) | 4–6 h, con errores de digitación (ENT-003) |
| Ventaja | Lectura de factura con foto (declarada, por probar) | Contabilidad integrada (verificada) | Gratis y conocida (verificada) |
| Limitación | Sin contabilidad (observada) | Requiere capacitación; 2 de 6 la abandonaron (ENT-002, 004) | No muestra quiebres de stock (observada) |

Lectura: el rival real es la planilla. La diferencia demostrable es el tiempo (n=1, insuficiente). Por demostrar: 40 min con 5 locales (H-005, EXP-003).

## Ejemplo malo y por qué falla
| | Nosotros | Competidor A | Competidor B |
|---|---|---|---|
| Fácil de usar | ✅ | ❌ | ❌ |
| Innovador | ✅ | ❌ | ✅ |
| Precio | Barato | Caro | Caro |

- Las casillas son opiniones propias: no hay tarea de referencia, fuente ni fecha.
- Falta la alternativa "no hacer nada" o in-house.
- "Barato" y "caro" sin moneda, unidad ni IVA no se pueden comparar.

## Criterio de aceptación
- Hay una tarea de referencia y todas las alternativas se evalúan en ella.
- Se incluye "no hacer nada" o in-house.
- Cada precio tiene moneda, unidad, IVA y fecha de consulta; cada ventaja dice si está verificada o es declarada.
- Las diferencias "por demostrar" tienen una hipótesis y un experimento asociados.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
