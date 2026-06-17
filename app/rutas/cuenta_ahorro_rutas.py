"""Archivo: app/rutas/cuenta_ahorro_rutas.py
Descripcion: Rutas REST para cuentas de ahorro.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import cuenta_ahorro_controlador
from app.database import obtener_db
from app.dependencias import obtener_usuario_actual
from app.esquemas.cuenta_ahorro_esquema import CuentaAhorroCrear, CuentaAhorroRespuesta


router = APIRouter()


@router.post("", response_model=CuentaAhorroRespuesta, summary="Crear cuenta de ahorro")
def crear(datos: CuentaAhorroCrear, db: Session = Depends(obtener_db)):
    """Crea una cuenta para un socio con saldo inicial cero."""

    return cuenta_ahorro_controlador.crear(db, datos.socio_id)


@router.get("", response_model=list[CuentaAhorroRespuesta], summary="Listar cuentas")
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(obtener_db)):
    """Lista cuentas de ahorro existentes."""

    return cuenta_ahorro_controlador.listar(db, skip, limit)


@router.get("/mis-cuentas", response_model=list[CuentaAhorroRespuesta], summary="Listar cuentas permitidas")
def mis_cuentas(db: Session = Depends(obtener_db), usuario=Depends(obtener_usuario_actual)):
    """Lista todas las cuentas para personal interno y solo las propias para socios."""

    return cuenta_ahorro_controlador.listar_para_usuario(db, usuario)


@router.get("/socio/{socio_id}", response_model=list[CuentaAhorroRespuesta], summary="Listar cuentas por socio")
def listar_por_socio(socio_id: int, db: Session = Depends(obtener_db)):
    """Lista cuentas asociadas a un socio."""

    return cuenta_ahorro_controlador.listar_por_socio(db, socio_id)


@router.get("/numero/{numero_cuenta}", response_model=CuentaAhorroRespuesta, summary="Obtener cuenta por numero")
def obtener_por_numero(numero_cuenta: str, db: Session = Depends(obtener_db)):
    """Consulta una cuenta usando su numero unico."""

    return cuenta_ahorro_controlador.obtener_por_numero(db, numero_cuenta)


@router.get("/{id}", response_model=CuentaAhorroRespuesta, summary="Obtener cuenta por ID")
def obtener(id: int, db: Session = Depends(obtener_db)):
    """Consulta una cuenta por ID."""

    return cuenta_ahorro_controlador.obtener(db, id)


@router.patch("/{id}/bloquear", response_model=CuentaAhorroRespuesta, summary="Bloquear cuenta")
def bloquear(id: int, db: Session = Depends(obtener_db)):
    """Bloquea la cuenta para impedir operaciones."""

    return cuenta_ahorro_controlador.bloquear(db, id)


@router.patch("/{id}/desbloquear", response_model=CuentaAhorroRespuesta, summary="Desbloquear cuenta")
def desbloquear(id: int, db: Session = Depends(obtener_db)):
    """Devuelve la cuenta al estado ACTIVA."""

    return cuenta_ahorro_controlador.desbloquear(db, id)


@router.patch("/{id}/cerrar", response_model=CuentaAhorroRespuesta, summary="Cerrar cuenta")
def cerrar(id: int, db: Session = Depends(obtener_db)):
    """Cierra la cuenta e impide nuevas operaciones."""

    return cuenta_ahorro_controlador.cerrar(db, id)
