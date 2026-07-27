import { Ban, CirclePlus, LockKeyhole, Search, UnlockKeyhole } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { Alerta, EncabezadoPagina, EstadoCarga, EstadoVacio, EtiquetaEstado, Panel } from '../../componentes/comunes/Interfaz'
import { useAutenticacion } from '../../contextos/EstadoAutenticacion'
import { clienteApi } from '../../servicios/clienteApi'
import type { Cuenta, Socio } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'
import { fecha, moneda, nombreCompleto } from '../../utilidades/formato'

export function PaginaCuentas() {
  const { usuario } = useAutenticacion()
  const esSocio = usuario?.rol === 'SOCIO'
  const [cuentas, setCuentas] = useState<Cuenta[]>([])
  const [socios, setSocios] = useState<Socio[]>([])
  const [socioId, setSocioId] = useState('')
  const [busqueda, setBusqueda] = useState('')
  const [seleccionada, setSeleccionada] = useState<Cuenta | null>(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  const cargar = useCallback(async () => {
    try {
      setCargando(true)
      const [datosCuentas, datosSocios] = await Promise.all([
        clienteApi.get<Cuenta[]>(esSocio ? '/cuentas/mis-cuentas' : '/cuentas?limit=1000'),
        esSocio ? Promise.resolve([]) : clienteApi.get<Socio[]>('/socios?limit=1000'),
      ])
      setCuentas(datosCuentas)
      setSocios(datosSocios)
      setSeleccionada((actual) =>
        actual ? datosCuentas.find((cuenta) => cuenta.id === actual.id) ?? null : null,
      )
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    } finally {
      setCargando(false)
    }
  }, [esSocio])

  useEffect(() => {
    const temporizador = window.setTimeout(() => void cargar(), 0)
    return () => window.clearTimeout(temporizador)
  }, [cargar])

  const visibles = useMemo(() => {
    const texto = busqueda.toLowerCase()
    return cuentas.filter((cuenta) =>
      [cuenta.numero_cuenta, cuenta.estado, cuenta.socio_id].join(' ').toLowerCase().includes(texto),
    )
  }, [busqueda, cuentas])

  const crear = async () => {
    if (!socioId) {
      setError('Selecciona un socio para abrir la cuenta')
      return
    }
    try {
      await clienteApi.post<Cuenta>('/cuentas', { socio_id: Number(socioId) })
      setMensaje('Cuenta creada con saldo inicial cero')
      setSocioId('')
      await cargar()
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  const cambiarEstado = async (accion: 'bloquear' | 'desbloquear' | 'cerrar') => {
    if (!seleccionada) return
    if (!window.confirm(`¿Confirmas ${accion} la cuenta ${seleccionada.numero_cuenta}?`)) return
    try {
      const actualizada = await clienteApi.patch<Cuenta>(`/cuentas/${seleccionada.id}/${accion}`)
      setSeleccionada(actualizada)
      setMensaje(`Cuenta ${accion === 'bloquear' ? 'bloqueada' : accion === 'desbloquear' ? 'desbloqueada' : 'cerrada'} correctamente`)
      await cargar()
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  return (
    <>
      <EncabezadoPagina titulo="Cuentas de ahorro" descripcion="Consulta saldos, titulares y estado operativo de cada cuenta." />
      {error && <Alerta tipo="error" mensaje={error} cerrar={() => setError('')} />}
      {mensaje && <Alerta tipo="exito" mensaje={mensaje} cerrar={() => setMensaje('')} />}

      {!esSocio && (
        <Panel titulo="Abrir cuenta">
          <div className="formulario-lineal">
            <label>Socio
              <select value={socioId} onChange={(evento) => setSocioId(evento.target.value)}>
                <option value="">Selecciona un socio activo</option>
                {socios.filter((socio) => socio.estado === 'ACTIVO').map((socio) => <option value={socio.id} key={socio.id}>{socio.numero_socio} - {nombreCompleto(socio)}</option>)}
              </select>
            </label>
            <button type="button" className="boton-primario" onClick={() => void crear()}><CirclePlus /> Crear cuenta</button>
          </div>
        </Panel>
      )}

      <div className="distribucion-detalle">
        <Panel>
          <div className="barra-herramientas"><label className="buscador"><Search /><input value={busqueda} onChange={(evento) => setBusqueda(evento.target.value)} placeholder="Numero, estado o socio" /></label></div>
          {cargando ? <EstadoCarga /> : visibles.length === 0 ? <EstadoVacio texto="No existen cuentas para mostrar" /> : (
            <div className="tabla-contenedor">
              <table>
                <thead><tr><th>Numero</th><th>Socio</th><th>Saldo</th><th>Apertura</th><th>Estado</th></tr></thead>
                <tbody>
                  {visibles.map((cuenta) => (
                    <tr key={cuenta.id} onClick={() => setSeleccionada(cuenta)} className={seleccionada?.id === cuenta.id ? 'fila-seleccionada' : ''}>
                      <td><strong>{cuenta.numero_cuenta}</strong></td><td>Socio #{cuenta.socio_id}</td><td>{moneda(cuenta.saldo)}</td><td>{fecha(cuenta.fecha_apertura)}</td><td><EtiquetaEstado valor={cuenta.estado} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>
        <Panel titulo="Detalle de cuenta">
          {!seleccionada ? <EstadoVacio texto="Selecciona una cuenta" /> : (
            <div className="detalle-lista">
              <div><small>Numero</small><strong>{seleccionada.numero_cuenta}</strong></div>
              <div><small>Saldo disponible</small><strong className="monto-destacado">{moneda(seleccionada.saldo)}</strong></div>
              <div><small>Estado</small><EtiquetaEstado valor={seleccionada.estado} /></div>
              {!esSocio && (
                <div className="grupo-botones">
                  {seleccionada.estado !== 'BLOQUEADA' && seleccionada.estado !== 'CERRADA' && <button className="boton-secundario" onClick={() => void cambiarEstado('bloquear')}><LockKeyhole /> Bloquear</button>}
                  {seleccionada.estado === 'BLOQUEADA' && <button className="boton-secundario" onClick={() => void cambiarEstado('desbloquear')}><UnlockKeyhole /> Desbloquear</button>}
                  {seleccionada.estado !== 'CERRADA' && <button className="boton-secundario boton-peligro" onClick={() => void cambiarEstado('cerrar')}><Ban /> Cerrar</button>}
                </div>
              )}
            </div>
          )}
        </Panel>
      </div>
    </>
  )
}
