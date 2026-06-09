# Step 1: Login (opens browser) — you do this once
# Step 2: Push repo automatically

Write-Host "Step 1: Log in to GitHub (browser will open)..." -ForegroundColor Cyan
gh auth login -h github.com -p https -w

if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "`nStep 2: Pushing code..." -ForegroundColor Cyan
& "$PSScriptRoot\push-github.ps1"
