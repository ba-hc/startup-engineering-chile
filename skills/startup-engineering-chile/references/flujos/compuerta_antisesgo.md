# Compuerta antisesgo (antes de una decisión costosa o irreversible)

Úsala cuando el fundador está por: renunciar a su empleo, pagar a una agencia o desarrollador, firmar un arriendo, regalar un piloto sin fecha de cierre, contratar, o poner ahorros. Es corta y brutalmente honesta.

## Pasos
1. **Nombra la decisión y su costo** (dinero, meses, costo de oportunidad) y si es reversible.
2. **Lee el expediente**: `expediente.py ver hipotesis` y `ver evidencias`. ¿Qué hipótesis tiene que ser cierta para que la decisión valga la pena?
3. **Separa la evidencia en tres tipos**:
   - *Cumplidos*: "me encanta", "avísame cuando esté", likes, encuestas de intención. **No cuentan.**
   - *Compromisos reales*: tiempo (otra reunión con el decisor, acceso a datos), reputación (presentarte a su jefe) o dinero (preventa, piloto pagado, orden de compra).
   - *Resultados*: uso medido, pago recurrente, retención.
4. **Compara con un umbral fijado ahora**, antes de mirar de nuevo los datos (p. ej. "renuncio si hay ≥3 pilotos pagados o $X de preventa"). Regístralo como experimento si aún no existe.
5. **Pérdida aceptable** (TPL-036): ¿cuánto puede perder sin dañar su vida? Si la decisión excede eso, achícala.
6. **Veredicto**:
   - **Go**: hay compromisos reales que superan el umbral y el costo está dentro de la pérdida aceptable.
   - **Hold**: falta un compromiso concreto; define el más barato que lo resolvería y su plazo.
   - **Kill / no ahora**: la evidencia son cumplidos o la decisión excede la pérdida aceptable.
7. Registra: `expediente.py add decisiones gate=<gate> decision=<Go|Hold|Kill> criterio="<umbral>" evidence_ids=… justificacion=…`.

Ejemplos de achicar: en vez de pagar una app completa, un prototipo no-code + 3 pilotos manuales; en vez de renunciar, 2 días a la semana durante 8 semanas con un criterio de salida; en vez de piloto gratis, piloto con precio simbólico y fecha de decisión firmada.
