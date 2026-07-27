import { Download, FileSpreadsheet, FileText, Play } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Alerta, EncabezadoPagina, EstadoVacio, Panel } from '../../componentes/comunes/Interfaz'
import { clienteApi } from '../../servicios/clienteApi'
import type { Socio } from '../../tipos/dominio'
import { mensajeError } from '../../utilidades/errores'
import { nombreCompleto } from '../../utilidades/formato'

type TipoReporte = 'libro-diario' | 'cartera-creditos' | 'historial-ahorros' | 'resumen-aportaciones'

function aFilas(datos: unknown): Array<Record<string, unknown>> {
  if (Array.isArray(datos)) return datos as Array<Record<string, unknown>>
  if (datos && typeof datos === 'object') {
    const objeto = datos as Record<string, unknown>
    const lista = Object.values(objeto).find((valor) => Array.isArray(valor))
    if (Array.isArray(lista)) return lista as Array<Record<string, unknown>>
    return [objeto]
  }
  return []
}

export function PaginaReportes() {
  const [tipo, setTipo] = useState<TipoReporte>('libro-diario')
  const [socios, setSocios] = useState<Socio[]>([])
  const [socioId, setSocioId] = useState('')
  const [resultado, setResultado] = useState<unknown>(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    clienteApi.get<Socio[]>('/socios?limit=1000').then(setSocios).catch((excepcion) => setError(mensajeError(excepcion)))
  }, [])

  const generar = async () => {
    if (['historial-ahorros', 'resumen-aportaciones'].includes(tipo) && !socioId) {
      setError('Selecciona un socio para generar este reporte')
      return
    }
    try {
      setCargando(true)
      const ruta = ['historial-ahorros', 'resumen-aportaciones'].includes(tipo)
        ? `/reportes/${tipo}/${socioId}`
        : `/reportes/${tipo}`
      setResultado(await clienteApi.get<unknown>(ruta))
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    } finally {
      setCargando(false)
    }
  }

  const exportarPdf = async () => {
    const filas = aFilas(resultado)
    if (!filas.length) return
    const [{ default: jsPDF }, { default: autoTable }] = await Promise.all([
      import('jspdf'),
      import('jspdf-autotable'),
    ])
    const columnas = Object.keys(filas[0])
    const documento = new jsPDF({ orientation: columnas.length > 6 ? 'landscape' : 'portrait' })
    documento.setFontSize(16)
    documento.text('Sistema de Gestion de Caja de Ahorros', 14, 18)
    documento.setFontSize(10)
    documento.text(`Reporte: ${tipo.replaceAll('-', ' ')}`, 14, 25)
    documento.text(`Generado: ${new Date().toLocaleString('es-EC')}`, 14, 31)
    autoTable(documento, {
      startY: 37,
      head: [columnas],
      body: filas.map((fila) => columnas.map((columna) => String(fila[columna] ?? ''))),
      styles: { fontSize: 7 },
      headStyles: { fillColor: [20, 94, 74] },
    })
    documento.save(`reporte-${tipo}.pdf`)
  }

  const exportarXlsx = async () => {
    const filas = aFilas(resultado)
    if (!filas.length) return
    const { default: writeXlsxFile } = await import('write-excel-file/browser')
    const columnas = Object.keys(filas[0])
    const datos = [
      columnas.map((columna) => ({ value: columna, fontWeight: 'bold' as const, backgroundColor: '#DDEFE8' })),
      ...filas.map((fila) => columnas.map((columna) => ({ value: String(fila[columna] ?? '') }))),
    ]
    await writeXlsxFile(datos).toFile(`reporte-${tipo}.xlsx`)
  }

  const filas = aFilas(resultado)

  return (
    <>
      <EncabezadoPagina titulo="Reportes" descripcion="Genera reportes con datos reales y exportalos en PDF o XLSX." />
      {error && <Alerta tipo="error" mensaje={error} cerrar={() => setError('')} />}
      <Panel titulo="Parametros del reporte">
        <div className="formulario-lineal">
          <label>Reporte<select value={tipo} onChange={(evento) => { setTipo(evento.target.value as TipoReporte); setResultado(null) }}><option value="libro-diario">Libro Diario</option><option value="cartera-creditos">Cartera de creditos</option><option value="historial-ahorros">Historial de ahorros</option><option value="resumen-aportaciones">Resumen de aportaciones</option></select></label>
          {['historial-ahorros', 'resumen-aportaciones'].includes(tipo) && <label>Socio<select value={socioId} onChange={(evento) => setSocioId(evento.target.value)}><option value="">Selecciona</option>{socios.map((socio) => <option value={socio.id} key={socio.id}>{socio.numero_socio} - {nombreCompleto(socio)}</option>)}</select></label>}
          <button className="boton-primario" onClick={() => void generar()} disabled={cargando}><Play /> {cargando ? 'Generando' : 'Generar reporte'}</button>
        </div>
      </Panel>
      <Panel titulo="Resultado">
        {!resultado ? <EstadoVacio texto="Configura y genera un reporte" /> : (
          <>
            <div className="barra-herramientas">
              <span>{filas.length} registros preparados</span>
              <div className="grupo-botones"><button className="boton-secundario" onClick={() => void exportarPdf()}><FileText /> PDF</button><button className="boton-secundario" onClick={() => void exportarXlsx()}><FileSpreadsheet /> XLSX</button><button className="boton-icono" title="Descargar reporte"><Download /></button></div>
            </div>
            <pre className="resultado-json">{JSON.stringify(resultado, null, 2)}</pre>
          </>
        )}
      </Panel>
    </>
  )
}
