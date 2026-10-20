#!/usr/bin/env python3
"""Crea un libro de trabajo Excel vacío con las hojas y columnas que usan los scripts.

Uso:
    python3 crear_libro_trabajo.py caso.xlsx
"""

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import DESCRIPCIONES, HOJAS, ajustar_columnas  # noqa: E402


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("salida", help="ruta del .xlsx a crear")
    p.add_argument("--sobrescribir", action="store_true", help="reemplaza el archivo si existe")
    a = p.parse_args()

    if os.path.exists(a.salida) and not a.sobrescribir:
        sys.exit(f"ERROR: {a.salida} ya existe. Use --sobrescribir para reemplazarlo.")

    filas = []
    for hoja, cols in HOJAS.items():
        for c in cols:
            filas.append({"hoja": hoja, "columna": c, "descripcion": DESCRIPCIONES.get(hoja, {}).get(c, "")})
    filas.append({"hoja": "(todas)", "columna": "fuente_doc / ref",
                  "descripcion": "archivo de origen y página, folio o fila. Obligatorio para toda cifra."})

    with pd.ExcelWriter(a.salida, engine="openpyxl") as w:
        pd.DataFrame(filas).to_excel(w, sheet_name="Instrucciones", index=False)
        for hoja, cols in HOJAS.items():
            pd.DataFrame(columns=cols).to_excel(w, sheet_name=hoja, index=False)
        ajustar_columnas(w)
    print(f"Libro creado: {a.salida}")


if __name__ == "__main__":
    main()
