"""Archivo: app/repositorios/aportacion_repositorio.py
Descripcion: Consultas para tipos y movimientos de aportacion.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.modelos.aportacion_modelo import Aportacion
from app.modelos.tipo_aportacion_modelo import TipoAportacion
from app.repositorios.base_repositorio import RepositorioBase


class TipoAportacionRepositorio(RepositorioBase):
    """Repositorio del catalogo de tipos de aportacion."""

    def __init__(self):
        """Inicializa el repositorio con el modelo TipoAportacion."""

        super().__init__(TipoAportacion)

    def obtener_por_nombre(self, db: Session, nombre):
        """Busca tipo de aportacion por nombre."""

        return db.query(TipoAportacion).filter(TipoAportacion.nombre == nombre).first()


class AportacionRepositorio(RepositorioBase):
    """Repositorio de aportaciones."""

    def __init__(self):
        """Inicializa el repositorio con el modelo Aportacion."""

        super().__init__(Aportacion)

    def listar_por_socio(self, db: Session, socio_id: int):
        """Lista aportaciones de un socio."""

        return db.query(Aportacion).filter(Aportacion.socio_id == socio_id).order_by(Aportacion.fecha.desc()).all()


tipo_aportacion_repositorio = TipoAportacionRepositorio()
aportacion_repositorio = AportacionRepositorio()
