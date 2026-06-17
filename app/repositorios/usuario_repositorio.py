"""Archivo: app/repositorios/usuario_repositorio.py
Descripcion: Consultas especificas para usuarios.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session

from app.modelos.usuario_modelo import Usuario
from app.repositorios.base_repositorio import RepositorioBase


class UsuarioRepositorio(RepositorioBase):
    """Repositorio de usuarios."""

    def __init__(self):
        super().__init__(Usuario)

    def obtener_por_nombre_usuario(self, db: Session, nombre_usuario: str):
        """Busca usuario por nombre de usuario."""

        return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

    def obtener_por_correo(self, db: Session, correo: str):
        """Busca usuario por correo electronico."""

        return db.query(Usuario).filter(Usuario.correo == correo).first()


usuario_repositorio = UsuarioRepositorio()

