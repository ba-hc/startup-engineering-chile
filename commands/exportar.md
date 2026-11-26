---
description: Genera entregables desde el expediente - dashboard HTML, one-pager, deck, reporte semanal, Excel, ZIP o data room
argument-hint: "[dashboard | onepager | deck | semanal | excel | zip | dataroom]"
---

Usa la skill **startup-engineering-chile** (scripts en `skills/startup-engineering-chile/scripts/`).

Qué exportar: $ARGUMENTS (si está vacío, genera el dashboard y el one-pager).

| Pedido | Comando |
|---|---|
| dashboard | `python <skill>/scripts/dashboard.py --dir <carpeta>` |
| onepager / semanal / deck | `expediente.py informe onepager\|semanal\|deck --dir <carpeta>` |
| excel | `expediente.py exportar todos --dir <carpeta> --xlsx` |
| csv | `expediente.py exportar todos --dir <carpeta>` |
| zip (para descargar o cambiar de equipo) | `expediente.py empaquetar --dir <carpeta> [--salida <carpeta de descargas>]` |
| dataroom | `dataroom.py revisar --dir <carpeta>` y, si está bien, `dataroom.py armar --dir <carpeta> [--zip]` |
| cohorte (incubadora) | `cohorte.py --raiz <carpeta de equipos> --html cohorte.html [--xlsx cohorte.xlsx]` |

Antes de entregar:
1. Corre `python <skill>/scripts/auditar.py --dir <carpeta>`: si hay ALERTA (cifras distintas entre `00_estado.md` y el modelo, decisiones que citan evidencia inexistente, datos personales), dila primero.
2. Toda cifra sin EV- queda marcada `[SIN RESPALDO]` o `[FALTA EVIDENCIA]`: la presentación no crea evidencia.
3. Revisa que no lleve datos personales ni confidenciales.

Responde con la ruta de cada archivo en una línea y, en formato 1-3-1, lo que el lector va a notar primero, hasta 3 vacíos que conviene cerrar y el próximo paso.
