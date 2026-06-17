"""Archivo: app/rutas/reporte_rutas.py
Descripcion: Rutas REST para reportes JSON.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import reporte_controlador
from app.database import obtener_db
from app.esquemas.reporte_esquema import ReporteCarteraCreditos, ReporteHistorialAhorros, ReporteLibroDiario, ReporteResumenAportaciones


router = APIRouter()


@router.get("/libro-diario", response_model=ReporteLibroDiario, summary="Reporte de libro diario")
def libro_diario(db: Session = Depends(obtener_db)):
    """Devuelve asientos reales. En este punto se podria integrar exportacion PDF/Excel."""

    return reporte_controlador.libro_diario(db)


@router.get("/historial-ahorros/{socio_id}", response_model=ReporteHistorialAhorros, summary="Reporte de historial de ahorros")
def historial_ahorros(socio_id: int, db: Session = Depends(obtener_db)):
    """Devuelve depositos y retiros reales por socio."""

    return reporte_controlador.historial_ahorros(db, socio_id)


@router.get("/cartera-creditos", response_model=ReporteCarteraCreditos, summary="Reporte de cartera de creditos")
def cartera_creditos(db: Session = Depends(obtener_db)):
    """Devuelve creditos, estados y saldo pendiente total."""

    return reporte_controlador.cartera_creditos(db)


@router.get("/resumen-aportaciones/{socio_id}", response_model=ReporteResumenAportaciones, summary="Resumen de aportaciones")
def resumen_aportaciones(socio_id: int, db: Session = Depends(obtener_db)):
    """Devuelve aportaciones totalizadas por tipo."""

    return reporte_controlador.resumen_aportaciones(db, socio_id)

