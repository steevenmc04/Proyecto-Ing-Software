import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'
import { AutenticacionContexto, type AutenticacionValor } from '../contextos/EstadoAutenticacion'
import type { Usuario } from '../tipos/dominio'
import { RutaProtegida } from './RutaProtegida'

const administrador: Usuario = {
  id: 1,
  nombre_usuario: 'admin',
  nombre_completo: 'Administrador General',
  correo: 'admin@example.com',
  rol: 'ADMINISTRADOR',
  activo: true,
  fecha_creacion: '2026-01-01T00:00:00',
}

function valor(usuario: Usuario | null, cargando = false): AutenticacionValor {
  return {
    usuario,
    cargando,
    mensajeSesion: '',
    iniciarSesion: vi.fn(),
    cerrarSesion: vi.fn(),
    limpiarMensaje: vi.fn(),
  }
}

function renderizarRuta(estado: AutenticacionValor, roles?: Usuario['rol'][]) {
  render(
    <AutenticacionContexto.Provider value={estado}>
      <MemoryRouter initialEntries={['/privado']}>
        <Routes>
          <Route element={<RutaProtegida roles={roles} />}>
            <Route path="/privado" element={<h1>Contenido privado</h1>} />
          </Route>
          <Route path="/login" element={<h1>Acceso</h1>} />
          <Route path="/acceso-denegado" element={<h1>Acceso denegado</h1>} />
        </Routes>
      </MemoryRouter>
    </AutenticacionContexto.Provider>,
  )
}

describe('RutaProtegida', () => {
  it('envia al login cuando no existe una sesion', () => {
    renderizarRuta(valor(null))
    expect(screen.getByRole('heading', { name: 'Acceso' })).toBeInTheDocument()
  })

  it('impide acceder a un rol no autorizado', () => {
    renderizarRuta(valor({ ...administrador, rol: 'SOCIO' }), ['ADMINISTRADOR'])
    expect(screen.getByRole('heading', { name: 'Acceso denegado' })).toBeInTheDocument()
  })

  it('permite acceder a un rol autorizado', () => {
    renderizarRuta(valor(administrador), ['ADMINISTRADOR'])
    expect(screen.getByRole('heading', { name: 'Contenido privado' })).toBeInTheDocument()
  })
})
