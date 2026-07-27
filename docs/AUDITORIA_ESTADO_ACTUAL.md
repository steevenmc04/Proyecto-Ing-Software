# Auditoria Del Estado Actual

Fecha de auditoria: 26 de julio de 2026.

## 1. Resumen Del Repositorio

El repositorio contiene un backend academico funcional para el Sistema de
Gestion de Caja de Ahorros. Esta implementado con FastAPI, SQLAlchemy y
Pydantic, incluye una pagina HTML monolitica para demostracion y una suite de
pruebas ampliada para la T02.04.

Datos verificados:

- Rama actual: `main`.
- Remoto: `origin/main`.
- Commits al iniciar la auditoria: 26.
- Python: 3.14.4.
- Node.js: 24.15.0.
- npm: 11.12.1.
- Frontend React: no existe.
- Migraciones Alembic: no existen.
- Configuracion Sites: no existe.
- Rutas OpenAPI: 51.
- Operaciones OpenAPI: 57.
- Pruebas: 34 aprobadas.
- Cobertura: 83.93%.
- Advertencias de pruebas: 410.

El arbol de trabajo ya contenia cambios locales preparados antes de esta
auditoria. Incluyen pruebas T02.04, cobertura, un workflow, un documento Word y
scripts de generacion. Esos cambios se conservan y deben revisarse antes de
crear commits.

## 2. Arquitectura Encontrada

El backend sigue esta secuencia:

```text
Ruta -> Controlador -> Servicio -> Repositorio -> Modelo -> Base de datos
```

Carpetas principales:

- `app/modelos`: entidades y enumeraciones SQLAlchemy.
- `app/esquemas`: contratos Pydantic.
- `app/repositorios`: acceso a datos.
- `app/servicios`: reglas de negocio.
- `app/controladores`: coordinacion de casos de uso.
- `app/rutas`: endpoints FastAPI.
- `app/utilidades`: seguridad, respuestas y generadores.
- `app/static`: pagina HTML de demostracion existente.
- `tests/unit`: pruebas unitarias y de endpoints.
- `tests/integration`: flujos integrados.
- `docs`: documentacion academica.

La separacion por capas es adecuada. El principal problema arquitectonico es
que la autorizacion no se aplica de forma transversal: la mayoria de las rutas
administrativas y financieras no requieren autenticacion.

## 3. Tecnologias Encontradas

Backend:

- FastAPI 0.115.x.
- Starlette 0.40-0.41.
- SQLAlchemy 2.x.
- Pydantic 2.x.
- Uvicorn.
- PyJWT.
- Passlib y BCrypt.
- SQLite para desarrollo y pruebas.
- PyMySQL para MySQL.
- pytest, pytest-cov y coverage.

Frontend actual:

- HTML, CSS y JavaScript sin framework en `app/static/index.html`.
- No existe React, Vite, TypeScript, React Router, Vitest ni Playwright.

Calidad:

- Cobertura configurada con minimo de 80%.
- No existe Ruff instalado ni configurado.
- No existe Mypy instalado ni configurado.
- El workflow actual solo valida Python y usa un umbral distinto de cobertura.

## 4. Modulos Existentes

- Autenticacion.
- Usuarios y roles.
- Socios.
- Cuentas de ahorro.
- Depositos y retiros.
- Tipos y movimientos de aportacion.
- Creditos.
- Cuotas de amortizacion.
- Asientos contables.
- Reportes.
- API externa.
- Seed academico.

## 5. Endpoints Reales

El contrato OpenAPI expone 57 operaciones. Los grupos encontrados son:

- `/api/v1/auth`: login y usuario actual.
- `/api/v1/usuarios`: CRUD, activacion y desactivacion.
- `/api/v1/socios`: listado, busqueda, perfil y mantenimiento.
- `/api/v1/cuentas`: listado, consulta y cambios de estado.
- `/api/v1/transacciones`: depositos, retiros y consultas.
- `/api/v1/aportaciones`: catalogo, depositos, retiros y consultas.
- `/api/v1/creditos`: solicitud, decision, desembolso, pago y cuotas.
- `/api/v1/cuotas`: consulta individual.
- `/api/v1/asientos`: Libro Diario y filtro por fechas.
- `/api/v1/reportes`: ahorros, creditos, aportaciones y Libro Diario.
- `/api/v1/cuenta/movimientos`: API externa con `X-API-KEY`.
- `/salud`: comprobacion basica actual.

Swagger y ReDoc cargaron correctamente en `/docs` y `/redoc`. El contrato
detallado se generara en `docs/CONTRATO_API.md`.

## 6. Pruebas Existentes

Comando ejecutado:

```powershell
pytest -q
```

Resultado real:

```text
34 passed, 410 warnings
Total coverage: 83.93%
```

Existen pruebas de autenticacion, usuarios, socios, cuentas, transacciones,
aportaciones, creditos, cuotas, reportes y API externa. Tambien existen tres
flujos de integracion.

No existen pruebas de frontend ni pruebas E2E en navegador.

## 7. Problemas Encontrados

