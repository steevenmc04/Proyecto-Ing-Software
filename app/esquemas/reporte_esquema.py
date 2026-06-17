"""Archivo: app/esquemas/reporte_esquema.py
Descripcion: Esquemas de reportes JSON del sistema.
Autor: Martinez Steeven
Version: 1.0
"""

from decimal import Decimal

from pydantic import BaseModel

from app.esquemas.aportacion_esquema import AportacionRespuesta
from app.esquemas.asiento_contable_esquema import AsientoContableRespuesta
from app.esquemas.credito_esquema import CreditoRespuesta
from app.esquemas.transaccion_esquema import TransaccionRespuesta


class ReporteLibroDiario(BaseModel):
    """Reporte del libro diario en formato JSON."""

    total: Decimal
    asientos: list[AsientoContableRespuesta]


class ReporteHistorialAhorros(BaseModel):
    """Reporte de depositos y retiros de un socio."""

    socio_id: int
    movimientos: list[TransaccionRespuesta]


class ReporteCarteraCreditos(BaseModel):
    """Reporte de cartera crediticia vigente."""

    total_creditos: int
    saldo_total_pendiente: Decimal
    creditos: list[CreditoRespuesta]


class ReporteResumenAportaciones(BaseModel):
    """Reporte de aportaciones totalizadas por tipo."""

    socio_id: int
    total: Decimal
    totales_por_tipo: dict[str, Decimal]
    aportaciones: list[AportacionRespuesta]

