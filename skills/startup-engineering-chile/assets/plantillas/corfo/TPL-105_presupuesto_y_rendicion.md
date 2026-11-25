# TPL-105 — Presupuesto y rendición

**Para qué:** que cada peso tenga actividad, resultado, cuenta y respaldo, de la postulación a la rendición. · **Gate:** transversal (fondos: formulación y ejecución) · **Alimenta:** `rendiciones.csv`

## Completar
Una fila por gasto, columnas idénticas a `rendiciones.csv` (`expediente.py add rendiciones actividad="…" presupuesto_CLP=… …`).

| gasto_id | actividad | resultado | cuenta_presupuestaria | presupuesto_CLP | comprometido_CLP | pagado_CLP | subsidio_CLP | aporte_CLP | proveedor | documento | fecha | autorizacion | medio_verificacion | estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [GAS-001] | [igual que en TPL-106] | [medible] | [según bases vigentes] | | | | | | | [factura/boleta] | [AAAA-MM-DD] | | [contrato, acta] | |

*presupuesto = subsidio + aporte en cada fila; fechas AAAA-MM-DD.*
*IVA recuperable, vehículos, inmuebles, deudas y gastos previos suelen ser no financiables; remuneración de socios y honorarios: [según bases vigentes].*
**Formulación:** `python scripts/fondos_lint.py presupuesto --instrumento <clave> --dir .` (tope, % cofinanciamiento).
**Ejecución:** `python scripts/fondos_lint.py rendiciones --dir . --inicio <inicio convenio> --fin <fin convenio>` (fechas, documentos, duplicados).
**Conciliación mensual:** presupuestado [ ] · comprometido [ ] · pagado [ ] · rendido [ ] · aprobado [ ]. *Pagado no es rendido, y rendido no es aprobado.*

## Ejemplo bueno (ficticio)
LeeConmigo: fluidez lectora para 2° básico. Semilla Inicia (75%), convenio 2027-03-01 a 2027-10-31 (supuesto).
```
gasto_id,actividad,resultado,cuenta_presupuestaria,presupuesto_CLP,comprometido_CLP,pagado_CLP,subsidio_CLP,aporte_CLP,proveedor,documento,fecha,autorizacion,medio_verificacion,estado
GAS-001,Desarrollo del motor de lectura en voz alta,Prototipo con error ≤ 10%,Recursos humanos,8000000,8000000,4000000,6000000,2000000,Desarrollador externo,Factura 1187,2027-04-30,,contrato + informe de avance 1,confirmado
GAS-002,Piloto en 4 cursos de 2° básico,Informe de piloto con línea base,Operación,3200000,1200000,1200000,2400000,800000,Imprenta,Factura 5531,2027-05-15,,acta de entrega firmada,confirmado
GAS-003,Pruebas de usabilidad con docentes,12 docentes completan la tarea sin ayuda,Operación,1600000,,,1200000,400000,,,2027-06-01,,,propuesta-agente
```
`presupuesto`: subsidio 75,0%, bajo el tope. `rendiciones`: sin problemas.

## Ejemplo malo y por qué falla
```
GAS-001,Desarrollo app,,Recursos humanos,9000000,9000000,9000000,9000000,0,Socio fundador,Boleta 15,2027-03-10,,,confirmado
GAS-002,Compra de camioneta para terreno,Logística,Inversión,4000000,4000000,4000000,3000000,500000,Automotora,Boleta 15,2027-02-20,,,confirmado
```
- Cofinanciamiento: subsidio 92% del total y fila sin aporte (`presupuesto` → PROBLEMA).
- GAS-002: presupuesto ≠ subsidio + aporte, camioneta (suele no ser financiable) y fecha anterior al convenio.
- Documento repetido y sin medio de verificación (`rendiciones` → PROBLEMA).
- Paga al socio sin revisar las bases.

## Criterio de aceptación
- `fondos_lint.py presupuesto` corre sin PROBLEMA y los AVISO tienen respuesta escrita.
- Cada `actividad` coincide con una actividad de TPL-106 (`fondos_lint.py coherencia` sin PROBLEMA).
- Todo gasto pagado tiene documento único, fecha dentro del convenio y medio de verificación.

## Decisión
Criterio fijado antes: [ ] · Resultado: [ ] · Decisión: Go / Hold / Recycle / Kill · Próxima acción, responsable y fecha: [ ]
