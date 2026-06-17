"""Archivo: app/modelos/cuenta_ahorro_modelo.py
Descripcion: Modelo de cuentas de ahorro de socios.
Autor: Martinez Steeven
Version: 1.0
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class EstadoCuenta(str, enum.Enum):
    """Estados operativos de una cuenta de ahorro."""

    ACTIVA = "ACTIVA"
    BLOQUEADA = "BLOQUEADA"
    SALDO_CERO = "SALDO_CERO"
    CERRADA = "CERRADA"


class CuentaAhorro(Base):
    """Cuenta de ahorro perteneciente a un socio."""

    __tablename__ = "cuentas_ahorro"

    id = Column(Integer, primary_key=True, index=True)
    numero_cuenta = Column(String(30), unique=True, nullable=False, index=True)
    saldo = Column(Numeric(12, 2), default=0, nullable=False)
    fecha_apertura = Column(DateTime, default=datetime.utcnow, nullable=False)
    estado = Column(Enum(EstadoCuenta), default=EstadoCuenta.ACTIVA, nullable=False)
    socio_id = Column(Integer, ForeignKey("socios.id"), nullable=False)

    socio = relationship("Socio", back_populates="cuentas")
    transacciones = relationship("Transaccion", back_populates="cuenta", cascade="all, delete-orphan")

