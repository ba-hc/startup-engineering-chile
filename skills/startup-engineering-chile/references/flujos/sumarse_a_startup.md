# Sumarse a una startup ajena: evaluar una oferta de opciones o equity

Para quien recibe una oferta como primer empleado, socio tardío o asesor. No es la startup del usuario, así que **no hace falta crear expediente**: responde como consulta puntual y ofrece guardar el análisis en un documento si lo pide.

**Última verificación:** 2026-11-25. No reemplaza a un abogado ni a un contador.

## 1. Las preguntas que hay que hacer (pídelas por escrito)
1. **¿Qué % representa la oferta y sobre qué base?** Debe ser *fully diluted*: acciones emitidas, más pool de opciones completo, más SAFE y notas convertidos. Un "1%" sobre acciones emitidas puede ser bastante menos después.
2. **¿Cuántas acciones hay en total, incluidas las preferentes?** (Carta, Holloway).
3. **¿Qué instrumentos hay por convertir?** SAFE, notas, warrants, y con qué cap y descuento.
4. **¿Cuánta preferencia de liquidación va antes que los comunes?** Es la suma de lo invertido × su múltiplo. Bajo ese valor de salida, tus acciones valen cero.
5. **Precio de ejercicio y forma de pago.**
6. **Vesting:** plazo, cliff y qué pasa si te despiden sin causa.
7. **Aceleración:** single o double trigger. Index Ventures recomienda como máximo *double-trigger* parcial para ejecutivos.
8. **Ventana para ejercer si te vas:** lo típico en EE.UU. son 90 días; algunas empresas la extienden.
9. **¿La empresa puede recomprar tus acciones, y a qué precio?**
10. **¿Es un plan formal pactado en tu contrato de trabajo?** Cambia el impuesto (punto 3).

## 2. Cuánto vale (en escenarios, no como promesa)
Usa los números de la empresa y corre:
```
python <skill>/scripts/finanzas.py salida --comunes "Fundadores:8000000,Pool emitido:500000" \
  --preferentes "Seed:1500000000:2000000" --opciones "Mi oferta:100000:150" \
  --valores 2000000000,10000000000,40000000000
```
Muestra cuánto recibirías en cada valor de salida, después de preferencias y del precio de ejercicio.

Compara con lo que dejas de ganar: (sueldo de mercado − sueldo ofrecido) × años de vesting. Si la diferencia es grande, la oferta solo conviene si de verdad crees en un escenario alto, y aun así es un boleto de lotería con probabilidad baja.

Señales de una oferta razonable para un primer empleado clave en seed:
- vesting de 4 años con cliff de 1;
- ventana de ejercicio no menor a 90 días;
- información completa de la tabla de propiedad.

## 3. Impuestos en Chile (SII, Circular 43 de 2021, art. 17 N°8 letra l) LIR)
- **Plan pactado en el contrato de trabajo** (individual o colectivo):
  - ni la entrega ni el ejercicio de la opción son renta;
  - al vender las acciones se tributa por la diferencia con lo pagado, reajustada por IPC.
- **Plan NO pactado en el contrato:** el ejercicio se grava como mayor remuneración (impuesto único de segunda categoría) sobre la diferencia entre el valor de las acciones y lo pagado. Puede generar impuesto sin haber recibido caja.
- **Asesores o socios que no son trabajadores:** la circular no los cubre directamente; se analiza el contrato caso a caso.
- **Phantom shares** (bono ligado al valor): no hay oficio específico. *Inferencia:* probablemente tributan como remuneración al pagarse. Confírmalo con un contador.
- Si la matriz está en Delaware, también aplica la tributación de EE.UU. sobre las opciones: requiere asesoría en ambos países.

## 4. Socio tardío (entra con acciones, no con opciones)
- Mismas preguntas del punto 1, más:
  - pacto de accionistas vigente;
  - vesting propio (es razonable aceptar uno);
  - cesión de PI de lo que aportes;
  - obligaciones como accionista de una SpA.
- Pide ver el registro de accionistas (art. 431 del Código de Comercio) y los estatutos.
- Ver `socios_equity.md` para el pacto.

## 5. Cierre
Un resumen de una página:
- qué te ofrecen;
- qué falta saber;
- tres escenarios de valor;
- costo de oportunidad;
- riesgos;
- recomendación de qué negociar (lo más negociable suele ser la ventana de ejercicio, la aceleración y la información).

Si el usuario lo pide, guárdalo como documento. No lo registres en un expediente de startup.
