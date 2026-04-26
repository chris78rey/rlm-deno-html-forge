# Publicar este proyecto en GitHub público

Antes de publicar, el repositorio no debe incluir:

- `.env`
- `config.yaml` con rutas locales
- `context/tema.md` real
- `input_html/` con documentos reales
- `output_html/`
- `reports/`
- `.work/`

## Preparación rápida en PowerShell

```powershell
.\scripts\prepare_public_repo.ps1
git status
```

## Primer commit público

```powershell
git init
git add .
git commit -m "Initial public release"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/rlm-deno-html-forge.git
git push -u origin main
```

## Uso luego de clonar

```powershell
copy config.example.yaml config.yaml
copy context\tema.example.md context\tema.md
copy .env.example .env
```

Luego editar `.env`, `config.yaml` y `context/tema.md` localmente.
