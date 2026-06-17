"""Archivo: app/rutas/aportacion_rutas.py
Descripcion: Rutas REST para aportaciones.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import aportacion_controlador
from app.database import obtener_db
from app.esquemas.aportacion_esquema import AportacionCrear, AportacionRespuesta, TipoAportacionCrear, TipoAportacionRespuesta


router = APIRouter()


@router.post("/tipos", response_model=TipoAportacionRespuesta, summary="Crear tipo de aportacion")
def crear_tipo(datos: TipoAportacionCrear, db: Session = Depends(obtener_db)):
    """Crea un tipo de aportacion ORDINARIA o EXTRAORDINARIA."""

    return aportacion_controlador.crear_tipo(db, datos)


@router.get("/tipos", response_model=list[TipoAportacionRespuesta], summary="Listar tipos de aportacion")
def listar_tipos(db: Session = Depends(obtener_db)):
    """Lista catalogo de tipos de aportacion."""

    return aportacion_controlador.listar_tipos(db)


@router.post("/deposito", response_model=AportacionRespuesta, summary="Registrar deposito de aportacion")
def deposito(datos: AportacionCrear, db: Session = Depends(obtener_db)):
    """Registra deposito de aportacion y asiento contable."""

    return aportacion_controlador.deposito(db, datos)


@router.post("/retiro", response_model=AportacionRespuesta, summary="Registrar retiro de aportacion")
def retiro(datos: AportacionCrear, db: Session = Depends(obtener_db)):
    """Retira aportacion validando antiguedad minima de seis meses."""

    return aportacion_controlador.retiro(db, datos)


@router.get("", response_model=list[AportacionRespuesta], summary="Listar aportaciones")
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(obtener_db)):
    """Lista movimientos de aportaciones."""

    return aportacion_controlador.listar(db, skip, limit)


@router.get("/socio/{socio_id}", response_model=list[AportacionRespuesta], summary="Aportaciones por socio")
def listar_por_socio(socio_id: int, db: Session = Depends(obtener_db)):
    """Lista aportaciones asociadas a un socio."""

    return aportacion_controlador.listar_por_socio(db, socio_id)

