# Sistema de Gestion de Caja de Ahorros

Backend funcional desarrollado para la Tarea T02.03 de Ingenieria de Software. El sistema implementa servicios REST documentados con Swagger para administrar usuarios, socios, cuentas de ahorro, depositos, retiros, aportaciones, creditos, cuotas de amortizacion, libro diario contable, reportes y una API externa de consulta de movimientos.

Repositorio placeholder: https://github.com/usuario/sistema-caja-ahorros-backend

## Objetivo academico

Demostrar la implementacion backend del sistema definido en T02.01 SRS y T02.02 DDS, usando una arquitectura por capas tipo modelo, repositorio, servicio, controlador y ruta. La entrega queda lista para ejecutarse localmente y publicarse en GitHub.

## Tecnologias usadas

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- SQLite para desarrollo local
- `DATABASE_URL` preparado para PostgreSQL o MySQL
- BCrypt para contrasenas
- JWT basico con PyJWT
- Pytest para pruebas
- Swagger en `/docs`
- Redoc en `/redoc`

## Arquitectura del proyecto

La arquitectura separa responsabilidades:

- `modelos`: entidades SQLAlchemy y relaciones.
- `esquemas`: modelos Pydantic para request y response.
- `repositorios`: consultas a base de datos.
- `servicios`: reglas de negocio.
- `controladores`: capa intermedia entre rutas y servicios.
- `rutas`: endpoints REST documentados.
- `utilidades`: seguridad, generadores y respuestas comunes.

## Estructura de carpetas

```text
sistema-caja-ahorros-backend/
|-- app/
|   |-- main.py
|   |-- config.py
|   |-- database.py
|   |-- dependencias.py
|   |-- modelos/
|   |-- esquemas/
|   |-- repositorios/
|   |-- servicios/
|   |-- controladores/
|   |-- rutas/
|   `-- utilidades/
|-- tests/
|-- docs/
|-- seed.py
|-- requirements.txt
|-- README.md
|-- .env.example
|-- .gitignore
`-- run.py
```

## Documentacion academica T02.03

La carpeta `docs/` contiene los documentos solicitados por la tarea:

- Requerimientos del sistema.
- Diseno y arquitectura.
- Tareas de seguimiento.
- Evidencias de funcionamiento.
- Conclusiones de 200 palabras.
- PDF de soporte para AVAC.

Archivo PDF generado:

```text
docs/T02_03_GrupoXX_MartinezSteeven.pdf
```

## Instalacion paso a paso

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

Copiar `.env.example` a `.env` si se desea personalizar configuracion:

```env
DATABASE_URL=sqlite:///./caja_ahorros.db
CLAVE_JWT=clave-academica-cambiar-en-produccion
API_KEY_EXTERNA=API-KEY-DEMO-123
```

Para MySQL Workbench se debe usar MySQL Server y el driver `pymysql`, incluido en `requirements.txt`.

Ejemplo para MySQL:

```env
DATABASE_URL=mysql+pymysql://usuario_caja:ClaveCaja123@localhost:3306/caja_ahorros
```

## Usar MySQL Workbench

1. Abrir MySQL Workbench y conectarse al servidor local.
2. Abrir el archivo `database_mysql.sql`.
3. Ejecutar todo el script para crear:
   - Base de datos `caja_ahorros`
   - Usuario `usuario_caja`
   - Permisos sobre la base
4. Crear un archivo `.env` copiando `.env.example`.
5. En `.env`, activar esta linea:

```env
DATABASE_URL=mysql+pymysql://usuario_caja:ClaveCaja123@localhost:3306/caja_ahorros
```

6. Instalar dependencias:

```bash
pip install -r requirements.txt
```

7. Iniciar el backend para que SQLAlchemy cree las tablas en MySQL:

```bash
uvicorn app.main:app --reload
```

8. En otra terminal, cargar datos de prueba:

```bash
python seed.py
```

Despues de eso, puedes revisar las tablas desde MySQL Workbench en el esquema `caja_ahorros`.

## Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

Tambien se puede ejecutar:

```bash
python run.py
```

## Levantar todo el proyecto localmente

### Opcion rapida con SQLite

```powershell
cd C:\Users\steeven\Documents\ProyectoIngSoftware
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python seed.py
uvicorn app.main:app --reload
```

Abrir en el navegador:

- Pagina funcional: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
- Salud API: http://127.0.0.1:8000/salud

La pagina funcional inicia con login. Despues muestra un menu desplegable con panel general, socios, cuentas, transacciones, creditos, reportes y API externa.

Usuarios recomendados para probar:

- Personal interno: `admin` / `Admin123`
- Cliente socio: `socio` / `Socio123`

Si ingresas como `admin`, se muestran formularios operativos para administrar el sistema. Si ingresas como `socio`, el sistema filtra los datos y solo muestra el perfil, cuentas y movimientos asociados a ese cliente.

### Opcion con MySQL Workbench

