# Firecrawl local: instalación, verificación y uso

Firecrawl convierte páginas web en markdown limpio. La skill lo usa para investigar competidores, verificar convocatorias y fuentes, y auditar el sitio propio. Corre en la máquina del usuario: no hay costo por página ni se envían las consultas a terceros (salvo la búsqueda, ver abajo).

Documentación oficial: https://docs.firecrawl.dev/quickstarts/firecrawl-local y https://docs.firecrawl.dev/contributing/self-host. Las instrucciones cambian entre versiones; si algo no coincide, revisa la doc de la versión instalada.

## 1. Verificar si ya está corriendo
```
python scripts/firecrawl.py health --deep --guardar <proyecto>/expediente/.herramientas.json
```
- `--deep` hace un scrape real, un map y una búsqueda, y guarda qué funciona (`scrape: ok`, `search: no disponible`…). Así no hay que volver a probar en cada sesión: lee ese archivo.
- `health` sin `--deep` solo confirma que algo responde en el puerto.
- Código de salida 2 → no responde. Ofrece al usuario configurarlo (sección 2) **y mientras tanto sigue trabajando** con las herramientas web del agente (WebFetch/WebSearch), anotando la fuente igual que si viniera de Firecrawl. No bloquees la sesión por esto.

URL distinta a `http://localhost:3002`: define `FIRECRAWL_API_URL`. Si la instancia exige clave: `FIRECRAWL_API_KEY`.

## 2. Instalación (guiar al usuario paso a paso; confirmar antes de ejecutar comandos que instalan software)

### Opción A — Docker Compose (recomendada; instancia completa)
Requisitos: Git y Docker Desktop (Windows/macOS) o Docker Engine + Compose v2. En Windows, Docker Desktop requiere WSL2 (lo ofrece instalar la primera vez).
```
git clone https://github.com/firecrawl/firecrawl.git
cd firecrawl
```
Crear `.env` en la raíz del repo:
```
USE_DB_AUTHENTICATION=false
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<al menos 32 caracteres aleatorios>
POSTGRES_DB=postgres
```
Levantar y comprobar:
```
docker compose up --build -d
docker compose ps --all
python scripts/firecrawl.py health --deep        # en Windows evita depender de curl
```
Prueba real (la salud no prueba Playwright ni Redis):
```
python scripts/firecrawl.py scrape https://example.com
```
Apagar: `docker compose down`. Logs: `docker compose logs --tail=200 api playwright-service`.

Opcionales en `.env` (verifica los nombres en `apps/api/.env.example` de tu versión):
- **Búsqueda local**: un backend SearXNG propio (p. ej. un contenedor `searxng/searxng` en el mismo compose y `SEARXNG_ENDPOINT=http://searxng:8080`). Sin él, `search` falla o usa un respaldo frágil según la versión. No es necesario: la skill descubre con la búsqueda web del agente y usa Firecrawl para leer y archivar.
- **Formatos con LLM** (`json`, `summary`): proveedor compatible con OpenAI u Ollama (`OPENAI_API_KEY`/`OPENAI_BASE_URL`/`MODEL_NAME` u `OLLAMA_BASE_URL`). La skill **no los necesita**: el agente lee el markdown y extrae él mismo.

### Opción B — binario `firecrawl-local` (sin Docker)
Requiere Rust + compilador C (y Chrome para páginas con JavaScript).
```
cargo install firecrawl-local
firecrawl-local serve        # escucha en http://localhost:3002
```
Sirve `/v2/scrape`, `/v2/map`, `/v2/crawl`, `/v2/batch/scrape`. La búsqueda y los formatos LLM se delegan a Firecrawl Cloud (`FIRECRAWL_CLOUD=off` para impedirlo; entonces `search` no estará disponible).

