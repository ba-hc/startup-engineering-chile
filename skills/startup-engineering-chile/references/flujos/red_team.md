# Red team: ensayo contra objeciones duras

Conversacional, no un documento. El fundador elige una persona (o las tres en serie); tú la interpretas con firmeza y respeto, **una objeción a la vez**, esperas su respuesta y repreguntas si esquiva. Basa cada objeción en el expediente: lo que no está registrado se cuestiona.

## Personas
**1. Evaluadora CORFO escéptica**
- ¿Es producto o es una consultoría disfrazada? ¿Qué queda cuando termina el proyecto?
- ¿Por qué esto es innovación y no adopción de algo que ya existe?
- ¿Este gasto ya lo financia otro fondo o un cliente? (doble financiamiento)
- El presupuesto: ¿por qué $X en RR.HH.? ¿Cada actividad produce un resultado medible?
- ¿El equipo tiene dedicación real? ¿Quién hace qué con qué experiencia?
- ¿Cumplen la admisibilidad (antigüedad, ventas, región) según las bases del llamado?

**2. Gerente de compras B2B chileno**
- Pagamos a 60–90 días: ¿aguanta tu caja? (corre `finanzas.py runway` con cobro diferido)
- ¿Se integra con nuestro ERP (Softland, Defontana, SAP, Buk)? ¿Quién lo mantiene?
- Son 3 personas: ¿qué pasa si quiebran? ¿Dónde están los datos? ¿Hay contrato de confidencialidad y SLA?
- ¿Quién más lo usa en Chile? ¿Puedo llamar a una referencia?
- ¿Esto pasa por licitación interna o lo apruebo yo? (unidad de decisión, TPL-022)

**3. Inversionista seed LatAm**
- El mercado chileno es chico: ¿cuál es el techo y cuál es el segundo país?
- ¿Por qué no lo hace un incumbente en 6 meses? ¿Qué barrera de entrada tienen?
- Retención: ¿cohortes? ¿NRR? ¿Por qué un cliente renovaría?
- ¿Cuánto levantan, para llegar a qué hito medible, y cuánto runway da?
- Cap table: ¿quién tiene qué, hay vesting, la PI está en la empresa?

## Cierre del ensayo
1. Tabla: objeción · calidad de la respuesta (sólida / débil / sin respuesta) · evidencia que falta.
2. Registra cada brecha relevante: `expediente.py add riesgos dominio=… riesgo=… mitigacion=…` y, si sale un aprendizaje, `add lecciones_mentores referente="red team (<persona>)" …`.
3. Propón la acción más barata que cierre la peor brecha (una entrevista, un dato, una cotización), no más slides.
