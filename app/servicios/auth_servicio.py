"""Archivo: app/servicios/auth_servicio.py
Descripcion: Servicio de login con BCrypt y JWT.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.esquemas.auth_esquema import LoginSolicitud
from app.repositorios.usuario_repositorio import usuario_repositorio
from app.utilidades.seguridad import crear_token_jwt, verificar_contrasena


class AuthServicio:
    """Gestiona autenticacion de usuarios activos."""

    def login(self, db: Session, datos: LoginSolicitud):
        """Valida credenciales y genera un token JWT."""

        usuario = usuario_repositorio.obtener_por_nombre_usuario(db, datos.nombre_usuario)
        if not usuario or not usuario.activo:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas o usuario inactivo")
        if not verificar_contrasena(datos.contrasena, usuario.contrasena_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
        token = crear_token_jwt(usuario.nombre_usuario, usuario.rol.value)
        return {"access_token": token, "token_type": "bearer", "usuario": usuario}


auth_servicio = AuthServicio()

