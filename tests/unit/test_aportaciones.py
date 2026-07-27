"""Archivo: tests/unit/test_aportaciones.py
Descripcion: Pruebas unitarias para el modulo de aportaciones.
"""

from tests.conftest import crear_socio_prueba

def test_registrar_aportacion_exitosa(cliente):
    """Verifica el registro de un deposito de aportacion."""
    socio = crear_socio_prueba(cliente, cedula="1234567890")
    
    # Crear un tipo de aportacion
    tipo_respuesta = cliente.post("/api/v1/aportaciones/tipos", json={"nombre": "ORDINARIA", "descripcion": "Ordinaria test"})
    tipo_id = tipo_respuesta.json()["id"]

    respuesta = cliente.post(
        "/api/v1/aportaciones/deposito",
        json={
            "socio_id": socio["id"],
            "tipo_aportacion_id": tipo_id,
            "monto": "20.00",
            "descripcion": "Mensual"
        }
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert float(datos["monto"]) == 20.00

def test_aportacion_monto_invalido(cliente):
    """Verifica validacion de monto negativo."""
    socio = crear_socio_prueba(cliente, cedula="1234567891")
    tipo_respuesta = cliente.post("/api/v1/aportaciones/tipos", json={"nombre": "EXTRAORDINARIA"})
    
    # Si retorna 400 por ya existir "EXTRAORDINARIA", obtenemos el primero
    if tipo_respuesta.status_code != 200:
        tipo_id = cliente.get("/api/v1/aportaciones/tipos").json()[0]["id"]
    else:
        tipo_id = tipo_respuesta.json()["id"]

    respuesta = cliente.post(
        "/api/v1/aportaciones/deposito",
        json={
            "socio_id": socio["id"],
            "tipo_aportacion_id": tipo_id,
            "monto": "-20.00"
        }
    )
    assert respuesta.status_code in [400, 422]

def test_obtener_aportaciones_socio(cliente):
    """Verifica obtener historial de aportaciones de un socio."""
    socio = crear_socio_prueba(cliente, cedula="1234567892")
    tipo = cliente.post("/api/v1/aportaciones/tipos", json={"nombre": "ORDINARIA"}).json()
    if "id" not in tipo:
        tipo = cliente.get("/api/v1/aportaciones/tipos").json()[0]
        
    tipo_id = tipo["id"]

    cliente.post("/api/v1/aportaciones/deposito", json={"socio_id": socio["id"], "tipo_aportacion_id": tipo_id, "monto": "20.00"})
    cliente.post("/api/v1/aportaciones/deposito", json={"socio_id": socio["id"], "tipo_aportacion_id": tipo_id, "monto": "20.00"})
    
    respuesta = cliente.get(f"/api/v1/aportaciones/socio/{socio['id']}")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert len(datos) == 2
