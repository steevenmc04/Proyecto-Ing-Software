"""Archivo: tests/test_autorizacion.py
Descripcion: Pruebas de autorizacion por usuario socio.
Autor: Martinez Steeven
Version: 1.0
"""

from app.esquemas.socio_esquema import SocioCrear
from app.esquemas.usuario_esquema import UsuarioCrear
from app.modelos.usuario_modelo import RolUsuario
from app.servicios.cuenta_ahorro_servicio import cuenta_ahorro_servicio
from app.servicios.socio_servicio import socio_servicio
from app.servicios.usuario_servicio import usuario_servicio


def test_socio_solo_ve_sus_cuentas(cliente):
    """Verifica que un usuario SOCIO no reciba cuentas de otros socios."""

    from app.database import SesionLocal

    db = SesionLocal()
    try:
        usuario_socio = usuario_servicio.crear(
            db,
            UsuarioCrear(
                nombre_usuario="cliente1",
                nombre_completo="Cliente Uno",
                correo="cliente1@caja.com",
                rol=RolUsuario.SOCIO,
                contrasena="Cliente123",
            ),
        )
        socio_uno = socio_servicio.crear(
            db,
            SocioCrear(
                cedula="1111111111",
                nombres="Cliente",
                apellidos="Uno",
                fecha_nacimiento="1998-01-01",
                direccion="Direccion uno",
                telefono="0991111111",
                correo="cliente1.socio@caja.com",
                usuario_id=usuario_socio.id,
            ),
        )
        socio_dos = socio_servicio.crear(
            db,
            SocioCrear(
                cedula="2222222222",
                nombres="Cliente",
                apellidos="Dos",
                fecha_nacimiento="1998-01-01",
                direccion="Direccion dos",
                telefono="0992222222",
                correo="cliente2.socio@caja.com",
            ),
        )
        cuenta_uno = cuenta_ahorro_servicio.crear(db, socio_uno.id)
        cuenta_uno_id = cuenta_uno.id
        cuenta_ahorro_servicio.crear(db, socio_dos.id)
    finally:
        db.close()

    login = cliente.post("/api/v1/auth/login", json={"nombre_usuario": "cliente1", "contrasena": "Cliente123"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    respuesta = cliente.get("/api/v1/cuentas/mis-cuentas", headers={"Authorization": f"Bearer {token}"})
    assert respuesta.status_code == 200
    cuentas = respuesta.json()
    assert len(cuentas) == 1
    assert cuentas[0]["id"] == cuenta_uno_id
