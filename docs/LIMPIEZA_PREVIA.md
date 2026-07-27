# Limpieza previa

Fecha de inspeccion: 26 de julio de 2026.

## Estado inicial

- Rama: `main`.
- Remoto: `https://github.com/steevenmc04/Proyecto-Ing-Software.git`.
- Archivos rastreados: 190.
- Archivos no rastreados y no ignorados: ninguno.
- Arbol de trabajo: limpio.
- Duplicados exactos entre archivos rastreados: ninguno.
- Nombres rastreados con sufijos copia, backup, old o temp: ninguno.

## Candidatos

| Archivo o grupo | Tipo | Rastreado | Referenciado | Motivo | Accion propuesta |
|---|---|---:|---:|---|---|
| `.coverage` | Cobertura generada | No | No | Se regenera con Pytest | Eliminar |
| `.pytest_cache/` | Cache de pruebas | No | No | No forma parte del producto | Eliminar |
| `.ruff_cache/` | Cache de lint | No | No | Se regenera con Ruff | Eliminar |
| `**/__pycache__/` y `*.pyc` | Bytecode Python | No | No | Se regenera al importar | Eliminar |
| `frontend/dist/` | Build Vite | No | Montado por FastAPI si existe | Se reproduce con `npm run build` | Eliminar y regenerar solo para verificar |
| `frontend/playwright-report/` | Reporte E2E | No | No | Resultado local de Playwright | Eliminar |
| `frontend/test-results/` | Resultado E2E | No | No | Resultado local de Playwright | Eliminar |
| `e2e_caja_ahorros.db` | Base E2E | No | Si, como salida generada | `preparar_e2e.py` la crea desde cero | Eliminar |
| `test_caja_ahorros.db` | Base Pytest | No | Si, como salida generada | Las fixtures crean y eliminan tablas | Eliminar |
| `auditoria_caja.db` | Base de auditoria local | No | No | Copia local de 9 tablas y 33 filas sin consumidor | Eliminar |
| `debug_autorizacion.db` | Base de depuracion | No | No | Base vacia y sin referencias | Eliminar |
| `caja_ahorros_local.db` | Base local | No | No se encontro referencia textual | Puede contener datos de demostracion del usuario | Conservar |
| `.env` | Configuracion local | No | Cargado por Pydantic | Puede contener secretos necesarios para ejecutar | Conservar e ignorar |
| `frontend/node_modules/` | Dependencias instaladas | No | Requerido para ejecucion local | Se reproduce con `npm ci`, pero permite verificar y ejecutar ahora | Conservar e ignorar |
| `docs/evidencias/` | Evidencia academica | Si | README, informe y trazabilidad | Entregable obligatorio | Conservar |
| `docs/entrega/` | Informe final | Si | README e indice documental | Entregable obligatorio | Conservar |
| `T02_04_Grupo01_MartinezSteeven.docx` | Documento academico | Si | Entrega previa | Archivo institucional | Conservar |

## Tamano previo

- `frontend/node_modules/`: 267.730.819 bytes, se conserva localmente.
- Candidatos confirmados para eliminar: aproximadamente 2,7 MB.
- Ningun candidato confirmado esta rastreado por Git.

## Verificaciones antes de eliminar

- Se buscaron referencias por nombre de cada base.
- Se revisaron tablas y conteos sin mostrar registros.
- Se comprobaron hashes de las bases; no se asumio que fueran copias exactas.
- Se revisaron nombres sospechosos y hashes de los 190 archivos rastreados.
- No se encontraron duplicados exactos rastreados.

