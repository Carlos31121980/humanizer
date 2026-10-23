#!/usr/bin/env python3
"""Cuantificación de daños en contratos de obra pública, con escenarios de sensibilidad.

Lee un libro Excel con tres hojas:

  Hechos:  id, descripcion, clase, fecha_debio_actuar, fecha_actuo, fuente_doc, ref
           clase: mandante / fuerza_mayor / reaccion_mandante / contratista / concurrente
           (los días de demora se calculan como fecha_actuo − fecha_debio_actuar)
  Rubros:  codigo, rubro, hecho_id, base_calculo, cantidad, unidad, tasa, monto_directo,
           fecha_dano, firmeza, fuente_doc, ref
           monto = cantidad × tasa, salvo que se indique monto_directo
           firmeza: firme / discutible (documento sólido o estimación)
  Parametros (opcional): parametro, valor
           ipc_acumulado (factor de actualización a fecha del informe, p. ej. 1.12),
           fecha_informe

Escenarios:
  base         todo lo reclamado, salvo hechos de clase contratista
  conservador  solo hechos mandante / reaccion_mandante, rubros firmes, sin R-09 ni R-10
  minimo       solo R-05 (intereses por EP atrasados) y R-07 (multas indebidas) firmes

Uso:
    python3 cuantificacion_danos.py caso_obra.xlsx [--salida resultado_danos.xlsx]
"""

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import ajustar_columnas, pesos  # noqa: E402

CLASES = {"mandante", "fuerza_mayor", "reaccion_mandante", "contratista", "concurrente"}
IMPUTABLES = {"mandante", "reaccion_mandante"}
COLS_HECHOS = ["id", "descripcion", "clase", "fecha_debio_actuar", "fecha_actuo", "fuente_doc", "ref"]
COLS_RUBROS = ["codigo", "rubro", "hecho_id", "base_calculo", "cantidad", "unidad", "tasa",
               "monto_directo", "fecha_dano", "firmeza", "fuente_doc", "ref"]


