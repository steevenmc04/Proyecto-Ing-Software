# Evidencias

Estas imagenes fueron capturadas contra la aplicacion local real mediante
Playwright. La base E2E se crea de forma aislada.

| Archivo | Evidencia |
|---|---|
| `01_login.png` | Inicio de sesion |
| `02_login_movil.png` | Login en movil |
| `03_dashboard.png` | Panel principal |
| `04_dashboard_movil.png` | Panel en movil |
| `05_socios.png` | Gestion de socios |
| `06_cuenta.png` | Cuenta de ahorro |
| `07_deposito.png` | Deposito |
| `08_retiro.png` | Retiro |
| `09_creditos.png` | Gestion de creditos |
| `10_amortizacion.png` | Tabla de amortizacion |
| `11_pago_cuota.png` | Pago de cuota |
| `12_libro_diario.png` | Libro Diario |
| `13_reportes.png` | Reportes |
| `14_swagger.png` | Swagger |
| `15_pruebas.png` | Ruff, Pytest, Vitest y los 12 flujos E2E |
| `16_cobertura.png` | Cobertura backend de 83.38% |
| `17_build_final.png` | Build Vite de produccion |

Las tres ultimas imagenes se regeneran con:

```powershell
cd frontend
npm run evidencias:calidad
```
