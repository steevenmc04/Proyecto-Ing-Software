"""Archivo: app/repositorios/credito_repositorio.py
Descripcion: Consultas especificas para creditos.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.modelos.credito_modelo import Credito
from app.repositorios.base_repositorio import RepositorioBase


class CreditoRepositorio(RepositorioBase):
    """Repositorio de creditos."""

    def __init__(self):
        """Inicializa el repositorio con el modelo Credito."""

        super().__init__(Credito)

    def listar_por_socio(self, db: Session, socio_id: int):
        """Lista creditos solicitados por un socio."""

        return db.query(Credito).filter(Credito.socio_id == socio_id).all()


credito_repositorio = CreditoRepositorio()
