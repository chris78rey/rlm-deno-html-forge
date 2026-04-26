# ⚙️ Configuración Explicada

**Guía detallada de cada bloque de configuración en config.yaml**

---

## Estructura del Archivo de Configuración

El archivo `config.yaml` (o `config.example.yaml`) contiene las siguientes secciones:

```yaml
paths:          # Rutas de directorios
theme:          # Temática y estilo
model:          # Configuración del modelo de IA
rlm:            # Parámetros de procesamiento
html:           # Parámetros de HTML
context:        # Contexto del documento
```

---

## 1. Sección: `paths`

Define las rutas de los directorios de trabajo.

```yaml
paths:
  input_dir: input_html/
  output_dir: output_html/
  reports_dir: reports/
```

### `input_dir`

**Ruta:** `input_html/`

**Descripción:** Carpeta donde se colocan los documentos HTML originales a procesar.

**Valor por defecto:** `input_html/`

**Notas:**
- Debe existir en el directorio raíz del proyecto
- Puede contener subcarpetas para organizar documentos
- Se procesarán todos los archivos `.html` y `.htm`

### `output_dir`

**Ruta:** `output_html/`

**Descripción:** Carpeta donde se guardan los documentos HTML transformados.

**Valor por defecto:** `output_html/`

**Notas:**
- Se crea automáticamente si no existe
- Mantiene la estructura de subcarpetas del `input_dir`
- Los archivos originales en `input_html` no se modifican

### `reports_dir`

**Ruta:** `reports/`

**Descripción:** Carpeta donde se generan los reportes de procesamiento.

**Valor por defecto:** `reports/`

**Archivos generados:**
- `report.html` - Vista visual completa
- `report.json` - Datos estructurados para programación
- `report.md` - Resumen en markdown

---

## 2. Sección: `theme`

Define la temática y estilo que se aplicará a los documentos.

```yaml
theme:
  new_theme: "Diseño corporativo profesional"
  style: "corporate"
```

### `new_theme`

**Tipo:** Texto

**Descripción:** Descripción de la temática que se aplicará a los documentos.

**Ejemplos:**
```yaml
new_theme: "Diseño corporativo profesional"
new_theme: "Estilo moderno minimalista"
new_theme: "Formato académico clásico"
new_theme: "Presentación ejecutiva elegante"
```

**Uso en el sistema:**
- Se incluye en el prompt del sistema para la IA
- Ayuda a la IA a entender el contexto deseado
- Influye en el tono y estilo del texto transformado

### `style`

**Tipo:** Texto (`corporate` | `modern` | `classic`)

**Descripción:** Estilo visual predefinido para la transformación.

**Opciones:**
- `corporate`: Colores sobrios, diseño limpio, profesional
- `modern`: Colores vibrantes, espacios amplios, tipografía actual
- `classic`: Colores neutros, tipografía serif, bordes elegantes

**Valor por defecto:** `corporate`

**Ejemplo completo:**
```yaml
theme:
  new_theme: "Documento corporativo para presentación ejecutiva"
  style: "corporate"
```

---

## 3. Sección: `model`

Define el modelo de IA que se utilizará para las transformaciones.

```yaml
model:
  name: "openrouter/auto"
  provider: "openrouter"
```

### `name`

**Tipo:** Texto

**Descripción:** Nombre del modelo de IA de OpenRouter.

**Valores comunes:**
- `openrouter/auto` - Modelo automático (mejor disponible)
- `anthropic/claude-3-sonnet` - Claude 3 Sonnet
- `anthropic/claude-3-haiku` - Claude 3 Haiku (más rápido)
- `openai/gpt-4-turbo` - GPT-4 Turbo
- `openai/gpt-3.5-turbo` - GPT-3.5 Turbo (más económico)

**Recomendaciones:**
- **Velocidad:** `claude-3-haiku` o `gpt-3.5-turbo`
- **Calidad:** `claude-3-sonnet` o `gpt-4-turbo`
- **Equilibrio:** `openrouter/auto`

### `provider`

**Tipo:** Texto

**Descripción:** Proveedor del servicio de IA.

**Valor actual:** `openrouter`

