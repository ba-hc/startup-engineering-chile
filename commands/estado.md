---
description: Dónde está tu startup - gate actual, chequeos, misión de 7 días y alertas del expediente
argument-hint: "[carpeta del proyecto] [G0-G9]"
---

Usa la skill **startup-engineering-chile** (scripts en `skills/startup-engineering-chile/scripts/` de este plugin).

Argumentos: $ARGUMENTS (carpeta del proyecto; por defecto la actual. Un gate como `G4` revisa ese gate en vez del actual).

1. Corre `python <skill>/scripts/expediente.py estado --dir <carpeta>` (Windows: `py -3`).
   - Si responde `SIN_EXPEDIENTE`, dilo en una línea y ofrece el onboarding de 3 preguntas. No crees nada sin que acepte.
   - Si pide migrar, corre `expediente.py migrar --dir <carpeta>` y repite.
2. Corre `expediente.py gate --dir <carpeta>` (con `--gate GX` si lo pidió) y `python <skill>/scripts/auditar.py --dir <carpeta>`.
3. Responde en formato 1-3-1:
   - **1** línea: gate actual según evidencia y la barrera principal.
   - **3** como máximo: chequeos que faltan, alertas de auditar (ALERTA primero) o acciones vencidas.
   - **1** próximo paso: la misión de 7 días vigente o, si venció, una nueva propuesta con criterio de éxito.
No pegues la salida completa de los scripts; el detalle queda en el expediente. Si el usuario quiere verlo, ofrece `dashboard.py`.
