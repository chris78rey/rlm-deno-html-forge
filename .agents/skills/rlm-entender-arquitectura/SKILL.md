---
name: rlm-entender-arquitectura
description: Explica la arquitectura de RLM Deno HTML Forge. Flujo de datos, componentes clave y seguridad del sistema.
---

# RLM - Entender la Arquitectura

**Resumen rápido de cómo funciona el sistema**

---

## Flujo de Datos

```
input_html/
    │
    ▼
[Deno/Pyodide] → Extrae texto del HTML
    │
    ▼
[Python] → Agrupa en lotes
    │
    ▼
[OpenRouter] → IA transforma texto
    │
    ▼
[Deno/Pyodide] → Reconstruye HTML
    │
    ▼
output_html/ + reports/
```

---

## Componentes Clave

| Componente | Tecnología | Función |
|------------|------------|---------|
| Orquestador | Python | Controla el flujo |
| Sandbox | Deno + Pyodide | Procesa HTML localmente |
| IA | OpenRouter | Transforma texto |
| Reportes | Python | Genera salidas |

---

## Seguridad

- ✅ HTML nunca sale de tu máquina
- ✅ Solo se envía texto a la IA
- ✅ Deno con permisos mínimos
- ✅ .env nunca se sube a Git

---

**Documentación completa:** `docs/00_MEMORIA_DEL_PROYECTO.md`
