"""Archivo: app/modelos/transaccion_modelo.py
Descripcion: Modelo de depositos, retiros y movimientos de aportacion.
Autor: Martinez Steeven
Version: 1.0
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class TipoTransaccion(str, enum.Enum):
    """Tipos de transacciones monetarias sobre cuentas."""

    DEPOSITO = "DEPOSITO"
    RETIRO = "RETIRO"
    APORTACION = "APORTACION"


class Transaccion(Base):
    """Movimiento que actualiza el saldo de una cuenta de ahorro."""

    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    numero_comprobante = Column(String(50), unique=True, nullable=False, index=True)
    tipo_transaccion = Column(Enum(TipoTransaccion), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    descripcion = Column(String(250), nullable=True)
    saldo_resultante = Column(Numeric(12, 2), nullable=False)
    cuenta_id = Column(Integer, ForeignKey("cuentas_ahorro.id"), nullable=False)
    usuario_cajero_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    cuenta = relationship("CuentaAhorro", back_populates="transacciones")
    usuario_cajero = relationship("Usuario", foreign_keys=[usuario_cajero_id], back_populates="transacciones_cajero")
    asiento_contable = relationship("AsientoContable", back_populates="transaccion", uselist=False)

