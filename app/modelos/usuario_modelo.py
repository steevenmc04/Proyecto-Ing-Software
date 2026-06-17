"""Archivo: app/modelos/usuario_modelo.py
Descripcion: Modelo de usuarios y roles del sistema.
Autor: Martinez Steeven
Version: 1.0
"""

import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class RolUsuario(str, enum.Enum):
    """Roles autorizados dentro de la caja de ahorros."""

    ADMINISTRADOR = "ADMINISTRADOR"
    GERENTE = "GERENTE"
    CAJERO = "CAJERO"
    SOCIO = "SOCIO"
    CONTADOR = "CONTADOR"


class Usuario(Base):
    """Usuario interno con rol y credenciales de acceso."""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False, index=True)
    nombre_completo = Column(String(150), nullable=False)
    correo = Column(String(120), unique=True, nullable=False, index=True)
    rol = Column(Enum(RolUsuario), nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)

    socios_registrados = relationship("Socio", foreign_keys="Socio.usuario_registro_id", back_populates="usuario_registro")
    transacciones_cajero = relationship("Transaccion", foreign_keys="Transaccion.usuario_cajero_id", back_populates="usuario_cajero")
    aportaciones_cajero = relationship("Aportacion", foreign_keys="Aportacion.usuario_cajero_id", back_populates="usuario_cajero")
    creditos_aprobados = relationship("Credito", foreign_keys="Credito.gerente_aprobador_id", back_populates="gerente_aprobador")
    creditos_desembolsados = relationship("Credito", foreign_keys="Credito.cajero_desembolso_id", back_populates="cajero_desembolso")

