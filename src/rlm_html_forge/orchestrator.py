from __future__ import annotations

from pathlib import Path
import asyncio
from collections import defaultdict

from tqdm import tqdm

from .config import AppConfig
from .deno_sandbox import DenoSandbox
from .openrouter_client import OpenRouterClient
from .loop_guard import LoopGuard, LoopGuardError
from .prompts import system_prompt, batch_prompt
from .reporting import FileReport, new_report
from .utils import ensure_dir, copy_assets, chunked
from .text_cleaner import clean_visible_spanish_text


class HtmlRLMOrchestrator:
    def __init__(self, config: AppConfig):
        self.config = config
        self.deno = DenoSandbox(config)
        self.client = OpenRouterClient(config)
        self.guard = LoopGuard(
            config.rlm.max_depth,
            config.rlm.max_calls_per_subagent,
            config.rlm.max_total_calls,
            config.rlm.max_money_spent,
            config.rlm.max_repair_attempts,
            config.rlm.max_same_error_repetitions,
            config.rlm.max_seconds_per_phase,
            config.rlm.input_cost_per_1m_tokens,
            config.rlm.output_cost_per_1m_tokens,
        )

    async def run(self) -> None:
        input_dir = Path(self.config.paths.input_dir)
        output_dir = Path(self.config.paths.output_dir)
        reports_dir = Path(self.config.paths.reports_dir)

        ensure_dir(input_dir)
        ensure_dir(output_dir)
        ensure_dir(reports_dir)

        print("Extrayendo estructura HTML dentro de Deno/Pyodide...")
        self.guard.begin_phase()
        manifest = await self.deno.extract()
        documents = manifest.get("documents", [])

        if not documents:
            print(f"No se encontraron HTML en {input_dir}")
            return

        print(f"Archivos HTML detectados: {len(documents)}")

        replacements_by_file: dict[str, dict[str, str]] = defaultdict(dict)
        errors_by_file: dict[str, list[str]] = defaultdict(list)

        semaphore = asyncio.Semaphore(self.config.rlm.concurrency)
        all_batches = []

        for doc in documents:
            source_path = doc["path"]
            targets = doc.get("targets", [])
            for batch in chunked(targets, self.config.rlm.batch_size):
                all_batches.append((source_path, batch))

        print(f"Lotes de subagentes: {len(all_batches)}")
        print(f"Contexto cargado: {len(self.config.context_text)} caracteres")

        sys_prompt = system_prompt(self.config)

        async def process_batch(batch_index: int, source_path: str, batch: list[dict]) -> None:
            async with semaphore:
                self.guard.check_depth(1)
                self.guard.check_phase_timeout("map")

                reduced_items = [
                    {
                        "id": t["id"],
                        "kind": t["kind"],
                        "tag": t.get("tag"),
                        "attribute": t.get("attr"),
                        "path_hint": t.get("path_hint"),
                        "original": t.get("original"),
                    }
                    for t in batch
                ]

                try:
                    data, llm_resp = await self.client.chat_json(
                        sys_prompt,
                        batch_prompt(reduced_items, self.config),
                    )
                    self.guard.register_call(
                        f"subagent:{self.config.model.model}",
                        llm_resp.input_tokens,
                        llm_resp.output_tokens,
                    )

                    items = data.get("items", [])
                    if not isinstance(items, list):
                        raise ValueError("La respuesta no tiene items como lista.")

                    allowed_ids = {t["id"] for t in batch}

                    for item in items:
                        if not isinstance(item, dict):
                            continue

                        target_id = str(item.get("id", ""))
                        replacement = clean_visible_spanish_text(str(item.get("replacement", "")))

                        if target_id in allowed_ids and replacement:
                            replacements_by_file[source_path][target_id] = replacement

                except Exception as exc:
                    msg = f"Batch {batch_index} falló: {exc}"
                    self.guard.register_error(str(exc))
                    errors_by_file[source_path].append(msg)

        tasks = [
            process_batch(i, source_path, batch)
            for i, (source_path, batch) in enumerate(all_batches, start=1)
        ]

        for fut in tqdm(asyncio.as_completed(tasks), total=len(tasks), unit="lote"):
            try:
                await fut
            except LoopGuardError:
                raise
            except Exception as exc:
                self.guard.register_error(str(exc))

        print("Ensamblando todos los HTML en una sola llamada a Deno...")
        assembled = await self.deno.assemble_many(documents, dict(replacements_by_file))

        file_reports: list[FileReport] = []

        for doc in tqdm(documents, unit="archivo"):
            source_path = doc["path"]
            try:
                src = Path(source_path)
                rel = src.relative_to(input_dir)
                dst = output_dir / rel

                final_html = assembled[source_path]
                ensure_dir(dst.parent)
                dst.write_text(final_html, encoding="utf-8", newline="")

                file_reports.append(
                    FileReport(
                        source_path,
                        str(dst),
                        len(doc.get("targets", [])),
                        len(replacements_by_file.get(source_path, {})),
                        "ok",
                        errors_by_file.get(source_path, []),
                    )
                )

            except Exception as exc:
                file_reports.append(
                    FileReport(
                        source_path,
                        None,
                        len(doc.get("targets", [])),
                        len(replacements_by_file.get(source_path, {})),
                        "error",
                        errors_by_file.get(source_path, []) + [str(exc)],
                    )
                )

        assets_copied = (
            copy_assets(input_dir, output_dir, {x.lower() for x in self.config.html.extensions})
            if self.config.html.copy_non_html_assets
            else 0
        )

        report = new_report(
            self.config.model.model,
            self.config.theme.new_theme,
            file_reports,
            self.guard.total_calls,
            self.guard.total_estimated_cost,
            assets_copied,
        )
        report.save(reports_dir)

        print("Proceso finalizado.")
        print(f"Reporte: {reports_dir / 'report.md'}")
        print(f"Salida: {output_dir}")
