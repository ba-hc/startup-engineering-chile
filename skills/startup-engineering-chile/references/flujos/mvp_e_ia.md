# MVP con IA y arquitectura frugal

Para productos que usan modelos de IA (LLM, visión, predicción). La pregunta no es "¿se puede hacer con IA?", sino:
- si el cliente paga por el resultado;
- si el margen aguanta el costo de inferencia;
- qué impide que te copien.

## 1. Validar antes de construir: "Mago de Oz" y concierge
- Entrega el resultado a mano o semimanual (una persona con herramientas existentes) a 3–10 clientes reales y cobra o pide un compromiso.
  - Mide: tiempo por caso, calidad aceptada por el cliente y disposición a pagar.
  - Si a mano no hay valor, la IA no lo crea.
- Registra el experimento con su umbral en `experimentos.csv` (TPL-061). El guardrail típico es la tasa de errores que el cliente tolera.

## 2. Costo unitario de inferencia
Calcula el costo por unidad de valor (por informe, por conversación, por documento):
- **Fórmula:** tokens de entrada y salida por caso × precio por token del proveedor, más reintentos, más revisión humana (minutos × costo hora), más infraestructura.
- **Cifras:** usa precios vigentes del proveedor con fecha de consulta en la bitácora (`tipo=fuente`). No los cites de memoria.
- **Margen:** ponlo como costo variable en `finanzas.py unit --precio … --costo-variable …`. Si el margen de contribución es menor a ~60% en software, revisa el precio, el modelo usado o el diseño (caché, modelos más pequeños para tareas simples, procesamiento por lotes).
- **Sensibilidad:** el costo por caso varía mucho entre usuarios. Mide la distribución en el piloto, no solo el promedio.

## 3. Foso defensivo más allá del "wrapper"
Pregunta por escrito qué de esto existe o se puede construir, y con qué evidencia:
- **Datos propios** que mejoran el resultado y que un competidor no tiene (con permiso de uso: ver privacidad).
- **Integración profunda** en el flujo del cliente (costo de cambio).
- **Distribución:** canal o alianza difícil de replicar.
- **Conocimiento del dominio** reflejado en evaluaciones propias: conjunto de casos con la respuesta correcta que mide la calidad en cada cambio.

Si la única ventaja es el prompt, asume que el proveedor del modelo o un competidor lo copiará. Regístralo como riesgo (`add bitacora tipo=riesgo …`).

## 4. Calidad y riesgo
- Define antes del piloto una **evaluación**: 30–100 casos reales anonimizados con la respuesta esperada, una métrica (exactitud, tasa de error grave) y un umbral para salir a producción.
- Errores con consecuencias (salud, finanzas, legal): revisión humana obligatoria, y TPL-097 (seguridad y privacidad). Ver `verticales_reguladas.md`.
- **Datos personales:** enviar datos de clientes a un proveedor de IA es tratamiento de datos. Hay que tener base de licitud, contrato con el proveedor y minimización. La Ley 21.719 rige desde el 15-oct-2027 (`privacidad.md`).

## 5. Regulación (al 2026-11-25)
- **Ley Fintec 21.521:** si el producto presta alguno de los 7 servicios regulados, requiere inscripción en el registro de la CMF y autorización. Los servicios son:
  - financiamiento colectivo;
  - sistemas alternativos de transacción;
  - asesoría crediticia;
  - asesoría de inversión;
  - custodia;
  - enrutamiento de órdenes;
  - intermediación.
  
  Desde el 03-02-2025 solo operan quienes están inscritos o lo solicitaron antes. Si dudas si tu producto cae en la ley, consulta a un abogado antes de lanzar.
- **Proyecto de ley de IA** (boletines 16821-19 y 15869-19): la Cámara lo despachó en octubre de 2025. En el Senado, la comisión aprobó la idea de legislar el 26-10-2026. **No es ley vigente.** Revisa su estado en senado.cl antes de afirmar obligaciones.

Cierra con: resultado del experimento Mago de Oz, costo unitario medido y margen, foso con evidencia y decisión de gate (G4/G5).
