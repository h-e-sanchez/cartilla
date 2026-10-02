# Título: Unir dos tablas (BUSCARV)
# Qué aprendes: cruzar presupuesto y real por sus columnas comunes con merge.
# En Excel: BUSCARV o BUSCARX, pero para todas las filas a la vez.
# ---
import pandas as pd

ppto = pd.read_csv("data/presupuesto.csv")
real = pd.read_csv("data/real.csv")

llaves = ["anio", "mes", "centro_costo", "cuenta"]
cruce = ppto.merge(real, on=llaves, how="outer", suffixes=("_ppto", "_real"))
cruce = cruce.sort_values(llaves, ignore_index=True)  # orden explícito: no depender de la versión de pandas

# how="outer" conserva las filas que estén en una sola tabla: nada desaparece en silencio.
print(cruce.head())
print("Filas sin pareja:", cruce.isna().any(axis=1).sum())
