# TPL-061 — Tarjeta de experimento (Experiment Canvas / Test Card)

**Para qué:** dejar escrito, antes de mirar un dato, qué se prueba, cómo se mide, qué umbral decide y qué se hará con cada resultado. · **Gate:** G1–G7 · **Alimenta:** `experimentos.csv`, `evidencias.csv`, `decisiones.csv`

## Completar
*Los pasos 1–6 se firman (fecha y responsable) antes de lanzar. Después solo se llena el 7.*

1. **Creemos que** [segmento] **hará** [comportamiento observable] **porque** [razón]. H-ID: [ ]
2. **Para verificarlo:** [método: entrevista, landing con pago, concierge, preventa, demo, PoC] con [población y canal de reclutamiento]. Comparador: [línea base, grupo control o ninguno, y por qué]
3. **Mediremos:** primaria [numerador / denominador]; diagnósticas [ ]; guardrail [lo que no puede empeorar]
4. **Acertamos si** [umbral] en [plazo]. Tamaño de muestra: [n mínimo y por qué]. *Con n < 20, informa conteos ("4 de 15"), no porcentajes ni significancia.*
5. **Reglas de decisión:**

| Resultado | Decisión |
|---|---|
| ≥ umbral | Go: [ ] |
| Zona gris [rango] | Hold / Recycle: [ ] |
| < mínimo | Kill / Recycle: [ ] |

6. **Costo máximo** [CLP y horas] · **Inicio / fin** [ ] · **Responsable** [ ] · **Firmado el** [fecha]
7. **Resultado** (solo después): [dato observado, n, EV-ID, qué no esperábamos]

*Un clic, un "me interesa" o un correo dejado no son ventas: si la hipótesis es de pago, la métrica es pago o compromiso.*

## Ejemplo bueno (ficticio)
"LimpiaSofá", limpieza de tapices a domicilio, Ñuñoa y Providencia. EXP-004 · H-006.
1. Hogares que ya contrataron una limpieza puntual pagarán una suscripción semestral (2 visitas) de $54.990 IVA incluido, porque repiten cada 4–6 meses (EV-015).
2. Preventa por WhatsApp a los 60 clientes de los últimos 12 meses (base propia). Línea base: 0 suscripciones; sin grupo control.
3. Primaria: pagos completados / clientes contactados. Diagnósticas: tasa de respuesta, objeción principal. Guardrail: ≤3 de 60 piden no ser contactados.
4. Acertamos si ≥9 de 60 pagan en 14 días. n = 60 es toda la base; se reporta como conteo.
5. ≥9 → Go: canal pagado con CAC máx. $12.000 · 4–8 → Hold: probar $44.990 con otros 60 · ≤3 → Kill a la suscripción, seguir con servicio puntual.
6. Costo máx. $80.000 + 6 h de la fundadora · 3–17 nov 2026 · Responsable: cofundadora comercial · Firmado el 30-10-2026.
7. Resultado: 7 de 60 pagaron (EV-019); 11 respondieron "en marzo". → Hold, según la regla.

## Ejemplo malo y por qué falla
"Hipótesis: a la gente le gustará la suscripción. Lanzamos una landing y medimos interés. Meta: 20% de conversión." Resultado: 8% dejó su correo. "Ajustamos la meta a 5% porque el mercado es nuevo: experimento exitoso, Go."
- La meta se bajó después de ver los datos: el resultado ya no prueba nada.
- "Interés" y correo dejado no miden pago; no hay denominador ni tamaño de muestra.
- No había reglas de decisión, costo máximo ni plazo antes de lanzar.

## Criterio de aceptación
- Hipótesis, métrica primaria (numerador y denominador), umbral, muestra y reglas de decisión tienen fecha de firma anterior al inicio.
- Si la hipótesis es de pago, la métrica es pago o compromiso verificable.
- Hay guardrail, costo máximo y responsable.
- El resultado está en `experimentos.csv` con EV-ID, y la decisión es la que dicta la regla o `decisiones.csv` explica por qué no.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
