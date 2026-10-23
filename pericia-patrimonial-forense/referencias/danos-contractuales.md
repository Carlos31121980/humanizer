# Módulo B: Cuantificación de daños en contratos de obra pública

Para demandas de indemnización de perjuicios de un contratista contra el
mandante público (SERVIU, MOP, municipios) por atrasos, demoras administrativas
o recepciones conflictivas. La pregunta pericial es **"¿cuánto perdió la empresa
por hechos imputables al mandante?"**, y se responde en cuatro pasos encadenados:
hecho → imputabilidad → nexo causal → cuantía. Si falla un eslabón, el rubro no
se cobra.

## B.1 Clasificación de los hechos generadores

Clasifica cada hecho ANTES de valorizar nada. La clasificación determina qué se
puede reclamar:

| Clase | Ejemplos | Qué da derecho a reclamar (en principio) |
|---|---|---|
| **Imputable al mandante** | Entrega tardía del terreno; demora en tramitar resoluciones de aumento de plazo o de obra; estados de pago pagados fuera de plazo; recepciones con observaciones contradictorias o fuera de bases; modificaciones de proyecto; suspensiones ordenadas | Ampliación de plazo **y** perjuicios: mayores gastos generales, sobrecostos, costos financieros, lucro cesante |
| **Fuerza mayor / caso fortuito** | Pandemia, cuarentenas, catástrofes | Ampliación de plazo y exención de multas. **No** da derecho a indemnización contra el mandante, salvo que las bases o el contrato asignen ese riesgo al mandante |
| **Reacción del mandante ante la fuerza mayor** | Negar o demorar la prórroga pedida por la pandemia; cursar multas pese a la fuerza mayor; exigir recursos o protocolos no previstos sin compensarlos | Esto **sí** es imputable al mandante: se reclama el daño causado por esa decisión, no por la pandemia |
| **Propio del contratista** | Falta de personal, problemas financieros propios, errores constructivos, atraso en subcontratos | Nada. Debe descontarse del cálculo, y es lo primero que la contraparte buscará |
| **Concurrente** | Atrasos del mandante y del contratista en el mismo período | Solo la porción atribuible al mandante; se requiere análisis de retraso para separarla |

Registra cada hecho en la hoja `Hechos` con su fecha, la fecha en que el
mandante debió actuar según bases o contrato, la fecha en que actuó, el
documento que lo prueba y su clase. Los días de demora se calculan solos.

## B.2 Línea base y análisis de retraso

- **Línea base:** plazo y precio del contrato original, programa de obra
  aprobado (carta Gantt) y presupuesto de oferta con sus gastos generales y
  utilidad. Sin línea base no hay forma de medir el daño.
- **Programa real:** fechas efectivas según libro de obra, estados de pago y
  actas.
- **Métodos de análisis de retraso**, de menor a mayor exigencia probatoria:
  1. *Comparación planificado vs. real* (as-planned vs. as-built): simple, sirve cuando hay un solo hecho dominante.
  2. *Impacto sobre el programa* (impacted as-planned): se insertan los hechos del mandante en el programa original y se mide el corrimiento.
  3. *Análisis por ventanas* (windows / time impact): se analiza período a período quién causó cada atraso. Es el más defendible cuando hay atrasos concurrentes.
- Declara en el informe qué método usaste y por qué. Un perito que no lo
  declara queda expuesto a que la contraparte diga que eligió el que daba más.

## B.3 Rubros de daño

| Código | Rubro | Cómo se calcula | Prueba típica | Ataque habitual de la contraparte |
|---|---|---|---|---|
| **R-01** | Mayores gastos generales por extensión de plazo | Gastos generales mensuales efectivos (o los de la oferta, si son menores y más defendibles) × meses de atraso imputable | Contabilidad de la obra, remuneraciones de staff, arriendos de instalación de faena, seguros | "Usaron la tasa de oferta pero la real era menor", "el staff estaba en otra obra" |
| **R-02** | Mano de obra y equipos ociosos o de baja productividad | Horas o días pagados sin producción × costo horario, en el período del hecho | Planillas, libros de asistencia, contratos de arriendo de maquinaria, libro de obra | Se exige probar que el recurso estuvo efectivamente en obra y no pudo reasignarse |
| **R-03** | Mayor costo de materiales e insumos por desplazamiento temporal | (precio efectivo − precio de oferta reajustado) × cantidades | Facturas, cotizaciones de oferta, índices de precios | "El reajuste contractual ya lo cubre": verificar la cláusula de reajuste |
| **R-04** | Costos financieros | Intereses y comisiones de créditos y líneas usadas para sostener la obra; costo de mantener boletas de garantía más tiempo | Contratos de crédito, cartolas, comisiones bancarias de boletas | Nexo causal: probar que el financiamiento se tomó por el atraso y no por caja general |
| **R-05** | Intereses y reajustes por estados de pago atrasados | Monto del EP × tasa (la de bases o la legal) × días de atraso respecto del plazo de pago de las bases | Estados de pago, fechas de ingreso y de pago efectivo, bases | Discusión sobre cuándo empieza a correr el plazo (ingreso, aprobación, resolución) |
| **R-06** | Costos de aceleración | Horas extra, turnos adicionales y recursos extra incurridos para recuperar atrasos causados por el mandante | Planillas, facturas, instrucción del mandante o necesidad probada | "La aceleración fue voluntaria": conviene que exista instrucción escrita o un rechazo de prórroga |
| **R-07** | Multas cobradas indebidamente | Multas aplicadas por atrasos cuya causa era del mandante o fuerza mayor | Resoluciones de multa, descuentos en EP | Agotamiento de reclamos administrativos previos, si las bases lo exigen |
| **R-08** | Costos de la recepción conflictiva | Trabajos rehechos por observaciones contradictorias o fuera de bases; mantención de obra y guardia hasta la recepción | Actas de recepción, observaciones, libro de obra, facturas | "Las observaciones eran legítimas": se compara cada observación con bases y especificaciones |
| **R-09** | Lucro cesante: utilidad no obtenida | Utilidad de oferta sobre obra no pagada o margen perdido; en pérdida de oportunidad, utilidad probable de obras que no se pudo tomar por capacidad comprometida | Presupuesto de oferta, propuestas rechazadas o no presentadas, capacidad de contratación | Es el rubro más difícil: los tribunales exigen certeza, no mera expectativa |
| **R-10** | Daño moral de la persona jurídica | Reservado a daño a la reputación comercial, excepcional | Pérdida de clientes, prensa, registro de contratistas | Rara vez se concede; valorar si conviene incluirlo |

