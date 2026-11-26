# TPL-097 — Checklist de protección de datos Ley 21.719 y seguridad (Security & Privacy)

> **Para qué sirve:** Revisar, dato por dato, si el producto trata datos personales con base de licitud, información, seguridad y contratos coherentes con la Ley 21.719, y dejar listo el paquete que piden los compradores corporativos.
> **Cuándo NO usarla:** Si el producto no trata datos de personas identificables (p. ej. solo telemetría de máquinas), y nunca como dictamen legal; vigencia, plazos y sanciones están en `references/flujos/privacidad.md` y la conclusión la valida un abogado.
> **Micro-ejemplo resuelto:** Una agenda para centros de kinesiología que pedía "diagnóstico" al reservar descubre que trata datos de salud (sensibles) sin necesitarlos para agendar: elimina el campo, y para las notas clínicas que sí necesita exige base específica, cifrado y acceso solo del profesional tratante.

**Gate:** transversal (G5 al diseñar; G7 antes de vender a empresas o tratar datos de terceros) · **Alimenta:** `bitacora.csv` (tipo riesgo y requisito), `decisiones.csv`

## Completar
*Orientación educativa. La Ley 21.719 modifica a fondo la Ley 19.628 y crea una agencia fiscalizadora; fechas de vigencia, plazos de adecuación y sanciones: `references/flujos/privacidad.md` (no los copies aquí). Valida con abogado.*

### 1. Inventario de datos
| Dato o grupo | Titular | ¿Sensible? | Finalidad | Base de licitud [consentimiento / contrato / obligación legal / interés legítimo / otra] | Dónde se guarda (país, proveedor) | Quién accede | Plazo de conservación | ¿Es necesario? |
|---|---|---|---|---|---|---|---|---|

### 2. Checklist
| # | Tema | Control | Estado [OK / FALTA / N/A] | Evidencia o acción · responsable · fecha |
|---|---|---|---|---|
| 1 | Inventario | ¿Completo y actualizado? | | |
| 2 | Base de licitud | ¿Cada finalidad tiene base? Si es consentimiento, ¿se puede acreditar? | | |
| 3 | Datos sensibles (salud, biométricos…) | ¿Solo si son necesarios, con base específica y más seguridad? | | |
| 4 | Derechos de los titulares | ¿Canal y plazo interno para acceso, rectificación, supresión, oposición, portabilidad y bloqueo? | | |
| 5 | Deber de información | ¿La política dice quién trata, para qué, con qué base, a quién comunica, cuánto guarda y cómo ejercer derechos? | | |
| 6 | Seguridad | ¿Cifrado, control de accesos, respaldos y registro de accesos proporcionales al riesgo? | | |
| 7 | Brechas | ¿Procedimiento escrito para detectar, contener, registrar y notificar a la autoridad y a los titulares cuando corresponda? | | |
| 8 | Encargados y terceros | ¿Contrato de encargo con cada proveedor que trata datos (nube, CRM, IA)? Si eres encargado de tu cliente, ¿lo firmaste? | | |
| 9 | Transferencias internacionales | ¿En qué país está cada dato y con qué garantía se transfiere? | | |
| 10 | Evaluación de impacto | ¿Corresponde (alto riesgo, sensibles a gran escala, perfilamiento, decisiones automatizadas)? ¿Hecha antes de lanzar? | | |
| 11 | Datos para entrenar IA | ¿El entrenamiento es una finalidad informada y con base propia? ¿Lo permite el contrato con el cliente? ¿El proveedor de IA entrena con tus datos? | | |
| 12 | Anonimización vs. seudonimización | ¿Lo "anónimo" es irreversible? Si se puede reidentificar (ID interno, hash de RUT), está seudonimizado y sigue siendo dato personal. | | |
| 13 | Minimización y conservación | ¿Se borra lo que ya no se necesita, en el plazo definido? | | |

**Paquete para comprador corporativo:** [ ] política de privacidad · [ ] contrato de encargo modelo · [ ] respuestas de seguridad (ubicación de datos, cifrado, accesos, respaldos, incidentes) · [ ] lista de subencargados

## Ejemplo bueno (ficticio)
AgendaKine SpA: agenda y fichas para centros de kinesiología; ~12.000 pacientes; AgendaKine actúa como encargada de cada centro.
- Inventario de 7 grupos; "diagnóstico al reservar" eliminado por innecesario; notas clínicas: sensibles, base verificada con abogado (REQ-012).
- Nube en otro país: transferencia con cláusulas contractuales del proveedor (REQ-013). Contrato de encargo firmado con los 18 centros.
- IA: proveedor de transcripción con contrato que prohíbe entrenar con los datos; AgendaKine no entrena modelos con fichas.
- Paneles internos con ID de paciente: seudonimizados, tratados como dato personal.
- Evaluación de impacto hecha por tratar datos de salud a escala; simulacro de brecha 2027-05 (R-021 cerrado).

## Ejemplo malo y por qué falla
> Los datos están anonimizados porque reemplazamos el nombre por el RUT con hash. Usamos las fichas para entrenar nuestro modelo, como dicen los términos (casilla premarcada). La seguridad la ve la nube.
- Un hash de RUT se revierte probando RUT posibles: es seudonimización, no anonimización.
- Una casilla premarcada no es consentimiento válido para datos de salud, y entrenar IA es otra finalidad.
- El proveedor de nube protege su infraestructura, no tus accesos ni tu configuración.

## Criterio de aceptación
- Inventario con finalidad, base y plazo para cada dato.
- Ningún FALTA sin responsable y fecha; ningún N/A sin justificar.
- Datos sensibles minimizados; el uso para IA está informado y permitido por contrato.
- Contratos de encargo firmados con proveedores y clientes que corresponda.
- Vigencia y plazos consultados en `references/flujos/privacidad.md`; revisión de abogado registrada en `decisiones.csv`.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
