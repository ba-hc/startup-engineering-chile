# TPL-068 — Informe de resultados de piloto (Pilot Results Report)

**Para qué:** contrastar el resultado con el criterio del acta, separar lo atribuible al producto de los confusores y cerrar con una decisión comercial. · **Gate:** G6–G7 · **Alimenta:** `pilotos.csv`, `evidencias.csv`, `decisiones.csv`

## Completar
**Piloto:** [PIL-ID, cuenta_id, fecha de firma del acta TPL-067] · **Pregunta del piloto (copiada del acta):** [ ]

### 1. Resultado vs. criterio fijado
| KPI-ID | Baseline | Meta del acta | Resultado | n / período | ¿Cumple? | EV-ID |
|---|---|---|---|---|---|---|

*Copia la meta tal como se firmó; si cambió, dilo aquí y explica por qué.*

### 2. Comparación y atribución
Diseño: [antes/después · grupo control · despliegue escalonado] · Confusores: [estacionalidad, promociones, cambios de personal, otros proyectos] · Cambio atribuible y nivel de confianza: [ ]

### 3. Adopción e implementación
Uso real: [% de usuarios activos semanales, tareas hechas en el sistema vs. fuera] · Guardrails: [ ] · Costo real de implementar y soportar (horas startup + horas cliente): [ ]

### 4. Lo que no funcionó
[fallas, rechazos, usuarios que volvieron a la alternativa] *Lo desfavorable va antes que cualquier testimonio.*

### 5. Decisión comercial
[contrato / extensión pagada / rechazo documentado], monto, fecha y quién decidió en el cliente.

## Ejemplo bueno (ficticio)
"GóndolaViva", alertas de reposición por cámara para una cadena regional de ferreterías, Región del Biobío. PIL-002 · CTA-007 · acta firmada 2-09-2026.

| KPI | Baseline | Meta | Resultado | n | ¿Cumple? | EV |
|---|---|---|---|---|---|---|
| KPI-006: % de horas con quiebre en 120 SKU críticos, locales piloto | 8,4% | ≤5,5% | 5,9% | 4 locales, 8 sem | No | EV-031 |
| Mismo KPI, locales control | 8,1% | – | 7,6% | 4 locales, 8 sem | – | EV-032 |

- Diseño: piloto vs. control pareado por ventas. Atribuible ≈ 2,0 pp (−2,5 vs −0,5). Confusor: campaña de temporada en 2 locales piloto (EV-033). Confianza moderada: solo 8 locales.
- Adopción: 9 de 12 reponedores atendieron ≥70% de las alertas; en turno noche se ignoraron. Guardrail ok: sin aumento de horas extra. Implementación: 46 h startup + 20 h cliente.
- No funcionó: 18% de falsas alertas en el pasillo de pinturas por reflejos.
- Decisión: meta no cumplida. El gerente de operaciones aprueba una extensión pagada de 6 semanas en 2 locales a 40 UF + IVA para corregir falsas alertas, con el mismo umbral (DEC-012).

## Ejemplo malo y por qué falla
"El piloto fue un éxito: los quiebres bajaron 30% y el equipo quedó muy contento ('nos cambió la vida', dijo un jefe de local). Recomendamos escalar a toda la cadena."
- No compara con la meta del acta ni con un control: el 30% puede ser la campaña de temporada.
- Usa un testimonio como prueba de adopción; no hay uso real ni n.
- Omite lo que falló y el costo de implementación.
- "Recomendamos escalar" no es una decisión comercial del cliente.

## Criterio de aceptación
- Pregunta y meta coinciden con el acta firmada, o el cambio está declarado.
- Hay comparador (control o antes/después) y al menos un confusor analizado.
- La adopción se mide con uso real y se incluye el costo de implementación.
- Cierra en contrato, extensión pagada o rechazo, registrado en `pilotos.csv` (decision_comercial) y `decisiones.csv`.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
