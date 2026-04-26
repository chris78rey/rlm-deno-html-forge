# Skill 01: Usar el Proyecto

**Guía rápida para ejecutar el procesamiento de HTML**

---

## Comando Principal

```bash
python -m rlm_html_forge.main --config config.yaml
```

---

## Flujo de Trabajo

### Paso 1: Preparar documentos
```
Colocar HTML en input_html/
```

### Paso 2: Configurar temática
```
Editar config.yaml → theme.new_theme
```

### Paso 3: Ejecutar
```bash
python -m rlm_html_forge.main --config config.yaml
```

### Paso 4: Ver resultados
```
output_html/  → Documentos transformados
reports/      → Reportes de procesamiento
```

---

## Comandos Rápidos

| Acción | Comando |
|--------|---------|
| Procesar documentos | `python -m rlm_html_forge.main --config config.yaml` |
| Ver input | `ls input_html/` |
| Ver output | `ls output_html/` |
| Ver reportes | `cat reports/report.md` |

---

## Verificación

```bash
# Verificar instalación
python --version      # Python 3.11+
deno --version        # Deno 2.x

# Verificar configuración
cat config.yaml

# Verificar documentos
ls input_html/
```

---

**Documentación completa:** `MANUAL_USO.md`
