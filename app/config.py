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
    origenes_cors: str = "http://127.0.0.1:5173,http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def lista_origenes_cors(self) -> list[str]:
        """Convierte la lista separada por comas en origenes CORS validos."""

        return [origen.strip() for origen in self.origenes_cors.split(",") if origen.strip()]


@lru_cache
def obtener_configuracion() -> Configuracion:
    """Devuelve una instancia cacheada de configuracion."""

    return Configuracion()
