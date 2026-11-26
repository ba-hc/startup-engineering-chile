# TPL-078 — Pirámide y encuesta de ajuste producto-mercado (PMF Pyramid)

> **Para qué sirve:** Revisar de abajo hacia arriba (cliente, necesidad, propuesta, funcionalidades, experiencia) dónde está roto el ajuste producto-mercado y medirlo con retención y con la pregunta "¿qué tan decepcionado estarías si ya no pudieras usarlo?".
> **Cuándo NO usarla:** Con menos de ~30–40 usuarios activos del segmento, o con personas que no han usado el producto de verdad; tampoco para declarar PMF sin retención: la encuesta complementa las cohortes (TPL-080), no las reemplaza.
> **Micro-ejemplo resuelto:** De 52 usuarios activos, 19 (37%) estarían "muy decepcionados", bajo el 40% de referencia; entre clínicas de 2–5 boxes son 13 de 24 (54%), así que el foco se concentra en ese segmento en vez de mejorar la interfaz para todos.

**Gate:** G7–G8 · **Alimenta:** `evidencias.csv`, `bitacora.csv` (tipo kpi y cohorte), `decisiones.csv`

## Completar
### 1. Pirámide (de abajo hacia arriba; no subas si el nivel de abajo está roto)
| Nivel | Pregunta | Evidencia (ID) | Estado [sólido / débil / roto] |
|---|---|---|---|
| 1. Cliente objetivo | ¿Segmento definido (TPL-020) y los que retienen son de él? | | |
| 2. Necesidad no resuelta | ¿Dolor confirmado en G1 para ese segmento? | | |
| 3. Propuesta de valor | ¿Por qué nos eligen frente a la alternativa (TPL-033)? | | |
| 4. Funcionalidades | ¿El conjunto mínimo resuelve la necesidad? | | |
| 5. Experiencia | ¿Lo usan sin ayuda? | | |

### 2. Encuesta de ajuste
**Muestra:** usuarios activos según definición previa [p. ej. ≥ 2 usos en las últimas 2 semanas] · N = [ ] · canal y fecha [ ]
1. ¿Qué tan decepcionado estarías si ya no pudieras usar [producto]? (muy / algo / nada / ya no lo uso)
2. ¿Qué tipo de persona crees que se beneficiaría más?
3. ¿Cuál es el principal beneficio que obtienes?
4. ¿Cómo podríamos mejorarlo?

| Segmento | N | "Muy decepcionados" | % |
|---|---|---|---|

*El 40% es una referencia de la industria, no una ley. Con N < 40, reporta conteos y no saques conclusiones del porcentaje.*

### 3. Retención (de TPL-080)
¿La curva se aplana? [mes y %] · retención neta de ingresos [ ] · ¿coincide el segmento que retiene con el que responde "muy"? [ ]

## Ejemplo bueno (ficticio)
CuidaTurno SpA: coordinación de turnos de cuidadoras para residencias de adultos mayores.
- Pirámide: 1 sólido (residencias de 20–60 camas, EV-150); 2 sólido (3,2 turnos sin cubrir por semana; 9 de 11 entrevistas); 3 débil (dicen elegir por precio); 4 sólido; 5 roto en residencias pequeñas (piden ayuda telefónica).
- Encuesta (2027-08, N = 64): total 26 "muy" (41%); 20–60 camas: 21 de 38 (55%); < 20 camas: 5 de 26 (19%).
- Cohortes: las de 20–60 camas se aplanan en 82% desde el mes 4; las de < 20 camas siguen cayendo (54% al mes 6).
- Decisión (DEC-040): foco en 20–60 camas, dejar de captar < 20 camas y entrevistar a 8 clientes sobre por qué nos eligen (nivel 3).

## Ejemplo malo y por qué falla
> Encuestamos a 300 personas de nuestra lista de correo (la mayoría nunca usó el producto): 45% estaría muy decepcionado. ¡Tenemos PMF! Ahora hay que mejorar la interfaz.
- La muestra no son usuarios activos: mide simpatía, no dependencia.
- Declara PMF sin mirar retención por cohorte.
- Salta al nivel 5 sin revisar si los niveles de abajo están sólidos.

## Criterio de aceptación
- Cada nivel de la pirámide tiene evidencia y estado; se trabaja el nivel roto más bajo.
- La encuesta usa solo usuarios activos según una definición previa, con N y conteos por segmento.
- La conclusión combina encuesta y retención por cohorte (TPL-080).
- La decisión de foco está en `decisiones.csv`.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
