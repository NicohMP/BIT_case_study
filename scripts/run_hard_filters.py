#!/usr/bin/env python3
"""CLI wrapper for Step 2 hard filters.

Prefer importing `polyscanner.filtering.runner.run_hard_filters` from code.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.filtering.runner import run_hard_filters  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run deterministic hard filters and store auditable decisions.")
    parser.add_argument("--limit", type=int, default=None, help="Optional cap on number of markets evaluated.")
    parser.add_argument("--batch-size", type=int, default=1000, help="DB upsert batch size.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    res = run_hard_filters(
        db_url=db_url,
        limit=args.limit,
        batch_size=int(args.batch_size),
        out_dir="reports",
    )

    print(
        "hard_filters_run:",
        {
            "run_id": res.run_id,
            "filter_version": res.filter_version,
            "config_sha256": res.config_sha256[:12],
            "evaluated": res.evaluated,
            "rejected": res.rejected,
            "rejected_pct": round(100.0 * res.rejected / max(1, res.evaluated), 2),
            "audit_report": res.audit_report,
            "runtime_s": round(res.runtime_s, 3),
        },
    )
    top20 = dict(list(res.top_rejection_reasons.items())[:20])
    print("top_rejection_reasons:", top20)
    print("\ntop_kept_by_volume_usd:")
    for line in res.top_kept_by_volume_usd:
        print(line)
    print("\ntop_rejected_by_volume_usd:")
    for line in res.top_rejected_by_volume_usd:
        print(line)
    print("\nkept_high_relevance_examples:")
    for line in res.kept_high_relevance_examples:
        print(line)
    print("\nkept_low_quality_examples:")
    for line in res.kept_low_quality_examples:
        print(line)


if __name__ == "__main__":
    main()
