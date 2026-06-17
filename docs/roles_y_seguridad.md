# Roles Y Seguridad

## Roles

- ADMINISTRADOR
- GERENTE
- CAJERO
- SOCIO
- CONTADOR

## Seguridad

El sistema usa BCrypt para almacenar contrasenas hasheadas y JWT para autenticar usuarios.

## Restriccion De Socios

Cuando un usuario tiene rol SOCIO, el backend filtra:

- Cuentas.
- Transacciones.
- Creditos.

Esto evita que un cliente consulte informacion de otros socios.

