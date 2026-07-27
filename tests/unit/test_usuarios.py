"""Archivo: tests/unit/test_usuarios.py
Descripcion: Pruebas unitarias para el modulo de usuarios.
"""

def test_crear_usuario_admin(cliente):
    """Verifica la creacion de un usuario administrador."""
    respuesta = cliente.post(
        "/api/v1/usuarios",
        json={
            "nombre_usuario": "nuevo_admin",
            "nombre_completo": "Nuevo Admin",
            "correo": "nuevoadmin@caja.com",
            "rol": "ADMINISTRADOR",
            "contrasena": "Segura123"
        }
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["nombre_usuario"] == "nuevo_admin"
    assert datos["rol"] == "ADMINISTRADOR"
    assert "id" in datos

def test_crear_usuario_duplicado(cliente):
    """Verifica que no se puedan crear usuarios con el mismo username o correo."""
    datos_usuario = {
        "nombre_usuario": "duplicado",
        "nombre_completo": "Duplicado",
        "correo": "duplicado@caja.com",
        "rol": "CAJERO",
        "contrasena": "Clave123"
    }
    cliente.post("/api/v1/usuarios", json=datos_usuario)
    respuesta2 = cliente.post("/api/v1/usuarios", json=datos_usuario)
    assert respuesta2.status_code == 400
    assert "ya esta en uso" in respuesta2.json()["detail"] or "ya existe" in respuesta2.json()["detail"]
