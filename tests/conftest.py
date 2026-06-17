"""Archivo: tests/conftest.py
Descripcion: Configuracion comun para pruebas automatizadas.
Autor: Martinez Steeven
Version: 1.0
"""

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app
from app.modelos import *  # noqa: F401,F403 - registra modelos en pruebas


@pytest.fixture()
def cliente():
    """Entrega un cliente HTTP con base de datos limpia en cada prueba."""

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as cliente_prueba:
        yield cliente_prueba
    Base.metadata.drop_all(bind=engine)


def crear_socio_prueba(cliente: TestClient, cedula: str = "0999999999"):
    """Crea un socio de prueba y devuelve el JSON de respuesta."""

    respuesta = cliente.post(
        "/api/v1/socios",
        json={
            "cedula": cedula,
            "nombres": "Maria",
            "apellidos": "Lopez",
            "fecha_nacimiento": "1994-03-10",
            "direccion": "Calle Central 123",
            "telefono": "0987654321",
            "correo": f"{cedula}@caja.com",
            "usuario_registro_id": None,
        },
    )
    assert respuesta.status_code == 200
    return respuesta.json()


def crear_cuenta_prueba(cliente: TestClient, socio_id: int):
    """Crea una cuenta de ahorro de prueba."""

    respuesta = cliente.post("/api/v1/cuentas", json={"socio_id": socio_id})
    assert respuesta.status_code == 200
    return respuesta.json()

