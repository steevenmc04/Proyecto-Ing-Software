"""Archivo: app/main.py
Descripcion: Punto de entrada FastAPI del Sistema de Gestion de Caja de Ahorros.
Autor: Martinez Steeven
Version: 1.0
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import obtener_configuracion
from app.database import Base, aplicar_migraciones_ligeras, engine
from app.modelos import *  # noqa: F401,F403 - registra modelos antes de crear tablas
from app.rutas import (
    api_externa_rutas,
    aportacion_rutas,
    asiento_contable_rutas,
    auth_rutas,
    credito_rutas,
    cuenta_ahorro_rutas,
    cuota_amortizacion_rutas,
    reporte_rutas,
    socio_rutas,
    transaccion_rutas,
    usuario_rutas,
)


configuracion = obtener_configuracion()
raiz_proyecto = Path(__file__).resolve().parents[1]
directorio_frontend = raiz_proyecto / "frontend" / "dist"
indice_frontend = directorio_frontend / "index.html"

Base.metadata.create_all(bind=engine)
aplicar_migraciones_ligeras()

app = FastAPI(
    title=configuracion.nombre_app,
    version=configuracion.version,
    description=(
        "Backend academico T02.03 para administrar socios, cuentas de ahorro, "
        "transacciones, aportaciones, creditos, amortizacion, libro diario, reportes "
        "y una API REST externa."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=configuracion.lista_origenes_cors,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-API-KEY"],
)

if (directorio_frontend.joinpath("assets").is_dir()):
    app.mount(
        "/assets",
        StaticFiles(directory=directorio_frontend / "assets"),
        name="frontend-assets",
    )

app.include_router(auth_rutas.router, prefix="/api/v1/auth", tags=["Autenticacion"])
app.include_router(usuario_rutas.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
app.include_router(socio_rutas.router, prefix="/api/v1/socios", tags=["Socios"])
app.include_router(cuenta_ahorro_rutas.router, prefix="/api/v1/cuentas", tags=["Cuentas de ahorro"])
app.include_router(transaccion_rutas.router, prefix="/api/v1/transacciones", tags=["Transacciones"])
app.include_router(aportacion_rutas.router, prefix="/api/v1/aportaciones", tags=["Aportaciones"])
app.include_router(credito_rutas.router, prefix="/api/v1/creditos", tags=["Creditos"])
app.include_router(cuota_amortizacion_rutas.router, prefix="/api/v1/cuotas", tags=["Cuotas de amortizacion"])
app.include_router(asiento_contable_rutas.router, prefix="/api/v1/asientos", tags=["Libro diario"])
app.include_router(reporte_rutas.router, prefix="/api/v1/reportes", tags=["Reportes"])
app.include_router(api_externa_rutas.router, prefix="/api/v1/cuenta", tags=["API externa"])


@app.get("/", include_in_schema=False)
def pagina_inicio():
    """Sirve el frontend compilado o dirige a Swagger si aun no existe."""

    if indice_frontend.is_file():
        return FileResponse(indice_frontend)
    return RedirectResponse("/docs")


@app.get("/salud", tags=["Salud"], summary="Verificar estado de la API")
def raiz():
    """Confirma que la API esta operativa y muestra las rutas de documentacion."""

    return {"mensaje": "Sistema de Gestion de Caja de Ahorros API", "swagger": "/docs", "redoc": "/redoc"}


@app.get("/api/v1/salud", tags=["Salud"], summary="Verificar estado versionado de la API")
def salud():
    """Devuelve el estado estable esperado por clientes y monitoreo."""

    return {"estado": "correcto", "aplicacion": configuracion.nombre_app}


@app.get("/{ruta_frontend:path}", include_in_schema=False)
def pagina_frontend(ruta_frontend: str):
    """Resuelve rutas y archivos del frontend React compilado."""

    if ruta_frontend.startswith(("api/", "docs", "redoc", "openapi.json")):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    archivo = directorio_frontend / ruta_frontend
    if archivo.is_file() and directorio_frontend in archivo.resolve().parents:
        return FileResponse(archivo)
    if indice_frontend.is_file():
        return FileResponse(indice_frontend)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Frontend no compilado. Ejecuta npm run build dentro de frontend.",
    )
