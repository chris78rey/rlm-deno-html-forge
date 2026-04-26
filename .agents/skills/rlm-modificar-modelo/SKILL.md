---
name: rlm-modificar-modelo
description: Cambia el modelo de IA de OpenRouter en RLM Deno HTML Forge. Explica opciones disponibles y recomendaciones.
---

# RLM - Modificar Modelo de IA

**Cómo cambiar el modelo de OpenRouter**

---

## Editar config.yaml

```yaml
model:
  name: "anthropic/claude-3-sonnet"
  provider: "openrouter"
```

---

## Modelos Disponibles

| Modelo | Velocidad | Calidad | Costo |
|--------|-----------|---------|-------|
| `openrouter/auto` | Media | Alta | Variable |
| `anthropic/claude-3-sonnet` | Media | Alta | Media |
| `anthropic/claude-3-haiku` | Rápida | Media | Baja |
| `openai/gpt-4-turbo` | Media | Alta | Alta |
| `openai/gpt-3.5-turbo` | Rápida | Media | Baja |

---

## Recomendaciones

### Velocidad máxima
```yaml
model:
  name: "anthropic/claude-3-haiku"
```

### Calidad máxima
```yaml
model:
  name: "anthropic/claude-3-sonnet"
```

### Equilibrio
```yaml
model:
  name: "openrouter/auto"
```

---

## Verificar Modelo

```bash
# Ejecutar procesamiento
python -m rlm_html_forge.main --config config.yaml

# Ver reporte
cat reports/report.json
```

---

**Documentación completa:** `docs/02_CONFIGURACION_EXPLICADA.md`
