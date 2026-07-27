import { expect, type Page, test } from '@playwright/test'

const DESTINO = '../docs/evidencias'

test.setTimeout(180_000)

async function iniciarSesion(page: Page) {
  await page.goto('/login')
  await page.getByRole('textbox', { name: 'Usuario' }).fill('admin')
  await page.getByPlaceholder('Ingresa tu contrasena').fill('Admin123')
  await page.getByRole('button', { name: 'Ingresar al sistema' }).click()
  await expect(page).toHaveURL(/\/dashboard$/, { timeout: 15_000 })
}

async function captura(page: Page, nombre: string) {
  await page.screenshot({ path: `${DESTINO}/${nombre}.png`, fullPage: true })
}

test('genera evidencias visuales reales del sistema', async ({ page }) => {
  await page.goto('/login')
  await captura(page, '01_login')

  await page.setViewportSize({ width: 390, height: 844 })
  await captura(page, '02_login_movil')
  await page.setViewportSize({ width: 1366, height: 768 })

  await iniciarSesion(page)
  await expect(page.getByText('Saldo total de ahorros')).toBeVisible()
  await captura(page, '03_dashboard')

  await page.setViewportSize({ width: 390, height: 844 })
  await captura(page, '04_dashboard_movil')
  await page.setViewportSize({ width: 1366, height: 768 })

  await page.goto('/socios')
  await expect(page.getByRole('heading', { name: 'Socios' })).toBeVisible()
  await page.getByRole('row', { name: /SOC-000001/ }).click()
  await captura(page, '05_socios')

  await page.goto('/cuentas')
  await expect(page.getByRole('heading', { name: 'Cuentas de ahorro' })).toBeVisible()
  await page.getByRole('row', { name: /CTA-000001/ }).click()
  await captura(page, '06_cuenta')

  await page.goto('/transacciones')
  await page.getByLabel('Cuenta').selectOption('1')
  await page.getByLabel('Monto').fill('25.50')
  await page.getByLabel('Descripcion').fill('Deposito de evidencia')
  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Confirmar operacion' }).click()
  await expect(page.getByText('Deposito registrado correctamente')).toBeVisible()
  await captura(page, '07_deposito')

  await page.getByRole('button', { name: 'Retiro' }).click()
  await page.getByLabel('Cuenta').selectOption('1')
  await page.getByLabel('Monto').fill('10.00')
  await page.getByLabel('Descripcion').fill('Retiro de evidencia')
  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Confirmar operacion' }).click()
  await expect(page.getByText('Retiro registrado correctamente')).toBeVisible()
  await captura(page, '08_retiro')

  await page.goto('/creditos')
  await expect(page.getByRole('heading', { name: 'Creditos' })).toBeVisible()
  await captura(page, '09_creditos')
  const creditoAprobado = page.getByRole('row', { name: /CRE-000002/ })
  await creditoAprobado.click()
  await expect(page.getByRole('heading', { name: 'Tabla de amortizacion' })).toBeVisible()
  await captura(page, '10_amortizacion')

  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Desembolsar' }).click()
  await expect(page.getByText('Operacion de credito completada correctamente')).toBeVisible()
  page.once('dialog', (dialogo) => dialogo.accept())
  await page.getByRole('button', { name: 'Pagar siguiente cuota' }).click()
  await expect(page.getByText('Operacion de credito completada correctamente')).toBeVisible()
  await captura(page, '11_pago_cuota')

  await page.goto('/contabilidad')
  await expect(page.getByRole('row', { name: /Pago cuota 1/ })).toBeVisible()
  await captura(page, '12_libro_diario')

  await page.goto('/reportes')
  await page.getByRole('button', { name: 'Generar reporte' }).click()
  await expect(page.getByText(/registros preparados/)).toBeVisible()
  await captura(page, '13_reportes')

  await page.goto('http://127.0.0.1:8000/docs')
  await expect(page.locator('.swagger-ui')).toBeVisible()
  await captura(page, '14_swagger')
})
