<div align="center">

# 🚀 Startup Engineering Chile

**Un mentor de startups para Claude: de la idea al negocio, con evidencia.**

Te acompaña sesión a sesión a validar tu idea, entrevistar clientes, analizar la competencia, definir precio, hacer los números y preparar tu postulación a CORFO, ANID o Start-Up Chile, dejando todo registrado en la carpeta de tu proyecto.

[![CI](https://github.com/ba-hc/startup-engineering-chile/actions/workflows/ci.yml/badge.svg)](https://github.com/ba-hc/startup-engineering-chile/actions/workflows/ci.yml)
[![Versión](https://img.shields.io/github/v/release/ba-hc/startup-engineering-chile?label=versión)](CHANGELOG.md)
[![Licencia: MIT](https://img.shields.io/badge/código-MIT-blue.svg)](LICENSE)
[![Licencia: CC BY 4.0](https://img.shields.io/badge/contenido-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENIDO.md)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-D97757.svg)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-3776AB.svg)](https://www.python.org/)

[Instalación](#-instalación) · [Cómo se usa](#-cómo-se-usa) · [Herramientas](#-herramientas) · [Demo](#-pruébalo-con-la-demo) · [Incubadoras](#-para-incubadoras-y-cursos) · [Privacidad](#-privacidad) · [Novedades](#-novedades-en-11)

</div>

---

## ¿Qué es?

Una **skill** (habilidad) para [Claude](https://claude.ai) basada en el pack *Startup Engineering Chile & LATAM 2026*. Incluye:

- 28 módulos de manual, 25 plantillas completas con ejemplos buenos y malos (y 83 más en el catálogo), umbrales por etapa y 17 registros;
- una guía de postulación a CORFO, una biblioteca de fuentes, casos y un plan de 90 días;
- scripts en Python para los cálculos y revisiones que no conviene dejar a la memoria del modelo.

Claude no te entrega el pack de golpe. Lo aplica a **tu** proyecto: conversa contigo, te hace las preguntas correctas, investiga en la web y lleva un **expediente de evidencia** que crece en cada sesión.

> **La unidad de trabajo es una decisión basada en evidencia, no un canvas completado.**

## ✨ Qué hace

| Modo | Para quién | Ejemplo |
|---|---|---|
| 🌱 **Empezar** | Tienes una idea y no sabes por dónde partir | *"Trabajé 6 años como enfermera y armar los turnos es un caos. Quiero hacer una app."* |
| 🔧 **Pulir** | Ya tienes algo en marcha: pitch, clientes, MVP o una postulación | *"Te dejo mi one-pager, quiero postular a Semilla Inicia."* |
| 🧩 **Complementar** | Necesitas una pieza puntual | *"Hazme un análisis de competencia para mi software de inventario."* |

Además:

- 🔁 **Retoma donde quedaron.** Lee el expediente, te pregunta por lo pendiente y analiza lo que traes (por ejemplo, notas de entrevistas) contra el criterio que fijaron *antes* de salir a terreno.
- 🧭 **Te ubica en una ruta de 10 etapas** (G0 Oportunidad → G9 Escala), con nivel de evidencia de 0 a 4 en cada una.
- 🧮 **Hace los números con scripts, no de memoria:** unit economics, runway, escenarios, dilución con SAFE (cap y descuento), reparto en una venta (preferencia de liquidación), costo de contratar en Chile y conversión CLP/UF/USD.
- 💸 **Más allá de validar:** capital privado (ángeles, SAFE, term sheet), venta a grandes empresas, caja y cobro, spin-offs universitarias, salud y otras verticales reguladas, productos con IA, sumarse a una startup ajena, y pivotar o cerrar con orden.
- 🔍 **Audita tu expediente:** detecta un Go sin evidencia, resultados bajo la meta, entrevistas complacientes, costo hundido y precios que no calzan con el pipeline.
- 🏛️ **Revisa tu postulación a fondos:** elegibilidad por instrumento, gastos no financiables, coherencia entre presupuesto y marco lógico, y límites de caracteres. Antes de afirmar un requisito, lo verifica en la fuente oficial.
- 🧪 **Pone a prueba tu propuesta** con un *red team* de tres evaluadores (CORFO, comprador B2B e inversionista) y una compuerta antisesgo antes de cada decisión.
- 🔎 **Investiga la competencia** y guarda cada página con URL y fecha, separando lo que dice el sitio de lo que está verificado.
- 🛑 **Es honesto:** no inventa entrevistas ni clientes, no baja la meta después de ver los datos y te dice cuándo conviene no construir todavía.

## 🧠 Cómo trabaja

```mermaid
flowchart LR
    A[Reflejar el problema<br/>sin nombrar la solución] --> B[Confirmar<br/>con el fundador]
    B --> C[Fijar el criterio<br/>antes de salir]
    C --> D[Trabajo de campo<br/>entrevistas, pilotos]
    D --> E{Decidir}
    E -->|Go| F[Siguiente etapa]
    E -->|Hold / Recycle| C
    E -->|Kill| G[Aprender y cerrar]
```

**Primer turno liviano** (~300 palabras): un espejo de tu problema para que lo corrijas, el hallazgo más importante, en qué etapa estás, máximo 3 preguntas y el próximo paso. El análisis completo queda en archivos, no en el chat.

**Tres niveles de profundidad**, según cuánto tiempo tengas:

| Nivel | Cuándo | Qué deja |
|---|---|---|
| **Consulta** | Una pregunta puntual (*"¿califico a Semilla Inicia?"*) | La respuesta; no crea expediente, solo lo ofrece |
| **Sprint** | Preparar algo concreto en días: una reunión, un pitch, una prueba de precio | Estado, hipótesis y evidencias |
| **Completo** | Validar en serio, postular a fondos, levantar inversión | Expediente que suma registros a medida que se usan (hasta 17) |

Si no lo dices, empieza liviano y sube de nivel cuando haga falta.

**Modo degradado.** Si no hay terminal ni Python (por ejemplo, Claude.ai sin ejecución de código), la skill trabaja igual:

- entrega plantillas y registros como bloques para copiar;
- hace los cálculos mostrando la fórmula;
- te avisa que no quedó guardado y te deja un resumen para pegar la próxima vez.

**Sin memoria entre conversaciones** (Claude.ai): al cerrar, la skill empaqueta el expediente en un ZIP para que lo descargues; la próxima vez lo subes y sigue donde quedaron (`expediente.py empaquetar` / `restaurar`). Para cambiar de conversación sin ZIP, `expediente.py resumen` da un estado de ~600 tokens.

Si no hay internet, usa las referencias incluidas con su fecha de corte y te lo dice.

<details>
<summary><b>Ver un ejemplo de primera respuesta</b></summary>

> ¡Hola! Seis años viendo el problema desde adentro es un muy buen punto de partida. Te cuento lo que entendí. Corrígeme si no es así:
>
> **Las supervisoras de enfermería necesitan que cada turno tenga a su gente, y hoy se les van unos 2 días al mes armando la programación en Excel.**
>
> **Lo más importante que encontré:** en Chile ya hay soluciones para esto (rFlex, Buk, Shifter). Esto no mata la idea, pero cambia la pregunta: hay que entender por qué tu clínica, y seguramente otras, siguen con Excel y WhatsApp.
>
> **Dónde estás hoy:** G0, una idea con una señal fuerte, sin evidencia todavía de otras clínicas ni de quién pagaría. Te sugiero que tu amigo no empiece a programar aún.
>
> 1. ¿En tu clínica alguien evaluó alguna vez un software de turnos?
> 2. ¿Quién habría tenido que aprobar la compra: la jefatura, RR.HH. o la gerencia?
> 3. ¿A cuántas supervisoras de otras clínicas les podrías escribir esta semana?
>
> **Próximo paso:** te preparo un guion para ~6 conversaciones y fijamos antes qué resultado nos diría que vale la pena seguir.

*Extracto resumido de una de las pruebas.*
</details>

## 📦 Instalación

### Opción A — Claude Code, como plugin (recomendada)

Dentro de Claude Code, escribe:

```
/plugin marketplace add ba-hc/startup-engineering-chile
/plugin install startup-engineering-chile@startup-engineering-chile
```

Confirma la instalación en el panel que se abre y reinicia Claude Code si te lo pide.

Desde la terminal también funciona:

```bash
claude plugin marketplace add ba-hc/startup-engineering-chile
claude plugin install startup-engineering-chile@startup-engineering-chile
```

**Actualizar:** `/plugin marketplace update startup-engineering-chile` y luego `claude plugin update startup-engineering-chile@startup-engineering-chile`. También puedes activar la actualización automática en `/plugin` → Marketplaces.

### Opción B — Claude Code, copia manual

**macOS / Linux**
```bash
git clone https://github.com/ba-hc/startup-engineering-chile.git
mkdir -p ~/.claude/skills
cp -r startup-engineering-chile/skills/startup-engineering-chile ~/.claude/skills/
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/ba-hc/startup-engineering-chile.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse startup-engineering-chile\skills\startup-engineering-chile "$env:USERPROFILE\.claude\skills\"
```

Si prefieres que la skill sea solo de un proyecto, cópiala en `.claude/skills/` dentro de esa carpeta.

### Opción C — Claude.ai o Claude Desktop

1. Descarga `startup-engineering-chile.zip` desde [Releases](https://github.com/ba-hc/startup-engineering-chile/releases/latest) (no lo descomprimas).
2. En **Configuración → Capacidades**, activa **Ejecución de código y creación de archivos**. En planes Team o Enterprise lo habilita quien administra la organización.
3. Ve a **Personalizar → Skills**, toca **+** → **Crear skill** → **Subir una skill** y elige el ZIP.
4. Verifica que la skill quede activada en la lista.

> Los menús de Claude cambian con el tiempo; si no ves la opción, revisa la [ayuda oficial de Skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Requisitos

- **Python 3.8 o superior** para los scripts (solo biblioteca estándar; no hay que instalar paquetes). En Windows, si `python` no funciona, la skill usa `py -3`.
- **Opcional:** acceso a internet para actualizar UF, UTM y dólar desde [mindicador.cl](https://mindicador.cl). Sin conexión se usan los valores de respaldo con su fecha.

### ¿Quedó instalada?

Abre Claude en la carpeta de tu proyecto y escribe *"tengo una idea para una startup y no sé por dónde partir"*. Si responde reflejando tu problema y ubicándote en una etapa (G0, G1…), está funcionando. Para revisar el entorno, pídele *"corre el doctor del expediente"*.

## 💬 Cómo se usa

No necesitas comandos especiales: habla de tu emprendimiento y la skill se activa sola. Algunas ideas para partir:

```text
Tengo una idea para una app de [problema]. ¿Por dónde parto?
Te dejo mi pitch en pitch.md. ¿Qué le falta para postular a Semilla Expande?
Necesito un análisis de competencia para [producto] en Chile.
Hice 5 entrevistas, te dejo las transcripciones. ¿Cómo lo ves?
¿Cuánto me cuesta contratar a un desarrollador con $1.800.000 líquidos?
Revisa mi presupuesto CORFO antes de enviarlo.
Mi socio quiere el 50%. ¿Cómo armamos el vesting?
Un ángel me ofrece un SAFE con cap de USD 2 millones. ¿Cuánto me diluyo?
Me ofrecieron opciones en una startup. ¿Cómo evalúo la oferta?
Llevamos un año y no despega. ¿Pivoteamos o cerramos?
¿Dónde estoy? Muéstrame mi ruta.
```

### El expediente

Todo queda en una carpeta `expediente/` dentro de tu proyecto, para retomar en la próxima sesión:

```text
expediente/
├── 00_estado.md          perfil, ruta por etapas, foco, trabajo de campo, acciones, bitácora
├── manifest.json         versión del esquema, nivel (sprint o completo) y tipo de startup
├── registros/*.csv       hipótesis, evidencias, decisiones, entrevistas, competencia…
├── documentos/TPL-*.md   plantillas trabajadas con tu proyecto
├── investigacion/        páginas guardadas con URL y fecha; notas de entrevistas anonimizadas
├── entregables/          informes, one-pager, dashboard, modelo financiero, exportaciones
└── .gitignore            evita subir entrevistas a git por accidente
```

Los CSV se abren en Excel. `expediente.py exportar` genera versiones con `;` y BOM, listas para Excel en español. Si vienes de la versión 1.0, la skill corre `expediente.py migrar` y actualiza tu expediente sin perder datos.

## 🧰 Herramientas

Claude las ejecuta por ti; también puedes usarlas directamente desde la terminal. Están en `skills/startup-engineering-chile/scripts/`.

| Script | Para qué |
|---|---|
| `expediente.py` | Crear, revisar (`doctor`, `estado`, `validar`), migrar y consultar el expediente; umbrales por etapa; búsqueda sin internet en el manual y las plantillas; informes (semanal, one-pager, deck en Markdown); resumen, empaquetar y restaurar para seguir en otra conversación |
| `finanzas.py` | Unit economics, punto de equilibrio, runway, escenarios desde el modelo, dilución (SAFE con cap y descuento, pool), reparto en una venta, costo empleado y boletas de honorarios |
| `auditar.py` | Contradicciones y sesgos del expediente: decisiones sin evidencia, metas no cumplidas, entrevistas complacientes, costo hundido |
| `indicadores_cl.py` | UF, UTM, dólar y euro del día, con caché; conversión entre CLP, UF y USD |
| `modelo_xlsx.py` | Leer y cambiar los supuestos del modelo financiero sin romper sus fórmulas |
| `fondos_lint.py` | Elegibilidad por instrumento, gastos no financiables, rendiciones, coherencia con el marco lógico y límites de caracteres |
| `ingesta.py` | Anonimizar transcripciones de entrevistas (.txt, .vtt, .srt) antes de guardarlas |
| `dashboard.py` | Tablero HTML del proyecto en un solo archivo, sin servidor |
| `cohorte.py` | Tablero de varios equipos para incubadoras y cursos |
| `firecrawl.py` | Opcional: archiva páginas si ya tienes Firecrawl corriendo |

Las cifras chilenas (tasas, topes, tramos de impuesto, UF de respaldo) y las reglas de cada fondo viven en archivos JSON con su fecha de verificación: `assets/parametros_cl.json`, `assets/fondos/instrumentos.json` y `assets/umbrales_gates.json`. `expediente.py doctor` avisa si alguna fecha venció.

## 🎬 Pruébalo con la demo

[`examples/expediente_demo/`](examples/expediente_demo/) contiene el expediente de **InspectaYa**, una startup ficticia a mitad de camino: entrevistas anonimizadas, un experimento de precio que no alcanzó la meta, un piloto, un presupuesto para un fondo y el dashboard generado. Sirve para ver cómo se ve un expediente real antes de empezar el tuyo. Los comandos para explorarlo están en su README.

## 🏫 Para incubadoras y cursos

Si acompañas a varios equipos, cada uno trabaja con su expediente y tú ves el conjunto:

```bash
python skills/startup-engineering-chile/scripts/cohorte.py --raiz cohorte-2027 --html cohorte-2027/tablero.html
```

El tablero muestra, por equipo:

- gate, entrevistas, evidencia confirmada y última decisión;
- días sin actividad;
- alertas: sin terreno, inactivo, acciones vencidas, hipótesis estancadas, fondo sin verificar.

Al final resume los bloqueos que se repiten en la generación, para decidir qué taller dar. Guía de uso: [`references/flujos/cohorte.md`](skills/startup-engineering-chile/references/flujos/cohorte.md).

## 🔒 Privacidad

El expediente guarda entrevistas, y eso son datos personales. Por defecto, la skill:

- **anonimiza:** usa ENT-001, rol y segmento; nunca nombre, correo, teléfono ni RUT;
- **avisa** si una fila parece contener esos datos;
- crea un `.gitignore` dentro del expediente;
- **pide permiso** antes de enviar información a servicios externos.

Hoy rige la Ley 19.628; la **Ley 21.719** de protección de datos entra en vigencia el **15 de octubre de 2027**. La skill trabaja desde ya con sus estándares de consentimiento. Detalle: [`references/flujos/privacidad.md`](skills/startup-engineering-chile/references/flujos/privacidad.md).

## 📚 Qué incluye

| Recurso | Cantidad | Dónde |
|---|---|---|
| Módulos del manual (oportunidad, problema, mercado, propuesta, pricing, pilotos, ventas, fondos…) | 28 | `references/manual/` |
| Flujos de trabajo (retomar, finanzas, fondos, capital privado, venta corporativa, caja, pivote y cierre, verticales reguladas…) | 20 | `references/flujos/` |
| Plantillas completas, con ejemplo bueno y malo | 25 | `assets/plantillas/` |
| Plantillas de catálogo (se generan como esqueleto con su criterio) | 83 | `assets/plantillas/catalogo_plantillas.csv` |
| Umbrales por etapa y tipo de startup (SaaS B2B, B2C, marketplace, deeptech, hardware, servicios) | 10 etapas × 6 | `assets/umbrales_gates.json` |
| Registros CSV (hipótesis, evidencias, experimentos, decisiones, competencia, pipeline…) | 17 | `assets/registros/` |
| Guía CORFO: elegir instrumento, admisibilidad, presupuesto, rendición, red team | 3 guías | `references/corfo/` |
| Fuentes con URL y estado de verificación | 268 | `references/biblioteca/` |
| Plan de 90 días, 20 workshops, currículo y mentoría | — | `references/operacion/` |
| Casos y ejemplo integral (datos pedagógicos) | — | `references/casos/` |
| Modelo financiero editable | 1 | `assets/modelo_financiero.xlsx` |
| Scripts | 10 | `scripts/` |

## 🔎 Investigación web

La skill usa la búsqueda web que tenga tu cliente de Claude y guarda cada página relevante con URL y fecha en `investigacion/`. Si ya tienes [Firecrawl](https://github.com/firecrawl/firecrawl) corriendo en tu máquina, también puede usarlo para archivar páginas; no hace falta instalarlo. Guía para quien lo quiera: [`references/firecrawl.md`](skills/startup-engineering-chile/references/firecrawl.md).

## 🧪 Resultados de las pruebas

La skill se probó con 6 casos realistas, comparando la misma tarea con y sin la skill (versión 1.0; última ronda, ambas con Claude Sonnet):

| Caso | Con skill | Sin skill |
|---|:---:|:---:|
| Empezar desde una idea | 6/8 | 1/8 |
| Pulir un one-pager para CORFO | 7/7 | 2/7 |
| Análisis de competencia | 6/7 | 4/7 |
| Retomar con entrevistas hechas | 8/8 | 6/8 |
| Retomar sin haber hecho el trabajo de campo | 7/7 | 2/7 |
| Presión para inventar entrevistas | 6/6 | 6/6 |
| **Total** | **94 %** | **50 %** |

Qué cambia en la práctica:

- **Sin la skill**, el modelo tiende a diseñar la app aunque no se haya validado el problema. Tampoco deja registro para retomar, y ante la admisibilidad a fondos responde dudando en vez de verificarla.
- **Con la skill**, las respuestas son más cortas y el detalle queda en archivos.

Desde entonces la batería creció a **24 casos**: socios, capital privado, compras públicas, internacionalización, red team, antisesgo, privacidad, cohorte, persistencia con ZIP, un caso multi-turno y 4 preguntas que **no** deben activar la skill. El largo de cada respuesta (palabras y preguntas) lo mide un script, no un evaluador LLM. Los casos nuevos todavía no tienen una ronda comparativa publicada. Cómo correrlos, con y sin la skill: [`docs/evals.md`](docs/evals.md).

### Tests de los scripts

```bash
python tools/check_refs.py                 # rutas citadas, nombres de archivo, catálogos, versión
python tools/validar_datos.py              # JSON de datos contra sus esquemas
python -m unittest discover -s tests -v    # cálculos, validación, anonimización, xlsx, evals
```

La [CI](.github/workflows/ci.yml) los corre en Ubuntu y Windows con Python 3.8 y 3.12, y además valida la demo y pasa `ruff`. Un [workflow semanal](.github/workflows/mantencion.yml) revisa los enlaces de la biblioteca y la antigüedad de los datos, y abre un issue si algo venció o se rompió.

## ⚠️ Límites

- **Fechas de corte.** Montos, plazos, tasas y requisitos de fondos están al **25-11-2026** y cambian en cada llamado. La skill los verifica en la fuente oficial, pero confirma siempre con las bases vigentes.
- **Indicadores.** UF, UTM y dólar vienen de mindicador.cl, un servicio comunitario que puede fallar. En ese caso se usan valores de respaldo y la skill te dice de qué fecha son.
- **Orientación educativa.** Lo legal, tributario, laboral, clínico y de inversión no reemplaza a un profesional.
- **No afiliado** a CORFO, ANID, Start-Up Chile, mindicador.cl ni Firecrawl.
- Los casos y ejemplos del pack, y la demo, usan **datos ficticios o pedagógicos**: no sirven como evidencia para una postulación.

## 🗂️ Estructura del repositorio

```text
.
├── .claude-plugin/           manifiestos para instalar como plugin de Claude Code
├── .github/workflows/        CI (referencias, datos, tests, demo, ruff) y mantención semanal
├── skills/
│   └── startup-engineering-chile/
│       ├── SKILL.md          instrucciones del mentor (enrutador)
│       ├── references/       manual, flujos, guía CORFO, biblioteca, casos, operación
│       ├── assets/           plantillas, registros CSV, modelo financiero, parámetros y fondos
│       ├── scripts/          10 scripts en Python (biblioteca estándar)
│       └── evals/            casos de prueba
├── examples/expediente_demo/ expediente ficticio de ejemplo
├── tests/                    tests de los scripts
├── tools/                    consistencia, esquemas de datos, enlaces, vigencia y medición de evals
├── docs/                     evals y proceso de construcción del pack (no van en la skill)
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE                   MIT (código)
└── LICENSE-CONTENIDO.md      CC BY 4.0 (contenido)
```

## 🆕 Novedades en 1.2

- **Plantillas podadas:** 25 completas, cada una con un ejemplo bueno, uno malo y su criterio de aceptación; las demás se generan como esqueleto. El manual perdió el texto repetido (−30 %).
- **Umbrales por etapa y tipo de startup**, y ejemplos de decisiones bien y mal tomadas.
- **8 flujos nuevos:** capital privado, sumarse a una startup, pivote y cierre, venta corporativa, caja y cobro, spin-offs universitarias, verticales reguladas y MVP con IA.
- **Continuidad fuera de Claude Code:** `empaquetar`, `restaurar` y `resumen`.
- **Scripts:** `auditar.py`, búsqueda BM25 sin internet, deck en Markdown, SAFE con descuento y reparto en una venta (waterfall).
- **Mantenimiento:** esquemas para los JSON de datos, revisión semanal de enlaces y fechas, y fecha de verificación leída de los datos (no escrita a mano).
- **Evals:** 24 casos y medición de largo por script.

Detalle completo en el [CHANGELOG](CHANGELOG.md).

## 🤝 Contribuir

¿Encontraste un requisito de fondo desactualizado, una fuente rota o un caso que la skill no maneja bien? Abre un [issue](https://github.com/ba-hc/startup-engineering-chile/issues) o un pull request.

Antes de enviar cambios, lee [CONTRIBUTING.md](CONTRIBUTING.md): cómo actualizar una cifra o una regla de fondo con su fuente y fecha, cómo agregar un flujo o un caso de prueba, y qué revisa la CI.

## 📄 Licencia

| Qué | Licencia | Incluye |
|---|---|---|
| **Código** | [MIT](LICENSE) | `scripts/`, `tests/`, `tools/`, manifiestos y CI |
| **Contenido** | [CC BY 4.0](LICENSE-CONTENIDO.md) | Manual, flujos, plantillas, guías, registros, parámetros y demo |

Puedes usar y adaptar el contenido, incluso comercialmente, citando la fuente.

<div align="center">

Hecho en Chile 🇨🇱 para fundadores de toda Latinoamérica.

</div>
