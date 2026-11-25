# Retomar una sesión y vuelco semanal

El mensaje de retomar es corto (~300–400 palabras): veredicto, lo inesperado, la decisión propuesta, el siguiente paso y ≤3 preguntas. La síntesis por entrevista, el conteo contra el criterio y los planes van al expediente (TPL-016, `experimentos.csv`, `00_estado.md`) y se mencionan en una línea. Si incluyes mensajes de contacto, dos cortos (≤50 palabras cada uno) en el chat y el resto en el expediente.

## Pasos
0. **Si los archivos no persisten** (Claude.ai u otra app de chat): si el usuario subió el ZIP de su expediente, `expediente.py restaurar <zip> --dir <carpeta>`; si pegó un resumen (`expediente.py resumen`), úsalo como estado y propón recrear el expediente con `init` y los registros que el resumen cite. Si no trae ninguno de los dos, pregúntale una vez si lo tiene antes de empezar de cero.
1. Lee la salida de `expediente.py estado`: ruta por gates, trabajo de campo pendiente, acciones vencidas, **hipótesis estancadas** (>14 días sin experimento ni evidencia nueva) y registros por confirmar. Si dice que el esquema es antiguo, corre `expediente.py migrar` antes de escribir.
2. Abre con una línea de dónde quedaron y pregunta por lo pendiente ("¿cómo te fue con las entrevistas?").
3. Según lo que traiga:
   - **Trae resultados** (notas de entrevistas, datos de piloto, respuestas a precio): si son transcripciones o notas con nombres, pásalas primero por `ingesta.py anonimizar` (ver `privacidad.md`). Analízalas con TPL-015/016, regístralas (`add entrevistas …`, `add evidencias …`), compáralas con el criterio fijado antes en `experimentos.csv` / `00_estado.md`, y decide. Si no se cumplió, dilo y registra Recycle/Kill/Hold con lo aprendido; señala hallazgos inesperados que abren otra hipótesis. **No ajustes el umbral a posteriori.**
   - **No hizo el trabajo de campo** (lo más común): no produzcas más documentos para llenar el vacío ni avances a diseñar producto. Diagnostica el bloqueo (casi siempre reclutar): redacta 2–3 mensajes de contacto listos para WhatsApp/LinkedIn/correo, sugiere dónde encontrar personas (ex colegas, colegios profesionales, gremios, grupos sectoriales) y achica el paso (2 conversaciones esta semana).
   - **Acciones vencidas > 2 semanas:** replanifica con el usuario; pregunta si el objetivo sigue vigente.
   - **Hipótesis estancadas:** propone el experimento más barato que las mueva, o descartarlas si ya no importan.
   - **Registros `propuesta-agente`:** pide que confirme o corrija los relevantes.
   - **Contradicciones y sesgos:** corre `auditar.py --dir <carpeta>`. Menciona solo las alertas que cambian la decisión de hoy (Go sin evidencia, resultado bajo el umbral, entrevistas complacientes, costo hundido); el resto queda en `00_estado.md`.
4. **"¿Dónde estoy?" / "ver mi ruta":** la tabla Ruta en ≤10 líneas y el siguiente paso. Si quiere algo visual o para compartir: `dashboard.py --dir <carpeta>`.
5. **Cierre de cada sesión:** actualiza Ruta, Foco, Trabajo de campo pendiente (tarea, plazo, criterio fijado antes, **qué traer de vuelta**), Próximas acciones y una fila de bitácora con "Para la próxima". Corre `expediente.py validar` si agregaste muchas filas. Si el entorno no conserva archivos, termina con `expediente.py empaquetar --dir <carpeta> --salida <carpeta descargable>` (en Claude.ai suele ser `/mnt/user-data/outputs`) y pide al usuario que descargue el ZIP y lo suba la próxima vez; si cambiará de conversación o de modelo, entrégale también `expediente.py resumen`.

## Vuelco semanal en 5 minutos
Cuando el fundador pega notas desordenadas o un resumen hablado de su semana ("hablé con 3 plantas, una pidió precio, el socio se va de vacaciones…"):
1. Anonimiza si trae nombres o contactos.
2. Separa en hechos (qué pasó), compromisos (tiempo, datos o dinero que alguien puso), opiniones y tareas. Las opiniones amables no son evidencia.
3. Propón en **una tabla** las filas a registrar (entrevistas, evidencias, cuentas_y_pipeline, acciones en `00_estado.md`) con su estado `propuesta-agente`; pide una confirmación en bloque ("¿lo guardo así?").
4. Tras confirmar, regístralas con `expediente.py add … --confirmado` y actualiza `00_estado.md`.
5. Señala lo que el vuelco revela: hipótesis estancadas, una cuenta que avanzó o se enfrió, acciones vencidas.
6. Si lo pide, `expediente.py informe semanal` genera el reporte para socios o mentores, y con eso redactas el correo mensual a inversionistas o mentores (logros, números, qué aprendimos, en qué pueden ayudar), citando solo lo registrado.
