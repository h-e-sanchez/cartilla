# Título: Importar un CSV a un DataFrame
# Qué aprendes: leer un archivo con pd.read_csv y mirar sus primeras filas.
# En Excel: Datos > Obtener datos > Desde texto/CSV.
# ---
import pandas as pd

# Un DataFrame (df) es una tabla: filas, columnas con nombre y un tipo por columna.
df = pd.read_csv("data/ventas_mensuales.csv")

print(df.head())  # las 5 primeras filas
print("Filas y columnas:", df.shape)
