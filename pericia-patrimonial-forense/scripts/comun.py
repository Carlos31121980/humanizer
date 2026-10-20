"""Definiciones compartidas del libro de trabajo forense."""

import sys

import pandas as pd

HOJAS = {
    "Movimientos": [
        "fecha", "cuenta", "descripcion", "abono", "cargo", "saldo",
        "contraparte", "medio", "origen_identificado", "fuente_doc", "ref",
    ],
    "Patrimonio": [
        "fecha_corte", "tipo", "categoria", "descripcion", "valor",
        "criterio_valor", "fuente_doc", "ref",
    ],
    "Ingresos": [
        "fecha", "concepto", "clasificacion", "monto", "acreditado",
        "fuente_doc", "ref",
    ],
    "Gastos": ["fecha", "concepto", "monto", "fuente_doc", "ref"],
}

DESCRIPCIONES = {
    "Movimientos": {
        "medio": "efectivo / transferencia / cheque / tarjeta / otro",
        "origen_identificado": "vacío si no se conoce; si se conoce: sueldo, venta, prestamo, propia, rescate...",
        "contraparte": "RUT o nombre; para traspasos propios use el número de la otra cuenta",
    },
    "Patrimonio": {
        "fecha_corte": "misma fecha para todos los ítems de un corte (p. ej. 31-12-2021)",
        "tipo": "activo / pasivo",
        "categoria": "inmueble, vehiculo, cuenta, inversion, derechos_sociales, efectivo, credito_hipotecario...",
        "criterio_valor": "costo / avaluo_fiscal / mercado (use el mismo en todos los cortes)",
    },
    "Ingresos": {
        "clasificacion": "renta_afecta / exenta / no_renta / prestamo / aporte / otro",
        "acreditado": "si / no (¿hay documento que lo pruebe?)",
    },
    "Gastos": {"concepto": "gastos de vida y desembolsos que no generan activo"},
}


def leer_hoja(ruta, hoja, obligatoria=True):
    """Lee una hoja del libro y normaliza fechas, montos y textos."""
    try:
        df = pd.read_excel(ruta, sheet_name=hoja)
    except ValueError:
        if obligatoria:
            sys.exit(f"ERROR: el libro {ruta} no tiene la hoja '{hoja}'.")
        return pd.DataFrame(columns=HOJAS[hoja])
    df.columns = [str(c).strip().lower() for c in df.columns]
    faltan = [c for c in HOJAS[hoja] if c not in df.columns]
    if faltan:
        sys.exit(f"ERROR: a la hoja '{hoja}' le faltan columnas: {', '.join(faltan)}")
    df = df.dropna(how="all").copy()
    for col in ("fecha", "fecha_corte"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            malas = df[df[col].isna()]
            if len(malas):
                filas = ", ".join(str(i + 2) for i in malas.index[:10])
                sys.exit(f"ERROR: fechas ilegibles en '{hoja}', filas Excel: {filas}")
    for col in ("abono", "cargo", "saldo", "valor", "monto"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    for col in ("tipo", "medio", "clasificacion", "acreditado", "criterio_valor"):
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip().str.lower()
    for col in ("cuenta", "contraparte", "origen_identificado", "fuente_doc", "ref", "descripcion"):
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()
    df["fila_excel"] = df.index + 2
    return df


def pesos(x):
    """Formatea un monto como pesos chilenos: $1.234.567."""
    signo = "-" if x < 0 else ""
    return f"{signo}${abs(round(x)):,.0f}".replace(",", ".")


def ajustar_columnas(writer):
    """Ensancha las columnas de todas las hojas escritas con openpyxl."""
    for hoja in writer.book.worksheets:
        for col in hoja.columns:
            largo = max((len(str(c.value)) for c in col if c.value is not None), default=8)
            hoja.column_dimensions[col[0].column_letter].width = min(max(10, largo + 2), 60)