```powershell
cd C:\Users\steeven\Documents\ProyectoIngSoftware
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Luego en MySQL Workbench ejecutar:

```text
database_mysql.sql
```

Crear `.env` y dejar activo:

```env
DATABASE_URL=mysql+pymysql://usuario_caja:ClaveCaja123@localhost:3306/caja_ahorros
```

Despues:

```powershell
python seed.py
uvicorn app.main:app --reload
```

### Comandos utiles de limpieza

```powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
Remove-Item -Force caja_ahorros.db -ErrorAction SilentlyContinue
```

## Cargar datos de prueba

```bash
python seed.py
```

Datos creados:

- Administrador: `admin` / `Admin123`
- Gerente: `gerente` / `Gerente123`
- Cajero: `cajero` / `Cajero123`
- Contador: `contador` / `Contador123`
- Cliente socio: `socio` / `Socio123`
- Socio de prueba con cedula `0102030405`
- Cuenta de ahorro activa
- Tres depositos y un retiro
- Aportacion ordinaria
- Credito pendiente
- Credito aprobado con cuotas
- Asientos contables relacionados

## Ejecutar pruebas

```bash
pytest
```

Las pruebas cubren creacion de socio, cuenta, deposito, retiro, bloqueo por saldo insuficiente, solicitud y aprobacion de credito, generacion de cuotas y consulta de API externa con API Key.

## Documentacion

- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## Endpoints por modulo

### Autenticacion

- `POST /api/v1/auth/login`

### Usuarios

- `POST /api/v1/usuarios`
- `GET /api/v1/usuarios`
- `GET /api/v1/usuarios/{id}`
- `PUT /api/v1/usuarios/{id}`
- `PATCH /api/v1/usuarios/{id}/activar`
- `PATCH /api/v1/usuarios/{id}/desactivar`

### Socios

- `POST /api/v1/socios`
- `GET /api/v1/socios`
- `GET /api/v1/socios/{id}`
- `GET /api/v1/socios/buscar/cedula/{cedula}`
- `PUT /api/v1/socios/{id}`
- `PATCH /api/v1/socios/{id}/activar`
- `PATCH /api/v1/socios/{id}/desactivar`

### Cuentas

- `POST /api/v1/cuentas`
- `GET /api/v1/cuentas`
- `GET /api/v1/cuentas/{id}`
- `GET /api/v1/cuentas/socio/{socio_id}`
- `GET /api/v1/cuentas/numero/{numero_cuenta}`
- `PATCH /api/v1/cuentas/{id}/bloquear`
- `PATCH /api/v1/cuentas/{id}/desbloquear`
- `PATCH /api/v1/cuentas/{id}/cerrar`

### Transacciones

- `POST /api/v1/transacciones/deposito`
- `POST /api/v1/transacciones/retiro`
- `GET /api/v1/transacciones`
- `GET /api/v1/transacciones/cuenta/{cuenta_id}`
- `GET /api/v1/transacciones/{id}`

### Aportaciones

- `POST /api/v1/aportaciones/tipos`
- `GET /api/v1/aportaciones/tipos`
- `POST /api/v1/aportaciones/deposito`
- `POST /api/v1/aportaciones/retiro`
- `GET /api/v1/aportaciones`
- `GET /api/v1/aportaciones/socio/{socio_id}`

### Creditos y cuotas

- `POST /api/v1/creditos/solicitar`
- `GET /api/v1/creditos`
- `GET /api/v1/creditos/{id}`
- `GET /api/v1/creditos/socio/{socio_id}`
- `PATCH /api/v1/creditos/{id}/aprobar`
- `PATCH /api/v1/creditos/{id}/rechazar`
- `PATCH /api/v1/creditos/{id}/desembolsar`
- `POST /api/v1/creditos/{id}/pagar-cuota`
- `GET /api/v1/creditos/{id}/cuotas`
- `GET /api/v1/cuotas/{id}`

### Libro diario y reportes

- `GET /api/v1/asientos`
- `GET /api/v1/asientos/{id}`
- `GET /api/v1/asientos/rango-fechas`
- `GET /api/v1/reportes/libro-diario`
- `GET /api/v1/reportes/historial-ahorros/{socio_id}`
- `GET /api/v1/reportes/cartera-creditos`
- `GET /api/v1/reportes/resumen-aportaciones/{socio_id}`

### API externa

- `GET /api/v1/cuenta/movimientos?cedula=0102030405&numeroCuenta=CTA-000001`
- Header requerido: `X-API-KEY: API-KEY-DEMO-123`

## Relaciones entre modulos

- Un usuario registra muchos socios.
- Un socio tiene muchas cuentas de ahorro.
- Una cuenta tiene muchas transacciones.
- Una transaccion actualiza el saldo de la cuenta y genera un asiento contable.
- Un socio tiene muchas aportaciones.
- Una aportacion actualiza el total del socio y genera asiento contable.
- Un socio puede solicitar muchos creditos.
- Un credito aprobado genera cuotas de amortizacion por metodo frances.
- El pago de cuotas actualiza saldo pendiente y genera asiento contable.
- Los reportes consultan datos reales de las tablas.
- La API externa consulta la misma cuenta y transacciones del historial de ahorros.

## Cumplimiento de T02.03

El proyecto cumple la T02.03 porque implementa un backend funcional con FastAPI, documentacion Swagger, arquitectura por capas, modelos relacionales con SQLAlchemy, schemas Pydantic, reglas de negocio, validaciones con `HTTPException`, autenticacion JWT, seed de datos, pruebas basicas con pytest, README tecnico y configuracion lista para GitHub.
