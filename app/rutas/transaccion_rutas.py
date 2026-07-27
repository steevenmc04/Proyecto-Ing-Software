"""Archivo: app/rutas/transaccion_rutas.py
Descripcion: Rutas REST para depositos y retiros.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import transaccion_controlador
from app.database import obtener_db
from app.dependencias import obtener_usuario_actual, requerir_roles
from app.esquemas.transaccion_esquema import TransaccionCrear, TransaccionRespuesta
from app.modelos.usuario_modelo import RolUsuario


router = APIRouter()


@router.post(
    "/deposito",
    response_model=TransaccionRespuesta,
    summary="Registrar deposito",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO))],
)
def deposito(datos: TransaccionCrear, db: Session = Depends(obtener_db)):
    """Registra deposito, aumenta saldo y genera asiento contable."""

    return transaccion_controlador.deposito(db, datos)


@router.post(
    "/retiro",
    response_model=TransaccionRespuesta,
    summary="Registrar retiro",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO))],
)
def retiro(datos: TransaccionCrear, db: Session = Depends(obtener_db)):
    """Registra retiro si existe saldo suficiente y genera asiento contable."""

    return transaccion_controlador.retiro(db, datos)


@router.get(
    "",
    response_model=list[TransaccionRespuesta],
    summary="Listar transacciones",
    dependencies=[
        Depends(
            requerir_roles(
                RolUsuario.ADMINISTRADOR,
                RolUsuario.GERENTE,
                RolUsuario.CAJERO,
                RolUsuario.CONTADOR,
            )
        )
    ],
)
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(obtener_db)):
    """Lista depositos y retiros registrados."""

    return transaccion_controlador.listar(db, skip, limit)


@router.get("/mis-transacciones", response_model=list[TransaccionRespuesta], summary="Listar transacciones permitidas")
def mis_transacciones(db: Session = Depends(obtener_db), usuario=Depends(obtener_usuario_actual)):
    """Lista todas las transacciones para personal interno y solo las propias para socios."""

    return transaccion_controlador.listar_para_usuario(db, usuario)


@router.get(
    "/cuenta/{cuenta_id}",
    response_model=list[TransaccionRespuesta],
    summary="Transacciones por cuenta",
    dependencies=[
        Depends(
            requerir_roles(
                RolUsuario.ADMINISTRADOR,
                RolUsuario.GERENTE,
                RolUsuario.CAJERO,
                RolUsuario.CONTADOR,
            )
        )
    ],
)
def listar_por_cuenta(cuenta_id: int, db: Session = Depends(obtener_db)):
    """Lista movimientos de una cuenta por ID."""

    return transaccion_controlador.listar_por_cuenta(db, cuenta_id)


@router.get(
    "/{id}",
    response_model=TransaccionRespuesta,
    summary="Obtener transaccion",
    dependencies=[
        Depends(
            requerir_roles(
                RolUsuario.ADMINISTRADOR,
                RolUsuario.GERENTE,
                RolUsuario.CAJERO,
                RolUsuario.CONTADOR,
            )
        )
    ],
)
def obtener(id: int, db: Session = Depends(obtener_db)):
    """Consulta una transaccion por ID."""

    return transaccion_controlador.obtener(db, id)
