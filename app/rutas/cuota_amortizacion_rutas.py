"""Archivo: app/rutas/cuota_amortizacion_rutas.py
Descripcion: Rutas REST para consulta individual de cuotas.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controladores import credito_controlador
from app.database import obtener_db
from app.dependencias import requerir_roles
from app.esquemas.cuota_amortizacion_esquema import CuotaAmortizacionRespuesta
from app.modelos.usuario_modelo import RolUsuario


router = APIRouter(
    dependencies=[
        Depends(
            requerir_roles(
                RolUsuario.ADMINISTRADOR,
                RolUsuario.GERENTE,
                RolUsuario.CAJERO,
                RolUsuario.CONTADOR,
            )
        )
    ]
)


@router.get("/{id}", response_model=CuotaAmortizacionRespuesta, summary="Obtener cuota")
def obtener(id: int, db: Session = Depends(obtener_db)):
    """Consulta una cuota de amortizacion por ID."""

    return credito_controlador.obtener_cuota(db, id)
