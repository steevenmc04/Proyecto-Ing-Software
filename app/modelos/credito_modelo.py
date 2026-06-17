"""Archivo: app/modelos/credito_modelo.py
Descripcion: Modelo de solicitudes y seguimiento de creditos.
Autor: Martinez Steeven
Version: 1.0
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class EstadoCredito(str, enum.Enum):
    """Estados del ciclo de vida de un credito."""

    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    DESEMBOLSADO = "DESEMBOLSADO"
    EN_PAGO = "EN_PAGO"
    VENCIDO = "VENCIDO"
    CANCELADO = "CANCELADO"


class Credito(Base):
    """Credito solicitado por un socio con amortizacion francesa."""

    __tablename__ = "creditos"

    id = Column(Integer, primary_key=True, index=True)
    numero_credito = Column(String(30), unique=True, nullable=False, index=True)
    socio_id = Column(Integer, ForeignKey("socios.id"), nullable=False)
    monto_solicitado = Column(Numeric(12, 2), nullable=False)
    monto_aprobado = Column(Numeric(12, 2), nullable=True)
    plazo_meses = Column(Integer, nullable=False)
    tasa_interes = Column(Numeric(5, 2), nullable=False)
    tipo_garantia = Column(String(100), nullable=False)
    proposito = Column(String(250), nullable=False)
    estado = Column(Enum(EstadoCredito), default=EstadoCredito.PENDIENTE, nullable=False)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_aprobacion = Column(DateTime, nullable=True)
    motivo_rechazo = Column(String(250), nullable=True)
    gerente_aprobador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    cajero_desembolso_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    saldo_pendiente = Column(Numeric(12, 2), default=0, nullable=False)

    socio = relationship("Socio", back_populates="creditos")
    gerente_aprobador = relationship("Usuario", foreign_keys=[gerente_aprobador_id], back_populates="creditos_aprobados")
    cajero_desembolso = relationship("Usuario", foreign_keys=[cajero_desembolso_id], back_populates="creditos_desembolsados")
    cuotas = relationship("CuotaAmortizacion", back_populates="credito", cascade="all, delete-orphan")
    asientos_contables = relationship("AsientoContable", back_populates="credito")

