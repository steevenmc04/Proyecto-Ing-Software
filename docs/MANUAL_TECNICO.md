# Manual tecnico

## Componentes

- `app/`: API FastAPI por capas.
- `frontend/`: SPA React, Vite y TypeScript.
- `tests/`: pruebas unitarias e integracion backend.
- `frontend/tests-e2e/`: flujos Playwright.
- `scripts/`: instalacion, ejecucion, contrato y verificacion.
- `docs/`: arquitectura, manuales, evidencias e informe.

El flujo backend es:

```text
Ruta -> Controlador -> Servicio -> Repositorio -> Modelo -> Base de datos
```

## Instalacion reproducible

```powershell
git clone https://github.com/steevenmc04/Proyecto-Ing-Software
cd Proyecto-Ing-Software
powershell -ExecutionPolicy Bypass -File .\scripts\instalar.ps1
Copy-Item .env.example .env
Copy-Item frontend\.env.example frontend\.env
python seed.py
```

## Configuracion

Backend: `DATABASE_URL`, `CLAVE_JWT`, `API_KEY_EXTERNA`,
`MINUTOS_EXPIRACION_JWT` y `ORIGENES_CORS`. Frontend: `VITE_API_URL`. Los
archivos `.env` no se versionan.

SQLite es el modo local. Para MySQL Workbench, ejecute
`database_mysql.sql` y use una URL `mysql+pymysql://` en `DATABASE_URL`.

## Ejecucion

```powershell
# Terminal 1
powershell -ExecutionPolicy Bypass -File .\scripts\iniciar-backend.ps1

# Terminal 2
powershell -ExecutionPolicy Bypass -File .\scripts\iniciar-frontend.ps1
```

Servicios: frontend `5173`, API `8000`, Swagger `/docs`, ReDoc `/redoc`,
OpenAPI `/openapi.json` y salud `/api/v1/salud`.

## Seguridad

Las contrasenas se hashean con BCrypt. El login entrega JWT con expiracion.
`app/dependencias.py` valida usuario activo y rol en cada ruta. Los endpoints
`mis-*` filtran por el socio asociado. La integracion externa usa
`X-API-KEY`, nunca el JWT ni una clave incluida en React. CORS se limita por
entorno.

## Integridad financiera

Los montos se procesan con `Decimal` y columnas `Numeric`. Servicios de
deposito, retiro, aportacion, desembolso y pago crean los cambios relacionados
antes de `confirmar_transaccion()`. Una excepcion produce `rollback`.

Los historicos financieros no se eliminan fisicamente. Las cuentas y socios
utilizan estados. La amortizacion usa el metodo frances y ajusta el redondeo.

## Base de datos

SQLAlchemy ejecuta `create_all` y migraciones ligeras compatibles con la
entrega. No se incorpora Alembic; antes de una evolucion productiva se debe
introducir un historial de migraciones versionado.

## Calidad

```powershell
ruff check app tests seed.py scripts
pytest -q
cd frontend
npm run lint
npm test
npm run build
npm run test:e2e
```

`scripts/verificar.ps1` agrupa estos pasos. GitHub Actions repite lint, pruebas,
cobertura y build en Python 3.11 y Node.js 24.

## Actualizar el contrato

```powershell
python scripts/generar_contrato_api.py
```

El script obtiene `app.openapi()` y genera las 58 operaciones documentadas en
`docs/CONTRATO_API.md`.

## Produccion

Compile `frontend/dist`, configure secretos en el proveedor, limite CORS al
dominio real y ejecute Uvicorn tras un proxy HTTPS. FastAPI sirve la SPA
compilada cuando `frontend/dist` existe. El repositorio esta preparado para
despliegue, pero no declara una URL remota.

