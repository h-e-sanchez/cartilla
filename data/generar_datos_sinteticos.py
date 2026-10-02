"""Genera los CSV sintéticos de cartilla para "Comercial Ejemplo S.A.".

Reproducible (semilla fija): la misma semilla genera siempre los mismos
archivos, así los ejemplos del manual imprimen siempre la misma salida y los
tests pueden compararla. Ningún dato real de ningún empleador.

Archivos que genera (todos en formato tidy: una fila por observación):

- ventas_mensuales.csv  anio, mes, sucursal, linea, unidades, monto
- ventas_diarias.csv    fecha, sucursal, monto
- presupuesto.csv       anio, mes, centro_costo, cuenta, monto
- real.csv              anio, mes, centro_costo, cuenta, monto
- dotacion.csv          id_colaborador, sucursal, cargo, fecha_ingreso, sueldo_base
- dotacion_sucia.csv    la misma dotación con nulos, duplicados y nombres
                        inconsistentes, para el módulo de limpieza

Uso:
    python data/generar_datos_sinteticos.py
    python data/generar_datos_sinteticos.py --seed 42 --salida data
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEMILLA = 42

SUCURSALES = ["Norte", "Centro", "Sur"]
LINEAS = {"hogar": 18_000, "ferreteria": 25_000, "jardin": 12_000}  # precio medio
ANIOS_VENTAS = [2025, 2026]

CENTROS = {
    "Comercial": ["comisiones", "marketing"],
    "Operaciones": ["fletes", "mantencion"],
    "Personas": ["remuneraciones", "capacitacion"],
}
RANGO_PRESUPUESTO = (2_000_000, 9_000_000)
TASA_DESVIACION_GRANDE = 0.25  # se inyecta en 2 líneas para que el ejemplo tenga alertas

CARGOS = {"Vendedor": 750_000, "Bodeguero": 680_000, "Jefe de Tienda": 1_450_000, "Analista": 1_200_000}
DOTACION_POR_SUCURSAL = 12


def _estacionalidad(mes: int) -> float:
    """Diciembre alto, febrero bajo: una curva simple y creíble para retail."""
    return {2: 0.8, 9: 1.1, 11: 1.15, 12: 1.4}.get(mes, 1.0)


def generar_ventas_mensuales(rng: random.Random) -> list[dict]:
    filas = []
    for anio in ANIOS_VENTAS:
        crecimiento = 1.0 if anio == 2025 else 1.08
        for mes in range(1, 13):
            for sucursal in SUCURSALES:
                for linea, precio in LINEAS.items():
                    unidades = int(rng.randint(80, 160) * _estacionalidad(mes) * crecimiento)
                    monto = unidades * int(precio * rng.uniform(0.95, 1.05))
                    filas.append({"anio": anio, "mes": mes, "sucursal": sucursal,
                                  "linea": linea, "unidades": unidades, "monto": monto})
    return filas


def generar_ventas_diarias(rng: random.Random) -> list[dict]:
    filas = []
    dia = date(2025, 1, 1)
    while dia <= date(2026, 12, 31):
        factor = _estacionalidad(dia.month) * (1.3 if dia.weekday() >= 5 else 1.0)
        for sucursal in SUCURSALES:
            monto = int(rng.gauss(900_000, 120_000) * factor)
            filas.append({"fecha": dia.isoformat(), "sucursal": sucursal, "monto": max(monto, 0)})
        dia += timedelta(days=1)
    return filas


def generar_presupuesto_y_real(rng: random.Random) -> tuple[list[dict], list[dict]]:
    presupuesto, real = [], []
    lineas = [(cc, cuenta) for cc, cuentas in CENTROS.items() for cuenta in cuentas]
    con_desvio = set(rng.sample(lineas, 2))
    for mes in range(1, 13):
        for cc, cuenta in lineas:
            base = rng.randint(*RANGO_PRESUPUESTO) // 1000 * 1000
            factor = rng.uniform(0.95, 1.05)
            if (cc, cuenta) in con_desvio and mes >= 7:
                factor += TASA_DESVIACION_GRANDE
            presupuesto.append({"anio": 2026, "mes": mes, "centro_costo": cc, "cuenta": cuenta, "monto": base})
            real.append({"anio": 2026, "mes": mes, "centro_costo": cc, "cuenta": cuenta, "monto": int(base * factor)})
    return presupuesto, real


def generar_dotacion(rng: random.Random) -> list[dict]:
    filas = []
    n = 1
    for sucursal in SUCURSALES:
        for _ in range(DOTACION_POR_SUCURSAL):
            cargo = rng.choice(list(CARGOS))
            ingreso = date(2018, 1, 1) + timedelta(days=rng.randint(0, 3000))
            sueldo = int(CARGOS[cargo] * rng.uniform(0.9, 1.2)) // 1000 * 1000
            filas.append({"id_colaborador": f"C{n:03d}", "sucursal": sucursal, "cargo": cargo,
                          "fecha_ingreso": ingreso.isoformat(), "sueldo_base": sueldo})
            n += 1
    return filas


def ensuciar_dotacion(rng: random.Random, dotacion: list[dict]) -> list[dict]:
    """Copia de la dotación con los problemas típicos de un Excel real."""
    sucia = [dict(f) for f in dotacion]
    for fila in rng.sample(sucia, 4):
        fila["sueldo_base"] = ""  # nulos
    for fila in rng.sample(sucia, 5):
        fila["sucursal"] = rng.choice(["norte", " Centro ", "SUR"])  # nombres inconsistentes
    for fila in rng.sample(sucia, 3):
        d = date.fromisoformat(fila["fecha_ingreso"])
        fila["fecha_ingreso"] = d.strftime("%d/%m/%Y")  # formato de fecha mixto
    sucia.extend(dict(f) for f in rng.sample(sucia, 3))  # duplicados exactos
    return sucia


def escribir(ruta: Path, filas: list[dict]) -> None:
    with ruta.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def generar(salida: Path, seed: int = SEMILLA) -> list[Path]:
    rng = random.Random(seed)
    salida.mkdir(parents=True, exist_ok=True)
    presupuesto, real = generar_presupuesto_y_real(rng)
    dotacion = generar_dotacion(rng)
    archivos = {
        "ventas_mensuales.csv": generar_ventas_mensuales(rng),
        "ventas_diarias.csv": generar_ventas_diarias(rng),
        "presupuesto.csv": presupuesto,
        "real.csv": real,
        "dotacion.csv": dotacion,
        "dotacion_sucia.csv": ensuciar_dotacion(rng, dotacion),
    }
    rutas = []
    for nombre, filas in archivos.items():
        ruta = salida / nombre
        escribir(ruta, filas)
        rutas.append(ruta)
    return rutas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, default=SEMILLA)
    parser.add_argument("--salida", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    for ruta in generar(args.salida, args.seed):
        print(f"escrito {ruta}")


if __name__ == "__main__":
    main()
