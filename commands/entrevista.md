---
description: Prepara entrevistas de descubrimiento (Mom Test) o analiza las notas que trajiste, anonimizadas
argument-hint: "[segmento a entrevistar | archivo de notas]"
---

Usa la skill **startup-engineering-chile** y lee `skills/startup-engineering-chile/references/flujos/privacidad.md` antes de tocar notas.

Entrada: $ARGUMENTS

**Si trae notas o transcripciones** (archivo o texto pegado):
1. Anonimiza primero: `python <skill>/scripts/ingestar.py anonimizar <archivo> --dir <carpeta>` (agrega `--nombres "…"` con los nombres que conozcas). Trabaja solo con la versión `_anon.md`; nunca copies nombres, correos, teléfonos ni RUT al expediente o al chat.
2. Separa hechos del pasado, opiniones y pedidos de funcionalidades. Contrasta con las hipótesis (`expediente.py ver hipotesis`) y su criterio de éxito fijado antes.
3. Registra con `expediente.py add entrevistas …` y `add evidencias …` (ENT-xxx, rol, segmento).

**Si va a salir a entrevistar**:
1. Crea o ajusta el guion: `expediente.py doc TPL-014 --dir <carpeta>`. Preguntas sobre la última vez que pasó, nada de "¿usarías…?".
2. Fija antes del terreno cuántas entrevistas y qué resultado confirma o refuta la hipótesis (`expediente.py umbrales --gate G1`).
3. Di qué traer de vuelta: hechos, citas breves, montos y frecuencias, sin datos personales.

Responde en formato 1-3-1: **1** qué aprendiste o qué vas a probar, **3** hallazgos o preguntas clave, **1** próximo paso (cuántas entrevistas más, con quién, para cuándo). El fundador hace las entrevistas: nunca las inventes ni las simules como evidencia.
