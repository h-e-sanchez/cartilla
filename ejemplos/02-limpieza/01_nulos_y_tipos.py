# Título: Nulos, tipos y fechas mixtas
# Qué aprendes: detectar celdas vacías, convertir texto a fecha y decidir qué hacer con los nulos.
# En Excel: Ir a especial > Celdas en blanco, y la función FECHANUMERO.
# ---
import pandas as pd

df = pd.read_csv("data/dotacion_sucia.csv")

print("Nulos por columna:")
print(df.isna().sum())

# Las fechas vienen en dos formatos (AAAA-MM-DD y DD/MM/AAAA). format="mixed" acepta ambos.
df["fecha_ingreso"] = pd.to_datetime(df["fecha_ingreso"], format="mixed", dayfirst=True)

# Un sueldo vacío no es cero: lo marcamos para revisarlo, no lo rellenamos a ciegas.
sin_sueldo = df[df["sueldo_base"].isna()]
print()
print("A revisar (sin sueldo):", ", ".join(sin_sueldo["id_colaborador"]))
