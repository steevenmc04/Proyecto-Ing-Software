import { Banknote, Check, CirclePlus, HandCoins, ListChecks, Search, X } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { Alerta, EncabezadoPagina, EstadoCarga, EstadoVacio, EtiquetaEstado, Panel } from '../../componentes/comunes/Interfaz'
import { useAutenticacion } from '../../contextos/EstadoAutenticacion'
import { clienteApi } from '../../servicios/clienteApi'
import type { Credito, Cuota, Socio } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'
import { fecha, moneda, nombreCompleto } from '../../utilidades/formato'

export function PaginaCreditos() {
  const { usuario } = useAutenticacion()
  const esSocio = usuario?.rol === 'SOCIO'
  const puedeSolicitar = esSocio || usuario?.rol === 'ADMINISTRADOR' || usuario?.rol === 'CAJERO'
  const puedeDecidir = usuario?.rol === 'ADMINISTRADOR' || usuario?.rol === 'GERENTE'
  const puedeCobrar = usuario?.rol === 'ADMINISTRADOR' || usuario?.rol === 'CAJERO'
  const [creditos, setCreditos] = useState<Credito[]>([])
  const [socios, setSocios] = useState<Socio[]>([])
  const [seleccionado, setSeleccionado] = useState<Credito | null>(null)
  const [cuotas, setCuotas] = useState<Cuota[]>([])
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [busqueda, setBusqueda] = useState('')
  const [socioId, setSocioId] = useState('')
  const [monto, setMonto] = useState('')
  const [plazo, setPlazo] = useState('12')
  const [tasa, setTasa] = useState('12')
  const [garantia, setGarantia] = useState('')
  const [proposito, setProposito] = useState('')
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  const cargar = useCallback(async () => {
    try {
      setCargando(true)
      if (esSocio) {
        const [perfil, propios] = await Promise.all([
          clienteApi.get<Socio>('/socios/perfil/me'),
          clienteApi.get<Credito[]>('/creditos/mis-creditos'),
        ])
        setSocios([perfil])
        setSocioId(String(perfil.id))
        setCreditos(propios)
      } else {
        const [todos, datosSocios] = await Promise.all([
          clienteApi.get<Credito[]>('/creditos?limit=1000'),
          clienteApi.get<Socio[]>('/socios?limit=1000'),
        ])
        setCreditos(todos)
        setSocios(datosSocios)
      }
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
    return creditos.filter((credito) =>
      [credito.numero_credito, credito.estado, credito.socio_id, credito.proposito]
        .join(' ')
        .toLowerCase()
        .includes(texto),
    )
  }, [busqueda, creditos])

  const seleccionar = async (credito: Credito) => {
    setSeleccionado(credito)
    setCuotas([])
    if (credito.estado !== 'PENDIENTE' && credito.estado !== 'RECHAZADO') {
      try {
        setCuotas(await clienteApi.get<Cuota[]>(`/creditos/${credito.id}/cuotas`))
      } catch (excepcion) {
        if (!esSocio) setError(mensajeError(excepcion))
      }
    }
  }

  const solicitar = async () => {
    if (!socioId || Number(monto) <= 0 || Number(plazo) <= 0 || Number(tasa) < 0 || !garantia || !proposito) {
      setError('Completa todos los datos del credito con valores validos')
      return
    }
    try {
      await clienteApi.post<Credito>('/creditos/solicitar', {
        socio_id: Number(socioId),
        monto_solicitado: Number(monto).toFixed(2),
        plazo_meses: Number(plazo),
        tasa_interes: Number(tasa).toFixed(2),
        tipo_garantia: garantia,
        proposito,
      })
      setMensaje('Solicitud de credito registrada')
      setMostrarFormulario(false)
      setMonto('')
      setGarantia('')
      setProposito('')
      await cargar()
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  const ejecutarAccion = async (accion: 'aprobar' | 'rechazar' | 'desembolsar' | 'pagar-cuota') => {
    if (!seleccionado || !usuario) return
    let datos: Record<string, unknown> = {}
    if (accion === 'aprobar') datos = { gerente_aprobador_id: usuario.id }
    if (accion === 'rechazar') {
      const motivo = window.prompt('Ingresa el motivo del rechazo')
      if (!motivo?.trim()) return
      datos = { motivo_rechazo: motivo.trim() }
    }
    if (accion === 'desembolsar') datos = { cajero_desembolso_id: usuario.id }
    if (accion === 'pagar-cuota') datos = { usuario_cajero_id: usuario.id }
    if (!window.confirm(`¿Confirmas la operacion ${accion.replace('-', ' ')}?`)) return
    try {
      if (accion === 'pagar-cuota') {
        await clienteApi.post<Cuota>(`/creditos/${seleccionado.id}/${accion}`, datos)
      } else {
        await clienteApi.patch<Credito>(`/creditos/${seleccionado.id}/${accion}`, datos)
      }
      setMensaje('Operacion de credito completada correctamente')
      await cargar()
      const actualizado = (await clienteApi.get<Credito[]>(esSocio ? '/creditos/mis-creditos' : '/creditos?limit=1000')).find((item) => item.id === seleccionado.id)
      if (actualizado) await seleccionar(actualizado)
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  return (
    <>
      <EncabezadoPagina
        titulo="Creditos"
        descripcion="Gestiona solicitudes, decisiones, amortizacion y pagos."
        acciones={puedeSolicitar ? <button className="boton-primario" onClick={() => setMostrarFormulario((valor) => !valor)}><CirclePlus /> Solicitar credito</button> : undefined}
      />
      {error && <Alerta tipo="error" mensaje={error} cerrar={() => setError('')} />}
      {mensaje && <Alerta tipo="exito" mensaje={mensaje} cerrar={() => setMensaje('')} />}
      {mostrarFormulario && (
        <Panel titulo="Nueva solicitud">
          <div className="formulario-rejilla">
            <label>Socio<select value={socioId} disabled={esSocio} onChange={(evento) => setSocioId(evento.target.value)}><option value="">Selecciona</option>{socios.filter((socio) => socio.estado === 'ACTIVO').map((socio) => <option value={socio.id} key={socio.id}>{socio.numero_socio} - {nombreCompleto(socio)}</option>)}</select></label>
            <label>Monto solicitado<input type="number" min="1" step="0.01" value={monto} onChange={(evento) => setMonto(evento.target.value)} /></label>
            <label>Plazo en meses<input type="number" min="1" max="120" value={plazo} onChange={(evento) => setPlazo(evento.target.value)} /></label>
            <label>Tasa anual (%)<input type="number" min="0" max="100" step="0.01" value={tasa} onChange={(evento) => setTasa(evento.target.value)} /></label>
            <label>Tipo de garantia<input value={garantia} onChange={(evento) => setGarantia(evento.target.value)} /></label>
            <label>Proposito<input value={proposito} onChange={(evento) => setProposito(evento.target.value)} /></label>
            <div className="acciones-formulario"><button type="button" className="boton-secundario" onClick={() => setMostrarFormulario(false)}>Cancelar</button><button type="button" className="boton-primario" onClick={() => void solicitar()}>Enviar solicitud</button></div>
          </div>
        </Panel>
      )}
      <div className="distribucion-detalle">
        <Panel>
          <div className="barra-herramientas"><label className="buscador"><Search /><input value={busqueda} onChange={(evento) => setBusqueda(evento.target.value)} placeholder="Numero, socio, estado o proposito" /></label></div>
          {cargando ? <EstadoCarga /> : visibles.length === 0 ? <EstadoVacio texto="No existen creditos para mostrar" /> : (
            <div className="tabla-contenedor"><table><thead><tr><th>Numero</th><th>Socio</th><th>Solicitud</th><th>Saldo</th><th>Estado</th></tr></thead><tbody>{visibles.map((credito) => <tr key={credito.id} onClick={() => void seleccionar(credito)} className={seleccionado?.id === credito.id ? 'fila-seleccionada' : ''}><td><strong>{credito.numero_credito}</strong></td><td>#{credito.socio_id}</td><td>{moneda(credito.monto_solicitado)}</td><td>{moneda(credito.saldo_pendiente)}</td><td><EtiquetaEstado valor={credito.estado} /></td></tr>)}</tbody></table></div>
          )}
        </Panel>
        <Panel titulo="Detalle del credito">
          {!seleccionado ? <EstadoVacio texto="Selecciona un credito" /> : (
            <div className="detalle-lista">
              <div><small>Numero</small><strong>{seleccionado.numero_credito}</strong></div>
              <div><small>Proposito</small><span>{seleccionado.proposito}</span></div>
              <div><small>Solicitud</small><span>{fecha(seleccionado.fecha_solicitud)}</span></div>
              <div><small>Monto aprobado</small><strong>{moneda(seleccionado.monto_aprobado)}</strong></div>
              <div><small>Saldo pendiente</small><strong>{moneda(seleccionado.saldo_pendiente)}</strong></div>
              <div><small>Estado</small><EtiquetaEstado valor={seleccionado.estado} /></div>
              <div className="grupo-botones">
                {puedeDecidir && seleccionado.estado === 'PENDIENTE' && <><button className="boton-primario" onClick={() => void ejecutarAccion('aprobar')}><Check /> Aprobar</button><button className="boton-secundario boton-peligro" onClick={() => void ejecutarAccion('rechazar')}><X /> Rechazar</button></>}
                {puedeCobrar && seleccionado.estado === 'APROBADO' && <button className="boton-primario" onClick={() => void ejecutarAccion('desembolsar')}><Banknote /> Desembolsar</button>}
                {puedeCobrar && ['DESEMBOLSADO', 'EN_PAGO'].includes(seleccionado.estado) && <button className="boton-primario" onClick={() => void ejecutarAccion('pagar-cuota')}><HandCoins /> Pagar siguiente cuota</button>}
              </div>
            </div>
          )}
        </Panel>
      </div>
      {seleccionado && cuotas.length > 0 && (
        <Panel titulo="Tabla de amortizacion">
          <div className="titulo-secundario"><ListChecks /><span>{cuotas.length} cuotas generadas por metodo frances</span></div>
          <div className="tabla-contenedor"><table><thead><tr><th>Cuota</th><th>Vencimiento</th><th>Capital</th><th>Interes</th><th>Total</th><th>Saldo</th><th>Estado</th></tr></thead><tbody>{cuotas.map((cuota) => <tr key={cuota.id}><td>#{cuota.numero_cuota}</td><td>{fecha(cuota.fecha_vencimiento)}</td><td>{moneda(cuota.capital)}</td><td>{moneda(cuota.interes)}</td><td><strong>{moneda(cuota.cuota_total)}</strong></td><td>{moneda(cuota.saldo_pendiente)}</td><td><EtiquetaEstado valor={cuota.estado} /></td></tr>)}</tbody></table></div>
        </Panel>
      )}
    </>
  )
}
