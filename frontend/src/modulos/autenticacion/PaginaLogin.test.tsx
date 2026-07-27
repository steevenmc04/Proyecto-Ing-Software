import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'
import { AutenticacionContexto, type AutenticacionValor } from '../../contextos/EstadoAutenticacion'
import { PaginaLogin } from './PaginaLogin'

const valorBase: AutenticacionValor = {
  usuario: null,
  cargando: false,
  mensajeSesion: '',
  iniciarSesion: vi.fn(),
  cerrarSesion: vi.fn(),
  limpiarMensaje: vi.fn(),
}

function renderizarLogin(valor: AutenticacionValor = valorBase) {
  return render(
    <AutenticacionContexto.Provider value={valor}>
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<PaginaLogin />} />
          <Route path="/dashboard" element={<h1>Panel principal</h1>} />
        </Routes>
      </MemoryRouter>
    </AutenticacionContexto.Provider>,
  )
}

describe('PaginaLogin', () => {
  it('muestra validaciones antes de enviar datos incompletos', async () => {
    const iniciarSesion = vi.fn()
    renderizarLogin({ ...valorBase, iniciarSesion })

    await userEvent.click(screen.getByRole('button', { name: 'Ingresar al sistema' }))

    expect(await screen.findByText('Ingresa un usuario valido')).toBeInTheDocument()
    expect(screen.getByText('La contrasena debe tener al menos 6 caracteres')).toBeInTheDocument()
    expect(iniciarSesion).not.toHaveBeenCalled()
  })

  it('inicia sesion y navega al panel con credenciales validas', async () => {
    const iniciarSesion = vi.fn().mockResolvedValue(undefined)
    renderizarLogin({ ...valorBase, iniciarSesion })

    await userEvent.type(screen.getByLabelText('Usuario'), 'admin')
    await userEvent.type(screen.getByLabelText('Contrasena'), 'Admin123')
    await userEvent.click(screen.getByRole('button', { name: 'Ingresar al sistema' }))

    expect(await screen.findByRole('heading', { name: 'Panel principal' })).toBeInTheDocument()
    expect(iniciarSesion).toHaveBeenCalledWith('admin', 'Admin123')
  })
})
