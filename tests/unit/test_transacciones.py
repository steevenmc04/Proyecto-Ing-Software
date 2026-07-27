"""Archivo: tests/unit/test_transacciones.py
Descripcion: Pruebas unitarias para transacciones (depositos y retiros).
"""

from tests.conftest import crear_socio_prueba, crear_cuenta_prueba

def test_deposito_exitoso(cliente):
    """Verifica que un deposito sume al saldo correctamente."""
    socio = crear_socio_prueba(cliente, cedula="0991112223")
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    
    respuesta = cliente.post(
        "/api/v1/transacciones/deposito",
        json={
            "cuenta_id": cuenta["id"],
            "monto": "250.50",
            "descripcion": "Deposito de prueba"
        }
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["tipo_transaccion"] == "DEPOSITO"
    assert float(datos["monto"]) == 250.50
    assert float(datos["saldo_resultante"]) == 250.50

def test_retiro_exitoso(cliente):
    """Verifica que un retiro reste del saldo correctamente."""
    socio = crear_socio_prueba(cliente, cedula="0992223334")
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    
    cliente.post(
        "/api/v1/transacciones/deposito",
        json={"cuenta_id": cuenta["id"], "monto": "500.00", "descripcion": "Inicial"}
    )
    
    respuesta = cliente.post(
        "/api/v1/transacciones/retiro",
        json={
            "cuenta_id": cuenta["id"],
            "monto": "200.00",
            "descripcion": "Retiro parcial"
        }
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["tipo_transaccion"] == "RETIRO"
    assert float(datos["saldo_resultante"]) == 300.00

def test_retiro_saldo_insuficiente(cliente):
    """Verifica el error al intentar retirar mas del saldo disponible."""
    socio = crear_socio_prueba(cliente, cedula="0993334445")
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    
    cliente.post(
        "/api/v1/transacciones/deposito",
        json={"cuenta_id": cuenta["id"], "monto": "100.00"}
    )
    
    respuesta = cliente.post(
        "/api/v1/transacciones/retiro",
        json={"cuenta_id": cuenta["id"], "monto": "150.00"}
    )
    assert respuesta.status_code == 400
    assert "insuficiente" in respuesta.json()["detail"].lower()

def test_transaccion_monto_invalido(cliente):
    """Verifica que no se acepten montos negativos o cero."""
    socio = crear_socio_prueba(cliente, cedula="0994445556")
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    
    respuesta = cliente.post(
        "/api/v1/transacciones/deposito",
        json={"cuenta_id": cuenta["id"], "monto": "-50.00"}
    )
    # Dependiendo de pydantic puede ser 422 o validacion de negocio 400
    assert respuesta.status_code in [400, 422]
