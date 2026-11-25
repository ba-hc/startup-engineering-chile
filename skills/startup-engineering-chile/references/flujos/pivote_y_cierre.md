# Pivotar o cerrar con orden

**Última verificación:** 2026-11-25. Orientación educativa: un cierre con deudas, trabajadores o subsidio vigente requiere abogado y contador.

Un Kill con evidencia es un buen resultado. Este flujo cuida tres cosas:
- que la decisión sea honesta;
- que el aprendizaje no se pierda;
- que el cierre no deje deudas con el SII, CORFO o los trabajadores.

## 1. Decidir: pivote, pausa o cierre
1. Corre la compuerta antisesgo (`compuerta_antisesgo.md`). El costo hundido empuja a seguir y el cansancio empuja a cerrar sin mirar los datos.
2. Revisa los criterios de TPL-095 (pre-mortem) fijados antes, si existen. Pregunta: ¿qué dijimos que nos haría detenernos?
3. Elige con el fundador:
   - **Pivote:** cambia una pieza (segmento, problema, canal, modelo de cobro) y conserva lo validado.
   - **Pausa:** congela gastos con una fecha y una condición para retomar.
   - **Cierre:** termina la empresa o el proyecto.
4. Registra la decisión en `decisiones.csv` con su evidencia (`gate=<actual> decision=Kill` o `Recycle`).

## 2. Archivar sin contaminar el ciclo nuevo (pivote)
- Marca como `descartado` las hipótesis refutadas en `hipotesis.csv` y escribe en `criterio_rechazo` la razón. No borres filas: el historial es evidencia.
- **Lo que se conserva:** entrevistas y evidencias que siguen valiendo para el nuevo foco. Cita sus IDs en las nuevas hipótesis.
- **Para empezar de cero en otra carpeta:** guarda una copia del expediente actual con `expediente.py empaquetar --dir <carpeta> --salida <carpeta>/archivo` y crea un expediente nuevo.
- `auditar.py` avisa si quedan experimentos abiertos sobre hipótesis descartadas (posible costo hundido).

## 3. Si hay un proyecto CORFO vigente
Revisa las Bases Administrativas Generales (BAG, Res. 28/2020 y sus modificaciones) y las bases del instrumento. Al 2026-11-25:
- **Avisar a tiempo es una obligación (BAG 11.3).** Si el proyecto no alcanzará sus resultados, el beneficiario debe informar y proponer el término anticipado. Omitir ese aviso figura entre las causales de término **imputable**.
- **Término por causa no imputable (14.1.3.1):**
  - se entrega un informe final de cierre en un plazo de hasta 30 días;
  - se restituye todo saldo no gastado, no rendido u observado;
  - si no se restituye, CORFO cobra la garantía.
- **Término por causa imputable (14.1.3.2):** negligencia, no informar, rendiciones duplicadas o documentos falsos.
  - Se restituye **todo** el subsidio recibido.
  - CORFO cobra las garantías.
- **Pivote dentro del proyecto (BAG 11.6 y 11.7):**
  - Se pueden pedir modificaciones que **no alteren la naturaleza ni el objetivo general**.
  - Si afectan cláusulas del convenio, se firma un modificatorio.
  - En Semilla Expande 2026, los cambios al plan y presupuesto se piden hasta 1 mes antes del término.
  - Si el pivote cambia el objetivo general, corresponde término anticipado, no modificación.
- **Equipo y propiedad:**
  - Los cambios de propiedad se informan antes de concretarse.
  - El retiro de un integrante sin reemplazo autorizado puede causar término anticipado (Semilla Expande 2026).
  - La entidad patrocinadora responde junto al beneficiario.
- No encontramos una inhabilidad expresa para volver a postular tras un término no imputable. Confírmalo con el ejecutivo.
- **Acción:** reunión con el ejecutivo CORFO y la patrocinadora **antes** de decidir. Lleva `fondos_lint.py rendiciones` al día y el saldo por rendir.

## 4. Cerrar la empresa (SpA) en Chile
Orden habitual (confírmalo con contador y abogado):
1. **Trabajadores (Código del Trabajo):**
   - Despido por necesidades de la empresa (art. 161) con aviso de 30 días, con copia a la Inspección, o una remuneración sustitutiva (art. 162).
   - Indemnización de 30 días por año, con tope de 330 días y base máxima de 90 UF (arts. 163 y 172).
   - **Cotizaciones al día:** si no lo están, el despido no termina el contrato (art. 162).
   - Finiquito pagado dentro de 10 días hábiles; puede firmarse en el sitio de la DT (art. 177).
   - Calcula el costo con `finanzas.py costo-empleado` como referencia.
2. **Término de giro en el SII:**
   - Se presenta en línea (formulario 2121) dentro de los **2 meses** siguientes al cese, con el balance final (art. 69 del Código Tributario; Circular SII 32/2025).
   - Antes hay que cerrar pendientes: anular folios, desafiliarse como facturador electrónico, libros.
   - El SII revisa en 6 meses (ampliables a 9). Las Pro Pyme tienen un procedimiento abreviado si los socios asumen responsabilidad solidaria.
   - El aviso tardío se multa.
3. **Disolución** en el Registro de Empresas y Sociedades ("Tu Empresa en un Día", opción "Disolver"), **después** del término de giro si hubo inicio de actividades.
4. **Si hay deudas que no se pueden pagar** (Ley 20.720, con abogado):
   - liquidación voluntaria;
   - liquidación voluntaria simplificada (micro y pequeñas empresas, Ley 21.563);
   - reorganización simplificada con veedor.
   
   La Superintendencia de Insolvencia y Reemprendimiento orienta.
5. **Activos y PI:** decide qué pasa con el código, la marca y el dominio (venta, cesión a los socios o liberación). Respeta las licencias y los contratos con clientes, incluida la devolución o eliminación de sus datos (`privacidad.md`).

## 5. Cierre del aprendizaje
- Escribe un informe de una página: qué se probó, qué se aprendió, qué haríamos distinto y qué evidencia sirve para otro proyecto.
- Guarda el expediente con `empaquetar`.
- Si el fundador quiere, conviértelo en un caso para su incubadora sin datos personales.
