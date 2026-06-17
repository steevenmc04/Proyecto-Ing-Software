"""Archivo: app/servicios/asiento_contable_servicio.py
Descripcion: Servicio para generar y consultar asientos contables.
Autor: Martinez Steeven
Version: 1.0
"""

from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modelos.asiento_contable_modelo import AsientoContable, TipoOrigenAsiento
from app.repositorios.asiento_contable_repositorio import asiento_contable_repositorio


class AsientoContableServicio:
    """Gestiona el libro diario y valida partida doble."""

    def crear_automatico(
        self,
        db: Session,
        descripcion: str,
        cuenta_debito: str,
        cuenta_credito: str,
        monto: Decimal,
        tipo_origen: TipoOrigenAsiento,
        transaccion_id: int | None = None,
        credito_id: int | None = None,
        aportacion_id: int | None = None,
    ) -> AsientoContable:
        """Crea un asiento desde un servicio financiero sin confirmar la transaccion aun."""

        if monto <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El monto del asiento debe ser mayor a 0")
        asiento = AsientoContable(
            descripcion=descripcion,
            cuenta_debito=cuenta_debito,
            cuenta_credito=cuenta_credito,
            monto=monto,
            tipo_origen=tipo_origen,
            transaccion_id=transaccion_id,
            credito_id=credito_id,
            aportacion_id=aportacion_id,
        )
        db.add(asiento)
        db.flush()
        return asiento

    def listar(self, db: Session, skip: int = 0, limit: int = 100):
        """Lista asientos contables."""

        return asiento_contable_repositorio.listar(db, skip, limit)

    def obtener(self, db: Session, asiento_id: int):
        """Obtiene un asiento por ID o devuelve 404."""

        asiento = asiento_contable_repositorio.obtener(db, asiento_id)
        if not asiento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asiento contable no encontrado")
        return asiento

    def listar_rango_fechas(self, db: Session, fecha_inicio, fecha_fin):
        """Lista asientos entre fechas para reportes contables."""

        return asiento_contable_repositorio.listar_rango_fechas(db, fecha_inicio, fecha_fin)


asiento_contable_servicio = AsientoContableServicio()

