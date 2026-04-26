# Manual de Uso - RLM Deno HTML Forge

**Sistema de procesamiento HTML seguro con Python + Deno**

---

## 📋 ¿Qué hace este sistema?

Transforma documentos HTML usando inteligencia artificial, pero **sin exponer tu HTML completo**:

- ✅ Extrae solo texto del HTML
- ✅ Envía texto al modelo de IA (OpenRouter)
- ✅ Recibe transformaciones sugeridas
- ✅ Aplica cambios localmente

**Resultado:** HTML con nueva temática manteniendo la estructura original.

---

## 🛠️ Requisitos Previos

Antes de empezar, necesitas:

| Requisito | Versión mínima | Cómo verificar |
|-----------|---------------|----------------|
| Python | 3.11+ | `python --version` |
| Deno | 2.x+ | `deno --version` |
| API Key OpenRouter | Cuenta activa | [openrouter.ai](https://openrouter.ai) |

### 🔑 Obtener API Key de OpenRouter

1. Ve a [openrouter.ai](https://openrouter.ai)
2. Inicia sesión o crea cuenta
3. Ve a **Settings** → **Keys**
4. Genera una nueva API key
5. **Cópiala** (no la compartas)

---

## 📥 Instalación Rápida

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/chris78rey/rlm-deno-html-forge.git
cd rlm-deno-html-forge
```

### Paso 2: Configurar entorno Python

```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Paso 3: Configurar variables de entorno

```powershell
# Windows - copiar ejemplo a archivo real
copy .env.example .env
```

```bash
# Linux/Mac
cp .env.example .env
```

Luego edita el archivo `.env` y pon tu API key:

```env
OPENROUTER_API_KEY=tu_api_key_aqui
```

### Paso 4: Preparar caché de Deno (una sola vez)

```bash
deno cache deno/pyodide_runner.ts
```

---

## 📂 Estructura de Carpetas

```
rlm-deno-html-forge/
├── input_html/      # ← Coloca aquí tus HTML a procesar
├── output_html/     # ← Aquí aparecerán los resultados
├── reports/         # ← Reportes de procesamiento
├── context/         # ← Archivos de contexto del proyecto
└── config.yaml      # ← Configuración del sistema
```

---

## 🚀 Uso Básico

### Paso 1: Preparar documentos

Coloca tus archivos HTML en la carpeta `input_html/`:

```
input_html/
├── mi_documento.html
├── otro_documento.htm
└── ...
```

### Paso 2: Configurar la temática

Edita `config.yaml`:

```yaml
theme:
  new_theme: "Tema profesional para documento corporativo"
```

También puedes configurar:

```yaml
theme:
  new_theme: "Tema moderno y minimalista"
  style: "corporate"  # corporate | modern | classic
```

### Paso 3: Ejecutar el procesamiento

```powershell
# Windows PowerShell
python -m rlm_html_forge.main --config config.yaml
```

```bash
# Linux/Mac
python -m rlm_html_forge.main --config config.yaml
```

### Paso 4: Ver resultados

Los archivos procesados aparecerán en:

- **`output_html/`** - HTML transformados
- **`reports/report.html`** - Reporte detallado
- **`reports/report.json`** - Datos en formato JSON

---

## 📝 Ejemplos Prácticos

### Ejemplo 1: Procesar un solo documento

```powershell
# 1. Copiar ejemplo a input_html/
copy examples\documento_ejemplo.html input_html\

# 2. Configurar
echo "theme:
  new_theme: 'Diseño para presentación ejecutiva'" > config.yaml

# 3. Ejecutar
python -m rlm_html_forge.main --config config.yaml
```

### Ejemplo 2: Procesar múltiples documentos

Si tienes varios HTML en `input_html/`, todos se procesarán automáticamente:

```
input_html/
├── documento1.html
├── documento2.html
├── documento3.html
└── ...
```

Simplemente ejecuta:

```bash
python -m rlm_html_forge.main --config config.yaml
```

### Ejemplo 3: Cambiar tema para diferente uso

**Para documento corporativo:**

```yaml
theme:
  new_theme: "Diseño corporativo profesional"
  style: "corporate"
```

**Para documento moderno:**

```yaml
theme:
  new_theme: "Diseño moderno minimalista"
  style: "modern"
```

**Para documento clásico:**

```yaml
theme:
  new_theme: "Diseño clásico elegante"
  style: "classic"
```

---

## ⚙️ Archivos de Configuración

### `.env` - Variables de entorno

```env
OPENROUTER_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

**Importante:** Nunca subas este archivo a GitHub.

### `config.yaml` - Configuración del sistema

```yaml
theme:
  new_theme: "Tema para documento específico"
  style: "corporate"  # Opciones: corporate, modern, classic

# Opcional: configuración avanzada
processing:
  max_retries: 3
  timeout: 300
```

### `context/tema.md` - Contexto adicional

Puedes añadir información de contexto sobre tu documento:

```markdown
Este documento es para la empresa XYZ,
con formato de informe de necesidades.
El público objetivo son directivos.
```

---

## 📊 Reportes Generados

### Reporte HTML (`reports/report.html`)

Vista visual completa del proceso con:

- Documentos procesados
- Resumen de transformaciones
- Estado de cada archivo

### Reporte JSON (`reports/report.json`)

Datos estructurados para integración:

```json
{
  "fecha": "2026-04-26T10:30:00",
  "documentos": [
    {
      "nombre": "documento1.html",
      "estado": "completado",
      "transformaciones": 5
    }
  ]
}
```

### Reporte Markdown (`reports/report.md`)

Versión legible para compartir con equipos.

---

## 🔧 Solución de Problemas Comunes

### Problema: "No se reconoce 'python'"

**Solución:**
```powershell
# Usar python3 en Linux/Mac
python3 -m rlm_html_forge.main --config config.yaml
```

### Problema: "API key no válida"

**Solución:**
1. Verifica que la API key esté bien copiada en `.env`
2. Asegúrate de que la cuenta de OpenRouter tenga saldo
3. Regenera la API key si es necesario

### Problema: "Deno no está en PATH"

**Solución:**
```powershell
# Windows: reinstalar Deno
# Descargar desde: https://deno.land/install
```

### Problema: "Archivos HTML no encontrados"

**Solución:**
1. Verifica que los archivos estén en `input_html/`
2. Asegúrate de que sean archivos `.html` o `.htm`
3. Ejecuta `ls input_html/` (o `dir input_html` en Windows)

### Problema: "Pyodide no cargado"

**Solución:**
```bash
# Ejecutar nuevamente la cache
deno cache deno/pyodide_runner.ts
```

---

## 🎯 Flujo de Trabajo Recomendado

```
1. Preparar documentos HTML
   └── Colocar en input_html/

2. Configurar temática
   └── Editar config.yaml

3. Ejecutar procesamiento
   └── python -m rlm_html_forge.main --config config.yaml

4. Revisar resultados
   └── Ver output_html/ y reports/

5. Ajustar si es necesario
   └── Modificar config.yaml y repetir
```

---

## ⚠️ Importante: Seguridad

- ✅ El HTML completo **NUNCA** se envía a la IA
- ✅ Solo se envían fragmentos de texto para transformación
- ✅ Todo el procesamiento ocurre localmente
- ✅ La IA solo recibe metadatos mínimos

---

## 📞 Soporte

Si tienes problemas:

1. Revisa el `README.md` para información técnica
2. Verifica la estructura en `README_GITHUB_PUBLICO.md`
3. Revisa los reportes generados en `reports/`

---

**Sistema listo para usar** ✅
