# Startups de base científico-tecnológica (EBCT) y transferencia desde la universidad

**Última verificación:** 2026-11-25. Montos y requisitos cambian en cada convocatoria: corre `fondos_lint.py instrumentos` y revisa las bases.

Usa el track `deeptech` (`expediente.py init --track deeptech`): los umbrales piden TRL, estado del arte y validación con usuarios industriales (`expediente.py umbrales`).

## 1. Escalas de madurez
- **TRL (madurez tecnológica, 1–9)** es la escala que piden ANID y CORFO. Es independiente de la madurez comercial: una tecnología en TRL 6 puede estar todavía en G1 si nadie confirmó el problema.
- Startup Ciencia 2026 agregó un autodiagnóstico KTH IRL que mide BRL, IPRL, TMRL, FRL y CRL. Ahí **CRL significa desarrollo de clientes** (*customer*), no madurez comercial. La herramienta es calculadorarl.cl.

## 2. Escalera de financiamiento (al 2026-11-25)
| Etapa | Instrumento | Quién postula | Monto / aporte | TRL |
|---|---|---|---|---|
| Tesis | **VIU 2026** (ANID) | Estudiantes o egresados, con patrocinio de su universidad | Hasta $36M; aporte ≥20% | ≥2 |
| I+D en la universidad | **FONDEF IDeA I+D 2027** (Res. Ex. ANID 9538/2026) | Solo entidades sin fines de lucro (universidades, centros), con 1–3 empresas asociadas | Hasta $230M en 24 meses; aporte ≥30% de la beneficiaria | 2–3 (sobre TRL 3 no puede postular) |
| Spin-off | **ANID Startup CTCI 2027** (ex Startup Ciencia) | Persona jurídica de menos de 10 años, micro o pequeña (ventas ≤25.000 UF) | Hasta $134,55M (85%); aporte ≥15% (10% si la lidera una mujer o está fuera de la RM). Cierra el 14-01-2027 | 3–7 |
| Validación de mercado | **CORFO Crea y Valida** | Empresas | Hasta $180M individual / $220M colaborativo; micro y pequeñas hasta 80% | Ver bases |
| Escalamiento | **CORFO Consolida y Expande** | Empresas | Ver bases vigentes | — |

"Ciencia 2030" no es un fondo para spin-offs: es un programa institucional para facultades de ciencias.

**Ley I+D (Ley 20.241, modificada por la Ley 21.755):**
- La empresa obtiene un crédito tributario de 35% de lo invertido en I+D certificado por CORFO, con tope de 15.000 UTM al año, y deduce el 65% restante como gasto.
- Monto mínimo: más de 100 UTM. Plazo para certificar: hasta el 31-12-2035.
- Solo le sirve a quien paga impuesto de primera categoría, así que suele llegar tarde para una startup sin utilidades.

## 3. Licencia de la PI desde la universidad
Si la tecnología nació en la universidad, la PI suele ser de la universidad. En FONDEF los resultados pertenecen a la institución beneficiaria. La spin-off necesita una **licencia** o una **cesión**.
- **Con quién negociar:** la oficina de transferencia (OTL) de la universidad. Los hubs de transferencia financiados por CORFO son HubTec (PUC), Know Hub (U. de Chile) y APTA (U. Católica del Norte y red).
- **Ejemplo de política (PUC, Decreto de Rectoría 187/2020):**
  - de los ingresos por transferencia, 15% va a la Dirección de Transferencia;
  - el resto se reparte 50% para los creadores, 30% para la facultad y 20% para la universidad.
  - La PUC puede dar a una spin-off condiciones preferentes. Si participa en el capital, nombra un director.
  - Los académicos pueden ser accionistas, pero necesitan autorización para ser gerentes. Pueden pedir permiso o reducción de jornada por hasta 2 años.
- **Qué negociar:**
  - exclusividad y campo de uso;
  - territorio;
  - regalía (% de ventas) o participación en el capital (o ambas);
  - pagos mínimos e hitos;
  - quién es dueño de las mejoras;
  - sublicencias;
  - qué pasa si la startup se vende;
  - plazo y causales de término.
  
  No hay una fuente pública confiable de regalías "típicas" en Chile: compara con la política de cada universidad y con el modelo financiero (`finanzas.py escenarios`).
- **Dedicación del equipo académico:** define por escrito cuántas horas aporta cada investigador y quién será el gerente de tiempo completo. Los evaluadores lo miran y los fondos lo exigen (Startup Ciencia pide gerente de 40 h).
- Registra cada activo en la bitácora (`add bitacora tipo=ip titulo=… detalle="titular, licencia, restricciones"`) y la negociación como riesgo (`tipo=riesgo`).

## 4. Errores frecuentes
- Confundir madurez técnica con validación de mercado: hay que hacer las entrevistas de G1 con usuarios industriales, no solo con académicos (`flujos/ciclo_bloque.md`).
- Publicar el resultado antes de evaluar la patente: la publicación destruye la novedad.
- Constituir la SpA sin resolver la licencia: los inversionistas y CORFO piden la cadena de titularidad.
- Postular a FONDEF como empresa: solo postulan entidades sin fines de lucro; la empresa entra como asociada.

Cierra con: TRL actual con su evidencia, gate comercial, instrumento siguiente con su fecha de cierre (bitácora, `tipo=requisito`) y estado de la licencia.
