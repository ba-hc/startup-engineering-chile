# Conectores y APIs abiertas de Chile

> **Para qué sirve:** saber qué dato público puedes traer de forma automática (UF, UTM, compras del Estado, marcas, datasets), qué credencial pide cada fuente y cuál es su límite, antes de prometer una integración o un análisis.
> **Cuándo NO usarla:** para datos personales de terceros o información detrás de un login del fundador (SII, bancos). Eso no se automatiza desde la skill.
> **Micro-ejemplo resuelto:** para un presupuesto CORFO en UF basta `scripts/indicadores_cl.py` (usa mindicador.cl, sin credenciales). Para estudiar a qué precio compra el Estado un servicio, el fundador pide su ticket de Mercado Público con ClaveÚnica y consulta órdenes de compra por proveedor, con 10.000 consultas diarias.

**Última verificación:** 2026-11-25. Orientación educativa, no asesoría legal. Las credenciales (ticket, API key) son **del fundador**: guárdalas en una variable de entorno, nunca en el expediente ni en un entregable.

## 1. Resumen
| Fuente | Qué entrega | Credencial | Límite | Oficial |
|---|---|---|---|---|
| mindicador.cl | UF, UTM, dólar, euro, IPC, IMACEC, TPM, cobre, desempleo, bitcoin | Ninguna | No publicado | **No** (servicio de terceros) |
| API CMF (v3) | Dólar, euro, IPC, TIP, TMC, TAB UF 360, UF, UTM; datos de bancos | **API key** por formulario | **10.000 peticiones al mes** por usuario | Sí |
| API Mercado Público | Licitaciones y órdenes de compra | **Ticket** con ClaveÚnica | **10.000 solicitudes diarias** por ticket, no modificable | Sí (ChileCompra) |
| datos.gob.cl | Catálogo de datasets del Estado (CKAN) | Ninguna para buscar | No publicado | Sí (Ministerio de Hacienda) |
| Banco Central (BDE) | Series estadísticas | Registro y credenciales en la BDE **[por verificar]** | **[por verificar]** | Sí |
| INAPI datos abiertos | Marcas y patentes en descarga | Ninguna | Descarga, no API | Sí |
| SII | Tablas de UF, UTM y otros valores en páginas web | No aplica | Sin API pública verificada | Sí |
| LeyChile (BCN) | Texto de normas | La consulta XML pidió API key el 25-11-2026 | **[por verificar]** | Sí |

