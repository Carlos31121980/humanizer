#!/usr/bin/env python3
"""Genera un caso ficticio de obra pública (caso_obra_demo.xlsx) para probar cuantificacion_danos.py.

Todos los datos son inventados.
"""

import os
import sys

import pandas as pd

salida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "caso_obra_demo.xlsx")

hechos = pd.DataFrame([
    ("H1", "Cuarentena comunal: paralización de faenas", "fuerza_mayor", "20-03-2020", "15-06-2020", "Res. Ex. MINSAL / libro de obra fs. 40-52", ""),
    ("H2", "SERVIU demora resolución de aumento de plazo por pandemia (solicitada 20-06-2020)", "reaccion_mandante", "20-07-2020", "05-11-2020", "Oficio ingreso N° 1234; Res. Ex. N° 998", "art. X bases: 30 días"),
    ("H3", "Estado de pago N° 7 pagado fuera de plazo", "mandante", "15-10-2020", "28-12-2020", "EP7, comprobante de pago", "bases: pago a 30 días"),
    ("H4", "Estado de pago N° 9 pagado fuera de plazo", "mandante", "15-02-2021", "30-04-2021", "EP9, comprobante de pago", ""),
    ("H5", "Recepción provisoria: observaciones contradictorias entre 1ª y 2ª visita", "mandante", "10-06-2021", "25-10-2021", "Actas de recepción 10-06-2021 y 25-10-2021", ""),
    ("H6", "Atraso en subcontrato de instalaciones eléctricas", "contratista", "01-03-2021", "15-04-2021", "libro de obra fs. 120", ""),
], columns=["id", "descripcion", "clase", "fecha_debio_actuar", "fecha_actuo", "fuente_doc", "ref"])

rubros = pd.DataFrame([
    ("R-01", "Mayores gastos generales por extensión de plazo", "H2", "GG mensuales efectivos × meses", 3.5, "mes", 18_000_000, None, "01-11-2020", "firme", "mayor contable obra 2020", ""),
    ("R-01", "Mayores gastos generales por extensión de plazo", "H5", "GG mensuales efectivos × meses", 4.5, "mes", 18_000_000, None, "01-10-2021", "firme", "mayor contable obra 2021", ""),
    ("R-01", "Mayores gastos generales por extensión de plazo", "H1", "GG mensuales × meses de cuarentena", 2.9, "mes", 18_000_000, None, "01-06-2020", "discutible", "mayor contable obra 2020", ""),
    ("R-02", "Equipos ociosos (grúa torre arrendada)", "H1", "días × tarifa arriendo", 87, "día", 350_000, None, "01-06-2020", "firme", "contrato arriendo grúa; facturas", ""),
    ("R-04", "Costo financiero línea de crédito para sostener obra", "H3", "intereses pagados período", None, None, None, 4_200_000, "31-12-2020", "discutible", "cartola línea de crédito", ""),
    ("R-05", "Intereses por EP N° 7 atrasado", "H3", "monto EP × tasa diaria × días", 74, "día", 95_000, None, "28-12-2020", "firme", "EP7; bases art. pago", ""),
    ("R-05", "Intereses por EP N° 9 atrasado", "H4", "monto EP × tasa diaria × días", 74, "día", 110_000, None, "30-04-2021", "firme", "EP9; bases art. pago", ""),
    ("R-07", "Multa por atraso cursada pese a prórroga pendiente", "H2", "monto descontado en EP 8", None, None, None, 12_500_000, "15-12-2020", "firme", "Res. multa N° 45; EP8", ""),
    ("R-08", "Trabajos rehechos por observaciones contradictorias", "H5", "facturas subcontrato terminaciones", None, None, None, 9_800_000, "30-09-2021", "firme", "facturas 1021-1030", ""),
    ("R-08", "Guardia y mantención hasta recepción", "H5", "meses × costo mensual", 4.5, "mes", 1_400_000, None, "01-10-2021", "firme", "facturas empresa de guardias", ""),
    ("R-09", "Lucro cesante: licitación no presentada por capacidad comprometida", "H5", "utilidad esperada obra X", None, None, None, 60_000_000, "01-08-2021", "discutible", "bases licitación X; carta gerencia", ""),
    ("R-02", "Horas extra por atraso subcontrato eléctrico", "H6", "horas × tarifa", 400, "hora", 9_000, None, "15-04-2021", "firme", "planillas", ""),
], columns=["codigo", "rubro", "hecho_id", "base_calculo", "cantidad", "unidad", "tasa", "monto_directo", "fecha_dano", "firmeza", "fuente_doc", "ref"])

parametros = pd.DataFrame([("ipc_acumulado", 1.18), ("fecha_informe", "30-09-2026")], columns=["parametro", "valor"])

with pd.ExcelWriter(salida, engine="openpyxl") as w:
    hechos.to_excel(w, sheet_name="Hechos", index=False)
    rubros.to_excel(w, sheet_name="Rubros", index=False)
    parametros.to_excel(w, sheet_name="Parametros", index=False)
print(f"Caso demo de obra creado: {salida}")
