# TPL-048 — Lienzo Lean (Lean Canvas)

> **Para qué sirve:** Resumir la apuesta de negocio en una página y señalar su supuesto más riesgoso antes de construir.
> **Cuándo NO usarla:** Como documento para convencer a un inversionista o a un fondo, o si lo llenas una vez y no lo versionas; sirve para pensar, no para vender.
> **Micro-ejemplo resuelto:** Un servicio de riego con sensores para paltos llena los 9 bloques y ve que todo depende de un supuesto sin evidencia (H-004: los asesores agrícolas lo recomendarán); la siguiente prueba es pedir a 5 asesores que lo ofrezcan a 2 clientes cada uno.

**Gate:** G0–G3 · **Alimenta:** `hipotesis.csv`, `decisiones.csv`

## Completar
*Orden: segmento → problema → alternativas → propuesta → solución. Marca cada bloque E (evidencia, ID) o S (supuesto, H-XXX).*

| # | Bloque | Pregunta guía | E/S + ID |
|---|---|---|---|
| 1 | Segmento y early adopter | [¿Quién, cuántos, dónde? ¿Qué rasgo tiene el primero que compraría?] | |
| 2 | Problema (top 3) | [Hecho observado, frecuencia, costo actual] *Escribe el problema sin nombrar tu solución* | |
| 3 | Alternativas actuales | [¿Qué usan hoy (Excel, papel, nada) y cuánto les cuesta?] | |
| 4 | Propuesta única | [Resultado + para quién + frente a qué alternativa, en una frase] | |
| 5 | Solución mínima | [Una capacidad por problema, máximo 3] | |
| 6 | Canales | [Cómo llegas a los primeros 10 clientes, a qué costo] *"Redes sociales" no es un canal* | |
| 7 | Ingresos | [Unidad de cobro, precio neto + IVA, quién paga] | |
| 8 | Costos | [Fijos/mes y variables por cliente, con soporte e implementación] | |
| 9 | Métrica clave | [La que muestra que el cliente obtiene valor; no descargas] | |
| 10 | Ventaja injusta | [Lo que no se copia comprando: acceso, datos, red] *"Usamos IA" no es ventaja* | |

**Supuesto más riesgoso:** [bloque, H-XXX, por qué el negocio cae si es falso] · **Prueba siguiente:** [EXP-XXX]

## Ejemplo bueno (ficticio)
"RiegoSur", sensores de humedad de suelo para huertos de cerezos, Región del Maule.
1. Productores de 10–40 ha con riego tecnificado, sin agrónomo; early adopter: quien ya perdió calibre por sobre-riego — E: ENT-002, ENT-005, ENT-007
2. Riegan por calendario; 6 de 9 sobre-riegan en postcosecha sin saberlo — E: EV-003
3. Calicata manual del asesor cada 15 días (incluida en su honorario); tensiómetros sin lectura remota — E: EV-004
4. "Sabes cuándo y cuánto regar cada cuartel sin ir al potrero" — S: H-002
5. Sensor + alerta por WhatsApp + reporte semanal para el asesor — S
6. Asesores con 15–30 huertos que recomiendan — S: H-004
7. 1,2 UF + IVA por sensor/mes, mínimo 4 sensores; paga el productor — S: H-003
8. Hardware ~$95.000/sensor + 2 h de instalación — E: cotización EV-006
9. % de cuarteles con riego ajustado tras alerta (4 semanas) — S
10. Un socio es asesor con 25 huertos clientes — E: perfil del equipo

**Supuesto más riesgoso:** H-004; sin recomendación del asesor, el CAC directo no cierra · **Prueba:** EXP-002

## Ejemplo malo y por qué falla
1. Agricultores de Chile · 2. Falta de tecnología en el agro · 3. No hay competencia · 4. Plataforma IoT con IA para agricultura inteligente · 7. Suscripción · 10. Tecnología propia
- Segmento sin tamaño ni early adopter; el problema nombra la solución ("falta de tecnología").
- "No hay competencia" ignora la calicata del asesor, la alternativa real y gratuita.
- Ingresos sin unidad, precio ni pagador; ningún bloque distingue evidencia de supuesto.

## Criterio de aceptación
- El problema no menciona la solución y tiene al menos un ID de evidencia.
- Hay ≥1 alternativa actual con su costo.
- Ingresos indican unidad, precio neto, IVA y quién paga.
- Cada bloque está marcado E (con ID) o S (con su H-XXX en `hipotesis.csv`).
- Se nombra un único supuesto más riesgoso con su EXP-ID.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
