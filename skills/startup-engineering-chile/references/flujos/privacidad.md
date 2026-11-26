# Privacidad y datos sensibles en el expediente

**Última verificación:** 2026-11-25. Orientación educativa, no asesoría legal.

**Marco legal:**
- Hoy rige la **Ley 19.628**.
- La **Ley 21.719**, nueva ley de protección de datos, fue publicada en el D.O. el 13-12-2024. Crea la Agencia de Protección de Datos Personales.
- Su vigencia original era el 1-12-2026. La **Ley 21.855** (D.O. N° 44.606, 23-11-2026) la trasladó al **15 de octubre de 2027**. Además, amplió el Consejo Directivo de la Agencia a 5 consejeros.
- Hasta esa fecha siguen las obligaciones de la Ley 19.628. Conviene trabajar desde ya con los estándares de la 21.719.

Fuentes, consultadas el 2026-11-25:
- [Ley 21.719 en el Diario Oficial](https://www.diariooficial.interior.gob.cl/publicaciones/2024/12/13/44023/01/2583630.pdf)
- [Ley 21.719 en LeyChile](https://www.bcn.cl/leychile/navegar?idNorma=1209272)
- [Ley 21.855 en LeyChile](https://www.bcn.cl/leychile/navegar?idNorma=1230520)

## Reglas por defecto de la skill
1. **Anonimiza entrevistas y notas.** Usa ENT-001, rol y segmento; nunca nombre, correo, teléfono, RUT ni dirección en los registros.
   - Para transcripciones (.txt, .md, .vtt, .srt): `ingestar.py anonimizar ARCHIVO --dir <carpeta> [--nombres "..."] [--id ENT-004]`.
   - `ingestar.py revisar ARCHIVO` solo informa datos personales, sin escribir.
   - Guarda solo la versión anonimizada. El script lista palabras que podrían ser nombres, para revisarlas a mano.
2. `expediente.py add` y `validar` avisan si una fila parece contener correo, teléfono o RUT.
3. El expediente trae `.gitignore` para que no se suba a git por accidente. Si el fundador lo quiere versionar, solo en un repositorio **privado**.
4. **Antes de enviar datos confidenciales a un servicio externo** (Firecrawl en la nube, otra IA, un formulario), avisa y pide permiso. Firecrawl local no envía datos fuera del computador (ver [herramientas.md](../herramientas.md)).
5. Precios de clientes B2B, cap tables y contratos van en el expediente, no en entregables compartibles, salvo que el fundador lo decida.
6. Revisa el dashboard y el one-pager antes de compartirlos: muestran lo que hay en el expediente.

## Consentimiento en entrevistas (lo que pide la Ley 21.719)
- **Regla general (art. 12):** consentimiento **libre, informado, específico en su finalidad, previo e inequívoco**. Puede ser verbal, escrito, electrónico o un acto afirmativo claro, y es revocable. El responsable debe poder acreditarlo.
- **Otras bases sin consentimiento (art. 13):** obligación legal, contrato o medidas precontractuales, interés legítimo que no afecte los derechos del titular, y defensa de derechos. Para datos económicos, financieros, bancarios o comerciales rige su Título III.
- **Datos sensibles** (salud, opiniones políticas, origen étnico, vida sexual, datos biométricos):
  - exigen consentimiento **expreso** y solo lo necesario (art. 16);
  - salud y perfil biológico tienen reglas propias (art. 16 bis);
  - en proyectos de salud, evita registrar datos clínicos de personas: registra hechos del proceso, no del paciente.
- **Derechos del titular (art. 4):** acceso, rectificación, supresión, oposición, portabilidad y bloqueo. Informa para qué se usan los datos, quién los ve y cuánto tiempo se guardan.
- **Seguridad** proporcional al tamaño de la empresa. Cuando la ley esté vigente, las vulneraciones se reportan a la Agencia "sin dilaciones indebidas". También a los titulares si afectan datos sensibles, datos de **menores de 14 años** o datos **económicos, financieros, bancarios o comerciales** (art. 14 sexies).
- **Sanciones (art. 35):**
  - multas de hasta 5.000, 10.000 o 20.000 UTM según gravedad;
  - recargo de 50% si no se corrige en 60 días;
  - con reincidencia, hasta el triple;
  - para empresas que no son EMT y reinciden, hasta 2% o 4% de los ingresos anuales.
  - En los primeros 12 meses de vigencia, a las empresas de menor tamaño la Agencia **podrá** aplicar como sanción una amonestación escrita (art. 6° transitorio). Es una facultad de la Agencia, no un límite garantizado.

Frase sugerida para iniciar una entrevista: "Estoy investigando cómo se hace hoy [proceso]. Tomaré notas sin tu nombre ni datos de contacto, solo para este estudio; puedes pedirme que las borre cuando quieras. ¿Te parece bien?" Registra `consentimiento=si` en `entrevistas.csv`.

## Si el producto mismo trata datos personales
Es un riesgo de G5/G7:
- usa TPL-097 (seguridad y privacidad);
- define una base de licitud por cada dato y aplica minimización;
- firma contratos con clientes (encargado de tratamiento);
- registra el riesgo en la bitácora (tipo riesgo).

Además, con la Ley 21.719:
- **Decisiones automatizadas (art. 8 bis):** si el producto decide o perfila con efectos jurídicos o significativos (scoring, selección de personal), el titular puede pedir explicación e intervención humana. Diséñalo desde el MVP.
- **Evaluación de impacto (art. 15 ter):** es obligatoria antes de tratar cuando hay perfiles con efectos significativos, tratamiento masivo, monitoreo sistemático de zonas públicas o datos sensibles bajo excepción del consentimiento.
- **Entrenar modelos de IA:** la ley no tiene una regla específica; se aplican las reglas generales y el art. 8 bis.
- **Fintech:** el consentimiento del Sistema de Finanzas Abiertas se suma a esta ley (ver [fintech_cmf.md](fintech_cmf.md)).

## Qué hacer ahora (antes del 15-10-2027)
| Plazo | Acción |
|---|---|
| Esta semana | Inventario de datos personales que toca el producto: qué dato, para qué, base de licitud y dónde se guarda. Una fila por tratamiento en la bitácora (tipo requisito) |
| Antes del primer piloto | Texto de consentimiento o aviso de privacidad, contrato de encargo con el cliente y procedimiento para atender derechos (acceso, supresión, portabilidad) |
| Antes de escalar | Evaluación de impacto si aplica el art. 15 ter; plan de respuesta a incidentes con aviso a la Agencia y a los titulares |
| Seguimiento | Revisa las instrucciones generales que publique la Agencia (por ejemplo, la lista orientativa de casos de evaluación de impacto); su fecha de publicación está **[por verificar]** |
