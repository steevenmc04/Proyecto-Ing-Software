# Plan Del Proyecto Final

## Fase 1. Auditoria Y Control

- Registrar estado real del repositorio.
- Conservar cambios locales existentes.
- Documentar riesgos, brechas y prioridades.
- Crear `AGENTS.md`.

Verificacion:

```powershell
git status --short --branch
pytest -q
```

## Fase 2. Backend Seguro

- Agregar `/api/v1/salud`.
- Configurar CORS mediante variables de entorno.
- Crear dependencias de autenticacion y autorizacion por roles.
- Proteger cada endpoint segun el dominio.
- Eliminar secretos y credenciales de la interfaz publica.
- Corregir reglas financieras y rollback.
- Agregar pruebas de regresion.

Verificacion:

```powershell
ruff check app tests
pytest -q
```

## Fase 3. Frontend Base

- Crear React, Vite y TypeScript en `frontend/`.
- Configurar React Router.
- Crear cliente HTTP centralizado.
- Implementar autenticacion y rutas protegidas.
- Crear layout responsivo con menu por rol.

Verificacion:

```powershell
cd frontend
npm run lint
npm run test
npm run build
```

## Fase 4. Modulos Funcionales

- Dashboard.
- Usuarios.
- Socios.
- Cuentas.
- Depositos y retiros.
- Aportaciones.
- Creditos y amortizacion.
- Libro Diario.
- Reportes y exportacion.

Cada modulo debe consumir endpoints reales y mostrar carga, vacio, error y
confirmacion.

## Fase 5. Calidad Y Automatizacion

- Pruebas de componentes y servicios.
- Pruebas E2E de flujos criticos.
- Scripts PowerShell.
- GitHub Actions integral.
- Cobertura backend minima 70%, objetivo 80%.

## Fase 6. Documentacion Y Evidencias

- Contrato API.
- Arquitectura completa y frontend.
- Matriz de trazabilidad.
- Plan de pruebas.
- Manuales.
- Tareas.
- Guion de exposicion.
- Checklist.
- Capturas reales.
- Informe Markdown y PDF reproducible.

## Fase 7. Cierre

- Instalacion limpia.
- Pruebas y builds.
- Revision de secretos y temporales.
- Revision de Git.
- Commits pequenos por trabajo real.
- Push solo con todas las verificaciones aprobadas.
