#!/usr/bin/env python3
"""Step 5d: Render a security signal report JSON to analyst markdown."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.reporting.security_signal_report_markdown import render_security_signal_report_markdown  # noqa: E402


def _utc_ts() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")


def main() -> None:
    p = argparse.ArgumentParser(description="Render Step-5 security signal report JSON to markdown.")
    p.add_argument("--report-json", type=str, required=True, help="Path to report JSON produced by generate_security_signal_report.py")
    p.add_argument("--out", type=str, default=None, help="Output markdown path (default: reports/security_signal_report_*.md).")
    args = p.parse_args()

    report_path = Path(args.report_json)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    md = render_security_signal_report_markdown(report=report)

    out = args.out
    if not out:
        sec = report.get("security") or {}
        ticker = str(sec.get("ticker") or "SEC")
        out = str(Path("reports") / f"security_signal_report_{ticker}_{_utc_ts()}.md")
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print({"out_path": str(out_path)})


if __name__ == "__main__":
    main()

