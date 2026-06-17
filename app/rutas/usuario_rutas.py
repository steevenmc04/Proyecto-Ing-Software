"""Archivo: app/rutas/usuario_rutas.py
Descripcion: Rutas REST para usuarios.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import usuario_controlador
from app.database import obtener_db
from app.esquemas.usuario_esquema import UsuarioActualizar, UsuarioCrear, UsuarioRespuesta


router = APIRouter()


@router.post("", response_model=UsuarioRespuesta, summary="Crear usuario")
def crear(datos: UsuarioCrear, db: Session = Depends(obtener_db)):
    """Crea un usuario con rol permitido y contrasena hasheada con BCrypt."""

    return usuario_controlador.crear(db, datos)


@router.get("", response_model=list[UsuarioRespuesta], summary="Listar usuarios")
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(obtener_db)):
    """Lista usuarios registrados en el sistema."""

    return usuario_controlador.listar(db, skip, limit)


@router.get("/{id}", response_model=UsuarioRespuesta, summary="Obtener usuario por ID")
def obtener(id: int, db: Session = Depends(obtener_db)):
    """Consulta un usuario por su identificador."""

    return usuario_controlador.obtener(db, id)


@router.put("/{id}", response_model=UsuarioRespuesta, summary="Actualizar usuario")
def actualizar(id: int, datos: UsuarioActualizar, db: Session = Depends(obtener_db)):
    """Actualiza datos basicos, rol o contrasena de un usuario."""

    return usuario_controlador.actualizar(db, id, datos)


@router.patch("/{id}/activar", response_model=UsuarioRespuesta, summary="Activar usuario")
def activar(id: int, db: Session = Depends(obtener_db)):
    """Activa un usuario para permitir login."""

    return usuario_controlador.activar(db, id)


@router.patch("/{id}/desactivar", response_model=UsuarioRespuesta, summary="Desactivar usuario")
def desactivar(id: int, db: Session = Depends(obtener_db)):
    """Desactiva un usuario e impide que inicie sesion."""

    return usuario_controlador.desactivar(db, id)

