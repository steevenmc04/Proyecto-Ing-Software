"""Archivo: app/modelos/__init__.py
Descripcion: Importa todos los modelos para registrar las tablas SQLAlchemy.
Autor: Martinez Steeven
Version: 1.0
"""

from app.modelos.aportacion_modelo import Aportacion
from app.modelos.asiento_contable_modelo import AsientoContable
from app.modelos.credito_modelo import Credito
from app.modelos.cuenta_ahorro_modelo import CuentaAhorro
from app.modelos.cuota_amortizacion_modelo import CuotaAmortizacion
from app.modelos.socio_modelo import Socio
from app.modelos.tipo_aportacion_modelo import TipoAportacion
from app.modelos.transaccion_modelo import Transaccion
from app.modelos.usuario_modelo import Usuario

__all__ = [
    "Aportacion",
    "AsientoContable",
    "Credito",
    "CuentaAhorro",
    "CuotaAmortizacion",
    "Socio",
    "TipoAportacion",
    "Transaccion",
    "Usuario",
]

