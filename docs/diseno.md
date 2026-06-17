# Diseno Del Backend

## Arquitectura

El proyecto aplica una arquitectura por capas:

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

