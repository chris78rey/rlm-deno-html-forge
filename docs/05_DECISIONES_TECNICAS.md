# 🏗️ Decisiones Técnicas

**Documentación de decisiones de arquitectura y diseño del proyecto**

---

## 1. Introducción

Este documento explica las decisiones técnicas tomadas durante el desarrollo del proyecto, las alternativas consideradas y las razones de la selección final.

---

## 2. Arquitectura Híbrida: Python + Deno

### 2.1 Decisión

Usar **Python** como orquestador principal y **Deno** como sandbox de ejecución.

### 2.2 Alternativas Consideradas

| Alternativa | Ventajas | Desventajas |
|-------------|----------|-------------|
| Solo Python | Más simple, una sola base de código | Menor seguridad, código ejecutado sin sandbox |
| Solo Node.js | Un solo runtime | Menor ecosistema para procesamiento científico |
| Python + Docker | Aislamiento completo | Más pesado, más complejo de configurar |
| Python + Deno | ✅ Seguridad + ecosistema Python | Requiere dos runtimes |

### 2.3 Por Qué Python + Deno

#### Python (Orquestador)
- ✅ **Ecosistema rico:** Librerías para procesamiento de archivos, API calls, async/await
- ✅ **Pydantic:** Validación de configuración robusta
- ✅ **AsyncIO:** Procesamiento paralelo eficiente
- ✅ **Reportes:** Generación de HTML, JSON, Markdown

#### Deno (Sandbox)
- ✅ **Seguridad:** Permiso explícito por recurso (read-only)
- ✅ **TypeScript nativo:** Código más mantenible
- ✅ **Pyodide:** Python en WASM dentro de Deno
- ✅ **Aislamiento:** Código no puede acceder a sistema sin permisos

### 2.4 Flujo de Trabajo

```
Python (orquestador)
    │
    ├─ Carga configuración
    ├─ Lee archivos de entrada
    ├─ Prepara prompts para IA
    ├─ Llama a Deno para extracción
    ├─ Llama a OpenRouter para transformación
    ├─ Llama a Deno para reensamblado
    ├─ Guarda resultados
    └─ Genera reportes

Deno (sandbox)
    │
    ├─ Extrae texto de HTML (Pyodide)
    ├─ Reconstruye HTML con reemplazos
    └─ NUNCA envía datos a internet
```

---

## 3. Uso de OpenRouter

### 3.1 Decisión

Usar **OpenRouter** como proveedor de modelos de IA.

### 3.2 Alternativas Consideradas

| Proveedor | Ventajas | Desventajas |
|-----------|----------|-------------|
| OpenAI API | Modelo potente, bien documentado | Solo modelos OpenAI, costoso |
| Anthropic API | Claude potente, buen contexto | Solo modelos Anthropic |
| Local LLM | Privacidad total, sin costo por llamada | Requiere hardware potente, complejo |
| OpenRouter | ✅ Múltiples modelos, unified API | Depende de servicio externo |

### 3.3 Por Qué OpenRouter

#### Múltiples Modelos
- ✅ Acceso a Claude, GPT, Llama, Mistral, etc.
- ✅ Puede cambiar modelo sin cambiar código
- ✅ Fallback automático entre modelos

#### Unified API
- ✅ Una sola API para múltiples proveedores
- ✅ Simplicidad en el código
- ✅ Fácil de cambiar de proveedor

#### Costos
- ✅ Precios transparentes por modelo
- ✅ Control de gastos configurado
- ✅ Sin costo fijo mensual

### 3.4 Arquitectura del Cliente

```python
class OpenRouterClient:
    def __init__(self, config):
        self.api_key = os.environ["OPENROUTER_API_KEY"]
        self.model = config.model.name
    
    async def chat_json(self, system_prompt, user_prompt):
        # Llama a OpenRouter
        # Retorna datos estructurados JSON
```

**Ventajas:**
- ✅ Reutilizable para cualquier modelo
- ✅ Manejo de errores centralizado
- ✅ Logging de uso

---

## 4. Procesamiento por Lotes (Batching)

### 4.1 Decisión

Agrupar fragmentos de texto en lotes para procesamiento eficiente.

### 4.2 Alternativas Consideradas

| Enfoque | Ventajas | Desventajas |
|---------|----------|-------------|
| Procesar todo junto | Una sola llamada | Prompt muy largo, límites de contexto |
| Procesar uno por uno | Simple, controlado | Muchas llamadas, lento, costoso |
| **Batching** | ✅ Balance costo/velocidad | Requiere lógica de agrupación |

