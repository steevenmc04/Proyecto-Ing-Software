"""Archivo: tests/unit/test_reportes.py
Descripcion: Pruebas unitarias para el modulo de reportes.
"""

from tests.conftest import crear_socio_prueba, crear_cuenta_prueba

def test_reporte_libro_diario(cliente):
    """Verifica que se pueda obtener el reporte de libro diario."""
    socio = crear_socio_prueba(cliente, cedula="7776665551")
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    cliente.post(
        "/api/v1/transacciones/deposito",
        json={"cuenta_id": cuenta["id"], "monto": "100.00", "descripcion": "Dep Inicial"}
    )
    
    respuesta = cliente.get("/api/v1/reportes/libro-diario")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "asientos" in datos
    assert len(datos["asientos"]) > 0

def test_reporte_historial_ahorros(cliente):
    """Verifica que se pueda obtener el reporte de historial de ahorros de un socio."""
    socio = crear_socio_prueba(cliente, cedula="7776665552")
    cuenta = crear_cuenta_prueba(cliente, socio["id"])
    cliente.post(
        "/api/v1/transacciones/deposito",
        json={"cuenta_id": cuenta["id"], "monto": "200.00", "descripcion": "Ahorro"}
    )
    
    respuesta = cliente.get(f"/api/v1/reportes/historial-ahorros/{socio['id']}")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "movimientos" in datos
    assert len(datos["movimientos"]) > 0

def test_reporte_cartera_creditos(cliente):
    """Verifica que se pueda obtener el reporte de la cartera de creditos."""
    socio = crear_socio_prueba(cliente, cedula="7776665553")
    cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio["id"],
            "monto_solicitado": "1000.00",
            "plazo_meses": 12,
            "tasa_interes": "10.00",
            "tipo_garantia": "Ninguna",
            "proposito": "Prueba"
        }
    )
    
    respuesta = cliente.get("/api/v1/reportes/cartera-creditos")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "creditos" in datos
    assert len(datos["creditos"]) > 0

def test_reporte_resumen_aportaciones(cliente):
    """Verifica el resumen de aportaciones de un socio."""
    socio = crear_socio_prueba(cliente, cedula="7776665554")
    tipo = cliente.post("/api/v1/aportaciones/tipos", json={"nombre": "ORDINARIA"}).json()
    if "id" not in tipo:
        tipo = cliente.get("/api/v1/aportaciones/tipos").json()[0]
    tipo_id = tipo["id"]
    
    cliente.post("/api/v1/aportaciones/deposito", json={"socio_id": socio["id"], "tipo_aportacion_id": tipo_id, "monto": "15.00"})
    cliente.post("/api/v1/aportaciones/deposito", json={"socio_id": socio["id"], "tipo_aportacion_id": tipo_id, "monto": "15.00"})
    
    respuesta = cliente.get(f"/api/v1/reportes/resumen-aportaciones/{socio['id']}")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["total"] == "30.00"
    assert len(datos["aportaciones"]) == 2
