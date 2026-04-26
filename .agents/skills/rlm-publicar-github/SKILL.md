---
name: rlm-publicar-github
description: Publica el repositorio RLM Deno HTML Forge en GitHub. Pasos para preparar, inicializar Git y subir a GitHub.
---

# RLM - Publicar en GitHub

**Guía para publicar el repositorio en GitHub**

---

## Pasos Rápidos

### 1. Preparar repositorio

```powershell
# Windows PowerShell
.\scripts\prepare_public_repo.ps1
```

### 2. Inicializar Git

```bash
git init
git add .
git commit -m "Initial public release"
git branch -M main
```

### 3. Conectar y subir

```bash
git remote add origin https://github.com/TU_USUARIO/rlm-deno-html-forge.git
git push -u origin main
```

---

## Archivos Excluidos

Estos NO se suben a GitHub:

- ❌ `.env` (secretos API)
- ❌ `config.yaml` (configuración local)
- ❌ `input_html/*.htm` (documentos reales)
- ❌ `output_html/` (resultados)
- ❌ `reports/` (reportes)

---

**Documentación completa:** `README_GITHUB_PUBLICO.md`
