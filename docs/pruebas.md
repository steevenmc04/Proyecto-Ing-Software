# Pruebas Del Sistema

## Comando

```powershell
pytest -q
```

## Cobertura Basica

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

## Resultado Esperado

```text
9 passed
```

