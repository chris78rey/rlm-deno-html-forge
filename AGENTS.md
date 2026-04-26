# 🤖 AGENTS.md - Guía para Agentes de IA

**Documento de contexto para agentes de IA (ChatGPT, Copilot, Codex, etc.)**

**Propósito:** Ayudar a cualquier agente de IA a entender rápidamente el proyecto y trabajar con él eficientemente.

---

## 1. Información Básica del Proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | RLM Deno HTML Forge |
| **Lenguaje principal** | Python 3.11+ |
| **Framework** | Deno 2.x + Pyodide |
| **API de IA** | OpenRouter |
| **Propósito** | Transformar HTML usando IA sin exponer el HTML completo |

---

## 2. Estructura del Proyecto

```
rlm-deno-html-forge/
├── src/rlm_html_forge/         # Código Python
│   ├── main.py                 # ✅ Punto de entrada principal
│   ├── orchestrator.py         # ✅ Orquestador principal
│   ├── deno_sandbox.py         # ✅ Interfaz con Deno
│   ├── openrouter_client.py    # ✅ Cliente API
│   ├── config.py               # ✅ Configuración
│   ├── prompts.py              # ✅ Prompts para IA
│   ├── reporting.py            # ✅ Generación de reportes
│   └── ...
├── deno/
│   └── pyodide_runner.ts       # ✅ Sandbox Deno/Pyodide
├── input_html/                 # 📁 Tus documentos HTML
├── output_html/                # 📁 Resultados generados
├── reports/                    # 📁 Reportes
├── config.yaml                 # ⚙️ Configuración (local)
├── .env                        # 🔐 Secretos (no subir a Git)
└── docs/                       # 📚 Documentación
```

---

## 3. Comandos Principales

### 3.1 Ejecución del Proyecto

```bash
# Activar entorno virtual
source .venv/bin/activate          # Linux/Mac
.venv\Scripts\activate             # Windows

# Ejecutar procesamiento
python -m rlm_html_forge.main --config config.yaml
```

### 3.2 Verificación del Entorno

```bash
# Verificar versiones
python --version          # Python 3.11+
deno --version            # Deno 2.x

# Verificar dependencias
pip list
deno info deno/pyodide_runner.ts
```

### 3.3 Gestión de Git

```bash
# Ver estado
git status

# Commit y push
git add .
git commit -m "Mensaje"
git push
```

---

## 4. Archivos de Entrada y Salida

### 4.1 Entradas (Input)

| Ruta | Contenido |
|------|-----------|
| `input_html/` | Documentos HTML originales a transformar |
| `config.yaml` | Configuración del proyecto |
| `context/tema.md` | Contexto e instrucciones específicas |
| `.env` | API key de OpenRouter (secreto) |

### 4.2 Salidas (Output)

| Ruta | Contenido |
|------|-----------|
| `output_html/` | Documentos HTML transformados |
| `reports/report.html` | Reporte visual del proceso |
| `reports/report.json` | Reporte estructurado (datos) |
| `reports/report.md` | Reporte en markdown |

---

## 5. Flujo de Trabajo

### Paso a Paso para un Agente

```
1. LEER configuración
   ├── Cargar config.yaml
   ├── Cargar context/tema.md
   └── Cargar .env (API key)

2. ANALIZAR documentos HTML
   ├── Escanear input_html/
   ├── Extraer fragmentos de texto
   └── Generar lista de targets

3. PREPARAR procesamiento
   ├── Agrupar targets en lotes
   ├── Preparar prompts para IA
   └── Configurar límites de seguridad

4. PROCESAR con IA
   ├── Enviar lotes a OpenRouter
   ├── Recibir transformaciones
   └── Validar respuestas

5. REENSAMBLAR HTML
   ├── Aplicar reemplazos
   ├── Mantener estructura original
   └── Generar documentos finales

6. GUARDAR resultados
   ├── Escribir output_html/
   ├── Generar reportes
   └── Limpiar temporales
```

---

## 6. Configuración (config.yaml)

### 6.1 Estructura del Archivo