### 4.3 Cómo Funciona el Batching

```python
# Fragmentos detectados
fragmentos = [f1, f2, f3, ..., f100]

# Agrupación en lotes de 35
batch_size = 35
batches = [
    [f1, f2, ..., f35],      # Lote 1
    [f36, f37, ..., f70],    # Lote 2
    [f71, f72, ..., f100]    # Lote 3
]

# Procesamiento paralelo
async def process_batch(batch):
    return await client.chat_json(...)

# 3 llamadas en paralelo (no 100)
```

### 4.4 Ventajas

| Aspecto | Sin Batching | Con Batching (35) |
|---------|--------------|-------------------|
| Llamadas API | 100 | 3 |
| Tiempo | 100x | 3x |
| Costo | 100% | ~15% |
| Límite de contexto | Riesgo alto | Controlado |

### 4.5 Configuración

```yaml
rlm:
  batch_size: 35  # Fragmentos por lote
  concurrency: 6  # Lotes simultáneos
```

---

## 5. Seguridad del Sandbox

### 5.1 Decisión

Usar Deno con permisos restringidos para ejecutar código de procesamiento.

### 5.2 Alternativas Consideradas

| Enfoque | Seguridad | Complejidad |
|---------|-----------|-------------|
| Ejecutar directamente | Baja | Baja |
| Docker | Alta | Alta |
| Deno con permisos | ✅ Alta | Media |

### 5.3 Permisos Implementados

```bash
deno run \
  --deny-net \              # ❌ No internet
  --no-prompt \             # ❌ Sin interacción
  --cached-only \           # ❌ Sin descargas
  --allow-read=rutas \      # ✅ Solo lectura
  deno/pyodide_runner.ts
```

### 5.4 Por Qué Estos Permisos

| Permiso | Razón | Seguridad |
|---------|-------|-----------|
| `--deny-net` | Nunca enviar datos externos | ✅ Máxima |
| `--allow-read` | Leer HTML de entrada | ✅ Controlado |
| `--no-prompt` | Sin interacción manual | ✅ Automatizado |
| `--cached-only` | Sin descargas nuevas | ✅ Aislado |

### 5.5 Límites Adicionales

```python
# En el orquestador
self.guard = LoopGuard(
    max_depth=10,                    # Profundidad máxima
    max_calls_per_subagent=50,       # Límite por proceso
    max_total_calls=1000,            # Límite total
    max_money_spent=10.0,            # Límite de costos
)
```

---

## 6. Extracción con Pyodide

### 6.1 Decisión

Usar Pyodide (Python en WASM) dentro de Deno para procesar HTML.

### 6.2 Alternativas Consideradas

| Enfoque | Ventajas | Desventajas |
|---------|----------|-------------|
| Regex puro | Simple, rápido | Limitado, frágil |
| JavaScript puro | Nativo en Deno | Menos librerías |
| Beautiful Soup (Python) | Potente, flexible | No disponible en Deno |
| **Pyodide** | ✅ Python en Deno | +150ms carga inicial |

### 6.3 Cómo Funciona

```
Deno
  ├─ Inicializa Pyodide (WASM)
  ├─ Pyodide carga Python 3.x
  ├─ Usa Beautiful Soup en Python
  ├─ Extrae texto de HTML
  └─ Devuelve a Deno → Python
```

### 6.4 Ventajas de Pyodide

- ✅ Acceso a librerías Python completas
- ✅ Beautiful Soup para análisis HTML
- ✅ Código Python mantenible
- ✅ Aislado dentro del sandbox

### 6.5 Costo de Inicialización

```typescript
// Primera ejecución: ~150ms
const pyodide = await loadPyodide();

// Ejecuciones posteriores: ~10ms
// (usando caché de Deno)
```

---

## 7. Sistema de Reportes

### 7.1 Decisión

Generar múltiples formatos de reporte (HTML, JSON, Markdown).

### 7.2 Formatos Implementados

| Formato | Propósito | Ventajas |
|---------|-----------|----------|
| **HTML** | Vista visual | Fácil de leer, formato completo |
| **JSON** | Datos estructurados | Fácil de procesar programáticamente |
| **Markdown** | Documentación | Legible en GitHub, fácil de compartir |

### 7.3 Estructura del Reporte

```python
class FileReport:
    filename: str          # Nombre del archivo
    status: str            # completado / con_errores
    replacements: int      # Número de reemplazos
    errors: list[str]      # Lista de errores
    duration: float        # Tiempo de procesamiento
```

