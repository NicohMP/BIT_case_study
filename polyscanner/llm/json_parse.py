from __future__ import annotations

import json
import re
from typing import Any


def strip_code_fences(text: str) -> str:
    t = (text or "").strip()
    if not t.startswith("```"):
        return t
    t = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


def extract_first_json_substring(text: str) -> str | None:
    """Extract the first JSON object/array substring using bracket matching."""
    t = strip_code_fences(text)
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
                continue

    return None


def remove_trailing_commas(text: str) -> str:
    return re.sub(r",(\s*[}\]])", r"\1", text)

def repair_invalid_escapes(text: str) -> str:
    """Repair invalid JSON escape sequences commonly produced by LLMs.

    LLMs sometimes emit backslashes in strings to mimic markdown escaping (e.g. '\\_')
    or produce malformed unicode escapes (e.g. '\\u12G4'). These are invalid JSON.

    This function is intentionally conservative: it only escapes backslashes that are
    not part of a valid JSON escape sequence, turning them into literal backslashes.
    """
    t = text
    # Malformed unicode escapes: \u must be followed by exactly 4 hex digits.
    t = re.sub(r"\\u(?![0-9a-fA-F]{4})", r"\\\\u", t)
    # Any other invalid escape (not one of \" \\ \/ \b \f \n \r \t \uXXXX).
    t = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", t)
    return t


def parse_json_object(text: str) -> dict[str, Any]:
    """Parse a JSON object, applying minimal safe repairs for common LLM slips."""
    raw = strip_code_fences(text)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = None

    if parsed is None:
        sub = extract_first_json_substring(raw)
        if sub is not None:
            try:
                parsed = json.loads(sub)
            except json.JSONDecodeError:
                # Try escape repair (e.g. '\_' or malformed '\uXXXX') then re-parse.
                try:
                    parsed = json.loads(repair_invalid_escapes(sub))
                except json.JSONDecodeError:
                    parsed = None

    if parsed is None:
        sub = extract_first_json_substring(raw) or raw
        sub2 = remove_trailing_commas(sub)
        try:
            parsed = json.loads(sub2)
        except json.JSONDecodeError:
            parsed = json.loads(repair_invalid_escapes(sub2))

    if not isinstance(parsed, dict):
        raise ValueError("LLM JSON response was not an object")
    return parsed
