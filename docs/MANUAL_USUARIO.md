# Manual de usuario

## Ingreso

1. Abra `http://127.0.0.1:5173`.
2. Escriba usuario y contrasena.
3. Seleccione **Ingresar**.
4. El sistema mostrara solo los modulos autorizados para su rol.

La sesion se cierra desde el menu del usuario. Si el token expira, la
aplicacion vuelve al inicio de sesion y muestra el motivo.

## Navegacion

En escritorio, el menu lateral permite cambiar de modulo. En movil, el boton
de menu abre las mismas opciones. El encabezado identifica al usuario activo y
la ruta actual. Las operaciones muestran carga, confirmacion o error.

## Usuarios

Disponible para ADMINISTRADOR. Permite listar, crear, editar, activar y
desactivar usuarios. El nombre de usuario y el correo deben ser unicos. La
contrasena debe cumplir la longitud indicada por el formulario.

## Socios

ADMINISTRADOR y CAJERO pueden registrar y editar socios. La busqueda acepta
cedula, nombre o numero de socio. La cedula no puede repetirse. Un socio
inactivo conserva su historial, pero no puede iniciar nuevas operaciones.

## Cuentas

1. Abra **Cuentas**.
2. Seleccione el socio.
3. Cree la cuenta; su saldo inicial sera USD 0,00.
4. Use las acciones para bloquear, desbloquear o cerrar.

Una cuenta bloqueada o cerrada no admite movimientos. Solo se puede cerrar con
saldo cero.

## Depositos y retiros

En **Transacciones**, elija tipo, cuenta, monto y descripcion. El monto debe ser
mayor que cero. Un retiro no puede exceder el saldo. Al confirmar, el sistema
actualiza saldo, comprobante y asiento contable como una sola operacion.

## Aportaciones

Seleccione socio, tipo y monto. Las aportaciones pueden ser ordinarias o
extraordinarias. Los retiros respetan la permanencia minima definida por el
backend. El resumen siempre se calcula desde la base de datos.

## Creditos

1. Registre una solicitud para un socio.
2. GERENTE o ADMINISTRADOR aprueba o rechaza.
3. Al aprobar, consulte la tabla de amortizacion.
4. CAJERO o ADMINISTRADOR realiza el desembolso.
5. Registre pagos de cuota desde el detalle.

No se puede desembolsar un credito pendiente o rechazado.

## Contabilidad y reportes

**Libro Diario** permite filtrar y consultar asientos. Cada asiento mantiene
debito y credito por el mismo valor. En **Reportes** se consultan ahorros,
cartera, aportaciones y diario; los resultados se exportan a PDF o XLSX.

## Rol SOCIO

El socio puede consultar exclusivamente sus cuentas, movimientos y creditos
asociados al usuario autenticado. No puede administrar datos de terceros.

## Mensajes frecuentes

- **401**: la sesion expiro o no se inicio.
- **403**: el rol no tiene permiso.
- **404**: el registro solicitado no existe o no pertenece al usuario.
- **422**: revise los campos marcados por el formulario.
- **Saldo insuficiente**: reduzca el monto del retiro.

