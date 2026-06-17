"""Archivo: app/controladores/socio_controlador.py
Descripcion: Controlador de socios.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.esquemas.socio_esquema import SocioActualizar, SocioCrear
from app.servicios.socio_servicio import socio_servicio


def crear(db: Session, datos: SocioCrear):
    """Crea socio."""

    return socio_servicio.crear(db, datos)


def listar(db: Session, skip: int, limit: int, buscar: str | None):
    """Lista o busca socios."""

    return socio_servicio.listar(db, skip, limit, buscar)


def obtener(db: Session, id: int):
    """Obtiene socio por ID."""

    return socio_servicio.obtener(db, id)


def obtener_por_cedula(db: Session, cedula: str):
    """Obtiene socio por cedula."""

    return socio_servicio.obtener_por_cedula(db, cedula)


def obtener_por_usuario(db: Session, usuario_id: int):
    """Obtiene socio vinculado a un usuario."""

    return socio_servicio.obtener_por_usuario(db, usuario_id)


def actualizar(db: Session, id: int, datos: SocioActualizar):
    """Actualiza socio."""

    return socio_servicio.actualizar(db, id, datos)


def activar(db: Session, id: int):
    """Activa socio."""

    return socio_servicio.cambiar_estado(db, id, True)


def desactivar(db: Session, id: int):
    """Desactiva socio."""

    return socio_servicio.cambiar_estado(db, id, False)
