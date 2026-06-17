"""Archivo: app/database.py
Descripcion: Conexion SQLAlchemy y dependencia de sesion de base de datos.
Autor: Martinez Steeven
Version: 1.0
"""

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import obtener_configuracion


configuracion = obtener_configuracion()

argumentos_conexion = {}
if configuracion.database_url.startswith("sqlite"):
    argumentos_conexion = {"check_same_thread": False}

engine = create_engine(configuracion.database_url, connect_args=argumentos_conexion)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def obtener_db():
    """Abre una sesion de base de datos y la cierra al finalizar la peticion."""

    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()


def aplicar_migraciones_ligeras():
    """Agrega columnas simples cuando existe una base local creada por una version anterior."""

    inspector = inspect(engine)
    if "socios" in inspector.get_table_names():
        columnas = {columna["name"] for columna in inspector.get_columns("socios")}
        if "usuario_id" not in columnas:
            with engine.begin() as conexion:
                conexion.execute(text("ALTER TABLE socios ADD COLUMN usuario_id INTEGER"))
