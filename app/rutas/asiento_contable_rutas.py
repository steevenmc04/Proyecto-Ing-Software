"""Archivo: app/rutas/asiento_contable_rutas.py
Descripcion: Rutas REST del libro diario contable.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import asiento_contable_controlador
from app.database import obtener_db
from app.esquemas.asiento_contable_esquema import AsientoContableRespuesta


router = APIRouter()


@router.get("", response_model=list[AsientoContableRespuesta], summary="Listar asientos contables")
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(obtener_db)):
    """Lista asientos del libro diario."""

    return asiento_contable_controlador.listar(db, skip, limit)


@router.get("/rango-fechas", response_model=list[AsientoContableRespuesta], summary="Asientos por rango de fechas")
def rango_fechas(fecha_inicio: date | None = None, fecha_fin: date | None = None, db: Session = Depends(obtener_db)):
    """Filtra asientos por fecha inicial y final."""

    return asiento_contable_controlador.rango_fechas(db, fecha_inicio, fecha_fin)


@router.get("/{id}", response_model=AsientoContableRespuesta, summary="Obtener asiento contable")
def obtener(id: int, db: Session = Depends(obtener_db)):
    """Consulta un asiento por ID."""

    return asiento_contable_controlador.obtener(db, id)

