# Vender a grandes empresas e innovación abierta

**Última verificación:** 2026-11-25. Complementa el módulo 16 (go-to-market), TPL-067 (piloto) y `compras_publicas.md` (Estado).

## 1. Antes de la primera reunión
- **Mapa de decisión:** identifica en la cuenta (TPL-020) a cuatro personas:
  - el usuario;
  - el dueño del presupuesto;
  - quien aprueba técnicamente (TI, ciberseguridad, prevención de riesgos);
  - quien compra (abastecimiento).
  
  Cada una tiene una objeción distinta. Regístralas en `cuentas_y_pipeline.csv`.
- **Canal de entrada:** programas de innovación abierta y desafíos corporativos (`desafios_corporativos.csv`), presentaciones de inversionistas o clientes actuales. La puerta fría a abastecimiento rara vez funciona en una startup.

## 2. Registros de proveedores (requisito habitual para facturar)
| Registro | Quién lo usa (al 2026-11-25) |
|---|---|
| **SICEP** | Asociación de Industriales de Antofagasta; minería, energía e industria. Más de 3.800 proveedores; actualización anual. |
| **REGIC** | Registro para mandantes mineros, operado por Achilles. Codelco invita primero desde REGIC en compras sobre USD 300 mil y servicios sobre USD 100 mil. |
| **SAP Ariba / SAP Business Network** | Grandes empresas e instituciones, por ejemplo Codelco y el Banco Central. |
| **Registro de Proveedores del Estado** (ChileCompra) | Para vender al Estado (`compras_publicas.md`). |

La inscripción pide antecedentes legales, tributarios, laborales y financieros, y a veces tiene costo. Inicia el trámite cuando haya una oportunidad concreta, no antes.

## 3. Requisitos que frenan pilotos
Prepara un paquete corto antes de que lo pidan:
- **Seguridad de la información:** dónde están los datos, cifrado, accesos, respaldo, proveedor de nube, gestión de incidentes. Usa TPL-097.
- **Datos personales:** rol de encargado del tratamiento y contrato. Ver `privacidad.md`.
- **Seguros y cumplimiento:** prevención de riesgos si hay trabajo en faena, y cumplimiento laboral de subcontratistas.

## 4. Piloto pagado que se convierte en contrato
Usa TPL-067 completo. Lo que más evita el *pilot purgatory* es:
- **Piloto pagado**, aunque sea a precio reducido: separa el interés real de la curiosidad.
- **KPI y baseline** firmados por el sponsor antes de partir.
- **Precio posterior y condición de conversión** escritos: "si el KPI mejora ≥X%, se emite una OC por 12 meses a $Y".
- **Duración fija**, con una sola extensión posible.
- **Quien firma la OC** sabe del piloto desde el día 1.

## 5. Cobrar: plazos y caja
- **Ley de pago a 30 días (Ley 19.983, modificada por la Ley 21.131):**
  - El plazo máximo es de **30 días corridos** desde la recepción de la factura.
  - Se puede pactar un plazo mayor por escrito, sin abuso, inscribiéndolo en el registro del Ministerio de Economía dentro de 5 días hábiles. Ese pacto excepcional **no cabe** entre una empresa de menor tamaño vendedora y una gran empresa compradora, salvo excepciones (pagos anticipados o por avance).
  - Si pagan tarde, se devenga interés por mora más una comisión de 1% del saldo.
  - El Estado paga en 30 días, o hasta 60 si las bases lo fundan.
- **Factoring:**
  - La factura electrónica es cedible si el cliente no la reclama dentro de 8 días.
  - La cesión se hace electrónicamente y se anota en el registro del SII.
  - Compara el costo del factoring con el de financiar el IVA y la caja (`caja_y_cobro.md`).
- En el modelo, usa el plazo **real** de pago, no el legal: muchos clientes tienen ciclos de recepción conforme que retrasan la factura.

## 6. Ciclo de venta y pronóstico
- Los ciclos de 3–9 meses son normales en minería, energía y retail grande. Pon esa duración en el runway (`finanzas.py runway`) antes de contratar.
- Pronóstico = Σ valor × probabilidad, solo para etapas con criterio de salida cumplido (TPL-083).

Cierra con: cuenta, mapa de decisión, siguiente paso con fecha, registro requerido y condición de conversión del piloto.
