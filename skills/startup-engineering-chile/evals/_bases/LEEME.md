# Bases compartidas de fixtures

Expedientes que usan varios casos (`fixture.json` → `"base": "_bases/<nombre>"`). No son casos de eval: `tools/armar_fixture.py` los copia y luego aplica los archivos propios de cada caso.

- `turnos/`: expediente de una plataforma de turnos de enfermería en G1 (retomar-con-entrevistas, retomar-sin-campo).
