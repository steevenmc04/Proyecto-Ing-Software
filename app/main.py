"""Archivo: app/main.py
Descripcion: Punto de entrada FastAPI del Sistema de Gestion de Caja de Ahorros.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import FastAPI

from app.config import obtener_configuracion
from app.database import Base, engine
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

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=configuracion.nombre_app,
    version=configuracion.version,
    description=(
        "Backend academico T02.03 para administrar socios, cuentas de ahorro, "
        "transacciones, aportaciones, creditos, amortizacion, libro diario, reportes "
        "y una API REST externa."
    ),
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


@app.get("/", tags=["Salud"], summary="Verificar estado de la API")
def raiz():
    """Confirma que la API esta operativa y muestra las rutas de documentacion."""

    return {"mensaje": "Sistema de Gestion de Caja de Ahorros API", "swagger": "/docs", "redoc": "/redoc"}

