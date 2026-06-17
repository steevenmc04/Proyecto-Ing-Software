"""Archivo: app/esquemas/cuota_amortizacion_esquema.py
Descripcion: Esquemas para cuotas de amortizacion.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.modelos.cuota_amortizacion_modelo import EstadoCuota


class CuotaAmortizacionRespuesta(BaseModel):
    """Respuesta de una cuota generada por metodo frances."""

    id: int
    credito_id: int
    numero_cuota: int
    fecha_vencimiento: date
    capital: Decimal
    interes: Decimal
    cuota_total: Decimal
    saldo_pendiente: Decimal
    estado: EstadoCuota

    model_config = ConfigDict(from_attributes=True)

