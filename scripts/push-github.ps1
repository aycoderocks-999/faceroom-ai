# Run AFTER: gh auth login
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "=== FaceRoom AI — GitHub Push ===" -ForegroundColor Cyan

gh auth status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not logged in. Run: gh auth login" -ForegroundColor Red
    exit 1
}

$repoName = "faceroom-ai"
$remote = git remote get-url origin 2>$null

if (-not $remote) {
    Write-Host "Creating public repo: $repoName" -ForegroundColor Green
    gh repo create $repoName --public --source=. --remote=origin --description "FaceRoom AI - Distributed Face Recognition & Event Photo Retrieval"
    git branch -M main
    git push -u origin main
} else {
    Write-Host "Pushing to existing remote: $remote" -ForegroundColor Green
    git branch -M main
    git push -u origin main
}

Write-Host ""
Write-Host "Done! Repo URL:" -ForegroundColor Green
gh repo view --web 2>$null
gh repo view --json url -q .url
