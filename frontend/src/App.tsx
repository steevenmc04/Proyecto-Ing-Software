import { Ban, CircleHelp, Home } from 'lucide-react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { LayoutPrincipal } from './componentes/navegacion/LayoutPrincipal'
import { PaginaLogin } from './modulos/autenticacion/PaginaLogin'
import { PaginaAportaciones } from './modulos/aportaciones/PaginaAportaciones'
import { PaginaContabilidad } from './modulos/contabilidad/PaginaContabilidad'
import { PaginaCreditos } from './modulos/creditos/PaginaCreditos'
import { PaginaCuentas } from './modulos/cuentas/PaginaCuentas'
import { PaginaDashboard } from './modulos/inicio/PaginaDashboard'
import { PaginaReportes } from './modulos/reportes/PaginaReportes'
import { PaginaSocios } from './modulos/socios/PaginaSocios'
import { PaginaTransacciones } from './modulos/transacciones/PaginaTransacciones'
import { PaginaUsuarios } from './modulos/usuarios/PaginaUsuarios'
import { RutaProtegida } from './rutas/RutaProtegida'

function PaginaEstado({ denegado = false }: { denegado?: boolean }) {
  return (
    <main className="pagina-estado">
      {denegado ? <Ban aria-hidden="true" /> : <CircleHelp aria-hidden="true" />}
      <h1>{denegado ? 'Acceso denegado' : 'Pagina no encontrada'}</h1>
      <p>
        {denegado
          ? 'Tu rol no tiene permisos para consultar este modulo.'
          : 'La direccion solicitada no existe dentro del sistema.'}
      </p>
      <a className="boton-primario" href="/dashboard"><Home /> Volver al panel</a>
    </main>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<PaginaLogin />} />
      <Route element={<RutaProtegida />}>
        <Route element={<LayoutPrincipal />}>
          <Route path="/dashboard" element={<PaginaDashboard />} />
          <Route element={<RutaProtegida roles={['ADMINISTRADOR']} />}>
            <Route path="/usuarios" element={<PaginaUsuarios />} />
          </Route>
          <Route element={<RutaProtegida roles={['ADMINISTRADOR', 'GERENTE', 'CAJERO', 'CONTADOR']} />}>
            <Route path="/socios" element={<PaginaSocios />} />
            <Route path="/aportaciones" element={<PaginaAportaciones />} />
            <Route path="/reportes" element={<PaginaReportes />} />
          </Route>
          <Route path="/cuentas" element={<PaginaCuentas />} />
          <Route path="/transacciones" element={<PaginaTransacciones />} />
          <Route path="/creditos" element={<PaginaCreditos />} />
          <Route element={<RutaProtegida roles={['ADMINISTRADOR', 'GERENTE', 'CONTADOR']} />}>
            <Route path="/contabilidad" element={<PaginaContabilidad />} />
          </Route>
          <Route path="/acceso-denegado" element={<PaginaEstado denegado />} />
        </Route>
      </Route>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<PaginaEstado />} />
    </Routes>
  )
}

export default App
