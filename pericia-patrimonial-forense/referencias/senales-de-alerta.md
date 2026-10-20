# Catálogo de señales de alerta (30)

Cada señal trae qué buscar, cómo se ve en los datos, la explicación
alternativa típica y la prueba que la resuelve. Las que marca automáticamente
`scripts/analisis_movimientos.py` llevan **[auto]**.

La presencia de una señal **no prueba nada por sí sola**. Su valor depende de
cuántas coinciden, de su magnitud y de si la explicación alternativa queda
descartada.

---

## A. Efectivo y depósitos

**S-01 Depósitos en efectivo recurrentes sin actividad que los genere** [auto]
- *Se ve:* abonos en efectivo frecuentes en la cuenta de una persona sin giro
  comercial, o que exceden los ingresos del giro declarado.
- *Alternativa:* negocio informal declarado, ahorro previo en efectivo, ventas
  de bienes personales.
- *Resuelve:* boletas o facturas emitidas, F29, contratos de venta y retiros
  previos de efectivo que expliquen el reingreso.

**S-02 Retiros en efectivo de alto monto sin destino documentado** [auto]
- *Se ve:* giros por caja de montos altos, sobre todo antes de adquisiciones.
- *Alternativa:* compras en efectivo legítimas o pagos a trabajadores.
- *Resuelve:* escrituras, boletas o comprobantes de pago coincidentes en fecha y monto.

**S-03 Fraccionamiento bajo umbral** [auto]
- *Se ve:* varias operaciones en un plazo breve, cada una apenas bajo un umbral
  (por defecto 450 UF, el umbral de registro de efectivo de la Ley 19.913; el
  script lo recibe como parámetro en pesos) y que juntas lo superan.
- *Alternativa:* ingresos diarios de un comercio, cuotas pactadas.
- *Resuelve:* patrón histórico del giro y documentos de venta de esos días.
- *Ojo:* verificar el umbral y el valor de la UF de cada fecha.

**S-04 Montos redondos** [auto]
- *Se ve:* alta proporción de abonos o cargos en múltiplos exactos de $100.000
  o $1.000.000.
- *Alternativa:* préstamos familiares, aportes de capital y arriendos suelen ser redondos.
- *Resuelve:* contrato o mutuo que respalde cada monto.

## B. Flujo y estructura de cuentas

**S-05 Cuenta de paso** [auto]
- *Se ve:* un abono seguido de cargos de monto similar dentro de pocos días,
  con saldo que vuelve casi a cero.
- *Alternativa:* cuenta operativa de pagos a proveedores, o cuenta de un mandatario.
- *Resuelve:* mandato, contratos y quién es el beneficiario final de los cargos.

**S-06 Triangulación entre relacionados**
- *Se ve:* fondos que salen de A, pasan por B y C (cónyuge, sociedad, empleado)
  y vuelven a A o a un activo de A.
- *Alternativa:* préstamos intragrupo documentados o reorganización societaria.
- *Resuelve:* mutuos con fecha cierta, registros contables de las tres partes.

**S-07 Concentración en pocas contrapartes** [auto]
- *Se ve:* una o dos contrapartes explican la mayoría de los abonos.
- *Alternativa:* cliente único o empleador.
- *Resuelve:* contrato de prestación o de trabajo, y facturación correlativa.

**S-08 Cuentas no declaradas o abiertas cerca de la operación investigada**
- *Se ve:* cuentas que aparecen en transferencias pero no en el inventario
  entregado, o abiertas y cerradas en torno a una adquisición.
- *Alternativa:* cuentas de inversión o de crédito olvidadas.
- *Resuelve:* certificado de cuentas vigentes o requerimiento al banco vía tribunal.

**S-09 Transferencias con el exterior sin respaldo**
- *Se ve:* giros internacionales, especialmente a jurisdicciones de baja
  tributación o centros financieros, sin contrato subyacente.
- *Alternativa:* inversiones declaradas, pago de estudios o ayuda familiar.
- *Resuelve:* declaraciones juradas de inversiones en el exterior, formularios
  cambiarios y contratos.

**S-10 Desviación de la ley de Benford** [auto]
- *Se ve:* la distribución del primer dígito de los montos se aparta
  significativamente de Benford (MAD alto).
- *Alternativa:* muestras pequeñas, montos con tope o tarifas fijas. Benford no
  aplica bien con menos de unas 300 observaciones o con montos acotados.
- *Uso:* solo como indicador para dirigir la revisión, nunca como prueba.

**S-11 Movimientos duplicados o reversados** [auto]
- *Se ve:* mismo monto, misma contraparte y fecha cercana, repetidos.
- *Alternativa:* error bancario o pago en cuotas iguales.
- *Resuelve:* comprobantes individuales.

## C. Patrimonio y nivel de vida

**S-12 Incremento patrimonial sin renta suficiente**
- *Se ve:* el método de patrimonio neto arroja una diferencia positiva no
  explicada (`scripts/patrimonio_neto.py`).
- *Alternativa:* herencias, donaciones, préstamos, rentas exentas o ingresos no
  constitutivos de renta no incorporados.
- *Resuelve:* posesión efectiva, insinuación de donación, mutuos y certificados.

**S-13 Gasto de vida incompatible con la renta declarada**
- *Se ve:* colegios, viajes, tarjetas de crédito y servicio doméstico que
  superan la renta líquida (presunción del art. 70 inc. 1° LIR).
- *Alternativa:* gastos pagados por terceros (padres, empleador) o con
  endeudamiento.
- *Resuelve:* estados de cuenta de tarjetas y quién pagó cada cuota.

