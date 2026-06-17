"""Archivo: app/rutas/transaccion_rutas.py
Descripcion: Rutas REST para depositos y retiros.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import transaccion_controlador
from app.database import obtener_db
from app.esquemas.transaccion_esquema import TransaccionCrear, TransaccionRespuesta


router = APIRouter()


@router.post("/deposito", response_model=TransaccionRespuesta, summary="Registrar deposito")
def deposito(datos: TransaccionCrear, db: Session = Depends(obtener_db)):
    """Registra deposito, aumenta saldo y genera asiento contable."""

    return transaccion_controlador.deposito(db, datos)


@router.post("/retiro", response_model=TransaccionRespuesta, summary="Registrar retiro")
def retiro(datos: TransaccionCrear, db: Session = Depends(obtener_db)):
    """Registra retiro si existe saldo suficiente y genera asiento contable."""

    return transaccion_controlador.retiro(db, datos)


@router.get("", response_model=list[TransaccionRespuesta], summary="Listar transacciones")
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(obtener_db)):
    """Lista depositos y retiros registrados."""

    return transaccion_controlador.listar(db, skip, limit)


@router.get("/cuenta/{cuenta_id}", response_model=list[TransaccionRespuesta], summary="Transacciones por cuenta")
def listar_por_cuenta(cuenta_id: int, db: Session = Depends(obtener_db)):
    """Lista movimientos de una cuenta por ID."""

    return transaccion_controlador.listar_por_cuenta(db, cuenta_id)


@router.get("/{id}", response_model=TransaccionRespuesta, summary="Obtener transaccion")
def obtener(id: int, db: Session = Depends(obtener_db)):
    """Consulta una transaccion por ID."""

    return transaccion_controlador.obtener(db, id)

