# TPL-094 — Registro de riesgos (Risk Register / FMEA)

> **Para qué sirve:** Llevar en un solo lugar los riesgos que pueden matar o frenar el proyecto, con probabilidad, impacto, detección, señal temprana, mitigación y dueño, y revisarlos en cada gate.
> **Cuándo NO usarla:** Como lista genérica para llenar un formulario ("riesgo de mercado", "riesgo tecnológico"), ni para problemas que ya ocurrieron, que van a la lista de acciones; un riesgo sin señal ni dueño no se está gestionando.
> **Micro-ejemplo resuelto:** R-003 "el cliente principal (62% de los ingresos) no renueva en marzo": probabilidad 3, impacto 5; señal: no agenda la reunión de renovación antes del 15 de enero; mitigación: cerrar 2 cuentas de 15 UF/mes antes de febrero; dueña: la CEO.

**Gate:** transversal (se revisa en cada cambio de gate) · **Alimenta:** `bitacora.csv` (tipo riesgo), `decisiones.csv`

## Completar
Cada fila es una entrada de `bitacora.csv` (tipo riesgo, ID R-001…): `expediente.py add riesgos riesgo="…" probabilidad=… impacto=…`

| risk_id | Causa → efecto | Tipo [demanda / venta / técnica / economía / equipo / legal / regulatorio / financiamiento] | P (1–5) | I (1–5) | D (1–5; 5 = difícil de detectar) | P×I×D | Señal temprana y umbral | Mitigación que empieza ya | Plan si ocurre | Dueño | Próxima revisión |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [R-001] | | | | | | | | | | | |

*Un riesgo de impacto 5 no se compensa con otros bajos: no promedies ni lo ordenes solo por P×I×D. Revisa el top 5 en cada cambio de gate y cierra con fecha los que ya no aplican.*
*Vienen de: pre-mortem (TPL-095), red team (TPL-108), data room (TPL-092), privacidad (TPL-097).*

## Ejemplo bueno (ficticio)
SolarAgro SpA: monitoreo de bombas solares de riego en el valle de Elqui.
| ID | Causa → efecto | Tipo | P | I | D | P×I×D | Señal | Mitigación | Dueño |
|---|---|---|---|---|---|---|---|---|---|
| R-001 | Sin cobertura celular en 30% de los predios → los datos no llegan | técnica | 4 | 4 | 2 | 32 | > 10% de lecturas perdidas en el piloto | probar enlace de radio de largo alcance en 3 predios en mayo | CTO |
| R-002 | La caja de los clientes se concentra en la cosecha → morosidad el resto del año | economía | 4 | 3 | 3 | 36 | > 20% de facturas impagas a 60 días | cobro anual anticipado con 10% de descuento | CEO |
| R-003 | Proveedor único del sensor de caudal → 3 meses sin stock | técnica | 2 | 5 | 4 | 40 | plazo de entrega > 6 semanas | homologar un segundo proveedor | CTO |
| R-004 | Un socio sigue a media jornada → velocidad insuficiente | equipo | 3 | 4 | 2 | 24 | < 20 h/semana dos meses seguidos | revisar dedicación y vesting (TPL-034) | ambos |

Revisado en G5 el 2027-06-02 (DEC-030): R-003 encabeza la lista por impacto 5 aunque su probabilidad sea baja.

## Ejemplo malo y por qué falla
> Riesgos: 1) mercado: medio; 2) tecnológico: bajo; 3) financiero: alto. Mitigación: buscar financiamiento y hacer un buen producto.
- Son categorías, no causas: nadie puede observarlas ni actuar sobre ellas.
- Sin señal, umbral ni dueño.
- Las mitigaciones son deseos, no acciones con fecha.

## Criterio de aceptación
- Cada riesgo describe una causa y un efecto propios del proyecto.
- P, I y D están puntuados; los de impacto 5 se tratan aparte.
- Cada riesgo del top 5 tiene señal con umbral, mitigación en curso, dueño y fecha de revisión.
- Está en `bitacora.csv` (tipo riesgo) y se revisó en el último cambio de gate.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