**S-14 Activos a nombre de terceros con uso propio**
- *Se ve:* inmuebles o vehículos inscritos a nombre de un familiar, empleado o
  sociedad, pero usados, pagados o mantenidos por el investigado (posible
  testaferro).
- *Alternativa:* comodato o arriendo real.
- *Resuelve:* quién pagó el precio, contribuciones, seguros y gastos comunes.

**S-15 Adquisiciones bajo o sobre el valor de mercado**
- *Se ve:* precio de escritura muy distinto del avalúo fiscal o de la tasación.
- *Alternativa:* bien deteriorado, venta urgente o relación familiar.
- *Resuelve:* tasación independiente y comparables.
- *Nota:* considerar la facultad de tasación del art. 64 CT (verificar texto).

**S-16 Préstamos de terceros sin respaldo**
- *Se ve:* el contribuyente justifica fondos con "préstamos" de familiares o
  amigos, sin contrato, sin fecha cierta y sin transferencia bancaria trazable.
- *Alternativa:* préstamo real informal.
- *Resuelve:* capacidad económica del prestamista, transferencia de origen,
  pagos posteriores y mutuo con fecha cierta. Es el punto más litigado en los
  casos del art. 70 LIR.

**S-17 Ingresos alegados como exentos o no renta sin acreditar**
- *Se ve:* se invocan herencias, indemnizaciones, ventas de bienes o
  devoluciones de capital sin documento (art. 71 LIR).
- *Resuelve:* documento constitutivo más trazabilidad bancaria del ingreso.

**S-18 Pago de deudas a un ritmo superior a los ingresos**
- *Se ve:* prepagos de créditos hipotecarios o de consumo que la renta no explica.
- *Resuelve:* certificados de prepago y origen de los fondos usados.

## D. Empresa y contabilidad

**S-19 Gastos personales cargados a la empresa**
- *Se ve:* supermercados, colegios, viajes familiares o vehículos registrados
  como gasto o crédito fiscal (relación con art. 97 N° 20 CT).
- *Alternativa:* gasto efectivamente vinculado al giro.
- *Resuelve:* necesidad del gasto para producir la renta y su beneficiario.

**S-20 Facturas falsas o de proveedores sin capacidad operativa**
- *Se ve:* proveedores sin trabajadores, activos ni domicilio real; facturas
  correlativas; pagos devueltos en efectivo.
- *Resuelve:* existencia material del servicio (guías, correos, entregables),
  situación tributaria del emisor y destino final del pago.

**S-21 Cuentas por cobrar o pagar a relacionados que no se mueven**
- *Se ve:* saldos con socios o relacionados que se arrastran años sin pago ni intereses.
- *Alternativa:* financiamiento de largo plazo pactado.
- *Resuelve:* contratos, actas y registros de las otras partes.

**S-22 Retiros de socios no registrados o inconsistentes con los registros tributarios**
- *Se ve:* los fondos salen de la empresa hacia el socio sin reflejo como
  retiro, dividendo o préstamo.
- *Resuelve:* conciliación entre libro mayor, cartola y registros RAI/REX/SAC (o
  el régimen que corresponda).

**S-23 Diferencias entre ventas declaradas (F29) y abonos bancarios**
- *Se ve:* los abonos de clientes exceden en forma persistente las ventas
  declaradas.
- *Alternativa:* préstamos, aportes, anticipos o cobros de períodos anteriores.
- *Resuelve:* conciliación mensual entre F29, libro de ventas y cartolas.

**S-24 Inventarios o activos fijos que no calzan**
- *Se ve:* el balance muestra existencias o activos sin respaldo físico ni
  documental, o que desaparecen sin venta registrada.
- *Resuelve:* toma de inventario y facturas de compra y venta.

**S-25 Contabilidad reconstruida o modificada tras el inicio de la fiscalización**
- *Se ve:* fechas de creación o modificación de archivos posteriores al
  requerimiento, o libros "reconstituidos".
- *Resuelve:* metadatos de los archivos, versiones previas y el aviso de
  pérdida de libros (art. 97 N° 16 CT).

## E. Operaciones y conducta

**S-26 Disminución de activos tras conocer un procedimiento**
- *Se ve:* ventas, donaciones o constitución de gravámenes poco después de
  una notificación del SII o de una querella (relación con art. 97 N° 27 CT).
- *Alternativa:* operación planificada antes del procedimiento o con
  justificación económica.
- *Resuelve:* fechas de promesas, negociaciones previas y destino del precio.

**S-27 Reorganizaciones sin razón de negocios aparente**
- *Se ve:* divisiones, fusiones o aportes cuyo único efecto visible es
  tributario (posible abuso o simulación, arts. 4 bis a 4 quinquies CT).
- *Alternativa:* razones de negocio documentadas.
- *Resuelve:* actas, informes previos, correos y planificación comercial.
- *Ojo:* aquí la carga de probar abuso o simulación es del SII (art. 4 bis inc. final CT).

**S-28 Uso de sociedades sin actividad real (cascarón)**
- *Se ve:* sociedades con capital mínimo, sin empleados, con flujos altos y
  domicilio compartido.
- *Resuelve:* actividad efectiva, contratos y beneficiario final.

**S-29 Operaciones con activos de difícil valoración**
- *Se ve:* compraventa de arte, joyas, criptoactivos, derechos sociales de
  sociedades cerradas o caballos de carrera, que permiten fijar precios arbitrarios.
- *Resuelve:* tasación, historial de la contraparte y trazabilidad del pago.

**S-30 Inconsistencias en el relato del contribuyente**
- *Se ve:* explicaciones que cambian entre la respuesta a la citación, el
  reclamo y la declaración judicial, o que contradicen los documentos.
- *Uso:* no es una señal financiera, pero orienta qué documento pedir. Compara
  siempre las versiones con fecha.
