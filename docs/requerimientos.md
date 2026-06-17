# Requerimientos Del Sistema

## Proyecto

Sistema de Gestion de Caja de Ahorros.

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

