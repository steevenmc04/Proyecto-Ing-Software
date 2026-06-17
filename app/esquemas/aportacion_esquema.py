"""Archivo: app/esquemas/aportacion_esquema.py
Descripcion: Esquemas para tipos y movimientos de aportacion.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.modelos.aportacion_modelo import OperacionAportacion
from app.modelos.tipo_aportacion_modelo import NombreTipoAportacion


class TipoAportacionCrear(BaseModel):
    """Datos para crear un tipo de aportacion."""

    nombre: NombreTipoAportacion
    descripcion: str | None = None


class TipoAportacionRespuesta(TipoAportacionCrear):
    """Respuesta del catalogo de tipos de aportacion."""

    id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class AportacionCrear(BaseModel):
    """Datos para registrar deposito o retiro de aportacion."""

    socio_id: int
    tipo_aportacion_id: int
    monto: Decimal = Field(..., gt=0)
    descripcion: str | None = None
    usuario_cajero_id: int | None = None


class AportacionRespuesta(BaseModel):
    """Respuesta de aportacion registrada."""

    id: int
    tipo_aportacion_id: int
    operacion: OperacionAportacion
    monto: Decimal
    fecha: datetime
    descripcion: str | None = None
    socio_id: int
    usuario_cajero_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

