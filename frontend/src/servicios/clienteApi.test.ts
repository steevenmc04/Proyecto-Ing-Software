import { beforeEach, describe, expect, it, vi } from 'vitest'
import {
  clienteApi,
  guardarToken,
  obtenerToken,
} from './clienteApi'

describe('clienteApi', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('adjunta el token y serializa solicitudes JSON', async () => {
    guardarToken('token-prueba')
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ id: 7 }), {
        status: 201,
        headers: { 'Content-Type': 'application/json' },
      }),
    )
    vi.stubGlobal('fetch', fetchMock)

    await expect(clienteApi.post<{ id: number }>('/socios', { nombres: 'Ana' }))
      .resolves.toEqual({ id: 7 })

    const [, opciones] = fetchMock.mock.calls[0]
    const encabezados = opciones.headers as Headers
    expect(encabezados.get('Authorization')).toBe('Bearer token-prueba')
    expect(encabezados.get('Content-Type')).toBe('application/json')
    expect(opciones.body).toBe('{"nombres":"Ana"}')
  })

  it('elimina una sesion vencida al recibir 401', async () => {
    guardarToken('token-vencido')
    const evento = vi.fn()
    window.addEventListener('sesion-vencida', evento)
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: 'Token invalido' }), {
          status: 401,
          headers: { 'Content-Type': 'application/json' },
        }),
      ),
    )

    await expect(clienteApi.get('/auth/me')).rejects.toMatchObject({
      estado: 401,
      message: 'Token invalido',
    })
    expect(obtenerToken()).toBeNull()
    expect(evento).toHaveBeenCalledOnce()
    window.removeEventListener('sesion-vencida', evento)
  })

  it('convierte errores de red en un mensaje controlado', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('sin red')))
    await expect(clienteApi.get('/salud')).rejects.toMatchObject({
      estado: 0,
      message: 'No se pudo conectar con el servidor',
    })
  })
})
