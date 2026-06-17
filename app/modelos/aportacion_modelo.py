"""Archivo: app/modelos/aportacion_modelo.py
Descripcion: Modelo de aportaciones monetarias de socios.
Autor: Martinez Steeven
Version: 1.0
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class OperacionAportacion(str, enum.Enum):
    """Operaciones disponibles para aportaciones."""

    DEP = "DEP"
    RET = "RET"


class Aportacion(Base):
    """Deposito o retiro de aportacion asociado a un socio."""

    __tablename__ = "aportaciones"

    id = Column(Integer, primary_key=True, index=True)
    tipo_aportacion_id = Column(Integer, ForeignKey("tipos_aportacion.id"), nullable=False)
    operacion = Column(Enum(OperacionAportacion), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    descripcion = Column(String(250), nullable=True)
    socio_id = Column(Integer, ForeignKey("socios.id"), nullable=False)
    usuario_cajero_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    socio = relationship("Socio", back_populates="aportaciones")
    tipo_aportacion = relationship("TipoAportacion", back_populates="aportaciones")
    usuario_cajero = relationship("Usuario", foreign_keys=[usuario_cajero_id], back_populates="aportaciones_cajero")
    asiento_contable = relationship("AsientoContable", back_populates="aportacion", uselist=False)

