"""Archivo: tests/unit/test_auth.py
Descripcion: Pruebas unitarias para el modulo de autenticacion.
"""

from app.esquemas.usuario_esquema import UsuarioCrear
from app.modelos.usuario_modelo import RolUsuario
from app.servicios.usuario_servicio import usuario_servicio

def test_login_exitoso(cliente):
    """Verifica que un usuario pueda iniciar sesion correctamente."""
    from app.database import SesionLocal
    db = SesionLocal()
    try:
        usuario_servicio.crear(
            db,
            UsuarioCrear(
                nombre_usuario="admin_test",
                nombre_completo="Admin Test",
                correo="admin@test.com",
                rol=RolUsuario.ADMINISTRADOR,
                contrasena="Admin123"
            )
        )
    finally:
        db.close()

    respuesta = cliente.post("/api/v1/auth/login", json={"nombre_usuario": "admin_test", "contrasena": "Admin123"})
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "access_token" in datos
    assert datos["token_type"] == "bearer"

def test_login_credenciales_invalidas(cliente):
    """Verifica que retorne 401 con credenciales incorrectas."""
    respuesta = cliente.post("/api/v1/auth/login", json={"nombre_usuario": "noexiste", "contrasena": "clave"})
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Credenciales invalidas o usuario inactivo"
