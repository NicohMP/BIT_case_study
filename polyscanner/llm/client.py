from __future__ import annotations

from typing import Any

from polyscanner.env import get_env, load_env
from polyscanner.llm import gemini as gemini_client
from polyscanner.llm import ollama as ollama_client


class LlmBackendError(RuntimeError):
    pass


def get_backend() -> str:
    load_env()
    return (get_env("LLM_BACKEND") or "gemini").strip().lower()


def get_model(*, backend: str) -> str:
    b = (backend or "").strip().lower()
    if b == "ollama":
        return ollama_client.get_model()
    return gemini_client.get_model()


def list_backends() -> list[str]:
    return ["gemini", "ollama"]


def generate_json(
    *,
    prompt: str,
    system: str | None = None,
    backend: str | None = None,
    model: str | None = None,
    temperature: float = 0.3,
    timeout_s: int = 60,
    max_retries: int = 6,
    retry_base_s: float = 1.5,
    retry_max_s: float = 120.0,
) -> dict[str, Any]:
    b = (backend or get_backend()).strip().lower()
    if not model:
        model = get_model(backend=b)
    if b == "ollama":
        return ollama_client.generate_json(
            prompt=prompt,
            system=system,
            model=model,
            temperature=temperature,
            timeout_s=timeout_s,
            max_retries=max_retries,
            retry_base_s=retry_base_s,
            retry_max_s=retry_max_s,
        )
    if b == "gemini":
        return gemini_client.generate_json(
            prompt=prompt,
            system=system,
            model=model,
            temperature=temperature,
            timeout_s=timeout_s,
            max_retries=max_retries,
            retry_base_s=retry_base_s,
            retry_max_s=retry_max_s,
        )
    raise LlmBackendError(f"Unknown LLM backend: {b!r} (expected 'gemini' or 'ollama')")
