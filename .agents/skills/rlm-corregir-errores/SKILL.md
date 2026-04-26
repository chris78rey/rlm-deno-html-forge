---
name: rlm-corregir-errores
description: Solución rápida a problemas comunes en RLM Deno HTML Forge. Errores de API key, Deno, Pyodide y procesamiento.
---

# RLM - Corregir Errores Comunes

**Solución rápida a problemas frecuentes**

---

## Errores Comunes

### 1. OPENROUTER_API_KEY no encontrado

```bash
# Crear .env desde ejemplo
cp .env.example .env

# Editar con tu API key
# OPENROUTER_API_KEY=sk-xxxxx
```

### 2. Deno no reconocido

```bash
# Instalar Deno
# Windows: irm https://deno.land/install.ps1 | iex
# Linux/Mac: curl -fsSL https://deno.land/install.sh | sh
```

### 3. Pyodide no carga

```bash
# Preparar caché
deno cache deno/pyodide_runner.ts
```

### 4. Modelo tarda mucho

```yaml
rlm:
  concurrency: 8
```

### 5. Rate limit de OpenRouter

```yaml
rlm:
  concurrency: 3
```

---

## Verificar Logs

```bash
cat reports/report.md
cat reports/report.json
```

---

**Documentación completa:** `docs/03_SOLUCION_DE_PROBLEMAS.md`
