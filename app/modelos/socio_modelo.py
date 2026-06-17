"""Archivo: app/modelos/socio_modelo.py
Descripcion: Modelo de socios registrados en la caja de ahorros.
Autor: Martinez Steeven
Version: 1.0
"""

import enum
from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class EstadoSocio(str, enum.Enum):
    """Estados disponibles para un socio."""

    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


class Socio(Base):
    """Persona afiliada a la caja de ahorros."""

    __tablename__ = "socios"

    id = Column(Integer, primary_key=True, index=True)
    numero_socio = Column(String(30), unique=True, nullable=False, index=True)
    cedula = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False, index=True)
    apellidos = Column(String(100), nullable=False, index=True)
    fecha_nacimiento = Column(Date, nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(30), nullable=False)
    correo = Column(String(120), nullable=False)
    estado = Column(Enum(EstadoSocio), default=EstadoSocio.ACTIVO, nullable=False)
    total_aportaciones = Column(Numeric(12, 2), default=0, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow, nullable=False)
    usuario_registro_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=True)

    usuario_registro = relationship("Usuario", foreign_keys=[usuario_registro_id], back_populates="socios_registrados")
    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="socio_perfil")
    cuentas = relationship("CuentaAhorro", back_populates="socio", cascade="all, delete-orphan")
    aportaciones = relationship("Aportacion", back_populates="socio", cascade="all, delete-orphan")
    creditos = relationship("Credito", back_populates="socio", cascade="all, delete-orphan")
