# Sistema de Gestion de Caja de Ahorros

Aplicacion web universitaria para administrar usuarios, socios, cuentas de
ahorro, transacciones, aportaciones, creditos, amortizacion, contabilidad y
reportes. El frontend React consume la API FastAPI real; no utiliza datos
codificados para simular operaciones.

- Autor: Steeven Ariel Martinez Campos
- Grupo: 01
- Repositorio: https://github.com/steevenmc04/Proyecto-Ing-Software
- Documentacion API: http://127.0.0.1:8000/docs

![Panel principal](docs/evidencias/03_dashboard.png)

## Objetivo y alcance

El proyecto integra los requerimientos T02.01, el diseno T02.02, el backend
T02.03 y las pruebas T02.04 en una aplicacion demostrable de principio a fin.
Incluye autenticacion, autorizacion por roles, reglas financieras, persistencia
relacional, interfaz responsiva, pruebas automatizadas, CI y documentacion.

## Tecnologias reales

### Backend

- Python 3.11 o superior.
- FastAPI 0.115, Uvicorn y Pydantic 2.
- SQLAlchemy 2.
- SQLite para desarrollo y pruebas.
- MySQL mediante PyMySQL para uso con MySQL Workbench.
- JWT, BCrypt, Pytest, Coverage y Ruff.

### Frontend

- React 19, TypeScript 6 y Vite 8.
- React Router, React Hook Form y Zod.
- Lucide React.
- jsPDF, jsPDF-AutoTable y write-excel-file.
- Vitest, React Testing Library y Playwright.

## Arquitectura

El backend conserva la separacion:

```text
Ruta -> Controlador -> Servicio -> Repositorio -> Modelo -> Base de datos
```

El frontend se organiza por modulos y comparte autenticacion, cliente HTTP,
componentes y utilidades. Las operaciones financieras se validan en el servicio
y se confirman con rollback ante errores.

Documentos:

- [Arquitectura completa](docs/ARQUITECTURA_COMPLETA.md)
- [Arquitectura frontend](docs/ARQUITECTURA_FRONTEND.md)
- [Contrato de las 58 operaciones](docs/CONTRATO_API.md)

## Estructura

```text
ProyectoIngSoftware/
|-- app/
|   |-- modelos/
|   |-- esquemas/
|   |-- repositorios/
|   |-- servicios/
|   |-- controladores/
|   |-- rutas/
|   `-- utilidades/
|-- frontend/
|   |-- src/
|   |-- tests-e2e/
|   `-- package.json
|-- tests/
|   |-- unit/
|   `-- integration/
|-- scripts/
|-- docs/
|   |-- evidencias/
|   `-- entrega/
|-- seed.py
|-- database_mysql.sql
`-- README.md
```

## Requisitos

- Python 3.11+.
- Node.js 20+ y npm.
- Git.
- MySQL Server y MySQL Workbench solo si se usara MySQL.

## Instalacion en Windows

Desde PowerShell:

```powershell
cd C:\Users\steeven\Documents\ProyectoIngSoftware
powershell -ExecutionPolicy Bypass -File .\scripts\instalar.ps1
Copy-Item .env.example .env
Copy-Item frontend\.env.example frontend\.env
python seed.py
```

Equivalente manual:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Set-Location frontend
npm ci
Set-Location ..
python seed.py
```

El seed es idempotente y crea datos academicos coherentes.

## Variables de entorno

Copiar `.env.example` a `.env` y cambiar las claves antes de cualquier entorno
distinto del desarrollo local.

```env
NOMBRE_APP=Sistema de Gestion de Caja de Ahorros
VERSION=1.0
DATABASE_URL=sqlite:///./caja_ahorros.db
CLAVE_JWT=reemplazar-por-secreto-aleatorio
ALGORITMO_JWT=HS256
MINUTOS_EXPIRACION_JWT=480
API_KEY_EXTERNA=reemplazar-por-clave-externa
ORIGENES_CORS=http://127.0.0.1:5173,http://localhost:5173
```

Frontend:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Los archivos `.env` no se versionan.

## Base de datos

SQLite es el valor predeterminado. SQLAlchemy crea las tablas y
`aplicar_migraciones_ligeras()` mantiene compatibilidad con la version
academica existente. El proyecto no utiliza Alembic; esta limitacion se
documenta para una futura evolucion.

### MySQL Workbench

1. Abrir `database_mysql.sql` en MySQL Workbench.
2. Ejecutar el script completo.
3. Configurar `.env`:

```env
DATABASE_URL=mysql+pymysql://usuario_caja:ClaveCaja123@localhost:3306/caja_ahorros
```

4. Ejecutar `python seed.py`.
5. Iniciar FastAPI.

## Levantar el proyecto

Terminal 1, backend:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\iniciar-backend.ps1
```

Terminal 2, frontend:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\iniciar-frontend.ps1
```

Abrir:

- Frontend: http://127.0.0.1:5173
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI: http://127.0.0.1:8000/openapi.json
- Salud: http://127.0.0.1:8000/api/v1/salud

### Build integrado

```powershell
Set-Location frontend
npm run build
Set-Location ..
powershell -ExecutionPolicy Bypass -File .\scripts\iniciar-backend.ps1
```

