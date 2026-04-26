#!/bin/bash

# Script para procesar documentos por categoría (Linux/Mac)
# Ejecutar desde la raíz del proyecto: bash scripts/procesar_por_categoria.sh

echo "=========================================="
echo "  RLM HTML Forge - Procesamiento por Categoría"
echo "=========================================="
echo ""

# Activar entorno virtual
echo "Activando entorno virtual..."
source .venv/bin/activate

# Verificar carpetas
carpetas=("corporativos" "modernos" "clasicos" "otros")
for carpeta in "${carpetas[@]}"; do
    ruta="input_html/$carpeta"
    if [ -d "$ruta" ]; then
        archivos=$(find "$ruta" -maxdepth 1 \( -name "*.html" -o -name "*.htm" \) 2>/dev/null | wc -l)
        if [ "$archivos" -gt 0 ]; then
            echo "📂 $carpeta: $archivos archivos"
        else
            echo "📂 $carpeta: vacía"
        fi
    fi
done

echo ""
echo "------------------------------------------"
echo ""

# Opciones de procesamiento
echo "¿Qué quieres procesar?"
echo "  1) Corporativos (config_corporate.yaml)"
echo "  2) Modernos (config_modern.yaml)"
echo "  3) Clásicos (config_classic.yaml)"
echo "  4) Todos los documentos (config_corporate.yaml)"
echo "  5) Personalizado (especificar config)"
echo ""

read -p "Selecciona una opción (1-5): " opcion

case $opcion in
    1)
        echo "⚙️  Procesando documentos corporativos..."
        python -m rlm_html_forge.main --config config/config_corporate.yaml
        ;;
    2)
        echo "⚙️  Procesando documentos modernos..."
        python -m rlm_html_forge.main --config config/config_modern.yaml
        ;;
    3)
        echo "⚙️  Procesando documentos clásicos..."
        python -m rlm_html_forge.main --config config/config_classic.yaml
        ;;
    4)
        echo "⚙️  Procesando todos los documentos con corporativo..."
        python -m rlm_html_forge.main --config config/config_corporate.yaml
        ;;
    5)
        read -p "Ruta del archivo config (ej: config/config_corporate.yaml): " config
        echo "⚙️  Procesando con $config..."
        python -m rlm_html_forge.main --config "$config"
        ;;
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "  ¡Procesamiento completado!"
echo "=========================================="
echo ""
echo "Resultados:"
echo "  📁 output_html/ - Documentos transformados"
echo "  📁 reports/ - Reportes generados"
echo ""
