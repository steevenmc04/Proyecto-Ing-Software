import { ArrowDownToLine, ArrowUpFromLine, CalendarRange, ReceiptText, Search } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { Alerta, EncabezadoPagina, EstadoCarga, EstadoVacio, Panel } from '../../componentes/comunes/Interfaz'
import { useAutenticacion } from '../../contextos/EstadoAutenticacion'
import { clienteApi } from '../../servicios/clienteApi'
import type { Cuenta, Transaccion } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'
import { fecha, moneda } from '../../utilidades/formato'

export function PaginaTransacciones() {
  const { usuario } = useAutenticacion()
  const puedeOperar = usuario?.rol === 'ADMINISTRADOR' || usuario?.rol === 'CAJERO'
  const [cuentas, setCuentas] = useState<Cuenta[]>([])
  const [movimientos, setMovimientos] = useState<Transaccion[]>([])
  const [tipo, setTipo] = useState<'deposito' | 'retiro'>('deposito')
  const [cuentaId, setCuentaId] = useState('')
  const [monto, setMonto] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [busqueda, setBusqueda] = useState('')
  const [fechaInicio, setFechaInicio] = useState('')
  const [fechaFin, setFechaFin] = useState('')
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')
  const [comprobante, setComprobante] = useState<Transaccion | null>(null)

  const cargar = useCallback(async () => {
    try {
      setCargando(true)
      const esSocio = usuario?.rol === 'SOCIO'
      const [datosCuentas, datosMovimientos] = await Promise.all([
        clienteApi.get<Cuenta[]>(esSocio ? '/cuentas/mis-cuentas' : '/cuentas?limit=1000'),
        clienteApi.get<Transaccion[]>(esSocio ? '/transacciones/mis-transacciones' : '/transacciones?limit=1000'),
      ])
      setCuentas(datosCuentas)
      setMovimientos(datosMovimientos)
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    } finally {
      setCargando(false)
    }
  }, [usuario])

  useEffect(() => {
    const temporizador = window.setTimeout(() => void cargar(), 0)
    return () => window.clearTimeout(temporizador)
  }, [cargar])

  const visibles = useMemo(() => movimientos.filter((movimiento) => {
    const texto = busqueda.toLowerCase()
    const coincideTexto = [movimiento.numero_comprobante, movimiento.tipo_transaccion, movimiento.descripcion, movimiento.cuenta_id].join(' ').toLowerCase().includes(texto)
    const dia = movimiento.fecha.slice(0, 10)
    return coincideTexto && (!fechaInicio || dia >= fechaInicio) && (!fechaFin || dia <= fechaFin)
  }), [busqueda, fechaFin, fechaInicio, movimientos])

  const registrar = async () => {
    const valor = Number(monto)
    if (!cuentaId || !Number.isFinite(valor) || valor <= 0) {
      setError('Selecciona una cuenta e ingresa un monto mayor que cero')
      return
    }
    const cuenta = cuentas.find((item) => item.id === Number(cuentaId))
    if (!cuenta || !['ACTIVA', 'SALDO_CERO'].includes(cuenta.estado)) {
      setError('La cuenta seleccionada no permite movimientos')
      return
    }
    if (tipo === 'retiro' && Number(cuenta.saldo) < valor) {
      setError('El saldo disponible no cubre el retiro')
      return
    }
    if (!window.confirm(`¿Confirmas el ${tipo} de ${moneda(valor)} en ${cuenta.numero_cuenta}?`)) return
    try {
      const resultado = await clienteApi.post<Transaccion>(`/transacciones/${tipo}`, {
        cuenta_id: Number(cuentaId),
        monto: valor.toFixed(2),
        descripcion: descripcion || undefined,
        usuario_cajero_id: usuario?.id,
      })
      setComprobante(resultado)
      setMensaje(`${tipo === 'deposito' ? 'Deposito' : 'Retiro'} registrado correctamente`)
      setMonto('')
      setDescripcion('')
      await cargar()
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  return (
    <>
      <EncabezadoPagina titulo="Transacciones" descripcion="Registra operaciones y consulta el historial de movimientos." />
      {error && <Alerta tipo="error" mensaje={error} cerrar={() => setError('')} />}
      {mensaje && <Alerta tipo="exito" mensaje={mensaje} cerrar={() => setMensaje('')} />}

      {puedeOperar && (
        <Panel titulo="Nueva operacion">
          <div className="selector-segmentado" role="group" aria-label="Tipo de operacion">
            <button type="button" className={tipo === 'deposito' ? 'seleccionado' : ''} onClick={() => setTipo('deposito')}><ArrowDownToLine /> Deposito</button>
            <button type="button" className={tipo === 'retiro' ? 'seleccionado' : ''} onClick={() => setTipo('retiro')}><ArrowUpFromLine /> Retiro</button>
          </div>
          <div className="formulario-lineal">
            <label>Cuenta<select value={cuentaId} onChange={(evento) => setCuentaId(evento.target.value)}><option value="">Selecciona una cuenta</option>{cuentas.map((cuenta) => <option value={cuenta.id} key={cuenta.id}>{cuenta.numero_cuenta} - {moneda(cuenta.saldo)} - {cuenta.estado}</option>)}</select></label>
            <label>Monto<input type="number" min="0.01" step="0.01" value={monto} onChange={(evento) => setMonto(evento.target.value)} placeholder="0.00" /></label>
            <label>Descripcion<input value={descripcion} onChange={(evento) => setDescripcion(evento.target.value)} placeholder="Motivo de la operacion" /></label>
            <button type="button" className="boton-primario" onClick={() => void registrar()}><ReceiptText /> Confirmar operacion</button>
          </div>
        </Panel>
      )}

      {comprobante && (
        <Panel titulo="Comprobante generado">
          <div className="comprobante">
            <div><small>Numero</small><strong>{comprobante.numero_comprobante}</strong></div><div><small>Operacion</small><span>{comprobante.tipo_transaccion}</span></div><div><small>Monto</small><strong>{moneda(comprobante.monto)}</strong></div><div><small>Saldo resultante</small><strong>{moneda(comprobante.saldo_resultante)}</strong></div>
          </div>
        </Panel>
      )}

      <Panel titulo="Historial">
        <div className="barra-herramientas filtros">
          <label className="buscador"><Search /><input value={busqueda} onChange={(evento) => setBusqueda(evento.target.value)} placeholder="Comprobante, tipo o cuenta" /></label>
          <label className="filtro-fecha"><CalendarRange /><input type="date" value={fechaInicio} onChange={(evento) => setFechaInicio(evento.target.value)} aria-label="Fecha inicial" /></label>
          <label className="filtro-fecha"><input type="date" value={fechaFin} onChange={(evento) => setFechaFin(evento.target.value)} aria-label="Fecha final" /></label>
        </div>
        {cargando ? <EstadoCarga /> : visibles.length === 0 ? <EstadoVacio texto="No existen movimientos para los filtros aplicados" /> : (
          <div className="tabla-contenedor"><table><thead><tr><th>Comprobante</th><th>Fecha</th><th>Tipo</th><th>Cuenta</th><th>Descripcion</th><th className="alinear-derecha">Monto</th><th className="alinear-derecha">Saldo</th></tr></thead><tbody>{visibles.map((movimiento) => <tr key={movimiento.id}><td><strong>{movimiento.numero_comprobante}</strong></td><td>{fecha(movimiento.fecha)}</td><td>{movimiento.tipo_transaccion}</td><td>#{movimiento.cuenta_id}</td><td>{movimiento.descripcion || 'Sin descripcion'}</td><td className="alinear-derecha">{moneda(movimiento.monto)}</td><td className="alinear-derecha">{moneda(movimiento.saldo_resultante)}</td></tr>)}</tbody></table></div>
        )}
      </Panel>
    </>
  )
}