```yaml
paths:
  input_dir: input_html/
  output_dir: output_html/
  reports_dir: reports/

theme:
  new_theme: "Tema del documento"
  style: "corporate"  # corporate | modern | classic

model:
  name: "openrouter/auto"
  provider: "openrouter"

rlm:
  concurrency: 6      # Llamadas paralelas a IA
  batch_size: 35      # Fragmentos por llamada
  max_depth: 10       # Profundidad máxima
  max_calls_per_subagent: 50
  max_total_calls: 1000
  max_money_spent: 10.0  # USD límite

html:
  min_text_length: 8
  max_text_length: 1500

context:
  file: "context/tema.md"
```

### 6.2 Parámetros Críticos

| Parámetro | Valor por defecto | Impacto |
|-----------|-------------------|---------|
| `rlm.concurrency` | 6 | Más alto = más rápido, pero más costoso |
| `rlm.batch_size` | 35 | Más alto = menos llamadas, prompt más largo |
| `html.min_text_length` | 8 | Ignora textos más cortos |
| `html.max_text_length` | 1500 | Límite por fragmento |

---

## 7. Seguridad y Privacidad

### 7.1 Qué NO debe subirse a Git

```bash
# ❌ NUNCA subir estos archivos
.env                    # API keys y secretos
config.yaml             # Configuración local
context/tema.md         # Contenido real del documento
input_html/*.htm        # Documentos originales
output_html/            # Resultados
reports/                # Reportes
.work/                  # Temporales
```

### 7.2 Cómo se protege el HTML

```
HTML Completo → Extraído localmente → Solo texto → IA → Reemplazos → HTML Transformado
     ❌                ✅                  ✅         ✅      ✅            ✅
  NO sale        Se procesa          Fragmentos  Nunca   Devuelve   Resultado
  de máquina     en tu PC            pequeños    HTML    textos     local
                               +              +          +          +
                         Deno/Pyodide    OpenRouter   Python     Python
```

### 7.3 Límites de Seguridad (LoopGuard)

```python
max_depth: 10                    # Profundidad máxima de llamadas
max_calls_per_subagent: 50       # Límite por subagente
max_total_calls: 1000            # Límite total
max_money_spent: 10.0            # Límite de costos (USD)
max_repair_attempts: 3           # Reintentos por error
max_seconds_per_phase: 300       # Timeout por fase (5 min)
```

---

## 8. Módulos Principales

### 8.1 orchestrator.py (Orquestador)

```python
class HtmlRLMOrchestrator:
    def __init__(self, config):
        self.deno = DenoSandbox(config)      # Sandbox Deno
        self.client = OpenRouterClient(config) # Cliente API
        self.guard = LoopGuard(...)          # Seguridad
    
    async def run(self):
        # 1. Extraer HTML
        manifest = await self.deno.extract()
        
        # 2. Procesar lotes
        for batch in batches:
            data = await self.client.chat_json(...)
        
        # 3. Reensamblar HTML
        assembled = await self.deno.assemble_many(...)
        
        # 4. Guardar resultados
        # 5. Generar reportes
```

### 8.2 deno_sandbox.py (Deno/Pyodide)

```python
class DenoSandbox:
    async def extract(self):
        """Extrae fragmentos de texto de HTML"""
        # Ejecuta: deno run --allow-read pyodide_runner.ts extract
    
    async def assemble_many(self, documents, replacements):
        """Reconstruye HTML con reemplazos"""
        # Ejecuta: deno run --allow-read pyodide_runner.ts assemble
```

### 8.3 openrouter_client.py (API)

```python
class OpenRouterClient:
    async def chat_json(self, system_prompt, user_prompt):
        """Llama a OpenRouter con JSON response"""
        # POST a https://openrouter.ai/api/v1/chat/completions
        # Con headers de autenticación
```

---

