import type { ErrorApi } from '../tipos/dominio'

const URL_BASE = (import.meta.env.VITE_API_URL || '/api/v1').replace(/\/$/, '')
const CLAVE_TOKEN = 'caja_ahorros_token'

export class ExcepcionApi extends Error {
  estado: number
  detalle?: unknown

  constructor(error: ErrorApi) {
    super(error.mensaje)
    this.name = 'ExcepcionApi'
    this.estado = error.estado
    this.detalle = error.detalle
  }
}

export function obtenerToken(): string | null {
  return sessionStorage.getItem(CLAVE_TOKEN)
}

export function guardarToken(token: string): void {
  sessionStorage.setItem(CLAVE_TOKEN, token)
}

export function eliminarToken(): void {
  sessionStorage.removeItem(CLAVE_TOKEN)
}

function normalizarDetalle(detalle: unknown): string {
  if (typeof detalle === 'string') return detalle
  if (Array.isArray(detalle)) {
    return detalle
      .map((item) => {
        if (typeof item === 'object' && item && 'msg' in item) return String(item.msg)
        return String(item)
      })
      .join('. ')
  }
  return 'No fue posible completar la solicitud'
}

async function peticion<T>(
  ruta: string,
  opciones: RequestInit = {},
  signal?: AbortSignal,
): Promise<T> {
  const token = obtenerToken()
  const encabezados = new Headers(opciones.headers)
  if (!encabezados.has('Content-Type') && opciones.body) {
    encabezados.set('Content-Type', 'application/json')
  }
  if (token) encabezados.set('Authorization', `Bearer ${token}`)

  let respuesta: Response
  try {
    respuesta = await fetch(`${URL_BASE}${ruta}`, {
      ...opciones,
      headers: encabezados,
      signal,
    })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    throw new ExcepcionApi({
      estado: 0,
      mensaje: 'No se pudo conectar con el servidor',
      detalle: error,
    })
  }

  const contenido = respuesta.status === 204 ? null : await respuesta.json().catch(() => null)
  if (!respuesta.ok) {
    if (respuesta.status === 401 && token) {
      eliminarToken()
      window.dispatchEvent(new CustomEvent('sesion-vencida'))
    }
    throw new ExcepcionApi({
      estado: respuesta.status,
      mensaje: normalizarDetalle(contenido?.detail),
      detalle: contenido,
    })
  }
  return contenido as T
}

export const clienteApi = {
  get: <T>(ruta: string, signal?: AbortSignal) => peticion<T>(ruta, {}, signal),
  post: <T>(ruta: string, datos?: unknown) =>
    peticion<T>(ruta, {
      method: 'POST',
      body: datos === undefined ? undefined : JSON.stringify(datos),
    }),
  put: <T>(ruta: string, datos: unknown) =>
    peticion<T>(ruta, { method: 'PUT', body: JSON.stringify(datos) }),
  patch: <T>(ruta: string, datos?: unknown) =>
    peticion<T>(ruta, {
      method: 'PATCH',
      body: datos === undefined ? undefined : JSON.stringify(datos),
    }),
}
