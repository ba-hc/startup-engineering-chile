# TPL-059 — Mapa de supuestos (Assumption Map)

> **Para qué sirve:** Ordenar los supuestos por importancia y evidencia para probar primero el que, si es falso, mata el proyecto.
> **Cuándo NO usarla:** Cuando ya conoces el supuesto crítico y tienes listo el experimento para probarlo; volver a mapear solo posterga la prueba.
> **Micro-ejemplo resuelto:** De 12 supuestos de una app de préstamo de herramientas entre vecinos, "los vecinos devuelven la herramienta en buen estado" es crítico y no tiene evidencia; se prueba primero con 20 préstamos en un condominio de Maipú, antes de programar pagos.

**Gate:** G0–G5 · **Alimenta:** `hipotesis.csv`, `experimentos.csv`

## Completar
1. Extrae 8–15 supuestos de tus canvas, al menos uno por dominio: demanda, valor, pago, canal, implementación, técnica, economía.
2. Escríbelos refutables: *"≥X de Y [segmento] hacen/pagan Z en [plazo]"*, no "a los clientes les gustará".
3. Puntúa cada uno:
   - **Importancia 1–5:** ¿se cae el modelo si es falso?
   - **Evidencia 0–4** (escala de la skill): 0 nada · 1 hipótesis · 2 secundaria · 3 primaria parcial · 4 comprobable.
   - **Riesgo = importancia × (4 − evidencia).** Ordena de mayor a menor.

| H-ID | Dominio | Enunciado refutable | Imp. | Evid. | Riesgo | Depende de | Criterio de rechazo | EXP-ID |
|---|---|---|---|---|---|---|---|---|

*Prioriza el de mayor riesgo aunque sea incómodo de probar, no el más fácil.* Si dos empatan, va primero aquel del que dependen otros.

**Cuadrante "probar ya" (imp. ≥4 y evid. ≤1):** [ ] · **Supuesto #1 y su experimento:** [ ]

## Ejemplo bueno (ficticio)
"MateRefuerzo", tutoría en línea de matemáticas para 7° y 8° básico pagada por colegios particulares subvencionados, Región de Valparaíso.

| H-ID | Dominio | Enunciado | Imp. | Evid. | Riesgo | Dep. | Rechazo | EXP |
|---|---|---|---|---|---|---|---|---|
| H-001 | demanda | ≥5 de 10 jefes de UTP reportan una brecha en matemática que su refuerzo actual no cubre | 5 | 3 | 5 | – | <3 de 10 | hecho: 7 de 10 (ENT-001…010) |
| H-002 | pago | ≥2 de 8 sostenedores comprometen ≥$1,5 M por semestre de presupuesto propio | 5 | 0 | 20 | H-001 | 0 de 8 | EXP-001 |
| H-003 | implementación | Los colegios liberan 2 h semanales de sala de computación | 4 | 1 | 12 | – | <50% de colegios | EXP-002 |
| H-004 | valor | Alumnos con ≥10 sesiones suben ≥10 puntos en la prueba diagnóstica | 4 | 2 | 8 | H-003 | <5 puntos | piloto |
| H-005 | técnica | La plataforma funciona con la conexión del colegio | 3 | 3 | 3 | – | caídas >10% de sesiones | – |

**Supuesto #1:** H-002 (riesgo 20). Ofrecer un convenio semestral firmado a 8 sostenedores antes de producir más contenido.

## Ejemplo malo y por qué falla
| Supuesto | Prioridad |
|---|---|
| Los alumnos quieren aprender | Alta |
| La plataforma es escalable | Alta |
| Podemos hacer videos de calidad | Alta |

Priorizado: "videos de calidad", porque el equipo sabe hacerlos.
- Supuestos no refutables y sin criterio de rechazo.
- Todo "Alta": sin escala de importancia ni de evidencia no hay orden posible.
- Falta el supuesto de pago (quién paga y con qué presupuesto), que es el más riesgoso.
- Se elige lo cómodo de probar, no lo riesgoso.

## Criterio de aceptación
- Hay al menos un supuesto de demanda, uno de pago y uno de implementación o técnica.
- Cada supuesto es refutable, tiene criterio de rechazo y está en `hipotesis.csv` con su H-ID.
- Importancia y evidencia están puntuadas y el riesgo se calcula con la misma fórmula para todos.
- El supuesto #1 es el de mayor riesgo (o se justifica por dependencia) y tiene EXP-ID.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
