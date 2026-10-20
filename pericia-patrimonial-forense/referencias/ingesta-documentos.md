# Ingesta de documentos

## Por formato

| Formato | Cómo leerlo | Cuidados |
|---|---|---|
| PDF nativo (cartolas, F22 y F29 descargados del SII) | Skill `pdf` (extracción de texto y tablas) | Verifica que las sumas de la tabla extraída calcen con los totales impresos de la cartola. |
| PDF escaneado o foto | Skill `pdf` con OCR | El OCR confunde 1/7, 5/S y 0/O. Cuadra siempre contra el saldo inicial y final. Marca las cifras con la fuente `OCR`. |
| Word (.docx): contratos, mutuos, declaraciones | Skill `docx` | Revisa los metadatos (autor, fecha de creación y modificación) cuando la fecha cierta importe. |
| Excel o CSV: cartolas exportadas, mayores, planillas del cliente | Skill `xlsx` o pandas | Las planillas del cliente **no son prueba por sí mismas**: son su versión. Contrástalas con el documento primario. Revisa fórmulas ocultas, filas filtradas y hojas ocultas. |
| Correos (.eml, .msg) o capturas de WhatsApp | Lectura directa | Útiles para fechas e intención. Anota los encabezados y el remitente. |

## Control de integridad
1. `python3 scripts/inventario_evidencia.py <carpeta> --salida inventario.csv`
   antes de abrir nada.
2. Nunca edites los originales. Trabaja en una carpeta `trabajo/`.
3. En cada cartola, comprueba que saldo inicial + abonos − cargos = saldo final.
   Si no cuadra, hay movimientos faltantes o un error de extracción.
4. Comprueba la **continuidad**: el saldo final de un mes debe ser el saldo
   inicial del siguiente. Los saltos indican cartolas faltantes.

## Columnas mínimas por movimiento
`fecha, cuenta, descripcion, abono, cargo, saldo, contraparte, medio
(efectivo/transferencia/cheque/tarjeta/otro), fuente_doc, ref`
