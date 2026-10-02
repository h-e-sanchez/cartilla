# Título: Exportar el resultado
# Qué aprendes: guardar un DataFrame como CSV listo para Excel o Power BI.
# En Excel: Archivo > Guardar como > CSV UTF-8.
# ---
import pandas as pd

df = pd.read_csv("data/ventas_mensuales.csv")
resumen = df.groupby("sucursal", as_index=False)[["unidades", "monto"]].sum()

# sep=";" y decimal="," hacen que el Excel en español lo abra en columnas.
resumen.to_csv("resumen_sucursal.csv", index=False, sep=";", decimal=",")

# "with" abre el archivo y lo cierra solo al terminar el bloque.
with open("resumen_sucursal.csv", encoding="utf-8") as archivo:
    print(archivo.read())
