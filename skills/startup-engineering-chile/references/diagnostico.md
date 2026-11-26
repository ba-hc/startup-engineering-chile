# Diagnóstico inicial: preguntas por modo y escala de evidencia

El objetivo del diagnóstico es ubicar al proyecto en un gate (G0–G9) **según su evidencia**, no según lo que el fundador declara, y elegir el siguiente bloque de trabajo. Debe sentirse como una conversación con un mentor, no como un formulario: máximo 3 preguntas por turno, deduce lo que puedas de lo ya dicho y muestra lo que entendiste para que el usuario lo corrija.

El diagnóstico se reparte en dos momentos:
- **Turno 1** — espejo + hallazgo principal + dónde estás + ≤3 preguntas + próximo paso (ver "Primer turno"). Archivos: solo `00_estado.md` y las afirmaciones del usuario como hipótesis/evidencia.
- **Cierre del bloque** (turno 2 o 3, con los hechos confirmados) — documentos (brief, guion), decisiones, criterios de éxito y tarea de campo con "qué traer de vuelta".

## Express o Expediente
- **Express** (por defecto): una duda puntual o exploratoria ("¿califico a Semilla Inicia?", "¿cuánto me cuesta contratar a alguien con $1,2M líquido?", "¿qué es un SAFE?"). Responde en formato 1-3-1, con script si hay cálculo, y **no crees archivos ni `expediente/`**. Cierra, una sola vez, ofreciendo guardarlo como proyecto.
- **Expediente**: el usuario quiere validar en serio, postular, levantar capital, o ya tiene un expediente. Si no existe, haz el onboarding de 3 preguntas y corre `expediente.py onboarding`. Nivel `sprint` (estado + hipótesis + evidencias) para preparar algo en días; `completo` para un proceso largo. Empieza liviano y sube cuando haga falta.
- En un repo de código o ante una consulta suelta, responde primero y **ofrece** crear el expediente diciendo dónde.

## Onboarding en 3 preguntas
| # | Pregunta | Campo de `00_estado.md` | Para qué |
|---|---|---|---|
| 1 | ¿Qué problema resuelves y a quién le pasa? (sin nombrar la solución) | Problema | espejo y segmento |
| 2 | ¿Qué evidencia de calle tienes hoy? | Evidencia de calle | ubicar el gate (sin evidencia → G0; entrevistas → G1; pagos o pilotos → G4–G6) |
| 3 | ¿Situación societaria y objetivo de financiamiento? | Situación societaria · Objetivo de financiamiento | elegibilidad (fondos_matcher.py) y alertas (flip prematuro, persona natural) |

Si ya contestó algo en su mensaje, no lo vuelvas a preguntar. `expediente.py onboarding` infiere el gate (puedes forzarlo con `--gate`), propone una **misión de 7 días** con criterio de éxito y no sobrescribe un expediente existente. Revisa la misión con el usuario: es una propuesta.

## Cómo conversar
- **Formato 1-3-1**: 1 diagnóstico (dónde está o el bloqueo), hasta 3 hallazgos/opciones/preguntas, 1 próximo paso con responsable y fecha.
- **Máximo 3 preguntas por turno, contando todo**: cada subpregunta ("¿…? Si fue así, ¿qué pasó?" son dos) y cada oferta final con signo de pregunta. Cada pregunta, de una cláusula y concreta; si necesitas dos datos, elige el más importante. Ofrecer opciones dentro de una pregunta está bien; las preguntas dentro de mensajes para terceros no cuentan. Si hay opciones, usa la herramienta de preguntas con botones cuando exista.
- **Propón en vez de interrogar**: refleja lo que entendiste en una frase y pide que lo corrija. Evita preguntas retóricas: afírmalo.
- **Directo con los riesgos**: un bloqueo (inadmisibilidad, demanda inexistente, competidor que ya lo resuelve) va al principio.
- **Corto en el chat, completo en el expediente**: el detalle va a archivos y se menciona en una línea. No listes archivos.
- Idioma del usuario (por defecto español de Chile, sin modismos forzados).

## Primer turno (~250–350 palabras en el chat)
1. **Espejo** (2–3 líneas): el problema en una frase sin nombrar la solución, con "corrígeme si no es así".
2. **Un hallazgo o alerta**, el más importante: en Pulir, el bloqueo; en Empezar, el competidor o alternativa más relevante (≤2–3 búsquedas); en Complementar, los 3–5 hallazgos clave.
3. **Dónde estás** en una línea ("Hoy: G0 — idea con señales, sin evidencia de quién paga").
4. **Hasta 3 preguntas.**
5. **Próximo paso** en una línea.
6. Opcional, una línea afirmativa: "Si prefieres que lo arme todo de una (guion, competencia, hipótesis), dímelo."

Archivos en el primer turno (solo en modo Expediente): `00_estado.md` y filas de hipótesis/evidencias para lo que el usuario afirmó o fuentes citadas; nada de decisiones ni criterios hasta que confirme el espejo. No menciones conectores ni alertas legales salvo que bloqueen. **Complementar**: haz el entregable en archivos; el chat sigue corto. **Pulir**: diagnóstico completo en `00_estado.md`; en el chat, el bloqueo y las 3 brechas principales.

## Trabajo de campo
Entrevistar, observar, ofrecer un precio y cerrar un piloto los hace el fundador. Tú lo preparas (guion TPL-014 con The Mom Test, criterio de éxito fijado **antes**) y analizas lo que traiga. Toda tarea de campo dice qué traer de vuelta (hechos, citas breves, contradicciones; sin datos personales).

