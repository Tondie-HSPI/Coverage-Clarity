$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendRoot = Join-Path $projectRoot "backend"
$pythonPath = Join-Path $projectRoot "..\\venv\\Scripts\\python.exe"

if (-not (Test-Path $pythonPath)) {
    $pythonPath = "C:\\Users\\tondr\\OneDrive\\Documents\\business_helper_ai\\venv\\Scripts\\python.exe"
}

if (-not (Test-Path $pythonPath)) {
    throw "Python virtual environment not found. Install backend requirements in a venv and update start-backend.ps1."
}

Set-Location $backendRoot
& $pythonPath -m uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
