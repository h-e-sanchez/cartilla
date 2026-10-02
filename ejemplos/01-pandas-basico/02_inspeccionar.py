# Título: Inspeccionar tipos y resumen
# Qué aprendes: revisar los tipos de cada columna y un resumen estadístico rápido.
# En Excel: Formato de celdas + las funciones CONTAR, PROMEDIO, MIN y MAX.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_mensuales.csv")

print(df.dtypes)  # int64 = entero, object = texto
print()
print(df[["unidades", "monto"]].describe().round(0))  # conteo, media, desviación, mín, máx
