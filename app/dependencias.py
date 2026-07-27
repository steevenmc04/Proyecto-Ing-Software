"""Archivo: app/dependencias.py
Descripcion: Dependencias reutilizables para seguridad y base de datos.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import obtener_db
from app.modelos.usuario_modelo import RolUsuario
from app.repositorios.usuario_repositorio import usuario_repositorio
from app.utilidades.seguridad import decodificar_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(obtener_db)):
    """Obtiene el usuario autenticado desde un JWT basico."""

    datos = decodificar_token(token)
    nombre_usuario = datos.get("sub")
    if not nombre_usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")
    usuario = usuario_repositorio.obtener_por_nombre_usuario(db, nombre_usuario)
    if not usuario or not usuario.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autorizado")
    return usuario


def requerir_roles(*roles_permitidos: RolUsuario):
    """Crea una dependencia que autoriza unicamente los roles indicados."""

    def validar_rol(usuario=Depends(obtener_usuario_actual)):
        if usuario.rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para realizar esta operacion",
            )
        return usuario

    validar_rol.roles_permitidos = tuple(rol.value for rol in roles_permitidos)
    return validar_rol
