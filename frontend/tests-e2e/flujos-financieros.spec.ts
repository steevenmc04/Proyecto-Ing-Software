import { expect, type APIRequestContext, type Page, test } from '@playwright/test'

const API = 'http://127.0.0.1:8000/api/v1'
let secuencia = 0

async function iniciarSesion(page: Page) {
  await page.goto('/login')
  await page.getByRole('textbox', { name: 'Usuario' }).fill('admin')
  await page.getByPlaceholder('Ingresa tu contrasena').fill('Admin123')
  await page.getByRole('button', { name: 'Ingresar al sistema' }).click()
  await expect(page).toHaveURL(/\/dashboard$/, { timeout: 15_000 })
}

async function tokenAdministrador(request: APIRequestContext): Promise<string> {
  const respuesta = await request.post(`${API}/auth/login`, {
    data: { nombre_usuario: 'admin', contrasena: 'Admin123' },
  })
  expect(respuesta.ok()).toBeTruthy()
  return (await respuesta.json()).access_token
}

async function crearSocio(request: APIRequestContext) {
  secuencia += 1
  const token = await tokenAdministrador(request)
  const sufijo = String(Date.now() + secuencia).slice(-8)
  const datos = {
    cedula: `17${sufijo}`,
    nombres: 'Maria Elena',
    apellidos: `Prueba ${sufijo}`,
    fecha_nacimiento: '1992-06-15',
    direccion: 'Calle de Integracion 123',
    telefono: `09${sufijo}`,
    correo: `maria.${sufijo}@example.com`,
    usuario_registro_id: 1,
  }
  const respuesta = await request.post(`${API}/socios`, {
    data: datos,
    headers: { Authorization: `Bearer ${token}` },
  })
  expect(respuesta.ok()).toBeTruthy()
  return { token, datos, socio: await respuesta.json() }
}

async function crearCredito(request: APIRequestContext, estado: 'PENDIENTE' | 'APROBADO' | 'DESEMBOLSADO') {
  const { token, socio } = await crearSocio(request)
  const solicitud = await request.post(`${API}/creditos/solicitar`, {
    data: {
      socio_id: socio.id,
      monto_solicitado: '1250.00',
      plazo_meses: 6,
      tasa_interes: '11.50',
      tipo_garantia: 'Garante personal',
      proposito: `Prueba E2E ${Date.now()}`,
    },
    headers: { Authorization: `Bearer ${token}` },
  })
  expect(solicitud.ok()).toBeTruthy()
  const credito = await solicitud.json()

  if (estado === 'APROBADO' || estado === 'DESEMBOLSADO') {
    const aprobacion = await request.patch(`${API}/creditos/${credito.id}/aprobar`, {
      data: { gerente_aprobador_id: 1 },
      headers: { Authorization: `Bearer ${token}` },
    })
    expect(aprobacion.ok()).toBeTruthy()
  }
  if (estado === 'DESEMBOLSADO') {
    const desembolso = await request.patch(`${API}/creditos/${credito.id}/desembolsar`, {
      data: { cajero_desembolso_id: 1 },
      headers: { Authorization: `Bearer ${token}` },
    })
    expect(desembolso.ok()).toBeTruthy()
  }
  return credito
}

test.beforeEach(async ({ page }) => {
  await iniciarSesion(page)
})

test('01 inicia sesion y muestra indicadores reales', async ({ page }) => {
  await expect(page.getByRole('heading', { name: /Buenos dias, Administrador/ })).toBeVisible()
  await expect(page.getByText('Saldo total de ahorros')).toBeVisible()
})

test('02 registra un socio desde el formulario', async ({ page }) => {
  const sufijo = String(Date.now()).slice(-8)
  await page.goto('/socios')
  await page.getByRole('button', { name: 'Registrar socio' }).click()
  await page.getByLabel('Cedula').fill(`18${sufijo}`)
  await page.getByLabel('Nombres').fill('Pedro Luis')
  await page.getByLabel('Apellidos').fill(`E2E ${sufijo}`)
  await page.getByLabel('Fecha de nacimiento').fill('1990-03-20')
  await page.getByLabel('Direccion').fill('Avenida de Pruebas 456')
  await page.getByLabel('Telefono').fill(`09${sufijo}`)
  await page.getByLabel('Correo').fill(`pedro.${sufijo}@example.com`)
  await page.getByRole('button', { name: 'Guardar socio' }).click()
  await expect(page.getByText('Socio registrado correctamente')).toBeVisible()
})

