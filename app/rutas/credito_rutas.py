"""Archivo: app/rutas/credito_rutas.py
Descripcion: Rutas REST para creditos y cuotas.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controladores import credito_controlador
from app.database import obtener_db
from app.dependencias import obtener_usuario_actual, requerir_roles
from app.esquemas.credito_esquema import CreditoAprobar, CreditoDesembolsar, CreditoRechazar, CreditoRespuesta, CreditoSolicitar, PagoCuotaSolicitud
from app.esquemas.cuota_amortizacion_esquema import CuotaAmortizacionRespuesta
from app.modelos.usuario_modelo import RolUsuario
from app.repositorios.socio_repositorio import socio_repositorio


router = APIRouter()


@router.post("/solicitar", response_model=CreditoRespuesta, summary="Solicitar credito")
def solicitar(
    datos: CreditoSolicitar,
    db: Session = Depends(obtener_db),
    usuario=Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO, RolUsuario.SOCIO)),
):
    """Registra una solicitud de credito con estado PENDIENTE."""

    if usuario.rol == RolUsuario.SOCIO:
        socio = socio_repositorio.obtener_por_usuario(db, usuario.id)
        if not socio or socio.id != datos.socio_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Un socio solo puede solicitar creditos para su propio perfil",
            )
    return credito_controlador.solicitar(db, datos)


@router.get(
    "",
    response_model=list[CreditoRespuesta],
    summary="Listar creditos",
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
    """Lista creditos registrados."""

    return credito_controlador.listar(db, skip, limit)


@router.get("/mis-creditos", response_model=list[CreditoRespuesta], summary="Listar creditos permitidos")
def mis_creditos(db: Session = Depends(obtener_db), usuario=Depends(obtener_usuario_actual)):
    """Lista todos los creditos para personal interno y solo los propios para socios."""

    return credito_controlador.listar_para_usuario(db, usuario)


@router.get(
    "/socio/{socio_id}",
    response_model=list[CreditoRespuesta],
    summary="Creditos por socio",
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
def listar_por_socio(socio_id: int, db: Session = Depends(obtener_db)):
    """Lista creditos solicitados por un socio."""

    return credito_controlador.listar_por_socio(db, socio_id)


@router.get(
    "/{id}",
    response_model=CreditoRespuesta,
    summary="Obtener credito",
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
    """Consulta un credito por ID."""

    return credito_controlador.obtener(db, id)


@router.patch(
    "/{id}/aprobar",
    response_model=CreditoRespuesta,
    summary="Aprobar credito",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.GERENTE))],
)
def aprobar(id: int, datos: CreditoAprobar = CreditoAprobar(), db: Session = Depends(obtener_db)):
    """Aprueba credito pendiente y genera cuotas con metodo frances."""

    return credito_controlador.aprobar(db, id, datos)


@router.patch(
    "/{id}/rechazar",
    response_model=CreditoRespuesta,
    summary="Rechazar credito",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.GERENTE))],
)
def rechazar(id: int, datos: CreditoRechazar, db: Session = Depends(obtener_db)):
    """Rechaza credito pendiente guardando motivo de rechazo."""

    return credito_controlador.rechazar(db, id, datos)


@router.patch(
    "/{id}/desembolsar",
    response_model=CreditoRespuesta,
    summary="Desembolsar credito",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO))],
)
def desembolsar(id: int, datos: CreditoDesembolsar = CreditoDesembolsar(), db: Session = Depends(obtener_db)):
    """Desembolsa credito aprobado y genera asiento contable."""

    return credito_controlador.desembolsar(db, id, datos)


@router.post(
    "/{id}/pagar-cuota",
    response_model=CuotaAmortizacionRespuesta,
    summary="Pagar siguiente cuota",
    dependencies=[Depends(requerir_roles(RolUsuario.ADMINISTRADOR, RolUsuario.CAJERO))],
)
def pagar_cuota(id: int, datos: PagoCuotaSolicitud = PagoCuotaSolicitud(), db: Session = Depends(obtener_db)):
    """Paga la siguiente cuota pendiente, actualiza saldo y genera asiento."""

    return credito_controlador.pagar_cuota(db, id, datos)


@router.get(
    "/{id}/cuotas",
    response_model=list[CuotaAmortizacionRespuesta],
    summary="Listar cuotas del credito",
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
def listar_cuotas(id: int, db: Session = Depends(obtener_db)):
    """Lista tabla de amortizacion del credito."""

    return credito_controlador.listar_cuotas(db, id)
