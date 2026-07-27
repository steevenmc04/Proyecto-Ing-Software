import { CalendarRange, Search } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { Alerta, EncabezadoPagina, EstadoCarga, EstadoVacio, Panel } from '../../componentes/comunes/Interfaz'
import { clienteApi } from '../../servicios/clienteApi'
import type { Asiento } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'
import { fecha, moneda } from '../../utilidades/formato'

export function PaginaContabilidad() {
  const [asientos, setAsientos] = useState<Asiento[]>([])
  const [busqueda, setBusqueda] = useState('')
  const [fechaInicio, setFechaInicio] = useState('')
  const [fechaFin, setFechaFin] = useState('')
  const [seleccionado, setSeleccionado] = useState<Asiento | null>(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  const cargar = useCallback(async () => {
    try {
      setCargando(true)
      const parametros = new URLSearchParams()
      if (fechaInicio) parametros.set('fecha_inicio', fechaInicio)
      if (fechaFin) parametros.set('fecha_fin', fechaFin)
      const ruta = parametros.size ? `/asientos/rango-fechas?${parametros}` : '/asientos?limit=1000'
      setAsientos(await clienteApi.get<Asiento[]>(ruta))
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    } finally {
      setCargando(false)
    }
  }, [fechaFin, fechaInicio])

  useEffect(() => {
    const temporizador = window.setTimeout(() => void cargar(), 0)
    return () => window.clearTimeout(temporizador)
  }, [cargar])

  const visibles = useMemo(() => {
    const texto = busqueda.toLowerCase()
    return asientos.filter((asiento) => [asiento.descripcion, asiento.cuenta_debito, asiento.cuenta_credito, asiento.tipo_origen].join(' ').toLowerCase().includes(texto))
  }, [asientos, busqueda])

  const total = visibles.reduce((suma, asiento) => suma + Number(asiento.monto), 0)

  return (
    <>
      <EncabezadoPagina titulo="Libro Diario" descripcion="Consulta asientos de partida doble y su origen financiero." />
      {error && <Alerta tipo="error" mensaje={error} cerrar={() => setError('')} />}
      <Panel>
        <form className="barra-herramientas filtros" onSubmit={(evento) => { evento.preventDefault(); void cargar() }}>
          <label className="buscador"><Search /><input value={busqueda} onChange={(evento) => setBusqueda(evento.target.value)} placeholder="Descripcion, cuenta u origen" /></label>
          <label className="filtro-fecha"><CalendarRange /><input type="date" value={fechaInicio} onChange={(evento) => setFechaInicio(evento.target.value)} aria-label="Fecha inicial" /></label>
          <label className="filtro-fecha"><input type="date" value={fechaFin} onChange={(evento) => setFechaFin(evento.target.value)} aria-label="Fecha final" /></label>
          <button className="boton-secundario">Aplicar filtros</button>
        </form>
        {cargando ? <EstadoCarga /> : visibles.length === 0 ? <EstadoVacio texto="No existen asientos para los filtros aplicados" /> : (
          <div className="tabla-contenedor"><table><thead><tr><th>Fecha</th><th>Descripcion</th><th>Cuenta debito</th><th>Cuenta credito</th><th>Origen</th><th className="alinear-derecha">Debito</th><th className="alinear-derecha">Credito</th></tr></thead><tbody>{visibles.map((asiento) => <tr key={asiento.id} onClick={() => setSeleccionado(asiento)} className={seleccionado?.id === asiento.id ? 'fila-seleccionada' : ''}><td>{fecha(asiento.fecha)}</td><td><strong>{asiento.descripcion}</strong></td><td>{asiento.cuenta_debito}</td><td>{asiento.cuenta_credito}</td><td>{asiento.tipo_origen}</td><td className="alinear-derecha">{moneda(asiento.monto)}</td><td className="alinear-derecha">{moneda(asiento.monto)}</td></tr>)}</tbody><tfoot><tr><td colSpan={5}>Totales</td><td className="alinear-derecha">{moneda(total)}</td><td className="alinear-derecha">{moneda(total)}</td></tr></tfoot></table></div>
        )}
      </Panel>
      {seleccionado && <Panel titulo="Trazabilidad del asiento"><div className="comprobante"><div><small>ID</small><strong>#{seleccionado.id}</strong></div><div><small>Origen</small><span>{seleccionado.tipo_origen}</span></div><div><small>Transaccion</small><span>{seleccionado.transaccion_id ?? 'No aplica'}</span></div><div><small>Credito</small><span>{seleccionado.credito_id ?? 'No aplica'}</span></div><div><small>Aportacion</small><span>{seleccionado.aportacion_id ?? 'No aplica'}</span></div></div></Panel>}
    </>
  )
}
