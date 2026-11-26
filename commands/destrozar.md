---
description: Red team sin piedad de tu idea, pitch o postulación - las objeciones que te harían un jurado CORFO, un inversionista o un cliente
argument-hint: "[idea, archivo del pitch o 'postulación']"
---

Usa la skill **startup-engineering-chile** y lee `skills/startup-engineering-chile/references/flujos/red_team.md`.

Qué destrozar: $ARGUMENTS (si está vacío, usa el `00_estado.md` del expediente; si no hay expediente, pide la idea en una frase).

1. Elige el jurado según el objetivo: comité CORFO/ANID, inversionista ángel o VC, comprador corporativo o el Estado.
2. Ataca primero las **barreras críticas** (no hay evidencia de que alguien tenga el problema, nadie paga, competidor que ya lo resuelve, ilegal o inseguro), luego economía y equipo. Cita la evidencia del expediente (EV-xxx) o di que no existe.
3. Si hay un pitch o one-pager, corre `python <skill>/scripts/dataroom.py revisar --dir <carpeta>` para listar cifras sin respaldo.
4. Responde en formato 1-3-1: **1** veredicto (lo que mataría el proyecto hoy), **3** objeciones más duras con la respuesta que hoy tendría o "sin respuesta", **1** experimento de 7 días que responde la peor.

Sé duro con la idea y respetuoso con la persona. No inventes datos para "defenderla". Si el usuario quiere guardarlo, registra cada objeción sin respuesta como riesgo: `expediente.py add bitacora tipo=riesgo …`.
