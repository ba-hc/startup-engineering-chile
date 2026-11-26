---
description: Qué fondos públicos calzan con tu startup (CORFO, ANID, Sercotec, Start-Up Chile) y revisión del presupuesto antes de postular
argument-hint: "[instrumento o perfil: 'SpA de 8 meses, sin ventas, TRL 4']"
---

Usa la skill **startup-engineering-chile** y lee `skills/startup-engineering-chile/references/flujos/fondos.md` (y `references/flujos/sercotec_vs_corfo.md` si es una pyme tradicional).

Contexto: $ARGUMENTS

1. **Calce**: `python <skill>/scripts/fondos_matcher.py --dir <carpeta>` (lee el perfil de `00_estado.md`). Sin expediente, pasa el perfil con flags: `--tipo natural|juridica --meses-inicio N --ventas-12m CLP --trl N [--mujeres] [--tradicional]`. Si falta un dato que decide, pregúntalo (máximo 3 preguntas).
2. **Presupuesto** (si ya tiene uno o una rendición): `python <skill>/scripts/presupuesto_corfo.py revisar --dir <carpeta> --instrumento <clave>`; con un CSV suelto, `--csv ARCHIVO`. Los PROBLEMA son bloqueantes (IVA recuperable, gastos fuera de plazo, tope, cofinanciamiento); los AVISO se verifican en las bases.
3. Responde en formato 1-3-1: **1** el instrumento que mejor calza (o "ninguno hoy" y por qué), **3** requisitos o problemas que deciden, **1** próximo paso con fecha (p. ej. cierre de convocatoria).

Montos y requisitos tienen fecha `_verificado` en `assets/fondos/instrumentos.json`: dila y pide confirmar en las bases vigentes. Nunca infles cifras para calzar; si la única forma es inventar, dilo y ofrece la vía honesta.
