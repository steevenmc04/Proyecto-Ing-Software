"""Archivo: app/repositorios/transaccion_repositorio.py
Descripcion: Consultas especificas para transacciones.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.modelos.transaccion_modelo import Transaccion
from app.repositorios.base_repositorio import RepositorioBase


class TransaccionRepositorio(RepositorioBase):
    """Repositorio de transacciones."""

    def __init__(self):
        super().__init__(Transaccion)

    def listar_por_cuenta(self, db: Session, cuenta_id: int, limit: int | None = None):
        """Lista movimientos de una cuenta ordenados del mas reciente al mas antiguo."""

        consulta = db.query(Transaccion).filter(Transaccion.cuenta_id == cuenta_id).order_by(Transaccion.fecha.desc(), Transaccion.id.desc())
        if limit:
            consulta = consulta.limit(limit)
        return consulta.all()


transaccion_repositorio = TransaccionRepositorio()

