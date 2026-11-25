# Verticales reguladas: salud y otras

**Última verificación:** 2026-11-25. En una vertical regulada, la regulación es una hipótesis de G5 tan crítica como la técnica. Regístrala en `hipotesis.csv` y en `riesgos.csv` desde G1. Orientación educativa: confirma con un abogado del sector.

## 1. Salud (healthtech)
### ¿Tu software es un dispositivo médico?
- **Régimen chileno:** el art. 111 del Código Sanitario y el DS 825/1998 hacen obligatorio el registro solo para los dispositivos que un decreto incorpora al régimen de control, de forma progresiva.
- **Decreto exento 25 (D.O. 19-03-2026):** incorpora 39 dispositivos de alto riesgo. Entre ellos hay dos tipos de software:
  - procesamiento y análisis de imágenes oncológicas;
  - planificación de tratamiento oncológico.
  
  Ambos tienen un plazo de 36 meses (hasta aprox. marzo de 2029).
- **Inferencia por verificar:** un software fuera de esas categorías no tendría hoy registro obligatorio en Chile. Pero si diagnostica o trata, el riesgo de responsabilidad es igual de alto. Si vas a exportar, aplica la regulación del país de destino (FDA, MDR europeo).
- **Diseño:** documenta el uso previsto ("apoya a…", "no reemplaza el juicio clínico"), la evaluación con casos reales y la revisión humana.

### Datos de pacientes
- **Ley 20.584:** la ficha clínica es obligatoria, puede ser electrónica, toda su información es dato sensible y se conserva al menos 15 años.
- **Hoy:** con la Ley 19.628, los datos de salud son sensibles y solo se tratan con autorización legal, consentimiento o para beneficios de salud.
- **Desde el 15-10-2027 (Ley 21.719):**
  - se exige consentimiento expreso;
  - el uso de datos de salud queda restringido a los fines de las leyes sanitarias, con excepciones.
- **Regla de la skill:** en la validación, registra hechos del proceso, no datos de pacientes. Ver `privacidad.md`.

### Telemedicina
- La Ley 21.541 (2023) permite atender por salud digital con registros iguales a los presenciales y con medios que cumplan los estándares de seguridad del MINSAL. Los prestadores institucionales requieren autorización sanitaria.
- Hay una norma técnica (NGT N°237, 2024) y una circular de la Superintendencia de Salud (IF N°514, 2025).

### Vender a salud pública
- **CENABAST:** fue el mayor comprador de salud en Mercado Público en 2025 ($1,66 billones transados; 245 proveedores).
- Las compras públicas siguen la Ley 19.886 (`compras_publicas.md`).
- Los ciclos son largos y piden registro de proveedor. Valida primero con prestadores privados o con un servicio de salud que tenga un sponsor clínico.

### Qué cambia en los gates
- **G1:** entrevista a clínicos **y** a quien paga (prestador, isapre, Fonasa, empleador). El paciente rara vez compra.
- **G5:** riesgo regulatorio evaluado (dispositivo, datos, autorización sanitaria) con fuente y fecha.
- **G6:** piloto con un comité o una jefatura clínica que lo autorice, y con un protocolo de datos.

## 2. Otras verticales: puntos de control a investigar
No hay una guía detallada en la skill. Usa la receta de investigación web R7 (`investigacion_web.md`), guarda la fuente con fecha y verifica en la norma.
| Vertical | Preguntas regulatorias típicas (verificar en la fuente oficial) |
|---|---|
| **Minería** | Acceso a faena y prevención de riesgos (SERNAGEOMIN, reglamento interno de cada compañía), registro de proveedores (`venta_corporativa.md`), pruebas en terreno con permisos de la operación |
| **Acuicultura y forestal** | Normativa ambiental y sanitaria (SERNAPESCA, SMA, CONAF), estacionalidad de los ciclos productivos, trabajo en zonas aisladas |
| **Agro** | SAG (insumos, sanidad), ventanas de cosecha que limitan los pilotos a ciertos meses |
| **Energía y clima** | SEC (certificación de productos eléctricos), CNE y coordinador eléctrico según el tipo de proyecto |
| **Fintech** | Ley 21.521 y CMF (`mvp_e_ia.md`) |
| **Educación** | Sostenedores y Mineduc (compras, datos de menores: consentimiento de padres) |
| **GovTech** | Ley 19.886, Compra Ágil (hasta 100 UTM), interoperabilidad y seguridad del Estado |

Cierra con: hipótesis regulatoria con su prueba (consulta con abogado o regulador, revisión de la norma), costo y plazo estimados del cumplimiento en el modelo, y riesgo en `riesgos.csv` con su responsable.