**Nota:** Actualmente solo se soporta OpenRouter como proveedor.

---

## 4. Sección: `rlm`

Parámetros de procesamiento que afectan velocidad, costos y calidad.

```yaml
rlm:
  concurrency: 6
  batch_size: 35
  max_depth: 10
  max_calls_per_subagent: 50
  max_total_calls: 1000
  max_money_spent: 10.0
  max_repair_attempts: 3
  max_same_error_repetitions: 3
  max_seconds_per_phase: 300
  input_cost_per_1m_tokens: 1.0
  output_cost_per_1m_tokens: 1.0
```

### `concurrency`

**Tipo:** Entero

**Descripción:** Número de llamadas paralelas a la API de IA.

**Valor por defecto:** `6`

**Impacto:**
- ✅ **Más alto:** Procesamiento más rápido
- ❌ **Más alto:** Mayor riesgo de rate limit
- ❌ **Más alto:** Más consumo de tokens simultáneo

**Recomendaciones:**
- `4-6` para uso normal
- `2-3` si tienes límites de API
- `8-10` si necesitas máxima velocidad (con cuenta con límites altos)

### `batch_size`

**Tipo:** Entero

**Descripción:** Número de fragmentos de texto por cada llamada a la IA.

**Valor por defecto:** `35`

**Impacto:**
- ✅ **Más alto:** Menos llamadas API (más económico)
- ❌ **Más alto:** Prompt más largo (puede exceder límites)
- ❌ **Más alto:** Mayor riesgo de error en la respuesta

**Ejemplo:**
```
Documento con 100 fragmentos:
batch_size = 35 → 3 llamadas API
batch_size = 10 → 10 llamadas API
```

**Recomendaciones:**
- `35` para uso general
- `20` si usas modelos con límites de contexto pequeños
- `50` si usas modelos con contexto grande

### `max_depth`

**Tipo:** Entero

**Descripción:** Profundidad máxima de recursión en el procesamiento.

**Valor por defecto:** `10`

**Uso:** Limita la profundidad de análisis de estructuras HTML anidadas.

### `max_calls_per_subagent`

**Tipo:** Entero

**Descripción:** Límite de llamadas por subproceso.

**Valor por defecto:** `50`

**Uso:** Previene bucles infinitos en un solo documento.

### `max_total_calls`

**Tipo:** Entero

**Descripción:** Límite total de llamadas API en toda la ejecución.

**Valor por defecto:** `1000`

**Uso:** Control de costos máximo.

### `max_money_spent`

**Tipo:** Float

**Descripción:** Límite máximo de dinero (USD) que se puede gastar.

**Valor por defecto:** `10.0`

**Uso:** Seguridad de costos. Si se supera, el proceso se detiene.

### `max_repair_attempts`

**Tipo:** Entero

**Descripción:** Número de intentos de reparación si falla un lote.

**Valor por defecto:** `3`

**Uso:** Reintentos automáticos ante errores transitorios.

### `max_same_error_repetitions`

**Tipo:** Entero

**Descripción:** Máximo de veces que un mismo error puede ocurrir.

**Valor por defecto:** `3`

**Uso:** Detección de errores persistentes.

### `max_seconds_per_phase`

**Tipo:** Entero

**Descripción:** Tiempo máximo (segundos) por fase de procesamiento.

**Valor por defecto:** `300` (5 minutos)

**Uso:** Timeout para evitar bloqueos eternos.

### `input_cost_per_1m_tokens`

**Tipo:** Float

**Descripción:** Costo por 1 millón de tokens de entrada (USD).

**Valor por defecto:** `1.0`

**Nota:** Depende del modelo utilizado. Ver tarifas de OpenRouter.

### `output_cost_per_1m_tokens`

**Tipo:** Float

**Descripción:** Costo por 1 millón de tokens de salida (USD).

**Valor por defecto:** `1.0`

**Nota:** Depende del modelo utilizado. Ver tarifas de OpenRouter.

---

## 5. Sección: `html`

Parámetros de procesamiento de HTML.

```yaml
html:
  min_text_length: 8
  max_text_length: 1500
```

### `min_text_length`

**Tipo:** Entero

