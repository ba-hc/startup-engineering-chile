# Fintech en Chile: Ley Fintec (21.521), registro CMF y datos personales

> **Para qué sirve:** detectar en G1–G5 si el modelo de negocio activa la obligación de inscribirse en la CMF y cuánto cambia eso el plan (tiempo, capital, cumplimiento).
> **Cuándo NO usarla:** si el producto solo es software que un banco o corredora usa internamente bajo su propia licencia, si se trata de emisión de tarjetas de prepago, seguros o bancos (otros marcos, no cubiertos aquí), o para obtener una opinión legal: esto es un mapa, no un dictamen.
> **Micro-ejemplo resuelto:** una app que recomienda a personas en qué fondo invertir según su perfil es "asesoría de inversión" (art. 2 c) → para prestarla en forma profesional debe inscribirse en el Registro de Prestadores de Servicios Financieros de la CMF. Si además quiere leer cartolas bancarias con permiso del cliente, puede hacerlo como Proveedor de Servicios basados en Información dentro del Sistema de Finanzas Abiertas (registro voluntario; NCG 514). La NCG 569 postergó la vigencia del SFA a julio de 2027.

**Última verificación:** 2026-11-25. Orientación educativa, no asesoría legal. Fuentes consultadas el 2026-11-25:
- [Ley 21.521 en LeyChile](https://www.bcn.cl/leychile/navegar?idNorma=1187323)
- [Sección Ley Fintec de la CMF](https://www.cmfchile.cl/portal/principal/623/w4-propertyvalue-48738.html)
- [NCG 569](https://www.cmfchile.cl/portal/normativa/624/w4-article-111273.html)
- [Comunicado de la CMF del 01-06-2026](https://www.cmfchile.cl/portal/prensa/625/w4-article-110881.html)

## 1. La ley en una tabla
| Dato | Valor verificado |
|---|---|
| Publicación | D.O. 04-01-2023; rige desde el 03-02-2023 |
| Títulos II (servicios Fintec) y III (Finanzas Abiertas) | Rigen desde que entra en vigor la norma de la CMF respectiva |
| Registro | **Registro de Prestadores de Servicios Financieros** (RPSF) de la CMF |
| Quién se inscribe | "Sólo podrán dedicarse **en forma profesional**" a los servicios regulados quienes estén inscritos; las inscritas son personas jurídicas (art. 5) |
| Proporcionalidad | La CMF puede eximir requisitos o fijar formas de cumplimiento menos gravosas a entidades que no comprometen la fe pública según los límites de sus normas, pero **nunca la inscripción** ni las obligaciones de datos personales de la ley (art. 4) |
| Antecedentes | No se inscribe a quien, en los 10 años anteriores, fue sancionado con cancelación por infracciones graves (art. 6) |
| Lavado de activos | La ley modifica la Ley 19.913 para que las entidades inscritas reporten a la UAF (art. 36) |
| Criptoactivos | La ley los define |

## 2. ¿Qué activa la inscripción? (art. 2 y art. 5)
| Si tu startup hace… | Servicio regulado | Qué exige |
|---|---|---|
| Conecta a quienes buscan financiamiento con quienes lo aportan (préstamos, inversión en proyectos) | a) Plataforma de financiamiento colectivo | Inscripción y autorización previa de la CMF (art. 7) |
| Opera un lugar físico o virtual para cotizar o transar instrumentos sin ser bolsa | b) Sistema alternativo de transacción | Inscripción y autorización |
| Evalúa la capacidad de pago o la identidad de personas para obtener crédito, o recomienda inversiones | c) Asesoría crediticia o de inversión | Inscripción y autorización |
| Guarda instrumentos financieros de terceros | d) Custodia | Inscripción y autorización. Patrimonio mínimo: el mayor entre **5.000 UF** y 3% de los activos ponderados por riesgo, cuando la CMF lo determine por norma según el riesgo (hasta 6% si la gestión de riesgos es deficiente) |
| Recibe y enruta órdenes, o intermedia instrumentos | e) Enrutamiento de órdenes e intermediación | Igual que custodia para intermediación |
| Inicia pagos desde la cuenta del cliente con su permiso | Proveedor de Servicios de Iniciación de Pagos | Registro **propio** en la CMF (obligatorio); la CMF resuelve en 6 meses |
| Lee datos financieros del cliente con su permiso (agregador, scoring con cartolas) | Proveedor de Servicios basados en Información | Registro **voluntario** en la CMF; participa en el SFA bajo NCG 514 |

