# TPL-110 — Carta de intención B2B (Letter of Intent, LOI)

> **Para qué sirve:** Convertir el interés de una empresa compradora en un compromiso escrito con condición, monto, plazo y firmante con atribución, para avanzar a piloto o contrato y usarlo como evidencia ante fondos o inversionistas.
> **Cuándo NO usarla:** Si el cliente ya está dispuesto a pagar un piloto o emitir una OC (pide eso, que vale más), o si quien firma no tiene atribución de compra: una carta firmada por un usuario entusiasta no prueba nada.
> **Micro-ejemplo resuelto:** "Si el piloto de 6 semanas en la obra de Quilicura baja las horas de cuadrilla detenida de 40 a ≤ 25 al mes, emitiremos OC por 12 meses a 18 UF/mes por obra para 4 obras (864 UF + IVA)" es evidencia; "nos interesa conocer más su solución", no.

**Gate:** G6–G7 (también como evidencia en fondos) · **Alimenta:** `cuentas_y_pipeline.csv`, `evidencias.csv`, `pilotos.csv`

## Completar
*Orientación educativa: una LOI suele ser no vinculante, salvo las cláusulas que se declaren vinculantes (confidencialidad, exclusividad, vigencia). Si se redacta como obligación de comprar puede ser una promesa o un contrato según el Código Civil: revísala con abogado. Una carta de intención no es una venta facturada; revisa su efecto en la elegibilidad de fondos (TPL-103).*

| Campo | Contenido |
|---|---|
| Partes | [razón social y RUT del comprador · SpA proveedora] |
| Firmante y atribución | [cargo; aprueba compras hasta [ ] UF; respaldo: poder o política de compras] |
| Problema y alcance | [proceso, sitio, volumen] |
| Condición de compra | [si KPI ≥ meta en el piloto (TPL-067) o si ocurre [ ] → compra] |
| Precio y cantidad | [precio neto + IVA, unidades, duración del contrato] |
| Plazos | [inicio del piloto, fecha de decisión, vigencia de la carta] |
| Qué aporta cada parte | [datos, acceso al sitio, contraparte técnica] |
| Cláusulas vinculantes | [confidencialidad (TPL-111), exclusividad si existe, ley aplicable] |
| Cláusulas no vinculantes | [intención de compra] |
| Próximo paso | [acción, responsable, fecha] |

*Una LOI sin condición medible, sin precio o sin fecha de decisión es una carta de apoyo: regístrala como tal.*

## Ejemplo bueno (ficticio)
PlanoClaro SpA: control de avance de obra con fotos georreferenciadas. Cuenta: constructora mediana de la RM (CTA-011).
- Firmante: gerente de operaciones, aprueba compras hasta 1.000 UF (política de compras, EV-081).
- Condición: si en el piloto pagado de 8 semanas (PIL-004, 60 UF + IVA) el informe semanal de avance baja de 6 h a ≤ 2 h por obra, la constructora emite OC por 12 meses para 5 obras a 15 UF/mes por obra (900 UF + IVA).
- Plazos: piloto desde 2027-04-01; decisión dentro de 20 días hábiles tras el informe; carta vigente hasta 2027-07-31.
- Vinculantes: confidencialidad y ley chilena. No vinculante: la compra.
- Registrada como EV-082 con etiqueta "LOI condicionada", no como venta; la cuenta pasa a etapa "piloto acordado".

## Ejemplo malo y por qué falla
> "La empresa X manifiesta su interés en la innovadora solución de PlanoClaro y en explorar oportunidades de colaboración." Firma: ingeniero de proyectos. Presentada al fondo como "cliente asegurado".
- Sin condición, monto ni plazo: no compromete nada.
- Quien firma no compra ni tiene presupuesto.
- Presentarla como venta resta credibilidad ante un evaluador y puede afectar la elegibilidad si se confunde con ventas.

## Criterio de aceptación
- Firma quien tiene atribución de compra y esa atribución tiene respaldo.
- Hay condición medible, precio, cantidad y fecha de decisión.
- Las cláusulas vinculantes y no vinculantes están separadas; un abogado la revisó si obliga a algo.
- Está en `evidencias.csv` como intención (no venta) y la cuenta avanzó en `cuentas_y_pipeline.csv`.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
