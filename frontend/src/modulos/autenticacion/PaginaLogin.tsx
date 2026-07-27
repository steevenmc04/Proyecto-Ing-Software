import { zodResolver } from '@hookform/resolvers/zod'
import { BadgeDollarSign, Eye, EyeOff, LoaderCircle, LockKeyhole, UserRound } from 'lucide-react'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Navigate, useNavigate } from 'react-router-dom'
import { z } from 'zod'
import { Alerta } from '../../componentes/comunes/Interfaz'
import { useAutenticacion } from '../../contextos/EstadoAutenticacion'
import { mensajeError } from '../../utilidades/errores'

const esquema = z.object({
  nombre_usuario: z.string().min(3, 'Ingresa un usuario valido'),
  contrasena: z.string().min(6, 'La contrasena debe tener al menos 6 caracteres'),
})

type FormularioLogin = z.infer<typeof esquema>

export function PaginaLogin() {
  const { usuario, iniciarSesion, mensajeSesion, limpiarMensaje } = useAutenticacion()
  const [mostrarContrasena, setMostrarContrasena] = useState(false)
  const [error, setError] = useState('')
  const navegar = useNavigate()
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormularioLogin>({
    resolver: zodResolver(esquema),
    defaultValues: { nombre_usuario: '', contrasena: '' },
  })

  if (usuario) return <Navigate to="/dashboard" replace />

  const enviar = async (datos: FormularioLogin) => {
    setError('')
    limpiarMensaje()
    try {
      await iniciarSesion(datos.nombre_usuario, datos.contrasena)
      navegar('/dashboard', { replace: true })
    } catch (excepcion) {
      setError(mensajeError(excepcion))
    }
  }

  return (
    <main className="pagina-login">
      <section className="login-identidad">
        <div className="login-marca">
          <BadgeDollarSign aria-hidden="true" />
          <span>Caja de Ahorros</span>
        </div>
        <div className="login-mensaje">
          <p className="sobrelinea">Sistema financiero cooperativo</p>
          <h1>Gestion clara para cada movimiento.</h1>
          <p>
            Administra socios, ahorros, creditos y contabilidad desde una sola
            plataforma segura.
          </p>
        </div>
        <div className="login-indicadores" aria-label="Caracteristicas principales">
          <span>Control por roles</span>
          <span>Datos en tiempo real</span>
          <span>Trazabilidad contable</span>
        </div>
      </section>

      <section className="login-acceso">
        <form className="formulario-login" onSubmit={handleSubmit(enviar)} noValidate>
          <div>
            <p className="sobrelinea">Acceso seguro</p>
            <h2>Iniciar sesion</h2>
            <p>Utiliza las credenciales academicas asignadas a tu rol.</p>
          </div>
          {(error || mensajeSesion) && (
            <Alerta tipo="error" mensaje={error || mensajeSesion} />
          )}
          <label>
            Usuario
            <span className="campo-con-icono">
              <UserRound aria-hidden="true" />
              <input
                {...register('nombre_usuario')}
                autoComplete="username"
                placeholder="Ej. admin"
                aria-invalid={Boolean(errors.nombre_usuario)}
              />
            </span>
            {errors.nombre_usuario && <small className="error-campo">{errors.nombre_usuario.message}</small>}
          </label>
          <label>
            Contrasena
            <span className="campo-con-icono">
              <LockKeyhole aria-hidden="true" />
              <input
                {...register('contrasena')}
                type={mostrarContrasena ? 'text' : 'password'}
                autoComplete="current-password"
                placeholder="Ingresa tu contrasena"
                aria-invalid={Boolean(errors.contrasena)}
              />
              <button
                type="button"
                className="boton-icono"
                onClick={() => setMostrarContrasena((valor) => !valor)}
                aria-label={mostrarContrasena ? 'Ocultar contrasena' : 'Mostrar contrasena'}
              >
                {mostrarContrasena ? <EyeOff /> : <Eye />}
              </button>
            </span>
            {errors.contrasena && <small className="error-campo">{errors.contrasena.message}</small>}
          </label>
          <button className="boton-primario boton-ancho" disabled={isSubmitting}>
            {isSubmitting && <LoaderCircle className="girar" aria-hidden="true" />}
            {isSubmitting ? 'Validando acceso' : 'Ingresar al sistema'}
          </button>
          <p className="nota-seguridad">
            Las credenciales de demostracion se encuentran en el README local.
          </p>
        </form>
      </section>
    </main>
  )
}
