#!/usr/bin/env python3
"""Launch the Polyscanner Web UI on http://127.0.0.1:8000.

Usage:
  ./venv/bin/python scripts/run_webui.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    try:
        import uvicorn  # type: ignore
    except Exception as e:  # noqa: BLE001
        raise SystemExit(
            "Missing dependency: uvicorn. Install it with:\n"
            "  ./venv/bin/pip install uvicorn\n"
            f"Original error: {e}"
        ) from e

    host = os.getenv("WEBUI_HOST") or "127.0.0.1"
    port = int(os.getenv("WEBUI_PORT") or "8000")
    log_level = os.getenv("WEBUI_LOG_LEVEL") or "info"

    uvicorn.run("polyscanner.webui.app:app", host=host, port=port, reload=False, log_level=log_level)


if __name__ == "__main__":
    main()

