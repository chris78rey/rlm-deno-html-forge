---
name: rlm-deno-html-forge
description: Infraestructura híbrida Python/Deno para procesamiento de HTML con IA. Transforma documentos manteniendo la estructura original sin exponer el HTML completo.
---

# RLM Deno HTML Forge

**Sistema de procesamiento HTML seguro con Python + Deno**

---

## ¿Qué Hace Este Proyecto?

Transforma documentos HTML usando inteligencia artificial, pero **sin exponer el HTML completo**:

- ✅ Extrae solo texto del HTML localmente
- ✅ Envía texto a la IA (OpenRouter) para transformación
- ✅ Aplica cambios manteniendo la estructura original
- ✅ Genera reportes de procesamiento

**Resultado:** HTML con nueva temática manteniendo la estructura original.

---

## Arquitectura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ INPUT_HTML/ │ ──▶ │ Procesamiento│ ──▶ │ OUTPUT_HTML/│
│  (HTML orig)│     │ AI + Local   │     │ (HTML trans)│
└─────────────┘     │ Python+Deno  │     └─────────────┘
                    └──────────────┘
```

**Tecnologías:**
- Python 3.11+ (Orquestador)
- Deno 2.x (Sandbox de seguridad)
- Pyodide (Python en WASM)
- OpenRouter (IA)

---

## Comando Principal

```bash
python -m rlm_html_forge.main --config config.yaml
```

---

## Flujo de Trabajo

1. **Colocar HTML** en `input_html/`
2. **Configurar temática** en `config.yaml`
3. **Ejecutar** el comando principal
4. **Ver resultados** en `output_html/` y `reports/`

---

## Seguridad

- ✅ HTML nunca sale de tu máquina
- ✅ Solo se envía texto a la IA (fragmentos)
- ✅ Deno con permisos mínimos (`--deny-net`)
- ✅ Límites de costos configurables

---

## Skills Disponibles

| Skill | Descripción |
|-------|-------------|
| `rlm-usar-proyecto` | Ejecutar el procesamiento |
| `rlm-entender-arquitectura` | Entender cómo funciona |
| `rlm-modificar-modelo` | Cambiar modelo de IA |
| `rlm-corregir-errores` | Solucionar problemas |
| `rlm-publicar-github` | Publicar en GitHub |

---

**Documentación completa:**
- `MANUAL_USO.md` - Guía de usuario
- `docs/00_MEMORIA_DEL_PROYECTO.md` - Mapa mental
- `AGENTS.md` - Guía para agentes de IA
