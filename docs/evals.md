# Casos de prueba (evals)

Los casos están en [`skills/startup-engineering-chile/evals/`](../skills/startup-engineering-chile/evals/). Cada uno tiene un `prompt.md` (ajustes de la corrida y mensaje del usuario), un `case.yaml` (resultado esperado) y un criterio por archivo en `graders/`. Algunos traen además `place-files.sh`, que arma el expediente o las notas en la carpeta de trabajo antes de correr (ver [Fixtures](#fixtures-sin-copias-del-expediente)). El formato es el que leen `claude plugin eval` y la skill skill-creator.

## Qué cubren (29 casos)
| Área | Casos |
|---|---|
| Empezar, complementar, pulir | `empezar-idea-turnos-enfermeria`, `complementar-competencia-bodegas`, `pulir-pitch-con-errores` |
| Modo Express | `express-consulta-sin-archivos` (duda puntual: respuesta corta y cero archivos) |
| Retomar y continuidad | `retomar-con-entrevistas`, `retomar-sin-campo`, `retomar-con-zip-restaurar` (persistencia con ZIP), `multiturno-continuar-opcion-acordada` (multi-turno simulado: el historial va en `conversacion_anterior.md`) |
| Rigor y sesgos | `presion-inventar-entrevistas`, `antisesgo-go-con-resultado-bajo-umbral`, `red-team-destroza-mi-idea`, `pilot-purgatory-b2b` (pilotos gratis no son PMF), `trampa-presupuesto-corfo` (presión para "pulir" un presupuesto con errores bloqueantes) |
| Dominios | `finanzas-unit-economics-inflados`, `corfo-presupuesto-coherencia`, `socios-reparto-dedicacion-desigual`, `capital-privado-safe-angel`, `compras-publicas-compra-agil-municipio`, `internacionalizacion-mexico-prematuro`, `flip-delaware-prematuro`, `derivacion-sercotec-tradicional` |
| Datos y operación | `privacidad-notas-con-datos-personales`, `compliance-ley-21719`, `resiliencia-expediente-danado`, `cohorte-incubadora-dos-equipos` |
| No debe activarse | `activacion-negativa-sii-pyme`, `activacion-negativa-inversion-personal`, `activacion-negativa-entrevista-trabajo`, `activacion-negativa-programar-producto` |

Las fechas y cifras de los fixtures son ficticias.

## Fixtures sin copias del expediente
El repo no guarda expedientes completos por caso. Cada `place-files.sh` llama a [`tools/armar_fixture.py`](../tools/armar_fixture.py), que lee `fixture.json` y arma la carpeta de trabajo por capas:

| Paso | Clave de `fixture.json` | Qué hace |
|---|---|---|
| 1 | `capas[].base: "demo"` | Copia `examples/expediente_demo/expediente` (siempre el esquema vigente) |
| 1 | `capas[].base: "vacio"` | `00_estado.md` + `manifest.json` + registros con solo encabezado (`proyecto`, `nivel`, `registros`) |
| 1 | `capas[].base: "_bases/<nombre>"` | Expediente compartido por varios casos (hoy `_bases/turnos`, de los dos `retomar-*`) |
| 2 | — | Copia `files/` del caso encima: solo lo que lo distingue (su `00_estado.md`, notas, un CSV con datos) |
| 3 | `eliminar` | Borra rutas para simular daños |
| 4 | `empaquetar` | Arma el ZIP como `expediente.py empaquetar` (`retomar-con-zip-restaurar`) |

`destino` en cada capa permite varios expedientes (la cohorte arma `equipo_a/` desde el demo y `equipo_b/` vacío). Para probar un caso a mano: `mkdir /tmp/x && cd /tmp/x && bash ruta/al/caso/place-files.sh`. Un test de la CI arma todos los fixtures y valida sus expedientes.

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
2. Si necesita archivos, copia el `place-files.sh` de otro caso, describe la base en `fixture.json` y pon en `files/` solo las diferencias. No dupliques el demo ni registros vacíos: los arma el generador. No incluyas `.gitignore` dentro del expediente del fixture (el de `init` ignora todo).
3. Agrega sus límites a `tools/limites_respuesta.json`.
4. Corre `python -m unittest discover -s tests`.
