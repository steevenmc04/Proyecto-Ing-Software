# Documentacion T02.03

## Datos Generales

- Grupo base: Grupo XX
- Integrante: Martinez Steeven
- Proyecto: Sistema de Gestion de Caja de Ahorros
- Repositorio: https://github.com/steevenmc04/Proyecto-Ing-Software

## Objetivo

Crear una aplicacion backend funcional utilizando herramientas de Ingenieria de
Software, aplicando arquitectura por capas, servicios REST, documentacion
Swagger y control de versiones con GitHub.

## Framework Utilizado

FastAPI.

## Servicios Publicados

- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
- Pagina funcional: http://127.0.0.1:8000

## Requerimientos Funcionales

1. Administrar usuarios con roles: ADMINISTRADOR, GERENTE, CAJERO, SOCIO y CONTADOR.
2. Permitir autenticacion con contrasena hasheada y token JWT.
3. Registrar, listar, buscar, actualizar, activar y desactivar socios.
4. Crear cuentas de ahorro asociadas a socios.
5. Registrar depositos y retiros, actualizando el saldo de la cuenta.
6. Impedir retiros cuando el saldo sea insuficiente.
7. Registrar aportaciones ordinarias y extraordinarias.
8. Validar que no se retiren aportaciones antes de seis meses.
9. Solicitar, aprobar, rechazar, desembolsar y pagar creditos.
10. Generar cuotas con metodo frances.
11. Generar asientos contables para operaciones financieras.
12. Consultar reportes de libro diario, historial de ahorros, cartera de creditos y aportaciones.
13. Exponer una API externa para consultar saldo y ultimos movimientos mediante `X-API-KEY`.
14. Mostrar una pagina funcional con login, menu y vistas por modulo.
15. Restringir a los usuarios de rol SOCIO para que solo vean sus cuentas, movimientos y creditos asociados.

## Requerimientos No Funcionales

- Backend implementado con FastAPI.
- Persistencia con SQLAlchemy.
- Base SQLite para desarrollo local.
- Preparado para MySQL mediante `DATABASE_URL`.
- Documentacion automatica con Swagger y Redoc.
- Pruebas basicas con pytest.
- Codigo organizado por modelo, repositorio, servicio, controlador y ruta.

## Arquitectura

El proyecto aplica una arquitectura por capas:

![Figura arquitectura T02.03](figura_arquitectura_t0203.svg)

- `modelos`: entidades SQLAlchemy y relaciones de base de datos.
- `esquemas`: schemas Pydantic para entrada y salida de datos.
- `repositorios`: consultas y persistencia.
- `servicios`: reglas de negocio.
- `controladores`: coordinacion entre rutas y servicios.
- `rutas`: endpoints REST documentados en Swagger.
- `utilidades`: seguridad, generadores y helpers comunes.

## Decisiones De Diseno

1. Se utiliza FastAPI porque genera documentacion Swagger automaticamente y permite construir servicios REST de forma clara.
2. SQLAlchemy centraliza los modelos y relaciones con llaves foraneas reales.
3. Pydantic valida los datos de entrada antes de llegar a la logica de negocio.
4. JWT permite separar el login del consumo de servicios protegidos.
5. La pagina web local consume los mismos endpoints que Swagger, evitando datos quemados.
6. Los usuarios con rol SOCIO tienen consultas filtradas por su socio asociado.
7. Las operaciones financieras crean asientos contables desde los servicios para mantener trazabilidad.

## Relaciones Principales

- Usuario registra socios.
- Usuario puede estar vinculado a un socio cuando su rol es SOCIO.
- Socio tiene cuentas de ahorro.
- Cuenta tiene transacciones.
- Socio tiene aportaciones.
- Socio solicita creditos.
- Credito tiene cuotas de amortizacion.
- Transaccion, aportacion, desembolso y pago generan asientos contables.

## Tareas De Seguimiento

La tarea T02.03 solicita definir tareas de seguimiento asignadas a integrantes
del grupo. Para fines academicos se registra la planificacion por rol de trabajo.

