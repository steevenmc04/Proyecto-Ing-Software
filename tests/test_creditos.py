"""Archivo: tests/test_creditos.py
Descripcion: Pruebas basicas del modulo de creditos.
Autor: Martinez Steeven
Version: 1.0
"""

from tests.conftest import crear_socio_prueba


def test_solicitar_credito(cliente):
    """Verifica que un credito inicie en estado pendiente."""

    socio = crear_socio_prueba(cliente)
    respuesta = cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "1000.00",
            "plazo_meses": 6,
            "tasa_interes": "12.00",
            "tipo_garantia": "Garante personal",
            "proposito": "Prueba academica",
        },
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "PENDIENTE"


def test_aprobar_credito_y_generar_cuotas(cliente):
    """Verifica que al aprobar se generen cuotas de amortizacion."""

    socio = crear_socio_prueba(cliente)
    solicitud = cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "1200.00",
            "plazo_meses": 12,
            "tasa_interes": "12.00",
            "tipo_garantia": "Garante personal",
            "proposito": "Capital de trabajo",
        },
    ).json()
    aprobacion = cliente.patch(f"/api/v1/creditos/{solicitud['id']}/aprobar", json={})
    assert aprobacion.status_code == 200
    assert aprobacion.json()["estado"] == "APROBADO"
    cuotas = cliente.get(f"/api/v1/creditos/{solicitud['id']}/cuotas")
    assert cuotas.status_code == 200
    assert len(cuotas.json()) == 12

