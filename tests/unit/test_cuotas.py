"""Archivo: tests/unit/test_cuotas.py
Descripcion: Pruebas unitarias para cuotas de amortizacion.
"""

from tests.conftest import crear_socio_prueba

def test_generacion_y_consulta_cuotas(cliente):
    """Verifica que al aprobar un credito, se puedan consultar sus cuotas."""
    socio = crear_socio_prueba(cliente, cedula="8889990001")
    
    solicitud = cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "1200.00",
            "plazo_meses": 12,
            "tasa_interes": "12.00",
            "tipo_garantia": "Personal",
            "proposito": "Prueba cuotas"
        }
    ).json()
    
    cliente.patch(f"/api/v1/creditos/{solicitud['id']}/aprobar", json={})
    
    respuesta = cliente.get(f"/api/v1/creditos/{solicitud['id']}/cuotas")
    assert respuesta.status_code == 200
    cuotas = respuesta.json()
    assert len(cuotas) == 12
    assert cuotas[0]["numero_cuota"] == 1
    assert float(cuotas[0]["saldo_pendiente"]) > 0

def test_obtener_cuota_individual(cliente):
    """Verifica consultar una cuota por su ID."""
    socio = crear_socio_prueba(cliente, cedula="8889990002")
    solicitud = cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "500.00",
            "plazo_meses": 6,
            "tasa_interes": "10.00",
            "tipo_garantia": "Personal",
            "proposito": "Prueba individual"
        }
    ).json()
    
    cliente.patch(f"/api/v1/creditos/{solicitud['id']}/aprobar", json={})
    cuotas = cliente.get(f"/api/v1/creditos/{solicitud['id']}/cuotas").json()
    
    cuota_id = cuotas[0]["id"]
    respuesta = cliente.get(f"/api/v1/cuotas/{cuota_id}")
    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == cuota_id
