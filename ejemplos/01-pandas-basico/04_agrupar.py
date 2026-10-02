# Título: Agrupar y resumir (tabla dinámica)
# Qué aprendes: sumar por categoría con groupby y armar una tabla cruzada con pivot_table.
# En Excel: Insertar > Tabla dinámica.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_mensuales.csv")

# Venta total por sucursal y año, en millones.
por_sucursal = df.groupby(["sucursal", "anio"])["monto"].sum() / 1e6
print(por_sucursal.round(1))
print()

# La misma idea como tabla cruzada: líneas en filas, años en columnas.
tabla = pd.pivot_table(df, values="monto", index="linea", columns="anio", aggfunc="sum") / 1e6
print(tabla.round(1))
