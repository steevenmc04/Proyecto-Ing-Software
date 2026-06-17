"""Archivo: app/utilidades/generadores.py
Descripcion: Generadores de codigos unicos para socios, cuentas y creditos.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime

from sqlalchemy.orm import Session


def generar_codigo_secuencial(db: Session, modelo, campo: str, prefijo: str, ancho: int = 6) -> str:
    """Genera codigos tipo SOC-000001 asegurando unicidad en la tabla."""

    ultimo = db.query(modelo).order_by(modelo.id.desc()).first()
    siguiente = (ultimo.id + 1) if ultimo else 1
    atributo = getattr(modelo, campo)
    codigo = f"{prefijo}-{siguiente:0{ancho}d}"
    while db.query(modelo).filter(atributo == codigo).first():
        siguiente += 1
        codigo = f"{prefijo}-{siguiente:0{ancho}d}"
    return codigo


def generar_numero_comprobante(db: Session, modelo, campo: str = "numero_comprobante") -> str:
    """Genera un comprobante con fecha y secuencia global."""

    fecha = datetime.utcnow().strftime("%Y%m%d")
    siguiente = db.query(modelo).count() + 1
    atributo = getattr(modelo, campo)
    codigo = f"COMP-{fecha}-{siguiente:06d}"
    while db.query(modelo).filter(atributo == codigo).first():
        siguiente += 1
        codigo = f"COMP-{fecha}-{siguiente:06d}"
    return codigo

