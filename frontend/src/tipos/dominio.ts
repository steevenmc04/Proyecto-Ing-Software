export type Rol =
  | 'ADMINISTRADOR'
  | 'GERENTE'
  | 'CAJERO'
  | 'CONTADOR'
  | 'SOCIO'

export interface Usuario {
  id: number
  nombre_usuario: string
  nombre_completo: string
  correo: string
  rol: Rol
  activo: boolean
  fecha_creacion: string
}

export interface Socio {
  id: number
  numero_socio: string
  cedula: string
  nombres: string
  apellidos: string
  fecha_nacimiento: string
  direccion: string
  telefono: string
  correo: string
  estado: 'ACTIVO' | 'INACTIVO'
  total_aportaciones: string
  fecha_registro: string
  usuario_id?: number | null
}

export interface Cuenta {
  id: number
  numero_cuenta: string
  saldo: string
  fecha_apertura: string
  estado: 'ACTIVA' | 'BLOQUEADA' | 'SALDO_CERO' | 'CERRADA'
  socio_id: number
}

export interface Transaccion {
  id: number
  numero_comprobante: string
  tipo_transaccion: 'DEPOSITO' | 'RETIRO'
  monto: string
  fecha: string
  descripcion?: string | null
  saldo_resultante: string
  cuenta_id: number
  usuario_cajero_id?: number | null
}

export interface TipoAportacion {
  id: number
  nombre: 'ORDINARIA' | 'EXTRAORDINARIA'
  descripcion?: string | null
  activo: boolean
}

export interface Aportacion {
  id: number
  tipo_aportacion_id: number
  operacion: 'DEP' | 'RET'
  monto: string
  fecha: string
  descripcion?: string | null
  socio_id: number
  usuario_cajero_id?: number | null
}

export type EstadoCredito =
  | 'PENDIENTE'
  | 'APROBADO'
  | 'RECHAZADO'
  | 'DESEMBOLSADO'
  | 'EN_PAGO'
  | 'VENCIDO'
  | 'CANCELADO'

export interface Credito {
  id: number
  numero_credito: string
  socio_id: number
  monto_solicitado: string
  monto_aprobado?: string | null
  plazo_meses: number
  tasa_interes: string
  tipo_garantia: string
  proposito: string
  estado: EstadoCredito
  fecha_solicitud: string
  fecha_aprobacion?: string | null
  motivo_rechazo?: string | null
  gerente_aprobador_id?: number | null
  cajero_desembolso_id?: number | null
  saldo_pendiente: string
}

export interface Cuota {
  id: number
  credito_id: number
  numero_cuota: number
  fecha_vencimiento: string
  capital: string
  interes: string
  cuota_total: string
  saldo_pendiente: string
  estado: 'PENDIENTE' | 'PAGADA' | 'VENCIDA'
}

export interface Asiento {
  id: number
  fecha: string
  descripcion: string
  cuenta_debito: string
  cuenta_credito: string
  monto: string
  tipo_origen: string
  transaccion_id?: number | null
  credito_id?: number | null
  aportacion_id?: number | null
}

export interface TokenRespuesta {
  access_token: string
  token_type: string
}

export interface ErrorApi {
  estado: number
  mensaje: string
  detalle?: unknown
}
