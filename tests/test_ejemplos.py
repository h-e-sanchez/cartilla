import json

import pytest

from herramientas import ejemplos

RUTAS = ejemplos.listar()


@pytest.mark.parametrize("ruta", RUTAS, ids=[r.stem for r in RUTAS])
def test_ejemplo_corre_y_coincide_con_su_salida(ruta):
    esperada = ejemplos.salida_esperada(ruta)
    assert esperada.exists(), f"falta {esperada.name}: corre python -m herramientas.ejemplos"
    assert ejemplos.ejecutar(ruta) == esperada.read_text(encoding="utf-8")


@pytest.mark.parametrize("ruta", RUTAS, ids=[r.stem for r in RUTAS])
def test_encabezado_completo(ruta):
    meta = ejemplos.leer_encabezado(ruta)
    assert set(meta) == {"titulo", "aprendes", "excel"}


def test_manifiesto_al_dia():
    guardado = json.loads((ejemplos.EJEMPLOS / "manifest.json").read_text(encoding="utf-8"))
    assert guardado == ejemplos.manifiesto(), "corre python -m herramientas.ejemplos"


def test_cada_modulo_tiene_ejemplos():
    for modulo in ejemplos.manifiesto()["modulos"]:
        assert modulo["ejemplos"], modulo["id"]
