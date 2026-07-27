# AGENTS.md

## Objetivo

Mantener y completar el Sistema de Gestion de Caja de Ahorros para una entrega
universitaria reproducible. El backend administra socios, cuentas, movimientos,
aportaciones, creditos, amortizacion, contabilidad y reportes.

## Arquitectura

```text
Ruta -> Controlador -> Servicio -> Repositorio -> Modelo -> Base de datos
```

No se deben colocar reglas financieras en las rutas ni acceso directo a la base
de datos desde la interfaz.

## Estructura Actual

- `app`: backend FastAPI.
- `tests`: pruebas backend.
- `frontend`: frontend React cuando sea creado.
- `docs`: documentacion y evidencias.
- `scripts`: automatizacion PowerShell.
- `seed.py`: datos academicos idempotentes.

## Tecnologias

- Python, FastAPI, SQLAlchemy, Pydantic y pytest.
- SQLite local y MySQL mediante `DATABASE_URL`.
- React, Vite y TypeScript para el frontend final.

## Backend

Instalacion:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Ejecucion:

```powershell
python seed.py
python -m uvicorn app.main:app --reload
```

Pruebas y cobertura:

```powershell
pytest -q
coverage report
```

## Frontend

Instalacion y ejecucion:

```powershell
cd frontend
npm ci
npm run dev
```

Calidad:

```powershell
npm run lint
npm test
npm run build
npm run test:e2e
```

La URL se configura con `VITE_API_URL`. El cliente HTTP centralizado esta en
`frontend/src/servicios/clienteApi.ts`.

## Convenciones

- Dominio, mensajes y documentacion en espanol.
- Dinero con `Decimal` en backend.
- Tipos explicitos en TypeScript.
- Una responsabilidad principal por modulo.
- Validaciones financieras en backend y frontend.
- No usar `TODO`, pseudocodigo ni datos falsos.
- Mantener compatibilidad del contrato REST.

## Seguridad

- No versionar `.env`, tokens, API Keys, bases locales ni archivos de cobertura.
- Las contrasenas se almacenan hasheadas.
- JWT debe expirar.
- La autorizacion backend es obligatoria; ocultar botones no es seguridad.
- CORS se configura por entorno.
- Los valores de `.env.example` deben ser ejemplos no utilizables en produccion.

## Base De Datos

- Toda operacion financiera con varias escrituras debe confirmarse o revertirse
  como una sola transaccion.
- No borrar fisicamente historicos financieros.
- Respetar claves foraneas, unicidad y estados.
- No usar `float` para montos.
- Revisar migraciones antes de cambiar modelos.
- Las pruebas E2E usan `e2e_caja_ahorros.db`; nunca apuntarlas a datos reales.

## Roles

- ADMINISTRADOR: usuarios y consulta general.
- GERENTE: decision de creditos y reportes.
- CAJERO: socios, cuentas y operaciones.
- CONTADOR: Libro Diario y reportes contables.
- SOCIO: solo sus propios datos.

## Flujos Financieros

- Deposito/retiro: saldo, transaccion, comprobante y asiento en una unidad.
- Credito: solicitud, decision, amortizacion, desembolso y pago.
- Aportacion: deposito/retiro con permanencia minima.
- Contabilidad: debito y credito iguales, montos positivos y trazabilidad.

## Archivos Sensibles

Revisar con especial cuidado antes de modificar:

- `app/modelos/*`
- `app/servicios/*`
- `app/database.py`
- `app/dependencias.py`
- `seed.py`
- `.env.example`
- `database_mysql.sql`
- `.github/workflows/*`
- `frontend/src/servicios/clienteApi.ts`
- `frontend/src/contextos/*`

## Criterio De Terminado

Una tarea esta terminada cuando:

- implementacion real completa;
- pruebas proporcionales al riesgo;
- lint y build aprobados;
- documentacion actualizada;
- sin secretos ni temporales;
- cambios revisados en Git;
- evidencia reproducible del resultado.
