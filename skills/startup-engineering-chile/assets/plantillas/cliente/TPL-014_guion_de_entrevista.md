# TPL-014 — Guion de entrevista de descubrimiento (Mom Test)

> **Para qué sirve:** Obtener hechos del pasado sobre el problema, sin vender ni pedir opinión sobre la idea.
> **Cuándo NO usarla:** En una reunión comercial con un comprador que ya reconoce el problema y pide propuesta; ahí corresponde vender y negociar, no hacer descubrimiento.
> **Micro-ejemplo resuelto:** En lugar de "¿usarías una app para controlar mermas?", se pregunta "¿cuándo fue la última vez que botaron mercadería vencida y cuánto fue?"; la jefa de local responde "el lunes, unos $85.000 en lácteos", un hecho que se registra como evidencia.

**Gate:** G1 · **Alimenta:** `entrevistas.csv`, `evidencias.csv`

## Completar
**Hipótesis que pone a prueba:** [H-xxx] · **A quién:** [rol, segmento, criterio de inclusión] · **Duración:** 30–40 min · **Entrevistas meta:** [N por segmento]

**Apertura y consentimiento (leer tal cual):** "Estoy investigando cómo se hace hoy [proceso]. Tomaré notas sin tu nombre ni datos de contacto, solo para este estudio; puedes pedirme que las borre cuando quieras. ¿Te parece bien?" → si dice sí, `consentimiento=si`.

| Bloque | Preguntas (sobre hechos y pasado) | H-xxx |
|---|---|---|
| Contexto | ¿Cómo es un día/semana normal en [proceso]? ¿Quién más participa? | |
| Última vez | Cuéntame la última vez que pasó [problema]. ¿Qué hiciste, paso a paso? | |
| Alternativa | ¿Cómo lo resuelven hoy? ¿Qué herramienta, persona o servicio usan? | |
| Costo | ¿Cuánto tiempo o dinero te costó esa vez? ¿Cada cuánto ocurre? | |
| Intentos previos | ¿Han probado otra forma? ¿Qué pasó? ¿Cuánto pagaron? | |
| Decisión | La última vez que compraron algo para esto, ¿quién lo aprobó y cómo? | |
| Cierre | ¿Con quién más debería hablar? ¿Me podrías mostrar [documento, planilla]? | |

*Prohibidas: "¿Usarías…?", "¿Pagarías…?", "¿Te parece buena idea…?". Cámbialas por "¿Qué hiciste la última vez…?" y "¿Cuánto gastaste en…?". No muestres la solución antes del cierre.*

**Qué traer de vuelta:** hechos con número y denominador, citas breves (≤15 palabras), contradicciones, quién decide. Registro como ENT-xxx + rol + segmento; sin nombre, teléfono, RUT ni razón social.

## Ejemplo bueno (ficticio)
Proyecto "Retorno" — cobro de fletes de transportistas pyme (1–10 camiones), Biobío.
- H-002: ≥5 de 8 dueños cobraron al menos una factura >45 días tarde por guía de despacho perdida o rechazada en los últimos 3 meses.
- A quién: dueño que factura; excluye empresas con área de cobranza.
- Última vez: "Cuéntame la última factura que te rechazaron o pagaron tarde. ¿Qué faltaba?"
- Proceso: "¿Qué pasa con la guía firmada desde que el chofer descarga hasta que facturas?"
- Costo: "¿Cuántos días pasaron entre la entrega y el pago? ¿Cómo cubriste el combustible mientras?"
- Decisión: "La última vez que contrataron un servicio para la oficina, ¿quién lo decidió?"
- Cierre: "¿Me mostrarías una guía rechazada, con los datos tapados?" · "¿Con qué otro transportista hablo?"

## Ejemplo malo y por qué falla
> 1. ¿Te parece útil una app para digitalizar guías? 2. ¿La usarías todos los días? 3. ¿Cuánto pagarías al mes? 4. Déjame tu nombre, teléfono y empresa para avisarte cuando salga.
- Preguntas hipotéticas sobre el futuro: dan respuestas amables, no evidencia.
- Presenta la solución al inicio: el descubrimiento se vuelve pitch.
- No pregunta por la última vez, el costo ni quién decide.
- Pide datos personales sin consentimiento ni finalidad.

## Criterio de aceptación
- Al menos 80% de las preguntas piden hechos pasados (última vez, cuánto, quién).
- Ninguna pregunta antes del cierre menciona la solución o la empresa del fundador.
- Cada bloque está ligado a una H-xxx con umbral fijado antes de entrevistar.
- Incluye la frase de consentimiento y el formato ENT-xxx sin datos personales.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
