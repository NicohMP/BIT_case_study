"""Ollama (local) client helper.

This is a fallback backend for report-time LLM generation when hosted APIs are throttled.
It calls the local Ollama server (default: http://127.0.0.1:11434) and requests JSON-only output.
"""

from __future__ import annotations

import json
import random
import time
from typing import Any

import requests

from polyscanner.env import get_env, load_env
from polyscanner.llm.json_parse import parse_json_object, strip_code_fences


class OllamaError(RuntimeError):
    pass


def get_base_url() -> str:
    load_env()
    return (get_env("OLLAMA_BASE_URL") or "http://127.0.0.1:11434").rstrip("/")


def get_model() -> str:
    load_env()
    return get_env("OLLAMA_MODEL") or "qwen2.5:7b-instruct"


def generate_json(
    *,
    prompt: str,
    system: str | None = None,
    model: str | None = None,
    temperature: float = 0.2,
    timeout_s: int = 120,
    max_retries: int = 2,
    retry_base_s: float = 2.0,
    retry_max_s: float = 30.0,
) -> dict[str, Any]:
    base_url = get_base_url()
    model = model or get_model()

    payload: dict[str, Any] = {
        "model": str(model),
        "stream": False,
        "messages": [],
        "format": "json",
        "options": {
            "temperature": float(temperature),
        },
    }
    if system:
        payload["messages"].append({"role": "system", "content": str(system)})
    payload["messages"].append({"role": "user", "content": str(prompt)})

    last_err: Exception | None = None
    for attempt in range(int(max_retries) + 1):
        try:
            resp = requests.post(
                f"{base_url}/api/chat",
                json=payload,
                timeout=float(timeout_s),
            )
            if resp.status_code >= 400:
                raise OllamaError(f"Ollama error {resp.status_code}: {resp.text[:1000]}")
            data = resp.json()
            last_err = None
            break
        except (requests.RequestException, OllamaError) as e:
            last_err = e
            if attempt < int(max_retries):
                sleep_s = min(float(retry_base_s) * (2**attempt), float(retry_max_s))
                sleep_s = sleep_s + random.uniform(0.0, min(0.25 * sleep_s, 1.5))
                time.sleep(sleep_s)
                continue
            raise OllamaError(
                f"Ollama request failed: {e}. Is Ollama running (and reachable at {base_url}) and is the model pulled?"
            ) from e

    if last_err is not None:
        raise OllamaError(f"Ollama request failed after retries: {last_err}") from last_err

    try:
        text = data["message"]["content"]
    except Exception as e:  # noqa: BLE001
        raise OllamaError(f"Unexpected Ollama response shape: {e}; body={data}") from e

    try:
        parsed = parse_json_object(text)
    except Exception as e:  # noqa: BLE001
        snippet = strip_code_fences(text)
        head = snippet[:800]
        tail = snippet[-800:] if len(snippet) > 800 else ""
        msg = f"Ollama returned invalid JSON: {e}. head={head!r}"
        if tail:
            msg += f" tail={tail!r}"
        raise OllamaError(msg) from e

    parsed["_raw"] = data
    return parsed

