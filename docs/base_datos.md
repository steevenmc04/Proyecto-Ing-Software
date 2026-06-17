# Base De Datos

## Motor Local

El proyecto usa SQLite por defecto para desarrollo local.

## Motor Alternativo

El proyecto esta preparado para MySQL mediante la variable:

```env
DATABASE_URL=mysql+pymysql://usuario_caja:ClaveCaja123@localhost:3306/caja_ahorros
```

## Tablas Principales

- usuarios
- socios
- cuentas_ahorro
- transacciones
- tipos_aportacion
- aportaciones
- creditos
- cuotas_amortizacion
- asientos_contables

## Observacion

SQLAlchemy crea las tablas automaticamente al iniciar la aplicacion.

