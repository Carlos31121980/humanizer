#!/usr/bin/env python3
"""Análisis de depósitos y detección automática de señales de alerta en movimientos.

Lee la hoja Movimientos del libro de trabajo y marca las señales S-01, S-02,
S-03, S-04, S-05, S-07, S-10 y S-11 del catálogo. Cada fila marcada conserva su
fuente_doc, ref y fila_excel para poder citarla.

Uso:
    python3 analisis_movimientos.py caso.xlsx --uf 39500 [opciones]

El umbral de fraccionamiento (S-03) es 450 UF por defecto. Indique --uf con el
valor de la UF del período o, si lo prefiere, --umbral directamente en pesos.
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import ajustar_columnas, leer_hoja, pesos  # noqa: E402

BENFORD = np.log10(1 + 1 / np.arange(1, 10))
COLS = ["fila_excel", "fecha", "cuenta", "descripcion", "abono", "cargo", "contraparte", "medio", "fuente_doc", "ref"]


def depositos(m, propias):
    ab = m[m["abono"] > 0].copy()
    ab["es_propia"] = ab["contraparte"].isin(propias) | ab["origen_identificado"].str.lower().eq("propia")
    ab["identificado"] = ~ab["es_propia"] & (ab["origen_identificado"] != "")
    ab["no_identificado"] = ~ab["es_propia"] & ~ab["identificado"]
    total = ab["abono"].sum()
    propia = ab[ab["es_propia"]]["abono"].sum()
    ident = ab[ab["identificado"]]["abono"].sum()
    resto = ab[ab["no_identificado"]]["abono"].sum()
    resumen = pd.DataFrame([
        ("Total abonos", total),
        ("− Traspasos entre cuentas propias", propia),
        ("− Abonos de origen identificado", ident),
        ("Resultado: abonos de origen NO identificado", resto),
    ], columns=["concepto", "monto"])
    por_origen = (ab[ab["identificado"]].groupby("origen_identificado")["abono"]
                  .agg(["count", "sum"]).reset_index().rename(columns={"count": "n", "sum": "monto"}))
    return resumen, por_origen, ab[ab["no_identificado"]][COLS]


def s03_fraccionamiento(m, umbral, ventana, piso, todos_medios):
    if not umbral:
        return pd.DataFrame()
    base = m[(m["abono"] > 0) & (m["abono"] < umbral) & (m["abono"] >= umbral * piso)]
    if not todos_medios:
        base = base[base["medio"] == "efectivo"]
    grupos, gid = [], 0
    for cuenta, g in base.sort_values("fecha").groupby("cuenta"):
        g = g.reset_index(drop=True)
        i = 0
        while i < len(g):
            j = i
            while j + 1 < len(g) and (g.loc[j + 1, "fecha"] - g.loc[i, "fecha"]).days <= ventana:
                j += 1
            bloque = g.loc[i:j]
            if len(bloque) >= 2 and bloque["abono"].sum() >= umbral:
                gid += 1
                grupos.append(bloque.assign(grupo=gid, suma_grupo=bloque["abono"].sum()))
                i = j + 1
            else:
                i += 1
    if not grupos:
        return pd.DataFrame()
    return pd.concat(grupos)[["grupo", "suma_grupo"] + COLS]


def s05_paso(m, dias, monto_min, tolerancia):
    filas = []
    for cuenta, g in m.sort_values("fecha").groupby("cuenta"):
        ab = g[(g["abono"] >= monto_min)]
        for _, r in ab.iterrows():
            sal = g[(g["cargo"] > 0) & (g["fecha"] >= r["fecha"]) & (g["fecha"] <= r["fecha"] + pd.Timedelta(days=dias))]
            if sal.empty:
                continue
            ratio = sal["cargo"].sum() / r["abono"]
            if ratio >= 1 - tolerancia:
                filas.append({**{c: r[c] for c in COLS}, "cargos_siguientes": sal["cargo"].sum(),
                              "ratio_salida": round(ratio, 2), "n_cargos": len(sal),
                              "destinos": "; ".join(sorted(set(sal["contraparte"]) - {""}))[:200]})
    return pd.DataFrame(filas)


def s07_concentracion(ab_terceros, top):
    if ab_terceros.empty:
        return pd.DataFrame()
    g = ab_terceros.assign(contraparte=ab_terceros["contraparte"].replace("", "(sin dato)")) \
        .groupby("contraparte")["abono"].agg(["count", "sum"]).sort_values("sum", ascending=False)
    g["participacion"] = (g["sum"] / g["sum"].sum()).round(4)
    g["acumulado"] = g["participacion"].cumsum().round(4)
    return g.head(top).reset_index().rename(columns={"count": "n", "sum": "monto"})


def s10_benford(m):
    montos = pd.concat([m["abono"], m["cargo"]])
    montos = montos[montos >= 10]
    n = len(montos)
    if n == 0:
        return pd.DataFrame(), None, n
    d = montos.astype("int64").astype(str).str[0].astype(int)
    obs = d.value_counts(normalize=True).reindex(range(1, 10), fill_value=0).values
    mad = float(np.mean(np.abs(obs - BENFORD)))
    tabla = pd.DataFrame({"digito": range(1, 10), "esperado": BENFORD.round(4),
                          "observado": obs.round(4), "diferencia": (obs - BENFORD).round(4)})
    return tabla, mad, n


def nivel_benford(mad):
    # Umbrales de conformidad de Nigrini para el primer dígito
    if mad <= 0.006:
        return "conformidad cercana"
    if mad <= 0.012:
        return "conformidad aceptable"
    if mad <= 0.015:
        return "conformidad marginal"
    return "no conformidad"


def s11_duplicados(m, dias):
    m = m.assign(monto=m["abono"] - m["cargo"]).sort_values("fecha")
    filas, gid = [], 0
    for _, g in m.groupby(["cuenta", "monto", "contraparte"]):
        if len(g) < 2:
            continue
        g = g.reset_index(drop=True)
        inicio = 0
        for k in range(1, len(g) + 1):
            if k == len(g) or (g.loc[k, "fecha"] - g.loc[k - 1, "fecha"]).days > dias:
                if k - inicio >= 2:
                    gid += 1
                    filas.append(g.loc[inicio:k - 1].assign(grupo=gid))
                inicio = k
    return pd.concat(filas)[["grupo"] + COLS] if filas else pd.DataFrame()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("libro")
    p.add_argument("--salida", default="resultado_movimientos.xlsx")
    p.add_argument("--uf", type=float, help="valor UF en pesos para calcular el umbral de 450 UF")
    p.add_argument("--umbral-uf", type=float, default=450, help="umbral en UF (por defecto 450)")
    p.add_argument("--umbral", type=float, help="umbral S-03 en pesos (reemplaza a --uf)")
    p.add_argument("--ventana-dias", type=int, default=7, help="ventana de agrupación S-03 (días)")
    p.add_argument("--piso", type=float, default=0.5, help="S-03: solo operaciones ≥ piso × umbral")
    p.add_argument("--todos-medios", action="store_true", help="S-03 sobre todos los medios, no solo efectivo")
    p.add_argument("--monto-alto", type=float, default=5_000_000, help="S-02: retiro en efectivo alto (pesos)")
    p.add_argument("--redondo", type=float, default=100_000, help="S-04: múltiplo considerado redondo")
    p.add_argument("--redondo-min", type=float, default=1_000_000, help="S-04: monto mínimo a considerar")
    p.add_argument("--paso-dias", type=int, default=3, help="S-05: días para salida de fondos")
    p.add_argument("--paso-min", type=float, default=5_000_000, help="S-05: abono mínimo a analizar")
    p.add_argument("--paso-tolerancia", type=float, default=0.10, help="S-05: salida ≥ (1 − tol) × abono")
    p.add_argument("--dup-dias", type=int, default=2, help="S-11: días entre posibles duplicados")
    p.add_argument("--cuentas-propias", default="", help="cuentas o RUT propios separados por coma")
    a = p.parse_args()

    m = leer_hoja(a.libro, "Movimientos")
    if m.empty:
        sys.exit("ERROR: la hoja Movimientos está vacía.")
    propias = {c.strip() for c in a.cuentas_propias.split(",") if c.strip()} | set(m["cuenta"].unique())
    umbral = a.umbral or (a.uf * a.umbral_uf if a.uf else None)

    dep_res, dep_origen, no_ident = depositos(m, propias)
    efectivo = m[m["medio"] == "efectivo"]
    s01 = efectivo[efectivo["abono"] > 0][COLS]
    s01_mes = (s01.assign(mes=s01["fecha"].dt.to_period("M").astype(str))
               .groupby(["cuenta", "mes"])["abono"].agg(["count", "sum"]).reset_index()
               .rename(columns={"count": "n", "sum": "monto"}))
    s02 = efectivo[efectivo["cargo"] >= a.monto_alto][COLS]
    s03 = s03_fraccionamiento(m, umbral, a.ventana_dias, a.piso, a.todos_medios)
    mon = m["abono"] + m["cargo"]
    s04 = m[(mon >= a.redondo_min) & (mon % a.redondo == 0)][COLS]
    s05 = s05_paso(m, a.paso_dias, a.paso_min, a.paso_tolerancia)
    terceros = m[(m["abono"] > 0) & ~m["contraparte"].isin(propias) & (m["origen_identificado"].str.lower() != "propia")]
    s07 = s07_concentracion(terceros, 15)
    s10, mad, n_benford = s10_benford(m)
    s11 = s11_duplicados(m, a.dup_dias)

    n_mont = int((mon >= a.redondo_min).sum())
    resumen = [
        ("Período", f"{m['fecha'].min():%d-%m-%Y} a {m['fecha'].max():%d-%m-%Y}"),
        ("Movimientos analizados", len(m)),
        ("Cuentas", ", ".join(sorted(m["cuenta"].unique()))),
        ("Abonos de origen no identificado", pesos(dep_res["monto"].iloc[3])),
        ("S-01 Depósitos en efectivo", f"{len(s01)} por {pesos(s01['abono'].sum())}"),
        ("S-02 Retiros en efectivo ≥ " + pesos(a.monto_alto), f"{len(s02)} por {pesos(s02['cargo'].sum())}"),
        ("S-03 Fraccionamiento (umbral " + (pesos(umbral) if umbral else "NO INDICADO: use --uf o --umbral") + ")",
         f"{s03['grupo'].nunique() if len(s03) else 0} grupo(s), {len(s03)} operaciones"),
        ("S-04 Montos redondos", f"{len(s04)} de {n_mont} movimientos ≥ {pesos(a.redondo_min)} "
                                 f"({(len(s04) / n_mont * 100 if n_mont else 0):.0f}%)"),
        ("S-05 Posible cuenta de paso", f"{len(s05)} abono(s)"),
        ("S-07 Mayor contraparte", f"{s07.iloc[0]['contraparte']} ({s07.iloc[0]['participacion']:.0%} de abonos de terceros)"
         if len(s07) else "sin datos"),
        ("S-10 Benford (MAD)", f"{mad:.4f}: {nivel_benford(mad)} (n={n_benford}"
                               + (", MUESTRA PEQUEÑA: no concluyente" if n_benford < 300 else "") + ")"
         if mad is not None else "sin datos"),
        ("S-11 Posibles duplicados", f"{s11['grupo'].nunique() if len(s11) else 0} grupo(s)"),
    ]
    res = pd.DataFrame(resumen, columns=["indicador", "resultado"])
    res.loc[len(res)] = ("Advertencia", "Indicadores automáticos: orientan la revisión, no prueban por sí solos. "
                                        "Cada hallazgo requiere explicación alternativa (ver catálogo).")

    with pd.ExcelWriter(a.salida, engine="openpyxl") as w:
        res.to_excel(w, sheet_name="Resumen", index=False)
        dep_res.to_excel(w, sheet_name="Depositos", index=False)
        dep_origen.to_excel(w, sheet_name="Depositos", index=False, startrow=len(dep_res) + 2)
        no_ident.to_excel(w, sheet_name="Abonos_no_identificados", index=False)
        for nombre, df in (("S01_efectivo", s01), ("S01_por_mes", s01_mes), ("S02_retiros_efectivo", s02),
                           ("S03_fraccionamiento", s03), ("S04_redondos", s04), ("S05_cuenta_paso", s05),
                           ("S07_contrapartes", s07), ("S10_benford", s10), ("S11_duplicados", s11)):
            (df if len(df) else pd.DataFrame({"resultado": ["sin hallazgos"]})).to_excel(w, sheet_name=nombre, index=False)
        ajustar_columnas(w)

    print("ANÁLISIS DE MOVIMIENTOS")
    for k, v in resumen:
        print(f"  {k}: {v}")
    print("\n  Depósitos:")
    for _, r in dep_res.iterrows():
        print(f"    {r['concepto']:<40}{pesos(r['monto']):>18}")
    print(f"\nDetalle en {a.salida}")


if __name__ == "__main__":
    main()
