---
name: rlm-deno-html-forge
description: Infraestructura híbrida Python/Deno para procesamiento de HTML con IA. Transforma documentos manteniendo la estructura original sin exponer el HTML completo.
---

# RLM Deno HTML Forge

**Sistema de procesamiento HTML seguro con Python + Deno**

---

## ¿Qué Hace Este Proyecto?

Transforma documentos HTML usando inteligencia artificial:

- ✅ Extrae solo texto del HTML localmente
- ✅ Envía texto a la IA para transformación
- ✅ Aplica cambios manteniendo la estructura original
- ✅ Genera reportes de procesamiento

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
- ✅ Deno con permisos mínimos
- ✅ Límites de costos configurables

---

**Documentación completa:**
- `MANUAL_USO.md` - Guía de usuario
- `docs/00_MEMORIA_DEL_PROYECTO.md` - Mapa mental
