# Flip societario (Delaware, Caimán): cuándo sí, cuándo es prematuro

> **Para qué sirve:** frenar un flip hecho por moda y, cuando un inversionista líder lo exige, llegar al abogado con las preguntas correctas y sabiendo qué fondos chilenos se ponen en riesgo.
> **Cuándo NO usarla:** para decidir la estructura final o el costo tributario de un caso concreto; eso lo hace un abogado y un contador con el term sheet en la mano.
> **Micro-ejemplo resuelto:** SpA chilena sin term sheet, postulando a ANID Startup CTCI y con una aceleradora que "recomienda Delaware" → no hay flip. ANID exige una beneficiaria constituida en Chile. Se revisa de nuevo cuando un inversionista líder ponga el flip como condición por escrito.

**Última verificación:** 2026-11-25. Orientación educativa, no asesoría legal ni tributaria.

**Regla por defecto de la skill: no hay flip hasta que un inversionista líder lo exija por escrito** (term sheet o carta firmada). Antes de eso, la SpA chilena basta para vender, levantar SAFE locales y postular a fondos públicos (ver [socios_equity.md](socios_equity.md)).

## 1. Qué es
El flip crea una sociedad holding en el extranjero (típicamente Delaware, EE.UU., o Islas Caimán). Los fundadores cambian sus acciones de la SpA chilena por acciones de la holding, y la SpA queda como filial. La forma exacta (canje, aporte o compraventa) la define el abogado.

## 2. Señales de que es prematuro
| Señal | Por qué importa |
|---|---|
| No hay inversionista líder que lo exija por escrito | Pagas costos y complejidad por una ronda que no existe |
| Dependes de fondos públicos chilenos en los próximos 12–18 meses | Varios exigen beneficiaria chilena (ver sección 3) |
| No tienes clientes ni operación fuera de Chile | La holding no agrega ventas |
| El equipo no tiene contador ni abogado con experiencia transfronteriza | Errores en el canje de acciones son caros de corregir |
| La caja cubre menos de 6 meses (ver [caja_y_cobro.md](caja_y_cobro.md)) | El flip consume tiempo de fundadores y caja |

