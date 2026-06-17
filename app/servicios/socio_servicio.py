"""Archivo: app/servicios/socio_servicio.py
Descripcion: Servicio de reglas para socios.
Autor: Martinez Steeven
Version: 1.0
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.esquemas.socio_esquema import SocioActualizar, SocioCrear
from app.modelos.socio_modelo import EstadoSocio, Socio
from app.repositorios.socio_repositorio import socio_repositorio
from app.repositorios.usuario_repositorio import usuario_repositorio
from app.utilidades.generadores import generar_codigo_secuencial


class SocioServicio:
    """Gestiona registro, busqueda y estado de socios."""

    def crear(self, db: Session, datos: SocioCrear):
        """Registra un socio con numero unico y cedula no duplicada."""

        if socio_repositorio.obtener_por_cedula(db, datos.cedula):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un socio con esa cedula")
        if datos.usuario_registro_id and not usuario_repositorio.obtener(db, datos.usuario_registro_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario registrador no encontrado")
        socio = Socio(
            numero_socio=generar_codigo_secuencial(db, Socio, "numero_socio", "SOC"),
            cedula=datos.cedula,
            nombres=datos.nombres,
            apellidos=datos.apellidos,
            fecha_nacimiento=datos.fecha_nacimiento,
            direccion=datos.direccion,
            telefono=datos.telefono,
            correo=str(datos.correo),
            usuario_registro_id=datos.usuario_registro_id,
        )
        return socio_repositorio.guardar(db, socio)

    def listar(self, db: Session, skip: int = 0, limit: int = 100, buscar: str | None = None):
        """Lista socios o busca por termino."""

        if buscar:
            return socio_repositorio.buscar(db, buscar)
        return socio_repositorio.listar(db, skip, limit)

    def obtener(self, db: Session, socio_id: int):
        """Obtiene socio por ID."""

        socio = socio_repositorio.obtener(db, socio_id)
        if not socio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
        return socio

    def obtener_por_cedula(self, db: Session, cedula: str):
        """Obtiene socio por cedula."""

        socio = socio_repositorio.obtener_por_cedula(db, cedula)
        if not socio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Socio no encontrado")
        return socio

    def actualizar(self, db: Session, socio_id: int, datos: SocioActualizar):
        """Actualiza datos personales del socio."""

        socio = self.obtener(db, socio_id)
        cambios = datos.model_dump(exclude_unset=True)
        if "correo" in cambios:
            socio.correo = str(cambios.pop("correo"))
        for campo, valor in cambios.items():
            setattr(socio, campo, valor)
        db.commit()
        db.refresh(socio)
        return socio

    def cambiar_estado(self, db: Session, socio_id: int, activo: bool):
        """Activa o desactiva un socio."""

        socio = self.obtener(db, socio_id)
        socio.estado = EstadoSocio.ACTIVO if activo else EstadoSocio.INACTIVO
        db.commit()
        db.refresh(socio)
        return socio


socio_servicio = SocioServicio()

