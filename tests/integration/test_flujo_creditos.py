"""Archivo: tests/integration/test_flujo_creditos.py
Descripcion: Prueba de integracion del flujo completo de creditos.
"""

def test_flujo_completo_creditos(cliente):
    """
    Simula el flujo:
    1. Crear socio
    2. Solicitar credito
    3. Aprobar credito
    4. Desembolsar
    5. Pagar primera cuota
    """
    # 1. Crear Socio
    respuesta_socio = cliente.post(
        "/api/v1/socios",
        json={
            "cedula": "1231231234",
            "nombres": "Socio",
            "apellidos": "Credito",
            "fecha_nacimiento": "1990-01-01",
            "direccion": "Calle Principal",
            "telefono": "0998887776",
            "correo": "credito1@caja.com"
        }
    )
    assert respuesta_socio.status_code == 200
    socio_id = respuesta_socio.json()["id"]

    # 2. Solicitar Credito
    respuesta_solicitud = cliente.post(
        "/api/v1/creditos/solicitar",
        json={
            "socio_id": socio_id,
            "monto_solicitado": "5000.00",
            "plazo_meses": 12,
            "tasa_interes": "12.00",
            "tipo_garantia": "Garante personal",
            "proposito": "Adquisicion de equipos"
        }
    )
    assert respuesta_solicitud.status_code == 200
    credito = respuesta_solicitud.json()
    credito_id = credito["id"]
    assert credito["estado"] == "PENDIENTE"

    # 3. Aprobar Credito
    respuesta_aprobacion = cliente.patch(f"/api/v1/creditos/{credito_id}/aprobar", json={})
    assert respuesta_aprobacion.status_code == 200
    assert respuesta_aprobacion.json()["estado"] == "APROBADO"

    # 4. Desembolsar Credito
    # Primero se requiere una cuenta para desembolsar? En este backend tal vez no es obligatorio,
    # enviaremos cuenta_id opcional o json vacio.
    respuesta_desembolso = cliente.patch(f"/api/v1/creditos/{credito_id}/desembolsar", json={})
    assert respuesta_desembolso.status_code == 200
    assert respuesta_desembolso.json()["estado"] == "DESEMBOLSADO"

    # 5. Pagar Primera Cuota
    cuotas = cliente.get(f"/api/v1/creditos/{credito_id}/cuotas").json()
    assert len(cuotas) == 12
    assert cuotas[0]["estado"] == "PENDIENTE"

    respuesta_pago = cliente.post(f"/api/v1/creditos/{credito_id}/pagar-cuota", json={})
    assert respuesta_pago.status_code == 200
    
    # Verificar que la cuota este pagada
    cuota_pagada = respuesta_pago.json()
    assert cuota_pagada["estado"] == "PAGADA"
