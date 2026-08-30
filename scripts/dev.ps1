# GrantFlow — spustenie lokálneho stacku (API + PWA)
# Použitie: .\scripts\dev.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

# Env
$AiEnv = Join-Path $Root "grantflow-ai\.env"
$AiEnvExample = Join-Path $Root "grantflow-ai\.env.example"
if (-not (Test-Path $AiEnv)) {
  Copy-Item $AiEnvExample $AiEnv
  Write-Host "Vytvorené grantflow-ai\.env"
}

$WebEnv = Join-Path $Root "web-app\.env.local"
$WebEnvExample = Join-Path $Root "web-app\.env.example"
if (-not (Test-Path $WebEnv)) {
  Copy-Item $WebEnvExample $WebEnv
  Write-Host "Vytvorené web-app\.env.local"
}

$Uvicorn = Join-Path $Root "grantflow-ai\.venv\Scripts\uvicorn.exe"
if (-not (Test-Path $Uvicorn)) {
  Write-Error "Chýba venv. Spusti: cd grantflow-ai; python -m venv .venv; .\.venv\Scripts\pip install -r requirements.txt"
}

Write-Host "API  → http://127.0.0.1:8001/docs"
Write-Host "PWA  → http://localhost:3000"
Write-Host ""

Start-Process pwsh -ArgumentList @(
  "-NoExit", "-NoLogo", "-Command",
  "Set-Location '$Root\grantflow-ai'; & '.\.venv\Scripts\uvicorn.exe' app.main:app --reload --port 8001"
)

Start-Process pwsh -ArgumentList @(
  "-NoExit", "-NoLogo", "-Command",
  "Set-Location '$Root\web-app'; npm run dev"
)
