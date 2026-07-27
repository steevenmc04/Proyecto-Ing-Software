# Plan de pruebas

## Objetivo

Verificar reglas de negocio, seguridad, integracion entre capas, experiencia
React y los flujos financieros completos sin depender de servicios remotos.

## Entorno

- Backend: Python 3.11 soportado; SQLite aislado para pruebas.
- Frontend: Node.js 20 o superior, Chromium de Playwright.
- CI: Ubuntu, Python 3.11 y Node.js 24.
- Cobertura minima exigida: 70% del paquete `app`.

## Niveles

| Nivel | Alcance | Ubicacion | Comando |
|---|---|---|---|
| Unitario backend | Validaciones, estados, roles y calculos | `tests/unit` | `pytest -q tests/unit` |
| Integracion backend | API externa y flujos financieros | `tests/integration` | `pytest -q tests/integration` |
| Unitario frontend | Login, rutas y cliente HTTP | `frontend/src/**/*.test.tsx` | `npm test` |
| E2E | Navegador, API y base aislada | `frontend/tests-e2e` | `npm run test:e2e` |
| Estatico | Python y TypeScript | Ruff y ESLint | `ruff check ...`; `npm run lint` |
| Produccion | Tipos y empaquetado | Vite | `npm run build` |

## Doce flujos E2E

1. Login valido y apertura del panel.
2. Registro de un socio.
3. Apertura de una cuenta.
4. Deposito y actualizacion del saldo.
5. Retiro sin sobregiro.
6. Consulta del historial de movimientos.
7. Solicitud de credito.
8. Aprobacion por un rol autorizado.
9. Generacion de tabla de amortizacion.
10. Desembolso de credito aprobado.
11. Pago de la siguiente cuota.
12. Verificacion del asiento en Libro Diario.

La base `e2e_caja_ahorros.db` se crea nuevamente con
`scripts/preparar_e2e.py`; no modifica la base local del usuario.

## Casos negativos prioritarios

- Credenciales invalidas y JWT ausente.
- Rol sin permiso y socio consultando recursos ajenos.
- Cedula, usuario, correo o numero de cuenta duplicado.
- Monto cero o negativo.
- Retiro superior al saldo.
- Operacion en cuenta bloqueada o cerrada.
- Cierre con saldo diferente de cero.
- Credito no aprobado que intenta desembolsarse.
- API externa sin `X-API-KEY`, con clave invalida o cuenta no asociada.
- Datos incompletos que deben producir error 422.

## Criterios de salida

- Ruff y ESLint sin errores.
- Todas las pruebas backend y frontend aprobadas.
- Cobertura backend mayor o igual a 70%.
- Los doce flujos E2E aprobados.
- Build Vite aprobado.
- Swagger, ReDoc, salud y SPA responden por HTTP.
- No quedan procesos de prueba ni bases E2E versionadas.

## Ejecucion

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verificar.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verificar.ps1 -IncluirE2E
```

Los resultados consolidados y sus capturas se guardan en
`docs/evidencias/`.

