# Título: Presupuesto vs. real con alertas
# Qué aprendes: calcular la desviación acumulada por línea y clasificarla con un umbral.
# En Excel: SUMAR.SI.CONJUNTO + formato condicional.
# ---
import pandas as pd

llaves = ["anio", "mes", "centro_costo", "cuenta"]
cruce = pd.read_csv("data/presupuesto.csv").merge(
    pd.read_csv("data/real.csv"), on=llaves, suffixes=("_ppto", "_real")
)

# Acumulado del año (YTD) por línea.
ytd = cruce.groupby(["centro_costo", "cuenta"])[["monto_ppto", "monto_real"]].sum()
ytd["desv_%"] = (ytd["monto_real"] / ytd["monto_ppto"] - 1) * 100

UMBRAL = 8  # % sobre el cual una línea pasa a alerta
ytd["estado"] = ytd["desv_%"].abs().gt(UMBRAL).map({True: "ALERTA", False: "ok"})

print(ytd.assign(**{"desv_%": ytd["desv_%"].round(1)})[["desv_%", "estado"]])
