"""Archivo: app/modelos/asiento_contable_modelo.py
Descripcion: Modelo de asientos del libro diario contable.
Autor: Martinez Steeven
Version: 1.0
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class TipoOrigenAsiento(str, enum.Enum):
    """Origen financiero del asiento contable."""

    TRANSACCION = "TRANSACCION"
    APORTACION = "APORTACION"
    CREDITO = "CREDITO"
    PAGO_CUOTA = "PAGO_CUOTA"


class AsientoContable(Base):
    """Registro contable con debito y credito por el mismo monto."""

    __tablename__ = "asientos_contables"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    descripcion = Column(String(250), nullable=False)
    cuenta_debito = Column(String(120), nullable=False)
    cuenta_credito = Column(String(120), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    tipo_origen = Column(Enum(TipoOrigenAsiento), nullable=False)
    transaccion_id = Column(Integer, ForeignKey("transacciones.id"), nullable=True)
    credito_id = Column(Integer, ForeignKey("creditos.id"), nullable=True)
    aportacion_id = Column(Integer, ForeignKey("aportaciones.id"), nullable=True)

    transaccion = relationship("Transaccion", back_populates="asiento_contable")
    credito = relationship("Credito", back_populates="asientos_contables")
    aportacion = relationship("Aportacion", back_populates="asiento_contable")

