"""Archivo: tests/unit/test_creditos.py
Descripcion: Pruebas unitarias para el modulo de creditos.
"""

from tests.conftest import crear_socio_prueba

def test_solicitar_credito(cliente):
    """Verifica que se pueda solicitar un credito."""
    socio = crear_socio_prueba(cliente, cedula="2223334445")
    
    respuesta = cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "5000.00",
            "plazo_meses": 12,
            "tasa_interes": "10.00",
            "tipo_garantia": "Garante personal",
            "proposito": "Compra de vehiculo"
        }
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["estado"] == "PENDIENTE"
    assert float(datos["monto_solicitado"]) == 5000.00

def test_aprobar_credito(cliente):
    """Verifica la aprobacion de un credito."""
    socio = crear_socio_prueba(cliente, cedula="3334445556")
    solicitud = cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "2000.00",
            "plazo_meses": 6,
            "tasa_interes": "12.00",
            "tipo_garantia": "Ninguna",
            "proposito": "Viaje"
        }
    ).json()
    
    aprobacion = cliente.patch(f"/api/v1/creditos/{solicitud['id']}/aprobar", json={})
    assert aprobacion.status_code == 200
    assert aprobacion.json()["estado"] == "APROBADO"

def test_rechazar_credito(cliente):
    """Verifica el rechazo de un credito."""
    socio = crear_socio_prueba(cliente, cedula="4445556667")
    solicitud = cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "10000.00",
            "plazo_meses": 24,
            "tasa_interes": "15.00",
            "tipo_garantia": "Hipotecaria",
            "proposito": "Negocio"
        }
    ).json()
    
    rechazo = cliente.patch(
        f"/api/v1/creditos/{solicitud['id']}/rechazar",
        json={"motivo_rechazo": "Capacidad de pago insuficiente"}
    )
    assert rechazo.status_code == 200
    assert rechazo.json()["estado"] == "RECHAZADO"

def test_obtener_creditos_socio(cliente):
    """Verifica que se listen los creditos de un socio."""
    socio = crear_socio_prueba(cliente, cedula="5556667778")
    cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "1000.00",
            "plazo_meses": 12,
            "tasa_interes": "10.00",
            "tipo_garantia": "Ninguna",
            "proposito": "Personal"
        }
    )
    
    respuesta = cliente.get(f"/api/v1/creditos/socio/{socio['id']}")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
