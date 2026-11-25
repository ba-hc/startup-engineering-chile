# Ciclo de trabajo de un bloque (módulo) y cierre de gate

1. **Elige el módulo** con `references/mapa_modulos.md` y lee su archivo en `references/manual/` (propósito, procedimiento, entregables, criterio de salida, errores). Ignora la sección "Ejercicio aplicado": es para cursos.
2. **Reúne insumos**: expediente, lo que sabe el usuario y, si sirve, investigación web (`references/investigacion_web.md`).
3. **Crea la plantilla** si aporta: `expediente.py doc TPL-0XX --dir <carpeta>`. Prefiere las troncales (`expediente.py plantillas --troncales`). Pre-rellena, marca "por confirmar" lo inferido y cita evidencia/supuesto/fuente en cada fila.
4. **Contrasta** con el criterio de salida y los "Errores y alertas" del módulo. Si no se cumple, lo que falta suele ser trabajo de campo, no más documentos.
5. **Registra con el script**, no escribiendo CSV a mano: `expediente.py add <registro> campo=valor …` (ID, fecha y estado automáticos; valida columnas, fechas AAAA-MM-DD y campos obligatorios: un experimento necesita `hypothesis_id`, `metrica` y `umbral`; una evidencia, `afirmacion` y `fuente_url_o_ruta`). Para mostrar: `expediente.py ver <registro>`. Para Excel en español: `expediente.py exportar`. Esquemas y fórmulas: `references/formulas_y_registros.md`.
6. **Calcula con scripts** cuando haya números (`references/flujos/finanzas.md`).
7. **Decide** (`add decisiones gate=G… decision=Go|Hold|Recycle|Kill justificacion=…`) cuando el usuario haya confirmado los hechos base.
8. **Actualiza `00_estado.md`** (Ruta, Foco, Próximas acciones, bitácora).

No hace falta completar todas las plantillas: elige las que resuelven la incertidumbre actual. Ritmo semanal orientativo: `references/operacion/01_plan_90_dias.md`.

## Plantillas troncales (25)
Oportunidad y problema: TPL-001, 005 · Cliente: 014 (guion), 015 (snapshot), 016 (codificación), 020 (ICP) · Mercado: 030 (TAM/SAM/SOM), 031 (benchmark) · Estrategia: 036 (pérdida aceptable) · Negocio: 048 (Lean Canvas), 049 (VPC), 054 (pricing) · Validación: 059 (supuestos), 061 (experimento), 067/068 (piloto) · Ventas: 083 (pipeline) · Finanzas: 087 (unit economics), 088 (caja) · Operación: 095 (pre-mortem y criterios de kill) · Fondos: 103–106, 108.

Las otras 83 son variantes o profundizaciones (otros canvas, mapas, scorecards): úsalas solo si el usuario las pide o si una troncal no alcanza.
