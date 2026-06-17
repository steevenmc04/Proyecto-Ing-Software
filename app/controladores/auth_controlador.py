"""Archivo: app/controladores/auth_controlador.py
Descripcion: Controlador de autenticacion.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.esquemas.auth_esquema import LoginSolicitud
from app.servicios.auth_servicio import auth_servicio


def login(db: Session, datos: LoginSolicitud):
    """Delegacion de login al servicio de autenticacion."""

    return auth_servicio.login(db, datos)

