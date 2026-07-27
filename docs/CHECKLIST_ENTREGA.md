# Checklist de entrega

## Repositorio

- [x] Se trabajo dentro del repositorio existente.
- [x] El historial supera 20 commits reales.
- [x] No se reescribio el historial.
- [x] `.env`, bases locales, `node_modules` y cobertura estan ignorados.
- [x] No se versionan claves ni tokens reales.
- [x] Se eliminaron artefactos de cobertura y la interfaz HTML obsoleta.

## Backend

- [x] FastAPI inicia localmente.
- [x] Arquitectura por capas conservada.
- [x] Salud, Swagger, ReDoc y OpenAPI disponibles.
- [x] Autenticacion JWT y usuario activo.
- [x] Autorizacion backend por roles.
- [x] Recursos del SOCIO filtrados por propietario.
- [x] CORS configurable.
- [x] Reglas financieras y rollback.
- [x] API externa protegida con `X-API-KEY`.
- [x] Pruebas y cobertura mayor al 70%.
- [x] Ruff sin errores.

## Frontend

- [x] React, Vite y TypeScript.
- [x] Login, cierre y expiracion de sesion.
- [x] Rutas y menu por rol.
- [x] Dashboard y modulos operativos.
- [x] Formularios conectados al backend real.
- [x] Estados de carga, vacio, exito y error.
- [x] Vista adaptable en escritorio y movil.
- [x] Exportacion PDF y XLSX.
- [x] Vitest y ESLint aprobados.
- [x] Build de produccion aprobado.
- [x] Doce flujos Playwright definidos y verificados.

## Documentacion

- [x] README principal.
- [x] Auditoria y plan.
- [x] AGENTS.md.
- [x] Arquitectura backend y frontend.
- [x] Contrato de 58 operaciones generado desde OpenAPI.
- [x] Matriz RF-001 a RF-022.
- [x] Plan de pruebas.
- [x] Manual de usuario y manual tecnico.
- [x] Tareas de seguimiento.
- [x] Guion de exposicion.
- [x] Evidencias visuales.
- [x] Informe final Markdown.
- [x] Informe PDF reproducible.

## Despliegue

- [x] Variables documentadas.
- [x] SQLite y MySQL Workbench documentados.
- [x] Scripts PowerShell de instalacion y ejecucion.
- [x] Build integrado servido por FastAPI.
- [x] GitHub Actions configurado.
- [ ] URL remota: no se proporciono proveedor ni credenciales; no se declara
      como desplegado.

## Riesgos aceptados

- [x] Ausencia de Alembic documentada.
- [x] Advertencias de Python 3.14 documentadas; CI usa Python 3.11.
- [x] Aviso de React Router limitado a RSC documentado; la SPA no usa RSC.

