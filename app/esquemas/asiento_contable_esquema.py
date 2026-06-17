"""Archivo: app/esquemas/asiento_contable_esquema.py
Descripcion: Esquemas del libro diario contable.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.modelos.asiento_contable_modelo import TipoOrigenAsiento


class AsientoContableRespuesta(BaseModel):
    """Respuesta de asiento contable."""

    id: int
    fecha: datetime
    descripcion: str
    cuenta_debito: str
    cuenta_credito: str
    monto: Decimal
    tipo_origen: TipoOrigenAsiento
    transaccion_id: int | None = None
    credito_id: int | None = None
    aportacion_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

