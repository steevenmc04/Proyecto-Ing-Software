# Matriz de trazabilidad

Los identificadores RF-001 a RF-022 se normalizaron a partir del alcance
funcional T02.01-TFINAL encontrado en el repositorio. `CUMPLE` significa que
existen implementacion, prueba automatizada y evidencia verificable.

| ID | Requisito | Modelo | Endpoint principal | Servicio | Pantalla | Prueba | Estado | Evidencia |
|---|---|---|---|---|---|---|---|---|
| RF-001 | Iniciar sesion con credenciales validas | Usuario | `POST /api/v1/auth/login` | Autenticacion | Login | `tests/unit/test_auth.py` | CUMPLE | `01_login.png` |
| RF-002 | Restringir funciones por rol | Usuario/Rol | `GET /api/v1/auth/me` | Autenticacion y dependencias | Menu y rutas | `test_autorizacion_roles.py` | CUMPLE | `03_dashboard.png` |
| RF-003 | Administrar usuarios | Usuario | `/api/v1/usuarios` | Usuario | Usuarios | `tests/unit/test_usuarios.py` | CUMPLE | Prueba automatizada |
| RF-004 | Registrar y buscar socios | Socio | `/api/v1/socios` | Socio | Socios | `tests/unit/test_socios.py` | CUMPLE | `05_socios.png` |
| RF-005 | Activar o desactivar socios | Socio | `PATCH /api/v1/socios/{id}/*` | Socio | Socios | `tests/unit/test_socios.py` | CUMPLE | Prueba automatizada |
| RF-006 | Abrir cuentas con saldo inicial cero | CuentaAhorro | `POST /api/v1/cuentas` | CuentaAhorro | Cuentas | `tests/unit/test_cuentas.py` | CUMPLE | `06_cuenta.png` |
| RF-007 | Bloquear, desbloquear y cerrar cuentas | CuentaAhorro | `PATCH /api/v1/cuentas/{id}/*` | CuentaAhorro | Cuentas | `tests/unit/test_cuentas.py` | CUMPLE | Prueba automatizada |
| RF-008 | Registrar depositos atomicos | Transaccion/Asiento | `POST /api/v1/transacciones/deposito` | Transaccion | Transacciones | `test_flujo_transacciones.py` | CUMPLE | `07_deposito.png` |
| RF-009 | Registrar retiros sin sobregiro | Transaccion/Asiento | `POST /api/v1/transacciones/retiro` | Transaccion | Transacciones | `test_flujo_transacciones.py` | CUMPLE | `08_retiro.png` |
| RF-010 | Consultar movimientos y comprobantes | Transaccion | `/api/v1/transacciones` | Transaccion | Transacciones | `tests/unit/test_transacciones.py` | CUMPLE | `08_retiro.png` |
| RF-011 | Administrar tipos de aportacion | TipoAportacion | `/api/v1/aportaciones/tipos` | Aportacion | Aportaciones | `tests/unit/test_aportaciones.py` | CUMPLE | Prueba automatizada |
| RF-012 | Depositar y retirar aportaciones | Aportacion/Asiento | `/api/v1/aportaciones/*` | Aportacion | Aportaciones | `tests/unit/test_aportaciones.py` | CUMPLE | Prueba automatizada |
| RF-013 | Solicitar creditos | Credito | `POST /api/v1/creditos/solicitar` | Credito | Creditos | `test_flujo_creditos.py` | CUMPLE | `09_creditos.png` |
| RF-014 | Aprobar o rechazar por rol autorizado | Credito | `PATCH /api/v1/creditos/{id}/*` | Credito | Creditos | `test_flujo_creditos.py` | CUMPLE | `09_creditos.png` |
| RF-015 | Generar amortizacion francesa | Credito/Cuota | `GET /api/v1/creditos/{id}/cuotas` | Amortizacion | Creditos | `tests/unit/test_creditos.py` | CUMPLE | `10_amortizacion.png` |
| RF-016 | Desembolsar un credito aprobado | Credito/Asiento | `PATCH /api/v1/creditos/{id}/desembolsar` | Credito | Creditos | `test_flujo_creditos.py` | CUMPLE | Flujo E2E 09 |
| RF-017 | Pagar cuotas y actualizar el credito | Cuota/Credito/Asiento | `POST /api/v1/creditos/{id}/pagar-cuota` | Credito | Creditos | `test_flujo_creditos.py` | CUMPLE | `11_pago_cuota.png` |
| RF-018 | Consultar Libro Diario con partida doble | AsientoContable | `/api/v1/asientos` | AsientoContable | Contabilidad | `tests/unit/test_reportes.py` | CUMPLE | `12_libro_diario.png` |
| RF-019 | Generar reportes desde datos reales | Varias entidades | `/api/v1/reportes/*` | Reporte | Reportes | `tests/unit/test_reportes.py` | CUMPLE | `13_reportes.png` |
| RF-020 | Exportar reportes a PDF y XLSX | Respuestas de reportes | `/api/v1/reportes/*` | Cliente de reportes | Reportes | Build y E2E | CUMPLE | `13_reportes.png` |
| RF-021 | Exponer saldo y tres movimientos con API Key | Cuenta/Transaccion | `GET /api/v1/cuenta/movimientos` | API externa | Integracion externa | `test_flujo_api_externa.py` | CUMPLE | Swagger y prueba |
| RF-022 | Permitir al socio consultar solo datos propios | Socio/Cuenta/Credito | `/mis-cuentas`, `/mis-transacciones`, `/mis-creditos` | Autorizacion por propiedad | Panel del socio | `test_autorizacion_roles.py` | CUMPLE | Prueba automatizada |

## Requisitos no funcionales

| ID | Requisito | Verificacion | Estado |
|---|---|---|---|
| RNF-001 | API documentada | Swagger, ReDoc y `CONTRATO_API.md` | CUMPLE |
| RNF-002 | Interfaz responsiva | Capturas de escritorio y movil | CUMPLE |
| RNF-003 | Cobertura minima de 70% | Pytest y Coverage | CUMPLE |
| RNF-004 | Build de produccion | `npm run build` | CUMPLE |
| RNF-005 | Sin secretos versionados | Configuracion por entorno, `.gitignore` y revision Git | CUMPLE |
| RNF-006 | Despliegue remoto | No se solicito proveedor ni credenciales | NO VERIFICADO |
