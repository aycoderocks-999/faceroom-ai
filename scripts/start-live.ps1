# Start FaceRoom AI for live Vercel + tunneled backend
# Run this whenever you want the public Vercel site to work

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "=== FaceRoom AI Live Mode ===" -ForegroundColor Cyan

# Docker infra
Set-Location $Root
docker compose up -d postgres redis qdrant 2>$null

# Backend
$p = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty OwningProcess
if (-not $p) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root\backend'; .\venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000"
    Start-Sleep -Seconds 4
}

# Tunnel
Write-Host "Starting public tunnel (keep this window open)..." -ForegroundColor Green
npx --yes localtunnel --port 8000
