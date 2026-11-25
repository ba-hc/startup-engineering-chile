# Vender al Estado: Compra Ágil, licitaciones y GovTech

**Última verificación:** 2026-11-25 (fuente: chilecompra.cl). Para muchas startups B2B y GovTech el Estado es el primer gran cliente viable.

## Diagnóstico rápido (3 preguntas)
1. ¿Qué organismo tiene el problema y quién lo sufre (usuario) vs. quién compra (jefatura, abastecimiento)?
2. ¿Cuánto costaría el primer contrato? Eso define la modalidad.
3. ¿Estás inscrito en Mercado Público (ChileProveedores) y tienes inicio de actividades para facturar?

## Modalidades (referencia)
| Monto del primer contrato | Modalidad típica | Notas |
|---|---|---|
| Hasta **100 UTM** (convierte con `indicadores_cl.py convertir 100 UTM CLP`) | **Compra Ágil** | Mínimo 3 cotizaciones; por regla general dirigida a empresas de menor tamaño y proveedores locales; plazos cortos. La vía más realista para un primer piloto pagado |
| Sobre 100 UTM | Licitación pública, convenio marco o trato directo (causales acotadas) | Bases técnicas y administrativas; garantías; plazos de meses |
| Innovación sin solución en el mercado | Compra pública de innovación / desafíos (ver `desafios_corporativos.csv`) | Revisa programas vigentes de ChileCompra, gobiernos regionales y Laboratorio de Gobierno |

## Cómo preparar una Compra Ágil
- **Ficha y cotización**: describe el resultado (no la tecnología), plazo, entregables, precio con IVA explícito, condiciones de pago y soporte. Un piloto acotado (1 servicio, 1–3 meses) con métrica de éxito.
- **Habilidad**: inscripción vigente, sin deudas laborales ni previsionales, documentos tributarios al día.
- **Datos**: si tratas datos de personas o de salud, explica seguridad y confidencialidad desde la cotización.
- **Después**: el piloto pagado es evidencia de nivel 4 (`add pilotos`, `add evidencias`) y referencia para licitaciones.

## Investigar demanda con datos públicos
- Buscador de Mercado Público: licitaciones y órdenes de compra históricas por rubro y organismo (precios de referencia reales).
- API de Mercado Público: requiere un *ticket* personal (se obtiene con ClaveÚnica; 10.000 consultas diarias). Si el fundador lo tiene, úsalo con su permiso; si no, usa el buscador web o Firecrawl sobre páginas públicas.
- Registra hallazgos en `competencia.csv` (quién vende hoy y a qué precio) y `cuentas_y_pipeline.csv` (organismos objetivo).

## Trabas frecuentes
Pagos a 30 días por ley, pero en la práctica pueden demorar: modela la caja. Cotizar sin entender las bases (multas, garantías). Presentarse como "plataforma" cuando el organismo compra un servicio con resultado.
