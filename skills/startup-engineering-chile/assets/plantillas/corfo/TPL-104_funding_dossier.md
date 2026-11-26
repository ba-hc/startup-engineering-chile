# TPL-104 — Expediente de postulación (Funding Dossier)

> **Para qué sirve:** Definir la intervención que financia el fondo (no toda la empresa), con resultados verificables, adicionalidad y presupuesto reconciliado.
> **Cuándo NO usarla:** Antes de pasar la matriz de elegibilidad (TPL-103), o si el fondo te obliga a hacer algo que no está en tu plan; postular solo por la plata desvía el proyecto.
> **Micro-ejemplo resuelto:** En vez de "financiar el crecimiento de la empresa", la intervención es "validar el sensor de heladas en 3 viñas del Maule en 8 meses", con subsidio de $25 M, aporte de $8,3 M (75/25) y resultado verificable "error de predicción ≤ 1 °C".

**Gate:** transversal (fondos, tras TPL-103) · **Alimenta:** `rendiciones.csv`, `bitacora.csv` (tipo kpi y riesgo)

## Completar
**Convocatoria:** [ ] · **Bases:** [versión, fecha, URL] · **Cierre:** [fecha y hora] · **Elegibilidad:** TPL-103 sin NO CUMPLE
**Intervención financiable:** [qué parte del negocio paga el subsidio y qué queda fuera]
**Incertidumbre que resuelve:** [técnica o comercial; hipótesis H-xxx]
**Objetivo general:** [transformación verificable, con magnitud y plazo]
*Sin verbos vagos (potenciar, revolucionar, aumentar sin cifra). Los objetivos específicos son resultados, no tareas.*

| Resultado (objetivo específico) | Indicador | Línea base | Meta | Mes | Medio de verificación |
|---|---|---|---|---|---|
| [ ] | | | | | |

| Adicionalidad | Sin subsidio | Con subsidio | Diferencia verificable |
|---|---|---|---|
| [desarrollo / validación / comercialización / plazo] | | | |

**Presupuesto:** total [ ] = subsidio [ ] + aporte [ ] → detalle en TPL-105 y `fondos_lint.py presupuesto --instrumento <clave> --dir .`
**Actividades y cronograma:** TPL-106 (`fondos_lint.py coherencia`) · **Riesgos top 3:** [ ] → `bitacora.csv` (tipo riesgo)
**Respuestas:** `entregables/postulacion_<instrumento>.md` con `## Título [máx N]` y `fondos_lint.py caracteres`; cada una: afirmación → evidencia → comparación → límite → siguiente acción.

## Ejemplo bueno (ficticio)
TallaJusta: medición de talla por foto para distribuidoras de ropa de trabajo. Semilla Inicia [según bases vigentes]. Intervención: validar medición y piloto; tienda online e importación quedan fuera.
Incertidumbre: ¿la medición reduce devoluciones por talla? (H-003). Objetivo general: en 8 meses, demostrar en 3 distribuidoras que esas devoluciones bajan a la mitad.

| Resultado | Indicador | Base | Meta | Mes | Verificación |
|---|---|---|---|---|---|
| Medición validada | % con error ≤ 1 talla (n=300) | sin dato | ≥ 90% | 4 | protocolo y datos |
| Piloto en 3 distribuidoras | devoluciones por talla | 14% (EV-061) | ≤ 7% | 7 | registro de devoluciones |
| Oferta comercial probada | ofertas con precio / aceptadas | 0 / 0 | 3 / ≥ 1 | 8 | propuestas y contrato |

Adicionalidad: sin subsidio, 1 distribuidora en 14 meses; con subsidio, 3 en 8 (EV-065, cotización). Presupuesto: $19.600.000 = $14.700.000 subsidio (75%) + $4.900.000 aporte (supuesto, por confirmar en bases).

## Ejemplo malo y por qué falla
> Objetivo: revolucionar la ropa de trabajo en Chile con IA. Actividades: desarrollar la app, marketing, contratar equipo. Pedimos $15M para sueldos y lanzamiento. Resultado: liderar el mercado.
- Verbo vago; meta sin cifra, fecha ni verificación.
- Financia toda la empresa, no una intervención con incertidumbre definida.
- Tareas como objetivos; omite aporte y cofinanciamiento.
- No dice qué cambia gracias al subsidio.

## Criterio de aceptación
- Cada resultado tiene indicador, línea base (o "sin dato"), meta, mes y medio de verificación.
- La intervención declara qué queda fuera del financiamiento.
- `fondos_lint.py presupuesto` y `coherencia` corren sin PROBLEMA.
- Las cifras del formulario coinciden con TPL-105, TPL-106 y el modelo financiero.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
