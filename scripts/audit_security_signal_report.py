#!/usr/bin/env python3
"""Step 5e: Audit a generated LLM report against its context pack."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.reporting.security_signal_report_audit import (  # noqa: E402
    audit_security_signal_report,
    render_security_signal_report_audit_markdown,
)


def _utc_ts() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")


def main() -> None:
    p = argparse.ArgumentParser(description="Audit Step-5 security signal report JSON for grounding/consistency.")
    p.add_argument("--pack", type=str, required=True, help="Path to context pack JSON.")
    p.add_argument("--report-json", type=str, required=True, help="Path to generated report JSON.")
    p.add_argument("--max-markets", type=int, default=10)
    p.add_argument("--max-rate-like", type=int, default=3)
    p.add_argument("--out", type=str, default=None, help="Output markdown path (default: reports/security_report_audit_*.md).")
    args = p.parse_args()

    pack = json.loads(Path(args.pack).read_text(encoding="utf-8"))
    report = json.loads(Path(args.report_json).read_text(encoding="utf-8"))

    issues = audit_security_signal_report(
        report=report,
        pack=pack,
        max_markets=int(args.max_markets),
        max_rate_like=int(args.max_rate_like),
    )
    md = render_security_signal_report_audit_markdown(issues=issues)

    out = args.out
    if not out:
        sec = (report.get("security") or {}) if isinstance(report, dict) else {}
        ticker = str(sec.get("ticker") or "SEC")
        out = str(Path("reports") / f"security_signal_report_audit_{ticker}_{_utc_ts()}.md")
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")

    errors = len([x for x in issues if x.level == "error"])
    warnings = len([x for x in issues if x.level == "warning"])
    print({"out_path": str(out_path), "errors": errors, "warnings": warnings})
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

