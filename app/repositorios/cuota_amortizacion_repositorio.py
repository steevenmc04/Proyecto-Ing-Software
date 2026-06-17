"""Archivo: app/repositorios/cuota_amortizacion_repositorio.py
Descripcion: Consultas de cuotas de amortizacion.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.modelos.cuota_amortizacion_modelo import EstadoCuota, CuotaAmortizacion
from app.repositorios.base_repositorio import RepositorioBase


class CuotaAmortizacionRepositorio(RepositorioBase):
    """Repositorio de cuotas de amortizacion."""

    def __init__(self):
        super().__init__(CuotaAmortizacion)

    def listar_por_credito(self, db: Session, credito_id: int):
        """Lista cuotas de un credito por numero de cuota."""

        return db.query(CuotaAmortizacion).filter(CuotaAmortizacion.credito_id == credito_id).order_by(CuotaAmortizacion.numero_cuota.asc()).all()

    def obtener_siguiente_pendiente(self, db: Session, credito_id: int):
        """Obtiene la primera cuota pendiente para registrar pago secuencial."""

        return (
            db.query(CuotaAmortizacion)
            .filter(CuotaAmortizacion.credito_id == credito_id, CuotaAmortizacion.estado == EstadoCuota.PENDIENTE)
            .order_by(CuotaAmortizacion.numero_cuota.asc())
            .first()
        )


cuota_amortizacion_repositorio = CuotaAmortizacionRepositorio()