## 3. Lo verificado que el flip puede afectar (consultado 2026-11-25)
| Instrumento | Requisito verificado | Fuente |
|---|---|---|
| ANID Startup CTCI 2027 | Beneficiaria: **persona jurídica constituida en Chile**, menos de 10 años, con I+D en su objeto social y desarrolladas "en territorio nacional". Gastos de I+D fuera de Chile requieren solicitud de pertinencia 30 días antes. El director debe tener residencia y ejercer desde Chile. Las asociadas sí pueden ser extranjeras | [Bases Startup CTCI 2027](https://s3.us-east-1.amazonaws.com/documentos.anid.cl/investigacion-aplicada/2027/StartupCTCI/Rex_9568_2026_Startup_CTCI_2027_a5c2b3d9f1e6a4c8b0d7f2e1a9c3d6.pdf) |
| ProChile GoGlobal 2026 | Persona jurídica **chilena** de primera categoría con facturación en Chile en los últimos 12 meses | [GoGlobal 2026](https://www.prochile.gob.cl/convocatorias/detalle/goglobal-2026) |
| CORFO Semilla Inicia | Postula una persona natural residente o una "persona jurídica constituida en Chile" con inicio de actividades no anterior a 18 meses y sin ventas. Si gana una persona natural, debe "constituir en Chile una persona jurídica" en el plazo que fije CORFO | [Bases Técnicas Res. 1498](https://saowcsblobassets.blob.core.windows.net/assets/CONV/26INI-BB1/2%29%20Bases%20Tecnicas%20Semilla%20Inicia%202025%20Res%201498.pdf) |
| Ley I+D (Ley 20.241) | El crédito es contra el impuesto de primera categoría chileno, con contabilidad completa | [Ley 20.241](https://www.bcn.cl/leychile/navegar?idNorma=268637); ver [ley_id.md](ley_id.md) |

Si la SpA sigue existiendo como filial, ¿sigue siendo elegible cuando su dueña es una sociedad extranjera? **[por verificar]** en las bases de cada llamado. Pregúntalo por escrito a CORFO o ANID antes del flip.

## 4. Lo verificado sobre impuestos en Chile
**Venta indirecta (Ley sobre Impuesto a la Renta, art. 10).** Cuando un no residente vende acciones de una sociedad extranjera, la renta puede quedar afecta a impuesto en Chile si se cumple alguno de estos casos:
- (a) al menos **20%** del valor de mercado viene de activos subyacentes chilenos (por ejemplo, acciones de la SpA), y se enajena al menos **10%** en 12 meses;
- (b) los activos subyacentes chilenos valen **210.000 UTA** o más, y se enajena al menos 10%;
- (c) la sociedad está en un territorio considerado **régimen fiscal preferencial** (art. 41 H), en cuyo caso basta cualquier porcentaje, salvo prueba en contrario ante el SII.

Fuente: [DL 824, Ley sobre Impuesto a la Renta, en LeyChile](https://www.bcn.cl/leychile/navegar?idNorma=6368), consultado 2026-11-25.

**[por verificar]** con un asesor:
- El tratamiento tributario en Chile del canje o aporte de acciones de la SpA a la holding por fundadores residentes en Chile (mayor valor).
- Si Caimán o Delaware figuran en la lista de regímenes fiscales preferenciales del SII (art. 41 H).
- Los impuestos en EE.UU. o Caimán, los precios de transferencia entre holding y filial, y la retención sobre pagos al exterior.
- El costo de constitución y mantención anual (agente registrado, impuestos estatales, contabilidad en dos países). No hay cifras verificadas aquí: pide cotizaciones escritas.

## 5. Checklist de preguntas para el abogado
- [ ] ¿Qué exige exactamente el term sheet? ¿Delaware C-Corp, Caimán u otra? ¿Es condición de cierre o "deseable"?
- [ ] ¿Qué mecanismo propones (canje, aporte, compraventa)? ¿Qué impuesto genera en Chile para cada fundador y cuándo se paga?
- [ ] ¿Cómo se trasladan las opciones o el vesting de la SpA (ver [socios_equity.md](socios_equity.md)) y los SAFE o notas ya firmados?
- [ ] ¿La SpA conserva su elegibilidad en CORFO, ANID y ProChile? ¿Qué pasa con proyectos en ejecución y sus convenios?
- [ ] ¿Quién es dueño de la propiedad intelectual: la holding o la SpA? ¿Hay que cederla? ¿Qué impuesto genera?
- [ ] ¿Qué obligaciones de reporte nacen en Chile y en el extranjero (SII, Banco Central, estado de constitución)?
- [ ] ¿Cuánto cuesta el flip y la mantención anual en los dos países? Pide un presupuesto escrito con hitos.
- [ ] ¿Quién paga los costos: la ronda, la empresa o los fundadores?
- [ ] ¿Cómo afecta una futura venta de la holding (art. 10 LIR)?
- [ ] ¿Qué pasa con contratos de clientes chilenos, cuentas bancarias y trabajadores?

## 6. Trampas típicas
- **Hacer el flip "porque así lo hacen en Silicon Valley".** Sin un inversionista que lo exija, solo suma costos.
- **Firmar el flip con un proyecto ANID o CORFO en ejecución sin preguntar.** Puedes incumplir el convenio.
- **Olvidar el art. 10 LIR.** La venta de la holding puede tributar en Chile.
- **Ceder la propiedad intelectual sin valorizarla.** Genera riesgo tributario y conflictos con convenios de fondos.

Ver también [internacionalizacion.md](internacionalizacion.md) y [capital_privado.md](capital_privado.md).
