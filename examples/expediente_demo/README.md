# Expediente de demostración: InspectaYa

> **Proyecto ficticio.** InspectaYa, sus fundadoras, entrevistas, clientes y cifras son inventados para mostrar cómo se ve un expediente con trabajo real. **No sirven como evidencia** para ninguna postulación.

InspectaYa es una startup imaginaria que ayuda a jefes de mantención de plantas medianas a entregar informes de inspección el mismo día. El expediente muestra un proyecto a mitad de camino:

- **G1 Problema en Go:** 8 entrevistas anonimizadas y 2 evidencias.
- **G4 Economía en Hold:** el experimento de precio no alcanzó el umbral fijado antes de salir a terreno.
- **Siguientes pasos:** un piloto en curso, una cuenta en el pipeline y 3 líneas de presupuesto para un fondo con fechas en 2027.

Todo se construyó con los scripts de la skill (`init`, `add`, `doc`, `modelo`, `ingestar`, `informe`, `dashboard`), así que sirve también como prueba de que funcionan juntos.

## Qué mirar

| Archivo | Qué muestra |
|---|---|
| `expediente/00_estado.md` | Perfil (con situación societaria, objetivo de financiamiento y TRL/CRL), ruta por gates, misión de 7 días, números clave y acciones |
| `expediente/registros/*.csv` | Las 8 tablas núcleo (hipótesis, evidencias, entrevistas, experimentos, decisiones, competencia, pipeline, piloto), rendiciones con aporte pecuniario y la bitácora con un riesgo y un KPI (esquema v3) |
| `expediente/documentos/TPL-031_competitive_benchmark.md` | Una plantilla trabajada con el proyecto |
| `expediente/investigacion/notas/ENT-009_anon.md` | Una transcripción pasada por `ingestar.py anonimizar` |
| `expediente/entregables/` | Informe semanal, one-pager, dashboard HTML interactivo y modelo financiero (con la hoja `Fondos_y_moneda`) |

## Pruébalo

Desde la raíz del repositorio (en Windows, usa `py -3` si `python` no funciona):

```bash
S=skills/startup-engineering-chile/scripts
D=examples/expediente_demo

python $S/expediente.py estado   --dir $D      # resumen, misión de 7 días, hipótesis estancadas, acciones vencidas
python $S/expediente.py gate     --dir $D      # chequeos deterministas del gate actual
python $S/expediente.py validar  --dir $D      # columnas, IDs, claves foráneas, fechas, datos personales
python $S/expediente.py informe semanal --dir $D
python $S/dashboard.py --dir $D                # genera entregables/dashboard.html
python $S/fondos_lint.py rendiciones --dir $D --inicio 2027-02-01 --fin 2027-06-30
python $S/fondos_matcher.py --dir $D          # qué fondos calzan con el perfil de 00_estado.md
python $S/auditar.py --dir $D                 # contradicciones, sesgos e integridad (la demo no tiene ALERTAS)
python $S/dataroom.py revisar --dir $D        # qué falta para un data room
python $S/modelo_xlsx.py leer $D/expediente/entregables/modelo_financiero.xlsx --hoja Supuestos
python $S/finanzas.py escenarios --modelo $D/expediente/entregables/modelo_financiero.xlsx
```

Para ver el modo cohorte, arma el fixture del eval de cohorte (`mkdir cohorte && cd cohorte && bash ../skills/startup-engineering-chile/evals/cohorte-incubadora-dos-equipos/place-files.sh`) y corre `python ../$S/cohorte.py --raiz . --html tablero.html --xlsx cohorte.xlsx`.

## Diferencia con un expediente real

En un proyecto real, `expediente init` crea `expediente/.gitignore` para que las entrevistas no se suban a git por accidente. En esta demo se borró ese archivo para poder publicarla.
