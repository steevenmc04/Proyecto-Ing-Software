"""Archivo: app/controladores/cuenta_ahorro_controlador.py
Descripcion: Controlador de cuentas de ahorro.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.modelos.cuenta_ahorro_modelo import EstadoCuenta
from app.servicios.cuenta_ahorro_servicio import cuenta_ahorro_servicio


def crear(db: Session, socio_id: int):
    """Crea cuenta."""

    return cuenta_ahorro_servicio.crear(db, socio_id)


def listar(db: Session, skip: int, limit: int):
    """Lista cuentas."""

    return cuenta_ahorro_servicio.listar(db, skip, limit)


def obtener(db: Session, id: int):
    """Obtiene cuenta por ID."""

    return cuenta_ahorro_servicio.obtener(db, id)


def listar_por_socio(db: Session, socio_id: int):
    """Lista cuentas por socio."""

    return cuenta_ahorro_servicio.listar_por_socio(db, socio_id)


def obtener_por_numero(db: Session, numero_cuenta: str):
    """Obtiene cuenta por numero."""

    return cuenta_ahorro_servicio.obtener_por_numero(db, numero_cuenta)


def bloquear(db: Session, id: int):
    """Bloquea cuenta."""

    return cuenta_ahorro_servicio.cambiar_estado(db, id, EstadoCuenta.BLOQUEADA)


def desbloquear(db: Session, id: int):
    """Desbloquea cuenta."""

    return cuenta_ahorro_servicio.cambiar_estado(db, id, EstadoCuenta.ACTIVA)


def cerrar(db: Session, id: int):
    """Cierra cuenta."""

    return cuenta_ahorro_servicio.cambiar_estado(db, id, EstadoCuenta.CERRADA)


def movimientos_externos(db: Session, cedula: str, numero_cuenta: str, api_key: str | None):
    """Consulta API externa."""

    return cuenta_ahorro_servicio.consultar_api_externa(db, cedula, numero_cuenta, api_key)

