"""Archivo: app/repositorios/asiento_contable_repositorio.py
Descripcion: Consultas del libro diario contable.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import date, datetime, time

from sqlalchemy.orm import Session

from app.modelos.asiento_contable_modelo import AsientoContable
from app.repositorios.base_repositorio import RepositorioBase


class AsientoContableRepositorio(RepositorioBase):
    """Repositorio de asientos contables."""

    def __init__(self):
        super().__init__(AsientoContable)

    def listar_rango_fechas(self, db: Session, fecha_inicio: date | None, fecha_fin: date | None):
        """Filtra asientos por rango de fechas opcional."""

        consulta = db.query(AsientoContable)
        if fecha_inicio:
            consulta = consulta.filter(AsientoContable.fecha >= datetime.combine(fecha_inicio, time.min))
        if fecha_fin:
            consulta = consulta.filter(AsientoContable.fecha <= datetime.combine(fecha_fin, time.max))
        return consulta.order_by(AsientoContable.fecha.desc()).all()


asiento_contable_repositorio = AsientoContableRepositorio()

