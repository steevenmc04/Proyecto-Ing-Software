"""Archivo: tests/unit/test_socios.py
Descripcion: Pruebas unitarias para el modulo de socios.
"""

from tests.conftest import crear_socio_prueba

def test_crear_socio_exitoso(cliente):
    """Verifica la creacion exitosa de un socio."""
    socio = crear_socio_prueba(cliente, cedula="0998887776")
    assert socio["id"] > 0
    assert socio["numero_socio"].startswith("SOC-")
    assert socio["estado"] == "ACTIVO"
    assert socio["nombres"] == "Maria"

def test_crear_socio_cedula_duplicada(cliente):
    """Verifica que no se pueda crear un socio con una cedula ya registrada."""
    crear_socio_prueba(cliente, cedula="0999999999")
    respuesta = cliente.post(
        "/api/v1/socios",
        json={
            "cedula": "0999999999",
            "nombres": "Juan",
            "apellidos": "Perez",
            "fecha_nacimiento": "1990-01-01",
            "direccion": "Direccion",
            "telefono": "0988888888",
            "correo": "juan@caja.com"
        }
    )
    assert respuesta.status_code == 400
    assert "ya registrado" in respuesta.json()["detail"].lower() or "uso" in respuesta.json()["detail"].lower() or "existe" in respuesta.json()["detail"].lower()

def test_obtener_socio_por_id(cliente):
    """Verifica obtener un socio por su ID."""
    socio_creado = crear_socio_prueba(cliente, cedula="0997776665")
    respuesta = cliente.get(f"/api/v1/socios/{socio_creado['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json()["cedula"] == "0997776665"

def test_obtener_socio_inexistente(cliente):
    """Verifica respuesta 404 para un socio que no existe."""
    respuesta = cliente.get("/api/v1/socios/9999")
    assert respuesta.status_code == 404