def leer(ruta, hoja, cols, obligatoria=True):
    try:
        df = pd.read_excel(ruta, sheet_name=hoja)
    except ValueError:
        if obligatoria:
            sys.exit(f"ERROR: el libro no tiene la hoja '{hoja}'.")
        return pd.DataFrame(columns=cols)
    df.columns = [str(c).strip().lower() for c in df.columns]
    faltan = [c for c in cols if c not in df.columns]
    if faltan:
        sys.exit(f"ERROR: a la hoja '{hoja}' le faltan columnas: {', '.join(faltan)}")
    df = df.dropna(how="all").copy()
    df["fila_excel"] = df.index + 2
    for c in df.columns:
        if c.startswith("fecha"):
            df[c] = pd.to_datetime(df[c], dayfirst=True, errors="coerce")
        elif c in ("cantidad", "tasa", "monto_directo"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        elif df[c].dtype == object:
            df[c] = df[c].fillna("").astype(str).str.strip()
    return df


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("libro")
    p.add_argument("--salida", default="resultado_danos.xlsx")
    a = p.parse_args()

    h = leer(a.libro, "Hechos", COLS_HECHOS)
    r = leer(a.libro, "Rubros", COLS_RUBROS)
    par = leer(a.libro, "Parametros", ["parametro", "valor"], obligatoria=False)
    params = dict(zip(par["parametro"].str.lower(), par["valor"])) if len(par) else {}
    factor = float(params.get("ipc_acumulado", 1.0) or 1.0)

    av = []
    h["clase"] = h["clase"].str.lower()
    for _, x in h[~h["clase"].isin(CLASES)].iterrows():
        av.append(("Hechos", x["fila_excel"], f"clase '{x['clase']}' no reconocida; se trata como 'contratista' (no se cobra)."))
    h.loc[~h["clase"].isin(CLASES), "clase"] = "contratista"
    h["dias_demora"] = (h["fecha_actuo"] - h["fecha_debio_actuar"]).dt.days
    for _, x in h[h["dias_demora"].isna()].iterrows():
        av.append(("Hechos", x["fila_excel"], "Falta fecha_debio_actuar o fecha_actuo: no se calculan días de demora."))
    for _, x in h[h["fuente_doc"] == ""].iterrows():
        av.append(("Hechos", x["fila_excel"], "Hecho sin fuente_doc: no puede sostenerse en juicio."))
    for _, x in h[h["clase"] == "fuerza_mayor"].iterrows():
        av.append(("Hechos", x["fila_excel"], "Fuerza mayor: da plazo, no indemnización. Los rubros ligados a este hecho "
                   "se incluyen solo en el escenario base y deben justificarse en las bases o el contrato."))
    for _, x in h[h["clase"] == "concurrente"].iterrows():
        av.append(("Hechos", x["fila_excel"], "Atraso concurrente: documente el análisis de retraso que separa la porción del mandante."))

    r["firmeza"] = r["firmeza"].str.lower()
    r["monto"] = r["monto_directo"].where(r["monto_directo"].notna(), r["cantidad"] * r["tasa"])
    for _, x in r[r["monto"].isna()].iterrows():
        av.append(("Rubros", x["fila_excel"], "Sin monto: indique cantidad y tasa, o monto_directo."))
    r["monto"] = r["monto"].fillna(0)
    for _, x in r[r["fuente_doc"] == ""].iterrows():
        av.append(("Rubros", x["fila_excel"], "Rubro sin fuente_doc."))
    for _, x in r[~r["firmeza"].isin(["firme", "discutible"])].iterrows():
        av.append(("Rubros", x["fila_excel"], f"firmeza '{x['firmeza']}' no reconocida; se trata como 'discutible'."))
    r.loc[~r["firmeza"].isin(["firme", "discutible"]), "firmeza"] = "discutible"
    r = r.merge(h[["id", "clase", "dias_demora"]], left_on="hecho_id", right_on="id", how="left").drop(columns=["id"])
    for _, x in r[r["clase"].isna()].iterrows():
        av.append(("Rubros", x["fila_excel"], f"hecho_id '{x['hecho_id']}' no existe en Hechos: rubro excluido de todos los escenarios."))
    r["clase"] = r["clase"].fillna("sin_hecho")
    r["monto_actualizado"] = r["monto"] * factor

    esc = {
        "base": (r["clase"] != "contratista") & (r["clase"] != "sin_hecho"),
        "conservador": r["clase"].isin(IMPUTABLES) & (r["firmeza"] == "firme") & ~r["codigo"].isin(["R-09", "R-10"]),
        "minimo": r["clase"].isin(IMPUTABLES) & (r["firmeza"] == "firme") & r["codigo"].isin(["R-05", "R-07"]),
    }
    for nombre, mask in esc.items():
        r[f"en_{nombre}"] = mask

    por_rubro = r.groupby(["codigo", "rubro"]).agg(
        n=("monto", "size"), monto=("monto", "sum"), actualizado=("monto_actualizado", "sum"),
        base=("monto_actualizado", lambda s: s[r.loc[s.index, "en_base"]].sum()),
        conservador=("monto_actualizado", lambda s: s[r.loc[s.index, "en_conservador"]].sum()),
        minimo=("monto_actualizado", lambda s: s[r.loc[s.index, "en_minimo"]].sum()),
    ).reset_index()
    tot = {k: r.loc[r[f"en_{k}"], "monto_actualizado"].sum() for k in esc}
    resumen = pd.DataFrame([
        ("Factor de actualización aplicado", factor),
        ("Escenario BASE (todo lo reclamable)", tot["base"]),
        ("Escenario CONSERVADOR (imputable al mandante, firme, sin lucro cesante)", tot["conservador"]),
        ("Escenario MÍNIMO (solo intereses por EP y multas indebidas)", tot["minimo"]),
        ("Excluido: rubros de hechos del contratista", r.loc[r["clase"] == "contratista", "monto_actualizado"].sum()),
        ("Excluido: rubros sin hecho asociado", r.loc[r["clase"] == "sin_hecho", "monto_actualizado"].sum()),
        ("En riesgo: rubros ligados a fuerza mayor", r.loc[r["clase"] == "fuerza_mayor", "monto_actualizado"].sum()),
    ], columns=["concepto", "valor"])

    cadena = r[["codigo", "rubro", "hecho_id", "clase", "dias_demora", "base_calculo", "cantidad", "unidad", "tasa",
                "monto", "monto_actualizado", "firmeza", "fuente_doc", "ref", "en_base", "en_conservador", "en_minimo"]]
    hechos_out = h[["id", "descripcion", "clase", "fecha_debio_actuar", "fecha_actuo", "dias_demora", "fuente_doc", "ref"]]

    with pd.ExcelWriter(a.salida, engine="openpyxl") as w:
        resumen.to_excel(w, sheet_name="Resumen", index=False)
        por_rubro.to_excel(w, sheet_name="Por_rubro", index=False)
        cadena.to_excel(w, sheet_name="Cadena_causal", index=False)
        hechos_out.to_excel(w, sheet_name="Hechos", index=False)
        pd.DataFrame(av, columns=["hoja", "fila_excel", "advertencia"]).to_excel(w, sheet_name="Advertencias", index=False)
        ajustar_columnas(w)

    print("CUANTIFICACIÓN DE DAÑOS CONTRACTUALES")
    print(f"  Hechos: {len(h)} ({', '.join(f'{k}: {v}' for k, v in h['clase'].value_counts().items())})")
    imp = h[h["clase"].isin(IMPUTABLES)]["dias_demora"].sum()
    print(f"  Días de demora acumulados imputables al mandante: {int(imp) if pd.notna(imp) else 0}")
    print(f"  Factor de actualización: {factor}")
    print(f"\n  {'Rubro':<52}{'Base':>16}{'Conserv.':>16}{'Mínimo':>16}")
    for _, x in por_rubro.iterrows():
        print(f"  {x['codigo']} {x['rubro'][:46]:<48}{pesos(x['base']):>16}{pesos(x['conservador']):>16}{pesos(x['minimo']):>16}")
    print(f"  {'TOTAL':<52}{pesos(tot['base']):>16}{pesos(tot['conservador']):>16}{pesos(tot['minimo']):>16}")
    print(f"\n{len(av)} advertencia(s). Detalle en {a.salida}")


if __name__ == "__main__":
    main()