Con `frontend/dist` presente, FastAPI sirve la SPA tambien en
http://127.0.0.1:8000.

## Roles

| Rol | Permisos principales |
|---|---|
| ADMINISTRADOR | Usuarios, configuracion, consulta y operaciones generales |
| GERENTE | Decisiones de credito, cartera y reportes |
| CAJERO | Socios, cuentas, transacciones, aportaciones y cobros |
| CONTADOR | Libro Diario y reportes contables |
| SOCIO | Sus propias cuentas, movimientos y creditos |

El backend valida los roles; ocultar un boton en React no sustituye esta
autorizacion.

## Credenciales academicas

Solo para la base creada por `seed.py`:

| Rol | Usuario | Contrasena |
|---|---|---|
| Administrador | `admin` | `Admin123` |
| Gerente | `gerente` | `Gerente123` |
| Cajero | `cajero` | `Cajero123` |
| Contador | `contador` | `Contador123` |
| Socio | `socio` | `Socio123` |

No deben utilizarse en produccion.

## Modulos y flujos

- Usuarios: crear, listar, asignar rol, activar y desactivar.
- Socios: registrar, buscar, consultar detalle y cambiar estado.
- Cuentas: abrir, consultar saldo, bloquear, desbloquear y cerrar con saldo cero.
- Transacciones: deposito, retiro, comprobante, historial y asiento.
- Aportaciones: tipos, deposito, retiro a partir de seis meses y resumen.
- Creditos: solicitud, decision, amortizacion francesa, desembolso y pago.
- Contabilidad: partida doble y trazabilidad del origen.
- Reportes: Libro Diario, ahorros, cartera y aportaciones; PDF y XLSX.
- API externa: saldo y ultimos tres movimientos mediante `X-API-KEY`.

## API externa

```http
GET /api/v1/cuenta/movimientos?cedula=0102030405&numeroCuenta=CTA-000001
X-API-KEY: valor-configurado-en-el-servidor
```

La clave externa nunca se incluye en JavaScript publico.

## Pruebas y cobertura

Verificacion completa sin E2E:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verificar.ps1
```

Incluir los doce flujos E2E:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verificar.ps1 -IncluirE2E
```

Comandos individuales:

```powershell
ruff check app tests seed.py scripts
pytest -q
Set-Location frontend
npm run lint
npm test
npm run build
npm run test:e2e
```

Ultima verificacion local:

- Backend: 38 pruebas aprobadas.
- Cobertura backend: 83.37%.
- Frontend: 8 pruebas aprobadas.
- E2E: 12 flujos completos aprobados en Chromium.
- ESLint, Ruff y build: aprobados.

## Integracion continua

`.github/workflows/calidad.yml` ejecuta Ruff, Pytest con cobertura minima de
70%, ESLint, Vitest y el build de produccion. No contiene secretos.

## Despliegue

El repositorio queda preparado, no publicado en un entorno remoto. Para
desplegar:

1. Configurar secretos y `DATABASE_URL` en el proveedor.
2. Limitar `ORIGENES_CORS` al dominio real.
3. Ejecutar `npm ci && npm run build` en `frontend`.
4. Ejecutar `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Usar un gestor de migraciones antes de evolucionar el esquema en produccion.

## Solucion de problemas

### 401 Unauthorized

Iniciar sesion y enviar `Authorization: Bearer <token>`. La API externa utiliza
`X-API-KEY`, no JWT.

### No conecta a MySQL

Confirmar que MySQL Server este iniciado, que el esquema exista y que la URL use
`mysql+pymysql://`.

### El frontend no conecta

Revisar `VITE_API_URL`, iniciar el backend en el puerto 8000 y confirmar
`ORIGENES_CORS`.

### El puerto esta ocupado

Cerrar el proceso anterior o cambiar el puerto en el script y en la variable de
URL correspondiente.

## Documentacion

- [Auditoria](docs/AUDITORIA_ESTADO_ACTUAL.md)
- [Contrato API](docs/CONTRATO_API.md)
- [Matriz de trazabilidad](docs/MATRIZ_TRAZABILIDAD.md)
- [Plan de pruebas](docs/PLAN_PRUEBAS.md)
- [Manual de usuario](docs/MANUAL_USUARIO.md)
- [Manual tecnico](docs/MANUAL_TECNICO.md)
- [Tareas](docs/TAREAS_PROYECTO.md)
- [Guion de exposicion](docs/GUION_EXPOSICION.md)
- [Checklist](docs/CHECKLIST_ENTREGA.md)
- [Informe final](docs/entrega/TFINAL_Grupo01_MartinezSteeven.md)

## Riesgos residuales

- No hay migraciones Alembic; se usa creacion y migracion ligera.
- `npm audit` informa dos entradas de severidad alta asociadas a una vulnerabilidad
  del modo RSC de React Router 7.18.1. Esta SPA no usa RSC, acciones de servidor
  ni SSR. Bajar a 7.11.0 reintroduce multiples vulnerabilidades corregidas, por
  lo que se conserva 7.18.1 y se debe actualizar cuando exista una version
  compatible corregida.
- Python 3.14 muestra advertencias internas de FastAPI/Starlette sobre una API de
  `asyncio`; el entorno soportado de CI es Python 3.11.

## Autor

Steeven Ariel Martinez Campos, Grupo 01.
