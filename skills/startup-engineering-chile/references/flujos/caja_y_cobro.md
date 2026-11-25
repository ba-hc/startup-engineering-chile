# Caja, facturación y cobro en Chile

**Última verificación:** 2026-11-25. Orientación educativa: el régimen tributario y los PPM se definen con un contador. Complementa `trampas_chile.md` y TPL-088.

## 1. Documentos
- **Factura afecta:** IVA de 19% (DL 825, art. 14). El IVA se devenga al **emitir** la factura, no al cobrarla (art. 9 a).
- **Factura exenta** (código 34): solo para operaciones que la ley declara exentas. No la uses por conveniencia.
- **Exportación de servicios:**
  - Exenta de IVA si el Servicio Nacional de Aduanas califica el servicio como exportación (Res. Ex. 2.511/2007 y modificaciones; DL 825 art. 12 E N°16).
  - Si el servicio no está en el listado, se presenta una solicitud fundada que se resuelve en 35 días hábiles. La calificación no tiene costo y no vence.
  - La factura de exportación es electrónica. Permite recuperar el IVA de las compras (art. 36).
- **Boleta:** solo electrónica desde 2021.

## 2. El IVA y la caja: el costo oculto de cobrar a 60 días
- El F29 se paga hasta el **día 20** del mes siguiente si facturas electrónicamente y declaras en línea (día 12 en general). Si se emitió la factura, el IVA se paga aunque el cliente no haya pagado.
- *Ejemplo:* facturas $10.000.000 + IVA el 5 de marzo con pago a 60 días. Pagas $1.900.000 de IVA el 20 de abril y cobras el 4 de mayo. Financias el IVA unas 2 semanas, y el neto completo 60 días.
- **Modélalo:** usa `finanzas.py escenarios` con el parámetro `diferido` (cobro diferido) y revisa el mes de caja mínima. En TPL-088 agrega una línea de IVA neto a pagar.
- Si el cliente es una gran empresa, revisa la Ley de pago a 30 días (`venta_corporativa.md`) y el factoring.

## 3. Medios de pago y cobro recurrente (al 2026-11-25)
| Proveedor | Qué cubre | Comisión publicada |
|---|---|---|
| **Transbank** | Webpay Plus (crédito y débito); **Patpass** para cargos recurrentes en tarjeta de crédito | Sin tabla pública verificada; tarifas en proceso de desregulación (FNE, 2026) |
| **Flow** | Tarjetas, transferencias, billeteras | 2,89% + IVA (abono al 3er día hábil) o 3,19% + IVA (al día siguiente) |
| **Khipu** | Transferencias; "Pagos Automáticos" con mandato | 0,69% + IVA + UF 0,0105 + IVA por transacción |
| **Fintoc** | Transferencias, tarjetas (desde 2026), pagos recurrentes y débito directo | Sin página pública de precios |
| **Mercado Pago** | Link de pago, suscripciones | No verificada |
| **Getnet** (Santander) | Link de pago, web checkout | Solo simulador |
| **Stripe** | — | **No opera para empresas chilenas** (en LatAm solo Brasil y México) |

Cómo elegir:
- **B2C con suscripción:** tarjeta con cargo recurrente (Patpass, Mercado Pago) o débito o mandato de cuenta (Khipu, Fintoc). Las transferencias son más baratas, pero tienen más fricción al primer pago.
- **B2B:** factura y transferencia. El costo real es el plazo de pago, no la comisión.
- Pon la comisión en el costo variable de `finanzas.py unit`. A precios bajos, un 3% más IVA se nota en el margen.

## 4. Régimen y obligaciones (con contador)
- **Pro Pyme General (14 D N°3)** vs. **Transparente (14 D N°8)** vs. régimen general: la tasa de primera categoría y los PPM dependen del régimen. Ver tasas en `trampas_chile.md`. La skill no simula regímenes tributarios: esa elección es de un contador.
- Antes de emitir la primera factura, inicio de actividades con el giro correcto. Revisa si cambia la elegibilidad a fondos (`trampas_chile.md`).

Cierra con: medio de cobro elegido y su costo en `finanzas.py unit`, plazo de pago promedio de los clientes en el modelo y la acción "revisar régimen con contador" con fecha.
