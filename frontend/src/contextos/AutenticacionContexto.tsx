import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { clienteApi, eliminarToken, guardarToken, obtenerToken } from '../servicios/clienteApi'
import type { TokenRespuesta, Usuario } from '../tipos/dominio'
import { AutenticacionContexto } from './EstadoAutenticacion'

export function ProveedorAutenticacion({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null)
  const [cargando, setCargando] = useState(true)
  const [mensajeSesion, setMensajeSesion] = useState('')

  const cerrarSesion = useCallback(() => {
    eliminarToken()
    setUsuario(null)
  }, [])

  const recuperarUsuario = useCallback(async () => {
    if (!obtenerToken()) {
      setCargando(false)
      return
    }
    try {
      setUsuario(await clienteApi.get<Usuario>('/auth/me'))
    } catch {
      cerrarSesion()
    } finally {
      setCargando(false)
    }
  }, [cerrarSesion])

  useEffect(() => {
    const temporizador = window.setTimeout(() => void recuperarUsuario(), 0)
    return () => window.clearTimeout(temporizador)
  }, [recuperarUsuario])

  useEffect(() => {
    const sesionVencida = () => {
      cerrarSesion()
      setMensajeSesion('Tu sesion vencio. Ingresa nuevamente.')
    }
    window.addEventListener('sesion-vencida', sesionVencida)
    return () => window.removeEventListener('sesion-vencida', sesionVencida)
  }, [cerrarSesion])

  const iniciarSesion = async (nombreUsuario: string, contrasena: string) => {
    const token = await clienteApi.post<TokenRespuesta>('/auth/login', {
      nombre_usuario: nombreUsuario,
      contrasena,
    })
    guardarToken(token.access_token)
    setUsuario(await clienteApi.get<Usuario>('/auth/me'))
    setMensajeSesion('')
  }

  const valor = useMemo(
    () => ({
      usuario,
      cargando,
      mensajeSesion,
      iniciarSesion,
      cerrarSesion,
      limpiarMensaje: () => setMensajeSesion(''),
    }),
    [usuario, cargando, mensajeSesion, cerrarSesion],
  )

  return <AutenticacionContexto.Provider value={valor}>{children}</AutenticacionContexto.Provider>
}
