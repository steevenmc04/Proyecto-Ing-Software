$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $PSScriptRoot

Push-Location (Join-Path $Raiz "frontend")
try {
    npm run dev -- --host 127.0.0.1 --port 5173
} finally {
    Pop-Location
}
