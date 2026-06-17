"""Archivo: app/servicios/cuenta_ahorro_servicio.py
Descripcion: Servicio de cuentas de ahorro y API externa.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import obtener_configuracion
from app.esquemas.cuenta_ahorro_esquema import CuentaMovimientosExternoRespuesta, MovimientoExternoRespuesta
from app.modelos.cuenta_ahorro_modelo import CuentaAhorro, EstadoCuenta
from app.repositorios.cuenta_ahorro_repositorio import cuenta_ahorro_repositorio
from app.repositorios.socio_repositorio import socio_repositorio
from app.repositorios.transaccion_repositorio import transaccion_repositorio
from app.utilidades.generadores import generar_codigo_secuencial


class CuentaAhorroServicio:
    """Gestiona apertura, estado y consulta de cuentas."""

    def crear(self, db: Session, socio_id: int):
        """Crea una cuenta con saldo inicial cero."""

        if not socio_repositorio.obtener(db, socio_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
        cuenta = CuentaAhorro(
            numero_cuenta=generar_codigo_secuencial(db, CuentaAhorro, "numero_cuenta", "CTA"),
            socio_id=socio_id,
            saldo=0,
            estado=EstadoCuenta.ACTIVA,
        )
        return cuenta_ahorro_repositorio.guardar(db, cuenta)

    def listar(self, db: Session, skip: int = 0, limit: int = 100):
        """Lista cuentas."""

        return cuenta_ahorro_repositorio.listar(db, skip, limit)

    def obtener(self, db: Session, cuenta_id: int):
        """Obtiene cuenta por ID."""

        cuenta = cuenta_ahorro_repositorio.obtener(db, cuenta_id)
        if not cuenta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
        return cuenta

    def obtener_por_numero(self, db: Session, numero_cuenta: str):
        """Obtiene cuenta por numero unico."""

        cuenta = cuenta_ahorro_repositorio.obtener_por_numero(db, numero_cuenta)
        if not cuenta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
        return cuenta

    def listar_por_socio(self, db: Session, socio_id: int):
        """Lista cuentas por socio."""

        if not socio_repositorio.obtener(db, socio_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
        return cuenta_ahorro_repositorio.listar_por_socio(db, socio_id)

    def cambiar_estado(self, db: Session, cuenta_id: int, estado: EstadoCuenta):
        """Cambia estado operativo de la cuenta."""

        cuenta = self.obtener(db, cuenta_id)
        cuenta.estado = estado
        db.commit()
        db.refresh(cuenta)
        return cuenta

    def validar_operable(self, cuenta: CuentaAhorro):
        """Impide movimientos en cuentas bloqueadas o cerradas."""

        if cuenta.estado in [EstadoCuenta.BLOQUEADA, EstadoCuenta.CERRADA]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se permiten operaciones en cuentas bloqueadas o cerradas")

    def consultar_api_externa(self, db: Session, cedula: str, numero_cuenta: str, api_key: str | None):
        """Valida API Key y devuelve saldo mas ultimos tres movimientos reales."""

        if api_key != obtener_configuracion().api_key_externa:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API Key invalida")
        cuenta = self.obtener_por_numero(db, numero_cuenta)
        if cuenta.socio.cedula != cedula:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La cuenta no pertenece a la cedula enviada")
        movimientos = transaccion_repositorio.listar_por_cuenta(db, cuenta.id, limit=3)
        return CuentaMovimientosExternoRespuesta(
            saldo=cuenta.saldo,
            movimientos=[
                MovimientoExternoRespuesta(tipo=mov.tipo_transaccion.value, fecha=mov.fecha.date().isoformat(), monto=mov.monto)
                for mov in movimientos
            ],
        )


cuenta_ahorro_servicio = CuentaAhorroServicio()

