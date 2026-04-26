from __future__ import annotations
from pathlib import Path
import shutil, json, re

def ensure_dir(path: str | Path) -> None: Path(path).mkdir(parents=True, exist_ok=True)

def write_json(path: str | Path, data) -> None:
    ensure_dir(Path(path).parent)
    with Path(path).open('w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=2)

def copy_assets(input_dir: Path, output_dir: Path, html_extensions: set[str]) -> int:
    count = 0
    for src in input_dir.rglob('*'):
        if not src.is_file(): continue
        if src.suffix.lower() in html_extensions: continue
        dst = output_dir / src.relative_to(input_dir)
        ensure_dir(dst.parent); shutil.copy2(src, dst); count += 1
    return count

def extract_json_object(text: str) -> dict:
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```[a-zA-Z0-9_-]*', '', text).strip()
        text = re.sub(r'```$', '', text).strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict): return parsed
    except Exception: pass
    start = text.find('{')
    if start < 0: raise ValueError('No se encontró inicio de JSON.')
    depth = 0; in_string = False; escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if escaped: escaped = False; continue
        if ch == '\\': escaped = True; continue
        if ch == '"': in_string = not in_string; continue
        if in_string: continue
        if ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: return json.loads(text[start:i+1])
    raise ValueError('No se pudo extraer JSON válido.')

def chunked(seq: list, size: int):
    for i in range(0, len(seq), size): yield seq[i:i+size]
