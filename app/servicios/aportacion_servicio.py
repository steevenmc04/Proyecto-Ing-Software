"""Archivo: app/servicios/aportacion_servicio.py
Descripcion: Servicio de aportaciones y reglas de retiro a seis meses.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.esquemas.aportacion_esquema import AportacionCrear, TipoAportacionCrear
from app.modelos.aportacion_modelo import Aportacion, OperacionAportacion
from app.modelos.asiento_contable_modelo import TipoOrigenAsiento
from app.modelos.tipo_aportacion_modelo import TipoAportacion
from app.repositorios.aportacion_repositorio import aportacion_repositorio, tipo_aportacion_repositorio
from app.repositorios.socio_repositorio import socio_repositorio
from app.repositorios.usuario_repositorio import usuario_repositorio
from app.servicios.asiento_contable_servicio import asiento_contable_servicio


class AportacionServicio:
    """Gestiona catalogo y movimientos de aportaciones."""

    def crear_tipo(self, db: Session, datos: TipoAportacionCrear):
        """Crea tipo de aportacion si no existe."""

        if tipo_aportacion_repositorio.obtener_por_nombre(db, datos.nombre):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El tipo de aportacion ya existe")
        tipo = TipoAportacion(nombre=datos.nombre, descripcion=datos.descripcion)
        return tipo_aportacion_repositorio.guardar(db, tipo)

    def listar_tipos(self, db: Session):
        """Lista tipos de aportacion."""

        return tipo_aportacion_repositorio.listar(db)

    def _validar_referencias(self, db: Session, datos: AportacionCrear):
        """Valida socio, tipo de aportacion y cajero opcional."""

        socio = socio_repositorio.obtener(db, datos.socio_id)
        if not socio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
        tipo = tipo_aportacion_repositorio.obtener(db, datos.tipo_aportacion_id)
        if not tipo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de aportacion no encontrado")
        if datos.usuario_cajero_id and not usuario_repositorio.obtener(db, datos.usuario_cajero_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario cajero no encontrado")
        return socio, tipo

    def registrar_deposito(self, db: Session, datos: AportacionCrear):
        """Registra deposito, aumenta total real y genera asiento contable."""

        socio, _ = self._validar_referencias(db, datos)
        socio.total_aportaciones = Decimal(socio.total_aportaciones) + datos.monto
        aportacion = Aportacion(
            socio_id=datos.socio_id,
            tipo_aportacion_id=datos.tipo_aportacion_id,
            operacion=OperacionAportacion.DEP,
            monto=datos.monto,
            descripcion=datos.descripcion or "Deposito de aportacion",
            usuario_cajero_id=datos.usuario_cajero_id,
        )
        db.add(aportacion)
        db.flush()
        asiento_contable_servicio.crear_automatico(
            db,
            descripcion="Deposito de aportacion",
            cuenta_debito="Caja/Bancos",
            cuenta_credito="Aportaciones de socios",
            monto=datos.monto,
            tipo_origen=TipoOrigenAsiento.APORTACION,
            aportacion_id=aportacion.id,
        )
        db.commit()
        db.refresh(aportacion)
        return aportacion

    def registrar_retiro(self, db: Session, datos: AportacionCrear):
        """Retira aportaciones solo si existe deposito con antiguedad minima de seis meses."""

        socio, _ = self._validar_referencias(db, datos)
        deposito_antiguo = (
            db.query(Aportacion)
            .filter(
                Aportacion.socio_id == datos.socio_id,
                Aportacion.operacion == OperacionAportacion.DEP,
                Aportacion.fecha <= datetime.utcnow() - timedelta(days=180),
            )
            .first()
        )
        if not deposito_antiguo:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pueden retirar aportaciones antes de 6 meses")
        if Decimal(socio.total_aportaciones) < datos.monto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aportaciones insuficientes")
        socio.total_aportaciones = Decimal(socio.total_aportaciones) - datos.monto
        aportacion = Aportacion(
            socio_id=datos.socio_id,
            tipo_aportacion_id=datos.tipo_aportacion_id,
            operacion=OperacionAportacion.RET,
            monto=datos.monto,
            descripcion=datos.descripcion or "Retiro de aportacion",
            usuario_cajero_id=datos.usuario_cajero_id,
        )
        db.add(aportacion)
        db.flush()
        asiento_contable_servicio.crear_automatico(
            db,
            descripcion="Retiro de aportacion",
            cuenta_debito="Aportaciones de socios",
            cuenta_credito="Caja/Bancos",
            monto=datos.monto,
            tipo_origen=TipoOrigenAsiento.APORTACION,
            aportacion_id=aportacion.id,
        )
        db.commit()
        db.refresh(aportacion)
        return aportacion

    def listar(self, db: Session, skip: int = 0, limit: int = 100):
        """Lista aportaciones."""

        return aportacion_repositorio.listar(db, skip, limit)

    def listar_por_socio(self, db: Session, socio_id: int):
        """Lista aportaciones de un socio."""

        if not socio_repositorio.obtener(db, socio_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
        return aportacion_repositorio.listar_por_socio(db, socio_id)


aportacion_servicio = AportacionServicio()

