from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml


@dataclass
class PathsConfig:
    input_dir: str = "./input_html"
    output_dir: str = "./output_html"
    reports_dir: str = "./reports"
    work_dir: str = "./.work"


@dataclass
class ThemeConfig:
    new_theme: str
    language: str = "español"
    tone: str = "claro y profesional"
    audience: str = "usuarios generales"
    extra_context: str = ""
    context_file: str = "./context/tema.md"


@dataclass
class ModelConfig:
    provider: str = "openrouter"
    model: str = "minimax/minimax-m2.7"
    endpoint: str = "https://openrouter.ai/api/v1/chat/completions"
    api_key_env: str = "OPENROUTER_API_KEY"
    temperature: float = 0.25
    timeout_seconds: int = 120
    max_retries: int = 2
    http_referer: str = "http://localhost"
    x_title: str = "RLM Deno HTML Forge"


@dataclass
class RLMRuntimeConfig:
    max_depth: int = 3
    max_calls_per_subagent: int = 200
    max_total_calls: int = 300
    max_money_spent: float = 2.0
    max_repair_attempts: int = 3
    max_same_error_repetitions: int = 2
    max_seconds_per_phase: int = 900
    concurrency: int = 6
    batch_size: int = 35
    input_cost_per_1m_tokens: float = 0.0
    output_cost_per_1m_tokens: float = 0.0

    def to_fast_rlm_config_dict(self) -> dict[str, Any]:
        return {
            "primary_agent": "minimax/minimax-m2.7",
            "sub_agent": "minimax/minimax-m2.7",
            "max_depth": self.max_depth,
            "max_calls_per_subagent": self.max_calls_per_subagent,
            "max_money_spent": self.max_money_spent,
            "api_max_retries": 3,
            "api_timeout_ms": self.max_seconds_per_phase * 1000,
        }


@dataclass
class SandboxConfig:
    deno_bin: str = "deno"
    runner_ts: str = "./deno/pyodide_runner.ts"
    cached_only: bool = True
    no_prompt: bool = True
    deny_net: bool = True
    allow_read: list[str] = field(default_factory=list)


@dataclass
class HtmlConfig:
    extensions: list[str] = field(default_factory=lambda: [".html", ".htm"])
    copy_non_html_assets: bool = True
    min_text_length: int = 8
    max_text_length: int = 1500
    skip_tags: list[str] = field(default_factory=list)
    skip_text_regex: list[str] = field(default_factory=list)


@dataclass
class AppConfig:
    paths: PathsConfig
    theme: ThemeConfig
    model: ModelConfig
    rlm: RLMRuntimeConfig
    sandbox: SandboxConfig
    html: HtmlConfig
    root_dir: Path
    context_text: str = ""

    @classmethod
    def from_yaml(cls, config_path: str | Path) -> "AppConfig":
        path = Path(config_path).resolve()
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        cfg = cls(
            paths=PathsConfig(**raw.get("paths", {})),
            theme=ThemeConfig(**raw.get("theme", {})),
            model=ModelConfig(**raw.get("model", {})),
            rlm=RLMRuntimeConfig(**raw.get("rlm", {})),
            sandbox=SandboxConfig(**raw.get("sandbox", {})),
            html=HtmlConfig(**raw.get("html", {})),
            root_dir=path.parent,
        )
        cfg.resolve_paths()
        cfg.load_context()
        return cfg

    def resolve_paths(self) -> None:
        def r(p: str) -> str:
            q = Path(p)
            if not q.is_absolute():
                q = self.root_dir / q
            return str(q.resolve())

        self.paths.input_dir = r(self.paths.input_dir)
        self.paths.output_dir = r(self.paths.output_dir)
        self.paths.reports_dir = r(self.paths.reports_dir)
        self.paths.work_dir = r(self.paths.work_dir)
        self.sandbox.runner_ts = r(self.sandbox.runner_ts)
        self.sandbox.allow_read = [r(p) for p in self.sandbox.allow_read]

        if self.theme.context_file:
            self.theme.context_file = r(self.theme.context_file)

    def load_context(self) -> None:
        parts: list[str] = []

        if self.theme.extra_context.strip():
            parts.append(self.theme.extra_context.strip())

        if self.theme.context_file:
            context_path = Path(self.theme.context_file)
            if context_path.exists():
                parts.append(context_path.read_text(encoding="utf-8", errors="replace").strip())

        self.context_text = "\n\n".join([p for p in parts if p])
