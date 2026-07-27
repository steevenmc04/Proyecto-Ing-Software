param(
    [switch]$SinRecarga
)

$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $PSScriptRoot
$PythonLocal = Join-Path $Raiz ".venv\Scripts\python.exe"
$Python = if (Test-Path -LiteralPath $PythonLocal) { $PythonLocal } else { "python" }

Push-Location $Raiz
try {
    if ($SinRecarga) {
        & $Python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
    } else {
        & $Python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
    }
} finally {
    Pop-Location
}