Los requisitos de garantías, gobierno corporativo y gestión de riesgos por servicio están en la **NCG 502**. Los montos exactos por servicio son **[por verificar]** en la norma vigente.

## 3. Normas de la CMF
| Norma | Qué regula | Fechas |
|---|---|---|
| **NCG 502** | Registro, autorización y obligaciones de prestadores (Título II) | Publicada 12-01-2024; vigente 03-02-2024. Quienes ya operaban debían pedir inscripción **hasta el 03-02-2025**. Pueden seguir mientras la CMF resuelve; si no la pidieron, solo pueden cerrar operaciones vigentes (art. 2° transitorio) |
| **NCG 514** | **Sistema de Finanzas Abiertas** (SFA) | Publicada 03-07-2024 |
| **NCG 569** | Modifica la NCG 514: Anexo N°3 de especificaciones técnicas, más gradualidad, "participación simplificada", piloto y **sandbox tecnológico** del SFA | Publicada 01-06-2026; **posterga la entrada en vigor del SFA a julio de 2027** |

- Cuidado: la NCG 502 **no** regula Open Finance. Para Open Finance cita la NCG 514, modificada por la NCG 569.
- Calendario por fase del SFA: **[por verificar]**. Una presentación de la CMF (agosto de 2026) muestra un hito el 03-07-2028; consulta la sección Ley Fintec antes de planificar.
- **Sandbox:** lo verificado es el *sandbox* tecnológico del SFA de la NCG 569, un ambiente de pruebas técnicas. Portal de desarrolladores: [openfinancechile.atlassian.net](https://openfinancechile.atlassian.net/wiki/spaces/OFAC/overview), consultado 2026-11-25. Un "sandbox regulatorio" que permita operar sin inscripción **no** está verificado **[por verificar]**. No lo prometas en el pitch.

## 4. Superposición con la Ley 21.719 (datos personales)
| Tema | Ley 21.521 / SFA | Ley 21.719 (vigente desde el 15-10-2027) |
|---|---|---|
| Base para tratar datos | **Consentimiento expreso** del cliente para consultas de información o iniciación de pagos; la CMF fija la forma y cómo revocarlo | Consentimiento libre, informado, específico, previo e inequívoco (art. 12) o bases del art. 13. Para datos financieros y comerciales rige la letra a), según su Título III |
| Uso limitado | Prohibido usar, guardar o acceder a datos fuera de lo autorizado, o tras la revocación o el vencimiento | Principio de finalidad; derechos de acceso, rectificación, supresión, oposición, portabilidad y bloqueo (art. 4) |
| Incidentes | Interrumpir el acceso y avisar al cliente, a la CMF y a la institución proveedora ante vulnerabilidades | Reportar a la Agencia y a los titulares si afecta datos financieros o comerciales (art. 14 sexies) |
| Decisiones automatizadas | No regulado aquí | Derecho a no ser objeto de decisiones automatizadas con efectos significativos (art. 8 bis): ojo con el scoring |
| Evaluación de impacto | No aplica | Obligatoria si hay perfiles con efectos jurídicos significativos o tratamiento masivo (art. 15 ter) |

Hoy rige la Ley 19.628. Detalle y fechas en [privacidad.md](privacidad.md).

## 5. Qué hacer ahora
1. Describe en una frase qué hace el producto con el dinero, los instrumentos o los datos del cliente. Compárala con la tabla de la sección 2.
2. Si calza con un servicio regulado, registra en la bitácora (tipo riesgo) "requiere inscripción CMF". Agrega la tarea "confirmar con abogado fintech" antes del G5.
3. Prioriza un MVP que **no** preste el servicio regulado: por ejemplo, software para una entidad ya inscrita, o una lista de espera sin ejecutar operaciones.
4. Si usas scoring o decisiones automatizadas, prepara la explicación y la intervención humana desde el diseño.
5. Más contexto de producto en [mvp_e_ia.md](mvp_e_ia.md) y [verticales_reguladas.md](verticales_reguladas.md).

## 6. Trampas típicas
- **"Somos tecnología, no servicio financiero."** La ley mira lo que haces en forma profesional, no cómo te llamas.
- **Citar la NCG 502 para Open Finance.** Es la NCG 514, modificada por la NCG 569.
- **Prometer a inversionistas un sandbox regulatorio.** No está verificado.
- **Pedir el consentimiento una vez y usar los datos para todo.** El SFA lo limita a lo autorizado.
