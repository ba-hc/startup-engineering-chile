# Registros reutilizables y guía de fórmulas
Los CSV de `registros/` están intencionadamente vacíos: son esquemas para registrar evidencia real. Usar UTF-8, mantener IDs estables, evitar PII innecesaria y enlazar los archivos autorizados mediante ID, no compartir datos sensibles en carpetas públicas. El XLSX complementa estos registros con un escenario hipotético editable.

| Métrica | Fórmula / definición | Advertencia |
|---|---|---|
| TAM | unidades potenciales × precio anual neto | Definir unidad y alcance, no ventas de sector |
| SAM | unidades que puedes atender × precio anual | Filtros justificados |
| SOM | mínimo de capacidad comercial, operacional y SAM × precio | Horizonte explícito |
| ARPA | ingreso recurrente mensual / clientes activos | No incluir setup |
| MRR final | MRR inicial + nuevo + expansión − contracción − churn | Misma moneda y período |
| ARR | MRR × 12 para ingresos recurrentes comparables | No equivale a ingresos realizados |
| GRR | (MRR inicial − contracción − churn) / MRR inicial | Excluye expansión |
| NRR | (MRR inicial + expansión − contracción − churn) / MRR inicial | Excluye nuevos clientes |
| Logo churn | clientes cancelados / clientes iniciales | Definir período |
| CAC | gasto comercial y marketing atribuible / nuevos clientes | Incluir trabajo fundador y cohortes |
| Contribución | ingresos netos − costos variables directos | No confundir margen bruto contable |
| Margen | contribución / ingresos netos | Cero ingresos = no interpretable |
| LTV simplificado | contribución mensual / churn mensual | Solo estable, no usar churn cero; considerar cohortes y descuento |
| CAC payback | CAC / contribución mensual | Ignora desfase si no se modela |
| Punto equilibrio | costos fijos / contribución unitaria, redondear arriba | Solo con contribución positiva y sin otros gastos |
| ROI cliente | (beneficio realizable − TCO) / TCO | No equiparar horas ahorradas a efectivo |
| VAN | − inversión inicial + suma flujos descontados | Tasa coherente con períodos y riesgos |
| TIR | tasa que hace VAN 0 | Puede no existir o haber varias; no usar sola |
| Burn neto | salidas operativas − entradas operativas | No confundir subsidio con ventas |
| Runway simple | caja / burn mensual positivo | No fiable con flujos variables; usar proyección |
| DSO | cuentas por cobrar / ventas a crédito × días | Homogeneizar período |
| Conversión | salidas de etapa / entradas de etapa | Cohorte y ventana |
| GMV | valor transacciones intermediadas | No es ingreso del marketplace |
| Take rate | ingresos atribuibles / GMV | Neto según criterio contable |
| Cost per successful task | costo total atribuible / tareas correctas | Incluye revisión, fallas e infraestructura |

Modelo de caja: facturación ≠ cobro. Separar CAPEX de OPEX, IVA, impuestos, aportes, deuda, subsidio, inversiones y capital de trabajo. Para valoración usar escenarios y supuestos explícitos. Consultar módulo 19 y fuentes FIA–Gearbox, Damodaran, Forrester, Sercotec y SaaS Capital. No es modelo contable, tributario o financiero certificado.
