"""Archivo: app/rutas/auth_rutas.py
Descripcion: Rutas de autenticacion.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import auth_controlador
from app.database import obtener_db
from app.dependencias import obtener_usuario_actual
from app.esquemas.auth_esquema import LoginSolicitud, TokenRespuesta
from app.esquemas.usuario_esquema import UsuarioRespuesta


router = APIRouter()


@router.post("/login", response_model=TokenRespuesta, summary="Iniciar sesion")
def login(datos: LoginSolicitud, db: Session = Depends(obtener_db)):
    """Valida credenciales de un usuario activo y devuelve un JWT basico."""

    return auth_controlador.login(db, datos)


@router.get("/me", response_model=UsuarioRespuesta, summary="Obtener usuario autenticado")
def me(usuario=Depends(obtener_usuario_actual)):
    """Devuelve los datos del usuario autenticado por JWT."""

    return usuario
