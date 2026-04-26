# Script para procesar documentos por categoría
# Ejecutar desde la raíz del proyecto

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  RLM HTML Forge - Procesamiento por Categoría" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
.venv\Scripts\activate

# Verificar carpetas
$carpetas = @("corporativos", "modernos", "clasicos", "otros")
foreach ($carpeta in $carpetas) {
    $ruta = "input_html\$carpeta"
    if (Test-Path $ruta) {
        $archivos = Get-ChildItem $ruta -Filter "*.html", "*.htm" -ErrorAction SilentlyContinue
        if ($archivos) {
            Write-Host "📂 $carpeta: $($archivos.Count) archivos" -ForegroundColor Green
        } else {
            Write-Host "📂 $carpeta: vacía" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "------------------------------------------" -ForegroundColor Gray

# Opciones de procesamiento
Write-Host ""
Write-Host "¿Qué quieres procesar?" -ForegroundColor Yellow
Write-Host "  1) Corporativos (config_corporate.yaml)" -ForegroundColor White
Write-Host "  2) Modernos (config_modern.yaml)" -ForegroundColor White
Write-Host "  3) Clásicos (config_classic.yaml)" -ForegroundColor White
Write-Host "  4) Todos los documentos (config_corporate.yaml)" -ForegroundColor White
Write-Host "  5) Personalizado (especificar config)" -ForegroundColor White
Write-Host ""

$opcion = Read-Host "Selecciona una opción (1-5)"

switch ($opcion) {
    "1" {
        Write-Host "⚙️  Procesando documentos corporativos..." -ForegroundColor Cyan
        Write-Host "python -m rlm_html_forge.main --config config/config_corporate.yaml" -ForegroundColor Gray
        python -m rlm_html_forge.main --config config/config_corporate.yaml
    }
    "2" {
        Write-Host "⚙️  Procesando documentos modernos..." -ForegroundColor Cyan
        Write-Host "python -m rlm_html_forge.main --config config/config_modern.yaml" -ForegroundColor Gray
        python -m rlm_html_forge.main --config config/config_modern.yaml
    }
    "3" {
        Write-Host "⚙️  Procesando documentos clásicos..." -ForegroundColor Cyan
        Write-Host "python -m rlm_html_forge.main --config config/config_classic.yaml" -ForegroundColor Gray
        python -m rlm_html_forge.main --config config/config_classic.yaml
    }
    "4" {
        Write-Host "⚙️  Procesando todos los documentos con corporativo..." -ForegroundColor Cyan
        Write-Host "python -m rlm_html_forge.main --config config/config_corporate.yaml" -ForegroundColor Gray
        python -m rlm_html_forge.main --config config/config_corporate.yaml
    }
    "5" {
        $config = Read-Host "Ruta del archivo config (ej: config/config_corporate.yaml)"
        Write-Host "⚙️  Procesando con $config..." -ForegroundColor Cyan
        python -m rlm_html_forge.main --config $config
    }
    default {
        Write-Host "❌ Opción no válida" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  ¡Procesamiento completado!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Resultados:" -ForegroundColor Yellow
Write-Host "  📁 output_html/ - Documentos transformados" -ForegroundColor White
Write-Host "  📁 reports/ - Reportes generados" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Gray
Read-Host
