# TPL-111 — Acuerdo de confidencialidad (Non-Disclosure Agreement, NDA)

> **Para qué sirve:** Proteger información concreta (datos de un cliente, código, precios, secretos de proceso) por un plazo definido cuando de verdad hay que compartirla para un piloto, una integración o una due diligence.
> **Cuándo NO usarla:** En entrevistas de descubrimiento, para mostrar el pitch a inversionistas (la mayoría no firma NDA y pedirlo resta) o para "proteger la idea"; tampoco reemplaza la cesión de PI a la SpA ni el contrato de encargo de datos personales.
> **Micro-ejemplo resuelto:** Antes de recibir 18 meses de registros de mantención de una planta, la startup firma un NDA mutuo de 3 años que define como confidencial "los registros entregados y sus derivados", excluye lo que ya era público y obliga a devolver o destruir los datos 30 días después del piloto.

**Gate:** transversal (antes de compartir información sensible: típ. G5–G7 y due diligence) · **Alimenta:** `bitacora.csv` (tipo ip y riesgo), `cuentas_y_pipeline.csv`

## Completar
*Orientación educativa; lo revisa un abogado. En Chile un NDA es un contrato (Código Civil, y Código de Comercio entre comerciantes): para cobrar perjuicios hay que probarlos, salvo que se pacte una cláusula penal. Si se comparten datos personales, además se firma un contrato de encargo de tratamiento (TPL-097).*

| Elemento | Contenido |
|---|---|
| Tipo | [unilateral (revela una parte) / mutuo] |
| Partes y firmantes con poder | [razón social, RUT, representante] |
| Propósito permitido | [evaluar el piloto X; integrar Y] — *la información solo se usa para esto* |
| Información confidencial | [lista específica; marcada o identificada por escrito] |
| Excepciones | [ya pública, ya conocida, desarrollada de forma independiente, recibida lícitamente de un tercero, exigida por ley o autoridad] |
| Quién accede | [solo quien necesita conocerla; asesores con deber de confidencialidad] |
| Plazo | [vigencia + años de obligación posterior; secretos de proceso mientras lo sean] |
| Devolución o destrucción | [plazo y certificado] |
| PI | [el NDA no cede ni licencia nada; quién es dueño de mejoras y derivados] |
| Incumplimiento | [cláusula penal en UF o indemnización de perjuicios] |
| Ley y conflictos | [ley chilena; tribunales de Santiago o arbitraje] |
| No contratación / exclusividad | [solo si se justifica; suele ir en otro contrato] |

## Ejemplo bueno (ficticio)
PredictaPlanta SpA y una planta de alimentos de la Región de O'Higgins (CTA-014), para el piloto PIL-006. NDA mutuo.
- Propósito: evaluar la predicción de fallas de compresores con datos históricos de la planta.
- Confidencial: registros de mantención 2025–2026 y planos de la sala de máquinas (planta); código y modelo (startup). Excepciones estándar.
- Plazo: 2 años de vigencia + 3 de obligación; datos devueltos o destruidos 30 días tras el piloto, con certificado.
- PI: los registros siguen siendo de la planta; el modelo y sus mejoras genéricas, de la startup; el informe con resultados de la planta, de la planta.
- Cláusula penal de 200 UF; ley chilena; arbitraje en Santiago. Revisado por abogado; registrado como IP-004 en bitácora.

## Ejemplo malo y por qué falla
> Pedimos NDA a cada persona que entrevistamos y a los 20 inversionistas a los que enviamos el deck. El texto, bajado de internet en inglés, dice que "toda información, en cualquier forma, es confidencial para siempre" y no dice de quién es lo que se desarrolle en el piloto.
- En descubrimiento o con inversionistas, el NDA espanta conversaciones y no protege nada valioso.
- "Toda información, para siempre" no identifica qué se protege y es difícil de exigir.
- Sin regla de PI, el cliente podría reclamar el modelo entrenado con sus datos.
- Ley y jurisdicción ajenas para un contrato entre partes chilenas.

## Criterio de aceptación
- Hay una razón concreta para compartir información y está escrita como propósito.
- Información confidencial, excepciones, plazo y devolución están definidos.
- La propiedad de mejoras y derivados quedó explícita.
- Si hay datos personales, existe además el contrato de encargo de tratamiento.
- Lo revisó un abogado y quedó registrado en `bitacora.csv` (tipo ip).

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
