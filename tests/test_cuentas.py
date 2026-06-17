"""Archivo: tests/test_cuentas.py
Descripcion: Pruebas basicas del modulo de cuentas de ahorro.
Autor: Martinez Steeven
Version: 1.0
"""

from tests.conftest import crear_cuenta_prueba, crear_socio_prueba


def test_crear_cuenta(cliente):
    """Verifica que la cuenta se cree con saldo cero y estado activo."""

    socio = crear_socio_prueba(cliente)
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    assert cuenta["numero_cuenta"].startswith("CTA-")
    assert cuenta["saldo"] == "0.00"
    assert cuenta["estado"] == "ACTIVA"

