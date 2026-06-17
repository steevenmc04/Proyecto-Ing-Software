"""Archivo: app/repositorios/base_repositorio.py
Descripcion: Operaciones CRUD comunes para repositorios.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy.orm import Session


class RepositorioBase:
    """Repositorio generico para reducir codigo repetido."""

    def __init__(self, modelo):
        """Inicializa el repositorio con el modelo SQLAlchemy que administrara."""

        self.modelo = modelo

    def listar(self, db: Session, skip: int = 0, limit: int = 100):
        """Lista registros con paginacion basica."""

        return db.query(self.modelo).offset(skip).limit(limit).all()

    def obtener(self, db: Session, id: int):
        """Obtiene un registro por su identificador."""

        return db.query(self.modelo).filter(self.modelo.id == id).first()

    def guardar(self, db: Session, instancia):
        """Guarda una instancia y refresca sus datos."""

        db.add(instancia)
        db.commit()
        db.refresh(instancia)
        return instancia
