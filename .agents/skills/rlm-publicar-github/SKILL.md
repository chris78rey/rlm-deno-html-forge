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

```bash
# Linux/Mac
bash scripts/prepare_public_repo.sh
```

### 2. Inicializar Git

```bash
git init
git add .
git commit -m "Initial public release"
git branch -M main
```

### 3. Crear repositorio en GitHub

1. Ve a: https://github.com/new
2. Nombre: `rlm-deno-html-forge`
3. **NO marcar** "Add a README"
4. **NO marcar** "Add .gitignore"
5. Click en "Create repository"

### 4. Conectar y subir

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
- ❌ `context/tema.md` (contexto real)

---

## Verificar

```bash
# Ver archivos excluidos
git status --ignored

# Ver archivos subidos
git ls-tree -r main --name-only
```

---

## Enlace del Repositorio

```
https://github.com/TU_USUARIO/rlm-deno-html-forge
```

---

**Documentación completa:** `README_GITHUB_PUBLICO.md`
