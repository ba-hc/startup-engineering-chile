# Umbrales por gate y ejemplos de decisiones

## Umbrales
Los umbrales de cada gate, comunes y por tipo de startup (*track*), están en `assets/umbrales_gates.json`. `expediente.py umbrales [--gate G4]` los muestra para el track del proyecto (`init --track` o `manifest.json`). Úsalos para **proponer** el criterio antes de salir a terreno. Si el fundador quiere otro umbral, que lo justifique por escrito antes de ver los datos y registralo en `experimentos.csv`.

Tracks: `saas_b2b`, `b2c`, `marketplace`, `deeptech`, `hardware`, `servicios`. Si el proyecto mezcla dos (p. ej. hardware con suscripción), usa el más exigente en cada gate.

Reglas que no cambian con el track:
- **Las barreras críticas no se promedian.** Sin problema confirmado (G1), un buen pitch no sirve.
- **Intención declarada no es compromiso.** "Me interesa", "lo compraría" o "avísame cuando esté" valen nivel 1. Valen nivel 3–4: tiempo comprometido (piloto con datos reales), acceso (datos, reunión con el aprobador) o dinero (preventa, depósito, OC).
- **El umbral se fija antes.** Bajarlo después de ver los datos es Recycle con un umbral nuevo, no Go.

## Ejemplos de decisiones de gate

### Bueno: Hold en G4 (SaaS B2B, ficticio)
> **DEC-004 · G4 · Hold.** Criterio fijado el 03-03 (EXP-002): 2 de 6 plantas firman una carta de intención a $150.000 + IVA/mes. Resultado: 1 de 6 firmó (EV-011). Otras 3 dijeron "nos interesa" sin firmar (nivel 1). Las 2 restantes piden integración con su ERP (ENT-014, ENT-016). **Decisión:** Hold 3 semanas. Probamos el plan de $90.000 sin integración con las 3 interesadas y fijamos de nuevo el umbral (2 de 3). Si no se cumple, Recycle del segmento.

Por qué es bueno:
- Cita el criterio con su fecha y el experimento.
- Separa los compromisos de las intenciones.
- Explica las objeciones con evidencia.
- Fija la siguiente prueba y la condición de salida.

### Malo: Go en G4
> **G4 Go.** Las entrevistas fueron muy positivas, a todos les gustó la idea y varios dijeron que pagarían. El mercado es grande (1 % de las pymes de Chile).

Por qué falla:
- No hubo criterio previo.
- "Dijeron que pagarían" es nivel 1.
- El tamaño de mercado es top-down y no responde la pregunta del gate.
- No cita evidencia.

### Bueno: Kill en G1 (B2C, ficticio)
> **DEC-002 · G1 · Kill.** Criterio (EXP-001): ≥5 de 12 padres relatan haber perdido una cita médica escolar en los últimos 3 meses. Resultado: 2 de 12 (EV-003, EV-004), y ambos lo resolvieron con el calendario del teléfono. El problema existe, pero es raro y tiene una alternativa gratuita suficiente. Aprendizaje: 7 de 12 mencionaron, sin que se les preguntara, la coordinación de turnos para llevar a los hijos (ENT-003, 005, 006…). Abrimos H-006 sobre ese problema.

### Malo: Go en G6 con un piloto eterno
> **G6 Go.** El piloto lleva 5 meses y el cliente está contento. Seguimos.

Por qué falla:
- No hay baseline, KPI ni precio posterior.
- "Contento" no es una métrica.
- Un piloto de 5 meses sin conversión es una señal de *pilot purgatory*.
- Corresponde Hold: fijar fecha de cierre y una propuesta de contrato.

## Ejemplos de plantillas
Cada plantilla troncal (`expediente.py plantillas --troncales`) trae un ejemplo bueno y uno malo. Para las demás, `expediente.py doc TPL-XXX` crea un esqueleto con su criterio de aceptación. Arma la estructura con el capítulo del manual del dominio y el nivel de detalle de las troncales.
