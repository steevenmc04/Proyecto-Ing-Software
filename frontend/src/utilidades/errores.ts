import { ExcepcionApi } from '../servicios/clienteApi'

export function mensajeError(error: unknown): string {
  if (error instanceof ExcepcionApi) return error.message
  if (error instanceof Error) return error.message
  return 'Ocurrio un error inesperado'
}
