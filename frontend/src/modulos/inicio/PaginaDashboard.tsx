import {
  ArrowDownLeft,
  ArrowUpRight,
  CreditCard,
  Landmark,
  TrendingUp,
  Users,
} from 'lucide-react'
import { useEffect, useState } from 'react'
import { Alerta, EncabezadoPagina, EstadoCarga, EstadoVacio, EtiquetaEstado, Panel } from '../../componentes/comunes/Interfaz'
import { useAutenticacion } from '../../contextos/EstadoAutenticacion'
import { clienteApi } from '../../servicios/clienteApi'
import type { Credito, Cuenta, Socio, Transaccion } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'
import { fecha, moneda } from '../../utilidades/formato'

export function PaginaDashboard() {
  const { usuario } = useAutenticacion()
  const [socios, setSocios] = useState<Socio[]>([])
  const [cuentas, setCuentas] = useState<Cuenta[]>([])
  const [movimientos, setMovimientos] = useState<Transaccion[]>([])
  const [creditos, setCreditos] = useState<Credito[]>([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const controlador = new AbortController()
    const cargar = async () => {
      try {
        const esSocio = usuario?.rol === 'SOCIO'
        const [datosSocios, datosCuentas, datosMovimientos, datosCreditos] = await Promise.all([
          esSocio
            ? clienteApi.get<Socio>('/socios/perfil/me', controlador.signal).then((dato) => [dato])
            : clienteApi.get<Socio[]>('/socios?limit=1000', controlador.signal),
          clienteApi.get<Cuenta[]>(esSocio ? '/cuentas/mis-cuentas' : '/cuentas?limit=1000', controlador.signal),
          clienteApi.get<Transaccion[]>(
            esSocio ? '/transacciones/mis-transacciones' : '/transacciones?limit=8',
            controlador.signal,
          ),
          clienteApi.get<Credito[]>(esSocio ? '/creditos/mis-creditos' : '/creditos?limit=1000', controlador.signal),
        ])
        setSocios(datosSocios)
        setCuentas(datosCuentas)
        setMovimientos(datosMovimientos)
        setCreditos(datosCreditos)
      } catch (excepcion) {
        if (!(excepcion instanceof DOMException && excepcion.name === 'AbortError')) {
          setError(mensajeError(excepcion))
        }
      } finally {
        setCargando(false)
      }
    }
    void cargar()
    return () => controlador.abort()
  }, [usuario?.rol])

  if (cargando) return <EstadoCarga texto="Preparando panel general" />

  const sociosActivos = socios.filter((socio) => socio.estado === 'ACTIVO').length
  const saldoAhorros = cuentas.reduce((total, cuenta) => total + Number(cuenta.saldo), 0)
  const creditosPendientes = creditos.filter((credito) => credito.estado === 'PENDIENTE').length
  const cartera = creditos.reduce((total, credito) => total + Number(credito.saldo_pendiente), 0)

  return (
    <>
      <EncabezadoPagina
        titulo={`Buenos dias, ${usuario?.nombre_completo.split(' ')[0] ?? 'usuario'}`}
        descripcion="Este es el estado actual de la caja de ahorros."
      />
      {error && <Alerta tipo="error" mensaje={error} />}
      <section className="rejilla-indicadores">
        <article className="indicador">
          <span className="indicador-icono indicador-verde"><Users /></span>
          <div><small>Socios activos</small><strong>{sociosActivos}</strong></div>
          <span className="tendencia">Datos actuales</span>
        </article>
        <article className="indicador">
          <span className="indicador-icono indicador-azul"><Landmark /></span>
          <div><small>Saldo total de ahorros</small><strong>{moneda(saldoAhorros)}</strong></div>
          <span className="tendencia">En {cuentas.length} cuentas</span>
        </article>
        <article className="indicador">
          <span className="indicador-icono indicador-ambar"><CreditCard /></span>
          <div><small>Creditos pendientes</small><strong>{creditosPendientes}</strong></div>
          <span className="tendencia">Por revisar</span>
        </article>
        <article className="indicador">
          <span className="indicador-icono indicador-rojo"><TrendingUp /></span>
          <div><small>Cartera de creditos</small><strong>{moneda(cartera)}</strong></div>
          <span className="tendencia">Saldo pendiente</span>
        </article>
      </section>

      <Panel titulo="Movimientos recientes">
        {movimientos.length === 0 ? (
          <EstadoVacio texto="Todavia no existen movimientos para mostrar" />
        ) : (
          <div className="tabla-contenedor">
            <table>
              <thead>
                <tr>
                  <th>Comprobante</th>
                  <th>Tipo</th>
                  <th>Fecha</th>
                  <th>Cuenta</th>
                  <th className="alinear-derecha">Monto</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {movimientos.slice(0, 8).map((movimiento) => (
                  <tr key={movimiento.id}>
                    <td><strong>{movimiento.numero_comprobante}</strong></td>
                    <td>
                      <span className={`tipo-movimiento ${movimiento.tipo_transaccion === 'DEPOSITO' ? 'tipo-ingreso' : 'tipo-egreso'}`}>
                        {movimiento.tipo_transaccion === 'DEPOSITO' ? <ArrowDownLeft /> : <ArrowUpRight />}
                        {movimiento.tipo_transaccion}
                      </span>
                    </td>
                    <td>{fecha(movimiento.fecha)}</td>
                    <td>Cuenta #{movimiento.cuenta_id}</td>
                    <td className="alinear-derecha">{moneda(movimiento.monto)}</td>
                    <td><EtiquetaEstado valor="PROCESADO" /></td>
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
