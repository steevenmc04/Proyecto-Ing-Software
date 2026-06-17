"""Archivo: run.py
Descripcion: Script opcional para ejecutar el servidor Uvicorn.
Autor: Martinez Steeven
Version: 1.0
"""

import uvicorn


def main():
    """Ejecuta la API en modo desarrollo."""

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()

