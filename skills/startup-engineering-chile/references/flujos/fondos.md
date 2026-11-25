# Financiamiento no dilutivo: elegir, verificar, formular y rendir

**Última verificación:** 2026-11-25. Montos, porcentajes, antigüedad y ventas cambian por convocatoria y región. Regla obligatoria: cuando una condición de elegibilidad decida si el fundador postula o no, di que es un dato de referencia y pide contrastarlo con las **bases del llamado vigente** antes de escribir una línea.

Orden: **1) instrumento correcto para la etapa → 2) admisibilidad con las bases vigentes → 3) recién entonces escribir.** No fuerces todo a Semilla Inicia.

## 1. Router por etapa (referencia, ver fuentes en `assets/fondos/instrumentos.json`)
| Situación del proyecto | Primero mira | Por qué / alerta |
|---|---|---|
| Idea o prototipo, persona natural o empresa < 18 meses **sin ventas**, innovación escalable | CORFO Semilla Inicia (hasta $15M, 75%; liderada por mujeres $17M, 85%) | Facturar antes de postular puede dejarte fuera; no hagas preventas sin revisar las bases |
| Empresa < 36 meses **con primeras ventas** (≤ $80M en 12 meses, ventas de la solución ≥ $100.000) | CORFO Semilla Expande (etapa 1 hasta $25M, 75%) | Ventas acreditadas con facturas, no cartas de intención; etapa 2 no automática |
| Ventas $80–800M y < 6 años | CORFO Escalamiento (hasta $60M, 70%) | Exige crecimiento acreditable |
| ≥ 24 meses de inicio de actividades, ventas y **riesgo tecnológico** (I+D+i) | CORFO Crea y Valida (hasta $180M; 80% micro/pequeña) | No sirve a startups muy nuevas; no cualquier SaaS es I+D |
| Base científico-tecnológica, micro/pequeña < 10 años | ANID Startup CTCI (ex Startup Ciencia; hasta ~$134,5M, 12 meses) | Aporte pecuniario mínimo 15% (10% mujeres o regiones); edición 2027 cierra 14-ene-2027 |
| Negocio sin innovación escalable (comercio, servicio local), persona sin inicio de actividades | Sercotec Capital Semilla Emprende / Abeja (≈ $3,5M) | Mejor calce que CORFO para emprendimientos tradicionales |
| Startup tecnológica que busca aceleración y red, sin ceder participación | Start-Up Chile Build ($15M), Ignite ($30M), Growth ($75M) | Términos por generación |
| Ya gasta en I+D y paga impuesto de primera categoría | Ley I+D (crédito 35%, tope 15.000 UTM/año, certifica CORFO) | Es beneficio tributario, no caja; requiere certificación previa del proyecto |
| Exporta o va a exportar | ProChile (programas y concursos sectoriales) | Revisa la convocatoria del año; suele exigir empresa constituida |
| Vender al Estado como primer cliente | `compras_publicas.md` | No es un fondo, pero suele ser más rápido que un subsidio |

Verifica: `python <skill>/scripts/fondos_lint.py instrumentos` y luego
`fondos_lint.py elegibilidad --instrumento semilla_inicia --tipo juridica --meses-inicio 10 --ventas-12m 0`.
El resultado distingue CUMPLE / NO CUMPLE / FALTA DATO / VERIFICAR. Registra cada requisito en `corfo_elegibilidad.csv` con la URL de la base y el artículo.

## 2. Formulación
Lee `references/corfo/01_guia_de_postulacion.md` (instrumentos, admisibilidad, rúbrica de referencia), `02_proyecto_presupuesto_rendicion.md` y `03_pitch_y_red_team.md`. Separa el expediente permanente del *funding dossier* por convocatoria (TPL-104). Cada respuesta: afirmación → evidencia → comparación → límite → siguiente acción.

- **Respuestas con límite de caracteres**: escríbelas en `expediente/entregables/postulacion_<instrumento>.md` con el límite en el título (`## Problema [máx 1500]`) y corre `fondos_lint.py caracteres` antes de pegarlas en el portal (deja ~3% de margen).
- **Presupuesto**: registra cada ítem en `rendiciones.csv` (actividad, resultado, cuenta, presupuesto, subsidio, aporte) y corre `fondos_lint.py presupuesto --instrumento X --dir <carpeta>`: verifica que presupuesto = subsidio + aporte, tope y % de cofinanciamiento, y avisa de ítems que suelen ser no financiables.
- **Coherencia**: `fondos_lint.py coherencia --marco documentos/TPL-106_marco_logico_y_gantt.md --dir <carpeta>`: toda actividad del marco lógico tiene presupuesto y todo gasto sirve a una actividad.
- Ensaya con `red_team.md` (persona "Evaluador CORFO") antes de enviar.

## 3. Ejecución y rendición
- Desde el día 1: cada gasto con fecha dentro del convenio, documento (factura/boleta), medio de verificación y autorización cuando las bases lo pidan. `fondos_lint.py rendiciones --dir <carpeta> --inicio AAAA-MM-DD --fin AAAA-MM-DD` revisa forma, fechas y documentos duplicados.
- Remuneraciones de socios y honorarios: revisa qué admite el manual de rendición del instrumento antes de presupuestarlos (ver `trampas_chile.md`).
- Reitemizaciones y cambios de alcance: solo con autorización; no "acomodes" gastos a cuentas con saldo.

## Nunca
Manipular ventas, fechas, la empresa postulante o la evidencia para calzar con las bases; presentar el mismo gasto a dos fondos (doble financiamiento); presentar cartas de intención como ventas.
