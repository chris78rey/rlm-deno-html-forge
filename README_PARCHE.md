# Parche: contexto amplio + mejora de velocidad

Este parche modifica el proyecto `rlm_deno_html_forge` para:

1. Permitir colocar un contexto largo en `context/tema.md`.
2. Usar ese contexto dentro del prompt del modelo.
3. Reducir la cantidad de llamadas al modelo aumentando `batch_size`.
4. Reducir demora de Deno/Pyodide ensamblando todos los HTML en una sola llamada.

## Cómo aplicar

Copiar estas carpetas y archivos encima del proyecto original:

```text
config.yaml
context/tema.md
src/rlm_html_forge/config.py
src/rlm_html_forge/prompts.py
src/rlm_html_forge/deno_sandbox.py
src/rlm_html_forge/orchestrator.py
deno/pyodide_runner.ts
```

En PowerShell, estando dentro de la carpeta del proyecto original:

```powershell
Copy-Item -Recurse -Force "RUTA_DEL_PARCHE\*" "."
```

Luego editar:

```text
context/tema.md
```

Ahí se puede pegar todo el contexto amplio del nuevo tema.

Después ejecutar:

```powershell
python -m rlm_html_forge.main --config config.yaml
```
