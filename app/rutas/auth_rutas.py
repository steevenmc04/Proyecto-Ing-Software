"""Archivo: app/rutas/auth_rutas.py
Descripcion: Rutas de autenticacion.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import auth_controlador
from app.database import obtener_db
from app.esquemas.auth_esquema import LoginSolicitud, TokenRespuesta


router = APIRouter()


@router.post("/login", response_model=TokenRespuesta, summary="Iniciar sesion")
def login(datos: LoginSolicitud, db: Session = Depends(obtener_db)):
    """Valida credenciales de un usuario activo y devuelve un JWT basico."""

    return auth_controlador.login(db, datos)

