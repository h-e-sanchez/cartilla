# Título: Filtrar filas y elegir columnas
# Qué aprendes: quedarte solo con las filas que cumplen una condición.
# En Excel: Autofiltro, o la función FILTRAR.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_mensuales.csv")

# Cada condición va entre paréntesis; & significa "y", | significa "o".
diciembre_sur = df[(df["mes"] == 12) & (df["sucursal"] == "Sur")]

print(diciembre_sur[["anio", "linea", "unidades", "monto"]])
