# Guion de exposicion

Duracion objetivo: 9 a 10 minutos.

## 1. Presentacion - 30 segundos

"Buenos dias. Soy Steeven Ariel Martinez Campos, del Grupo 01. Presento el
Sistema de Gestion de Caja de Ahorros, una aplicacion web completa construida
con FastAPI, React y una base de datos relacional."

## 2. Problema y objetivo - 45 segundos

Explicar que una caja de ahorros necesita controlar socios, saldos, creditos y
contabilidad sin duplicar datos ni permitir operaciones no autorizadas. El
objetivo fue integrar los entregables anteriores en un sistema demostrable,
seguro y trazable.

## 3. Arquitectura - 60 segundos

Mostrar `docs/ARQUITECTURA_COMPLETA.md`. Explicar el recorrido:

```text
React -> Ruta -> Controlador -> Servicio -> Repositorio -> Modelo -> BD
```

Destacar que las reglas financieras estan en servicios y que SQLite o MySQL se
intercambian mediante `DATABASE_URL`.

## 4. Backend - 60 segundos

Abrir Swagger. Mostrar salud, autenticacion, socios, cuentas, transacciones,
creditos, asientos y reportes. Explicar JWT, roles, `Decimal`, rollback y la
API externa protegida con `X-API-KEY`.

## 5. Frontend - 45 segundos

Mostrar el login, el layout adaptable, el usuario autenticado y el menu que
cambia segun el rol. Indicar que formularios y tablas consumen la API real.

## 6. Demostracion - 4 minutos

1. Iniciar sesion como administrador.
2. Registrar o buscar un socio.
3. Abrir una cuenta de ahorro.
4. Realizar un deposito y comprobar el saldo.
5. Mostrar que un retiro valida saldo y estado.
6. Solicitar y aprobar un credito.
7. Abrir la tabla de amortizacion.
8. Desembolsar y pagar una cuota.
9. Ver el asiento relacionado en Libro Diario.
10. Abrir reportes y exportar PDF o XLSX.

## 7. Pruebas y seguridad - 60 segundos

Mostrar las capturas de pruebas, cobertura y build. Mencionar pruebas backend,
frontend y doce flujos E2E. Explicar que el socio solo consulta datos propios,
las claves viven en `.env` y la autorizacion se valida en backend.

## 8. Conclusion - 30 segundos

"El resultado integra frontend, backend, persistencia, seguridad, pruebas y
documentacion. Los flujos principales son reproducibles localmente y el
repositorio queda listo para evaluacion y para un despliegue posterior."

## Preguntas probables

**Por que FastAPI?**  
Por validacion Pydantic, documentacion OpenAPI automatica, buen tipado y una
estructura adecuada para servicios.

**Como se evita un saldo negativo?**  
El servicio comprueba estado y saldo antes de modificar; saldo, transaccion y
asiento se confirman juntos o se revierten.

**Como se protegen las cuentas de un socio?**  
El JWT identifica al usuario y los endpoints `mis-*` filtran por su relacion
con Socio. Las rutas administrativas exigen roles.

**Como funciona la amortizacion?**  
Usa el metodo frances con `Decimal`, redondeo monetario y ajuste de la ultima
cuota para que el capital coincida.

**La API externa es el frontend?**  
No. Es una integracion separada para consultar saldo y tres movimientos con
`X-API-KEY`; la SPA usa JWT.

**Esta desplegado?**  
No se declara despliegue remoto. Esta validado localmente y preparado para que
un proveedor configure secretos, base, CORS y HTTPS.

**Que limitacion tecnica queda?**  
El esquema academico usa `create_all` y migraciones ligeras; un entorno
productivo deberia incorporar Alembic.

