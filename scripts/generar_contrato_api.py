"""Genera la matriz Markdown de endpoints desde las rutas reales de FastAPI."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastapi.routing import APIRoute


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from app.main import app  # noqa: E402


PANTALLAS = {
    "Autenticacion": "Inicio de sesion",
    "Usuarios": "Usuarios",
    "Socios": "Socios",
    "Cuentas de ahorro": "Cuentas",
    "Transacciones": "Transacciones / Dashboard",
    "Aportaciones": "Aportaciones",
    "Creditos": "Creditos",
    "Cuotas de amortizacion": "Creditos",
    "Libro diario": "Libro Diario",
    "Reportes": "Reportes",
    "API externa": "Integracion externa; no se consume desde el navegador",
    "Salud": "Monitoreo / Swagger",
}

PRUEBAS = {
    "Autenticacion": "tests/unit/test_auth.py",
    "Usuarios": "tests/unit/test_usuarios.py",
    "Socios": "tests/unit/test_socios.py",
    "Cuentas de ahorro": "tests/unit/test_cuentas.py",
    "Transacciones": "tests/unit/test_transacciones.py",
    "Aportaciones": "tests/unit/test_aportaciones.py",
    "Creditos": "tests/unit/test_creditos.py; tests/integration/test_flujo_creditos.py",
    "Cuotas de amortizacion": "tests/unit/test_cuotas.py",
    "Libro diario": "tests/unit/test_reportes.py",
    "Reportes": "tests/unit/test_reportes.py",
    "API externa": "tests/unit/test_api_externa.py; tests/integration/test_flujo_api_externa.py",
    "Salud": "tests/unit/test_autorizacion_roles.py",
}


def dependencias_ruta(ruta: APIRoute) -> list[Any]:
    pendientes = list(ruta.dependant.dependencies)
    resultado = []
    while pendientes:
        dependencia = pendientes.pop()
        resultado.append(dependencia)
        pendientes.extend(dependencia.dependencies)
    return resultado


def seguridad(ruta: APIRoute) -> tuple[str, str]:
    if ruta.path == "/api/v1/cuenta/movimientos":
        return "X-API-KEY", "Consumidor externo con clave valida"

    dependencias = dependencias_ruta(ruta)
    roles = sorted(
        {
            rol
            for dependencia in dependencias
            for rol in getattr(dependencia.call, "roles_permitidos", ())
        }
    )
    usa_jwt = roles or any(
        getattr(dependencia.call, "__name__", "") == "obtener_usuario_actual"
        for dependencia in dependencias
    )
    if roles:
        return "JWT Bearer", ", ".join(roles)
    if usa_jwt:
        return "JWT Bearer", "Cualquier usuario activo; el servicio filtra los datos propios"
    return "No", "Publico"


def resumir_esquema(valor: Any) -> str:
    if not valor:
        return "-"
    texto = json.dumps(valor, ensure_ascii=False, separators=(",", ":"))
    return texto.replace("|", "\\|")


def generar() -> str:
    openapi = app.openapi()
    rutas_fastapi = {
        (ruta.path, metodo.upper()): ruta
        for ruta in app.routes
        if isinstance(ruta, APIRoute)
        for metodo in ruta.methods
    }
    filas = []
    for ruta, operaciones in sorted(openapi["paths"].items()):
        for metodo, operacion in sorted(operaciones.items()):
            clave = (ruta, metodo.upper())
            ruta_fastapi = rutas_fastapi.get(clave)
            if not ruta_fastapi:
                continue
            modulo = (operacion.get("tags") or ["Sin modulo"])[0]
            autenticacion, roles = seguridad(ruta_fastapi)
            parametros = [
                f"{parametro['name']} ({parametro['in']})"
                for parametro in operacion.get("parameters", [])
            ]
            cuerpo = (
                operacion.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            respuestas = operacion.get("responses", {})
            exito = next(
                (
                    f"{codigo}: {datos.get('description', '')}"
                    for codigo, datos in respuestas.items()
                    if codigo.startswith("2")
                ),
                "-",
            )
            errores = ["422 validacion"]
            if autenticacion == "JWT Bearer":
                errores.extend(["401 sin sesion", "403 rol no autorizado"])
            if autenticacion == "X-API-KEY":
                errores.extend(["401 clave invalida", "404 cuenta no encontrada o no asociada"])
            if modulo not in {"Autenticacion", "Salud", "API externa"}:
                errores.append("400/404 segun regla de negocio")
            filas.append(
                [
                    metodo.upper(),
                    ruta,
                    modulo,
                    operacion.get("summary", "-"),
                    autenticacion,
                    roles,
                    ", ".join(parametros) or "-",
                    resumir_esquema(cuerpo),
                    exito,
                    "; ".join(errores),
                    PANTALLAS.get(modulo, "No aplica"),
                    PRUEBAS.get(modulo, "No identificada"),
                ]
            )

    encabezados = [
        "Metodo",
        "Ruta",
        "Modulo",
        "Descripcion",
        "Autenticacion",
        "Roles",
        "Parametros",
        "Cuerpo",
        "Respuesta exitosa",
        "Errores",
        "Pantalla",
        "Prueba",
    ]
    lineas = [
        "# Contrato real de la API",
        "",
        "Documento generado desde `app.openapi()` y las dependencias reales de FastAPI.",
        "No debe editarse manualmente; se actualiza con `python scripts/generar_contrato_api.py`.",
        "",
        f"Total de operaciones documentadas: **{len(filas)}**.",
        "",
        "| " + " | ".join(encabezados) + " |",
        "|" + "|".join(["---"] * len(encabezados)) + "|",
    ]
    lineas.extend(
        "| " + " | ".join(str(celda).replace("\n", " ").replace("|", "\\|") for celda in fila) + " |"
        for fila in filas
    )
    lineas.extend(
        [
            "",
            "## Convenciones",
            "",
            "- Los errores `400/404` dependen de las reglas de negocio de cada servicio.",
            "- FastAPI documenta automaticamente los errores de validacion `422`.",
            "- La API externa usa exclusivamente `X-API-KEY`; la clave no se incluye en el frontend.",
            "- Las rutas de SOCIO filtran cuentas, movimientos y creditos por el usuario del JWT.",
        ]
    )
    return "\n".join(lineas) + "\n"


if __name__ == "__main__":
    destino = RAIZ / "docs" / "CONTRATO_API.md"
    destino.write_text(generar(), encoding="utf-8")
    print(f"Contrato generado: {destino}")
