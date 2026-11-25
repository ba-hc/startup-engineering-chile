# Trampas frecuentes del ecosistema chileno (checklist)

**Última verificación:** 2026-11-25. Orientación educativa: confirma con contador o abogado. Cifras actualizables en `assets/parametros_cl.json`.

## Empresa y SII
- [ ] **Inicio de actividades** antes de facturar; giro que calce con lo que vendes. Cuidado: la fecha de inicio cuenta para la antigüedad que piden los fondos (Semilla Inicia exige < 18 meses para personas jurídicas).
- [ ] **Facturación afecta vs. exenta**: la mayoría de los servicios de software paga IVA (19%); ciertas exportaciones de servicios pueden ser exentas con requisitos. Pon el IVA explícito en cada cotización.
- [ ] **Régimen tributario**: Pro Pyme General (14 D N°3) tiene tasa de primera categoría transitoria de 12,5% en 2025–2027 (15% en 2028); el régimen general es 27% en 2026 y baja gradualmente desde 2027. Elige con contador.
- [ ] **Preventas y ventas antes de postular**: pueden cambiar tu elegibilidad (Inicia exige no tener ventas; Expande exige tenerlas). Revisa antes de emitir la primera factura.

## Personas y remuneraciones
- [ ] **Costo de contratar**: el costo empresa supera el líquido en ~30–45% (cotizaciones del trabajador + aportes del empleador: AFC, mutual y la cotización de la reforma de pensiones, que sube cada agosto hasta 2033). Calcula con `finanzas.py costo-empleado`.
- [ ] **Boletas de honorarios**: retención 15,25% en 2026 (16% en 2027, 17% en 2028). No uses honorarios para relaciones que son laborales (subordinación, horario): riesgo de demanda.
- [ ] **Socios que se pagan con el fondo**: muchas bases limitan o regulan la remuneración de socios y los honorarios a personas relacionadas; revisa el manual de rendición del instrumento antes de presupuestar.

## Fondos y patrocinio
- [ ] Algunos instrumentos exigen **entidad patrocinadora** (incubadora): revisa qué cobra (overhead), qué servicios son obligatorios y cuáles opcionales, y si pide participación (las bases pueden restringirlo).
- [ ] **Doble financiamiento**: el mismo gasto no se rinde a dos fondos.
- [ ] Guarda cada documento desde el día 1 (factura, transferencia, entregable): `fondos_lint.py rendiciones` revisa la forma.

## Marca y propiedad intelectual
- [ ] **Búsqueda en INAPI** antes de lanzar nombre o invertir en marketing: busca marcas iguales o parecidas en las clases Niza que te aplican (software: 9 y 42; servicios digitales: suele sumarse 35). Registrar es barato comparado con un rebranding forzado.
- [ ] Dominio .cl en NIC Chile a nombre de la empresa, no de un socio.
- [ ] PI cedida a la SpA (código, diseño, contenidos) — ver `socios_equity.md`.

## Datos personales
- [ ] Hoy rige la Ley 19.628; la Ley 21.719 entra en vigencia el **15-oct-2027** (postergada por la Ley 21.855). Prepárate desde ya: ver `privacidad.md`.
