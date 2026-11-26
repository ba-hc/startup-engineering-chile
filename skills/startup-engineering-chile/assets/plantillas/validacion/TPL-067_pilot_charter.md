# TPL-067 — Acta de piloto (Pilot Charter)

> **Para qué sirve:** Acordar con el cliente, antes del día 1, qué responde el piloto, cómo se mide, cuánto cuesta y qué pasa al final.
> **Cuándo NO usarla:** Si el cliente aún no reconoce el problema ni tiene presupuesto identificado; ahí falta descubrimiento, y el piloto será una demo larga.
> **Micro-ejemplo resuelto:** Piloto de 8 semanas en 2 sucursales de una cadena de farmacias por 90 UF + IVA; KPI: quiebres de stock (baseline 7,2% en 6 meses, meta ≤ 4%); si se cumple, OC anual por 30 sucursales a 1.400 UF + IVA.

**Gate:** G6 · **Alimenta:** `pilotos.csv`, `bitacora.csv` (tipo kpi), `cuentas_y_pipeline.csv`

## Completar
*Se firma por ambas partes antes de empezar. Sin sponsor, comprador, baseline y criterio de conversión no hay piloto, sino demo sin fin ("pilot purgatory").*

**Personas:** sponsor (dueño del problema, usa el resultado) [rol] · comprador (firma la OC, tiene presupuesto) [rol] · usuario operativo [rol] · responsable startup [ ]
**Pregunta del piloto:** [una sola, verificable: "¿reduce X en Y bajo condiciones Z?"]
**Alcance:** sitio o área [ ] · incluye / no incluye [ ] · datos e integración que aporta el cliente [ ] · confidencialidad y seguridad [ ]

| KPI-ID | Fórmula | Baseline (fuente, período) | Meta | Guardrail |
|---|---|---|---|---|

*Baseline medido antes y con la misma fórmula; si no existe, las primeras semanas son de medición.*
**Duración:** [semanas, fecha de inicio y de informe] · *Máx. una extensión, con motivo escrito.*
**Costo del piloto:** [monto neto + IVA, quién paga, hitos] · *Un piloto pagado, aunque sea en parte, prueba presupuesto.*
**Después del piloto:** precio de contrato [ ] · plazo de decisión del cliente [días tras el informe] · criterio de conversión [si KPI ≥ meta y guardrails ok → OC por (alcance) a (precio)] · si no se cumple [ ]

## Ejemplo bueno (ficticio)
"VibraCinta", sensores de vibración que anticipan fallas de polines en correas; faena de cobre mediana, Antofagasta. PIL-001 · CTA-003.
- Sponsor: superintendente de mantención · Comprador: gerente de operaciones (aprueba OC ≤1.500 UF, EV-021) · Usuario: planificador.
- Pregunta: ¿anticipa con ≥72 h las fallas de polines en la correa CV-2?
- Alcance: correa CV-2 (1,2 km), 40 sensores; el cliente entrega su bitácora de detenciones; los datos son suyos; sin integración a ERP.
- KPI-004: horas/mes de detención no programada por polines. Baseline 11,5 (bitácora 12 meses, EV-022). Meta ≤6 promedio meses 2–3. Guardrails: 0 incidentes de seguridad por instalación; ≤2 falsas alarmas/semana.
- Duración: 12 semanas, 4-11-2026 a 27-01-2027; informe el 3-02-2027.
- Costo: 180 UF + IVA, 50% al inicio; la startup pone el hardware.
- Conversión: si se cumplen meta y guardrails, OC anual por 3 correas a 1.150 UF + IVA dentro de 30 días del informe; si no, rechazo documentado, sin extensión gratis.

## Ejemplo malo y por qué falla
"Piloto gratuito de 3 meses en la planta para que conozcan la solución. Contacto: ingeniero de confiabilidad. Mediremos satisfacción. Si les gusta, conversamos un contrato."
- Gratis y sin comprador: nadie con presupuesto se compromete.
- Sin baseline ni KPI operacional; "satisfacción" no responde una pregunta de valor.
- "Si les gusta, conversamos" no es criterio de conversión: es la entrada al pilot purgatory.

## Criterio de aceptación
- Sponsor y comprador identificados por rol; la atribución de compra del comprador, verificada.
- Cada KPI tiene fórmula, baseline medido con fuente y meta numérica.
- Hay fecha de fin e informe, y el costo indica monto, IVA y quién paga.
- Precio posterior y criterio de conversión a contrato quedan escritos y firmados antes del día 1.
- Existe la fila en `pilotos.csv` con su cuenta_id.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
