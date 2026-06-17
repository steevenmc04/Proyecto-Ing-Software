"""Archivo: app/controladores/credito_controlador.py
Descripcion: Controlador de creditos y cuotas.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.esquemas.credito_esquema import CreditoAprobar, CreditoDesembolsar, CreditoRechazar, CreditoSolicitar, PagoCuotaSolicitud
from app.servicios.credito_servicio import credito_servicio


def solicitar(db: Session, datos: CreditoSolicitar):
    """Solicita credito."""

    return credito_servicio.solicitar(db, datos)


def listar(db: Session, skip: int, limit: int):
    """Lista creditos."""

    return credito_servicio.listar(db, skip, limit)


def obtener(db: Session, id: int):
    """Obtiene credito."""

    return credito_servicio.obtener(db, id)


def listar_por_socio(db: Session, socio_id: int):
    """Lista creditos por socio."""

    return credito_servicio.listar_por_socio(db, socio_id)


def aprobar(db: Session, id: int, datos: CreditoAprobar):
    """Aprueba credito."""

    return credito_servicio.aprobar(db, id, datos)


def rechazar(db: Session, id: int, datos: CreditoRechazar):
    """Rechaza credito."""

    return credito_servicio.rechazar(db, id, datos)


def desembolsar(db: Session, id: int, datos: CreditoDesembolsar):
    """Desembolsa credito."""

    return credito_servicio.desembolsar(db, id, datos)


def pagar_cuota(db: Session, id: int, datos: PagoCuotaSolicitud):
    """Paga siguiente cuota."""

    return credito_servicio.pagar_siguiente_cuota(db, id, datos)


def listar_cuotas(db: Session, id: int):
    """Lista cuotas."""

    return credito_servicio.listar_cuotas(db, id)


def obtener_cuota(db: Session, id: int):
    """Obtiene cuota."""

    return credito_servicio.obtener_cuota(db, id)

