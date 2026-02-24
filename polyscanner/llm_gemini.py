"""Gemini (Google AI Studio) client helpers.

Loads `GOOGLE_API_KEY` from environment (typically via `.env`) and calls the
Generative Language API (Gemini) using plain HTTP.

Why this module exists:
- Keep report generation provider-specific code isolated.
- Avoid adding heavyweight dependencies for the case study.

Env vars:
- GOOGLE_API_KEY (preferred) or LLM_API_KEY (fallback)
- GEMINI_MODEL or LLM_MODEL (fallback)
"""

from __future__ import annotations

import json
import os
import random
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
    load_dotenv = None  # type: ignore[assignment]


class GeminiError(RuntimeError):
    pass


def _env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def get_api_key() -> str:
    if load_dotenv is not None:
        load_dotenv(override=False)
    key = _env("GOOGLE_API_KEY") or _env("LLM_API_KEY")
    if not key:
        raise GeminiError("Missing GOOGLE_API_KEY (or LLM_API_KEY) in environment/.env")
    return key


def get_model() -> str:
    if load_dotenv is not None:
        load_dotenv(override=False)
    return _env("GEMINI_MODEL") or _env("LLM_MODEL") or "gemini-2.0-flash"


def generate_json(
    *,
    prompt: str,
    system: str | None = None,
    model: str | None = None,
    temperature: float = 0.3,
    timeout_s: int = 60,
    max_retries: int = 6,
    retry_base_s: float = 1.5,
) -> dict[str, Any]:
    """Call Gemini and return a parsed JSON object.

    The prompt should instruct the model to return a single JSON object.
    """
    key = get_api_key()
    model = model or get_model()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    params = {"key": key}

    payload: dict[str, Any] = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": float(temperature),
            # Best-effort hint; if unsupported, Gemini will still return text.
            "responseMimeType": "application/json",
        },
    }
    if system:
        payload["systemInstruction"] = {"parts": [{"text": system}]}

    full_url = f"{url}?{urlencode(params)}"
    data_bytes = json.dumps(payload).encode("utf-8")

    last_err: Exception | None = None
    for attempt in range(max_retries + 1):
        req = Request(
            full_url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(req, timeout=timeout_s) as resp:
                body = resp.read().decode("utf-8")
            last_err = None
            break
        except HTTPError as e:
            last_err = e
            # 429 (rate/capacity) and 5xx are often transient: retry with backoff.
            if e.code in {429, 500, 502, 503, 504} and attempt < max_retries:
                retry_after = None
                try:
                    retry_after = e.headers.get("Retry-After")
                except Exception:
                    retry_after = None

                if retry_after:
                    try:
                        sleep_s = float(retry_after)
                    except ValueError:
                        sleep_s = retry_base_s * (2**attempt)
                else:
                    sleep_s = retry_base_s * (2**attempt)

                # add small jitter
                sleep_s = sleep_s + random.uniform(0.0, min(0.25 * sleep_s, 2.0))
                time.sleep(sleep_s)
                continue

            err_body = e.read().decode("utf-8") if hasattr(e, "read") else str(e)
            raise GeminiError(f"Gemini error {e.code}: {err_body[:1000]}") from e
        except URLError as e:
            last_err = e
            if attempt < max_retries:
                sleep_s = retry_base_s * (2**attempt) + random.uniform(0.0, 0.5)
                time.sleep(sleep_s)
                continue
            raise GeminiError(f"Gemini request failed: {e}") from e

    if last_err is not None:
        raise GeminiError(f"Gemini request failed after retries: {last_err}") from last_err

    data = json.loads(body)
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:  # noqa: BLE001
        raise GeminiError(f"Unexpected Gemini response shape: {e}; body={data}") from e

    # Parse JSON with a small robustness fallback (strip accidental prose).
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise GeminiError(f"Gemini did not return JSON. Text={text[:500]}")
        parsed = json.loads(text[start : end + 1])

    if not isinstance(parsed, dict):
        raise GeminiError("Gemini JSON response was not an object")

    parsed["_raw"] = data
    return parsed
