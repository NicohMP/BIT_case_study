#!/usr/bin/env python3
"""Step 5b: Validate a context pack before LLM calls."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.reporting.security_report_validation import validate_context_pack  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Validate Step-5 security context pack JSON.")
    p.add_argument("--pack", type=str, required=True, help="Path to context pack JSON produced by build_security_report_pack.py")
    args = p.parse_args()

    pack_path = Path(args.pack)
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    issues = validate_context_pack(pack)

    errors = [x for x in issues if x.level == "error"]
    warnings = [x for x in issues if x.level == "warning"]

    for it in issues:
        loc = f" ({it.path})" if it.path else ""
        print(f"[{it.level.upper()}] {it.message}{loc}")

    print({"errors": len(errors), "warnings": len(warnings)})
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

