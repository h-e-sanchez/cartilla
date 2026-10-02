import csv
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("generador", RAIZ / "data" / "generar_datos_sinteticos.py")
generador = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(generador)


def test_misma_semilla_mismos_archivos(tmp_path):
    a = generador.generar(tmp_path / "a")
    b = generador.generar(tmp_path / "b")
    for ra, rb in zip(a, b):
        assert ra.read_bytes() == rb.read_bytes(), ra.name


def test_datos_versionados_coinciden_con_el_generador(tmp_path):
    for ruta in generador.generar(tmp_path):
        assert ruta.read_bytes() == (RAIZ / "data" / ruta.name).read_bytes(), ruta.name


def test_columnas_en_snake_case(tmp_path):
    for ruta in generador.generar(tmp_path):
        with ruta.open(encoding="utf-8") as f:
            for col in next(csv.reader(f)):
                assert col == col.lower() and " " not in col, (ruta.name, col)


def test_dotacion_sucia_tiene_los_problemas_que_ensena(tmp_path):
    generador.generar(tmp_path)
    with (tmp_path / "dotacion_sucia.csv").open(encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    assert any(f["sueldo_base"] == "" for f in filas)
    assert len(filas) > len({f["id_colaborador"] for f in filas})
    assert any("/" in f["fecha_ingreso"] for f in filas)
