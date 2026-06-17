"""Archivo: app/controladores/transaccion_controlador.py
Descripcion: Controlador de transacciones.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.esquemas.transaccion_esquema import TransaccionCrear
from app.servicios.transaccion_servicio import transaccion_servicio


def deposito(db: Session, datos: TransaccionCrear):
    """Registra deposito."""

    return transaccion_servicio.registrar_deposito(db, datos)


def retiro(db: Session, datos: TransaccionCrear):
    """Registra retiro."""

    return transaccion_servicio.registrar_retiro(db, datos)


def listar(db: Session, skip: int, limit: int):
    """Lista transacciones."""

    return transaccion_servicio.listar(db, skip, limit)


def listar_por_cuenta(db: Session, cuenta_id: int):
    """Lista transacciones por cuenta."""

    return transaccion_servicio.listar_por_cuenta(db, cuenta_id)


def obtener(db: Session, id: int):
    """Obtiene transaccion."""

    return transaccion_servicio.obtener(db, id)

