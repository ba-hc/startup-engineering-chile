# TPL-036 — Pérdida aceptable (Affordable Loss)

> **Para qué sirve:** Fijar, antes de experimentar, cuánto tiempo, dinero y costo de oportunidad estás dispuesto a perder y qué señales te hacen parar.
> **Cuándo NO usarla:** Para decisiones pequeñas y reversibles (un experimento de $50.000 o una tarde de trabajo), donde calcular la pérdida tarda más que asumirla.
> **Micro-ejemplo resuelto:** Una fundadora con $6.000.000 ahorrados fija como máximo $2.500.000 y 5 meses a media jornada; si en el mes 3 no tiene 3 clientes pagando, vuelve a jornada completa en su empleo.

**Gate:** G0 (se revisa en cada gate) · **Alimenta:** `decisiones.csv`, `experimentos.csv`

## Completar
*La pregunta no es "¿cuánto puedo ganar?", sino "si pierdo todo esto, ¿sigo bien?"*

**Medios disponibles:** quién soy [ ] · qué sé [ ] · a quién conozco [ ]

| Recurso | Disponible | Máximo que acepto perder | Quién más lo aprueba |
|---|---|---|---|
| Dinero (CLP) | | | [socio, pareja] |
| Horas por semana | | | |
| Plazo total (semanas) | | | |
| Costo de oportunidad (sueldo, bono, ascenso) | | | |
| Relaciones y reputación | | | |

**Lo que NO se arriesga:** [ahorro de emergencia, deuda personal, renunciar antes de X]

**Qué compra ese límite**
| EXP-xxx | Prueba | `costo_maximo_CLP` | Qué aprendo si sale mal |
|---|---|---|---|

**Puntos de control y umbrales de parada (fijados hoy):**
| Fecha | Señal medible | Si se cumple | Si no |
|---|---|---|---|

*Mover un umbral después de ver el resultado es gastar más allá del límite sin decidirlo.*

## Ejemplo bueno (ficticio)
Proyecto "Acompaña" — coordinación de cuidadoras a domicilio para adultos mayores, Viña del Mar. Fundadora con empleo de jornada completa.
- Medios: enfermera con 8 años en un servicio de salud; red de 15 cuidadoras de confianza; sin experiencia comercial.
- Dinero: dispone $3.000.000, acepta perder $1.200.000; aprueba su pareja (ingreso compartido).
- Horas: 8 h/semana durante 12 semanas = 96 h.
- Costo de oportunidad: no renuncia ni reduce jornada en este período.
- No se arriesga: fondo de emergencia de 6 meses ni deuda con tarjeta.
- EXP-001: página simple + avisos locales, $300.000; si nadie pide cotización, el canal digital no sirve.
- EXP-002: servicio manual a 4 familias por 4 semanas, $600.000 de turnos de prueba (tarifa por hora: supuesto a validar); aprendo si pagan el precio completo.
- Reserva: $300.000 para imprevistos.
- Semana 6: ≥2 familias pagando precio completo → Go a semana 12; si no → Recycle (cambiar segmento) o Kill.
- Semana 12: ≥5 familias pagando 2 meses seguidos → recién ahí evaluar reducir jornada (DEC-002).

## Ejemplo malo y por qué falla
> "Voy a invertir lo que haga falta hasta que funcione. Renuncio el próximo mes para dedicarme 100%. Si en un año no resulta, veremos."
- Sin monto ni horas máximas: el límite se define por agotamiento, no por decisión.
- Renunciar es la apuesta más cara y llega antes de cualquier evidencia.
- "Veremos" no es un umbral: no hay señal medible ni fecha de control.
- Nadie más aprueba el riesgo, aunque afecte el ingreso del hogar.

## Criterio de aceptación
- Hay un monto en CLP y un número de horas máximos, escritos antes del primer experimento.
- La suma de `costo_maximo_CLP` de los EXP no supera el límite de dinero.
- Cada punto de control tiene fecha, señal medible y acción en ambos casos.
- Lo que no se arriesga está escrito y lo aprueba al menos otra persona afectada.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