test('03 crea una cuenta de ahorro para un socio activo', async ({ page, request }) => {
  const { socio } = await crearSocio(request)
  await page.goto('/cuentas')
  await page.getByLabel('Socio').selectOption(String(socio.id))
  await page.getByRole('button', { name: 'Crear cuenta' }).click()
  await expect(page.getByText('Cuenta creada con saldo inicial cero')).toBeVisible()
})

test('04 registra un deposito y genera comprobante', async ({ page }) => {
  await page.goto('/transacciones')
  await page.getByLabel('Cuenta').selectOption('1')
  await page.getByLabel('Monto').fill('25.50')
  await page.getByLabel('Descripcion').fill('Deposito automatizado E2E')
  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Confirmar operacion' }).click()
  await expect(page.getByText('Deposito registrado correctamente')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Comprobante generado' })).toBeVisible()
})

test('05 registra un retiro validando el saldo', async ({ page }) => {
  await page.goto('/transacciones')
  await page.getByRole('button', { name: 'Retiro' }).click()
  await page.getByLabel('Cuenta').selectOption('1')
  await page.getByLabel('Monto').fill('10.00')
  await page.getByLabel('Descripcion').fill('Retiro automatizado E2E')
  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Confirmar operacion' }).click()
  await expect(page.getByText('Retiro registrado correctamente')).toBeVisible()
})

test('06 consulta y filtra el historial de movimientos', async ({ page }) => {
  await page.goto('/transacciones')
  await page.getByPlaceholder('Comprobante, tipo o cuenta').fill('Deposito inicial')
  await expect(page.getByRole('row', { name: /Deposito inicial/ })).toBeVisible()
})

test('07 solicita un credito para un socio activo', async ({ page, request }) => {
  const { socio } = await crearSocio(request)
  await page.goto('/creditos')
  await page.getByRole('button', { name: 'Solicitar credito' }).click()
  await page.getByLabel('Socio').selectOption(String(socio.id))
  await page.getByLabel('Monto solicitado').fill('900')
  await page.getByLabel('Plazo en meses').fill('6')
  await page.getByLabel('Tasa anual (%)').fill('10')
  await page.getByLabel('Tipo de garantia').fill('Garante solidario')
  await page.getByLabel('Proposito').fill('Compra de herramientas')
  await page.getByRole('button', { name: 'Enviar solicitud' }).click()
  await expect(page.getByText('Solicitud de credito registrada')).toBeVisible()
})

test('08 aprueba un credito pendiente', async ({ page, request }) => {
  const credito = await crearCredito(request, 'PENDIENTE')
  await page.goto('/creditos')
  await page.getByRole('row', { name: new RegExp(credito.numero_credito) }).click()
  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Aprobar' }).click()
  await expect(page.getByText('Operacion de credito completada correctamente')).toBeVisible()
})

test('09 muestra la tabla de amortizacion francesa', async ({ page, request }) => {
  const credito = await crearCredito(request, 'APROBADO')
  await page.goto('/creditos')
  await page.getByRole('row', { name: new RegExp(credito.numero_credito) }).click()
  await expect(page.getByRole('heading', { name: 'Tabla de amortizacion' })).toBeVisible()
  await expect(page.getByRole('row', { name: /^#1 / })).toBeVisible()
})

test('10 desembolsa un credito aprobado', async ({ page, request }) => {
  const credito = await crearCredito(request, 'APROBADO')
  await page.goto('/creditos')
  await page.getByRole('row', { name: new RegExp(credito.numero_credito) }).click()
  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Desembolsar' }).click()
  await expect(page.getByText('Operacion de credito completada correctamente')).toBeVisible()
})

test('11 paga la siguiente cuota de un credito desembolsado', async ({ page, request }) => {
  const credito = await crearCredito(request, 'DESEMBOLSADO')
  await page.goto('/creditos')
  await page.getByRole('row', { name: new RegExp(credito.numero_credito) }).click()
  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Pagar siguiente cuota' }).click()
  await expect(page.getByText('Operacion de credito completada correctamente')).toBeVisible()
})

test('12 consulta el Libro Diario con trazabilidad', async ({ page }) => {
  await page.goto('/contabilidad')
  await expect(page.getByRole('heading', { name: 'Libro Diario' })).toBeVisible()
  await expect(page.getByRole('row', { name: /Deposito COMP-/ }).first()).toBeVisible()
})
