"""Archivo: app/modelos/tipo_aportacion_modelo.py
Descripcion: Catalogo de tipos de aportacion permitidos.
Autor: Martinez Steeven
Version: 1.0
"""

import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class NombreTipoAportacion(str, enum.Enum):
    """Tipos academicos solicitados para aportaciones."""

    ORDINARIA = "ORDINARIA"
    EXTRAORDINARIA = "EXTRAORDINARIA"


class TipoAportacion(Base):
    """Catalogo de aportaciones ordinarias y extraordinarias."""

    __tablename__ = "tipos_aportacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Enum(NombreTipoAportacion), unique=True, nullable=False)
    descripcion = Column(String(200), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    aportaciones = relationship("Aportacion", back_populates="tipo_aportacion")

