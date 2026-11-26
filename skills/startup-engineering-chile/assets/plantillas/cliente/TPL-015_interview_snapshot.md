# TPL-015 — Ficha de entrevista (Interview Snapshot)

> **Para qué sirve:** Resumir una entrevista en una página, el mismo día, separando hechos de interpretación y ligándola a hipótesis.
> **Cuándo NO usarla:** Para conversaciones casuales de networking sin guion ni hipótesis; registrarlas como entrevista infla el conteo de evidencia.
> **Micro-ejemplo resuelto:** ENT-007 (jefe de bodega, distribuidora de 12 camiones) — hecho: "rehacemos 3 rutas por semana a mano, unas 2 h cada una"; interpretación: "el dolor sería la planificación, no el GPS"; se liga a H-003 como "apoya, débil (1 caso)".

**Gate:** G1 · **Alimenta:** `entrevistas.csv`, `evidencias.csv`, `hipotesis.csv`

## Completar
**ENT-xxx** · Fecha: [ ] · Segmento: [ ] · Rol: [ ] · Consentimiento: [si/no] · Entrevistador: [iniciales] · Notas originales anonimizadas: [ruta en `investigacion/notas/`]
*Nunca nombre, teléfono, correo, RUT ni razón social: solo rol y segmento.*

**Cita que resume (≤15 palabras):** "[ ]"

**Historia de la última vez** (`situacion`): [qué pasó, en orden, con fechas o plazos]

| Hechos observados o relatados (con número) | Interpretación del entrevistador |
|---|---|
| [ ] | [ ] |

*Lo que el entrevistado opina sobre el futuro ("lo usaría") va en interpretación, nunca en hechos.*

| Columna de `entrevistas.csv` | Contenido |
|---|---|
| necesidad | [ ] |
| alternativa (y lo que cuesta) | [ ] |
| presupuesto_declarado | [monto, período, quién aprueba; o "no declara"] |
| contradiccion (dijo vs. hizo) | [ ] |
| limitacion (sesgo, contexto, relación previa) | [ ] |

**Efecto en hipótesis:** [H-xxx: apoya / contradice / no aplica — por qué]
**Siguiente paso:** [referido, documento prometido, nueva pregunta para el guion]

## Ejemplo bueno (ficticio)
**ENT-007** · 14-10-2026 · Transportista pyme 1–10 camiones, Biobío · Dueño que factura · Consentimiento: si · Entrevistador: MC · `investigacion/notas/ENT-007.md`
**Cita:** "Esa guía la perdió el chofer y cobré casi dos meses después."
**Última vez:** entrega a un centro de distribución el 2-9; guía firmada extraviada; factura rechazada el 20-9; copia obtenida el 10-10; pago el 29-10 (57 días desde la entrega).
| Hechos | Interpretación |
|---|---|
| 4 camiones; 2 de ~60 facturas al mes rechazadas por guía en el último trimestre | El rechazo es poco frecuente pero muy costoso en caja |
| Pidió un avance de $1.500.000 a su cuñado para combustible | El dolor es de caja, no de papeleo |
| Fotografía las guías por WhatsApp "cuando se acuerda" | Ya existe un hábito digital parcial |
- necesidad: cobrar en plazo sin perseguir guías · alternativa: fotos por WhatsApp + carpeta física, $0 · presupuesto_declarado: no declara · contradiccion: dijo "ordeno todo los viernes", pero la carpeta mostrada tenía guías de 3 semanas sin archivar · limitacion: referido por un conocido del fundador.
**Efecto:** H-002 apoya (57 días > 45). **Siguiente paso:** referido a ENT-008; mostrará una guía rechazada con datos tapados.

## Ejemplo malo y por qué falla
> "Entrevista con Juan, Transportes Juan Ltda., +56 9 xxxx. Le encantó la idea, dijo que la usaría seguro y que en el rubro es un problemón. Muy buena entrevista."
- Expone datos personales e identificables en el expediente.
- Solo opiniones y promesas futuras; ningún hecho con número ni última vez.
- Interpretación ("problemón") mezclada con lo dicho; sin contradicciones ni limitaciones.
- No liga la entrevista a ninguna H-xxx ni deja siguiente paso.

## Criterio de aceptación
- Identificado solo por ENT-xxx, rol y segmento, con consentimiento registrado.
- Hay al menos una historia de "última vez" con fechas o plazos.
- Hechos e interpretación están en columnas separadas.
- Se declara al menos una limitación y el efecto sobre una H-xxx.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
