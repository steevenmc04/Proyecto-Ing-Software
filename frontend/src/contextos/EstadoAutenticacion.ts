import { createContext, useContext } from 'react'
import type { Usuario } from '../tipos/dominio'

export interface AutenticacionValor {
  usuario: Usuario | null
  cargando: boolean
  mensajeSesion: string
  iniciarSesion: (nombreUsuario: string, contrasena: string) => Promise<void>
  cerrarSesion: () => void
  limpiarMensaje: () => void
}

export const AutenticacionContexto = createContext<AutenticacionValor | null>(null)

export function useAutenticacion(): AutenticacionValor {
  const contexto = useContext(AutenticacionContexto)
  if (!contexto) throw new Error('AutenticacionContexto no esta disponible')
  return contexto
}
