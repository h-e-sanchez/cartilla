# Título: Reporte Excel con varias hojas
# Qué aprendes: escribir varias tablas en un mismo .xlsx, una por hoja.
# En Excel: copiar y pegar cada tabla en su hoja, todos los meses, a mano.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_mensuales.csv")

hojas = {
    "por_sucursal": df.groupby("sucursal", as_index=False)["monto"].sum(),
    "por_linea": df.groupby("linea", as_index=False)["monto"].sum(),
    "detalle_2026": df[df["anio"] == 2026],
}

with pd.ExcelWriter("reporte_ventas.xlsx") as excel:
    for nombre, tabla in hojas.items():
        tabla.to_excel(excel, sheet_name=nombre, index=False)

# Verificamos leyendo el archivo de vuelta.
libro = pd.read_excel("reporte_ventas.xlsx", sheet_name=None)
for nombre, tabla in libro.items():
    print(f"{nombre}: {len(tabla)} filas")
