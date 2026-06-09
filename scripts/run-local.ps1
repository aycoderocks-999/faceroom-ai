# FaceRoom AI — local Windows startup (no Docker required for basic mode)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "=== FaceRoom AI Local Startup ===" -ForegroundColor Cyan

# Backend venv
$venvPython = Join-Path $Root "backend\venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Creating Python virtual environment..."
    python -m venv (Join-Path $Root "backend\venv")
    & (Join-Path $Root "backend\venv\Scripts\pip.exe") install -r (Join-Path $Root "backend\requirements-base.txt")
}

# Init DB
Push-Location (Join-Path $Root "backend")
$env:DATABASE_URL = "sqlite:///./faceroom.db"
& $venvPython -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine); print('Database ready')"
Pop-Location

# Frontend deps
if (-not (Test-Path (Join-Path $Root "frontend\node_modules"))) {
    Write-Host "Installing frontend dependencies..."
    Push-Location (Join-Path $Root "frontend")
    npm install
    Pop-Location
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Green
Write-Host "  API:      http://localhost:8000" 
Write-Host "  Docs:     http://localhost:8000/docs"
Write-Host "  Frontend: http://localhost:5173"
Write-Host ""
Write-Host "Note: Face AI requires Redis + Celery worker + Qdrant (use Docker for full stack)"
Write-Host "Press Ctrl+C in each terminal to stop."
Write-Host ""

# Start backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root\backend'; `$env:DATABASE_URL='sqlite:///./faceroom.db'; .\venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 3

# Start frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root\frontend'; npm run dev"

Write-Host "Services launched in separate windows." -ForegroundColor Green
