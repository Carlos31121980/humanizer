#!/usr/bin/env python3
"""Genera un caso ficticio (caso_demo.xlsx) con señales sembradas para probar los scripts.

Todos los nombres, RUT y cifras son inventados.
"""

import os
import random
import sys

import pandas as pd

random.seed(7)
salida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "caso_demo.xlsx")
C1, C2 = "BCO-001-CC", "BCO-002-CC"
mov = []


def m(fecha, cuenta, desc, abono=0, cargo=0, contra="", medio="transferencia", origen="", doc="cartola", ref=""):
    mov.append(dict(fecha=fecha, cuenta=cuenta, descripcion=desc, abono=abono, cargo=cargo, saldo=None,
                    contraparte=contra, medio=medio, origen_identificado=origen,
                    fuente_doc=f"{doc}_{cuenta}_{fecha[3:5]}-{fecha[6:]}.pdf", ref=ref or "p. 1"))


# Sueldo y gastos corrientes 2022-2023
for anio in (2022, 2023):
    for mes in range(1, 13):
        m(f"05-{mes:02d}-{anio}", C1, "Remuneración", abono=2_850_000, contra="76.111.111-1", origen="sueldo")
        for _ in range(8):
            m(f"{random.randint(6, 28):02d}-{mes:02d}-{anio}", C1, "Compra tarjeta débito",
              cargo=random.randint(8_000, 480_000), contra="comercio", medio="tarjeta")
# S-03: depósitos en efectivo bajo 450 UF (~17,7 MM con UF 39.500) en pocos días
for d, monto in ((10, 15_900_000), (12, 16_200_000), (14, 14_800_000)):
    m(f"{d:02d}-03-2023", C2, "Depósito en efectivo", abono=monto, medio="efectivo")
# S-05: cuenta de paso
m("02-06-2023", C2, "Transferencia recibida", abono=40_000_000, contra="77.222.222-2")
m("03-06-2023", C2, "Transferencia enviada", cargo=24_000_000, contra="Inversiones Delta SpA")
m("04-06-2023", C2, "Transferencia enviada", cargo=15_500_000, contra="12.345.678-9")
# S-02: retiro alto en efectivo
m("20-08-2023", C1, "Giro por caja", cargo=9_000_000, medio="efectivo")
# Traspaso propio y préstamo "familiar" redondo
m("15-09-2023", C1, "Traspaso desde cuenta propia", abono=5_000_000, contra=C2)
m("15-09-2023", C2, "Traspaso a cuenta propia", cargo=5_000_000, contra=C1)
m("01-10-2023", C1, "Transferencia recibida", abono=20_000_000, contra="9.876.543-2")
# S-11: duplicado
m("10-11-2023", C1, "Pago proveedor", cargo=1_250_000, contra="Servicios Omega Ltda")
m("11-11-2023", C1, "Pago proveedor", cargo=1_250_000, contra="Servicios Omega Ltda")

movs = pd.DataFrame(mov)
movs["fecha"] = pd.to_datetime(movs["fecha"], dayfirst=True)
movs = movs.sort_values(["cuenta", "fecha"]).reset_index(drop=True)
movs["saldo"] = (movs["abono"] - movs["cargo"]).groupby(movs["cuenta"]).cumsum() + 10_000_000

pat = pd.DataFrame([
    # corte, tipo, categoria, descripcion, valor, criterio, fuente
    ("31-12-2021", "activo", "cuenta", "Saldo BCO-001", 10_000_000, "costo", "cartola_dic_2021.pdf"),
    ("31-12-2021", "activo", "cuenta", "Saldo BCO-002", 10_000_000, "costo", "cartola_dic_2021.pdf"),
    ("31-12-2021", "activo", "vehiculo", "Automóvil PPU AB-1234", 12_000_000, "costo", "factura_auto.pdf"),
    ("31-12-2021", "pasivo", "credito_consumo", "Crédito consumo Banco", 6_000_000, "costo", "cert_deuda_2021.pdf"),
    ("31-12-2022", "activo", "cuenta", "Saldo BCO-001", 14_000_000, "costo", "cartola_dic_2022.pdf"),
    ("31-12-2022", "activo", "cuenta", "Saldo BCO-002", 10_000_000, "costo", "cartola_dic_2022.pdf"),
    ("31-12-2022", "activo", "vehiculo", "Automóvil PPU AB-1234", 12_000_000, "costo", "factura_auto.pdf"),
    ("31-12-2022", "pasivo", "credito_consumo", "Crédito consumo Banco", 3_000_000, "costo", "cert_deuda_2022.pdf"),
    ("31-12-2023", "activo", "cuenta", "Saldo BCO-001", 18_000_000, "costo", "cartola_dic_2023.pdf"),
    ("31-12-2023", "activo", "cuenta", "Saldo BCO-002", 12_000_000, "costo", "cartola_dic_2023.pdf"),
    ("31-12-2023", "activo", "vehiculo", "Automóvil PPU AB-1234", 12_000_000, "costo", "factura_auto.pdf"),
    ("31-12-2023", "activo", "inmueble", "Depto. Rol 1234-56", 95_000_000, "costo", "escritura_compraventa.pdf"),
    ("31-12-2023", "pasivo", "credito_hipotecario", "Mutuo hipotecario", 40_000_000, "costo", "escritura_compraventa.pdf"),
], columns=["fecha_corte", "tipo", "categoria", "descripcion", "valor", "criterio_valor", "fuente_doc"])
pat["ref"] = ""

ing = pd.DataFrame([
    ("31-12-2022", "Remuneraciones 2022", "renta_afecta", 34_200_000, "si", "certificado_sueldos_2022.pdf"),
    ("31-12-2023", "Remuneraciones 2023", "renta_afecta", 34_200_000, "si", "certificado_sueldos_2023.pdf"),
    ("01-10-2023", "Préstamo de hermano", "prestamo", 20_000_000, "no", "declaracion_contribuyente.docx"),
    ("15-05-2023", "Venta de caballo de carrera", "no_renta", 15_000_000, "no", ""),
], columns=["fecha", "concepto", "clasificacion", "monto", "acreditado", "fuente_doc"])
ing["ref"] = ""

gas = pd.DataFrame([
    ("31-12-2022", "Gastos de vida 2022 (tarjetas y débito)", 22_000_000, "cartolas_2022"),
    ("31-12-2023", "Gastos de vida 2023 (tarjetas y débito)", 23_500_000, "cartolas_2023"),
    ("30-06-2023", "Impuestos y gastos de escrituración depto.", 3_000_000, "escritura_compraventa.pdf"),
], columns=["fecha", "concepto", "monto", "fuente_doc"])
gas["ref"] = ""

with pd.ExcelWriter(salida, engine="openpyxl") as w:
    movs.assign(fecha=movs["fecha"].dt.strftime("%d-%m-%Y")).to_excel(w, sheet_name="Movimientos", index=False)
    pat.to_excel(w, sheet_name="Patrimonio", index=False)
    ing.to_excel(w, sheet_name="Ingresos", index=False)
    gas.to_excel(w, sheet_name="Gastos", index=False)
print(f"Caso demo creado: {salida}")
