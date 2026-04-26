from __future__ import annotations
import os, asyncio
from dataclasses import dataclass
from typing import Any
import httpx
from .config import AppConfig
from .utils import extract_json_object

@dataclass
class LLMResponse:
    content: str
    input_tokens: int = 0
    output_tokens: int = 0

class OpenRouterClient:
    def __init__(self, config: AppConfig):
        self.config = config
        self.api_key = os.getenv(config.model.api_key_env, '').strip()
        if not self.api_key: raise RuntimeError(f'Falta la variable de ambiente {config.model.api_key_env}.')
    async def chat_json(self, system_prompt: str, user_prompt: str) -> tuple[dict[str, Any], LLMResponse]:
        last_error: Exception | None = None
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json', 'HTTP-Referer': self.config.model.http_referer, 'X-Title': self.config.model.x_title}
        payload = {'model': self.config.model.model, 'temperature': self.config.model.temperature, 'messages': [{'role':'system','content':system_prompt},{'role':'user','content':user_prompt}], 'response_format': {'type':'json_object'}}
        for attempt in range(self.config.model.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.config.model.timeout_seconds) as client:
                    resp = await client.post(self.config.model.endpoint, headers=headers, json=payload)
                    resp.raise_for_status(); data = resp.json()
                content = data['choices'][0]['message']['content']
                usage = data.get('usage', {}) or {}
                llm_resp = LLMResponse(content=content, input_tokens=int(usage.get('prompt_tokens') or 0), output_tokens=int(usage.get('completion_tokens') or 0))
                return extract_json_object(content), llm_resp
            except Exception as exc:
                last_error = exc; await asyncio.sleep(1 + attempt)
        raise RuntimeError(f'OpenRouter falló luego de reintentos: {last_error}')
