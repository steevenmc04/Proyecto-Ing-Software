"""Archivo: app/rutas/credito_rutas.py
Descripcion: Rutas REST para creditos y cuotas.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import credito_controlador
from app.database import obtener_db
from app.esquemas.credito_esquema import CreditoAprobar, CreditoDesembolsar, CreditoRechazar, CreditoRespuesta, CreditoSolicitar, PagoCuotaSolicitud
from app.esquemas.cuota_amortizacion_esquema import CuotaAmortizacionRespuesta


router = APIRouter()


@router.post("/solicitar", response_model=CreditoRespuesta, summary="Solicitar credito")
def solicitar(datos: CreditoSolicitar, db: Session = Depends(obtener_db)):
    """Registra una solicitud de credito con estado PENDIENTE."""

    return credito_controlador.solicitar(db, datos)


@router.get("", response_model=list[CreditoRespuesta], summary="Listar creditos")
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(obtener_db)):
    """Lista creditos registrados."""

    return credito_controlador.listar(db, skip, limit)


@router.get("/socio/{socio_id}", response_model=list[CreditoRespuesta], summary="Creditos por socio")
def listar_por_socio(socio_id: int, db: Session = Depends(obtener_db)):
    """Lista creditos solicitados por un socio."""

    return credito_controlador.listar_por_socio(db, socio_id)


@router.get("/{id}", response_model=CreditoRespuesta, summary="Obtener credito")
def obtener(id: int, db: Session = Depends(obtener_db)):
    """Consulta un credito por ID."""

    return credito_controlador.obtener(db, id)


@router.patch("/{id}/aprobar", response_model=CreditoRespuesta, summary="Aprobar credito")
def aprobar(id: int, datos: CreditoAprobar = CreditoAprobar(), db: Session = Depends(obtener_db)):
    """Aprueba credito pendiente y genera cuotas con metodo frances."""

    return credito_controlador.aprobar(db, id, datos)


@router.patch("/{id}/rechazar", response_model=CreditoRespuesta, summary="Rechazar credito")
def rechazar(id: int, datos: CreditoRechazar, db: Session = Depends(obtener_db)):
    """Rechaza credito pendiente guardando motivo de rechazo."""

    return credito_controlador.rechazar(db, id, datos)


@router.patch("/{id}/desembolsar", response_model=CreditoRespuesta, summary="Desembolsar credito")
def desembolsar(id: int, datos: CreditoDesembolsar = CreditoDesembolsar(), db: Session = Depends(obtener_db)):
    """Desembolsa credito aprobado y genera asiento contable."""

    return credito_controlador.desembolsar(db, id, datos)


@router.post("/{id}/pagar-cuota", response_model=CuotaAmortizacionRespuesta, summary="Pagar siguiente cuota")
def pagar_cuota(id: int, datos: PagoCuotaSolicitud = PagoCuotaSolicitud(), db: Session = Depends(obtener_db)):
    """Paga la siguiente cuota pendiente, actualiza saldo y genera asiento."""

    return credito_controlador.pagar_cuota(db, id, datos)


@router.get("/{id}/cuotas", response_model=list[CuotaAmortizacionRespuesta], summary="Listar cuotas del credito")
def listar_cuotas(id: int, db: Session = Depends(obtener_db)):
    """Lista tabla de amortizacion del credito."""

    return credito_controlador.listar_cuotas(db, id)