## 2. Detalle por fuente
### mindicador.cl (no oficial)
- `GET https://mindicador.cl/api` → `version`, `autor`, `fecha` y un objeto por indicador (`codigo`, `nombre`, `unidad_medida`, `fecha`, `valor`).
- Códigos: `uf`, `ivp`, `dolar`, `dolar_intercambio`, `euro`, `ipc`, `utm`, `imacec`, `tpm`, `libra_cobre`, `tasa_desempleo`, `bitcoin`.
- `GET /api/{indicador}` → últimos ~30 días en `serie`; `/api/{indicador}/{dd-mm-aaaa}` → un día; `/api/{indicador}/{aaaa}` → un año.
- Prueba del 25-11-2026: UF $41.405,45; UTM de noviembre $72.440; UTM de diciembre $72.802.
- La skill lo usa en `scripts/indicadores_cl.py`, con caché y respaldo en `assets/parametros_cl.json`.
- **Trampa típica:** citarlo como fuente oficial. En una postulación, contrasta con el [SII](https://www.sii.cl/valores_y_fechas/utm/utm2026.htm) o el Banco Central.

Fuente: [mindicador.cl/api](https://mindicador.cl/api), consultado 2026-11-25.

### API de la CMF
- Portal: [api.cmfchile.cl](https://api.cmfchile.cl/); [documentación](https://api.cmfchile.cl/documentacion/index.html); [uso de API key](https://api.cmfchile.cl/uso-de-api-key.html). Consultado 2026-11-25.
- Patrón: `https://api.cmfchile.cl/api-sbifv3/recursos_api/utm/2026/11?apikey=CLAVE&formato=json`. También existen `/anteriores`, `/posteriores` y `/periodo`. El formato por defecto es XML y solo funciona por HTTPS.
- Sin key responde `{"CodigoHTTP": 422, "CodigoError": 92, "Mensaje": "API key no ha sido suministrada"}` (probado el 25-11-2026).
- Actualización según la CMF: TAB, dólar y euro diarios en días hábiles; IPC, UF y UTM mensuales, cerca del día 9.
- **Trampa típica:** gastar las 10.000 peticiones mensuales en un ciclo; guarda caché.

### API de Mercado Público (ChileCompra)
- Ticket: aceptar términos, entrar con ClaveÚnica; el código llega por correo. Un ticket por persona.
- Patrón: `https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?codigo=…&ticket=…` (también `ordenesdecompra`, y `.jsonp` o `.xml`).
- Parámetros: `codigo`, `fecha` (ddmmaaaa), `estado` (licitaciones: `activas`, `adjudicada`…; órdenes: `todos`, `aceptada`…), `CodigoOrganismo`, `CodigoProveedor`.
- Códigos de estado de licitación: 5 Publicada, 6 Cerrada, 7 Desierta, 8 Adjudicada, 18 Revocada, 19 Suspendida.
- ChileCompra recomienda las cargas masivas entre 22:00 y 07:00.
- Uso en la skill: ver [compras_publicas.md](flujos/compras_publicas.md).

Fuente: [chilecompra.cl/api](https://www.chilecompra.cl/api/), consultado 2026-11-25.

### datos.gob.cl
- Portal del Ministerio de Hacienda, con 3.162 datasets de 276 instituciones al 25-11-2026.
- API CKAN sin autenticación para buscar: `https://datos.gob.cl/api/3/action/package_search?q=empresas&rows=5` (probado el 25-11-2026: `success: true`).
- Cada dataset trae su propia licencia y frecuencia de actualización: revísalas antes de usarlo.

Fuente: [datos.gob.cl](https://datos.gob.cl/), consultado 2026-11-25.

### Banco Central de Chile: Base de Datos Estadísticos (BDE)
- Documentación: [Web Services BDE](https://si3.bcentral.cl/estadisticas/Principal1/Web_Services/doc_es.htm), consultado 2026-11-25.
- Según resúmenes de búsqueda, que **no** se verificaron en la página:
  - requiere registrarse en la BDE, activar credenciales y aceptar condiciones;
  - ofrece un servicio REST (`SieteRestWS.ashx`) y uno SOAP.
- Todo esto está **[por verificar]**: no lo automatices hasta leer la documentación vigente.

### INAPI (marcas y patentes)
- No encontré una API REST pública documentada **[por verificar]**. Para uso masivo, consultar a inapi@inapi.cl.
- Buscadores web: [marcas](https://buscadormarcas.inapi.cl/Marca/BuscarMarca.aspx) y [patentes](https://buscadorpatentes.inapi.cl/).
- Datos abiertos en descarga: [marcas presentadas y registradas desde 2009](https://tramites.inapi.cl/OpenData/TrademarkOpenData) y [patentes](https://tramites.inapi.cl/OpenData/PatentOpenData).

Fuente: [inapi.cl/datos-abiertos](https://www.inapi.cl/datos-abiertos), consultado 2026-11-25.

### SII y LeyChile
- **SII:** no hay una API pública verificada para datos tributarios de empresas **[por verificar]**. Para valores, usa sus tablas web (por ejemplo, la [UTM 2026](https://www.sii.cl/valores_y_fechas/utm/utm2026.htm)), la API de la CMF o mindicador.cl. Los datos tributarios del fundador (carpeta tributaria, F29) los descarga **él** y los sube como archivo.
- **LeyChile:** el 25-11-2026 la consulta XML (`leychile.cl/Consulta/obtxml`) respondió con una página que pide API key. Para leer una norma, usa el navegador o archiva la página. El acceso automatizado está **[por verificar]**.

## 3. Firecrawl
Firecrawl es un **conector opcional avanzado** para archivar páginas públicas (bases, fichas de programas, competidores). Su uso, sus requisitos y sus límites de privacidad están en [herramientas.md](herramientas.md).

## 4. Reglas de uso
1. Cita la fuente y la fecha de cada valor que entre a una postulación. Registra la fuente en la bitácora (tipo fuente, `SRC-`).
2. No envíes datos personales ni confidenciales a un servicio externo sin permiso del fundador (ver [privacidad.md](flujos/privacidad.md)).
3. Si una API falla, usa el respaldo con fecha. No inventes el valor.
