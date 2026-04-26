from __future__ import annotations

import html
import re

MOJIBAKE_HINTS = ("Ã", "Â", "â€", "â€œ", "â€�", "â€“", "â€”", "�")


def fix_mojibake(text: str) -> str:
    """Intenta reparar texto UTF-8 leído erróneamente como Latin-1/Windows-1252."""
    if not text:
        return text

    candidate = text
    if any(x in candidate for x in MOJIBAKE_HINTS):
        try:
            repaired = candidate.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
            if repaired and repaired.count("�") <= candidate.count("�"):
                candidate = repaired
        except Exception:
            pass

    replacements = {
        "â€œ": "“",
        "â€�": "”",
        "â€˜": "‘",
        "â€™": "’",
        "â€“": "–",
        "â€”": "—",
        "Â¿": "¿",
        "Â¡": "¡",
        "Â°": "°",
        "Â ": " ",
        "Â": "",
    }
    for bad, good in replacements.items():
        candidate = candidate.replace(bad, good)

    return candidate


def clean_visible_spanish_text(text: str) -> str:
    """Limpia respuestas del modelo antes de reinyectarlas al HTML."""
    if text is None:
        return ""

    value = str(text).strip()
    value = html.unescape(value)
    value = fix_mojibake(value)
    value = value.replace("\ufeff", "")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\s+\n", "\n", value)
    return value.strip()
