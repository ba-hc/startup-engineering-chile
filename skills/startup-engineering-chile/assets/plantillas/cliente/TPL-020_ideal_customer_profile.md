# TPL-020 — Perfil de cliente ideal (Ideal Customer Profile)

**Para qué:** definir el segmento inicial con criterios que permitan listar cuentas concretas y saber a quién hablarle dentro de cada una. · **Gate:** G2 · **Alimenta:** `cuentas_y_pipeline.csv`, `hipotesis.csv`

## Completar
**Criterios de la cuenta** *(observables desde fuera; si no puedes verificarlo antes de llamar, no es un criterio)*
| Criterio | Valor | Inclusión / exclusión | Fuente o ID |
|---|---|---|---|
| Industria / actividad | [ ] | | |
| Tamaño (trabajadores, ventas, activos) | [ ] | | |
| Región | [ ] | | |
| Proceso o tecnología presente | [ ] | | |
| Señal de compra (cambio, incidente, licitación, contratación) | [ ] | | |

**Dolor observado y alternativa actual:** [ ] (EVI/ENT)

**Unidad de decisión** *(el usuario casi nunca es quien paga; no los fusiones)*
| Rol | Cargo típico | Qué gana o arriesga | Qué necesita ver para decir sí | Evidencia |
|---|---|---|---|---|
| Usuario | | | | |
| Comprador económico | | | | |
| Aprobador (finanzas, abastecimiento, gerencia) | | | | |
| Influenciador (técnico, seguridad, TI, legal) | | | | |

**Cómo listar cuentas:** fuente [ ] → filtro [ ] → N cuentas [ ] → primeras 10 en `cuentas_y_pipeline.csv`
**Fuera del ICP (anti-ICP):** [quién parece cliente pero no lo es, y por qué]

## Ejemplo bueno (ficticio)
Proyecto "Polín" — inspección de rodillos de correas transportadoras en plantas de áridos.
- Cuenta: planta de áridos o chancado con ≥800 m de correas, RM y Valparaíso, operación de 2 turnos (EV-040, 7 entrevistas).
- Señal de compra: detención no programada por correa cortada en los últimos 12 meses (5 de 7 la tuvieron, EV-041).
- Hoy: inspección visual en ronda semanal; cambio de rodillos al fallar.
- Usuario: supervisor de mantención — evita turnos de emergencia; necesita lista priorizada de rodillos (ENT-021, ENT-024).
- Comprador económico: jefe de planta — paga con presupuesto de mantención; necesita horas de detención evitadas (ENT-022).
- Aprobador: abastecimiento — exige proveedor inscrito y 3 cotizaciones sobre cierto monto (ENT-025; umbral por confirmar).
- Influenciador: prevencionista de riesgos — veta todo lo que implique acercarse a la correa en movimiento (ENT-023).
- Listar: directorio sectorial de áridos + permisos de extracción publicados → 62 plantas → 41 cumplen ≥800 m (supuesto, verificar en visita).
- Anti-ICP: faenas de gran minería (proveedor homologado de 6–12 meses, ciclo incompatible).

## Ejemplo malo y por qué falla
> "Empresas industriales y mineras de Chile y LATAM que quieran digitalizar su mantención e innovar. Decisor: el gerente. Canal: LinkedIn."
- No se puede convertir en una lista de cuentas: ningún criterio es observable.
- "El gerente" fusiona usuario, comprador, aprobador e influenciador.
- Mezcla gran minería y pymes con ciclos de compra incompatibles.
- Sin señal de compra, dolor con evidencia ni anti-ICP.

## Criterio de aceptación
- Con los criterios se obtiene una lista de cuentas con nombre y su N.
- Usuario, comprador económico, aprobador e influenciador aparecen como roles distintos (o se justifica que coinciden).
- Cada rol tiene al menos una evidencia ENT/EVI o queda marcado "supuesto".
- Hay al menos un criterio de exclusión y un anti-ICP explícito.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
