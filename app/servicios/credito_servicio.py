"""Archivo: app/servicios/credito_servicio.py
Descripcion: Servicio de creditos, aprobacion, desembolso y pago de cuotas.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.esquemas.credito_esquema import CreditoAprobar, CreditoDesembolsar, CreditoRechazar, CreditoSolicitar, PagoCuotaSolicitud
from app.modelos.asiento_contable_modelo import TipoOrigenAsiento
from app.modelos.credito_modelo import Credito, EstadoCredito
from app.modelos.cuota_amortizacion_modelo import EstadoCuota
from app.repositorios.credito_repositorio import credito_repositorio
from app.repositorios.cuota_amortizacion_repositorio import cuota_amortizacion_repositorio
from app.repositorios.socio_repositorio import socio_repositorio
from app.repositorios.usuario_repositorio import usuario_repositorio
from app.servicios.amortizacion_servicio import amortizacion_servicio
from app.servicios.asiento_contable_servicio import asiento_contable_servicio
from app.utilidades.generadores import generar_codigo_secuencial


class CreditoServicio:
    """Gestiona el ciclo completo de creditos."""

    def solicitar(self, db: Session, datos: CreditoSolicitar):
        """Registra solicitud con estado inicial PENDIENTE."""

        if not socio_repositorio.obtener(db, datos.socio_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
        credito = Credito(
            numero_credito=generar_codigo_secuencial(db, Credito, "numero_credito", "CRE"),
            socio_id=datos.socio_id,
            monto_solicitado=datos.monto_solicitado,
            plazo_meses=datos.plazo_meses,
            tasa_interes=datos.tasa_interes,
            tipo_garantia=datos.tipo_garantia,
            proposito=datos.proposito,
            saldo_pendiente=0,
        )
        return credito_repositorio.guardar(db, credito)

    def listar(self, db: Session, skip: int = 0, limit: int = 100):
        """Lista creditos."""

        return credito_repositorio.listar(db, skip, limit)

    def obtener(self, db: Session, credito_id: int):
        """Obtiene credito por ID."""

        credito = credito_repositorio.obtener(db, credito_id)
        if not credito:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credito no encontrado")
        return credito

    def listar_por_socio(self, db: Session, socio_id: int):
        """Lista creditos de un socio."""

        if not socio_repositorio.obtener(db, socio_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
        return credito_repositorio.listar_por_socio(db, socio_id)

    def aprobar(self, db: Session, credito_id: int, datos: CreditoAprobar):
        """Aprueba credito pendiente y genera tabla de amortizacion."""

        credito = self.obtener(db, credito_id)
        if credito.estado != EstadoCredito.PENDIENTE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo se puede aprobar un credito pendiente")
        if datos.gerente_aprobador_id and not usuario_repositorio.obtener(db, datos.gerente_aprobador_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gerente aprobador no encontrado")
        monto_aprobado = datos.monto_aprobado or credito.monto_solicitado
        credito.monto_aprobado = monto_aprobado
        credito.saldo_pendiente = monto_aprobado
        credito.gerente_aprobador_id = datos.gerente_aprobador_id
        credito.fecha_aprobacion = datetime.utcnow()
        credito.estado = EstadoCredito.APROBADO
        amortizacion_servicio.generar_tabla(db, credito)
        db.commit()
        db.refresh(credito)
        return credito

    def rechazar(self, db: Session, credito_id: int, datos: CreditoRechazar):
        """Rechaza credito pendiente guardando motivo."""

        credito = self.obtener(db, credito_id)
        if credito.estado != EstadoCredito.PENDIENTE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo se puede rechazar un credito pendiente")
        credito.estado = EstadoCredito.RECHAZADO
        credito.motivo_rechazo = datos.motivo_rechazo
        db.commit()
        db.refresh(credito)
        return credito

    def desembolsar(self, db: Session, credito_id: int, datos: CreditoDesembolsar):
        """Desembolsa credito aprobado y genera asiento contable."""

        credito = self.obtener(db, credito_id)
        if credito.estado != EstadoCredito.APROBADO:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El credito debe estar aprobado")
        if datos.cajero_desembolso_id and not usuario_repositorio.obtener(db, datos.cajero_desembolso_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cajero de desembolso no encontrado")
        credito.estado = EstadoCredito.DESEMBOLSADO
        credito.cajero_desembolso_id = datos.cajero_desembolso_id
        asiento_contable_servicio.crear_automatico(
            db,
            descripcion=f"Desembolso de credito {credito.numero_credito}",
            cuenta_debito="Cartera de creditos",
            cuenta_credito="Caja/Bancos",
            monto=Decimal(credito.monto_aprobado),
            tipo_origen=TipoOrigenAsiento.CREDITO,
            credito_id=credito.id,
        )
        db.commit()
        db.refresh(credito)
        return credito

    def pagar_siguiente_cuota(self, db: Session, credito_id: int, datos: PagoCuotaSolicitud):
        """Paga la primera cuota pendiente, reduce saldo y genera asiento."""

        credito = self.obtener(db, credito_id)
        if credito.estado not in [EstadoCredito.APROBADO, EstadoCredito.DESEMBOLSADO, EstadoCredito.EN_PAGO]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El credito no admite pagos de cuotas")
        if datos.usuario_cajero_id and not usuario_repositorio.obtener(db, datos.usuario_cajero_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario cajero no encontrado")
        cuota = cuota_amortizacion_repositorio.obtener_siguiente_pendiente(db, credito_id)
        if not cuota:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No existen cuotas pendientes")
        cuota.estado = EstadoCuota.PAGADA
        credito.saldo_pendiente = max(Decimal("0.00"), Decimal(credito.saldo_pendiente) - Decimal(cuota.capital))
        asiento_contable_servicio.crear_automatico(
            db,
            descripcion=f"Pago cuota {cuota.numero_cuota} del credito {credito.numero_credito}",
            cuenta_debito="Caja/Bancos",
            cuenta_credito="Cartera de creditos",
            monto=Decimal(cuota.cuota_total),
            tipo_origen=TipoOrigenAsiento.PAGO_CUOTA,
            credito_id=credito.id,
        )
        pendientes = [c for c in credito.cuotas if c.id != cuota.id and c.estado == EstadoCuota.PENDIENTE]
        credito.estado = EstadoCredito.CANCELADO if not pendientes else EstadoCredito.EN_PAGO
        if credito.estado == EstadoCredito.CANCELADO:
            credito.saldo_pendiente = Decimal("0.00")
        db.commit()
        db.refresh(cuota)
        return cuota

    def listar_cuotas(self, db: Session, credito_id: int):
        """Lista cuotas de un credito."""

        self.obtener(db, credito_id)
        return cuota_amortizacion_repositorio.listar_por_credito(db, credito_id)

    def obtener_cuota(self, db: Session, cuota_id: int):
        """Obtiene una cuota por ID."""

        cuota = cuota_amortizacion_repositorio.obtener(db, cuota_id)
        if not cuota:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuota no encontrada")
        return cuota


credito_servicio = CreditoServicio()

