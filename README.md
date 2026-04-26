# RLM Deno HTML Forge

Infraestructura híbrida local:

- Python: orquestador asíncrono, control de presupuesto, LoopGuard, llamadas a OpenRouter/MiniMax.
- Deno 2.x: sandbox V8 de confianza cero.
- Pyodide/WebAssembly dentro de Deno: REPL Python aislado para diseccionar y ensamblar HTML.
- OpenRouter: solo recibe fragmentos de texto y metadatos mínimos, nunca el HTML completo.

## Advertencia técnica importante

El procesamiento de archivos ocurre localmente. Si se usa OpenRouter, la generación textual no es offline: los fragmentos de texto extraídos se envían al modelo configurado. El HTML completo no se envía al modelo.

## Requisitos

- Python 3.11+
- Deno 2.x+
- API key de OpenRouter

Verificar:

```bash
python --version
deno --version
```

## Instalación

```bash
cd rlm_deno_html_forge
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell:

```powershell
cd rlm_deno_html_forge
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Editar `.env`:

```env
OPENROUTER_API_KEY=pega_aqui_tu_api_key
```

## Preparar Pyodide en caché de Deno

Este paso descarga/cachea Pyodide. Se hace una sola vez.

```bash
deno cache deno/pyodide_runner.ts
```

Luego el sandbox de ejecución real se lanza con:

```bash
--cached-only
--deny-net
--no-prompt
--allow-read=<carpetas_permitidas>
```

## Uso

1. Colocar HTML dentro de:

```text
input_html/
```

2. Editar `config.yaml`:

```yaml
theme:
  new_theme: "Nueva temática"
```

3. Ejecutar:

```bash
python -m rlm_html_forge.main --config config.yaml
```

El resultado se guarda en:

```text
output_html/
reports/report.json
reports/report.md
```

## Seguridad

El sandbox Deno se ejecuta con:

- `--deny-net`
- `--no-prompt`
- `--cached-only`
- `--allow-read` limitado a las carpetas configuradas
- sin `--allow-write`
- sin `--allow-run`
- sin `--allow-ffi`

Python escribe los archivos finales. Deno solo lee HTML y devuelve resultados estructurados por stdout.
