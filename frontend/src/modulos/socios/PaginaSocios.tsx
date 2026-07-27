import { zodResolver } from '@hookform/resolvers/zod'
import { Pencil, Plus, Power, Search, UserRoundSearch } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Alerta, EncabezadoPagina, EstadoCarga, EstadoVacio, EtiquetaEstado, Panel } from '../../componentes/comunes/Interfaz'
import { clienteApi } from '../../servicios/clienteApi'
import type { Socio } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'
import { fecha, moneda, nombreCompleto } from '../../utilidades/formato'

const esquemaSocio = z.object({
  cedula: z.string().min(10, 'Ingresa una identificacion valida').max(20),
  nombres: z.string().min(2, 'Ingresa los nombres'),
  apellidos: z.string().min(2, 'Ingresa los apellidos'),
  fecha_nacimiento: z.string().min(1, 'Selecciona la fecha'),
  direccion: z.string().min(3, 'Ingresa la direccion'),
  telefono: z.string().min(7, 'Ingresa un telefono valido'),
  correo: z.email('Correo no valido'),
})

type FormularioSocio = z.infer<typeof esquemaSocio>

export function PaginaSocios() {
  const [socios, setSocios] = useState<Socio[]>([])
  const [buscar, setBuscar] = useState('')
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [seleccionado, setSeleccionado] = useState<Socio | null>(null)
  const [socioEditando, setSocioEditando] = useState<Socio | null>(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<FormularioSocio>({
    resolver: zodResolver(esquemaSocio),
  })

  const cargar = useCallback(async (termino = '') => {
    try {
      setCargando(true)
      const query = termino.trim() ? `?buscar=${encodeURIComponent(termino.trim())}&limit=1000` : '?limit=1000'
      setSocios(await clienteApi.get<Socio[]>(`/socios${query}`))
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

  const abrirCreacion = () => {
    setSocioEditando(null)
    reset()
    setMostrarFormulario(true)
  }

  const abrirEdicion = (socio: Socio) => {
    setSocioEditando(socio)
    reset({
      cedula: socio.cedula,
      nombres: socio.nombres,
      apellidos: socio.apellidos,
      fecha_nacimiento: socio.fecha_nacimiento.slice(0, 10),
      direccion: socio.direccion,
      telefono: socio.telefono,
      correo: socio.correo,
    })
    setMostrarFormulario(true)
  }

  const guardar = async (datos: FormularioSocio) => {
    try {
      if (socioEditando) {
        const actualizado = await clienteApi.put<Socio>(`/socios/${socioEditando.id}`, {
          nombres: datos.nombres,
          apellidos: datos.apellidos,
          fecha_nacimiento: datos.fecha_nacimiento,
          direccion: datos.direccion,
          telefono: datos.telefono,
          correo: datos.correo,
        })
        setSeleccionado(actualizado)
        setMensaje('Socio actualizado correctamente')
      } else {
        await clienteApi.post<Socio>('/socios', datos)
        setMensaje('Socio registrado correctamente')
      }
      setMostrarFormulario(false)
      setSocioEditando(null)
      reset()
      await cargar(buscar)
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  const cambiarEstado = async (socio: Socio) => {
    const accion = socio.estado === 'ACTIVO' ? 'desactivar' : 'activar'
    if (!window.confirm(`¿Confirmas ${accion} a ${nombreCompleto(socio)}?`)) return
    try {
      await clienteApi.patch<Socio>(`/socios/${socio.id}/${accion}`)
      setMensaje(`Socio ${accion === 'activar' ? 'activado' : 'desactivado'} correctamente`)
      setSeleccionado(null)
      await cargar(buscar)
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  return (
    <>
      <EncabezadoPagina
        titulo="Socios"
        descripcion="Consulta, registra y administra los miembros de la caja."
        acciones={<button className="boton-primario" onClick={abrirCreacion}><Plus /> Registrar socio</button>}
      />
      {error && <Alerta tipo="error" mensaje={error} cerrar={() => setError('')} />}
      {mensaje && <Alerta tipo="exito" mensaje={mensaje} cerrar={() => setMensaje('')} />}

      {mostrarFormulario && (
        <Panel titulo={socioEditando ? 'Editar socio' : 'Registro de socio'}>
          <form className="formulario-rejilla" onSubmit={handleSubmit(guardar)}>
            <label>Cedula<input {...register('cedula')} disabled={Boolean(socioEditando)} />{errors.cedula && <small className="error-campo">{errors.cedula.message}</small>}</label>
            <label>Nombres<input {...register('nombres')} />{errors.nombres && <small className="error-campo">{errors.nombres.message}</small>}</label>
            <label>Apellidos<input {...register('apellidos')} />{errors.apellidos && <small className="error-campo">{errors.apellidos.message}</small>}</label>
            <label>Fecha de nacimiento<input {...register('fecha_nacimiento')} type="date" />{errors.fecha_nacimiento && <small className="error-campo">{errors.fecha_nacimiento.message}</small>}</label>
            <label>Direccion<input {...register('direccion')} />{errors.direccion && <small className="error-campo">{errors.direccion.message}</small>}</label>
            <label>Telefono<input {...register('telefono')} />{errors.telefono && <small className="error-campo">{errors.telefono.message}</small>}</label>
            <label>Correo<input {...register('correo')} type="email" />{errors.correo && <small className="error-campo">{errors.correo.message}</small>}</label>
            <div className="acciones-formulario"><button type="button" className="boton-secundario" onClick={() => { setMostrarFormulario(false); setSocioEditando(null) }}>Cancelar</button><button className="boton-primario" disabled={isSubmitting}>{socioEditando ? 'Actualizar socio' : 'Guardar socio'}</button></div>
          </form>
        </Panel>
      )}

      <div className="distribucion-detalle">
        <Panel>
          <form className="barra-herramientas" onSubmit={(evento) => { evento.preventDefault(); void cargar(buscar) }}>
            <label className="buscador"><Search /><input value={buscar} onChange={(evento) => setBuscar(evento.target.value)} placeholder="Cedula, nombre o numero de socio" /></label>
            <button className="boton-secundario"><UserRoundSearch /> Buscar</button>
          </form>
          {cargando ? <EstadoCarga /> : socios.length === 0 ? <EstadoVacio texto="No se encontraron socios" /> : (
            <div className="tabla-contenedor">
              <table>
                <thead><tr><th>Numero</th><th>Socio</th><th>Cedula</th><th>Aportaciones</th><th>Estado</th></tr></thead>
                <tbody>
                  {socios.map((socio) => (
                    <tr key={socio.id} className={seleccionado?.id === socio.id ? 'fila-seleccionada' : ''} onClick={() => setSeleccionado(socio)}>
                      <td><strong>{socio.numero_socio}</strong></td><td>{nombreCompleto(socio)}</td><td>{socio.cedula}</td><td>{moneda(socio.total_aportaciones)}</td><td><EtiquetaEstado valor={socio.estado} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>
        <Panel titulo="Detalle del socio">
          {!seleccionado ? <EstadoVacio texto="Selecciona un socio para ver su detalle" /> : (
            <div className="detalle-lista">
              <div><small>Nombre completo</small><strong>{nombreCompleto(seleccionado)}</strong></div>
              <div><small>Numero de socio</small><span>{seleccionado.numero_socio}</span></div>
              <div><small>Fecha de nacimiento</small><span>{fecha(seleccionado.fecha_nacimiento)}</span></div>
              <div><small>Correo</small><span>{seleccionado.correo}</span></div>
              <div><small>Telefono</small><span>{seleccionado.telefono}</span></div>
              <div><small>Direccion</small><span>{seleccionado.direccion}</span></div>
              <div className="grupo-botones"><button type="button" className="boton-secundario" onClick={() => abrirEdicion(seleccionado)}><Pencil /> Editar socio</button><button type="button" className="boton-secundario boton-peligro" onClick={() => void cambiarEstado(seleccionado)}><Power /> {seleccionado.estado === 'ACTIVO' ? 'Desactivar' : 'Activar'} socio</button></div>
            </div>
          )}
        </Panel>
      </div>
    </>
  )
}
