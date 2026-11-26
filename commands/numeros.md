---
description: Tus números con script - unit economics, runway, punto de equilibrio, escenarios y modelo Excel (CLP, UF o USD)
argument-hint: "[pregunta: '¿cuánto cobro?', 'runway', 'contratar a alguien con $1,2M líquido']"
---

Usa la skill **startup-engineering-chile** y lee `skills/startup-engineering-chile/references/flujos/finanzas.md`.

Pregunta: $ARGUMENTS

1. Toma los supuestos de "Números clave" en `00_estado.md` o del modelo (`python <skill>/scripts/modelo_xlsx.py leer <expediente>/entregables/modelo_financiero.xlsx`). Si falta uno que decide, pregúntalo; no lo inventes.
2. Calcula **siempre con script**, nunca a ojo: `finanzas.py unit|equilibrio|runway|escenarios --modelo …|costo-empleado|honorarios|dilucion|ley-id`. Conversiones con `indicadores_cl.py convertir 120 UF CLP` (cita valor y fecha).
3. Si hay expediente y no tiene modelo, ofrece `expediente.py modelo --dir <carpeta>`; la hoja `Fondos_y_moneda` muestra montos en CLP/UF/USD, equilibrio por escenario y meses de caja.
4. Responde en formato 1-3-1: **1** la cifra que decide (runway, clientes de equilibrio, margen), **3** supuestos que más la mueven y si son dato o hipótesis, **1** próximo paso para validar el supuesto más débil.

Marca cada supuesto como dato, estimación o meta. Un LTV/CAC sin historial de retención es una hipótesis.
