"""Archivo: app/esquemas/credito_esquema.py
Descripcion: Esquemas para solicitud, aprobacion y pago de creditos.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.modelos.credito_modelo import EstadoCredito


class CreditoSolicitar(BaseModel):
    """Datos para solicitar un credito."""

    socio_id: int
    monto_solicitado: Decimal = Field(..., gt=0)
    plazo_meses: int = Field(..., gt=0, le=120)
    tasa_interes: Decimal = Field(..., ge=0, le=100)
    tipo_garantia: str
    proposito: str


class CreditoAprobar(BaseModel):
    """Datos para aprobar un credito pendiente."""

    gerente_aprobador_id: int | None = None
    monto_aprobado: Decimal | None = Field(default=None, gt=0)


class CreditoRechazar(BaseModel):
    """Motivo de rechazo de una solicitud."""

    motivo_rechazo: str = Field(..., min_length=5, max_length=250)


class CreditoDesembolsar(BaseModel):
    """Datos del cajero que desembolsa el credito."""

    cajero_desembolso_id: int | None = None


class PagoCuotaSolicitud(BaseModel):
    """Solicitud para pagar la siguiente cuota pendiente."""

    usuario_cajero_id: int | None = None


class CreditoRespuesta(BaseModel):
    """Respuesta completa de credito."""

    id: int
    numero_credito: str
    socio_id: int
    monto_solicitado: Decimal
    monto_aprobado: Decimal | None = None
    plazo_meses: int
    tasa_interes: Decimal
    tipo_garantia: str
    proposito: str
    estado: EstadoCredito
    fecha_solicitud: datetime
    fecha_aprobacion: datetime | None = None
    motivo_rechazo: str | None = None
    gerente_aprobador_id: int | None = None
    cajero_desembolso_id: int | None = None
    saldo_pendiente: Decimal

    model_config = ConfigDict(from_attributes=True)

