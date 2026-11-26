# TPL-049 — Lienzo de propuesta de valor (Value Proposition Canvas)

> **Para qué sirve:** Comprobar que cada elemento de la oferta responde a un trabajo, dolor o ganancia observado en un segmento concreto.
> **Cuándo NO usarla:** Mezclando varios segmentos en un mismo lienzo, o sin entrevistas que respalden los dolores; termina siendo una lista de deseos.
> **Micro-ejemplo resuelto:** El dolor "el apoderado no sabe si su hijo llegó al colegio" (7 de 11 entrevistas) justifica la notificación de llegada; el "chat entre apoderados" no calza con ningún dolor observado y sale del MVP.

**Gate:** G3 · **Alimenta:** `hipotesis.csv`, `evidencias.csv`, `entrevistas.csv`

## Completar
**Segmento (uno solo):** [rol + tipo de organización + tamaño] · **Comprador, si es distinto:** [rol]
*Un canvas por segmento; si usuario y comprador son distintos, haz dos perfiles.*

### Perfil del cliente
| # | Tipo | Enunciado (en palabras del cliente) | Importancia 1–5 | Satisfacción con su alternativa 1–5 | ENT/EV o supuesto |
|---|---|---|---|---|---|
| J1 | Trabajo | [qué intenta lograr: funcional, social o emocional] | | | |
| D1 | Dolor | [obstáculo o costo concreto, con frecuencia] | | | |
| G1 | Ganancia | [resultado que mediría como éxito] | | | |

### Mapa de valor
| Elemento de la oferta | Cubre (D#, G#) | Tipo de valor (básico / funcional / facilidad / individual) | Prueba (EXP-ID) |
|---|---|---|---|

*Toda capacidad sin dolor o ganancia asociado se elimina o se marca "apuesta". Escribe resultados medibles, no adjetivos ("más fácil").*

**Ajuste:** [dolores con importancia ≥4 y satisfacción ≤2 que la oferta cubre] · **Promesa:** [resultado + plazo + alcance + cómo se prueba]

## Ejemplo bueno (ficticio)
"AgendaKine", confirmación de horas y lista de espera para centros de kinesiología de 3–8 boxes, Gran Concepción. Comprador = usuaria: dueña-administradora.

| # | Enunciado | Imp. | Sat. | Evidencia |
|---|---|---|---|---|
| J1 | "Tener los boxes llenos toda la semana" | 5 | 2 | ENT-001…ENT-008 |
| D1 | 15–20% de horas perdidas por inasistencia sin aviso | 5 | 1 | EV-002 (agendas de 3 centros, 6 semanas) |
| D2 | La secretaria pasa ~1 h diaria confirmando por teléfono | 4 | 2 | ENT-003, ENT-006 |
| G1 | Rellenar la hora liberada el mismo día | 4 | 1 | supuesto H-005 |

| Elemento | Cubre | Tipo | Prueba |
|---|---|---|---|
| Confirmación automática por WhatsApp 24 h antes | D1, D2 | funcional | EXP-003 |
| Lista de espera que ofrece la hora liberada | G1 | funcional | EXP-004 |
| Panel de ocupación por box | J1 | facilidad | apuesta: sin dolor observado |

**Promesa:** "Reduce a la mitad tus horas perdidas en 8 semanas" — supuesto, depende de EXP-003.

## Ejemplo malo y por qué falla
Cliente: clínicas, pacientes y kinesiólogos. Jobs: mejorar la salud. Pains: mala gestión. Gains: eficiencia. Producto: plataforma integral con IA, telemedicina, ficha clínica, pagos y agenda.
- Mezcla tres segmentos y a usuario con comprador en un solo perfil.
- Dolores y ganancias son adjetivos sin frecuencia ni costo, y nada tiene ENT/EV.
- El mapa de valor enumera funciones sin vincularlas a un dolor: canvas decorativo.
- No hay promesa medible ni prueba asociada.

## Criterio de aceptación
- El perfil cubre un solo segmento y nombra al comprador.
- Cada dolor y ganancia top tiene importancia, satisfacción y un ID o la marca "supuesto".
- Cada elemento de la oferta apunta a un D#/G# o está marcado "apuesta".
- La promesa tiene resultado, plazo y alcance, y su prueba existe en `experimentos.csv`.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
