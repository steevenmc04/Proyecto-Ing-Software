import { Navigate, Outlet } from 'react-router-dom'
import { EstadoCarga } from '../componentes/comunes/Interfaz'
import { useAutenticacion } from '../contextos/EstadoAutenticacion'
import type { Rol } from '../tipos/dominio'

export function RutaProtegida({ roles }: { roles?: Rol[] }) {
  const { usuario, cargando } = useAutenticacion()
  if (cargando) return <EstadoCarga texto="Validando sesion" />
  if (!usuario) return <Navigate to="/login" replace />
  if (roles && !roles.includes(usuario.rol)) return <Navigate to="/acceso-denegado" replace />
  return <Outlet />
}