### 7.4 Ventajas

- ✅ **Debugging:** Reporte HTML ayuda a diagnosticar problemas
- ✅ **Integración:** JSON permite integración con otros sistemas
- ✅ **Documentación:** Markdown es legible en GitHub
- ✅ **Auditoría:** Histórico de procesamientos

---

## 8. LoopGuard (Sistema de Seguridad)

### 8.1 Decisión

Implementar sistema de límites para prevenir costos excesivos y bucles infinitos.

### 8.2 Límites Implementados

| Límite | Valor | Propósito |
|--------|-------|-----------|
| `max_depth` | 10 | Evitar recursión infinita |
| `max_calls_per_subagent` | 50 | Límite por proceso |
| `max_total_calls` | 1000 | Límite global |
| `max_money_spent` | $10.00 | Límite de costos |
| `max_repair_attempts` | 3 | Reintentos por error |
| `max_same_error` | 3 | Detección de errores persistentes |
| `max_seconds_per_phase` | 300 | Timeout por fase |

### 8.3 Implementación

```python
class LoopGuard:
    def check_depth(self, depth):
        if depth > self.max_depth:
            raise LoopGuardError("Profundidad excedida")
    
    def register_call(self, model, input_tokens, output_tokens):
        self.total_calls += 1
        self.total_tokens += input_tokens + output_tokens
        self.total_cost += calculate_cost(...)
        
        if self.total_cost > self.max_money_spent:
            raise LoopGuardError("Costo máximo excedido")
```

### 8.4 Ventajas

- ✅ Protege contra errores de configuración
- ✅ Previene costos inesperados
- ✅ Detecta bucles infinitos
- ✅ Proporciona logs de diagnóstico

---

## 9. Manejo de Configuración

### 9.1 Decisión

Separar configuración de código usando archivos YAML y variables de entorno.

### 9.2 Estructura de Configuración

```
config.yaml          # Configuración del proyecto (no subido)
config.example.yaml  # Ejemplo para otros usuarios (sí subido)
.env                 # Secretos (no subido)
.env.example         # Ejemplo de secretos (sí subido)
```

### 9.3 Ventajas

| Aspecto | Con configuración separada | Hardcoded |
|---------|---------------------------|-----------|
| Flexibilidad | ✅ Cambiar sin recompilar | ❌ Requiere código |
| Seguridad | ✅ Secretos en .env | ❌ Secretos en código |
| Colaboración | ✅ Cada usuario su configuración | ❌ Conflictos de configuración |
| Despliegue | ✅ Fácil en diferentes entornos | ❌ Complejo |

### 9.4 Validación con Pydantic

```python
class AppConfig(BaseModel):
    paths: PathsConfig
    theme: ThemeConfig
    model: ModelConfig
    rlm: RLMConfig
    html: HTMLConfig
    context: ContextConfig
    
    @classmethod
    def from_yaml(cls, path: str):
        # Carga y valida configuración
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)
```

**Ventajas:**
- ✅ Validación automática de tipos
- ✅ Valores por defecto
- ✅ Mensajes de error claros
- ✅ Documentación integrada

---

## 10. Procesamiento Asíncrono

### 10.1 Decisión

Usar `asyncio` para procesamiento paralelo de lotes.

### 10.2 Alternativas Consideradas

| Enfoque | Ventajas | Desventajas |
|---------|----------|-------------|
| Síncrono | Simple, fácil de entender | Lento, no aprovecha paralelismo |
| Multiprocessing | Paralelo real | Más memoria, complejidad |
| **AsyncIO** | ✅ Eficiente, nativo Python | Requiere entender async |

### 10.3 Implementación

```python
async def process_batch(batch_index, source_path, batch):
    async with semaphore:  # Controla concurrencia
        # Llamada a IA
        data = await client.chat_json(...)
        return data

# Ejecutar múltiples lotes en paralelo
tasks = [
    process_batch(i, source, batch)
    for i, (source, batch) in enumerate(all_batches)
]

for fut in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
    await fut
```

### 10.4 Ventajas

| Métrica | Síncrono | AsyncIO |
|---------|----------|---------|
| Tiempo (10 lotes) | 10t | ~2t (concurrency=5) |
| Uso de CPU | Bajo | Alto |
| Complejidad | Baja | Media |

---

## 11. Estructura de Carpetas

### 11.1 Decisión

Organización modular por funcionalidad.

