# FaceRoom AI — one-shot cloud deploy helper
# Prerequisite: run `gh auth login` and `vercel login` once in your browser first.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "=== FaceRoom AI Cloud Deploy ===" -ForegroundColor Cyan

# 1. GitHub
$ghOk = $false
try { gh auth status 2>$null; $ghOk = $true } catch {}
if (-not $ghOk) {
    Write-Host "GitHub not logged in. Run: gh auth login" -ForegroundColor Yellow
    gh auth login
}

if (-not (git remote get-url origin 2>$null)) {
    $repoName = Read-Host "GitHub repo name (e.g. faceroom-ai)"
    gh repo create $repoName --public --source=. --remote=origin --push
} else {
    git push -u origin HEAD
}

# 2. Vercel frontend
Write-Host "`nDeploying frontend to Vercel..." -ForegroundColor Green
Set-Location "$Root\frontend"
if (-not $env:VITE_API_URL) {
    $env:VITE_API_URL = Read-Host "Render API URL (e.g. https://faceroom-api.onrender.com/api/v1)"
}
vercel --prod --yes

Write-Host "`n=== Done ===" -ForegroundColor Green
Write-Host "Next: deploy backend + worker on Render using docs/DEPLOYMENT.md"
Write-Host "Set Supabase, Qdrant, Upstash env vars in Render dashboard."
