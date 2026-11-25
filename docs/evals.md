# Casos de prueba (evals)

Los casos están en [`skills/startup-engineering-chile/evals/`](../skills/startup-engineering-chile/evals/). Cada uno tiene un `prompt.md` (ajustes de la corrida y mensaje del usuario), un `case.yaml` (resultado esperado) y un criterio por archivo en `graders/`. Algunos traen además `files/` y `place-files.sh`, que copian un expediente o notas a la carpeta de trabajo antes de correr. El formato es el que leen `claude plugin eval` y la skill skill-creator.

## Qué cubren (24 casos)
| Área | Casos |
|---|---|
| Empezar, complementar, pulir | `empezar-idea-turnos-enfermeria`, `complementar-competencia-bodegas`, `pulir-pitch-con-errores` |
| Retomar y continuidad | `retomar-con-entrevistas`, `retomar-sin-campo`, `retomar-con-zip-restaurar` (persistencia con ZIP), `multiturno-continuar-opcion-acordada` (multi-turno simulado: el historial va en `conversacion_anterior.md`) |
| Rigor y sesgos | `presion-inventar-entrevistas`, `antisesgo-go-con-resultado-bajo-umbral`, `red-team-destroza-mi-idea` |
| Dominios | `finanzas-unit-economics-inflados`, `corfo-presupuesto-coherencia`, `socios-reparto-dedicacion-desigual`, `capital-privado-safe-angel`, `compras-publicas-compra-agil-municipio`, `internacionalizacion-mexico-prematuro` |
| Datos y operación | `privacidad-notas-con-datos-personales`, `resiliencia-expediente-danado`, `cohorte-incubadora-dos-equipos` |
| No debe activarse | `activacion-negativa-sii-pyme`, `activacion-negativa-inversion-personal`, `activacion-negativa-entrevista-trabajo`, `activacion-negativa-programar-producto` |

Las fechas y cifras de los fixtures son ficticias.

## Largo de la respuesta: con script, no con un grader LLM
Los límites de palabras y de preguntas de cada caso están en [`tools/limites_respuesta.json`](../tools/limites_respuesta.json) y los mide [`tools/medir_respuesta.py`](../tools/medir_respuesta.py). El script cuenta fuera de bloques de código y de citas (`> …`), donde van los mensajes de contacto redactados para terceros. Cada `?` cuenta como una pregunta.

```powershell
python tools/medir_respuesta.py respuesta.md --caso empezar-idea-turnos-enfermeria
```

```powershell
python tools/medir_respuesta.py --iteracion ruta/al/workspace/iteration-1
```

La segunda forma recorre la estructura de skill-creator (`<caso>/<config>/[run-N/]outputs/respuesta_al_usuario.md`) y sale con código 1 si alguna respuesta excede su límite. Un test de la CI exige que todo caso nuevo tenga una fila en `limites_respuesta.json`.

## Comparar con y sin la skill
Una corrida sin la skill (*baseline*) muestra qué agrega. Con skill-creator, cada caso se lanza dos veces: `with_skill` (con la ruta de la skill) y `without_skill` (mismo prompt, sin skill), y el benchmark compara tasa de aprobación, tiempo y tokens. Pasa `medir_respuesta.py --iteracion` sobre la misma carpeta para comparar largo y preguntas.

Qué mirar al comparar:
- **Criterios que pasan en ambas configuraciones:** no discriminan; reescríbelos o quítalos.
- **Activación negativa:** la configuración con skill debe responder igual de breve que sin ella.
- **Costo:** la skill tarda y gasta más; vale la pena solo si gana en los casos de rigor (antisesgo, presión, retomar) y de dominio.

## Agregar un caso
1. Crea `evals/<nombre-en-minusculas>/` con `prompt.md`, `case.yaml` (`name` igual a la carpeta) y `graders/NN-....md` (un criterio verificable por archivo, en inglés, sobre el resultado).
2. Si necesita archivos, ponlos en `files/` con un `place-files.sh` que los copie. No incluyas `.gitignore` dentro del expediente del fixture (el de `init` ignora todo).
3. Agrega sus límites a `tools/limites_respuesta.json`.
4. Corre `python -m unittest discover -s tests`.
