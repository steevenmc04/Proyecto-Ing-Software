import { ArrowDownToLine, ArrowUpFromLine, HandCoins } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import { Alerta, EncabezadoPagina, EstadoCarga, EstadoVacio, Panel } from '../../componentes/comunes/Interfaz'
import { useAutenticacion } from '../../contextos/EstadoAutenticacion'
import { clienteApi } from '../../servicios/clienteApi'
import type { Aportacion, Socio, TipoAportacion } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'
import { fecha, moneda, nombreCompleto } from '../../utilidades/formato'

export function PaginaAportaciones() {
  const { usuario } = useAutenticacion()
  const puedeOperar = usuario?.rol === 'ADMINISTRADOR' || usuario?.rol === 'CAJERO'
  const [aportaciones, setAportaciones] = useState<Aportacion[]>([])
  const [tipos, setTipos] = useState<TipoAportacion[]>([])
  const [socios, setSocios] = useState<Socio[]>([])
  const [operacion, setOperacion] = useState<'deposito' | 'retiro'>('deposito')
  const [socioId, setSocioId] = useState('')
  const [tipoId, setTipoId] = useState('')
  const [monto, setMonto] = useState('')
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  const cargar = useCallback(async () => {
    try {
      setCargando(true)
      const [datosAportaciones, datosTipos, datosSocios] = await Promise.all([
        clienteApi.get<Aportacion[]>('/aportaciones?limit=1000'),
        clienteApi.get<TipoAportacion[]>('/aportaciones/tipos'),
        clienteApi.get<Socio[]>('/socios?limit=1000'),
      ])
      setAportaciones(datosAportaciones)
      setTipos(datosTipos)
      setSocios(datosSocios)
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

  const registrar = async () => {
    const valor = Number(monto)
    if (!socioId || !tipoId || !Number.isFinite(valor) || valor <= 0) {
      setError('Completa socio, tipo y monto mayor que cero')
      return
    }
    if (!window.confirm(`¿Confirmas el ${operacion} de aportacion por ${moneda(valor)}?`)) return
    try {
      await clienteApi.post<Aportacion>(`/aportaciones/${operacion}`, {
        socio_id: Number(socioId),
        tipo_aportacion_id: Number(tipoId),
        monto: valor.toFixed(2),
        usuario_cajero_id: usuario?.id,
      })
      setMensaje('Aportacion registrada correctamente')
      setMonto('')
      await cargar()
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  return (
    <>
      <EncabezadoPagina titulo="Aportaciones" descripcion="Gestiona aportaciones ordinarias y extraordinarias de los socios." />
      {error && <Alerta tipo="error" mensaje={error} cerrar={() => setError('')} />}
      {mensaje && <Alerta tipo="exito" mensaje={mensaje} cerrar={() => setMensaje('')} />}
      {puedeOperar && (
        <Panel titulo="Registrar aportacion">
          <div className="selector-segmentado"><button type="button" className={operacion === 'deposito' ? 'seleccionado' : ''} onClick={() => setOperacion('deposito')}><ArrowDownToLine /> Deposito</button><button type="button" className={operacion === 'retiro' ? 'seleccionado' : ''} onClick={() => setOperacion('retiro')}><ArrowUpFromLine /> Retiro</button></div>
          <div className="formulario-lineal">
            <label>Socio<select value={socioId} onChange={(evento) => setSocioId(evento.target.value)}><option value="">Selecciona</option>{socios.filter((socio) => socio.estado === 'ACTIVO').map((socio) => <option value={socio.id} key={socio.id}>{socio.numero_socio} - {nombreCompleto(socio)}</option>)}</select></label>
            <label>Tipo<select value={tipoId} onChange={(evento) => setTipoId(evento.target.value)}><option value="">Selecciona</option>{tipos.filter((tipo) => tipo.activo).map((tipo) => <option value={tipo.id} key={tipo.id}>{tipo.nombre}</option>)}</select></label>
            <label>Monto<input type="number" min="0.01" step="0.01" value={monto} onChange={(evento) => setMonto(evento.target.value)} /></label>
            <button type="button" className="boton-primario" onClick={() => void registrar()}><HandCoins /> Guardar aportacion</button>
          </div>
        </Panel>
      )}
      <Panel titulo="Historial de aportaciones">
        {cargando ? <EstadoCarga /> : aportaciones.length === 0 ? <EstadoVacio texto="No existen aportaciones" /> : (
          <div className="tabla-contenedor"><table><thead><tr><th>Fecha</th><th>Socio</th><th>Tipo</th><th>Operacion</th><th>Descripcion</th><th className="alinear-derecha">Monto</th></tr></thead><tbody>{aportaciones.map((aporte) => <tr key={aporte.id}><td>{fecha(aporte.fecha)}</td><td>Socio #{aporte.socio_id}</td><td>{tipos.find((tipo) => tipo.id === aporte.tipo_aportacion_id)?.nombre ?? aporte.tipo_aportacion_id}</td><td>{aporte.operacion === 'DEP' ? 'DEPOSITO' : 'RETIRO'}</td><td>{aporte.descripcion || 'Sin descripcion'}</td><td className="alinear-derecha">{moneda(aporte.monto)}</td></tr>)}</tbody></table></div>
        )}
      </Panel>
    </>
  )
}