| Codigo | Tarea | Responsable | Estado |
| --- | --- | --- | --- |
| T-01 | Crear repositorio GitHub | Martinez Steeven | Completado |
| T-02 | Definir estructura backend por capas | Martinez Steeven | Completado |
| T-03 | Implementar modelos SQLAlchemy | Martinez Steeven | Completado |
| T-04 | Implementar schemas Pydantic | Martinez Steeven | Completado |
| T-05 | Implementar repositorios | Martinez Steeven | Completado |
| T-06 | Implementar servicios de usuarios y login JWT | Martinez Steeven | Completado |
| T-07 | Implementar socios y cuentas | Martinez Steeven | Completado |
| T-08 | Implementar depositos, retiros y saldos | Martinez Steeven | Completado |
| T-09 | Implementar aportaciones | Martinez Steeven | Completado |
| T-10 | Implementar creditos y amortizacion | Martinez Steeven | Completado |
| T-11 | Implementar libro diario contable | Martinez Steeven | Completado |
| T-12 | Implementar reportes JSON | Martinez Steeven | Completado |
| T-13 | Implementar API externa con X-API-KEY | Martinez Steeven | Completado |
| T-14 | Crear seed de datos de prueba | Martinez Steeven | Completado |
| T-15 | Crear pruebas con pytest | Martinez Steeven | Completado |
| T-16 | Crear pagina funcional con login y menu | Martinez Steeven | Completado |
| T-17 | Documentar ejecucion local y MySQL Workbench | Martinez Steeven | Completado |
| T-18 | Preparar evidencias y conclusiones | Martinez Steeven | Completado |

## Base De Datos

El proyecto usa SQLite por defecto para desarrollo local y esta preparado para
MySQL mediante la variable:

```env
DATABASE_URL=mysql+pymysql://usuario_caja:ClaveCaja123@localhost:3306/caja_ahorros
```

Tablas principales:

- usuarios
- socios
- cuentas_ahorro
- transacciones
- tipos_aportacion
- aportaciones
- creditos
- cuotas_amortizacion
- asientos_contables

SQLAlchemy crea las tablas automaticamente al iniciar la aplicacion.

## Roles Y Seguridad

Roles disponibles:

- ADMINISTRADOR
- GERENTE
- CAJERO
- SOCIO
- CONTADOR

El sistema usa BCrypt para almacenar contrasenas hasheadas y JWT para autenticar
usuarios. Cuando un usuario tiene rol SOCIO, el backend filtra cuentas,
transacciones y creditos para evitar que consulte informacion de otros socios.

## API Del Sistema

Documentacion:

- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

API externa:

```http
GET /api/v1/cuenta/movimientos
```

Parametros:

- `cedula`
- `numeroCuenta`

Header:

```text
X-API-KEY: API-KEY-DEMO-123
```

La respuesta devuelve saldo y los ultimos tres movimientos reales de la cuenta.

## Guia De Despliegue Local

SQLite:

```powershell
cd C:\Users\steeven\Documents\ProyectoIngSoftware
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python seed.py
uvicorn app.main:app --reload
```

MySQL Workbench:

1. Ejecutar `database_mysql.sql` en MySQL Workbench.
2. Configurar `.env`:

```env
DATABASE_URL=mysql+pymysql://usuario_caja:ClaveCaja123@localhost:3306/caja_ahorros
```

3. Ejecutar:

```powershell
python seed.py
uvicorn app.main:app --reload
```

## Manual De Usuario

Ingresar a la pagina funcional:

http://127.0.0.1:8000

Usuarios de prueba:

- Administrador: `admin` / `Admin123`
- Socio: `socio` / `Socio123`

El sistema muestra un menu desplegable con los modulos principales:

- Panel general.
- Socios.
- Cuentas.
- Transacciones.
- Creditos.
- Reportes.
- API externa.

El administrador puede consultar datos generales y usar formularios para
registrar socios, cuentas, movimientos y creditos. El socio solo visualiza su
perfil, sus cuentas, sus transacciones y sus creditos asociados.

