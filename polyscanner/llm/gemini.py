"""Gemini (Google AI Studio) client helpers.

Loads `GOOGLE_API_KEY` from environment (typically via `.env`) and calls the
Generative Language API (Gemini) using plain HTTP.
"""

from __future__ import annotations

import json
import random
import re
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from polyscanner.env import get_env, load_env


class GeminiError(RuntimeError):
    pass


def get_api_key() -> str:
    load_env()
    key = get_env("GOOGLE_API_KEY") or get_env("LLM_API_KEY")
    if not key:
        raise GeminiError("Missing GOOGLE_API_KEY (or LLM_API_KEY) in environment/.env")
    return key


def get_model() -> str:
    load_env()
    return get_env("GEMINI_MODEL") or get_env("LLM_MODEL") or "gemini-2.0-flash"


def _strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if not t.startswith("```"):
        return t
    # Remove leading ```json (or any language tag) and trailing ```
    t = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


def _extract_first_json_substring(text: str) -> str | None:
    """Extract the first JSON object/array substring using bracket matching.

    Gemini sometimes adds preambles/epilogues (despite JSON mode). This attempts
    to recover the first well-formed {...} or [...] block while correctly
    handling strings and escapes.
    """
    t = _strip_code_fences(text)
    start = None
    for i, ch in enumerate(t):
        if ch in "{[":
            start = i
            break
    if start is None:
        return None

    stack: list[str] = []
    in_str = False
    esc = False

    for j in range(start, len(t)):
        ch = t[j]

        if in_str:
            if esc:
                esc = False
                continue
            if ch == "\\":
                esc = True
                continue
            if ch == '"':
                in_str = False
            continue

        if ch == '"':
            in_str = True
            continue

        if ch in "{[":
            stack.append(ch)
            continue
        if ch in "}]":
            if not stack:
                continue
            top = stack[-1]
            if (top == "{" and ch == "}") or (top == "[" and ch == "]"):
                stack.pop()
                if not stack:
                    return t[start : j + 1]
            else:
                # Mismatched close; keep scanning.
                continue

    return None


def _remove_trailing_commas(text: str) -> str:
    # Remove trailing commas before } or ]
    return re.sub(r",(\s*[}\]])", r"\1", text)


def _parse_json_object(text: str) -> dict[str, Any]:
    """Parse a JSON object, applying minimal safe repairs for common Gemini slips."""
    raw = _strip_code_fences(text)

    # 1) Strict parse as-is.
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = None

    # 2) Extract the first JSON substring (if the model added extra text).
    if parsed is None:
        sub = _extract_first_json_substring(raw)
        if sub is not None:
            try:
                parsed = json.loads(sub)
            except json.JSONDecodeError:
                parsed = None

    # 3) Minimal repair: trailing commas are the most common invalid-JSON failure.
    if parsed is None:
        sub = _extract_first_json_substring(raw) or raw
        parsed = json.loads(_remove_trailing_commas(sub))

    if not isinstance(parsed, dict):
        raise GeminiError("Gemini JSON response was not an object")
    return parsed


def generate_json(
    *,
    prompt: str,
    system: str | None = None,
    model: str | None = None,
    temperature: float = 0.3,
    timeout_s: int = 60,
    max_retries: int = 6,
    retry_base_s: float = 1.5,
    retry_max_s: float | None = None,
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

                if retry_max_s is not None:
                    sleep_s = min(sleep_s, float(retry_max_s))
                sleep_s = sleep_s + random.uniform(0.0, min(0.25 * sleep_s, 2.0))
                time.sleep(sleep_s)
                continue

            err_body = e.read().decode("utf-8") if hasattr(e, "read") else str(e)
            raise GeminiError(f"Gemini error {e.code}: {err_body[:1000]}") from e
        except URLError as e:
            last_err = e
            if attempt < max_retries:
                sleep_s = retry_base_s * (2**attempt) + random.uniform(0.0, 0.5)
                if retry_max_s is not None:
                    sleep_s = min(sleep_s, float(retry_max_s))
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

    try:
        parsed = _parse_json_object(text)
    except Exception as e:  # noqa: BLE001
        snippet = _strip_code_fences(text)
        head = snippet[:800]
        tail = snippet[-800:] if len(snippet) > 800 else ""
        msg = f"Gemini returned invalid JSON: {e}. head={head!r}"
        if tail:
            msg += f" tail={tail!r}"
        raise GeminiError(msg) from e

    parsed["_raw"] = data
    return parsed
