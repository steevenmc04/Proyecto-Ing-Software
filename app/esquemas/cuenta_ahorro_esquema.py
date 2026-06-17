"""Archivo: app/esquemas/cuenta_ahorro_esquema.py
Descripcion: Esquemas para cuentas de ahorro y consulta externa.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.modelos.cuenta_ahorro_modelo import EstadoCuenta


class CuentaAhorroCrear(BaseModel):
    """Solicitud de apertura de cuenta para un socio."""

    socio_id: int


class CuentaAhorroRespuesta(BaseModel):
    """Respuesta de cuenta de ahorro."""

    id: int
    numero_cuenta: str
    saldo: Decimal
    fecha_apertura: datetime
    estado: EstadoCuenta
    socio_id: int

    model_config = ConfigDict(from_attributes=True)


class MovimientoExternoRespuesta(BaseModel):
    """Movimiento expuesto por la API externa."""

    tipo: str
    fecha: str
    monto: Decimal


class CuentaMovimientosExternoRespuesta(BaseModel):
    """Respuesta de saldo y ultimos movimientos para integraciones externas."""

    saldo: Decimal
    movimientos: list[MovimientoExternoRespuesta]

