"""Archivo: tests/test_transacciones.py
Descripcion: Pruebas basicas de depositos, retiros y API externa.
Autor: Martinez Steeven
Version: 1.0
"""

from tests.conftest import crear_cuenta_prueba, crear_socio_prueba


def test_registrar_deposito(cliente):
    """Verifica que un deposito aumente el saldo y genere comprobante."""

    socio = crear_socio_prueba(cliente)
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    respuesta = cliente.post("/api/v1/transacciones/deposito", json={"cuenta_id": cuenta["id"], "monto": "200.00", "descripcion": "Deposito prueba"})
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["tipo_transaccion"] == "DEPOSITO"
    assert datos["saldo_resultante"] == "200.00"


def test_registrar_retiro(cliente):
    """Verifica que un retiro disminuya el saldo."""

    socio = crear_socio_prueba(cliente)
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    cliente.post("/api/v1/transacciones/deposito", json={"cuenta_id": cuenta["id"], "monto": "300.00"})
    respuesta = cliente.post("/api/v1/transacciones/retiro", json={"cuenta_id": cuenta["id"], "monto": "100.00"})
    assert respuesta.status_code == 200
    assert respuesta.json()["saldo_resultante"] == "200.00"


def test_impedir_retiro_saldo_insuficiente(cliente):
    """Verifica que no se permita retirar mas que el saldo disponible."""

    socio = crear_socio_prueba(cliente)
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    respuesta = cliente.post("/api/v1/transacciones/retiro", json={"cuenta_id": cuenta["id"], "monto": "50.00"})
    assert respuesta.status_code == 400
    assert "Saldo insuficiente" in respuesta.json()["detail"]


def test_api_externa_con_api_key(cliente):
    """Verifica la consulta externa de saldo y ultimos movimientos."""

    socio = crear_socio_prueba(cliente, cedula="0102030405")
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    cliente.post("/api/v1/transacciones/deposito", json={"cuenta_id": cuenta["id"], "monto": "200.00"})
    respuesta = cliente.get(
        "/api/v1/cuenta/movimientos",
        params={"cedula": "0102030405", "numeroCuenta": cuenta["numero_cuenta"]},
        headers={"X-API-KEY": "API-KEY-DEMO-123"},
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["saldo"] == "200.00"
    assert len(datos["movimientos"]) == 1

