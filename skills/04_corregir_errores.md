# Skill 04: Corregir Errores Comunes

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

### 4. No hay archivos en output_html/

```bash
# Verificar input
ls input_html/

# Debe haber archivos .html o .htm
```

### 5. Modelo tarda mucho

```yaml
# Aumentar concurrencia en config.yaml
rlm:
  concurrency: 8
```

### 6. Rate limit de OpenRouter

```yaml
# Reducir concurrencia en config.yaml
rlm:
  concurrency: 3
```

---

## Flujo de Diagnóstico

```
1. ¿Error al iniciar?
   └─ Verificar Python, Deno, dependencias

2. ¿Error durante procesamiento?
   └─ Revisar reports/report.md

3. ¿Sin archivos en output?
   └─ Verificar input_html/ y config.yaml
```

---

## Verificar Logs

```bash
# Ver reporte de errores
cat reports/report.md

# Ver reporte estructurado
cat reports/report.json
```

---

**Documentación completa:** `docs/03_SOLUCION_DE_PROBLEMAS.md`
