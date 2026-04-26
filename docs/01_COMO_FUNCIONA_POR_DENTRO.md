# 🔧 Cómo Funciona por Dentro - Flujo Interno Detallado

**Documentación técnica del funcionamiento interno del proyecto**

---

## Visión General del Flujo

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. INICIO: Python carga configuración y contexto                    │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. EXTRACCIÓN: Deno/Pyodide analiza HTML en input_html/             │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. PREPARACIÓN: Python agrupa elementos en lotes para procesar      │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 4. PROCESAMIENTO IA: OpenRouter transforma el texto por lotes       │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 5. REENSAMBLADO: Deno aplica transformaciones al HTML               │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 6. GUARDADO: Python escribe HTML transformado y reportes            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Paso 1: Inicio y Carga de Configuración

### 1.1 Punto de Entrada (main.py)

```python
# main.py
def main() -> None:
    load_dotenv()                          # Carga .env con API keys
    args = parse_args()                    # Lee argumentos CLI
    config = AppConfig.from_yaml(args.config)  # Carga config.yaml
    asyncio.run(HtmlRLMOrchestrator(config).run())
```

**Qué ocurre:**
- Se cargan las variables de entorno (API key de OpenRouter)
- Se lee el archivo de configuración (`config.yaml` por defecto)
- Se crea el objeto `HtmlRLMOrchestrator` con toda la configuración

### 1.2 Inicialización del Orquestador (orchestrator.py)

```python
class HtmlRLMOrchestrator:
    def __init__(self, config: AppConfig):
        self.config = config
        self.deno = DenoSandbox(config)         # Sandbox Deno
        self.client = OpenRouterClient(config)  # Cliente API
        self.guard = LoopGuard(...)             # Protección contra bucles
```

**Componentes inicializados:**
- `DenoSandbox`: Interfaz con Deno/Pyodide para procesamiento HTML
- `OpenRouterClient`: Cliente para llamadas a la API de OpenRouter
- `LoopGuard`: Sistema de seguridad para evitar bucles infinitos y costos excesivos

---

## Paso 2: Extracción de HTML (Deno/Pyodide)

### 2.1 Ejecución del Sandbox

```python
# orchestrator.py
print("Extrayendo estructura HTML dentro de Deno/Pyodide...")
manifest = await self.deno.extract()
documents = manifest.get("documents", [])
```

**Proceso interno en Deno/Pyodide:**

```
deno/pyodide_runner.ts
    │
    ▼
Carga Pyodide (Python en WASM)
    │
    ▼
Escanea input_html/
    │
    ▼
Analiza estructura HTML
    │
    ▼
Detecta elementos de texto:
  - <p>...</p>
  - <span>...</span>
  - <h1>...</h1>, <h2>...</h2>, etc.
  - Texto en atributos (alt, title)
    │
    ▼
Genera "manifest" con lista de documentos y targets
    │
    ▼
Devuelve a Python
```

**Estructura del manifest:**

```json
{
  "documents": [
    {
      "path": "input_html/documento1.html",
      "targets": [
        {
          "id": "text_001",
          "kind": "text",
          "tag": "p",
          "original": "Texto original aquí",
          "path_hint": "body > div > p:nth-child(2)"
        },
        // ... más targets
      ]
    }
  ]
}
```

### 2.2 ¿Qué es un "target"?

Un **target** es un fragmento de texto en el HTML que será transformado:

```html
<!-- HTML Original -->
<p>Hola mundo</p>

<!-- Target detectado -->
{
  "id": "text_001",
  "kind": "text",
  "original": "Hola mundo"
}
```

---

## Paso 3: Preparación de Lotes (Batching)

### 3.1 Agrupación de Targets

```python
# orchestrator.py
all_batches = []

for doc in documents:
    source_path = doc["path"]
    targets = doc.get("targets", [])
    for batch in chunked(targets, self.config.rlm.batch_size):
        all_batches.append((source_path, batch))
```

**¿Por qué lotes?**
- Llamadas individuales a IA son lentas y costosas
- Agrupar múltiples fragmentos en una llamada mejora eficiencia
- `batch_size` (por defecto: 35) controla cuántos fragmentos por llamada

**Ejemplo:**

```
Documento con 100 targets
batch_size = 35
→ 3 lotes: [35, 35, 30] targets
→ 3 llamadas a OpenRouter (no 100)
```

### 3.2 Preparación del Prompt

```python
# Prepara items reducidos para enviar a IA
reduced_items = [
    {
        "id": t["id"],
        "kind": t["kind"],
        "tag": t.get("tag"),
        "attribute": t.get("attr"),
        "path_hint": t.get("path_hint"),
        "original": t.get("original"),
    }
    for t in batch
]
```

**Estructura enviada a IA:**

```json
{
  "items": [
    {
      "id": "text_001",
      "kind": "text",
      "tag": "p",
      "original": "Texto original"
    },
    // ... hasta 35 items
  ]
}
```

**NO se envía:**
- ❌ HTML completo
- ❌ Estructura del documento
- ❌ Otros fragmentos no relacionados

---

## Paso 4: Procesamiento con IA (OpenRouter)

### 4.1 Llamada a la API

```python
# orchestrator.py
sys_prompt = system_prompt(self.config)

async def process_batch(batch_index, source_path, batch):
    data, llm_resp = await self.client.chat_json(
        sys_prompt,                    # Prompt del sistema (contexto)
        batch_prompt(reduced_items, self.config),  # Fragmentos a procesar
    )
```

**Prompt del Sistema (system_prompt):**
- Incluye `context/tema.md` (instrucciones específicas)
- Define estilo y temática deseada
- Instrucciones sobre cómo reescribir el texto

