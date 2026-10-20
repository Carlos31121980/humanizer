# Pericia Patrimonial Forense: skill para Claude Code

Skill para el análisis financiero forense y patrimonial en litigio tributario
(SII y TTA) y penal económico (delitos tributarios y lavado de activos), en Chile.

## Contenido
| Archivo | Para qué sirve |
|---|---|
| `SKILL.md` | Instrucciones de la skill: reglas, flujo de trabajo en 7 pasos (0 a 6) y entregables |
| `referencias/senales-de-alerta.md` | Catálogo de 30 señales de alerta con su explicación alternativa y la prueba que la resuelve |
| `referencias/metodos.md` | Patrimonio neto comparado, fuentes y usos, depósitos bancarios, trazabilidad y conciliación |
| `referencias/marco-normativo.md` | Normas de la LIR, el CT, la Ley 19.913 y la Ley 21.595, indicando cuáles están verificadas |
| `referencias/ingesta-documentos.md` | Cómo leer PDF, Word, Excel y escaneados, y los controles de integridad |
| `referencias/plantilla-informe.md` | Estructura del informe pericial y de la minuta interna de estrategia |
| `scripts/inventario_evidencia.py` | Inventario de archivos con hash SHA-256 (cadena de custodia) |
| `scripts/crear_libro_trabajo.py` | Crea el libro Excel de trabajo con sus columnas |
| `scripts/patrimonio_neto.py` | Patrimonio neto comparado y estado de fuentes y usos, con cuadratura automática |
| `scripts/analisis_movimientos.py` | Análisis de depósitos y señales S-01, 02, 03, 04, 05, 07, 10 y 11 |
| `ejemplos/generar_caso_demo.py` | Caso ficticio con señales sembradas para probar los scripts |

## Instalación
Copie la carpeta a `~/.claude/skills/pericia-patrimonial-forense/` (para uso
personal) o a `.claude/skills/` dentro de un proyecto. Los scripts requieren
Python 3.10 o superior, `pandas` y `openpyxl`.

## Prueba rápida
```bash
python3 ejemplos/generar_caso_demo.py /tmp/caso_demo.xlsx
python3 scripts/patrimonio_neto.py /tmp/caso_demo.xlsx --salida /tmp/res_pat.xlsx
python3 scripts/analisis_movimientos.py /tmp/caso_demo.xlsx --uf 39500 --salida /tmp/res_mov.xlsx
```

## Historial de versiones
- **0.1.0**: versión inicial. Las normas tributarias citadas se verificaron
  contra el texto vigente (corpus al 17-04-2026). Las de la Ley 19.913 y la Ley
  21.595 quedan marcadas como pendientes de verificar.
