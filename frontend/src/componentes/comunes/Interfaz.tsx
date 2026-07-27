import { AlertCircle, CheckCircle2, LoaderCircle, SearchX, X } from 'lucide-react'
import type { ReactNode } from 'react'

export function EncabezadoPagina({
  titulo,
  descripcion,
  acciones,
}: {
  titulo: string
  descripcion: string
  acciones?: ReactNode
}) {
  return (
    <header className="encabezado-pagina">
      <div>
        <h1>{titulo}</h1>
        <p>{descripcion}</p>
      </div>
      {acciones && <div className="acciones-pagina">{acciones}</div>}
    </header>
  )
}

export function EstadoCarga({ texto = 'Cargando informacion' }: { texto?: string }) {
  return (
    <div className="estado-contenido" role="status">
      <LoaderCircle className="girar" aria-hidden="true" />
      <span>{texto}</span>
    </div>
  )
}

export function EstadoVacio({ texto }: { texto: string }) {
  return (
    <div className="estado-contenido">
      <SearchX aria-hidden="true" />
      <span>{texto}</span>
    </div>
  )
}

export function Alerta({
  tipo,
  mensaje,
  cerrar,
}: {
  tipo: 'error' | 'exito'
  mensaje: string
  cerrar?: () => void
}) {
  return (
    <div className={`alerta alerta-${tipo}`} role={tipo === 'error' ? 'alert' : 'status'}>
      {tipo === 'error' ? <AlertCircle aria-hidden="true" /> : <CheckCircle2 aria-hidden="true" />}
      <span>{mensaje}</span>
      {cerrar && (
        <button type="button" className="boton-icono" onClick={cerrar} aria-label="Cerrar mensaje">
          <X aria-hidden="true" />
        </button>
      )}
    </div>
  )
}

export function EtiquetaEstado({ valor }: { valor: string }) {
  const normalizado = valor.toLowerCase().replaceAll('_', '-')
  return <span className={`etiqueta-estado estado-${normalizado}`}>{valor.replaceAll('_', ' ')}</span>
}

export function Panel({ children, titulo }: { children: ReactNode; titulo?: string }) {
  return (
    <section className="panel">
      {titulo && <h2>{titulo}</h2>}
      {children}
    </section>
  )
}
