"""Archivo: tests/integration/test_flujo_transacciones.py
Descripcion: Prueba de integracion del flujo completo de transacciones.
"""

def test_flujo_completo_socio_cuenta_transacciones(cliente):
    """
    Simula el flujo: 
    1. Crear socio
    2. Crear cuenta
    3. Realizar deposito
    4. Realizar retiro
    5. Validar saldo final
    """
    # 1. Crear Socio
    respuesta_socio = cliente.post(
        "/api/v1/socios",
        json={
            "cedula": "1020304050",
            "nombres": "Integracion",
            "apellidos": "Transaccion",
            "fecha_nacimiento": "1995-05-05",
            "direccion": "Avenida",
            "telefono": "0987654321",
            "correo": "integracion1@caja.com"
        }
    )
    assert respuesta_socio.status_code == 200
    socio_id = respuesta_socio.json()["id"]

    # 2. Crear Cuenta
    respuesta_cuenta = cliente.post("/api/v1/cuentas", json={"socio_id": socio_id})
    assert respuesta_cuenta.status_code == 200
    cuenta_id = respuesta_cuenta.json()["id"]

    # 3. Realizar Deposito
    respuesta_dep = cliente.post(
        "/api/v1/transacciones/deposito",
        json={"cuenta_id": cuenta_id, "monto": "1000.00", "descripcion": "Ahorro inicial"}
    )
    assert respuesta_dep.status_code == 200
    assert float(respuesta_dep.json()["saldo_resultante"]) == 1000.00

    # 4. Realizar Retiro
    respuesta_ret = cliente.post(
        "/api/v1/transacciones/retiro",
        json={"cuenta_id": cuenta_id, "monto": "250.00", "descripcion": "Gastos varios"}
    )
    assert respuesta_ret.status_code == 200
    assert float(respuesta_ret.json()["saldo_resultante"]) == 750.00

    # 5. Validar saldo final en cuentas
    respuesta_cuentas = cliente.get(f"/api/v1/cuentas/socio/{socio_id}")
    assert float(respuesta_cuentas.json()[0]["saldo"]) == 750.00
