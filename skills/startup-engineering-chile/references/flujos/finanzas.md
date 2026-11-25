# Finanzas: unit economics, caja, modelo, contratar y dilución

Regla: **ningún número financiero sale "a ojo"**. Corre el script, muestra la tabla corta en el chat y guarda el detalle en el expediente (TPL-087/088, `indicadores.csv`).

## Errores que debes detectar (y cómo)
| Error | Señal | Qué hacer |
|---|---|---|
| LTV sobre ingreso en vez de contribución | "LTV = precio × vida" | `finanzas.py unit` muestra ambos y cuánto infla |
| Churn inventado o casi cero | churn < 1% mensual sin cohortes | pide `cohortes.csv` o usa un rango; tope de vida 60 meses |
| Confundir margen bruto con ingreso | "facturamos 10M, ganamos 10M" | contribución = precio − costos variables directos |
| TAM top-down sin sustento | "el 1% de un mercado de US$5.000M" | TAM/SAM/SOM bottom-up (TPL-030): unidades × precio, filtros justificados, SOM limitado por capacidad comercial |
| Subsidio contado como venta | caja con fondo CORFO como ingreso | `escenarios` lo separa; en el pitch, subsidio ≠ tracción |
| Facturar = cobrar | caja sin cobro diferido | supuesto "Cobro diferido" del modelo |
| Costo de un empleado = sueldo líquido | "contrato a alguien con $1M" | `costo-empleado --liquido 1000000`: el costo empresa suele ser 30–45% más que el líquido |
| CAC sin el tiempo del fundador | CAC = solo publicidad | incluir horas comerciales valorizadas |

## Comandos
- `finanzas.py unit --precio P --costo-variable CV --cac CAC --churn 0.03` → contribución, margen, payback, LTV, LTV/CAC y alertas.
- `finanzas.py equilibrio --costos-fijos CF --precio P --costo-variable CV` → clientes para cubrir fijos.
- `finanzas.py runway --caja C --gasto G --ingreso I [--crecimiento-ingreso 0.05]`.
- `finanzas.py escenarios --modelo expediente/entregables/modelo_financiero.xlsx` → pesimista/base/optimista a 24 meses (simulación independiente de la planilla; factores explícitos, no probabilidades).
- `modelo_xlsx.py leer|set|verificar` para actualizar los supuestos del Excel sin romper fórmulas (ver `references/herramientas.md`).
- `finanzas.py costo-empleado (--bruto B | --liquido L) [--contrato plazo-fijo] [--gratificacion] [--provision-indemnizacion] [--mutual-adicional 0.0095]` → líquido, cotizaciones, aporte del empleador (reforma de pensiones, que desde ago-2026 incluye el SIS), AFC, mutual y costo empresa. Usa UF/UTM de `indicadores_cl.py` o del respaldo con fecha.
- `finanzas.py honorarios (--bruto | --liquido)` → retención 2026 (15,25%; 16% en 2027).
- `finanzas.py dilucion --fundadores "Ana:60,Beto:40" [--pool 10] [--safe 50000000:1000000000] --pre 2000000000 --inversion 500000000 --pool-post 10` → cap table antes y después; supuestos impresos (SAFE post-money solo con cap; pool pre-money).

## Monedas: CLP, UF y USD
Un modelo que mezcla SaaS en UF, servidores en USD y subsidio en CLP necesita una **fecha de corte**: anota en `00_estado.md` (o en la hoja Supuestos) "UF = $X y USD = $Y al AAAA-MM-DD" con `indicadores_cl.py obtener uf dolar`. Convierte con `indicadores_cl.py convertir`. En proyecciones largas, explicita si los precios en UF se reajustan y si los costos en USD tienen riesgo cambiario.

## Cuándo pedir un profesional
Estructura tributaria, contratos laborales, valorización para una ronda y cap tables con instrumentos complejos (descuentos, MFN, pro-rata, preferentes): el script da órdenes de magnitud para conversar, no la cifra final.
