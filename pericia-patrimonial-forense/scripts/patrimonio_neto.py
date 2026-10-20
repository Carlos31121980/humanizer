#!/usr/bin/env python3
"""Método de patrimonio neto comparado y estado de fuentes y usos de fondos.

Lee las hojas Patrimonio, Ingresos y Gastos del libro de trabajo. Cada par de
fechas de corte consecutivas define un período (c0, c1]: los ingresos y gastos
con fecha posterior a c0 y hasta c1 inclusive se imputan a ese período.

    Variación PN + Gastos = Usos de fondos
    Usos − Ingresos acreditados = Diferencia no justificada

Uso:
    python3 patrimonio_neto.py caso.xlsx [--salida resultado_patrimonio.xlsx]
"""

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import ajustar_columnas, leer_hoja, pesos  # noqa: E402


def advertencias(pat, ing, gas, cortes):
    av = []
    for nombre, df in (("Patrimonio", pat), ("Ingresos", ing), ("Gastos", gas)):
        sin = df[df["fuente_doc"] == ""]
        for _, r in sin.iterrows():
            av.append((nombre, r["fila_excel"], "Cifra sin fuente_doc: no puede usarse en el informe sin respaldo."))
    malos = pat[~pat["tipo"].isin(["activo", "pasivo"])]
    for _, r in malos.iterrows():
        av.append(("Patrimonio", r["fila_excel"], f"tipo '{r['tipo']}' no es 'activo' ni 'pasivo': fila ignorada."))
    criterios = pat[pat["descripcion"] != ""].groupby("descripcion")["criterio_valor"].nunique()
    for desc in criterios[criterios > 1].index:
        av.append(("Patrimonio", "-", f"'{desc}' se valoriza con criterios distintos entre cortes: "
                   "la variación puede reflejar plusvalía y no flujo de fondos."))
    presentes = pat.groupby("descripcion")["fecha_corte"].apply(set)
    for desc, fechas in presentes.items():
        if desc and len(fechas) < len(cortes):
            faltan = [c.strftime("%d-%m-%Y") for c in cortes if c not in fechas]
            av.append(("Patrimonio", "-", f"'{desc}' no figura en los cortes {', '.join(faltan)}: "
                       "confirme si se adquirió o enajenó (y el precio) o si falta el dato."))
    for nombre, df in (("Ingresos", ing), ("Gastos", gas)):
        fuera = df[(df["fecha"] <= cortes[0]) | (df["fecha"] > cortes[-1])]
        for _, r in fuera.iterrows():
            av.append((nombre, r["fila_excel"], "Fecha fuera de los períodos definidos por los cortes: no se imputa."))
    noacr = ing[~ing["acreditado"].isin(["si", "sí", "no"])]
    for _, r in noacr.iterrows():
        av.append(("Ingresos", r["fila_excel"], f"acreditado='{r['acreditado']}': se trata como NO acreditado."))
    return pd.DataFrame(av, columns=["hoja", "fila_excel", "advertencia"])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("libro")
    p.add_argument("--salida", default="resultado_patrimonio.xlsx")
    a = p.parse_args()

    pat = leer_hoja(a.libro, "Patrimonio")
    ing = leer_hoja(a.libro, "Ingresos", obligatoria=False)
    gas = leer_hoja(a.libro, "Gastos", obligatoria=False)

    cortes = sorted(pat["fecha_corte"].unique())
    if len(cortes) < 2:
        sys.exit("ERROR: se necesitan al menos dos fechas de corte en la hoja Patrimonio.")
    cortes = [pd.Timestamp(c) for c in cortes]

    av = advertencias(pat, ing, gas, cortes)
    pat = pat[pat["tipo"].isin(["activo", "pasivo"])].copy()
    pat["signo"] = pat["tipo"].map({"activo": 1, "pasivo": -1})
    ing["es_acreditado"] = ing["acreditado"].isin(["si", "sí"])

    # Patrimonio por corte y categoría
    por_cat = pat.pivot_table(index=["tipo", "categoria"], columns="fecha_corte", values="valor",
                              aggfunc="sum", fill_value=0)
    pn = {c: (pat[pat["fecha_corte"] == c]["valor"] * pat[pat["fecha_corte"] == c]["signo"]).sum() for c in cortes}

    resumen, fu = [], []
    for c0, c1 in zip(cortes, cortes[1:]):
        periodo = f"{c0:%d-%m-%Y} a {c1:%d-%m-%Y}"
        en = lambda df: df[(df["fecha"] > c0) & (df["fecha"] <= c1)]  # noqa: E731
        i_per, g_per = en(ing), en(gas)
        gastos = g_per["monto"].sum()
        acr = i_per[i_per["es_acreditado"]]["monto"].sum()
        noacr = i_per[~i_per["es_acreditado"]]["monto"].sum()
        var = pn[c1] - pn[c0]
        usos = var + gastos
        resumen.append({
            "periodo": periodo,
            "PN_inicial": pn[c0], "PN_final": pn[c1], "variacion_PN": var,
            "gastos_vida_y_desembolsos": gastos, "usos_de_fondos": usos,
            "ingresos_acreditados": acr,
            "diferencia_no_justificada": usos - acr,
            "ingresos_alegados_no_acreditados": noacr,
            "diferencia_si_se_acreditaran_todos": usos - acr - noacr,
        })

        # Fuentes y usos: variación de cada categoría + ingresos + gastos
        for (tipo, cat), fila in por_cat.iterrows():
            d = fila.get(c1, 0) - fila.get(c0, 0)
            if d == 0:
                continue
            if tipo == "activo":
                lado, concepto = ("uso", f"Aumento de {cat}") if d > 0 else ("fuente", f"Disminución de {cat}")
            else:
                lado, concepto = ("fuente", f"Aumento de pasivo: {cat}") if d > 0 else ("uso", f"Pago/disminución de pasivo: {cat}")
            fu.append({"periodo": periodo, "lado": lado, "concepto": concepto, "monto": abs(d)})
        for cl, m in i_per[i_per["es_acreditado"]].groupby("clasificacion")["monto"].sum().items():
            fu.append({"periodo": periodo, "lado": "fuente", "concepto": f"Ingreso acreditado: {cl}", "monto": m})
        if gastos:
            fu.append({"periodo": periodo, "lado": "uso", "concepto": "Gastos de vida y desembolsos", "monto": gastos})

    res = pd.DataFrame(resumen)
    tot = res.drop(columns=["periodo", "PN_inicial", "PN_final"]).sum()
    tot["periodo"], tot["PN_inicial"], tot["PN_final"] = "ACUMULADO", res["PN_inicial"].iloc[0], res["PN_final"].iloc[-1]
    res = pd.concat([res, tot.to_frame().T], ignore_index=True)

    fu = pd.DataFrame(fu, columns=["periodo", "lado", "concepto", "monto"])
    cierre = []
    # Control: usos − fuentes debe igualar la diferencia no justificada de cada período
    for _, r in res.iloc[:-1].iterrows():
        f = fu[fu["periodo"] == r["periodo"]]
        neto = f[f["lado"] == "uso"]["monto"].sum() - f[f["lado"] == "fuente"]["monto"].sum()
        if abs(neto - r["diferencia_no_justificada"]) > 1:
            sys.exit(f"ERROR de cuadratura en {r['periodo']}: fuentes y usos ({neto}) "
                     f"≠ diferencia ({r['diferencia_no_justificada']}). Revise los datos.")
        cierre.append({"periodo": r["periodo"], "lado": "fuente", "monto": neto,
                       "concepto": "DIFERENCIA NO JUSTIFICADA (cuadra usos y fuentes)"})
    fu = fu.sort_values(["periodo", "lado", "monto"], ascending=[True, False, False])
    fu = pd.concat([fu, pd.DataFrame(cierre)]).sort_values("periodo", kind="stable")

    por_cat.columns = [f"{c:%d-%m-%Y}" for c in por_cat.columns]
    por_cat = por_cat.reset_index()

    with pd.ExcelWriter(a.salida, engine="openpyxl") as w:
        res.to_excel(w, sheet_name="Resumen", index=False)
        fu.to_excel(w, sheet_name="Fuentes_Usos", index=False)
        por_cat.to_excel(w, sheet_name="Patrimonio_por_corte", index=False)
        av.to_excel(w, sheet_name="Advertencias", index=False)
        ajustar_columnas(w)

    print("MÉTODO DE PATRIMONIO NETO COMPARADO")
    for _, r in res.iterrows():
        print(f"\n{r['periodo']}")
        print(f"  Variación de patrimonio neto      {pesos(r['variacion_PN']):>18}")
        print(f"  + Gastos de vida y desembolsos    {pesos(r['gastos_vida_y_desembolsos']):>18}")
        print(f"  = Usos de fondos                  {pesos(r['usos_de_fondos']):>18}")
        print(f"  − Ingresos acreditados            {pesos(r['ingresos_acreditados']):>18}")
        print(f"  = DIFERENCIA NO JUSTIFICADA       {pesos(r['diferencia_no_justificada']):>18}")
        if r["ingresos_alegados_no_acreditados"]:
            print(f"    (alegados sin acreditar: {pesos(r['ingresos_alegados_no_acreditados'])}; "
                  f"si se acreditaran, diferencia = {pesos(r['diferencia_si_se_acreditaran_todos'])})")
    print(f"\n{len(av)} advertencia(s). Detalle en {a.salida}")


if __name__ == "__main__":
    main()
