# Recetas de investigación web (con Firecrawl local)

Cada receta termina en **registros y documentos del expediente**, no en un resumen suelto en el chat. Una investigación sin URL, fecha y limitación no sirve como evidencia. `FC` = `python <ruta-skill>/scripts/firecrawl.py`.

Antes de lanzar cualquier receta, dile al usuario en una línea qué vas a buscar y por qué (p. ej. "voy a revisar los sitios de 4 competidores para comparar precios y propuesta; toma unos minutos"). Al terminar, muéstrale lo encontrado en una tabla corta y pídele que corrija o agregue lo que sabe por experiencia: el fundador suele conocer competidores que no aparecen en Google.

---

## R1. Mapa de competencia (módulo 08 → TPL-031, TPL-033, competencia.csv)

**1. Construir la lista de alternativas** — no solo startups parecidas. El manual exige cinco tipos:
| Tipo | Ejemplo de cómo encontrarlo |
|---|---|
| Directo | búsqueda "[categoría] Chile", "[categoría] software LATAM", directorios (Capterra/G2 categoría + filtro país), ferias del sector |
| Indirecto | otra forma de resolver el mismo trabajo (consultoras, planillas, ERP con módulo) |
| In-house | ¿el cliente lo resuelve con su propio equipo/Excel? (pregúntalo al usuario y en entrevistas) |
| Servicio | agencias, outsourcing, consultores independientes |
| No hacer nada | costo de seguir igual (viene de entrevistas, no de la web) |

Búsqueda: usa la herramienta de búsqueda web del agente (es lo que funciona sin configuración). Usa `FC search` solo si `.herramientas.json` dice `search: ok`. Lanza varias consultas (español + inglés + portugués si aplica LATAM, nombre de la categoría + "precios", + "alternativas a [líder]"). Propón al usuario la lista y deja que elija 3–6 para profundizar.

**2. Ficha por competidor**
```
FC competidor https://competidor.com --nombre "Competidor" --out <proyecto>/expediente/investigacion/competencia
FC lote competidores.txt --out <proyecto>/expediente/investigacion/competencia     # varios a la vez
```
Genera `<competidor>/ficha.md` (solo la primera vez), y en `<competidor>/<fecha>/` un `.md` por página, `resumen.json` y, si hubo consulta previa, `cambios.md`. Sin Firecrawl: lee las mismas páginas con WebFetch y crea la ficha a mano con URL y fecha. Si el mapa no encontró la página de precios, revisa `FC map URL --search precio` y agrégala con `--extra URL`.

**3. Completar la ficha leyendo las páginas** — tú (el agente) extraes, citando archivo/URL. Reglas:
- Separa *declarado por el competidor* de *observado* (prueba gratuita, demo, reseñas de clientes) e *inferido por nosotros*.
- Precio: moneda original, unidad (por usuario, por mes, por empresa), fecha de consulta, IVA incluido o no. "Cotizar" es un dato (venta consultiva), no un vacío.
- Nada de "no tiene competencia" ni "nuestra ventaja es usar IA": el manual lo marca como error.

**4. Registrar**
- Una fila por alternativa: `expediente.py add competencia alternativa=… tipo=… segmento=… precio_CLP="1,9 UF + IVA/mes por sucursal" url=… evidence_id=EV-…` (ID y fecha automáticos). Si el precio está en UF o USD, escríbelo en su moneda y unidad dentro de `precio_CLP`; no conviertas sin decir con qué valor de UF/dólar y fecha.
- Una fila en `evidencias.csv` por afirmación importante (tipo `investigación secundaria`, `limitacion`: "declaración del sitio, no verificada").
- Documento `TPL-031` con la comparación en la *misma tarea y condiciones*; luego `TPL-033` (mapa de posicionamiento / strategy canvas) y, si sirve, `TPL-044` (ERRC).

**5. Cerrar con el criterio de salida del módulo 08**: ¿puede el usuario explicar por qué el comprador preferiría su oferta frente a la alternativa real, qué es condición mínima (tabla de entrada) y qué es ventaja verificable? Si no, la siguiente acción suele ser entrevistas (módulo 04), no más scraping.

---

## R2. Mercado y TAM/SAM/SOM bottom-up (módulo 07 → TPL-030, TPL-032)