## 9. Manejo de Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `OPENROUTER_API_KEY no encontrado` | `.env` no configurado | Crear `.env` con la API key |
| `Deno no reconocido` | Deno no instalado | Instalar Deno 2.x+ |
| `Pyodide no carga` | Cache no preparado | Ejecutar `deno cache deno/pyodide_runner.ts` |
| `No archivos en output_html/` | No se procesaron HTML | Verificar `input_html/` tiene archivos |
| `Rate limit` | Demasiadas llamadas | Reducir `concurrency` o esperar |
| `Tokens agotados` | Sin saldo en OpenRouter | Recargar cuenta OpenRouter |

---

## 10. Documentación Relacionada

| Archivo | Contenido |
|---------|-----------|
| `README.md` | Instalación y uso básico |
| `docs/00_MEMORIA_DEL_PROYECTO.md` | Mapa mental del proyecto |
| `docs/01_COMO_FUNCIONA_POR_DENTRO.md` | Flujo interno detallado |
| `docs/02_CONFIGURACION_EXPLICADA.md` | Explicación de config.yaml |
| `docs/03_SOLUCION_DE_PROBLEMAS.md` | Errores y soluciones |
| `MANUAL_USO.md` | Guía completa de usuario |
| `AGENTS.md` | Este documento (para agentes IA) |

---

## 11. Tareas de Agentes Comunes

### Tarea: "Procesar documentos HTML"

```bash
# 1. Verificar configuración
cat config.yaml

# 2. Verificar documentos de entrada
ls input_html/

# 3. Ejecutar procesamiento
python -m rlm_html_forge.main --config config.yaml

# 4. Verificar resultados
ls output_html/
cat reports/report.md
```

### Tarea: "Modificar temática"

```bash
# 1. Editar config.yaml
# Cambiar theme.new_theme y theme.style

# 2. Re-ejecutar
python -m rlm_html_forge.main --config config.yaml
```

### Tarea: "Añadir contexto personalizado"

```bash
# 1. Editar context/tema.md
# Añadir instrucciones específicas

# 2. Re-ejecutar
python -m rlm_html_forge.main --config config.yaml
```

### Tarea: "Subir a GitHub"

```bash
# 1. Ejecutar script de preparación
.\scripts\prepare_public_repo.ps1  # Windows
# o
bash scripts/prepare_public_repo.sh  # Linux/Mac

# 2. Verificar archivos excluidos
git status

# 3. Commit y push
git add .
git commit -m "Mensaje"
git push
```

---

## 12. Variables de Entorno (.env)

```env
OPENROUTER_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

**Importante:**
- Nunca compartir esta API key
- Nunca subir `.env` a Git
- Regenerar clave si se expone

---

## 13. Conexiones Externas

| Servicio | URL | Uso |
|----------|-----|-----|
| OpenRouter | https://openrouter.ai | Modelo de IA |
| GitHub | https://github.com/chris78rey/rlm-deno-html-forge | Repositorio |

---

## 14. Contacto y Soporte

- **Repositorio:** https://github.com/chris78rey/rlm-deno-html-forge
- **Documentación:** `docs/` y `MANUAL_USO.md`

---

## 15. Notas para Agentes de IA

### 📌 Antes de Modificar Código

1. **Lee primero:**
   - `docs/00_MEMORIA_DEL_PROYECTO.md`
   - `docs/01_COMO_FUNCIONA_POR_DENTRO.md`

2. **Verifica el entorno:**
   - Python 3.11+ instalado
   - Deno 2.x+ instalado
   - Dependencias en `requirements.txt`

3. **Respeta la seguridad:**
   - Nunca exponer HTML completo a la IA
   - Nunca subir archivos sensibles a Git
   - Respetar límites de LoopGuard

### 📌 Al Escribir Código

- Usa `async/await` para operaciones asíncronas
- Respeta la estructura de módulos existente
- Añade logs informativos
- Actualiza documentación si cambias lógica

### 📌 Al Responder al Usuario

- Muestra comandos exactos a ejecutar
- Explica el porqué de cada acción
- Sugiere verificación posterior
- Indica dónde encontrar más información

---

**Documento creado:** 2026-04-26
**Propósito:** Contexto para agentes de IA
**Última actualización:** Ver fecha del archivo
