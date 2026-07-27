# Limpieza realizada

Fecha: 26 de julio de 2026.

## Resumen

La limpieza se realizo exclusivamente sobre archivos ignorados y reproducibles.
No se elimino codigo, configuracion compartida, dependencias declaradas,
pruebas, documentacion, evidencias ni entregables academicos.

Tamano retirado respecto al inventario inicial: **2.863.731 bytes
(aproximadamente 2,73 MiB)**.

## Elementos eliminados

| Archivo o grupo | Rastreado | Motivo | Verificacion previa | Impacto esperado |
|---|---:|---|---|---|
| `.coverage` | No | Resultado generado | Pytest lo regenera | Ninguno |
| `.pytest_cache/` | No | Cache de Pytest | No contiene pruebas | Ninguno |
| `.ruff_cache/` | No | Cache de Ruff | Ruff lo regenera | Ninguno |
| 16 carpetas `__pycache__/` | No | Bytecode Python | Los `.py` originales estan rastreados | Ninguno |
| `frontend/dist/` | No | Build Vite | `npm run build` aprobado | Se regenera al compilar |
| `frontend/playwright-report/` | No | Reporte local E2E | No esta enlazado como evidencia | Ninguno |
| `frontend/test-results/` | No | Estado local E2E | Playwright lo regenera | Ninguno |
| `e2e_caja_ahorros.db` | No | Base E2E | `preparar_e2e.py` la crea desde cero | Ninguno |
| `test_caja_ahorros.db` | No | Base Pytest | Fixtures crean las tablas | Ninguno |
| `auditoria_caja.db` | No | Base temporal sin referencias | Busqueda por nombre y revision de esquema | Ninguno |
| `debug_autorizacion.db` | No | Base vacia sin referencias | Cero tablas y cero consumidores | Ninguno |

Los resultados de la verificacion volvieron a generar caches, build, reportes y
bases de prueba. Estos artefactos se eliminaron nuevamente despues de comprobar
que todas las pruebas habian aprobado.

## Elementos conservados

| Elemento | Motivo |
|---|---|
| `.env` | Configuracion local potencialmente sensible; permanece ignorada |
| `caja_ahorros_local.db` | Puede contener datos de demostracion del usuario |
| `frontend/node_modules/` | Dependencias locales para ejecucion inmediata; no se versiona |
| `docs/evidencias/` | Evidencia academica obligatoria |
| `docs/entrega/` | Informe final Markdown y PDF |
| `T02_04_Grupo01_MartinezSteeven.docx` | Documento academico |

Durante la revision final se detecto que el documento DOCX no estaba en el
directorio de trabajo. Se recupero exclusivamente ese archivo desde `HEAD` y se
comprobo que su blob Git coincide exactamente con
`eb12e3c54b195225ae84b5a5731ade0735ab55f7`. No se restauro ningun otro cambio.

## Duplicados

- Duplicados exactos rastreados: ninguno.
- Archivos rastreados con sufijos de copia o backup: ninguno.
- Duplicados eliminados: ninguno.

## Gitignore

Se reorganizaron y completaron reglas para:

- Python, caches y cobertura.
- Node, Vite, TypeScript, build y Playwright.
- `.env` y archivos de claves locales.
- SQLite y archivos WAL/SHM.
- logs de npm, yarn y pnpm.
- Windows, macOS, editores y archivos temporales.

`.env.example`, `frontend/.env.example`, lockfiles, pruebas, documentos,
evidencias y PDF final siguen rastreables.

## Verificacion posterior

| Comando o comprobacion | Resultado |
|---|---|
| `npm ci` | 272 paquetes instalados desde lockfile |
| Ruff | Aprobado |
| Pytest | 38 pruebas aprobadas |
| Cobertura backend | 83,31%, umbral 80% |
| ESLint | Aprobado |
| Vitest | 8 pruebas aprobadas |
| TypeScript y Vite | Build aprobado, 2.174 modulos |
| Playwright | 12 flujos E2E aprobados |
| `GET /` | 200 |
| `GET /docs` | 200 |
| `GET /redoc` | 200 |
| `GET /openapi.json` | 200 |
| `GET /api/v1/salud` | 200 y estado correcto |
| `npm run dev` | Vite 8.1.5 inicio; `/login` respondio 200 |

## Limitaciones no relacionadas con la limpieza

- `npm audit` informa dos avisos altos del modo RSC de React Router. La SPA no
  utiliza RSC ni acciones de servidor.
- Python 3.14 muestra advertencias de deprecacion internas de FastAPI/Starlette;
  CI usa Python 3.11.
