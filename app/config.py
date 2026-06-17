"""Archivo: app/config.py
Descripcion: Configuracion centralizada por variables de entorno.
Autor: Martinez Steeven
Version: 1.0
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    """Representa la configuracion general de la aplicacion."""

    nombre_app: str = "Sistema de Gestion de Caja de Ahorros"
    version: str = "1.0"
    database_url: str = "sqlite:///./caja_ahorros.db"
    clave_jwt: str = "clave-academica-cambiar-en-produccion"
    algoritmo_jwt: str = "HS256"
    minutos_expiracion_jwt: int = 480
    api_key_externa: str = "API-KEY-DEMO-123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def obtener_configuracion() -> Configuracion:
    """Devuelve una instancia cacheada de configuracion."""

    return Configuracion()

