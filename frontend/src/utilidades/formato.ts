export const formatoMoneda = new Intl.NumberFormat('es-EC', {
  style: 'currency',
  currency: 'USD',
})

export const formatoFecha = new Intl.DateTimeFormat('es-EC', {
  dateStyle: 'medium',
})

export function moneda(valor: string | number | null | undefined): string {
  return formatoMoneda.format(Number(valor ?? 0))
}

export function fecha(valor: string | null | undefined): string {
  if (!valor) return 'Sin fecha'
  return formatoFecha.format(new Date(valor))
}

export function nombreCompleto(socio: { nombres: string; apellidos: string }): string {
  return `${socio.nombres} ${socio.apellidos}`
}