### Opción C — servidor MCP
Si el usuario prefiere herramientas MCP: `npx -y firecrawl-mcp` con `FIRECRAWL_API_URL=http://localhost:3002` (Node 22+). En Windows, si aparece `spawn npx ENOENT`, usar la ruta de `npx.cmd` que entrega `where npx`. Si las herramientas `firecrawl_*` están disponibles en la sesión, puedes usarlas en vez del script; guarda los resultados en el expediente igual.

### Problemas comunes
| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| health OK pero scrape falla | servicio Playwright caído | `docker compose logs api playwright-service` |
| puerto ocupado | otro servicio en 3002 | liberar el puerto o mapear otro y ajustar `FIRECRAWL_API_URL` |
| errores de Redis | `REDIS_URL` apuntando a localhost | dentro de Compose debe ser `redis://redis:6379`; quitar overrides |
| página vacía o bloqueada | anti-bot / login / JS pesado | probar `--full`; si sigue, usar WebFetch o pedir al usuario el contenido; no intentar evadir bloqueos |
| `search` → código 3 | sin backend de búsqueda | usar la búsqueda web del agente y luego `scrape` de las URLs |

## 3. Uso desde la skill (`scripts/firecrawl.py`)
Guarda siempre dentro del expediente para que la evidencia quede trazable (cada archivo lleva URL y fecha de consulta en el encabezado).

| Objetivo | Comando |
|---|---|
| Ficha de un competidor (portada, precios, producto, clientes, integraciones, nosotros, seguridad) | `python scripts/firecrawl.py competidor https://competidor.cl --nombre "Competidor" --out expediente/investigacion/competencia` |
| Varios competidores en paralelo (un sitio a la vez por dominio) | `python scripts/firecrawl.py lote competidores.txt --out expediente/investigacion/competencia` — una línea `Nombre \| https://url` por competidor |
| Bases de un fondo en PDF (como texto) | `python scripts/firecrawl.py scrape https://…/bases.pdf --timeout 180 --out expediente/investigacion/fuentes --nombre "bases-expande-2027"` |
| Una página puntual | `python scripts/firecrawl.py scrape URL --out expediente/investigacion/mercado --nombre "ine-encuesta-x"` |
| Ver la estructura de un sitio | `python scripts/firecrawl.py map https://sitio.cl --search precios` |
| Varias páginas de una sección | `python scripts/firecrawl.py crawl https://sitio.cl/docs --limit 15 --out …` |
| Buscar (si la instancia lo permite) | `python scripts/firecrawl.py search "software inspecciones Chile" --limit 10` |

Ejecuta el script con su ruta absoluta y `--out` apuntando al expediente del proyecto. En Windows, si `python` no existe o abre la Microsoft Store, usa `py -3`; entrecomilla rutas con espacios.

**Instantáneas y cambios:** `competidor` guarda cada consulta en `<nombre>/<AAAA-MM-DD>/` y crea `<nombre>/ficha.md` solo la primera vez (nunca la sobrescribe, porque ahí queda el análisis). Si existe una consulta anterior, escribe `cambios.md` con las diferencias de precios detectados: útil al retomar ("Defontana subió de 1,5 a 2 UF").

**Fallas parciales:** un timeout o corte en una página se registra como error de esa página y la corrida sigue; solo si el servicio deja de responder se detiene, guardando lo obtenido (código 2).

## 4. Reglas de uso responsable
- Solo páginas públicas. No iniciar sesión, no saltar muros de pago ni CAPTCHAs, no recolectar datos personales (nombres de empleados, correos, teléfonos) más allá de lo que el análisis competitivo necesita.
- Respetar ritmo: el comando `competidor` pausa 1 s entre páginas; no lances crawls masivos (límite por defecto 20 páginas).
- Lo que un sitio dice es **declaración del competidor**, no un hecho verificado. Regístralo así en `evidencias.csv` (tipo: investigación secundaria / declaración).
- Las páginas guardadas son material de trabajo interno; no reproducir textos extensos de terceros en entregables públicos.