**Descripción:** Longitud mínima de texto para ser procesado.

**Valor por defecto:** `8`

**Uso:** Ignora textos muy cortos (como etiquetas de botones, etc.)

**Ejemplo:**
- Texto "OK" (2 caracteres) → No se procesa
- Texto "Hola mundo" (11 caracteres) → Se procesa

### `max_text_length`

**Tipo:** Entero

**Descripción:** Longitud máxima de un fragmento de texto.

**Valor por defecto:** `1500`

**Uso:** Divide textos largos en fragmentos procesables.

**Importante:** Límite de contexto del modelo. Si el modelo soporta 4000 tokens, un fragmento de 1500 caracteres (~500-1000 tokens) es seguro.

---

## 6. Sección: `context`

Configuración del contexto del documento.

```yaml
context:
  file: "context/tema.md"
```

### `file`

**Tipo:** Texto (ruta)

**Descripción:** Ruta al archivo de contexto del documento.

**Valor por defecto:** `context/tema.md`

**Contenido del archivo:**
```markdown
# Contexto del Documento

Este documento es para la empresa XYZ.
Formato: Informe de necesidades.
Público: Directivos.
Tono: Profesional y formal.
```

**Uso:** El contenido se incluye en el prompt de la IA para proporcionar contexto específico.

---

## Ejemplo Completo de config.yaml

```yaml
# Rutas de directorios
paths:
  input_dir: input_html/
  output_dir: output_html/
  reports_dir: reports/

# Temática del documento
theme:
  new_theme: "Diseño corporativo profesional para informes ejecutivos"
  style: "corporate"

# Configuración del modelo de IA
model:
  name: "openrouter/auto"
  provider: "openrouter"

# Parámetros de procesamiento RLM
rlm:
  concurrency: 6              # Llamadas paralelas
  batch_size: 35              # Fragmentos por llamada
  max_depth: 10               # Profundidad máxima
  max_calls_per_subagent: 50  # Límite por subproceso
  max_total_calls: 1000       # Límite total
  max_money_spent: 10.0       # Límite de costos (USD)
  max_repair_attempts: 3      # Reintentos por error
  max_same_error_repetitions: 3  # Errores iguales
  max_seconds_per_phase: 300  # Timeout por fase
  input_cost_per_1m_tokens: 1.0   # Costo entrada
  output_cost_per_1m_tokens: 1.0  # Costo salida

# Parámetros de HTML
html:
  min_text_length: 8      # Texto mínimo a procesar
  max_text_length: 1500   # Texto máximo por fragmento

# Contexto del documento
context:
  file: "context/tema.md"
```

---

## Variables de Entorno (.env)

El archivo `.env` contiene secretos que NO deben subirse a Git:

```env
OPENROUTER_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

**Importante:** La API key se carga automáticamente con `load_dotenv()` en `main.py`.

---

## Recomendaciones por Tipo de Documento

### Documentos Corporativos

```yaml
theme:
  new_theme: "Diseño corporativo profesional"
  style: "corporate"

rlm:
  concurrency: 4
  batch_size: 30
```

### Documentos Modernos/Portafolios

```yaml
theme:
  new_theme: "Diseño moderno minimalista"
  style: "modern"

rlm:
  concurrency: 6
  batch_size: 40
```

### Documentos Académicos/Tesis

```yaml
theme:
  new_theme: "Formato académico clásico"
  style: "classic"

rlm:
  concurrency: 3
  batch_size: 25
```

### Procesamiento Rápido (Pruebas)

```yaml
rlm:
  concurrency: 8
  batch_size: 50
  max_total_calls: 100
```

### Procesamiento Económico

```yaml
model:
  name: "anthropic/claude-3-haiku"

rlm:
  concurrency: 2
  batch_size: 20
```

---

## Verificación de Configuración

Antes de ejecutar, verifica tu configuración:

```bash
# 1. Verificar config.yaml
cat config.yaml

# 2. Verificar .env (solo si es tu entorno local)
cat .env

# 3. Verificar contexto
cat context/tema.md

# 4. Verificar documentos de entrada
ls input_html/
```

---

**Documento creado:** 2026-04-26
**Referencia:** `config.example.yaml`
