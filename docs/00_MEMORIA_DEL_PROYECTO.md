# 📚 Memoria del Proyecto - RLM Deno HTML Forge

**Documento de referencia para entender el proyecto en el futuro**

---

## 1. ¿Qué Hace Este Proyecto?

**Objetivo principal:** Transformar documentos HTML aplicándoles una nueva temática usando inteligencia artificial, **sin exponer el HTML completo a la IA**.

### Entrada → Procesamiento → Salida

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  INPUT_HTML/    │ ──▶ │ Procesamiento    │ ──▶ │ OUTPUT_HTML/    │
│  (HTML originales) │  │ AI + Local       │     │ (HTML transforma-│
└─────────────────┘     │ (Python + Deno)  │     │ dos)            │
                        └──────────────────┘     └─────────────────┘
```

---

## 2. Problema que Resuelve

**Problema:** Cambiar la apariencia/estilo de múltiples documentos HTML es manual, lento y requiere conocimientos de CSS/HTML.

**Solución:** Usar IA para analizar el texto, sugerir transformaciones y aplicarlas automáticamente manteniendo la estructura HTML original.

---

## 3. Arquitectura del Sistema

### Tecnologías Principales

| Tecnología | Rol | ¿Por qué? |
|------------|-----|-----------|
| **Python 3.11+** | Orquestador principal | Control de flujo, API calls, procesamiento de archivos |
| **Deno 2.x** | Sandbox de ejecución | Seguridad cero-trust, aislamiento del código |
| **Pyodide** | REPL Python en Deno | Ejecutar código Python dentro del sandbox |
| **OpenRouter** | Modelo de IA | Procesar fragmentos de texto para transformación |

### Flujo de Seguridad (Importante)

```
HTML COMPLETO        →  Nunca se envía a la IA
        │
        ▼
        │ Extrae texto localmente (Deno/Pyodide)
        ▼
        │ Envía solo fragmentos de texto (no HTML)
        ▼
        │ IA transforma el texto
        ▼
        │ Aplica transformaciones localmente
        ▼
        ▼
  HTML TRANSFORMADO
```

**Qué NO hace el proyecto:**
- ❌ No envía el HTML completo a OpenRouter
- ❌ No ejecuta código remoto
- ❌ No escribe archivos desde Deno (solo lectura)

---

## 4. Estructura de Carpetas

```
rlm-deno-html-forge/
├── src/rlm_html_forge/          # Código Python principal
│   ├── main.py                  # Punto de entrada
│   ├── orchestrator.py          # Orquestador del flujo
│   ├── deno_sandbox.py          # Interfaz con Deno
│   ├── openrouter_client.py     # Cliente OpenRouter
│   ├── config.py                # Configuración
│   └── ... (otros módulos)
├── deno/
│   └── pyodide_runner.ts        # Sandbox Deno + Pyodide
├── input_html/                  # Tus documentos HTML
├── output_html/                 # Documentos transformados
├── reports/                     # Reportes de procesamiento
├── config.yaml                  # Configuración del proyecto
├── .env                         # Secretos (API keys)
└── docs/                        # Documentación
```

---

## 5. Archivos de Configuración Clave

| Archivo | Propósito | ¿Se sube a GitHub? |
|---------|-----------|-------------------|
| `config.yaml` | Configuración del proyecto | ❌ No (es local) |
| `config.example.yaml` | Ejemplo de configuración | ✅ Sí |
| `.env` | API Keys y secretos | ❌ No |
| `.env.example` | Ejemplo de variables | ✅ Sí |
| `context/tema.md` | Contexto del documento actual | ❌ No |
| `context/tema.example.md` | Ejemplo de contexto | ✅ Sí |

---

## 6. Flujo de Datos

### Paso 1: Carga de Configuración
```
Python lee config.yaml
    ↓
Python carga contexto (context/tema.md)
    ↓
Python prepara sistema prompt con contexto
```

### Paso 2: Extracción de HTML
```
Deno/Pyodide abre input_html/
    ↓
Detecta todas las partes de texto reemplazables
    ↓
Genera lista de "targets" (elementos a transformar)
    ↓
Devuelve manifesto de documentos
```

### Paso 3: Procesamiento por Lotes
```
Python agrupa targets en lotes (batch_size: 35)
    ↓
