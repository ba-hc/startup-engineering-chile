# TPL-058 — Caso de negocio y ROI para el comprador (Business Case / ROI)

> **Para qué sirve:** Calcular con números del cliente cuánto gana o ahorra al comprar, separando caja de capacidad liberada, para que el sponsor lo defienda ante finanzas.
> **Cuándo NO usarla:** Si no tienes la línea base del cliente (horas, mermas, multas, kilómetros) o si la compra es tan pequeña que nadie la evalúa con planilla; un ROI armado con supuestos propios no convence a finanzas.
> **Micro-ejemplo resuelto:** Una planta pierde 18 h/mes de línea detenida a $350.000 la hora ($6,3 M/mes); si el sistema evita un tercio (6 h, $2,1 M/mes) y cuesta 30 UF/mes (≈ $1,2 M), el beneficio neto en caja es ≈ $0,9 M/mes.

**Gate:** G4 (–G7) · **Alimenta:** `evidencias.csv`, `cuentas_y_pipeline.csv`, `hipotesis.csv`

## Completar
**Cuenta:** [CTA-] · **Quién valida los números del lado del cliente:** [rol] · **Moneda:** CLP neto; IVA solo si el cliente no lo recupera
| Concepto | Fórmula | CLP/año | Fuente [dato del cliente / EV- / supuesto] |
|---|---|---|---|
| Línea base del problema | [volumen × costo unitario] | | |
| Mejora esperada | [% de un piloto o caso comparable] | | |
| Beneficio en caja | [gasto que deja de pagarse] | | |
| Capacidad liberada (no es caja) | [horas × costo, solo si se reasignan] | | |
| Costo total para el cliente | [licencia + implementación + horas internas] | | |
| Beneficio neto en caja | [beneficio en caja − costo total] | | |
| Payback | [inversión inicial ÷ beneficio neto mensual] | meses | |

| Escenario | Mejora | Beneficio neto año 1 | Payback |
|---|---|---|---|
| Conservador | | | |
| Base | | | |
| Optimista | | | |

*Presenta el conservador. Si no cierra, el caso no cierra.* · Riesgos para el cliente [implementación, adopción, dependencia]: [ ]

## Ejemplo bueno (ficticio)
RutaLibre SpA: ruteo de despacho para una distribuidora de bebidas con 14 camiones en Concepción (CTA-021).
- Línea base: 14 camiones × 22 días × 180 km = 55.440 km/mes × $650/km (combustible, neumáticos y mantención, según contabilidad del cliente, EV-121) ≈ $36,0 M/mes.
- Mejora: el piloto con 2 camiones redujo 8% los km (EV-122). Conservador 4%, base 8%, optimista 11%.
- Costo: 14 × 1,2 UF/mes ≈ $0,67 M/mes; implementación 25 UF (≈ $1,0 M) y 20 h internas (≈ $0,4 M).
- Conservador: ahorro $1,44 M/mes = $17,3 M/año; costo año 1 ≈ $9,5 M; beneficio neto ≈ $7,8 M; payback 1,8 meses.
- Capacidad liberada: 1,5 h diarias del planificador, que se reasignan a cobranza (no se suma a la caja).
- Números validados por el jefe de finanzas del cliente el 2027-06-20.

## Ejemplo malo y por qué falla
> Con nuestra solución ahorrará 30% de sus costos logísticos y 500 horas al año, equivalentes a $50 M. ROI de 900%.
- El 30% no tiene línea base del cliente ni piloto que lo respalde.
- Suma horas como caja: solo ahorran si se dejan de pagar o se reasignan.
- No incluye implementación ni horas internas, no tiene escenario conservador y nadie del cliente lo validó.

## Criterio de aceptación
- La línea base usa datos del cliente o EV-, y la mejora conservadora tiene respaldo de piloto o caso.
- Caja y capacidad liberada van en líneas separadas.
- El costo total incluye implementación y horas internas del cliente.
- El escenario conservador cierra y una persona del cliente validó los números.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
