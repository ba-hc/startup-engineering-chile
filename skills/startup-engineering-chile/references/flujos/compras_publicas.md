# Vender al Estado: Compra Ágil, licitaciones y GovTech

**Última verificación:** 2026-11-25. Orientación educativa, no asesoría legal. Para muchas startups B2B y GovTech, el Estado es el primer gran cliente viable.

Marco: la **Ley 21.634** (D.O. 11-12-2023) modificó la Ley 19.886 de compras públicas. Fuentes, consultadas el 2026-11-25:
- [Ley 21.634](https://www.bcn.cl/leychile/navegar?idNorma=1198903)
- [Ley 19.886 consolidada](https://www.bcn.cl/leychile/navegar?idNorma=213004)
- [ChileCompra: Compra Ágil](https://www.chilecompra.cl/ley-compra-agil/)
- [ChileCompra: compra pública de innovación](https://www.chilecompra.cl/cpi/)

## Diagnóstico rápido (3 preguntas)
1. ¿Qué organismo tiene el problema y quién lo sufre (usuario) vs. quién compra (jefatura, abastecimiento)?
2. ¿Cuánto costaría el primer contrato? Eso define la modalidad.
3. ¿Estás inscrito en Mercado Público (ChileProveedores) y tienes inicio de actividades para facturar?

## Modalidades (referencia)
| Monto del primer contrato | Modalidad típica | Notas |
|---|---|---|
| Hasta **100 UTM**: unos $7.244.000 con la UTM de noviembre de 2026 ($72.440). Convierte con `indicadores_cl.py convertir 100 UTM CLP` | **Compra Ágil** (art. 7 d) N°1, Ley 19.886) | Ver detalle en la sección siguiente. Es la vía más realista para un primer piloto pagado |
| Sobre 100 UTM | Licitación pública, convenio marco o trato directo (causales acotadas) | Bases técnicas y administrativas; garantías; plazos de meses |
| Necesidad sin solución adecuada en el mercado | **Contratos para la Innovación** o **Diálogo Competitivo de Innovación** (Ley 21.634) | Ver la sección "Compra pública de innovación". Registra el desafío en la bitácora (tipo desafio) |

**Compra Ágil en detalle:**
- Se hace "previa **solicitud** de al menos tres cotizaciones" en Mercado Público.
- Según ChileCompra, se puede contratar "aun cuando se reciba un número menor de ofertas". Basta la orden de compra aceptada, sin acto administrativo.
- **Debe realizarse con empresas de menor tamaño y proveedores locales.** Solo si ninguno de ellos cotiza, el organismo puede elegir a otro proveedor (arts. 7 d) N°1 y 56).
- Si no se elige la oferta de menor precio, hay que fundamentarlo en la orden de compra.
- El umbral subió de 30 a 100 UTM. Rige desde el **12-12-2024**, un año después de la publicación (art. 1° transitorio de la Ley 21.634).
- El reglamento es el Decreto 661 de 2024 de Hacienda; su fecha de publicación está **[por verificar]**.

## Cómo preparar una Compra Ágil
- **Ficha y cotización:** describe el resultado (no la tecnología), plazo, entregables, precio con IVA explícito, condiciones de pago y soporte. Propón un piloto acotado (1 servicio, 1–3 meses) con métrica de éxito.
- **Habilidad:** inscripción vigente en el Registro de Proveedores, sin deudas laborales ni previsionales y con documentos tributarios al día. Los requisitos exactos de habilidad están **[por verificar]** en el Registro.
- **Datos:** si tratas datos de personas o de salud, explica seguridad y confidencialidad desde la cotización (ver [privacidad.md](privacidad.md)).
- **Después:** el piloto pagado es evidencia de nivel 4 (`add pilotos`, `add evidencias`) y sirve de referencia para licitaciones.

## Compra pública de innovación (Ley 21.634)
| Procedimiento | Qué es | Lo que importa a una startup |
|---|---|---|
| **Contratos para la Innovación** (art. 7 d) N°4) | Procedimiento competitivo para necesidades sin productos o servicios adecuados en el mercado. Puede incluir I+D y terminar en adjudicación, en una nueva licitación o sin adjudicación | Por regla general, el organismo **paga los prototipos y la I+D aunque el proveedor no resulte adjudicado** (salvo excepción fundada) |
| **Diálogo Competitivo de Innovación** (N°5) | Fases sucesivas con diálogo estructurado entre organismo y proveedores | Permite ajustar la solución con el comprador antes de ofertar |
| **Uniones Temporales de Proveedores** (art. 55) | Alianza temporal para ofertar | En estos dos procedimientos se pueden formar **sin límite por tamaño de empresa** |

- **Vigencia:** ambos procedimientos rigen 18 meses después de la publicación de la ley, es decir, aproximadamente desde junio de 2025.
- **Apoyo de ChileCompra:** política de compra pública de innovación (DS 53 de Hacienda, 2024), manual "Contratos para la innovación" y curso gratuito. Contacto: cpi@chilecompra.cl.
- **Trampa típica:** confundir estos procedimientos con un subsidio. Es una compra; se gana compitiendo.

## Investigar demanda con datos públicos
- **Buscador de Mercado Público:** licitaciones y órdenes de compra históricas por rubro y organismo, con precios de referencia reales.
- **API de Mercado Público:** requiere un *ticket* personal, que se obtiene con ClaveÚnica (10.000 consultas diarias). Si el fundador lo tiene, úsalo con su permiso; si no, usa el buscador web o Firecrawl sobre páginas públicas. Detalle de parámetros en [conectores_y_apis.md](../conectores_y_apis.md).
- Registra los hallazgos en `competencia.csv` (quién vende hoy y a qué precio) y en `cuentas_y_pipeline.csv` (organismos objetivo).

## Trabas frecuentes
- **Plazos de pago:** pueden demorar más de lo pactado; modela la caja. El plazo legal de pago a proveedores está **[por verificar]** en la Ley 19.886 vigente.
- **Cotizar sin entender las bases:** multas y garantías.
- **Presentarse como "plataforma"** cuando el organismo compra un servicio con resultado.
