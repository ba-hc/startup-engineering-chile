# TPL-016 — Matriz de codificación cualitativa (Qualitative Coding Matrix)

> **Para qué sirve:** Convertir un conjunto de entrevistas en conclusiones auditables por segmento, con casos negativos y saturación documentada.
> **Cuándo NO usarla:** Con menos de 5–6 entrevistas por segmento; con tan poco material la matriz aparenta un rigor que los datos no tienen.
> **Micro-ejemplo resuelto:** De 14 entrevistas a colegios, el código "asistencia registrada a mano" aparece en 9 de 10 subvencionados y en 1 de 4 particulares; la conclusión se limita a subvencionados y se anota que las 2 últimas entrevistas no agregaron códigos nuevos (saturación).

**Gate:** G1(–G2) · **Alimenta:** `evidencias.csv`, `hipotesis.csv`

## Completar
**1. Libro de códigos** *(defínelo antes de codificar el lote; si agregas un código después, anótalo con fecha)*
| Código | Definición | Incluye / excluye | H-xxx |
|---|---|---|---|
| C1 | [ ] | [ ] | |

**2. Matriz** — filas = entrevistas agrupadas por segmento; celdas = hecho resumido + intensidad (0 ausente, 1 menciona, 2 relata un caso, 3 caso con costo medido).
| ENT | Segmento | C1 | C2 | C3 | Caso negativo |
|---|---|---|---|---|---|

**3. Saturación por segmento:** códigos nuevos en entrevistas 1–3: [ ] · 4–6: [ ] · 7–9: [ ]
**4. Conclusiones:** [afirmación] — respaldan [ENT-…] · contradicen [ENT-…] · nivel de evidencia [0–4]
**5. Sesgos y límites:** [reclutamiento, rol del entrevistador, lo que no se preguntó]
*Cuenta casos con su ID ("5 de 5"), no adjetivos ("muchos"); una conclusión sin el caso que la contradice no es auditable.*

## Ejemplo bueno (ficticio)
Proyecto "Suplente" — reemplazos cuando falta un profesor, colegios de la Región de Valparaíso. 9 entrevistas a inspectores o jefes de UTP.
- C1 coordinación el mismo día (≥30 min del inspector) · C2 curso sin clase o fusionado · C3 pago a reemplazo externo · C4 bolsa de reemplazos ya contratada.

| ENT | Segmento | C1 | C2 | C3 | Caso negativo |
|---|---|---|---|---|---|
| 011, 012, 014, 015, 017 | Particular subvencionado | 3,3,2,3,2 | 2,3,2,2,1 | 0,1,0,1,0 | — |
| 013, 016, 018, 019 | Particular pagado | 1,0,1,0 | 0,0,1,0 | 2,3,2,3 | ENT-016 (C4) |

- Saturación subvencionado: 4 → 1 → 0 códigos nuevos; pagado: solo 4 entrevistas, sin saturar.
- Conclusión: en subvencionados, 5 de 5 inspectores pierden ≥30 min el día de la ausencia (C1≥2); en pagados, 0 de 4 (C1≤1). Son segmentos distintos. H-004 apoyada solo en subvencionados, nivel 3 (EV-030).
- Contradice: ENT-016 tiene bolsa de reemplazos y no siente el problema → posible sustituto.
- Límite: 7 de 9 contactados por un mismo sostenedor; el entrevistador fue docente.

## Ejemplo malo y por qué falla
> "Temas: a todos les preocupan los reemplazos (muy frecuente). Los colegios quieren una plataforma. Conclusión: problema validado."
- Sin libro de códigos ni IDs: nadie puede reconstruir de dónde sale "todos".
- Mezcla segmentos con ciclos de compra y dolores distintos.
- "Quieren una plataforma" es una solución sugerida, no un hallazgo del problema.
- Sin casos negativos ni saturación: "validado" es una declaración, no una conclusión.

## Criterio de aceptación
- Cada código tiene definición e inclusión/exclusión escritas antes del lote.
- Cada conclusión cita IDs que respaldan y que contradicen, con conteo "x de n".
- La saturación se reporta por segmento, no para el total.
- Hay al menos un caso negativo o se declara explícitamente que no apareció.
- Se listan sesgos de reclutamiento y del entrevistador.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
