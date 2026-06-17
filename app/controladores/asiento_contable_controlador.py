"""Archivo: app/controladores/asiento_contable_controlador.py
Descripcion: Controlador de asientos contables.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.servicios.asiento_contable_servicio import asiento_contable_servicio


def listar(db: Session, skip: int, limit: int):
    """Lista asientos."""

    return asiento_contable_servicio.listar(db, skip, limit)


def obtener(db: Session, id: int):
    """Obtiene asiento."""

    return asiento_contable_servicio.obtener(db, id)


def rango_fechas(db: Session, fecha_inicio, fecha_fin):
    """Lista asientos por rango."""

    return asiento_contable_servicio.listar_rango_fechas(db, fecha_inicio, fecha_fin)

