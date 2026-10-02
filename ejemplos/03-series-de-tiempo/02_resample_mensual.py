# Título: De diario a mensual (resample)
# Qué aprendes: llevar una serie diaria a totales mensuales con resample.
# En Excel: tabla dinámica con la fecha agrupada por meses.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_diarias.csv", parse_dates=["fecha"])

# resample necesita la fecha como índice. "MS" = month start (inicio de mes).
mensual = df.set_index("fecha")["monto"].resample("MS").sum() / 1e6

print(mensual.head(6).round(1))
print("...")
print("Mes con más venta:", mensual.idxmax().strftime("%Y-%m"))
