"""Pruebas de autenticacion, roles, CORS y salud versionada."""

from fastapi.testclient import TestClient

from app.main import app


def test_ruta_administrativa_requiere_token(cliente):
    """Rechaza consultas administrativas sin JWT."""

    with TestClient(app) as cliente_anonimo:
        respuesta = cliente_anonimo.get("/api/v1/usuarios")

    assert respuesta.status_code == 401


def test_socio_no_puede_listar_usuarios(cliente):
    """Impide que un usuario SOCIO consulte el modulo administrativo."""

    cliente.post(
        "/api/v1/usuarios",
        json={
            "nombre_usuario": "socio_roles",
            "nombre_completo": "Socio Roles",
            "correo": "socio.roles@caja.com",
            "rol": "SOCIO",
            "contrasena": "Socio123",
        },
    )
    login = cliente.post(
        "/api/v1/auth/login",
        json={"nombre_usuario": "socio_roles", "contrasena": "Socio123"},
    )
    token = login.json()["access_token"]

    respuesta = cliente.get(
        "/api/v1/usuarios",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert respuesta.status_code == 403
    assert respuesta.json()["detail"] == "No tiene permisos para realizar esta operacion"


def test_salud_versionada(cliente):
    """Expone el contrato de salud requerido sin autenticacion."""

    with TestClient(app) as cliente_anonimo:
        respuesta = cliente_anonimo.get("/api/v1/salud")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "estado": "correcto",
        "aplicacion": "Sistema de Gestion de Caja de Ahorros",
    }


def test_cors_permite_frontend_local(cliente):
    """Permite preflight unicamente para el frontend configurado."""

    respuesta = cliente.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert respuesta.status_code == 200
    assert respuesta.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"
