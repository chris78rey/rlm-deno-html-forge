# Ejecutar desde la raíz del proyecto antes de subirlo a GitHub público.

Write-Host "Preparando repositorio público..." -ForegroundColor Cyan

# Crear archivos locales desde ejemplos si no existen.
if (!(Test-Path "config.yaml") -and (Test-Path "config.example.yaml")) {
  Copy-Item "config.example.yaml" "config.yaml"
}

if (!(Test-Path "context")) {
  New-Item -ItemType Directory "context" | Out-Null
}

if (!(Test-Path "context/tema.md") -and (Test-Path "context/tema.example.md")) {
  Copy-Item "context/tema.example.md" "context/tema.md"
}

# Asegurar carpetas vacías versionables.
foreach ($dir in @("input_html", "output_html", "reports", ".work")) {
  if (!(Test-Path $dir)) { New-Item -ItemType Directory $dir | Out-Null }
  $gitkeep = Join-Path $dir ".gitkeep"
  if (!(Test-Path $gitkeep)) { New-Item -ItemType File $gitkeep | Out-Null }
}

Write-Host "Si estos archivos ya estaban trackeados, se retirarán del índice Git." -ForegroundColor Yellow
git rm -r --cached input_html output_html reports .work 2>$null
git rm --cached config.yaml 2>$null
git rm --cached context/tema.md 2>$null
git rm --cached .env 2>$null

Write-Host "Listo. Revisa con: git status" -ForegroundColor Green