```
src/rlm_html_forge/
├── main.py              # Punto de entrada
├── orchestrator.py      # Orquestador principal
├── config.py            # Configuración y validación
├── deno_sandbox.py      # Interfaz con Deno
├── openrouter_client.py # Cliente API
├── loop_guard.py        # Sistema de seguridad
├── prompts.py           # Prompts para IA
├── reporting.py         # Generación de reportes
├── text_cleaner.py      # Limpieza de texto
└── utils.py             # Funciones utilitarias
```

### 11.2 Principios

| Principio | Aplicación |
|-----------|------------|
| **Separación de responsabilidades** | Cada módulo tiene un solo propósito |
| **DRY (Don't Repeat Yourself)** | Funciones utilitarias en `utils.py` |
| **KISS (Keep It Simple)** | Módulos pequeños y enfocados |
| **YAGNI (You Ain't Gonna Need It)** | Solo implementar lo necesario |

---

## 12. Manejo de Errores

### 12.1 Decisión

Sistema de manejo de errores con reintentos y logging.

### 12.2 Estrategias

| Estrategia | Implementación |
|------------|----------------|
| **Reintentos** | `max_repair_attempts` (3) |
| **Timeout** | `max_seconds_per_phase` (300s) |
| **Logging** | Reportes en HTML, JSON, Markdown |
| **Validación** | Pydantic para configuración |

### 12.3 Flujo de Error

```
Error detectado
    │
    ├─ ¿Reintentable? ── Sí ──> Reintentar (hasta max_repair_attempts)
    │
    ├─ ¿Timeout? ── Sí ──> Reportar y continuar
    │
    └─ Error permanente ──> Reportar y marcar documento
```

### 12.4 Ventajas

- ✅ Robustez ante errores transitorios
- ✅ Visibilidad completa con reportes
- ✅ No bloquea proceso completo por un error

---

## 13. Comparativa con Alternativas

### 13.1 Enfoque Actual vs. Alternativas

| Característica | Este Proyecto | Solo Python | Solo Node.js | Docker + Python |
|----------------|---------------|-------------|--------------|-----------------|
| Seguridad sandbox | ✅ Alta (Deno) | ⚠️ Media | ⚠️ Media | ✅ Alta |
| Ecosistema Python | ✅ Completo | ✅ Completo | ❌ Limitado | ✅ Completo |
| Simplicidad | ⚠️ Media | ✅ Alta | ⚠️ Media | ❌ Baja |
| Rendimiento | ✅ Bueno | ✅ Bueno | ✅ Bueno | ⚠️ Overhead |
| Aislamiento | ✅ Bueno | ⚠️ Básico | ⚠️ Básico | ✅ Excelente |
| Configuración | ⚠️ Media | ✅ Simple | ✅ Simple | ❌ Compleja |

### 13.2 Conclusión

El enfoque **Python + Deno** ofrece el mejor balance entre:
- ✅ Seguridad (sandbox aislado)
- ✅ Ecosistema (librerías Python)
- ✅ Simplicidad (API unificada)
- ✅ Rendimiento (procesamiento paralelo)

---

## 14. Decisiones Futuras

### 14.1 Mejoras Potenciales

| Mejora | Impacto | Prioridad |
|--------|---------|-----------|
| Cache de resultados | Reducir costos | Media |
| Soporte múltiples formatos | PDF, DOCX | Baja |
| Interfaz web | UX mejorada | Media |
| Plugin VS Code | Integración IDE | Baja |
| Batch processing offline | Sin internet | Alta |

### 14.2 Consideraciones Técnicas Futuras

1. **Cache de respuestas IA**
   - Almacenar respuestas de fragmentos repetidos
   - Reducir costos y tiempo

2. **Modelos locales**
   - Opcionalmente usar LLMs locales
   - Máxima privacidad

3. **Procesamiento por carpetas**
   - Configurar diferentes temáticas por carpeta
   - Procesamiento automatizado

---

## 15. Referencias y Recursos

### 15.1 Tecnologías

- **Python 3.11+:** https://www.python.org/
- **Deno 2.x:** https://deno.land/
- **Pyodide:** https://pyodide.org/
- **OpenRouter:** https://openrouter.ai/
- **Pydantic:** https://docs.pydantic.dev/

### 15.2 Librerías

| Librería | Uso |
|----------|-----|
| `asyncio` | Procesamiento asíncrono |
| `pydantic` | Validación de configuración |
| `tqdm` | Barras de progreso |
| `beautifulsoup4` | Análisis HTML (en Pyodide) |
| `python-dotenv` | Variables de entorno |

---

**Documento creado:** 2026-04-26
**Revisión:** 1.0
