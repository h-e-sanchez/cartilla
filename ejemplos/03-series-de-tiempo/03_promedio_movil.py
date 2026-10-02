# Título: Promedio móvil
# Qué aprendes: suavizar el ruido diario con una ventana de 7 días (rolling).
# En Excel: PROMEDIO sobre un rango que se desplaza fila a fila.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_diarias.csv", parse_dates=["fecha"])
total = df.groupby("fecha")["monto"].sum() / 1e6  # las 3 sucursales juntas

suave = total.rolling(window=7).mean()  # los 6 primeros días quedan vacíos (NaN)

tabla = pd.DataFrame({"diario": total, "movil_7d": suave}).round(2)
print(tabla.iloc[5:12])
