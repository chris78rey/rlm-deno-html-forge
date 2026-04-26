# 📁 Estructura de Carpetas para Documentos

Guía completa para organizar tus documentos HTML en el sistema.

---

## 🗂️ Estructura Recomendada

```
rlm-deno-html-forge/
├── input_html/
│   ├── corporativos/       # Documentos profesionales/empresariales
│   │   ├── documento1.html
│   │   ├── documento2.html
│   │   └── ...
│   ├── modernos/           # Documentos modernos/minimalistas
│   │   ├── documento3.html
│   │   ├── documento4.html
│   │   └── ...
│   ├── clasicos/           # Documentos clásicos/elegantes
│   │   ├── documento5.html
│   │   ├── documento6.html
│   │   └── ...
│   └── otros/              # Documentos varios
│       ├── documento7.html
│       └── ...
│   └── .gitkeep
├── config/                 # Configuraciones por temática
│   ├── config_corporate.yaml
│   ├── config_modern.yaml
│   └── config_classic.yaml
├── output_html/            # Resultados (automático)
├── reports/                # Reportes (automático)
└── scripts/
    ├── procesar_por_categoria.ps1    # Windows
    └── procesar_por_categoria.sh     # Linux/Mac
```

---

## 📂 Descripción de Carpetas

### `input_html/corporativos/`
- **Para:** Documentos profesionales, informes empresariales, presentaciones ejecutivas
- **Temática:** Colores sobrios, diseño limpio y profesional
- **Ejemplos:** Informes financieros, presentaciones corporativas, documentos legales

### `input_html/modernos/`
- **Para:** Documentos con diseño actual, minimalista
- **Temática:** Colores vibrantes, espacios amplios, tipografía moderna
- **Ejemplos:** Portafolios, proyectos creativos, documentos de startup

### `input_html/clasicos/**
- **Para:** Documentos formales, tradicionales
- **Temática:** Colores neutros, tipografía serif, bordes elegantes
- **Ejemplos:** Tesis, trabajos académicos, documentos formales

### `input_html/otros/`
- **Para:** Documentos que no encajan en las categorías anteriores
- **Temática:** Personalizada según necesidad

---

## 🚀 Cómo Usar

### Paso 1: Organiza tus 10 documentos

**Windows PowerShell:**
```powershell
# Ejemplo: mover documentos a carpetas
move-item "documento1.html" input_html\corporativos\
move-item "documento2.html" input_html\corporativos\
move-item "documento3.html" input_html\modernos\
# ... etc
```

**Linux/Mac:**
```bash
# Ejemplo: mover documentos a carpetas
mv documento1.html input_html/corporativos/
mv documento2.html input_html/corporativos/
mv documento3.html input_html/modernos/
# ... etc
```

### Paso 2: Ejecutar procesamiento

**Opción A: Script interactivo (recomendado)**

```powershell
# Windows
.\scripts\procesar_por_categoria.ps1
```

```bash
# Linux/Mac
bash scripts/procesar_por_categoria.sh
```

**Opción B: Comando directo**

```powershell
# Windows - Procesar corporativos
python -m rlm_html_forge.main --config config/config_corporate.yaml

# Windows - Procesar modernos
python -m rlm_html_forge.main --config config/config_modern.yaml

# Windows - Procesar clásicos
python -m rlm_html_forge.main --config config/config_classic.yaml
```

```bash
# Linux/Mac - Procesar corporativos
python -m rlm_html_forge.main --config config/config_corporate.yaml

# Linux/Mac - Procesar modernos
python -m rlm_html_forge.main --config config/config_modern.yaml

# Linux/Mac - Procesar clásicos
python -m rlm_html_forge.main --config config/config_classic.yaml
```

---

## 📊 Resultados del Procesamiento

Después de ejecutar, verás:

```
output_html/
├── corporativos/
│   ├── documento1.html    # ✅ Procesado
│   └── documento2.html    # ✅ Procesado
├── modernos/
│   ├── documento3.html    # ✅ Procesado
│   └── documento4.html    # ✅ Procesado
├── clasicos/
│   ├── documento5.html    # ✅ Procesado
│   └── documento6.html    # ✅ Procesado
└── otros/
    └── documento7.html    # ✅ Procesado

reports/
├── report.html
├── report.json
└── report.md
```

---

## 🎯 Ejemplo Práctico con 10 Documentos

Supongamos que tienes estos 10 documentos:

```
1. informe_financiero_2024.html     → corporativos/
2. balance_general.html              → corporativos/
3. reporte_ventas.html               → corporativos/
4. presentacion_startup.html         → modernos/
5. portafolio_diseno.html            → modernos/
6. proyecto_innovacion.html          → modernos/
7. tesis_universidad.html            → clasicos/
8. trabajo_investigacion.html        → clasicos/
9. documento_legal.html              → otros/
10. otro_documento.html              → otros/
```

**Procesamiento:**

```powershell
# 1. Procesar corporativos (3 documentos)
python -m rlm_html_forge.main --config config/config_corporate.yaml

# 2. Procesar modernos (3 documentos)
python -m rlm_html_forge.main --config config/config_modern.yaml

# 3. Procesar clásicos (2 documentos)
python -m rlm_html_forge.main --config config/config_classic.yaml

# 4. Procesar otros (2 documentos) - usando config corporativo como default
python -m rlm_html_forge.main --config config/config_corporate.yaml
```

---

## 📋 Resumen Rápido

| Categoría | Temática | Archivo Config | Comando |
|-----------|----------|----------------|---------|
| Corporativos | Profesional | `config_corporate.yaml` | `python -m rlm_html_forge.main --config config/config_corporate.yaml` |
| Modernos | Minimalista | `config_modern.yaml` | `python -m rlm_html_forge.main --config config/config_modern.yaml` |
| Clásicos | Elegante | `config_classic.yaml` | `python -m rlm_html_forge.main --config config/config_classic.yaml` |

---

## 💡 Consejos

1. **Organiza primero:** Coloca todos los documentos en las carpetas correctas antes de ejecutar
2. **Procesa por lotes:** Procesa una categoría a la vez para controlar el tiempo
3. **Revisa resultados:** Después de cada lote, verifica los documentos en `output_html/`
4. **Ajusta si es necesario:** Si un documento necesita temática diferente, muévelo a otra carpeta y re-procesa

---

**¡Tu sistema está listo para manejar 10+ documentos organizados!** ✅
