"""Archivo: app/servicios/transaccion_servicio.py
Descripcion: Servicio de depositos y retiros con asientos contables.
Autor: Martinez Steeven
Version: 1.0
"""

from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.esquemas.transaccion_esquema import TransaccionCrear
from app.modelos.asiento_contable_modelo import TipoOrigenAsiento
from app.modelos.cuenta_ahorro_modelo import EstadoCuenta
from app.modelos.transaccion_modelo import TipoTransaccion, Transaccion
from app.modelos.usuario_modelo import RolUsuario
from app.repositorios.cuenta_ahorro_repositorio import cuenta_ahorro_repositorio
from app.repositorios.socio_repositorio import socio_repositorio
from app.repositorios.transaccion_repositorio import transaccion_repositorio
from app.repositorios.usuario_repositorio import usuario_repositorio
from app.servicios.asiento_contable_servicio import asiento_contable_servicio
from app.servicios.cuenta_ahorro_servicio import cuenta_ahorro_servicio
from app.utilidades.generadores import generar_numero_comprobante


class TransaccionServicio:
    """Aplica reglas de depositos, retiros y saldos."""

    def _validar_cajero(self, db: Session, usuario_cajero_id: int | None):
        """Verifica que el cajero exista cuando se envia su ID."""

        if usuario_cajero_id and not usuario_repositorio.obtener(db, usuario_cajero_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario cajero no encontrado")

    def registrar_deposito(self, db: Session, datos: TransaccionCrear):
        """Aumenta saldo y genera asiento debitando caja contra obligaciones."""

        cuenta = cuenta_ahorro_servicio.obtener(db, datos.cuenta_id)
        cuenta_ahorro_servicio.validar_operable(cuenta)
        self._validar_cajero(db, datos.usuario_cajero_id)
        cuenta.saldo = Decimal(cuenta.saldo) + datos.monto
        cuenta.estado = EstadoCuenta.ACTIVA
        transaccion = Transaccion(
            numero_comprobante=generar_numero_comprobante(db, Transaccion),
            tipo_transaccion=TipoTransaccion.DEPOSITO,
            monto=datos.monto,
            descripcion=datos.descripcion or "Deposito en cuenta de ahorro",
            saldo_resultante=cuenta.saldo,
            cuenta_id=cuenta.id,
            usuario_cajero_id=datos.usuario_cajero_id,
        )
        db.add(transaccion)
        db.flush()
        asiento_contable_servicio.crear_automatico(
            db,
            descripcion=f"Deposito {transaccion.numero_comprobante}",
            cuenta_debito="Caja/Bancos",
            cuenta_credito="Obligaciones con socios",
            monto=datos.monto,
            tipo_origen=TipoOrigenAsiento.TRANSACCION,
            transaccion_id=transaccion.id,
        )
        db.commit()
        db.refresh(transaccion)
        return transaccion

    def registrar_retiro(self, db: Session, datos: TransaccionCrear):
        """Disminuye saldo validando suficiencia y genera asiento inverso."""

        cuenta = cuenta_ahorro_servicio.obtener(db, datos.cuenta_id)
        cuenta_ahorro_servicio.validar_operable(cuenta)
        self._validar_cajero(db, datos.usuario_cajero_id)
        if Decimal(cuenta.saldo) < datos.monto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente para realizar el retiro")
        cuenta.saldo = Decimal(cuenta.saldo) - datos.monto
        cuenta.estado = EstadoCuenta.SALDO_CERO if cuenta.saldo == 0 else EstadoCuenta.ACTIVA
        transaccion = Transaccion(
            numero_comprobante=generar_numero_comprobante(db, Transaccion),
            tipo_transaccion=TipoTransaccion.RETIRO,
            monto=datos.monto,
            descripcion=datos.descripcion or "Retiro de cuenta de ahorro",
            saldo_resultante=cuenta.saldo,
            cuenta_id=cuenta.id,
            usuario_cajero_id=datos.usuario_cajero_id,
        )
        db.add(transaccion)
        db.flush()
        asiento_contable_servicio.crear_automatico(
            db,
            descripcion=f"Retiro {transaccion.numero_comprobante}",
            cuenta_debito="Obligaciones con socios",
            cuenta_credito="Caja/Bancos",
            monto=datos.monto,
            tipo_origen=TipoOrigenAsiento.TRANSACCION,
            transaccion_id=transaccion.id,
        )
        db.commit()
        db.refresh(transaccion)
        return transaccion

    def listar(self, db: Session, skip: int = 0, limit: int = 100):
        """Lista transacciones."""

        return transaccion_repositorio.listar(db, skip, limit)

    def listar_para_usuario(self, db: Session, usuario):
        """Lista transacciones segun rol; un socio solo ve movimientos de sus cuentas."""

        if usuario.rol == RolUsuario.SOCIO:
            socio = socio_repositorio.obtener_por_usuario(db, usuario.id)
            if not socio:
                return []
            movimientos = []
            for cuenta in cuenta_ahorro_repositorio.listar_por_socio(db, socio.id):
                movimientos.extend(transaccion_repositorio.listar_por_cuenta(db, cuenta.id))
            movimientos.sort(key=lambda movimiento: movimiento.fecha, reverse=True)
            return movimientos
        return transaccion_repositorio.listar(db, 0, 1000)

    def obtener(self, db: Session, transaccion_id: int):
        """Obtiene una transaccion por ID."""

        transaccion = transaccion_repositorio.obtener(db, transaccion_id)
        if not transaccion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaccion no encontrada")
        return transaccion

    def listar_por_cuenta(self, db: Session, cuenta_id: int):
        """Lista movimientos de una cuenta por ID."""

        if not cuenta_ahorro_repositorio.obtener(db, cuenta_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
        return transaccion_repositorio.listar_por_cuenta(db, cuenta_id)


transaccion_servicio = TransaccionServicio()