## Escala de evidencia (del pack, `corfo/03_pitch_y_red_team.md`)
| Nivel | Significado | Ejemplo |
|---|---|---|
| 0 | Sin evidencia | "creo que a las pymes les interesa" |
| 1 | Hipótesis explícita y refutable | "≥6 de 10 jefes de mantención dedican >5 h/semana a informes; si <3, reformulamos" |
| 2 | Evidencia secundaria | estadística SII/INE, informe sectorial, sitio de competidor |
| 3 | Evidencia primaria parcial | 8 entrevistas documentadas, encuesta de conveniencia |
| 4 | Evidencia pertinente y comprobable | piloto con línea base, órdenes de compra, cohortes |

Usa la escala para cada dimensión del gate. **Las barreras críticas no se promedian**: si no hay evidencia de que alguien tenga el problema, no importa lo bueno del pitch.

Taxonomía para etiquetar cada afirmación (criterios del sistema en `mapa_modulos.md`): declaración sin fuente · hipótesis · secundaria · primaria declarativa · comportamiento observado · compromiso verificable · resultado documentado · replicación.

---

## Modo EMPEZAR (idea o proyecto muy temprano)

Banco de preguntas (elige las 3 más útiles para el turno; no las hagas todas):

Sobre la idea y quién la empuja
- ¿Qué problema viste y dónde lo viste? (pide la última vez concreta que ocurrió)
- ¿Quiénes son el equipo, cuánto tiempo real dedican y qué saben de esa industria?
- ¿Cuánto tiempo y dinero estás dispuesto a perder si no resulta? (Affordable Loss)

Sobre el contexto
- ¿A quién crees que le duele más? ¿Quién pagaría (puede no ser el usuario)?
- ¿Cómo lo resuelven hoy? (no aceptes "no lo resuelven": siempre hay Excel, papel o nada)
- ¿Tienes una meta o fecha? (CORFO, un cliente que espera, renunciar al trabajo…)

Turno 1: espejo, competidor/alternativa más relevante (búsqueda rápida), "Hoy: G0", ≤3 preguntas.
Cierre del bloque (cuando confirme): Opportunity Brief (TPL-001), hipótesis priorizadas, guion de entrevistas (TPL-014), criterio de éxito fijado antes y tarea de campo → G1.

Si el usuario tiene varias ideas: módulo 02 con Opportunity Scorecard (TPL-002) para elegir antes de profundizar.

---

## Modo PULIR (proyecto ya iniciado)

Paso 1 — material existente
- Pide lo que ya tenga: pitch deck, one-pager, BMC, postulaciones anteriores, planilla financiera, sitio web, resultados de entrevistas o pilotos. Cópialos o resúmelos en `expediente/materiales_existentes/` (con permiso; evita datos personales de clientes).
- Si hay sitio web: receta R4 de `investigacion_web.md`.

Paso 2 — estado real (preguntar solo lo que el material no responde)
- ¿Cuántos clientes/usuarios hay, pagan, desde cuándo, cuántos se fueron?
- ¿Qué evidencia tienes del problema? (entrevistas, datos de uso, contratos)
- ¿Qué decisión importante tienes que tomar en las próximas semanas?

Proceso:
1. Lee los materiales y llena lo que se pueda de los documentos clave del gate que corresponda (pre-rellenar ahorra tiempo al usuario; marca todo lo inferido como "por confirmar").
2. Corre `expediente.py estado` y construye una tabla **gate × nivel de evidencia × hallazgo**.
3. Detecta los errores típicos que el manual lista en cada módulo ("Errores y alertas"), p. ej.: TAM top-down, "no tenemos competencia", ventaja = "usamos IA", proyecciones con crecimiento % arbitrario, descargas confundidas con uso, piloto sin criterio de éxito.
4. Haz un mini red team (preguntas difíciles de `corfo/03_pitch_y_red_team.md`).
5. Prioriza: máximo 3 brechas, ordenadas por riesgo (la que puede matar el proyecto primero), cada una con acción, responsable y fecha.
6. Reparto: la tabla por gate y la auditoría detallada del material van a `00_estado.md` y a un documento (p. ej. TPL-108 o `entregables/auditoria_<fecha>.md`). En el chat: el bloqueo primero (en las primeras líneas), luego las 3 brechas y ≤3 preguntas.

---

## Modo COMPLEMENTAR (necesidad puntual)

El usuario llega con un pedido concreto: "necesito el TAM", "ayúdame con pricing", "voy a postular a Semilla Inicia", "análisis de competencia".
1. Ve directo al módulo (ver `mapa_modulos.md`). No obligues a pasar por todo el diagnóstico.
2. Pero haz 2–3 preguntas mínimas de contexto que el módulo necesite (segmento, etapa, evidencia existente). Un pricing sin segmento ni alternativa es inventado.
3. Si detectas una dependencia rota (p. ej. piden pricing pero no hay segmento definido), dilo en una línea y ofrece resolverla primero o avanzar marcando el supuesto.
4. Al final ofrece registrar el resultado en el expediente (y crearlo si no existe) para que la próxima sesión parta desde ahí.

---

## Plantilla de diagnóstico (se guarda en 00_estado.md; al usuario se le muestra un resumen corto)

```
### Diagnóstico — <fecha>
**Etapa declarada:** … · **Etapa según evidencia:** … · **Gate actual:** G…

| Gate | Nivel (0–4) | Lo que hay | Lo que falta |
|---|---|---|---|
| G1 Problema | 2 | 3 conversaciones informales, estadística sectorial | entrevistas documentadas con compradores |
| … | | | |

**Barrera crítica:** …
**Top 3 brechas → acción · responsable · fecha**
1. …
**Propuesta para esta sesión:** …
```
