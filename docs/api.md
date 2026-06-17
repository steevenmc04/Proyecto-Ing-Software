# API Del Sistema

## Documentacion

- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## API Externa

Endpoint:

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

