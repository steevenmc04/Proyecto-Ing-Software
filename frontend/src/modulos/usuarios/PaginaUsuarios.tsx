import { zodResolver } from '@hookform/resolvers/zod'
import { Pencil, Plus, Power, RefreshCcw, Search } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Alerta, EncabezadoPagina, EstadoCarga, EstadoVacio, EtiquetaEstado, Panel } from '../../componentes/comunes/Interfaz'
import { clienteApi } from '../../servicios/clienteApi'
import type { Rol, Usuario } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'

const esquemaUsuario = z.object({
  nombre_usuario: z.string().min(3, 'Minimo 3 caracteres'),
  nombre_completo: z.string().min(4, 'Ingresa el nombre completo'),
  correo: z.email('Correo no valido'),
  rol: z.enum(['ADMINISTRADOR', 'GERENTE', 'CAJERO', 'CONTADOR', 'SOCIO']),
  contrasena: z.string().refine((valor) => valor === '' || valor.length >= 6, 'Minimo 6 caracteres'),
})

type FormularioUsuario = z.infer<typeof esquemaUsuario>

export function PaginaUsuarios() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([])
  const [busqueda, setBusqueda] = useState('')
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [usuarioEditando, setUsuarioEditando] = useState<Usuario | null>(null)
  const [cargando, setCargando] = useState(true)
  const [mensaje, setMensaje] = useState('')
  const [error, setError] = useState('')
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormularioUsuario>({
    resolver: zodResolver(esquemaUsuario),
    defaultValues: { rol: 'CAJERO' },
  })

  const cargar = useCallback(async () => {
    try {
      setCargando(true)
      setUsuarios(await clienteApi.get<Usuario[]>('/usuarios?limit=1000'))
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    } finally {
      setCargando(false)
    }
  }, [])

  useEffect(() => {
    const temporizador = window.setTimeout(() => void cargar(), 0)
    return () => window.clearTimeout(temporizador)
  }, [cargar])

  const visibles = useMemo(() => {
    const texto = busqueda.trim().toLowerCase()
    if (!texto) return usuarios
    return usuarios.filter((usuario) =>
      [usuario.nombre_usuario, usuario.nombre_completo, usuario.correo, usuario.rol]
        .join(' ')
        .toLowerCase()
        .includes(texto),
    )
  }, [busqueda, usuarios])

  const abrirCreacion = () => {
    setUsuarioEditando(null)
    reset({ rol: 'CAJERO', nombre_usuario: '', nombre_completo: '', correo: '', contrasena: '' })
    setMostrarFormulario(true)
  }

  const abrirEdicion = (usuario: Usuario) => {
    setUsuarioEditando(usuario)
    reset({
      nombre_usuario: usuario.nombre_usuario,
      nombre_completo: usuario.nombre_completo,
      correo: usuario.correo,
      rol: usuario.rol,
      contrasena: '',
    })
    setMostrarFormulario(true)
  }

  const guardar = async (datos: FormularioUsuario) => {
    try {
      setError('')
      if (usuarioEditando) {
        await clienteApi.put<Usuario>(`/usuarios/${usuarioEditando.id}`, {
          nombre_completo: datos.nombre_completo,
          correo: datos.correo,
          rol: datos.rol,
          contrasena: datos.contrasena || undefined,
        })
        setMensaje('Usuario actualizado correctamente')
      } else {
        if (!datos.contrasena) {
          setError('La contrasena es obligatoria para crear un usuario')
          return
        }
        await clienteApi.post<Usuario>('/usuarios', datos)
        setMensaje('Usuario creado correctamente')
      }
      reset({ rol: 'CAJERO', nombre_usuario: '', nombre_completo: '', correo: '', contrasena: '' })
      setMostrarFormulario(false)
      setUsuarioEditando(null)
      await cargar()
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  const cambiarEstado = async (usuario: Usuario) => {
    const accion = usuario.activo ? 'desactivar' : 'activar'
    if (!window.confirm(`¿Deseas ${accion} a ${usuario.nombre_completo}?`)) return
    try {
      await clienteApi.patch<Usuario>(`/usuarios/${usuario.id}/${accion}`)
      setMensaje(`Usuario ${usuario.activo ? 'desactivado' : 'activado'} correctamente`)
      await cargar()
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  return (
    <>
      <EncabezadoPagina
        titulo="Usuarios"
        descripcion="Administra accesos, roles y estado de las cuentas internas."
        acciones={
          <button type="button" className="boton-primario" onClick={abrirCreacion}>
            <Plus /> Nuevo usuario
          </button>
        }
      />
      {error && <Alerta tipo="error" mensaje={error} cerrar={() => setError('')} />}
      {mensaje && <Alerta tipo="exito" mensaje={mensaje} cerrar={() => setMensaje('')} />}

      {mostrarFormulario && (
        <Panel titulo={usuarioEditando ? 'Editar usuario' : 'Crear usuario'}>
          <form className="formulario-rejilla" onSubmit={handleSubmit(guardar)}>
            <label>Usuario<input {...register('nombre_usuario')} disabled={Boolean(usuarioEditando)} />{errors.nombre_usuario && <small className="error-campo">{errors.nombre_usuario.message}</small>}</label>
            <label>Nombre completo<input {...register('nombre_completo')} />{errors.nombre_completo && <small className="error-campo">{errors.nombre_completo.message}</small>}</label>
            <label>Correo<input {...register('correo')} type="email" />{errors.correo && <small className="error-campo">{errors.correo.message}</small>}</label>
            <label>Rol<select {...register('rol')}><option>ADMINISTRADOR</option><option>GERENTE</option><option>CAJERO</option><option>CONTADOR</option><option>SOCIO</option></select></label>
            <label>{usuarioEditando ? 'Nueva contrasena (opcional)' : 'Contrasena'}<input {...register('contrasena')} type="password" />{errors.contrasena && <small className="error-campo">{errors.contrasena.message}</small>}</label>
            <div className="acciones-formulario">
              <button type="button" className="boton-secundario" onClick={() => { setMostrarFormulario(false); setUsuarioEditando(null) }}>Cancelar</button>
              <button className="boton-primario" disabled={isSubmitting}>{isSubmitting ? 'Guardando' : usuarioEditando ? 'Actualizar usuario' : 'Guardar usuario'}</button>
            </div>
          </form>
        </Panel>
      )}

      <Panel>
        <div className="barra-herramientas">
          <label className="buscador"><Search /><input value={busqueda} onChange={(evento) => setBusqueda(evento.target.value)} placeholder="Buscar por nombre, correo o rol" /></label>
          <button type="button" className="boton-icono" onClick={() => void cargar()} title="Actualizar listado"><RefreshCcw /></button>
        </div>
        {cargando ? <EstadoCarga /> : visibles.length === 0 ? <EstadoVacio texto="No se encontraron usuarios" /> : (
          <div className="tabla-contenedor">
            <table>
              <thead><tr><th>Usuario</th><th>Nombre</th><th>Correo</th><th>Rol</th><th>Estado</th><th>Acciones</th></tr></thead>
              <tbody>
                {visibles.map((usuario) => (
                  <tr key={usuario.id}>
                    <td><strong>{usuario.nombre_usuario}</strong></td>
                    <td>{usuario.nombre_completo}</td>
                    <td>{usuario.correo}</td>
                    <td>{usuario.rol as Rol}</td>
                    <td><EtiquetaEstado valor={usuario.activo ? 'ACTIVO' : 'INACTIVO'} /></td>
                    <td><div className="grupo-botones"><button type="button" className="boton-icono" onClick={() => abrirEdicion(usuario)} title="Editar usuario"><Pencil /></button><button type="button" className="boton-icono" onClick={() => void cambiarEstado(usuario)} title={usuario.activo ? 'Desactivar usuario' : 'Activar usuario'}><Power /></button></div></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>
    </>
  )
}
