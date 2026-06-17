"""Archivo: app/controladores/aportacion_controlador.py
Descripcion: Controlador de aportaciones.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.esquemas.aportacion_esquema import AportacionCrear, TipoAportacionCrear
from app.servicios.aportacion_servicio import aportacion_servicio


def crear_tipo(db: Session, datos: TipoAportacionCrear):
    """Crea tipo."""

    return aportacion_servicio.crear_tipo(db, datos)


def listar_tipos(db: Session):
    """Lista tipos."""

    return aportacion_servicio.listar_tipos(db)


def deposito(db: Session, datos: AportacionCrear):
    """Registra deposito."""

    return aportacion_servicio.registrar_deposito(db, datos)


def retiro(db: Session, datos: AportacionCrear):
    """Registra retiro."""

    return aportacion_servicio.registrar_retiro(db, datos)


def listar(db: Session, skip: int, limit: int):
    """Lista aportaciones."""

    return aportacion_servicio.listar(db, skip, limit)


def listar_por_socio(db: Session, socio_id: int):
    """Lista aportaciones por socio."""

    return aportacion_servicio.listar_por_socio(db, socio_id)

