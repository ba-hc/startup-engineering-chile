# Expediente de demostración: InspectaYa

> **Proyecto ficticio.** InspectaYa, sus fundadoras, entrevistas, clientes y cifras son inventados para mostrar cómo se ve un expediente con trabajo real. **No sirven como evidencia** para ninguna postulación.

InspectaYa es una startup imaginaria que ayuda a jefes de mantención de plantas medianas a entregar informes de inspección el mismo día. El expediente muestra un proyecto a mitad de camino:

- **G1 Problema en Go:** 8 entrevistas anonimizadas y 2 evidencias.
- **G4 Economía en Hold:** el experimento de precio no alcanzó el umbral fijado antes de salir a terreno.
- **Siguientes pasos:** un piloto en curso, una cuenta en el pipeline y 3 líneas de presupuesto para un fondo con fechas en 2027.

Todo se construyó con los scripts de la skill (`init`, `add`, `doc`, `modelo`, `ingesta`, `informe`, `dashboard`), así que sirve también como prueba de que funcionan juntos.

## Qué mirar

| Archivo | Qué muestra |
|---|---|
| `expediente/00_estado.md` | Perfil, ruta por gates, foco, acciones y bitácora |
| `expediente/registros/*.csv` | Hipótesis, entrevistas, experimentos, decisiones, competencia, pipeline, piloto, riesgos, KPI y rendiciones |
| `expediente/documentos/TPL-031_competitive_benchmark.md` | Una plantilla trabajada con el proyecto |
| `expediente/investigacion/notas/ENT-009_anon.md` | Una transcripción pasada por `ingesta.py anonimizar` |
| `expediente/entregables/` | Informe semanal, one-pager, dashboard HTML y modelo financiero |

## Pruébalo

Desde la raíz del repositorio (en Windows, usa `py -3` si `python` no funciona):

```bash
S=skills/startup-engineering-chile/scripts
D=examples/expediente_demo

python $S/expediente.py estado   --dir $D      # resumen, hipótesis estancadas, acciones vencidas
python $S/expediente.py validar  --dir $D      # columnas, IDs, claves foráneas, fechas, datos personales
python $S/expediente.py informe semanal --dir $D
python $S/dashboard.py --dir $D                # genera entregables/dashboard.html
python $S/fondos_lint.py rendiciones --dir $D --inicio 2027-02-01 --fin 2027-06-30
python $S/modelo_xlsx.py leer $D/expediente/entregables/modelo_financiero.xlsx --hoja Supuestos
python $S/finanzas.py escenarios --modelo $D/expediente/entregables/modelo_financiero.xlsx
```

Para ver el modo cohorte, copia la carpeta dos veces dentro de otra (por ejemplo `cohorte/equipo-a` y `cohorte/equipo-b`) y corre `python $S/cohorte.py --raiz cohorte --html cohorte/tablero.html`.

## Diferencia con un expediente real

En un proyecto real, `expediente init` crea `expediente/.gitignore` para que las entrevistas no se suban a git por accidente. En esta demo se borró ese archivo para poder publicarla.
