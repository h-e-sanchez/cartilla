# Título: Duplicados y nombres inconsistentes
# Qué aprendes: normalizar texto ("norte", " Centro ", "SUR") y quitar filas repetidas.
# En Excel: ESPACIOS + NOMPROPIO, y Datos > Quitar duplicados.
# ---
import pandas as pd

df = pd.read_csv("data/dotacion_sucia.csv")

print("Antes:", sorted(df["sucursal"].unique()))
df["sucursal"] = df["sucursal"].str.strip().str.capitalize()
print("Después:", sorted(df["sucursal"].unique()))

print()
print("Filas:", len(df), "| duplicadas:", df.duplicated().sum())
df = df.drop_duplicates()
print("Filas tras limpiar:", len(df))

# Validación final: cada colaborador debe aparecer una sola vez.
assert df["id_colaborador"].is_unique
