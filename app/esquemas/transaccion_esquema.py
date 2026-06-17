"""Archivo: app/esquemas/transaccion_esquema.py
Descripcion: Esquemas para depositos y retiros.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.modelos.transaccion_modelo import TipoTransaccion


class TransaccionCrear(BaseModel):
    """Datos para registrar una transaccion sobre una cuenta."""

    cuenta_id: int
    monto: Decimal = Field(..., gt=0)
    descripcion: str | None = None
    usuario_cajero_id: int | None = None


class TransaccionRespuesta(BaseModel):
    """Respuesta de transaccion con comprobante y saldo resultante."""

    id: int
    numero_comprobante: str
    tipo_transaccion: TipoTransaccion
    monto: Decimal
    fecha: datetime
    descripcion: str | None = None
    saldo_resultante: Decimal
    cuenta_id: int
    usuario_cajero_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

