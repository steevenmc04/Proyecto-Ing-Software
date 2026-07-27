param(
    [switch]$IncluirE2E
)

$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $PSScriptRoot
$PythonLocal = Join-Path $Raiz ".venv\Scripts\python.exe"
$Python = if (Test-Path -LiteralPath $PythonLocal) { $PythonLocal } else { "python" }

function Ejecutar {
    param([string]$Nombre, [scriptblock]$Comando)
    Write-Host "`n== $Nombre ==" -ForegroundColor Cyan
    & $Comando
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo la etapa: $Nombre"
    }
}

Push-Location $Raiz
try {
    Ejecutar "Lint backend" { & $Python -m ruff check app tests seed.py scripts }
    Ejecutar "Pruebas y cobertura backend" { & $Python -m pytest -q }

    Push-Location (Join-Path $Raiz "frontend")
    try {
        Ejecutar "Lint frontend" { npm run lint }
        Ejecutar "Pruebas frontend" { npm test }
        Ejecutar "Build frontend" { npm run build }
        if ($IncluirE2E) {
            Ejecutar "Pruebas E2E" { npm run test:e2e }
        }
    } finally {
        Pop-Location
    }
} finally {
    Pop-Location
}

Write-Host "`nVerificacion completada correctamente." -ForegroundColor Green