Reglas:
- **Sin doble cobro.** Los gastos generales (R-01) ya incluyen al staff: no
  sumar el mismo jefe de obra en R-02. Los intereses de R-05 no se duplican
  con R-04 sobre el mismo capital.
- **Descuenta lo ya compensado**: aumentos de plazo concedidos con
  compensación, obras extraordinarias pagadas, reajustes recibidos.
- **Pesos del día del daño y actualización**: cada rubro se calcula a valores de
  la fecha en que se incurrió y se actualiza a la fecha del informe con el
  índice que se declare (IPC u otro). Separa capital actualizado de intereses.

## B.4 Nexo causal

Por cada rubro, deja escrita la cadena: *hecho del mandante* → *efecto en obra*
→ *costo incurrido* → *documento que prueba el costo*. Si un costo se habría
producido de todos modos (por ejemplo, un crédito que la empresa ya tenía), no
hay nexo y el rubro cae o se reduce.

## B.5 Sensibilidad

El script calcula tres escenarios: **base** (todo lo reclamado), **conservador**
(solo hechos imputables al mandante con documento firme, tasas de oferta,
sin lucro cesante) y **mínimo** (solo R-05 y R-07, que son los más
objetivos). Presentar los tres evita que una sola partida débil hunda la
demanda, y le da al abogado un rango para negociar.

## B.6 Marco normativo de referencia

> Verificar cada texto antes de citarlo. Con SERVIU, lo primero son **las bases
> administrativas de la licitación y el contrato**: prevalecen sobre cualquier
> tabla general en materia de plazos, multas, reajustes y recepción.

| Norma | Para qué | Verificado |
|---|---|---|
| DS 236/2002 (V. y U.), Bases Generales Reglamentarias de Contratación de Obras para los SERVIU (modif. DS 34/2022, D.O. 2023) | Plazos, aumentos de plazo, multas, estados de pago, recepción provisoria y definitiva | Existencia confirmada (BCN idNorma 1194832, modificación). Leer artículos aplicables según fecha del contrato |
| DS 49/2022 (V. y U.), Bases Administrativas Generales para contratos de diseño y ejecución de obras SERVIU (modif. 2024) | Solo si el contrato es de diseño y construcción | Existencia confirmada (BCN idNorma 1196644). Revisar aplicabilidad |
| DS 355/1976 (V. y U.), Reglamento del Registro Nacional de Contratistas MINVU | Sanciones al contratista en el registro | No |
| Ley 19.886 y su reglamento | Licitación y contrato administrativo; aplicación supletoria | No |
| Ley 19.880 | Plazos de los procedimientos administrativos (demoras del organismo), silencio administrativo | No |
| Código Civil, arts. 1545, 1546, 1551, 1553, 1556, 1557, 1558, 1559 | Fuerza obligatoria, buena fe, mora, indemnización, daño emergente y lucro cesante, perjuicios previstos, intereses | No |
| Código Civil, art. 45 | Definición de fuerza mayor o caso fortuito | No |
| Ley 18.010 | Intereses corrientes y reajustabilidad | No |
| Ley 20.410 / normas de pago a 30 días a proveedores del Estado (ver Ley 21.131 y su aplicación a obras) | Plazo de pago de estados de pago e intereses por mora | No (verificar aplicabilidad a contratos de obra) |

Jurisprudencia a buscar con Legal Data Hunter o Oficio Circular: "indemnización
de perjuicios contratista SERVIU atraso recepción", "mayores gastos generales
obra pública", "fuerza mayor pandemia contrato de obra pública aumento de plazo",
"teoría de la imprevisión obra pública". Cita solo fallos verificados.
