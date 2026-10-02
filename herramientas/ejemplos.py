"""Fuente única de los ejemplos: lee los .py de ejemplos/, los ejecuta y arma el manifiesto.

La página (app.js) y los tests leen exactamente los mismos archivos, así el código
mostrado y el código probado nunca divergen.

Uso:
    python -m herramientas.ejemplos     # regenera ejemplos/manifest.json y las *.out.txt
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EJEMPLOS = RAIZ / "ejemplos"
DATOS = RAIZ / "data"

MODULOS = {
    "01-pandas-basico": {
        "titulo": "pandas básico",
        "descripcion": "Importar, inspeccionar, filtrar, agrupar, unir y exportar: el 80% del trabajo diario.",
    },
    "02-limpieza": {
        "titulo": "Limpieza y calidad de datos",
        "descripcion": "Nulos, fechas mixtas, duplicados y nombres inconsistentes, como llegan del Excel real.",
    },
    "03-series-de-tiempo": {
        "titulo": "Series de tiempo",
        "descripcion": "Fechas, resample mensual, promedio móvil, variación anual y presupuesto vs. real.",
    },
    "04-automatizacion-reportes": {
        "titulo": "Automatización de reportes",
        "descripcion": "Excel con varias hojas generado por código y funciones que se prueban solas.",
    },
}

CAMPOS = {"Título": "titulo", "Qué aprendes": "aprendes", "En Excel": "excel"}
SEPARADOR = "# ---"


def listar() -> list[Path]:
    return sorted(EJEMPLOS.glob("*/*.py"))


def leer_encabezado(ruta: Path) -> dict:
    """Lee las líneas '# Campo: valor' hasta el separador '# ---'."""
    meta = {}
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if linea.strip() == SEPARADOR:
            return meta
        for etiqueta, clave in CAMPOS.items():
            prefijo = f"# {etiqueta}:"
            if linea.startswith(prefijo):
                meta[clave] = linea[len(prefijo):].strip()
    raise ValueError(f"{ruta.name}: falta el separador '{SEPARADOR}'")


def ejecutar(ruta: Path) -> str:
    """Corre el ejemplo en una carpeta temporal con una copia de data/ y devuelve su salida."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(DATOS, Path(tmp) / "data", ignore=shutil.ignore_patterns("*.py"))
        res = subprocess.run(
            [sys.executable, str(ruta)], cwd=tmp, capture_output=True, text=True,
            encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"}, check=False,
        )
    if res.returncode != 0:
        raise RuntimeError(f"{ruta.name} falló:\n{res.stderr}")
    return res.stdout


def salida_esperada(ruta: Path) -> Path:
    return ruta.with_suffix(".out.txt")


def manifiesto() -> dict:
    modulos = []
    for carpeta, info in MODULOS.items():
        ejemplos = []
        for ruta in sorted((EJEMPLOS / carpeta).glob("*.py")):
            ejemplos.append({"archivo": f"{carpeta}/{ruta.name}", "id": ruta.stem, **leer_encabezado(ruta)})
        modulos.append({"id": carpeta, **info, "ejemplos": ejemplos})
    datos = sorted(p.name for p in DATOS.glob("*.csv"))
    return {"datos": datos, "modulos": modulos}


def main() -> None:
    (EJEMPLOS / "manifest.json").write_text(
        json.dumps(manifiesto(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    for ruta in listar():
        salida_esperada(ruta).write_text(ejecutar(ruta), encoding="utf-8", newline="\n")
        print(f"ok {ruta.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
