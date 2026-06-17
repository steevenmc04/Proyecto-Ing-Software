"""Archivo: app/servicios/usuario_servicio.py
Descripcion: Servicio de administracion de usuarios.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.esquemas.usuario_esquema import UsuarioActualizar, UsuarioCrear
from app.modelos.usuario_modelo import Usuario
from app.repositorios.usuario_repositorio import usuario_repositorio
from app.utilidades.seguridad import hashear_contrasena


class UsuarioServicio:
    """Aplica validaciones para crear y mantener usuarios."""

    def crear(self, db: Session, datos: UsuarioCrear):
        """Crea usuario evitando nombres o correos duplicados."""

        if usuario_repositorio.obtener_por_nombre_usuario(db, datos.nombre_usuario):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario ya existe")
        if usuario_repositorio.obtener_por_correo(db, str(datos.correo)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya existe")
        usuario = Usuario(
            nombre_usuario=datos.nombre_usuario,
            nombre_completo=datos.nombre_completo,
            correo=str(datos.correo),
            rol=datos.rol,
            contrasena_hash=hashear_contrasena(datos.contrasena),
        )
        return usuario_repositorio.guardar(db, usuario)

    def listar(self, db: Session, skip: int = 0, limit: int = 100):
        """Lista usuarios."""

        return usuario_repositorio.listar(db, skip, limit)

    def obtener(self, db: Session, usuario_id: int):
        """Obtiene usuario por ID."""

        usuario = usuario_repositorio.obtener(db, usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario

    def actualizar(self, db: Session, usuario_id: int, datos: UsuarioActualizar):
        """Actualiza datos de usuario y rehashea contrasena si cambia."""

        usuario = self.obtener(db, usuario_id)
        cambios = datos.model_dump(exclude_unset=True)
        if "correo" in cambios:
            existente = usuario_repositorio.obtener_por_correo(db, str(cambios["correo"]))
            if existente and existente.id != usuario_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya existe")
            usuario.correo = str(cambios.pop("correo"))
        if "contrasena" in cambios:
            usuario.contrasena_hash = hashear_contrasena(cambios.pop("contrasena"))
        for campo, valor in cambios.items():
            setattr(usuario, campo, valor)
        db.commit()
        db.refresh(usuario)
        return usuario

    def cambiar_estado(self, db: Session, usuario_id: int, activo: bool):
        """Activa o desactiva un usuario."""

        usuario = self.obtener(db, usuario_id)
        usuario.activo = activo
        db.commit()
        db.refresh(usuario)
        return usuario


usuario_servicio = UsuarioServicio()

