"""Archivo: app/rutas/socio_rutas.py
Descripcion: Rutas REST para socios.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.controladores import socio_controlador
from app.database import obtener_db
from app.dependencias import obtener_usuario_actual, requerir_roles
from app.esquemas.socio_esquema import SocioActualizar, SocioCrear, SocioRespuesta
from app.modelos.usuario_modelo import RolUsuario


router = APIRouter()


@router.post(
    "",
    response_model=SocioRespuesta,
    summary="Registrar socio",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO))],
)
def crear(datos: SocioCrear, db: Session = Depends(obtener_db)):
    """Registra un socio, valida cedula unica y genera numero de socio."""

    return socio_controlador.crear(db, datos)


@router.get(
    "",
    response_model=list[SocioRespuesta],
    summary="Listar socios",
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
def listar(skip: int = 0, limit: int = 100, buscar: str | None = Query(default=None), db: Session = Depends(obtener_db)):
    """Lista socios o busca por cedula, nombres o apellidos."""

    return socio_controlador.listar(db, skip, limit, buscar)


@router.get(
    "/buscar/cedula/{cedula}",
    response_model=SocioRespuesta,
    summary="Buscar socio por cedula",
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
def obtener_por_cedula(cedula: str, db: Session = Depends(obtener_db)):
    """Busca un socio por cedula."""

    return socio_controlador.obtener_por_cedula(db, cedula)


@router.get("/perfil/me", response_model=SocioRespuesta, summary="Obtener socio del usuario autenticado")
def obtener_mi_socio(db: Session = Depends(obtener_db), usuario=Depends(obtener_usuario_actual)):
    """Devuelve el socio vinculado al usuario autenticado."""

    return socio_controlador.obtener_por_usuario(db, usuario.id)


@router.get(
    "/{id}",
    response_model=SocioRespuesta,
    summary="Obtener socio por ID",
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
    """Consulta un socio por identificador."""

    return socio_controlador.obtener(db, id)


@router.put(
    "/{id}",
    response_model=SocioRespuesta,
    summary="Actualizar socio",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO))],
)
def actualizar(id: int, datos: SocioActualizar, db: Session = Depends(obtener_db)):
    """Actualiza informacion personal del socio."""

    return socio_controlador.actualizar(db, id, datos)


@router.patch(
    "/{id}/activar",
    response_model=SocioRespuesta,
    summary="Activar socio",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO))],
)
def activar(id: int, db: Session = Depends(obtener_db)):
    """Marca el socio como ACTIVO."""

    return socio_controlador.activar(db, id)


@router.patch(
    "/{id}/desactivar",
    response_model=SocioRespuesta,
    summary="Desactivar socio",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO))],
)
def desactivar(id: int, db: Session = Depends(obtener_db)):
    """Marca el socio como INACTIVO."""

    return socio_controlador.desactivar(db, id)
