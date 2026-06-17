"""Archivo: seed.py
Descripcion: Carga datos iniciales de prueba para la aplicacion.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import date, datetime, timedelta
from decimal import Decimal

from app.database import Base, SesionLocal, engine
from app.esquemas.aportacion_esquema import AportacionCrear, TipoAportacionCrear
from app.esquemas.credito_esquema import CreditoAprobar, CreditoSolicitar
from app.esquemas.socio_esquema import SocioCrear
from app.esquemas.transaccion_esquema import TransaccionCrear
from app.esquemas.usuario_esquema import UsuarioCrear
from app.modelos import *  # noqa: F401,F403 - registra todos los modelos
from app.modelos.aportacion_modelo import Aportacion, OperacionAportacion
from app.modelos.tipo_aportacion_modelo import NombreTipoAportacion
from app.modelos.usuario_modelo import RolUsuario
from app.repositorios.cuenta_ahorro_repositorio import cuenta_ahorro_repositorio
from app.repositorios.socio_repositorio import socio_repositorio
from app.repositorios.usuario_repositorio import usuario_repositorio
from app.servicios.aportacion_servicio import aportacion_servicio
from app.servicios.credito_servicio import credito_servicio
from app.servicios.cuenta_ahorro_servicio import cuenta_ahorro_servicio
from app.servicios.socio_servicio import socio_servicio
from app.servicios.transaccion_servicio import transaccion_servicio
from app.servicios.usuario_servicio import usuario_servicio


def crear_usuario_si_no_existe(db, datos: UsuarioCrear):
    """Crea un usuario solo si no existe por nombre de usuario."""

    usuario = usuario_repositorio.obtener_por_nombre_usuario(db, datos.nombre_usuario)
    if usuario:
        return usuario
    return usuario_servicio.crear(db, datos)


def crear_tipo_si_no_existe(db, nombre: NombreTipoAportacion):
    """Crea un tipo de aportacion si aun no existe."""

    existente = next((tipo for tipo in aportacion_servicio.listar_tipos(db) if tipo.nombre == nombre), None)
    if existente:
        return existente
    return aportacion_servicio.crear_tipo(db, TipoAportacionCrear(nombre=nombre, descripcion=f"Aportacion {nombre.value.lower()}"))


def main():
    """Carga usuarios, socio, cuenta, movimientos, aportacion, creditos y asientos."""

    Base.metadata.create_all(bind=engine)
    db = SesionLocal()
    try:
        admin = crear_usuario_si_no_existe(
            db,
            UsuarioCrear(
                nombre_usuario="admin",
                nombre_completo="Administrador General",
                correo="admin@caja.com",
                rol=RolUsuario.ADMINISTRADOR,
                contrasena="Admin123",
            ),
        )
        gerente = crear_usuario_si_no_existe(
            db,
            UsuarioCrear(
                nombre_usuario="gerente",
                nombre_completo="Gerente General",
                correo="gerente@caja.com",
                rol=RolUsuario.GERENTE,
                contrasena="Gerente123",
            ),
        )
        cajero = crear_usuario_si_no_existe(
            db,
            UsuarioCrear(
                nombre_usuario="cajero",
                nombre_completo="Cajero Principal",
                correo="cajero@caja.com",
                rol=RolUsuario.CAJERO,
                contrasena="Cajero123",
            ),
        )
        crear_usuario_si_no_existe(
            db,
            UsuarioCrear(
                nombre_usuario="contador",
                nombre_completo="Contador General",
                correo="contador@caja.com",
                rol=RolUsuario.CONTADOR,
                contrasena="Contador123",
            ),
        )

        socio = socio_repositorio.obtener_por_cedula(db, "0102030405")
        if not socio:
            socio = socio_servicio.crear(
                db,
                SocioCrear(
                    cedula="0102030405",
                    nombres="Juan Carlos",
                    apellidos="Perez Mora",
                    fecha_nacimiento=date(1995, 5, 12),
                    direccion="Av. Principal y Calle 10",
                    telefono="0999999999",
                    correo="juan.perez@caja.com",
                    usuario_registro_id=admin.id,
                ),
            )

        cuentas = cuenta_ahorro_repositorio.listar_por_socio(db, socio.id)
        cuenta = cuentas[0] if cuentas else cuenta_ahorro_servicio.crear(db, socio.id)

        if not cuenta.transacciones:
            transaccion_servicio.registrar_deposito(db, TransaccionCrear(cuenta_id=cuenta.id, monto=Decimal("500.00"), descripcion="Deposito inicial", usuario_cajero_id=cajero.id))
            transaccion_servicio.registrar_deposito(db, TransaccionCrear(cuenta_id=cuenta.id, monto=Decimal("700.00"), descripcion="Deposito de ahorro", usuario_cajero_id=cajero.id))
            transaccion_servicio.registrar_deposito(db, TransaccionCrear(cuenta_id=cuenta.id, monto=Decimal("400.00"), descripcion="Deposito adicional", usuario_cajero_id=cajero.id))
            transaccion_servicio.registrar_retiro(db, TransaccionCrear(cuenta_id=cuenta.id, monto=Decimal("100.00"), descripcion="Retiro de prueba", usuario_cajero_id=cajero.id))

        tipo_ordinaria = crear_tipo_si_no_existe(db, NombreTipoAportacion.ORDINARIA)
        crear_tipo_si_no_existe(db, NombreTipoAportacion.EXTRAORDINARIA)

        if not socio.aportaciones:
            aportacion = aportacion_servicio.registrar_deposito(
                db,
                AportacionCrear(socio_id=socio.id, tipo_aportacion_id=tipo_ordinaria.id, monto=Decimal("120.00"), descripcion="Aportacion ordinaria inicial", usuario_cajero_id=cajero.id),
            )
            # Se ajusta la fecha para que las pruebas manuales de retiro puedan validar la regla de seis meses.
            aportacion.fecha = datetime.utcnow() - timedelta(days=190)
            db.commit()

        if len(credito_servicio.listar(db)) < 1:
            credito_servicio.solicitar(
                db,
                CreditoSolicitar(
                    socio_id=socio.id,
                    monto_solicitado=Decimal("1500.00"),
                    plazo_meses=6,
                    tasa_interes=Decimal("12.00"),
                    tipo_garantia="Garante personal",
                    proposito="Credito pendiente de prueba",
                ),
            )

        if len(credito_servicio.listar(db)) < 2:
            credito_aprobado = credito_servicio.solicitar(
                db,
                CreditoSolicitar(
                    socio_id=socio.id,
                    monto_solicitado=Decimal("3000.00"),
                    plazo_meses=12,
                    tasa_interes=Decimal("12.00"),
                    tipo_garantia="Garante personal",
                    proposito="Capital de trabajo",
                ),
            )
            credito_servicio.aprobar(db, credito_aprobado.id, CreditoAprobar(gerente_aprobador_id=gerente.id))

        print("Datos de prueba cargados correctamente.")
        print("Usuarios: admin/Admin123, gerente/Gerente123, cajero/Cajero123, contador/Contador123")
        print(f"Socio de prueba: {socio.cedula}")
        print(f"Cuenta activa: {cuenta.numero_cuenta}")
        print("API Key externa: API-KEY-DEMO-123")
    finally:
        db.close()


if __name__ == "__main__":
    main()

