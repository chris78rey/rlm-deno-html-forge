from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
from .utils import ensure_dir

@dataclass
class FileReport:
    source: str
    output: str | None
    targets: int
    replaced: int
    status: str
    errors: list[str]

@dataclass
class RunReport:
    generated_at_utc: str
    model: str
    theme: str
    files: list[FileReport]
    total_calls: int
    estimated_cost: float
    assets_copied: int
    def save(self, reports_dir: str | Path) -> None:
        reports_dir = Path(reports_dir); ensure_dir(reports_dir); data = asdict(self)
        with (reports_dir/'report.json').open('w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=2)
        with (reports_dir/'report.md').open('w', encoding='utf-8') as f: f.write(self.to_markdown())
    def to_markdown(self) -> str:
        ok = len([x for x in self.files if x.status == 'ok']); err = len([x for x in self.files if x.status != 'ok'])
        total_targets = sum(x.targets for x in self.files); total_replaced = sum(x.replaced for x in self.files)
        lines = ['# Reporte RLM HTML Forge','',f'- Generado UTC: {self.generated_at_utc}',f'- Modelo: `{self.model}`',f'- Tema: {self.theme}',f'- Archivos correctos: {ok}',f'- Archivos con error: {err}',f'- Targets detectados: {total_targets}',f'- Textos reemplazados: {total_replaced}',f'- Assets copiados: {self.assets_copied}',f'- Llamadas LLM: {self.total_calls}',f'- Costo estimado: {self.estimated_cost:.6f}','','## Archivos','']
        for item in self.files:
            lines += [f'### {item.source}','',f'- Estado: `{item.status}`',f'- Salida: `{item.output or ""}`',f'- Targets: {item.targets}',f'- Reemplazados: {item.replaced}']
            if item.errors:
                lines.append('- Errores:')
                for e in item.errors: lines.append(f'  - {e}')
            lines.append('')
        return '\n'.join(lines)

def new_report(model: str, theme: str, files: list[FileReport], total_calls: int, estimated_cost: float, assets_copied: int) -> RunReport:
    return RunReport(datetime.now(timezone.utc).isoformat(), model, theme, files, total_calls, estimated_cost, assets_copied)