**Prompt de Fragmentos (batch_prompt):**
- Lista de fragmentos de texto originales
- Cada fragmento con su ID y contexto

### 4.2 Respuesta de la IA

La IA devuelve transformaciones sugeridas:

```json
{
  "items": [
    {
      "id": "text_001",
      "replacement": "Hola mundo transformado"
    },
    {
      "id": "text_002",
      "replacement": "Otro texto transformado"
    },
    // ... (una respuesta por cada item del batch)
  ]
}
```

### 4.3 Registro de Llamadas (LoopGuard)

```python
self.guard.register_call(
    f"subagent:{self.config.model.model}",
    llm_resp.input_tokens,
    llm_resp.output_tokens,
)
```

**Control de costos y seguridad:**
- Límite de llamadas totales
- Límite de tokens consumidos
- Límite de dinero gastado
- Detección de errores repetidos

### 4.4 Limpieza del Texto

```python
replacement = clean_visible_spanish_text(str(item.get("replacement", "")))
```

La función `clean_visible_spanish_text`:
- Normaliza espacios y saltos de línea
- Limpia caracteres especiales no visibles
- Mantiene el texto limpio para inyección en HTML

---

## Paso 5: Reensamblado del HTML

### 5.1 Ensamblar Todos los Documentos

```python
# orchestrator.py
print("Ensamblando todos los HTML en una sola llamada a Deno...")
assembled = await self.deno.assemble_many(documents, dict(replacements_by_file))
```

**Proceso en Deno/Pyodide:**

```
Recibe:
  - Lista de documentos
  - Diccionario de reemplazos por archivo y ID
    │
    ▼
Para cada documento:
  1. Abre el HTML original
  2. Busca cada target por su ID/path_hint
  3. Reemplaza el texto original por la transformación
  4. Mantiene toda la estructura HTML intacta
    │
    ▼
Devuelve HTML transformados
```

**Ejemplo de reemplazo:**

```
HTML Original:
  <p id="text_001">Hola mundo</p>

Reemplazo:
  {"text_001": "Saludos, universo"}

HTML Resultante:
  <p id="text_001">Saludos, universo</p>
```

### 5.2 ¿Cómo se identifican los targets?

Deno usa **path_hint** o **ID** para localizar exactamente dónde reemplazar:

```html
<!-- Path hint: body > div > p:nth-child(2) -->
<!-- O ID único: id="text_001" -->
<p id="text_001">Texto original</p>
```

---

## Paso 6: Guardado y Reportes

### 6.1 Escribir HTML Transformados

```python
for doc in documents:
    source_path = doc["path"]
    output_path = Path(self.config.paths.output_dir) / Path(source_path).name
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(assembled[source_path])
```

**Ubicación:**
- `input_html/documento.html` → `output_html/documento.html`

### 6.2 Generar Reportes

```python
# Reporte HTML
file_report = FileReport(
    filename=Path(source_path).name,
    status="completado" if not errors else "con_errores",
    replacements=len(replacements_by_file[source_path]),
    errors=errors_by_file[source_path],
)
file_reports.append(file_report)

# Reporte consolidado
new_report(file_reports, reports_dir)
```

**Reportes generados:**
- `reports/report.html` - Vista visual de todo el proceso
- `reports/report.json` - Datos estructurados para programación
- `reports/report.md` - Resumen legible

---

## Resumen del Flujo Completo

```
┌─────────────────────────────────────────────────────────────────────┐
│ FLUJO COMPLETO: Python + Deno + IA                                  │
└─────────────────────────────────────────────────────────────────────┘

1. Python (main.py)
   ├─ Carga .env (API key)
   ├─ Lee config.yaml
   └─ Inicia orchestrator

2. Deno/Pyodide (pyodide_runner.ts)
   ├─ Escanea input_html/
   ├─ Extrae todos los fragmentos de texto
   └─ Devuelve manifest con targets

3. Python (orchestrator.py)
   ├─ Agrupa targets en lotes (batch_size)
   ├─ Prepara prompts para IA
   └─ Inicia procesamiento paralelo

4. OpenRouter (API)
   ├─ Recibe prompt con contexto
   ├─ Transforma fragmentos de texto
   └─ Devuelve reemplazos

5. Python (orchestrator.py)
   ├─ Guarda reemplazos por ID
   ├─ Controla límites (LoopGuard)
   └─ Aguarda finalización de todos los lotes

6. Deno/Pyodide (pyodide_runner.ts)
   ├─ Recibe documentos y reemplazos
   ├─ Aplica transformaciones al HTML
   └─ Devuelve HTML transformados

7. Python (orchestrator.py)
   ├─ Escribe HTML en output_html/
   ├─ Genera reportes en reports/
   └─ Finaliza proceso
```

---

## Puntos Clave del Flujo

| Paso | Responsable | Qué hace |
|------|-------------|----------|
| 1 | Python | Carga configuración y contexto |
| 2 | Deno/Pyodide | Extrae texto del HTML |
| 3 | Python | Agrupa en lotes para procesamiento |
| 4 | OpenRouter | Transforma el texto |
| 5 | Deno/Pyodide | Reconstruye el HTML |
| 6 | Python | Guarda resultados y reportes |

---

## Seguridad en Cada Paso

1. **Extracción**: Solo texto visible, sin estructura HTML
2. **Lotes**: Fragmentos pequeños, sin contexto completo
3. **IA**: Nunca recibe el HTML completo
4. **Reensamblado**: Operación local, sin salida de datos
5. **Guardado**: Solo archivos finales en output_html/

---

**Documento creado:** 2026-04-26
**Referencia:** `src/rlm_html_forge/orchestrator.py`
