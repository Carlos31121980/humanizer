# Pericia Patrimonial Forense: skill para Claude Code

Skill para el análisis financiero forense en litigio, en Chile. Dos módulos:
- **A. Origen de fondos:** litigio tributario (SII y TTA) y penal económico
  (delitos tributarios y lavado de activos).
- **B. Daños contractuales:** perjuicios de un contratista contra un mandante
  público (SERVIU, MOP, municipios) por atrasos y demoras administrativas.

## Contenido
| Archivo | Para qué sirve |
|---|---|
| `SKILL.md` | Instrucciones de la skill: reglas, flujo de trabajo en 7 pasos (0 a 6) y entregables |
| `referencias/senales-de-alerta.md` | Catálogo de 30 señales de alerta con su explicación alternativa y la prueba que la resuelve |
| `referencias/metodos.md` | Patrimonio neto comparado, fuentes y usos, depósitos bancarios, trazabilidad y conciliación |
| `referencias/marco-normativo.md` | Normas de la LIR, el CT, la Ley 19.913 y la Ley 21.595, indicando cuáles están verificadas |
| `referencias/danos-contractuales.md` | Módulo B: clasificación de hechos, análisis de retraso, 10 rubros de daño, sensibilidad y marco normativo |
| `referencias/respaldo-metodologico.md` | Fuentes reconocidas de cada método (IRS, ACFE, Holland v. US, Nigrini, UAF, SCL Protocol, AACE, AICPA SSFS 1, NIST) y texto sugerido para la sección Metodología del informe |
| `referencias/ingesta-documentos.md` | Cómo leer PDF, Word, Excel y escaneados, y los controles de integridad |
| `referencias/plantilla-informe.md` | Estructura del informe pericial y de la minuta interna de estrategia |
| `scripts/inventario_evidencia.py` | Inventario de archivos con hash SHA-256 (cadena de custodia) |
| `scripts/crear_libro_trabajo.py` | Crea el libro Excel de trabajo con sus columnas |
| `scripts/patrimonio_neto.py` | Patrimonio neto comparado y estado de fuentes y usos, con cuadratura automática |
| `scripts/analisis_movimientos.py` | Análisis de depósitos y señales S-01, 02, 03, 04, 05, 07, 10 y 11 |
| `scripts/cuantificacion_danos.py` | Módulo B: cuantificación por rubro con escenarios base, conservador y mínimo |
| `ejemplos/generar_caso_demo.py` | Caso ficticio del módulo A con señales sembradas |
| `ejemplos/generar_caso_obra_demo.py` | Caso ficticio del módulo B (obra SERVIU con pandemia, EP atrasados y recepción conflictiva) |

## Instalación
Copie la carpeta a `~/.claude/skills/pericia-patrimonial-forense/` (para uso
personal) o a `.claude/skills/` dentro de un proyecto. Los scripts requieren
Python 3.10 o superior, `pandas` y `openpyxl`.

## Prueba rápida
```bash
python3 ejemplos/generar_caso_demo.py /tmp/caso_demo.xlsx
python3 scripts/patrimonio_neto.py /tmp/caso_demo.xlsx --salida /tmp/res_pat.xlsx
python3 scripts/analisis_movimientos.py /tmp/caso_demo.xlsx --uf 39500 --salida /tmp/res_mov.xlsx
python3 ejemplos/generar_caso_obra_demo.py /tmp/caso_obra.xlsx
python3 scripts/cuantificacion_danos.py /tmp/caso_obra.xlsx --salida /tmp/res_danos.xlsx
```

## Historial de versiones
- **0.3.0**: respaldo metodológico. Cada método queda vinculado a su fuente
  reconocida, verificada el 23-10-2026, y el informe cita el método, no la
  herramienta.
- **0.2.0**: módulo B de daños contractuales en obra pública. Separa desde el
  inicio los hechos de fuerza mayor (dan plazo, no indemnización) de la
  reacción del mandante frente a ellos (sí imputable), porque mezclarlos es el
  ataque más fácil de la contraparte. Tres escenarios de sensibilidad.
- **0.1.0**: versión inicial. Las normas tributarias citadas se verificaron
  contra el texto vigente (corpus al 17-04-2026). Las de la Ley 19.913 y la Ley
  21.595 quedan marcadas como pendientes de verificar.
