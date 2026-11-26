# TPL-076 — Hoja de ruta por resultados (Outcome Roadmap)

> **Para qué sirve:** Planificar los próximos 3–6 meses como resultados medibles para el cliente y el negocio, no como una lista de funcionalidades con fechas, conectados a los supuestos más riesgosos.
> **Cuándo NO usarla:** Como compromiso de fechas de entrega ante un cliente o un fondo (para eso está el Gantt, TPL-106), ni antes de tener un problema validado: sin G1, el roadmap planifica construir lo que nadie pidió.
> **Micro-ejemplo resuelto:** En vez de "T2: app móvil; T3: reportes", dice "Ahora: bajar el cierre de una inspección de 3,1 a 1 día (KPI-002); Siguiente: 60% de los inspectores usa la app sin ayuda; Después: integrar 2 aseguradoras", y la app móvil es solo una de las apuestas para lo primero.

**Gate:** G5 (–G8) · **Alimenta:** `hipotesis.csv`, `experimentos.csv`, `bitacora.csv` (tipo kpi)

## Completar
**Objetivo de negocio del período:** [p. ej. pasar a G7 con 10 clientes pagando] · **Métrica principal:** [KPI-ID] · **Horizonte:** [ ] · **Última revisión:** [fecha y gate]

| Horizonte | Resultado (comportamiento o métrica que cambia) | KPI-ID: baseline → meta | Supuesto que lo sostiene (H-) | Apuestas (opciones de solución) | Cómo sabremos (EXP-) | Estado |
|---|---|---|---|---|---|---|
| Ahora (0–6 semanas) | | | | | | |
| Siguiente (6–12 semanas) | | | | | | |
| Después (3–6 meses) | | | | | | |
| Fuera por ahora | [qué no se hará] | — | — | — | [por qué] | |

*Solo "Ahora" lleva compromisos de fecha. Las funcionalidades son apuestas para mover un resultado; si el experimento no lo mueve, se cambia la apuesta, no la meta.*
*Revisa el roadmap cuando cambia un supuesto o se cierra un gate.*

## Ejemplo bueno (ficticio)
BodegaClara SpA: control de inventario para ferreterías medianas. Objetivo: G7 con 10 ferreterías pagando a 2027-09-30.
| Horizonte | Resultado | KPI | Supuesto | Apuestas | Prueba | Estado |
|---|---|---|---|---|---|---|
| Ahora | El inventario cuadra al cierre de mes | KPI-004: diferencia 6,5% → ≤ 2% | H-011: el error nace en recepciones sin registrar | escaneo en recepción; alerta de guía sin ingresar | EXP-015 en 3 ferreterías | en curso |
| Siguiente | El dueño revisa la reposición sugerida cada semana | KPI-005: 0 → 70% de las semanas | H-012: confía en la sugerencia si ve el porqué | resumen semanal por WhatsApp; vista de quiebres | EXP-016 | — |
| Después | Venta a través de distribuidores | 2 distribuidores con 5 ferreterías c/u | H-014 | programa de socios | — | — |
| Fuera por ahora | App para clientes finales y tienda en línea | — | — | — | no aporta al objetivo de G7 | — |

## Ejemplo malo y por qué falla
> T1: login con redes sociales y panel nuevo. T2: app iOS y Android. T3: IA predictiva. T4: expansión a Perú. Todo con fecha comprometida.
- Es una lista de funcionalidades, sin resultado ni KPI.
- Fechas comprometidas a 12 meses sin evidencia de que alguna funcionalidad resuelva algo.
- Sin "fuera por ahora", todo cabe y nada se prioriza.

## Criterio de aceptación
- Cada fila de "Ahora" y "Siguiente" tiene KPI con baseline y meta, supuesto (H-) y experimento (EXP-).
- Las funcionalidades aparecen como apuestas, no como objetivos.
- Hay una lista explícita de lo que queda fuera y por qué.
- Se revisó en el último cambio de gate.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
