# TPL-108 — Pitch y red team

> **Para qué sirve:** Armar un pitch en el que cada frase tiene evidencia y ensayarlo contra las objeciones de una evaluadora, un comprador y un inversionista antes de presentarlo.
> **Cuándo NO usarla:** Si todavía no tienes evidencia de G1 que contar; pulir el pitch antes de salir a terreno convierte la falta de datos en un problema de oratoria.
> **Micro-ejemplo resuelto:** "los transportistas pierden 20% de sus viajes" se reemplaza por "6 de 9 transportistas entrevistados vuelven vacíos ≥ 2 veces por semana (EV-014)"; la pregunta del inversionista "¿por qué no lo hace una plataforma grande?" queda sin buena respuesta y se registra como R-009.

**Gate:** transversal (fondos e inversión) · **Alimenta:** `bitacora.csv` (tipo riesgo y leccion), `evidencias.csv`

## Completar
**Formato exigido:** [duración, video o presencial, apoyo visual: según bases vigentes] · **Demo:** [simulación / prototipo / producción]
| Seg. | Bloque | Criterio | Tu frase (≤ 2 líneas) | Evidencia (ID) |
|---|---|---|---|---|
| 20 | Problema y consecuencia | Relevancia | [ ] | |
| 25 | Usuario, comprador, segmento | Mercado | | |
| 30 | Solución y valor demostrado | Propuesta | | |
| 25 | Alternativas y diferencia comprobable | Innovación | | |
| 25 | Monetización, canal, economía | Modelo | | |
| 20 | Estado y evidencia | Validación | | |
| 20 | Equipo y dedicación | Capacidad | | |
| 15 | Qué financia y qué resultado logra | Plan | | |
*Cifra sin ID se quita. Subsidio no es tracción. "Usamos IA" no es una diferencia.*

**Red team** (`references/flujos/red_team.md`): una persona a la vez, una objeción por turno; no se discute hasta que termine.
| Persona [evaluadora CORFO / compras B2B / inversionista seed] | Objeción | Respuesta (1 línea) | Calidad [sólida / débil / sin respuesta] | Evidencia que falta | Acción más barata, responsable, fecha |
|---|---|---|---|---|---|
| [ ] | | | | | |

## Ejemplo bueno (ficticio)
RetornaPallet: arriendo y trazabilidad de pallets plásticos retornables para exportadoras de fruta en O'Higgins. Pitch de 3 min, demo = prototipo.
- Problema (20 s): "Una exportadora mediana pierde 1 de cada 9 pallets por temporada (EV-081, registros de 4 exportadoras)."
- Alternativas (25 s): "Hoy compran madera nueva o cuentan a mano; comparamos costo por viaje en TPL-031 (COMP-002)."
- Estado (20 s): "Piloto en 1 packing, 600 pallets, 2 meses (PIL-001); sin ventas aún."

| Persona | Objeción | Respuesta | Calidad | Falta | Acción |
|---|---|---|---|---|---|
| Evaluadora CORFO | ¿Producto o consultoría disfrazada? ¿Qué queda al terminar? | plataforma y etiquetas propias; servicio de conteo se elimina en mes 6 | débil | registro de PI | IP en `bitacora.csv` (tipo ip), socio A, 15-ene |
| Compras B2B | Pagamos a 90 días, ¿aguanta tu caja? | — | sin respuesta | caja con cobro diferido | `finanzas.py runway`, socio B, 10-ene |
| Inversionista seed | ¿Cuál es el segundo país? | Perú, misma fruta de exportación | débil | entrevistas allá | 3 llamadas, socio A, 31-ene |

## Ejemplo malo y por qué falla
> "Somos la plataforma líder en logística circular con IA. El mercado global de pallets es de US$80.000 millones. Ya tenemos tracción: ganamos un fondo y 500 personas siguen nuestra cuenta."
- "Líder" e "IA" sin comparación ni prueba.
- TAM top-down sin unidad ni fuente.
- Confunde subsidio y seguidores con tracción.
- No hubo red team: nadie preguntó por la caja ni por qué no lo hace un incumbente.

## Criterio de aceptación
- Cada frase con cifra tiene ID de evidencia o se marcó "supuesto".
- El pitch cabe en el tiempo exigido, cronometrado.
- Las tres personas hicieron al menos 3 objeciones y cada "débil" o "sin respuesta" quedó en `bitacora.csv` (tipo riesgo).
- La demo declara si es simulación, prototipo o producción.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
