# Privacidad y datos sensibles en el expediente

**Última verificación:** 2026-11-25. Marco: hoy rige la **Ley 19.628**. La **Ley 21.719** (nueva ley de protección de datos, crea la Agencia de Protección de Datos Personales) entra en vigencia el **15 de octubre de 2027**, postergada por la Ley 21.855 (D.O. 23-11-2026). Conviene trabajar desde ya con sus estándares.

## Reglas por defecto de la skill
1. **Anonimiza** entrevistas y notas: ENT-001, rol y segmento; nunca nombre, correo, teléfono, RUT ni dirección en los registros. Para transcripciones (.txt, .vtt, .srt, notas de reunión): `ingesta.py anonimizar ARCHIVO --dir <carpeta> [--nombres "..."] [--entrevistador "..."]`. Guarda solo la versión anonimizada; el script lista palabras que podrían ser nombres para revisarlas.
2. `expediente.py add` y `validar` avisan si una fila parece contener correo, teléfono o RUT.
3. El expediente trae `.gitignore` para que no se suba a git por accidente. Si el fundador lo quiere versionar, solo en un repositorio **privado**.
4. **Antes de enviar datos confidenciales a un servicio externo** (Firecrawl en la nube, otra IA, un formulario), avisa y pide permiso. Firecrawl local no envía datos fuera del computador.
5. Precios de clientes B2B, cap tables y contratos: en el expediente, no en entregables compartibles salvo que el fundador lo decida.
6. Revisa el dashboard y el one-pager antes de compartirlos: muestran lo que hay en el expediente.

## Consentimiento en entrevistas (lo que pide la Ley 21.719)
- Regla general: consentimiento **libre, informado, específico en su finalidad, previo e inequívoco** (puede ser verbal, escrito o electrónico); el responsable debe poder acreditarlo.
- **Datos sensibles** (salud, opiniones políticas, origen étnico, vida sexual, datos biométricos): consentimiento **expreso** y solo lo necesario. En proyectos de salud, evita registrar datos clínicos de personas: registra hechos del proceso, no del paciente.
- Informa para qué se usan, quién los ve y cuánto tiempo se guardan; respeta derechos de acceso, rectificación, supresión y oposición.
- Seguridad proporcional al tamaño de la empresa; reportar vulneraciones a la Agencia (y a los titulares si hay datos sensibles) cuando la ley esté vigente.
- Multas de hasta 5.000 / 10.000 / 20.000 UTM según gravedad; en los primeros 12 meses de vigencia, a empresas de menor tamaño la Agencia puede aplicar solo amonestación.

Frase sugerida para iniciar una entrevista: "Estoy investigando cómo se hace hoy [proceso]. Tomaré notas sin tu nombre ni datos de contacto, solo para este estudio; puedes pedirme que las borre cuando quieras. ¿Te parece bien?" Registra `consentimiento=si` en `entrevistas.csv`.

## Si el producto mismo trata datos personales
Es un riesgo de G5/G7: TPL-097 (seguridad y privacidad), base de licitud por cada dato, minimización, contratos con clientes (encargado de tratamiento), y registra el riesgo en `riesgos.csv`.
