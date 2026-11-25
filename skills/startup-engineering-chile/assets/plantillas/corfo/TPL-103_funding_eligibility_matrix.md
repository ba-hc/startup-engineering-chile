# TPL-103 — Matriz de elegibilidad del fondo (Funding Eligibility Matrix)

**Para qué:** confirmar con las bases vigentes que el postulante es admisible antes de escribir la postulación. · **Gate:** transversal (fondos; antes de formular) · **Alimenta:** `corfo_elegibilidad.csv`, `evidencias.csv`

## Completar
**1. Datos del postulante** (con respaldo)
| Dato | Valor | Respaldo (ID) |
|---|---|---|
| Tipo de postulante [natural / jurídica] | | |
| Meses de inicio de actividades SII [a la fecha que fijen las bases] | | |
| Ventas netas últimos 12 meses (CLP) / ventas de la solución | | |
| Región · liderazgo femenino · base científica | | |

**2. Instrumento candidato** según etapa (`references/flujos/fondos.md`) y revisión previa:
`python scripts/fondos_lint.py elegibilidad --instrumento <clave> --tipo <natural|juridica> --meses-inicio N --ventas-12m CLP [--ventas-solucion CLP]` → pega la salida.

**3. Matriz** · Convocatoria: [ ] · Versión de bases: [fecha, URL, copia guardada]
| requisito | articulo_pagina | evidence_id | estado [CUMPLE / NO CUMPLE / FALTA DATO / VERIFICAR] | responsable | vencimiento | observacion |
|---|---|---|---|---|---|---|
| [ ] | | | | | | |

*Copia el requisito desde las bases del llamado, no desde la ficha web ni desde este pack.*
*Carta de intención ≠ venta facturada. No factures ni hagas preventas sin revisar su efecto en la elegibilidad.*
*Un NO CUMPLE o un FALTA DATO crítico detiene la formulación hasta resolverlo.*

## Ejemplo bueno (ficticio)
KineCasa SpA: teleorientación kinesiológica para adultos mayores; 9 meses de inicio de actividades, sin ventas (EV-051). Candidato: Semilla Inicia.
`fondos_lint.py elegibilidad --instrumento semilla_inicia --tipo juridica --meses-inicio 9 --ventas-12m 0` → CUMPLE tipo y antigüedad (< 18); VERIFICAR convocatoria y región, restricciones de participación y patrocinador.

articulo_pagina: [según bases vigentes].
| requisito | evidence_id | estado | responsable | vencimiento | observacion |
|---|---|---|---|---|---|
| Persona jurídica chilena | EV-050 | CUMPLE | socia A | — | escritura y e-RUT |
| < 18 meses de inicio de actividades | EV-051 | CUMPLE | socia A | — | recalcular al cierre |
| Sin ventas | EV-052 | CUMPLE | socia A | — | no emitir boletas antes de postular |
| Convocatoria abierta en la región | — | VERIFICAR | socio B | 2027-01-15 | las de 2026 cerraron |
| Sin incompatibilidad con otros proyectos CORFO | — | FALTA DATO | socio B | 2027-01-10 | un socio tiene otra SpA con proyecto CORFO |

Veredicto: no se formula hasta cerrar la incompatibilidad.

## Ejemplo malo y por qué falla
> Instrumento: Semilla Inicia. ¿Cumplimos? Sí, somos startup. Monto: $15M. Requisitos: los revisamos en la web. Ventas: 2 clientes piloto pagando, eso suma puntos.
- Con ventas, una persona jurídica no cumple la regla de referencia "sin ventas" de Inicia: el lint daría NO CUMPLE.
- Requisitos tomados de la ficha web, sin versión ni fecha de bases.
- Asume el tope de subsidio, sin cofinanciamiento ni aporte.

## Criterio de aceptación
- Cada requisito cita bases con fecha y URL y tiene `evidence_id` o estado FALTA DATO.
- La salida de `fondos_lint.py elegibilidad` está pegada y sus VERIFICAR tienen responsable y fecha.
- No queda ningún NO CUMPLE ni FALTA DATO crítico antes de formular.
- Filas registradas en `corfo_elegibilidad.csv`.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
