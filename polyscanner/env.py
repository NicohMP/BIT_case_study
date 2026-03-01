"""Environment helpers.

We keep env access in one place so notebooks/scripts behave the same.

Conventions:
- Load `.env` if `python-dotenv` is installed.
- Prefer explicit function args, but allow env fallbacks for convenience.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
    load_dotenv = None  # type: ignore[assignment]

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_env() -> None:
    if load_dotenv is not None:
        load_dotenv(override=False)


def get_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def resolve_repo_relative(path: str | Path) -> Path:
    """Resolve a repo-relative path (relative to repo root) into an absolute Path."""
    p = Path(path)
    if p.is_absolute():
        return p
    return (REPO_ROOT / p).resolve()
