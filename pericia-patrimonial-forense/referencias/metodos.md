# Métodos de reconstrucción

## 1. Patrimonio neto comparado

Es el método que mejor dialoga con los arts. 70 y 71 LIR, porque mide si los
desembolsos e inversiones del período tienen un origen acreditado.

```
Patrimonio neto (PN) = Activos − Pasivos        (a cada fecha de corte)

Variación PN del período    = PN final − PN inicial
+ Gastos de vida y desembolsos que no generan activo
= Uso total de fondos (aplicaciones)

− Ingresos acreditados del período
  (renta afecta + rentas exentas + ingresos no renta + préstamos/aportes acreditados)
= DIFERENCIA NO JUSTIFICADA   (si es positiva)
```

**Reglas de aplicación**
- Usa el **mismo criterio de valorización** al inicio y al final. Si un
  inmueble se valoriza a costo al inicio y a mercado al final, la plusvalía
  aparece como "incremento" sin que haya habido flujo de fondos. Por defecto,
  valoriza a costo histórico de adquisición.
- El **PN inicial** debe ser tan sólido como el final. Un patrimonio inicial
  subestimado (efectivo acumulado no documentado, el llamado "colchón") es la
  defensa clásica y la más atacada. Documenta qué prueba lo sostiene.
- Separa los **préstamos**: aumentan activos y pasivos a la vez, así que no
  generan diferencia. Una deuda inexistente en el pasivo, en cambio, sí la
  genera, y es un punto frecuente de controversia.
- Trabaja **año comercial por año comercial** y también en el acumulado, porque
  el SII cita por períodos y la prescripción (art. 200 CT) corre por período.
- Si se comparan montos de años distintos, indica si están en pesos nominales o
  reajustados, y con qué índice.

**Script:** `python3 scripts/patrimonio_neto.py caso.xlsx --salida resultado.xlsx`

## 2. Fuentes y usos de fondos

Es la misma ecuación presentada como flujo: **fuentes** (ingresos, préstamos
recibidos, ventas de activos) frente a **usos** (compras de activos, pago de
deudas, gastos de vida, aumento de saldos). Sirve para explicar la diferencia
al tribunal en una sola tabla. El script la genera en la hoja `Fuentes_Usos`.

## 3. Análisis de depósitos bancarios

1. Suma todos los abonos del período en todas las cuentas.
2. Resta las transferencias entre cuentas propias (si no, se cuentan dos veces).
3. Resta los abonos de origen identificado y acreditado: sueldo, ventas
   facturadas, préstamos documentados, rescates de inversiones.
4. El remanente son los **abonos de origen no identificado**, que se analizan
   uno por uno o por patrón.

**Script:** `python3 scripts/analisis_movimientos.py caso.xlsx`. Marca las
transferencias propias si la columna `contraparte` coincide con una cuenta de
la lista `--cuentas-propias`.

## 4. Trazabilidad de fondos (tracing)

Sigue un monto específico desde su origen hasta su destino final. Es el
corazón del análisis de lavado de activos.
- Cuando el dinero se mezcla en una cuenta con fondos lícitos, declara el
  criterio que usas para asignarlo (FIFO, LIFO, prorrata o "saldo mínimo
  intermedio") y por qué. El resultado cambia según el criterio, y la
  contraparte lo va a atacar.
- Presenta la cadena como diagrama: cuenta, fecha, monto y documento en cada eslabón.

## 5. Conciliación tributaria-bancaria

Compara mes a mes el F29 (débito y crédito) y el libro de ventas con los abonos
bancarios de clientes, y el F22 con el patrimonio y los retiros. Las
diferencias persistentes del mismo signo son más significativas que una
diferencia aislada.

## Materialidad

Define al inicio un umbral bajo el cual no se investigan diferencias
individualmente (por ejemplo, 1% de los abonos anuales o un monto fijo
acordado con el abogado) y decláralo en el informe.
