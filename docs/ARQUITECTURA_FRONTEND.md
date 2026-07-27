# Arquitectura frontend

## Estructura

```text
frontend/src/
|-- componentes/
|   |-- comunes/Interfaz.tsx
|   `-- navegacion/LayoutPrincipal.tsx
|-- contextos/
|   |-- AutenticacionContexto.tsx
|   `-- EstadoAutenticacion.ts
|-- modulos/
|   |-- autenticacion/
|   |-- inicio/
|   |-- usuarios/
|   |-- socios/
|   |-- cuentas/
|   |-- transacciones/
|   |-- aportaciones/
|   |-- creditos/
|   |-- contabilidad/
|   `-- reportes/
|-- rutas/RutaProtegida.tsx
|-- servicios/clienteApi.ts
|-- tipos/dominio.ts
|-- utilidades/
|-- pruebas/
|-- App.tsx
`-- main.tsx
```

## Flujo de autenticacion

1. Login envia el contrato real `{nombre_usuario, contrasena}`.
2. El JWT se guarda en `sessionStorage`.
3. El proveedor recupera `/auth/me`.
4. El cliente adjunta `Authorization: Bearer`.
5. Una respuesta 401 elimina el token y emite `sesion-vencida`.
6. `RutaProtegida` controla sesion y roles.
7. El menu filtra opciones con el mismo mapa de roles visible.

El backend vuelve a validar cada operacion.

## Cliente HTTP

`clienteApi.ts` centraliza URL, JSON, token, cancelacion y errores. Normaliza
fallos de red y detalles FastAPI para evitar codigo repetido en pantallas.

## Modulos

Cada modulo consulta datos reales, administra estado de carga, error, vacio y
confirmacion. Los formularios de login, usuario y socio usan React Hook Form y
Zod; las operaciones financieras aplican validaciones inmediatas y el backend
repite las reglas.

## Diseno responsivo

- Barra lateral persistente en escritorio.
- Menu superpuesto y control accesible en movil.
- Tablas dentro de contenedores con desplazamiento horizontal.
- Dimensiones estables para botones, indicadores y paneles.
- Estados comunicados con texto y color.
- Moneda `es-EC` en USD y fechas coherentes.

## Exportacion

Los exportadores PDF y XLSX se cargan de forma dinamica al solicitarlos. Esto
mantiene el paquete principal en 388.38 kB y evita cargar bibliotecas de reporte
durante el login o las operaciones.

## Pruebas

- Vitest y Testing Library: login, validaciones, permisos y cliente HTTP.
- Playwright: doce flujos sobre base SQLite aislada.
- Capturas: escritorio y movil en `docs/evidencias`.
