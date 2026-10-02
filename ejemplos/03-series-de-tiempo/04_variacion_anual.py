# Título: Variación contra el año anterior (YoY)
# Qué aprendes: comparar cada mes con el mismo mes del año anterior.
# En Excel: (valor 2026 / valor 2025) - 1, columna por columna.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_mensuales.csv")

tabla = df.pivot_table(values="monto", index="mes", columns="anio", aggfunc="sum")
tabla["var_yoy_%"] = (tabla[2026] / tabla[2025] - 1) * 100

print((tabla[[2025, 2026]] / 1e6).round(1).join(tabla["var_yoy_%"].round(1)))
