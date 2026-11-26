# Socios, reparto de acciones, vesting y pacto

El conflicto entre cofundadores es una de las primeras causas de muerte temprana. Este flujo se hace **antes** de constituir o de levantar capital. Orientación educativa: el pacto lo redacta un abogado.

## 1. Conversación guiada (una sesión, con todos los socios si es posible)
- **Roles y dedicación**: quién hace qué, cuántas horas reales, desde cuándo, quién deja su trabajo y cuándo.
- **Aportes**: dinero, código, clientes, PI previa, red. ¿Se valoriza o se compensa aparte?
- **Expectativas**: tamaño de ambición, plazo, qué pasa si no hay tracción en 12 meses.
- **Salida**: qué pasa si alguien se va, se enferma o deja de rendir.
Regístralo en TPL-034 (Team Charter) y en `00_estado.md` → Equipo y dedicación.

## 2. Reparto
- **Fijo** (p. ej. 50/50 o 60/40): simple; riesgoso si las dedicaciones divergen. Iguales con dedicaciones distintas es la fuente clásica de conflicto.
- **Dinámico** (estilo "slicing pie"): acciones en proporción a aportes valorizados hasta un hito; justo pero exige registro disciplinado.
- Reserva un **pool de opciones** (típicamente 5–15%; ver §7) si se contratará talento clave; simula con `finanzas.py dilucion --fundadores "A:50,B:50" --pool 10`. Para llevar la tabla real: `cap_table.py init --fundadores "A:50,B:50" --pool 10 --vesting 48 --cliff 12 --inicio-vesting AAAA-MM-DD --dir <carpeta>`, luego `cap_table.py ver --fecha AAAA-MM-DD` (acciones consolidadas a esa fecha), `safe`, `emitir`, `ronda` y `exportar --xlsx`.

## 3. Vesting
Estándar de mercado: **4 años con 1 año de cliff** (nada si se va antes de 12 meses; luego mensual). En Chile se implementa vía pacto de accionistas con opción de compra sobre acciones no consolidadas (no es automático por ley). Define *good leaver* / *bad leaver* y precio de recompra.

## 4. Propiedad intelectual
Todo el código, marca y dominios deben quedar **a nombre de la SpA** (cesión de derechos de cada socio y freelancer). Revisa contratos laborales previos de los socios (cláusulas de PI o no competencia). Regístralo en la bitácora (`tipo=ip`). Antes de lanzar marca: búsqueda en INAPI (ver `trampas_chile.md`).

## 5. Constituir la SpA
- **Registro de Empresas y Sociedades ("Tu Empresa en un Día")**: gratis, en línea, RUT e inicio de actividades rápidos; modificaciones gratuitas en el mismo registro. Sirve y es habitual en etapas tempranas.
- **Escritura pública tradicional**: notaría, extracto, publicación e inscripción en el Conservador de Comercio; más costo, más flexibilidad para estatutos complejos.
- Desde la Ley 21.366 se puede **migrar** entre ambos regímenes. En rondas con fondos o inversionistas extranjeros (firmas, poderes apostillados, series de acciones) suele preferirse la escritura o migrar. Confírmalo con un abogado: la regla de firmas para personas jurídicas y extranjeros cambia.

## 6. Pacto de accionistas (temas mínimos)
Vesting y recompra · derecho de preferencia · *tag along* / *drag along* · gobierno (directorio, decisiones que requieren unanimidad) · no competencia y confidencialidad · resolución de conflictos (mediación/arbitraje) · qué pasa con un socio que deja de trabajar.

Cierra con: `add decisiones gate=G0 decision=Go justificacion="acuerdo de socios y vesting definidos"` y la acción "revisar pacto con abogado" con fecha.

## 7. Plan de opciones para el equipo (ESOP)
Orientación educativa al 2026-11-25; diseña el plan con abogado y contador.
- **Tamaño del pool:** 5–10% en etapa semilla es habitual; los inversionistas suelen pedir que se cree o amplíe **antes** de su ronda (pool shuffle), lo que diluye solo a los actuales. Simula con `finanzas.py dilucion --pool-post` y `finanzas.py salida` (cuánto vale cada opción en distintos precios de venta).
- **Base societaria:** el art. 24 de la Ley 18.046 permite reservar hasta 10% de un aumento de capital para planes de compensación de trabajadores; en una SpA se aplica de forma supletoria y el estatuto puede regularlo con más libertad (verificar con abogado).
- **Tributación:** el SII trata las opciones en la Circular 43 y oficios posteriores: el momento y la forma en que tributa el beneficio (al otorgar, ejercer o vender) dependen del diseño del plan. Pide la opinión de un contador **antes** de ofrecerlas.
- **Documento mínimo:** quiénes participan, vesting y cliff (igual que los fundadores), precio de ejercicio, qué pasa al renunciar o ser despedido (plazo para ejercer), aceleración en una venta, y quién administra el registro.
- **Alternativas simples** en etapas tempranas: acciones con vesting vía pacto, o un bono en efectivo atado a una venta (phantom). Para quien recibe una oferta de opciones, ver `sumarse_a_startup.md`.