Para cada lote, envía a OpenRouter:
  - Prompt del sistema
  - Lista de fragmentos de texto
  - Contexto del documento
    ↓
IA devuelve transformaciones sugeridas
    ↓
Python guarda reemplazos por ID
```

### Paso 4: Reensamblado
```
Deno/Pyodide reconstruye HTML
    ↓
Aplica reemplazos a las posiciones correctas
    ↓
Genera HTML transformado
    ↓
Python escribe en output_html/
```

### Paso 5: Reportes
```
Python genera reportes en reports/:
  - report.html (vista visual)
  - report.json (datos estructurados)
  - report.md (resumen markdown)
```

---

## 7. Configuración Crítica (documentada en 02_CONFIGURACION_EXPLICADA.md)

### Valores que afectan rendimiento

```yaml
rlm:
  concurrency: 6           # Cuántas llamadas simultáneas a IA
  batch_size: 35          # Cuántos fragmentos por llamada

html:
  min_text_length: 8      # Texto mínimo a procesar
  max_text_length: 1500   # Texto máximo por fragmento
```

**Impacto:**
- `concurrency`: Más alto = más rápido, pero más costo y riesgo de rate limit
- `batch_size`: Más alto = menos llamadas, pero prompt más largo
- `max_text_length`: Límite para evitar prompts gigantes

---

## 8. Seguridad y Privacidad

### Qué NO se sube a GitHub:
- ❌ `.env` (API keys)
- ❌ `config.yaml` (configuración local)
- ❌ `context/tema.md` (contenido real del documento)
- ❌ `input_html/*.htm` (documentos originales)
- ❌ `output_html/` (resultados)
- ❌ `reports/` (reportes generados)
- ❌ `.work/` (archivos temporales)

### Cómo se protege el HTML:
1. **Extracción local**: Deno/Pyodide procesa HTML en tu máquina
2. **Solo texto**: Solo se extrae texto visible, no estructura HTML
3. **Fragmentos**: El texto se divide en fragmentos pequeños
4. **Sin contexto completo**: Cada fragmento se procesa independientemente

---

## 9. Cómo Usar (Resumen Rápido)

```bash
# 1. Colocar HTML en input_html/
# 2. Configurar config.yaml
# 3. Ejecutar:
python -m rlm_html_forge.main --config config.yaml
# 4. Ver resultados en output_html/ y reports/
```

---

## 10. Archivos de Documentación Existentes

| Archivo | Contenido |
|---------|-----------|
| `README.md` | Instalación, requisitos, uso básico |
| `README_GITHUB_PUBLICO.md` | Guía para publicar en GitHub |
| `README_PARCHE.md` | Notas de parche/actualizaciones |
| `MANUAL_USO.md` | Manual completo de usuario |
| `docs/00_MEMORIA_DEL_PROYECTO.md` | Este documento (mapa mental) |
| `docs/01_COMO_FUNCIONA_POR_DENTRO.md` | Flujo interno detallado |
| `docs/02_CONFIGURACION_EXPLICADA.md` | Explicación de config.yaml |
| `docs/03_SOLUCION_DE_PROBLEMAS.md` | Errores comunes y soluciones |
| `docs/04_SEGURIDAD_Y_DATOS_PRIVADOS.md` | Protección de datos |
| `docs/05_DECISIONES_TECNICAS.md` | Decisiones de arquitectura |

---

## 11. Puntos Clave para Recordar

✅ **El HTML nunca sale de tu máquina**
✅ **Solo se envía texto a la IA, nunca el HTML completo**
✅ **Deno ejecuta en sandbox con permisos restringidos**
✅ **Python controla el flujo y escribe los archivos finales**
✅ **Los reportes quedan en `reports/` para seguimiento**

---

## 12. Revisar en el Futuro

Cuando vuelvas a este proyecto después de meses:

1. **Lee este documento primero** → `docs/00_MEMORIA_DEL_PROYECTO.md`
2. **Entiende el flujo interno** → `docs/01_COMO_FUNCIONA_POR_DENTRO.md`
3. **Revisa configuración** → `docs/02_CONFIGURACION_EXPLICADA.md`
4. **Resuelve problemas** → `docs/03_SOLUCION_DE_PROBLEMAS.md`

---

**Documento creado:** 2026-04-26
**Versión del proyecto:** Inicial
