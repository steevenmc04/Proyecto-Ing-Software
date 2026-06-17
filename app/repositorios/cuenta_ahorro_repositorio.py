"""Archivo: app/repositorios/cuenta_ahorro_repositorio.py
Descripcion: Consultas especificas para cuentas de ahorro.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.modelos.cuenta_ahorro_modelo import CuentaAhorro
from app.repositorios.base_repositorio import RepositorioBase


class CuentaAhorroRepositorio(RepositorioBase):
    """Repositorio de cuentas de ahorro."""

    def __init__(self):
        super().__init__(CuentaAhorro)

    def obtener_por_numero(self, db: Session, numero_cuenta: str):
        """Obtiene una cuenta por su numero unico."""

        return db.query(CuentaAhorro).filter(CuentaAhorro.numero_cuenta == numero_cuenta).first()

    def listar_por_socio(self, db: Session, socio_id: int):
        """Lista cuentas pertenecientes a un socio."""

        return db.query(CuentaAhorro).filter(CuentaAhorro.socio_id == socio_id).all()


cuenta_ahorro_repositorio = CuentaAhorroRepositorio()

