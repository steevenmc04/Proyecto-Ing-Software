"""Archivo: app/servicios/amortizacion_servicio.py
Descripcion: Servicio para calcular cuotas con metodo frances.
Autor: Martinez Steeven
Version: 1.0
"""

from calendar import monthrange
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.modelos.credito_modelo import Credito
from app.modelos.cuota_amortizacion_modelo import CuotaAmortizacion, EstadoCuota


CENTAVO = Decimal("0.01")


class AmortizacionServicio:
    """Calcula y persiste la tabla de amortizacion francesa."""

    def _redondear(self, valor: Decimal) -> Decimal:
        """Redondea valores monetarios a dos decimales."""

        return Decimal(valor).quantize(CENTAVO, rounding=ROUND_HALF_UP)

    def _sumar_meses(self, fecha: date, meses: int) -> date:
        """Suma meses conservando un dia valido dentro del mes destino."""

        mes_base = fecha.month - 1 + meses
        anio = fecha.year + mes_base // 12
        mes = mes_base % 12 + 1
        dia = min(fecha.day, monthrange(anio, mes)[1])
        return date(anio, mes, dia)

    def generar_tabla(self, db: Session, credito: Credito):
        """Genera cuotas usando C = P * [i(1+i)^n] / [(1+i)^n - 1]."""

        for cuota in list(credito.cuotas):
            db.delete(cuota)

        principal = Decimal(credito.monto_aprobado or credito.monto_solicitado)
        tasa_mensual = (Decimal(credito.tasa_interes) / Decimal("100")) / Decimal("12")
        plazo = int(credito.plazo_meses)

        # Si la tasa es cero, la cuota fija es solo capital dividido para el plazo.
        if tasa_mensual == 0:
            cuota_fija = principal / plazo
        else:
            factor = (Decimal("1") + tasa_mensual) ** plazo
            cuota_fija = principal * ((tasa_mensual * factor) / (factor - Decimal("1")))

        saldo = principal
        hoy = date.today()
        cuotas = []
        for numero in range(1, plazo + 1):
            interes = self._redondear(saldo * tasa_mensual)
            capital = self._redondear(cuota_fija - interes)
            # Ajuste final: evita que redondeos acumulados dejen centavos pendientes.
            if numero == plazo:
                capital = self._redondear(saldo)
            saldo = self._redondear(saldo - capital)
            cuota = CuotaAmortizacion(
                credito_id=credito.id,
                numero_cuota=numero,
                fecha_vencimiento=self._sumar_meses(hoy, numero),
                capital=capital,
                interes=interes,
                cuota_total=self._redondear(capital + interes),
                saldo_pendiente=max(Decimal("0.00"), saldo),
                estado=EstadoCuota.PENDIENTE,
            )
            db.add(cuota)
            cuotas.append(cuota)
        db.flush()
        return cuotas


amortizacion_servicio = AmortizacionServicio()