1. No existe frontend React, Vite y TypeScript.
2. Casi todas las rutas administrativas y financieras son publicas.
3. No existe una dependencia central de autorizacion por roles.
4. No hay CORS configurado.
5. Falta `GET /api/v1/salud` con el contrato solicitado.
6. La pagina HTML publica contiene credenciales y una API Key de demostracion.
7. La clave JWT y API Key tienen valores por defecto utilizables.
8. `database_mysql.sql` contiene una contrasena fija de demostracion.
9. No existe Alembic; solo `create_all` y una migracion ligera manual.
10. Se utilizan fechas UTC sin zona horaria y APIs `utcnow` obsoletas.
11. Varias operaciones financieras hacen `commit` dentro del servicio sin un
    manejador explicito de rollback.
12. No se valida siempre que el usuario referenciado tenga el rol requerido.
13. Un credito aprobado admite pago antes del desembolso.
14. No existe comprobante independiente para pagos de cuotas.
15. Los asientos representan debito y credito en una fila, pero no existen
    lineas contables separadas.
16. No existe exportacion PDF/XLSX.
17. No existe CI para frontend.
18. `.coverage` esta preparado para versionarse y debe eliminarse del indice.
19. Hay archivos de salida de pruebas y cobertura preparados para Git.
20. No existen manuales, trazabilidad, contrato, evidencias ni reporte final
    con la estructura nueva solicitada.

## 8. Riesgos Tecnicos

- Critico: acceso anonimo a operaciones financieras.
- Critico: exposicion de credenciales/API Key en la interfaz estatica.
- Alto: reglas de rol solo visibles en UI, no garantizadas en backend.
- Alto: falta de rollback uniforme en operaciones con varias escrituras.
- Alto: configuracion insegura si se despliega con valores por defecto.
- Medio: migraciones no reproducibles para cambios de esquema.
- Medio: fechas sin zona horaria y 410 advertencias.
- Medio: frontend inexistente y contrato sin cliente tipado.
- Bajo: duplicacion de dependencias en `requirements.txt`.

## 9. Funcionalidades Faltantes

- Frontend React completo y responsivo.
- Autorizacion backend por rol.
- Dashboard por rol.
- Pantallas de usuarios, socios, cuentas, transacciones, aportaciones,
  creditos, contabilidad y reportes.
- Exportacion PDF y XLSX.
- Pruebas unitarias de frontend y E2E.
- Scripts PowerShell de instalacion, inicio y verificacion.
- CI integral.
- Documentacion final, evidencias e informe PDF.

## 10. Plan De Correccion Priorizado

1. Preservar y ordenar los cambios locales existentes.
2. Agregar salud versionada, CORS por entorno y autorizacion por roles.
3. Corregir transacciones, validaciones y configuracion insegura.
4. Actualizar pruebas de regresion y conservar cobertura superior a 80%.
5. Crear React + Vite + TypeScript sobre el contrato real.
6. Implementar autenticacion, layout y modulos por rol.
7. Agregar exportacion, pruebas, E2E, scripts Windows y CI.
8. Completar documentacion, evidencias e informe reproducible.
9. Ejecutar instalacion y verificacion final.

## 11. Comparacion Solicitado Vs. Implementado

| Area | Estado | Evidencia |
| --- | --- | --- |
| Backend FastAPI | CUMPLE | La aplicacion inicia y OpenAPI carga |
| Arquitectura por capas | CUMPLE | Carpetas de rutas, controladores, servicios y repositorios |
| Swagger y ReDoc | CUMPLE | `/docs` y `/redoc` verificados |
| Modelos relacionales | CUMPLE PARCIALMENTE | Existen FK y relaciones; faltan restricciones y migraciones formales |
| Reglas financieras | CUMPLE PARCIALMENTE | Flujos base existen; faltan autorizacion y transaccion uniforme |
| Seguridad JWT | CUMPLE PARCIALMENTE | JWT existe; proteccion de rutas es insuficiente |
| API externa | CUMPLE PARCIALMENTE | Contrato funciona; la clave se muestra en UI/documentacion |
| Pruebas backend | CUMPLE | 34 pruebas y 83.93% |
| Frontend moderno | NO CUMPLE | Solo existe HTML monolitico |
| Pruebas frontend/E2E | NO CUMPLE | No existen |
| CI integral | CUMPLE PARCIALMENTE | Workflow solo backend y umbral inconsistente |
| Scripts Windows | NO CUMPLE | No existen |
| Documentacion final | CUMPLE PARCIALMENTE | README previo existe; faltan artefactos solicitados |
| Evidencias visuales | NO CUMPLE | No existe carpeta de evidencias reales |
| Informe PDF final | NO CUMPLE | No existe el informe TFINAL solicitado |
| Despliegue | NO VERIFICADO | Solo se comprobo ejecucion local |

## 12. Estado General

Estado inicial: **CUMPLE PARCIALMENTE**.

El backend tiene una base funcional y una cobertura suficiente, pero el
proyecto final todavia no cumple por la ausencia del frontend React, la
autorizacion incompleta y la falta de artefactos finales.
