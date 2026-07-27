"""Utilidades de fecha consistentes con las columnas DateTime existentes."""

from datetime import datetime, timezone


def ahora_utc() -> datetime:
    """Devuelve UTC sin zona para conservar compatibilidad con SQL DateTime."""

    return datetime.now(timezone.utc).replace(tzinfo=None)
