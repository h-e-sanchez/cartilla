# Título: Convertir el reporte en una función con prueba
# Qué aprendes: empaquetar un cálculo en una función y verificarlo con assert (la idea de pytest).
# En Excel: una plantilla que se copia cada mes, pero que además se revisa sola.
# ---
import pandas as pd


def desviacion_ytd(ppto: pd.DataFrame, real: pd.DataFrame, umbral: float = 8) -> pd.DataFrame:
    """Desviación acumulada por centro de costo, con estado según el umbral (%)."""
    llaves = ["anio", "mes", "centro_costo", "cuenta"]
    cruce = ppto.merge(real, on=llaves, suffixes=("_ppto", "_real"))
    out = cruce.groupby("centro_costo")[["monto_ppto", "monto_real"]].sum()
    out["desv_%"] = ((out["monto_real"] / out["monto_ppto"] - 1) * 100).round(1)
    out["alerta"] = out["desv_%"].abs() > umbral
    return out


# Prueba con datos inventados donde sabemos la respuesta: 110 vs. 100 = +10%.
mini = pd.DataFrame({"anio": [2026], "mes": [1], "centro_costo": ["X"], "cuenta": ["y"], "monto": [100]})
prueba = desviacion_ytd(mini, mini.assign(monto=110))
assert prueba.loc["X", "desv_%"] == 10.0 and prueba.loc["X", "alerta"]
print("Prueba OK")

# Con la prueba pasada, la usamos sobre los datos reales del ejemplo.
print(desviacion_ytd(pd.read_csv("data/presupuesto.csv"), pd.read_csv("data/real.csv")))
