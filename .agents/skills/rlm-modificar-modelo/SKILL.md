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

**Documentación completa:** `docs/02_CONFIGURACION_EXPLICADA.md`
