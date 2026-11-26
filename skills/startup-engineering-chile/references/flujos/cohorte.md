# Modo cohorte: incubadoras, cursos y aceleradoras

Para quien acompaña a varios equipos a la vez (docente, mentor, gestor de incubadora). Cada equipo usa la skill con su propio expediente; el mentor ve el conjunto.

## Organización recomendada
```
cohorte-2027/
├── equipo-alfa/expediente/
├── equipo-beta/expediente/
└── ...
```
Cada equipo inicia su expediente con `expediente.py init --dir cohorte-2027/equipo-alfa --proyecto "Alfa"`. Si los expedientes viven en carpetas compartidas, recuerda que contienen entrevistas: acceso solo para el equipo y sus mentores.

## Tablero
`python <skill>/scripts/cohorte.py --raiz cohorte-2027 --html cohorte-2027/tablero.html [--xlsx cohorte-2027/cohorte.xlsx] [--csv cohorte-2027/cohorte.csv] [--estancado 14]`
Por equipo: gate actual, chequeos del gate, entrevistas, evidencia confirmada, hipótesis estancadas, acciones vencidas, días sin actividad, días en el gate, TRL/CRL, misión de 7 días, última decisión y alertas (**sin terreno**, **estancado** (más de 14 días sin actividad; la columna «días en el gate» muestra cuánto lleva en la etapa), **misión vencida**, **acciones vencidas**, **hipótesis estancadas**, **fondo con requisitos sin verificar**, **expediente con errores**). Incluye una matriz TRL × CRL (avisa cuando la tecnología va 3 o más niveles delante del mercado). `--xlsx` consolida en un Excel la tabla de equipos y cada registro con la columna `equipo`. Al final, los bloqueos que se repiten en la generación y la distribución por gate. Solo lee: no toca los expedientes.

## Cómo usarlo en una sesión de mentoría
1. Corre el tablero antes de la sesión; ordena por alertas.
2. Con cada equipo en alerta, abre su expediente (`expediente.py estado --dir …`) y sigue `retomar.md`.
3. Si un bloqueo se repite en muchos equipos (p. ej. "sin terreno"), conviene un taller grupal: `references/operacion/workshops.csv` (20 talleres con duración, dinámica y criterio) y el currículo de 360 h en `references/operacion/curriculo_360h.csv`.
4. Para postulaciones grupales a fondos, revisa la elegibilidad de cada equipo con `fondos_lint.py elegibilidad` y deja los requisitos en su bitácora (`expediente.py add bitacora tipo=requisito titulo=… url=…`).

## Ética del seguimiento
El tablero mide actividad y evidencia, no talento. Úsalo para ayudar a destrabar, no para rankear públicamente. Un equipo que decide Kill con evidencia hizo bien su trabajo.
