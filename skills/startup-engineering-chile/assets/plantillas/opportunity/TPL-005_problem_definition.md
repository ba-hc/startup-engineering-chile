# TPL-005 — Definición del problema (Problem Definition)

**Para qué:** expresar la necesidad con unidad de medida, contexto y consecuencia económica, sin mencionar la solución. · **Gate:** G1 · **Alimenta:** `hipotesis.csv`, `evidencias.csv`

## Completar
**Enunciado:** [Rol] en [contexto] necesita [trabajo o resultado], pero [obstáculo medible], lo que provoca [consecuencia económica]. *Si la frase dice "no tienen un sistema de…", describiste la falta de tu solución, no el problema.*

| Nivel | Descripción | Hecho observado o hipótesis | ID |
|---|---|---|---|
| Síntoma (lo que se ve) | [ ] | | |
| Causa (por qué ocurre) | [ ] | | |
| Efecto (qué cuesta) | [ ] | | |

**Línea base** *(toda cifra con denominador y período: "18 h" no dice nada; "18 de 120 h agendadas por semana" sí)*
| Métrica | Valor | Denominador y período | Fuente / ID |
|---|---|---|---|
| Frecuencia | | | |
| Tiempo de trabajo vs. espera | | | |
| Errores o reprocesos | | | |
| Costo o ingreso perdido (CLP, neto) | | | |

**Proceso actual:** proveedor → entrada → actividad → salida → usuario → responsable: [ ]
**Alternativa actual y su costo:** [manual, servicio, software genérico, nada]
**Causas que podemos cambiar / que no:** [ ]
**Pregunta abierta:** ¿Cómo podríamos [ ]?
**Fuera de alcance:** [ ]
**Verificado con:** usuario [ENT-xxx] · responsable del presupuesto [ENT-xxx]

## Ejemplo bueno (ficticio)
Clínicas dentales privadas de 3–6 sillones, Región del Maule.
- Enunciado: la recepcionista de una clínica de 4 sillones necesita llenar la agenda, pero 15% de las horas reservadas no se presenta sin aviso, lo que deja sillones ociosos y honorarios no generados.
- Síntoma: huecos en la agenda (EV-010, agenda anonimizada de 8 semanas, 1 clínica). Causa: confirmación solo por llamada el día anterior, que no alcanza a todos (hipótesis H-003, 4 de 6 entrevistas: ENT-001…006). Efecto: hora sin facturar.
- Línea base: 18 de 120 h agendadas/semana no asistidas (EV-010); la recepcionista dedica 1,5 h/día a llamar (ENT-002, declarado).
- Costo: 18 h × $40.000 ingreso promedio por hora (supuesto, confirmar con contabilidad) = $720.000/semana no realizado; recuperable solo si el hueco se rellena: supuesto 50%.
- Alternativa: llamadas manuales + lista de espera en cuaderno.
- Fuera de alcance: inasistencia con aviso; deudas de pacientes.
- Verificado con: recepcionista (ENT-002) y dueña que decide gastos (ENT-005).
*Sin datos clínicos ni de pacientes: solo hechos del proceso.*

## Ejemplo malo y por qué falla
> "Las clínicas no tienen recordatorios automáticos por WhatsApp. Esto les hace perder millones y es un problema en todas las clínicas de Chile."
- Describe la ausencia de la solución, no la necesidad.
- "Millones" sin denominador, período ni fuente.
- "Todas las clínicas" sin segmento ni proceso observado.
- No separa síntoma de causa ni verifica con quien paga.

## Criterio de aceptación
- El enunciado no nombra producto, tecnología ni funcionalidad.
- Cada métrica de la línea base tiene denominador, período y fuente o "supuesto".
- La consecuencia económica separa lo bruto de lo realmente recuperable.
- Hay al menos una entrevista con usuario y una con quien controla el presupuesto.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
