"""Archivo: app/rutas/api_externa_rutas.py
Descripcion: Ruta publica externa protegida por X-API-KEY.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from app.controladores import cuenta_ahorro_controlador
from app.database import obtener_db
from app.esquemas.cuenta_ahorro_esquema import CuentaMovimientosExternoRespuesta


router = APIRouter()


@router.get("/movimientos", response_model=CuentaMovimientosExternoRespuesta, summary="Consultar saldo y ultimos movimientos")
def movimientos(
    cedula: str = Query(..., description="Cedula del socio"),
    numeroCuenta: str = Query(..., description="Numero de cuenta de ahorro"),
    x_api_key: str | None = Header(default=None, alias="X-API-KEY"),
    db: Session = Depends(obtener_db),
):
    """Valida X-API-KEY y devuelve saldo mas los ultimos tres movimientos reales."""

    return cuenta_ahorro_controlador.movimientos_externos(db, cedula, numeroCuenta, x_api_key)

