"""Archivo: app/esquemas/auth_esquema.py
Descripcion: Esquemas de autenticacion y respuesta JWT.
Autor: Martinez Steeven
Version: 1.0
"""

from pydantic import BaseModel

from app.esquemas.usuario_esquema import UsuarioRespuesta


class LoginSolicitud(BaseModel):
    """Credenciales de inicio de sesion."""

    nombre_usuario: str
    contrasena: str


class TokenRespuesta(BaseModel):
    """Respuesta de login con JWT."""

    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioRespuesta

