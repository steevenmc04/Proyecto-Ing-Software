"""Archivo: tests/test_socios.py
Descripcion: Pruebas basicas del modulo de socios.
Autor: Martinez Steeven
Version: 1.0
"""

from tests.conftest import crear_socio_prueba


def test_crear_socio(cliente):
    """Verifica que se pueda crear un socio con numero generado."""

    socio = crear_socio_prueba(cliente)
    assert socio["id"] > 0
    assert socio["numero_socio"].startswith("SOC-")
    assert socio["estado"] == "ACTIVO"

