"""Archivo: app/controladores/usuario_controlador.py
Descripcion: Controlador de usuarios.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.esquemas.usuario_esquema import UsuarioActualizar, UsuarioCrear
from app.servicios.usuario_servicio import usuario_servicio


def crear(db: Session, datos: UsuarioCrear):
    """Crea usuario."""

    return usuario_servicio.crear(db, datos)


def listar(db: Session, skip: int, limit: int):
    """Lista usuarios."""

    return usuario_servicio.listar(db, skip, limit)


def obtener(db: Session, id: int):
    """Obtiene usuario."""

    return usuario_servicio.obtener(db, id)


def actualizar(db: Session, id: int, datos: UsuarioActualizar):
    """Actualiza usuario."""

    return usuario_servicio.actualizar(db, id, datos)


def activar(db: Session, id: int):
    """Activa usuario."""

    return usuario_servicio.cambiar_estado(db, id, True)


def desactivar(db: Session, id: int):
    """Desactiva usuario."""

    return usuario_servicio.cambiar_estado(db, id, False)

