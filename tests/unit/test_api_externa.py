"""Archivo: tests/unit/test_api_externa.py
Descripcion: Pruebas unitarias para la API externa protegida.
"""

from tests.conftest import crear_socio_prueba, crear_cuenta_prueba

def test_api_externa_sin_api_key(cliente):
    """Verifica que retorne error si no se envia la API KEY."""
    respuesta = cliente.get(
        "/api/v1/cuenta/movimientos",
        params={"cedula": "0102030405", "numeroCuenta": "CTA-123"}
    )
    assert respuesta.status_code == 401
    assert "API Key" in respuesta.json()["detail"]

def test_api_externa_datos_invalidos(cliente):
    """Verifica respuesta 404 si la cedula o cuenta son incorrectas."""
    respuesta = cliente.get(
        "/api/v1/cuenta/movimientos",
        params={"cedula": "9999999999", "numeroCuenta": "CTA-999"},
        headers={"X-API-KEY": "API-KEY-DEMO-123"}
    )
    assert respuesta.status_code == 404

def test_api_externa_consulta_exitosa(cliente):
    """Verifica consulta correcta con API KEY y datos validos."""
    socio = crear_socio_prueba(cliente, cedula="0102030405")
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    cliente.post("/api/v1/transacciones/deposito", json={"cuenta_id": cuenta["id"], "monto": "150.00"})
    
    respuesta = cliente.get(
        "/api/v1/cuenta/movimientos",
        params={"cedula": "0102030405", "numeroCuenta": cuenta["numero_cuenta"]},
        headers={"X-API-KEY": "API-KEY-DEMO-123"}
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert float(datos["saldo"]) == 150.00
    assert len(datos["movimientos"]) > 0
