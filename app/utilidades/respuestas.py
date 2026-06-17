"""Archivo: app/utilidades/respuestas.py
Descripcion: Helpers simples para respuestas estandarizadas.
Autor: Martinez Steeven
Version: 1.0
"""


def respuesta_mensaje(mensaje: str) -> dict:
    """Devuelve una respuesta JSON uniforme para operaciones simples."""

    return {"mensaje": mensaje}

