"""Archivo: app/modelos/cuota_amortizacion_modelo.py
Descripcion: Modelo de cuotas generadas por metodo frances.
Autor: Martinez Steeven
Version: 1.0
"""

import enum

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class EstadoCuota(str, enum.Enum):
    """Estados de una cuota de amortizacion."""

    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    VENCIDA = "VENCIDA"


class CuotaAmortizacion(Base):
    """Cuota mensual con capital, interes y saldo pendiente."""

    __tablename__ = "cuotas_amortizacion"

    id = Column(Integer, primary_key=True, index=True)
    credito_id = Column(Integer, ForeignKey("creditos.id"), nullable=False)
    numero_cuota = Column(Integer, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    capital = Column(Numeric(12, 2), nullable=False)
    interes = Column(Numeric(12, 2), nullable=False)
    cuota_total = Column(Numeric(12, 2), nullable=False)
    saldo_pendiente = Column(Numeric(12, 2), nullable=False)
    estado = Column(Enum(EstadoCuota), default=EstadoCuota.PENDIENTE, nullable=False)

    credito = relationship("Credito", back_populates="cuotas")

