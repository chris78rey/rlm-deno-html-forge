from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import asyncio
import json
import shutil
import base64

from .config import AppConfig


@dataclass
class DenoResult:
    ok: bool
    data: dict
    stderr: str
    returncode: int


class DenoSandbox:
    def __init__(self, config: AppConfig):
        self.config = config

    def build_cmd(self) -> list[str]:
        sandbox = self.config.sandbox
        deno_bin = shutil.which(sandbox.deno_bin) or sandbox.deno_bin

        cmd = [deno_bin, "run"]

        if sandbox.no_prompt:
            cmd.append("--no-prompt")

        if sandbox.cached_only:
            cmd.append("--cached-only")

        if sandbox.allow_read:
            cmd.append("--allow-read=" + ",".join(sandbox.allow_read))

        if sandbox.deny_net:
            cmd.append("--deny-net")

        cmd.extend(["--deny-env", "--deny-run", "--deny-ffi"])
        cmd.append(str(Path(sandbox.runner_ts)))
        return cmd

    async def run_json(self, payload: dict, timeout_seconds: int = 300) -> DenoResult:
        proc = await asyncio.create_subprocess_exec(
            *self.build_cmd(),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        raw_input = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        stdout, stderr = await asyncio.wait_for(proc.communicate(raw_input), timeout=timeout_seconds)

        stderr_text = stderr.decode("utf-8", errors="replace")
        stdout_text = stdout.decode("utf-8", errors="replace")

        try:
            data = json.loads(stdout_text)
        except Exception as exc:
            data = {"ok": False, "error": f"No se pudo parsear stdout JSON desde Deno: {exc}", "stdout_preview": stdout_text[:2000]}

        return DenoResult(ok=bool(data.get("ok")), data=data, stderr=stderr_text, returncode=proc.returncode or 0)

    async def extract(self) -> dict:
        payload = {
            "action": "extract",
            "input_dir": self.config.paths.input_dir,
            "extensions": self.config.html.extensions,
            "html": {
                "min_text_length": self.config.html.min_text_length,
                "max_text_length": self.config.html.max_text_length,
                "skip_tags": self.config.html.skip_tags,
                "skip_text_regex": self.config.html.skip_text_regex,
            },
        }
        result = await self.run_json(payload, timeout_seconds=self.config.rlm.max_seconds_per_phase)
        if not result.ok:
            raise RuntimeError(f"Deno extract falló: {result.data} STDERR={result.stderr}")
        return result.data

    async def assemble_many(self, documents: list[dict], replacements_by_file: dict[str, dict[str, str]]) -> dict[str, str]:
        payload = {
            "action": "assemble_many",
            "documents": [
                {
                    "source_path": doc["path"],
                    "targets": doc.get("targets", []),
                    "replacements": replacements_by_file.get(doc["path"], {}),
                }
                for doc in documents
            ],
        }

        result = await self.run_json(payload, timeout_seconds=self.config.rlm.max_seconds_per_phase)
        if not result.ok:
            raise RuntimeError(f"Deno assemble_many falló: {result.data} STDERR={result.stderr}")

        assembled: dict[str, str] = {}
        for item in result.data.get("documents", []):
            html = base64.b64decode(item["value_base64"].encode("ascii")).decode("utf-8", errors="replace")
            assembled[item["source_path"]] = html

        return assembled
