#!/usr/bin/env python3
"""Inventario con hash SHA-256 de todos los archivos de una carpeta de evidencia.

Ejecútelo ANTES de abrir o convertir los documentos: el hash permite demostrar
después que el archivo analizado es el mismo que se recibió.

Uso:
    python3 inventario_evidencia.py <carpeta> [--salida inventario.csv]
"""

import argparse
import csv
import datetime as dt
import hashlib
import os
import sys

TIPOS = {
    ".pdf": "pdf", ".doc": "word", ".docx": "word", ".rtf": "word", ".odt": "word",
    ".xls": "excel", ".xlsx": "excel", ".xlsm": "excel", ".csv": "csv", ".ods": "excel",
    ".jpg": "imagen", ".jpeg": "imagen", ".png": "imagen", ".tif": "imagen", ".tiff": "imagen", ".heic": "imagen",
    ".eml": "correo", ".msg": "correo", ".txt": "texto", ".xml": "xml", ".zip": "comprimido", ".rar": "comprimido",
}


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("carpeta")
    p.add_argument("--salida", default="inventario.csv")
    a = p.parse_args()

    if not os.path.isdir(a.carpeta):
        sys.exit(f"ERROR: {a.carpeta} no es una carpeta.")
    salida_abs = os.path.abspath(a.salida)

    filas = []
    for raiz, _, archivos in os.walk(a.carpeta):
        for nombre in sorted(archivos):
            ruta = os.path.join(raiz, nombre)
            if os.path.abspath(ruta) == salida_abs or nombre.startswith("~$"):
                continue
            st = os.stat(ruta)
            ext = os.path.splitext(nombre)[1].lower()
            filas.append({
                "n": 0,
                "ruta": os.path.relpath(ruta, a.carpeta),
                "tipo": TIPOS.get(ext, "otro"),
                "bytes": st.st_size,
                "modificado": dt.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                "sha256": sha256(ruta),
            })
    filas.sort(key=lambda r: r["ruta"])
    for i, r in enumerate(filas, 1):
        r["n"] = i

    with open(a.salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["n", "ruta", "tipo", "bytes", "modificado", "sha256"])
        w.writeheader()
        w.writerows(filas)

    conteo = {}
    for r in filas:
        conteo[r["tipo"]] = conteo.get(r["tipo"], 0) + 1
    resumen = ", ".join(f"{k}: {v}" for k, v in sorted(conteo.items()))
    print(f"{len(filas)} archivos inventariados en {a.salida} ({resumen})")
    print(f"Generado: {dt.datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