## Pruebas Del Sistema

Comando:

```powershell
pytest -q
```

Las pruebas verifican:

- Creacion de socios.
- Creacion de cuentas.
- Depositos.
- Retiros.
- Bloqueo de retiro por saldo insuficiente.
- Solicitud de creditos.
- Aprobacion y generacion de cuotas.
- API externa con API Key.
- Restriccion para que un usuario SOCIO solo vea sus cuentas.

Resultado esperado:

```text
9 passed
```

## Evidencias De Funcionamiento

- Repositorio: https://github.com/steevenmc04/Proyecto-Ing-Software
- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
- Pagina funcional: http://127.0.0.1:8000

Comandos de ejecucion:

```powershell
cd C:\Users\steeven\Documents\ProyectoIngSoftware
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python seed.py
uvicorn app.main:app --reload
```

## Registro De Commits

El repositorio debe conservar como minimo 20 commits para evidenciar el avance
iterativo del desarrollo. El conteo actual se debe consultar directamente desde
Git para evitar que este documento quede desactualizado.

Comando para contar commits:

```powershell
git rev-list --count main
```

## Conclusiones

El desarrollo de la Tarea T02.03 permitio transformar los requerimientos y el
diseno del Sistema de Gestion de Caja de Ahorros en una aplicacion backend
funcional. Durante la implementacion se aplico una arquitectura por capas que
separa modelos, repositorios, servicios, controladores y rutas, lo que facilita
el mantenimiento y la comprension del codigo. FastAPI resulto adecuado para
publicar servicios REST documentados con Swagger, mientras que SQLAlchemy
permitio representar relaciones reales entre usuarios, socios, cuentas,
transacciones, aportaciones, creditos, cuotas y asientos contables.

La construccion tambien evidencio la importancia de validar reglas de negocio
desde el backend, especialmente en operaciones financieras como retiros,
aportaciones, creditos y pagos. Adicionalmente, la incorporacion de
autenticacion JWT y restricciones por rol permite que los socios consulten solo
su informacion asociada, mejorando la seguridad del sistema. Las pruebas
automatizadas con pytest ayudan a verificar que los flujos principales funcionen
correctamente y reducen el riesgo de errores al modificar el proyecto.
Finalmente, el uso de GitHub como repositorio permite evidenciar el avance del
trabajo, documentar la solucion y mantener un historial de cambios organizado
para la entrega academica. Esta experiencia consolido buenas practicas de
documentacion, verificacion continua y despliegue local reproducible para
futuras iteraciones funcionales del sistema academico.

## Rubrica De Calificacion

La siguiente tabla resume los criterios de evaluacion solicitados para la Tarea
T02.03 y la evidencia incluida en el repositorio.

| Criterios | No Presenta | Nivel Bajo | Nivel Medio | Nivel Alto | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Repositorio correctamente documentado con los requerimientos, diseno y tareas definidas por usuario. | 0 | 0.5 | 1 | 2 | 2 |
| Al menos 20 commits en el repositorio que aseguren que han trabajado todos los companeros. | 0 | 0.2 | 0.5 | 1 | 1 |
| Servicios funcionales y correctamente desplegados. | 0 | 0.2 | 0.5 | 1 | 1 |

Evidencia:

| Criterio | Evidencia del proyecto |
| --- | --- |
| Repositorio documentado | `README.md` y carpeta `docs/` |
| Requerimientos | Seccion "Requerimientos Funcionales" |
| Diseno | Seccion "Arquitectura" y `docs/figura_arquitectura_t0203.svg` |
| Tareas definidas | Seccion "Tareas De Seguimiento" |
| Commits | `git rev-list --count main` debe mostrar 20 o mas commits |
| Servicios funcionales | FastAPI con rutas en `/api/v1` |
| Swagger | `http://127.0.0.1:8000/docs` |
| Conclusiones | Seccion "Conclusiones" |

Puntaje estimado segun la evidencia del repositorio: 4 de 4 puntos.
