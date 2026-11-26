# TPL-092 — Sala de datos para due diligence (Data Room Checklist)

> **Para qué sirve:** Tener ordenado, actualizado y con acceso controlado lo que un inversionista o evaluador revisará en la due diligence, y encontrar los vacíos antes que ellos.
> **Cuándo NO usarla:** Antes de tener un interesado concreto o un term sheet en conversación (basta con mantener el expediente al día), ni para subir todo sin filtro: precios de clientes y datos personales se comparten solo cuando corresponde y con NDA (TPL-111).
> **Micro-ejemplo resuelto:** Al armar la sala, una SpA descubre que el código está en la cuenta personal de un ex socio y que 2 de sus 5 contratos con clientes no están firmados; los regulariza en 3 semanas, antes del term sheet, en vez de que aparezcan como condición de cierre.

**Gate:** G9 (antes de levantar capital) y transversal (fondos, venta de la empresa) · **Alimenta:** `evidencias.csv`, `bitacora.csv` (tipo riesgo), `decisiones.csv`

## Completar
*`scripts/dataroom.py` empaqueta el expediente y verifica que cada cifra del one-pager o del pitch cite un EV- existente. Comparte por carpeta, con permisos y registro de accesos, nunca como adjuntos por correo.*

| Carpeta | Documentos mínimos | ¿Está? | Versión / fecha | Responsable | Acceso [todos / tras term sheet / solo abogados] |
|---|---|---|---|---|---|
| 1. Societario | estatutos y modificaciones; registro de accionistas; pacto de accionistas (TPL-034); poderes; certificado de vigencia | | | | |
| 2. Capital | cap table (TPL-091); SAFE, notas y opciones (TPL-109) | | | | |
| 3. Propiedad intelectual | cesiones de socios y freelancers a la SpA; marcas en INAPI; dominios; licencias de software y datos | | | | |
| 4. Comercial | contratos y OC; cartas de intención (TPL-110); pipeline (TPL-083) | | | | |
| 5. Financiero y tributario | estados financieros; carpeta tributaria; F29 de 12 meses; flujo de caja (TPL-088); economía unitaria (TPL-087) | | | | |
| 6. Laboral | contratos de trabajo y honorarios; certificado de cotizaciones | | | | |
| 7. Producto y datos | arquitectura; checklist Ley 21.719 (TPL-097); incidentes | | | | |
| 8. Subsidios | convenios, obligaciones y rendiciones (TPL-105) | | | | |
| 9. Contingencias | juicios, reclamos, deudas, garantías | | | | |

**Vacíos encontrados:** [documento, riesgo, fecha de cierre] → `bitacora.csv` (tipo riesgo)
**Cifras del material de inversión sin EV-:** [salida de `scripts/dataroom.py`]

## Ejemplo bueno (ficticio)
CargaJusta SpA: cotizador de fletes para pymes; ronda pre-seed de $300 M en conversación con 2 ángeles.
- 41 documentos en 9 carpetas; 1–3 abiertas desde el inicio, 4–6 tras el term sheet, contratos con precios solo para los abogados del inversionista.
- `dataroom.py`: 2 cifras del pitch sin respaldo (MRR y churn), corregidas citando EV-090 y EV-091.
- Vacíos: marca sin registrar en INAPI (R-014, solicitud presentada 2027-05-02) y un freelancer sin cesión de PI (R-015, firmada 2027-05-10).
- F29 al día y certificado de cotizaciones sin deuda; un convenio de subsidio vigente con su obligación de informar cambios societarios anotada.

## Ejemplo malo y por qué falla
> Un enlace a una carpeta "Startup docs" con 300 archivos, borradores mezclados con versiones finales, la planilla con RUT y teléfonos de todos los clientes, y sin pacto de accionistas porque "está en conversación".
- Sin estructura ni versiones finales, el inversionista no sabe qué vale.
- Expone datos personales sin necesidad: problema de privacidad (TPL-097).
- Falta el pacto, que es lo primero que revisa un abogado.

## Criterio de aceptación
- Las 9 carpetas tienen estado; cada faltante tiene responsable y fecha.
- Cada cifra del material de inversión cita un EV- (`scripts/dataroom.py` sin errores).
- Niveles de acceso definidos y sin datos personales innecesarios.
- Los vacíos están en `bitacora.csv` (tipo riesgo) y se cerraron o explicaron antes del term sheet.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
