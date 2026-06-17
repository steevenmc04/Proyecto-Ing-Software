"""Archivo: app/controladores/reporte_controlador.py
Descripcion: Controlador de reportes.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.servicios.reporte_servicio import reporte_servicio


def libro_diario(db: Session):
    """Reporte libro diario."""

    return reporte_servicio.libro_diario(db)


def historial_ahorros(db: Session, socio_id: int):
    """Reporte historial de ahorros."""

    return reporte_servicio.historial_ahorros(db, socio_id)


def cartera_creditos(db: Session):
    """Reporte cartera crediticia."""

    return reporte_servicio.cartera_creditos(db)


def resumen_aportaciones(db: Session, socio_id: int):
    """Reporte resumen de aportaciones."""

    return reporte_servicio.resumen_aportaciones(db, socio_id)

