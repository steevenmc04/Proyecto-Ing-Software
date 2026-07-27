"""Archivo: tests/integration/test_flujo_api_externa.py
Descripcion: Prueba de integracion de consulta de la API externa.
"""

def test_flujo_completo_api_externa(cliente):
    """
    Simula el flujo:
    1. Crear socio
    2. Crear cuenta
    3. Hacer transacciones multiples
    4. Consultar API externa y validar saldos e historial
    """
    cedula_prueba = "9876543210"
    
    # 1. Crear Socio
    respuesta_socio = cliente.post(
        "/api/v1/socios",
        json={
            "cedula": cedula_prueba,
            "nombres": "Cliente",
            "apellidos": "Externo",
            "fecha_nacimiento": "1999-09-09",
            "direccion": "Web",
            "telefono": "0991112223",
            "correo": "externo@caja.com"
        }
    )
    assert respuesta_socio.status_code == 200
    socio_id = respuesta_socio.json()["id"]

    # 2. Crear Cuenta
    respuesta_cuenta = cliente.post("/api/v1/cuentas", json={"socio_id": socio_id})
    assert respuesta_cuenta.status_code == 200
    cuenta_data = respuesta_cuenta.json()
    cuenta_id = cuenta_data["id"]
    numero_cuenta = cuenta_data["numero_cuenta"]

    # 3. Hacer transacciones multiples
    cliente.post("/api/v1/transacciones/deposito", json={"cuenta_id": cuenta_id, "monto": "500.00", "descripcion": "Sueldo"})
    cliente.post("/api/v1/transacciones/retiro", json={"cuenta_id": cuenta_id, "monto": "100.00", "descripcion": "Luz"})
    cliente.post("/api/v1/transacciones/deposito", json={"cuenta_id": cuenta_id, "monto": "200.00", "descripcion": "Bono"})

    # Saldo final esperado: 600.00

    # 4. Consultar API externa
    respuesta_api = cliente.get(
        "/api/v1/cuenta/movimientos",
        params={"cedula": cedula_prueba, "numeroCuenta": numero_cuenta},
        headers={"X-API-KEY": "API-KEY-DEMO-123"}
    )
    assert respuesta_api.status_code == 200
    datos = respuesta_api.json()
    
    assert float(datos["saldo"]) == 600.00
    
    # Valida que retorne los ultimos 3 movimientos ordenados desc
    assert len(datos["movimientos"]) == 3
    assert float(datos["movimientos"][0]["monto"]) == 200.00 # El ultimo deposito de 200
    assert datos["movimientos"][0]["tipo"] == "DEPOSITO"
