"""Archivo: tests/unit/test_cuentas.py
Descripcion: Pruebas unitarias para el modulo de cuentas de ahorro.
"""

from tests.conftest import crear_socio_prueba, crear_cuenta_prueba

def test_crear_cuenta_ahorro(cliente):
    """Verifica la creacion de cuenta de ahorros para un socio."""
    socio = crear_socio_prueba(cliente)
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    assert cuenta["id"] > 0
    assert cuenta["numero_cuenta"].startswith("CTA-")
    assert cuenta["saldo"] == "0.00"
    assert cuenta["estado"] == "ACTIVA"

def test_crear_cuenta_socio_inexistente(cliente):
    """Verifica error al crear cuenta para socio inexistente."""
    respuesta = cliente.post("/api/v1/cuentas", json={"socio_id": 9999})
    assert respuesta.status_code == 404
    assert "no encontrado" in respuesta.json()["detail"].lower() or "no existe" in respuesta.json()["detail"].lower()

def test_obtener_cuentas_socio(cliente):
    """Verifica la obtencion de cuentas asociadas a un socio."""
    socio = crear_socio_prueba(cliente, cedula="1111111111")
    crear_cuenta_prueba(cliente, socio["id"])
    respuesta = cliente.get(f"/api/v1/cuentas/socio/{socio['id']}")
    assert respuesta.status_code == 200
    cuentas = respuesta.json()
    assert isinstance(cuentas, list)
    assert len(cuentas) == 1
    assert cuentas[0]["socio_id"] == socio["id"]
