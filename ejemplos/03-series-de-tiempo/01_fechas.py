# Título: Trabajar con fechas
# Qué aprendes: convertir una columna a fecha y sacar de ella el año, el mes y el día de la semana.
# En Excel: las funciones AÑO, MES y DIASEM.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_diarias.csv", parse_dates=["fecha"])

df["anio"] = df["fecha"].dt.year
df["mes"] = df["fecha"].dt.month
df["fin_de_semana"] = df["fecha"].dt.dayofweek >= 5  # 5 = sábado, 6 = domingo

print(df.head(4))
print()
print("Venta media diaria (fin de semana vs. semana):")
print(df.groupby("fin_de_semana")["monto"].mean().round(0))
