import {
  BadgeDollarSign,
  BookOpen,
  Building2,
  ChevronRight,
  CircleDollarSign,
  CreditCard,
  FileBarChart,
  HandCoins,
  LayoutDashboard,
  LogOut,
  Menu,
  Users,
  WalletCards,
  X,
} from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { useAutenticacion } from '../../contextos/EstadoAutenticacion'
import type { Rol } from '../../tipos/dominio'

const opciones = [
  { ruta: '/dashboard', etiqueta: 'Panel general', icono: LayoutDashboard, roles: null },
  { ruta: '/usuarios', etiqueta: 'Usuarios', icono: Users, roles: ['ADMINISTRADOR'] },
  {
    ruta: '/socios',
    etiqueta: 'Socios',
    icono: Building2,
    roles: ['ADMINISTRADOR', 'GERENTE', 'CAJERO', 'CONTADOR'],
  },
  { ruta: '/cuentas', etiqueta: 'Cuentas', icono: WalletCards, roles: null },
  { ruta: '/transacciones', etiqueta: 'Transacciones', icono: CircleDollarSign, roles: null },
  {
    ruta: '/aportaciones',
    etiqueta: 'Aportaciones',
    icono: HandCoins,
    roles: ['ADMINISTRADOR', 'GERENTE', 'CAJERO', 'CONTADOR'],
  },
  { ruta: '/creditos', etiqueta: 'Creditos', icono: CreditCard, roles: null },
  {
    ruta: '/contabilidad',
    etiqueta: 'Libro Diario',
    icono: BookOpen,
    roles: ['ADMINISTRADOR', 'GERENTE', 'CONTADOR'],
  },
  {
    ruta: '/reportes',
    etiqueta: 'Reportes',
    icono: FileBarChart,
    roles: ['ADMINISTRADOR', 'GERENTE', 'CAJERO', 'CONTADOR'],
  },
] as const

function puedeVer(roles: readonly string[] | null, rol: Rol): boolean {
  return !roles || roles.includes(rol)
}

export function LayoutPrincipal() {
  const { usuario, cerrarSesion } = useAutenticacion()
  const [menuAbierto, setMenuAbierto] = useState(false)
  const ubicacion = useLocation()

  if (!usuario) return null
  const opcionActual = opciones.find((opcion) => ubicacion.pathname.startsWith(opcion.ruta))

  return (
    <div className="aplicacion">
      <aside className={`barra-lateral ${menuAbierto ? 'barra-visible' : ''}`}>
        <div className="marca">
          <span className="marca-icono" aria-hidden="true">
            <BadgeDollarSign />
          </span>
          <div>
            <strong>Caja de Ahorros</strong>
            <small>Gestion financiera</small>
          </div>
          <button
            type="button"
            className="boton-icono cerrar-menu"
            onClick={() => setMenuAbierto(false)}
            aria-label="Cerrar menu"
          >
            <X />
          </button>
        </div>
        <nav aria-label="Navegacion principal">
          {opciones
            .filter((opcion) => puedeVer(opcion.roles, usuario.rol))
            .map((opcion) => {
              const Icono = opcion.icono
              return (
                <NavLink
                  key={opcion.ruta}
                  to={opcion.ruta}
                  onClick={() => setMenuAbierto(false)}
                  className={({ isActive }) => (isActive ? 'enlace-activo' : '')}
                >
                  <Icono aria-hidden="true" />
                  <span>{opcion.etiqueta}</span>
                </NavLink>
              )
            })}
        </nav>
        <div className="perfil-lateral">
          <span className="avatar">{usuario.nombre_completo.charAt(0).toUpperCase()}</span>
          <div>
            <strong>{usuario.nombre_completo}</strong>
            <small>{usuario.rol}</small>
          </div>
        </div>
      </aside>

      <div className="contenido-aplicacion">
        <header className="barra-superior">
          <button
            type="button"
            className="boton-icono abrir-menu"
            onClick={() => setMenuAbierto(true)}
            aria-label="Abrir menu"
          >
            <Menu />
          </button>
          <div className="breadcrumb" aria-label="Ruta actual">
            <span>Inicio</span>
            <ChevronRight aria-hidden="true" />
            <strong>{opcionActual?.etiqueta ?? 'Sistema'}</strong>
          </div>
          <button type="button" className="boton-secundario" onClick={cerrarSesion}>
            <LogOut aria-hidden="true" />
            Cerrar sesion
          </button>
        </header>
        <main>
          <Outlet />
        </main>
      </div>
      {menuAbierto && (
        <button
          type="button"
          className="velo-menu"
          onClick={() => setMenuAbierto(false)}
          aria-label="Cerrar menu"
        />
      )}
    </div>
  )
}
