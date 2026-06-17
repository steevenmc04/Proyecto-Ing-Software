"""Archivo: app/esquemas/usuario_esquema.py
Descripcion: Esquemas para crear, actualizar y mostrar usuarios.
Autor: Martinez Steeven
Version: 1.0
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.modelos.usuario_modelo import RolUsuario


class UsuarioBase(BaseModel):
    """Datos comunes de usuario."""

    nombre_usuario: str = Field(..., min_length=3, max_length=50)
    nombre_completo: str = Field(..., min_length=3, max_length=150)
    correo: EmailStr
    rol: RolUsuario


class UsuarioCrear(UsuarioBase):
    """Datos requeridos para registrar un usuario."""

    contrasena: str = Field(..., min_length=6, max_length=72)


class UsuarioActualizar(BaseModel):
    """Datos editables de un usuario."""

    nombre_completo: str | None = None
    correo: EmailStr | None = None
    rol: RolUsuario | None = None
    contrasena: str | None = Field(default=None, min_length=6, max_length=72)


class UsuarioRespuesta(UsuarioBase):
    """Respuesta publica de usuario sin exponer hash de contrasena."""

    id: int
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)