1. Define con el usuario la **unidad** (empresa, establecimiento, profesional, hogar) y el precio anual neto supuesto.
2. Fuentes chilenas de partida (todas en `references/biblioteca/fuentes.csv`):
   - SII estadísticas de empresas por rubro/tamaño/región — `https://www.sii.cl/sobre_el_sii/estadisticas_de_empresas.html`
   - INE (Encuesta Longitudinal de Empresas, Encuesta de Innovación) — `https://www.ine.gob.cl/`
   - ChileCompra datos abiertos (si el cliente es el Estado) — `https://datos-abiertos.chilecompra.cl/`
   - CMF, Banco Central, gremios sectoriales, superintendencias según la industria.
   Para otros países LATAM busca el equivalente (INEGI, DANE, IBGE, INEI…).
3. `FC scrape <url> --out <proyecto>/expediente/investigacion/mercado` para guardar la página de la estadística; las tablas grandes suelen venir como Excel/CSV descargable: **pide permiso antes de descargar archivos** (nombre, origen y tamaño) y regístralos.
4. Cada filtro del embudo TAM → SAM → SOM lleva fuente o se marca "supuesto" con plan para verificarlo. SOM sale de capacidad comercial y conversiones, nunca de "el 1% del mercado".
5. Registra fuentes en `fuentes_nuevas.csv` y el cálculo en `TPL-030`.

---

## R3. Verificar convocatorias CORFO / ANID / Start-Up Chile (módulo 25 → TPL-103, corfo_elegibilidad.csv)

Los montos, plazos y requisitos de `references/corfo/01_guia_de_postulacion.md` tienen fecha de corte (25-11-2026) y **cambian por llamado**. Antes de afirmarle al usuario que puede postular:
1. Scrapea la ficha del programa y la convocatoria vigente (URLs en la guía y en `fuentes.csv`, categoría CORFO). Si no sabes la URL vigente, busca "[instrumento] [año] convocatoria [región]".
2. Extrae: apertura, cierre (con hora y zona), beneficiario, antigüedad, ventas, monto y %, cofinanciamiento, patrocinador, documentos. Cita la página.
3. Las bases suelen ser PDF: léelas como texto con `FC scrape <url.pdf> --timeout 180 --out <proyecto>/expediente/investigacion/fuentes` (o WebFetch). Leer un PDF público no requiere permiso; descargar el archivo original sí (dile nombre, origen y tamaño).
4. Una fila por requisito: `expediente.py add corfo_elegibilidad convocatoria=… requisito=… url=… estado=cumple|no cumple|pendiente observacion=…`.
5. Si un requisito bloquea (p. ej. ventas mayores a lo permitido por Semilla Inicia), dilo claro y propone el instrumento que sí corresponde. Nunca sugieras alterar fechas de facturación o datos para calzar.

Para buscar proyectos adjudicados parecidos: DataInnovación (`https://datainnovacion.cl/buscador-proyectos`) y Data Emprendimiento de CORFO. Sirven para estudiar, no para estimar probabilidad de éxito.

---

## R4. Auditoría del sitio o materiales propios (modo *pulir*)

1. `FC competidor <sitio-propio> --nombre "propio" --out <proyecto>/expediente/investigacion/propio` (sí, la misma receta).
2. Revisa contra el expediente: ¿la promesa del sitio coincide con el problema validado? ¿El segmento es el ICP? ¿Hay afirmaciones sin evidencia ("reduce 80% el tiempo")? ¿El precio publicado coincide con el modelo financiero?
3. Lista las inconsistencias como hallazgos con acción sugerida; no reescribas el sitio a menos que lo pidan.

---

## R5. Señales de demanda y desafíos corporativos (módulos 02 y 15 → desafios_corporativos.csv)

Programas de innovación abierta, desafíos de corporaciones, licitaciones de Compra Pública de Innovación (`https://www.chilecompra.cl/cpi/`), Expande Minería, etc. Scrapea las bases públicas y registra organización, problema, requisitos, TRL, presupuesto publicado y condición de piloto. Son pistas de oportunidad (G0) y posibles pilotos (G6).

---

## R6. Re-verificar fuentes del pack

`references/biblioteca/fuentes.csv` tiene 268 fuentes, solo 59 reconsultadas al corte. Cuando una afirmación importante del usuario dependa de una fuente marcada como no verificada, scrapea la URL, confirma que dice lo que se cita y registra la reconsulta en `fuentes_nuevas.csv` (fecha, hallazgo, límite, estado). Si la URL murió, dilo y busca la fuente vigente.
