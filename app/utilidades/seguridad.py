"""Archivo: app/utilidades/seguridad.py
Descripcion: Hash BCrypt de contrasenas y generacion de JWT.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.config import obtener_configuracion


contexto_bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashear_contrasena(contrasena: str) -> str:
    """Hashea una contrasena usando BCrypt antes de guardarla."""

    return contexto_bcrypt.hash(contrasena)


def verificar_contrasena(contrasena: str, hash_contrasena: str) -> bool:
    """Compara una contrasena plana contra su hash BCrypt."""

    return contexto_bcrypt.verify(contrasena, hash_contrasena)


def crear_token_jwt(nombre_usuario: str, rol: str) -> str:
    """Genera un JWT basico con usuario, rol y fecha de expiracion."""

    configuracion = obtener_configuracion()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=configuracion.minutos_expiracion_jwt)
    payload = {"sub": nombre_usuario, "rol": rol, "exp": expiracion}
    return jwt.encode(payload, configuracion.clave_jwt, algorithm=configuracion.algoritmo_jwt)


def decodificar_token(token: str) -> dict:
    """Decodifica un JWT y convierte errores de seguridad en HTTP 401."""

    configuracion = obtener_configuracion()
    try:
        return jwt.decode(token, configuracion.clave_jwt, algorithms=[configuracion.algoritmo_jwt])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido o expirado") from exc

