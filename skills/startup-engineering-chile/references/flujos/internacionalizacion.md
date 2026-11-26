# Internacionalización desde Chile

Complementa el módulo 27 (`references/manual/G7-G9_venta_traccion_y_escala.md`). Regla: **no se internacionaliza un producto sin repetibilidad en casa** (G8): si en Chile aún no hay venta e implementación repetibles, salir multiplica el problema.

## 1. ¿Estás listo? (señales mínimas)
- Venta repetible con un ICP claro y un ciclo de venta conocido.
- Retención y margen que aguantan un CAC más alto (`finanzas.py unit` con CAC ×1,5–2).
- Producto que no depende de normativa chilena (SII, Previred, Mercado Público) o con un plan para adaptarlo.
- Caja para 12–18 meses de esfuerzo sin ingresos del nuevo país.

## 2. Elegir el primer mercado
Compara 2–3 países con datos, no por intuición: tamaño del ICP (número de cuentas), competencia local, regulación (facturación electrónica, datos, sector), idioma y cultura de compra, costo de entrada (entidad, equipo local), conexiones del equipo y clientes chilenos con operación allá (expandir con ellos es el camino más barato).
- **Perú y Colombia**: cercanos culturalmente, mercados medianos, facturación electrónica obligatoria con reglas propias.
- **México**: mercado grande, ciclo de venta más largo, competencia intensa; suele exigir presencia local.
- **EE.UU.**: mercado enorme y caro; tiene sentido con producto horizontal, inversionistas que lo exigen o clientes allá.
Haz entrevistas en el país objetivo (mismo guion, TPL-014) antes de abrir entidad.

## 3. ¿Delaware flip?
Crear una sociedad matriz en EE.UU. (Delaware C-Corp) dueña de la SpA chilena.
- **Conviene** cuando un inversionista o aceleradora relevante lo exige (muchos fondos de EE.UU. solo invierten así) o cuando la mayor parte del negocio estará allá.
- **No conviene todavía** si no hay inversionista que lo pida: cuesta (abogados en dos países, contabilidad, impuestos, *transfer pricing*), complica fondos chilenos (beneficiarios, domicilio) y es caro de deshacer.
- Antes de hacerlo: abogado tributario en ambos países, impacto en subsidios vigentes y en la PI (dónde queda).

## 4. Exportar servicios y precios regionales
- Exportación de servicios puede tener tratamiento de IVA especial con requisitos (consulta al contador).
- Precio en USD o moneda local con fecha de corte y regla de reajuste (`indicadores_cl.py`).
- Ajuste regional: no copies el precio chileno; valida con prueba de precio local.

## 5. Apoyos
ProChile (programas y concursos de internacionalización), Start-Up Chile (red), redes de la universidad o la incubadora, cámaras binacionales. Revisa convocatorias vigentes y regístralas en la bitácora (`tipo=requisito`). Aterrizaje en un mercado: `prochile_aterrizaje.md`.

Cierra con una decisión de gate (G9) y un experimento de entrada acotado (p. ej. 10 entrevistas + 2 pilotos en el país objetivo en 90 días).
