$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $PSScriptRoot
$Entorno = Join-Path $Raiz ".venv"
$Python = Join-Path $Entorno "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    python -m venv $Entorno
}

& $Python -m pip install --upgrade pip
& $Python -m pip install -r (Join-Path $Raiz "requirements.txt")

Push-Location (Join-Path $Raiz "frontend")
try {
    npm ci
} finally {
    Pop-Location
}

Write-Host "Instalacion completada." -ForegroundColor Green
