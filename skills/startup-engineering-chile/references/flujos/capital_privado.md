# Levantar capital privado: ángeles, aceleradoras, SAFE y VC

**Última verificación:** 2026-11-25. Orientación educativa: el instrumento y el pacto se revisan con abogado. Complementa el módulo 26 del manual.

## 0. ¿Conviene levantar ahora?
Antes de hablar de montos, responde con el fundador:
- **¿Para qué hito es la plata?** Escribe el hito verificable que se alcanza (p. ej. "G7: 10 clientes pagando") y cuánto cuesta llegar (`finanzas.py runway`).
- **¿Hay alternativa no dilutiva?** Ver `fondos.md`. Un subsidio de $15–75M sin ceder participación puede bastar para llegar al hito.
- **¿El negocio puede ser grande?** Un fondo de capital de riesgo busca retornos muy altos. Si el plan es una empresa rentable de tamaño medio, conviene más deuda, clientes o ángeles.
- **¿Qué evidencia hay?** En seed, los inversionistas miran sobre todo equipo, problema confirmado (G1–G3) y alguna tracción (G6–G7). Sin eso, prioriza terreno.

## 1. Mapa de fuentes en Chile (verificar antes de citar)
| Fuente | Qué ofrece (al 2026-11-25) | Fuente |
|---|---|---|
| **Start-Up Chile** | Subsidio sin cesión de participación. Build hasta $15M (90%), Ignite hasta $30M (80%; 90% si la líder es mujer), Growth hasta $75M (50%/60%; ventas de 2.400–25.000 UF). | startupchile.org |
| **Platanus Ventures** | USD 200.000 por 7% mediante SAFE post-money, con términos iguales para todos. Programa de 3 meses; exige un fundador técnico; invierte desde la idea. | platan.us/programa |
| **Redes de ángeles** | ChileGlobal Angels (Fundación Chile), Red de Ángeles UDD (programa Corfo "Invierte") y otras. No publican tickets. | fch.cl, uddventures |
| **Fondos con línea Corfo** | Corfo presta a fondos privados (FET, FT, FC) y estos invierten. La startup contacta a la administradora, no a Corfo. | corfo.gob.cl, programas de capital de riesgo |
| **Fondos regionales** | Fondos semilla y Serie A de LatAm. Muchos exigen trasladar la matriz a Delaware o Caimán en etapas de crecimiento. | `internacionalizacion.md` |

`expediente.py biblioteca "ángeles"` muestra fuentes adicionales con su estado de verificación.

## 2. Instrumentos
- **SAFE:** es el instrumento temprano más usado en Chile, adaptado desde el modelo de YC. No es deuda: normalmente no tiene vencimiento ni interés, y lleva cap y a veces descuento (Chambers, *Venture Capital 2026 – Chile*). YC no publica una versión para Chile, y Platanus publica modelos en español.
  - **Tributación:** el SII (Oficio 2219/2024, según resúmenes de estudios jurídicos) aceptó que un SAFE puede no ser mutuo. En ese caso no paga Impuesto de Timbres, y el costo tributario de las acciones es el monto invertido.
  - **Con abogado:** confirmar que esto aplica al texto exacto que se firma.
- **Nota convertible:** es deuda que se convierte en acciones. Paga Impuesto de Timbres (0,066% por mes, tope 0,8%) y tiene vencimiento.
- **Ronda con precio:** es un aumento de capital en la SpA que acuerdan los accionistas (art. 434 del Código de Comercio). Hay que actualizar el registro de accionistas (art. 431). El estatuto de la SpA se pacta libremente (art. 424).
- **Simula siempre:**
  - `finanzas.py dilucion --fundadores "A:50,B:50" --pool 10 --safe 100000000:1500000000 --safe 50000000:0:20 --pre 3000000000 --inversion 800000000 --pool-post 10` muestra la tabla de propiedad antes y después, a qué precio convierte cada SAFE y quién paga el aumento del pool.
  - `finanzas.py salida --comunes … --preferentes … --valores …` muestra cuánto recibe cada uno en distintas salidas.

## 3. Términos que hay que entender antes de firmar
| Término | Lo habitual en seed | Señal de alerta |
|---|---|---|
| Preferencia de liquidación | 1x no participativa, sin dividendos acumulativos | Más de 1x, o participativa |
| Vesting de fundadores | 4 años con cliff de 1 año; *reverse vesting* | Sin aceleración razonable ante despido sin causa |
| Pool de opciones | 5–10% en Chile; ~10% en seed según Index Ventures | Pool grande creado antes de la ronda (lo pagan solo los fundadores) |
| Pro rata | Derecho a mantener el % en rondas siguientes | Derechos de veto amplios para un ticket chico |
| Cap del SAFE | Coherente con la tracción y comparables | Cap muy alto que complica la ronda siguiente |

Fuentes: Chambers 2026 (Chile), Index Ventures *Rewarding Talent* y datos de Carta 2024–2025: menos del 5% de los acuerdos seed tuvo preferencia mayor a 1x.

## 4. Proceso (6–12 semanas)
1. **Materiales desde el expediente:**
   - `expediente.py informe deck`: borrador en Marp con cada vacío marcado [FALTA EVIDENCIA];
   - `informe onepager`;
   - modelo con `finanzas.py escenarios --modelo`;
   - data room mínimo: estatutos, registro de accionistas, pacto, PI cedida a la SpA, contratos con clientes y estados financieros. `dataroom.py revisar --dir <carpeta>` muestra qué falta en 9 carpetas y qué cifras del pitch no tienen EV-; `dataroom.py armar --zip` lo empaqueta sin notas de entrevistas;
   - cap table al día: `cap_table.py ver` y, para la ronda, `cap_table.py ronda --pre … --inversion … --pool-post …`.
2. **Lista de 30–60 inversionistas** con tesis compatible (etapa, sector, ticket). Regístralos en `cuentas_y_pipeline.csv` con `segmento=inversionista`.
3. **Red team antes de salir** (`red_team.md`, rol "Inversionista seed LatAm") y compuerta antisesgo (`compuerta_antisesgo.md`).
4. **Reuniones en bloque** de 2–3 semanas para crear ritmo. Registra cada objeción como evidencia: tres objeciones iguales son una hipótesis por probar, no un problema de pitch.
5. **Term sheet:** compáralo con la tabla del punto 3, simula con `finanzas.py` y revísalo con abogado antes de firmar.

## 5. Beneficios tributarios para inversionistas (estado al 2026-11-25)
- **Art. 107 de la LIR:** la Ley 21.850 vuelve a dejar exenta, desde el 01-01-2027, la ganancia de acciones con presencia bursátil. *Inferencia:* las acciones de una SpA que no cotiza normalmente no califican.
- **Proyecto MK4 (Boletín 18.643-05, en el Senado):** incluiría un estatuto de capital de riesgo, extendería el art. 107 a SpA y daría un crédito de 35% para personas naturales (tope 50 UTA), según prensa. **Es un proyecto, no una ley:** no lo presentes como beneficio vigente.

Cierra con: decisión de levantar o no (`decisiones.csv`, gate G9 o el actual), monto, hito y fecha límite. Si se decide no levantar todavía, anota qué evidencia lo cambiaría.
