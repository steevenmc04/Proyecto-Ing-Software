"""Archivo: app/esquemas/socio_esquema.py
Descripcion: Esquemas de socios de la caja de ahorros.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.modelos.socio_modelo import EstadoSocio


class SocioBase(BaseModel):
    """Datos personales principales del socio."""

    cedula: str = Field(..., min_length=5, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    fecha_nacimiento: date
    direccion: str = Field(..., min_length=3, max_length=200)
    telefono: str = Field(..., min_length=5, max_length=30)
    correo: EmailStr


class SocioCrear(SocioBase):
    """Datos necesarios para registrar un socio."""

    usuario_registro_id: int | None = None


class SocioActualizar(BaseModel):
    """Campos editables de un socio."""

    nombres: str | None = None
    apellidos: str | None = None
    fecha_nacimiento: date | None = None
    direccion: str | None = None
    telefono: str | None = None
    correo: EmailStr | None = None


class SocioRespuesta(SocioBase):
    """Respuesta completa de socio."""

    id: int
    numero_socio: str
    estado: EstadoSocio
    total_aportaciones: Decimal
    fecha_registro: datetime
    usuario_registro_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

