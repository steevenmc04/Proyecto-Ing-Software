"""Archivo: app/repositorios/socio_repositorio.py
Descripcion: Consultas especificas para socios.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.modelos.socio_modelo import Socio
from app.repositorios.base_repositorio import RepositorioBase


class SocioRepositorio(RepositorioBase):
    """Repositorio de socios."""

    def __init__(self):
        """Inicializa el repositorio con el modelo Socio."""

        super().__init__(Socio)

    def obtener_por_cedula(self, db: Session, cedula: str):
        """Busca socio por cedula."""

        return db.query(Socio).filter(Socio.cedula == cedula).first()

    def obtener_por_usuario(self, db: Session, usuario_id: int):
        """Busca el socio asociado a un usuario de rol SOCIO."""

        return db.query(Socio).filter(Socio.usuario_id == usuario_id).first()

    def buscar(self, db: Session, termino: str):
        """Busca socios por cedula, nombres o apellidos."""

        filtro = f"%{termino}%"
        return db.query(Socio).filter(or_(Socio.cedula.ilike(filtro), Socio.nombres.ilike(filtro), Socio.apellidos.ilike(filtro))).all()


socio_repositorio = SocioRepositorio()
