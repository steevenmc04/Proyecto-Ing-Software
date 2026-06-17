"""Archivo: app/servicios/reporte_servicio.py
Descripcion: Servicio de reportes JSON basados en datos reales.
Autor: Martinez Steeven
Version: 1.0
"""

from decimal import Decimal

from sqlalchemy.orm import Session

from app.modelos.aportacion_modelo import OperacionAportacion
from app.modelos.credito_modelo import Credito
from app.repositorios.aportacion_repositorio import aportacion_repositorio
from app.repositorios.cuenta_ahorro_repositorio import cuenta_ahorro_repositorio
from app.repositorios.transaccion_repositorio import transaccion_repositorio
from app.servicios.asiento_contable_servicio import asiento_contable_servicio
from app.servicios.socio_servicio import socio_servicio


class ReporteServicio:
    """Construye reportes consultando tablas reales."""

    def libro_diario(self, db: Session):
        """Reporte del libro diario. Aqui se podria integrar exportacion PDF/Excel."""

        asientos = asiento_contable_servicio.listar(db, 0, 1000)
        total = sum((Decimal(a.monto) for a in asientos), Decimal("0.00"))
        return {"total": total, "asientos": asientos}

    def historial_ahorros(self, db: Session, socio_id: int):
        """Reporte de ahorros por socio. Aqui se podria integrar exportacion PDF/Excel."""

        socio_servicio.obtener(db, socio_id)
        movimientos = []
        for cuenta in cuenta_ahorro_repositorio.listar_por_socio(db, socio_id):
            movimientos.extend(transaccion_repositorio.listar_por_cuenta(db, cuenta.id))
        movimientos.sort(key=lambda mov: mov.fecha, reverse=True)
        return {"socio_id": socio_id, "movimientos": movimientos}

    def cartera_creditos(self, db: Session):
        """Reporte de cartera de creditos. Aqui se podria integrar exportacion PDF/Excel."""

        creditos = db.query(Credito).all()
        total = sum((Decimal(c.saldo_pendiente) for c in creditos), Decimal("0.00"))
        return {"total_creditos": len(creditos), "saldo_total_pendiente": total, "creditos": creditos}

    def resumen_aportaciones(self, db: Session, socio_id: int):
        """Reporte de aportaciones por tipo. Aqui se podria integrar exportacion PDF/Excel."""

        socio_servicio.obtener(db, socio_id)
        aportaciones = aportacion_repositorio.listar_por_socio(db, socio_id)
        totales: dict[str, Decimal] = {}
        total = Decimal("0.00")
        for aportacion in aportaciones:
            signo = Decimal("1") if aportacion.operacion == OperacionAportacion.DEP else Decimal("-1")
            monto = Decimal(aportacion.monto) * signo
            nombre = aportacion.tipo_aportacion.nombre.value
            totales[nombre] = totales.get(nombre, Decimal("0.00")) + monto
            total += monto
        return {"socio_id": socio_id, "total": total, "totales_por_tipo": totales, "aportaciones": aportaciones}


reporte_servicio = ReporteServicio()

