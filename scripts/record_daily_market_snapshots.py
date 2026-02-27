#!/usr/bin/env python3
"""Record daily market snapshots (MVP storage for later Δp / g(m)).

Usage:
  ./venv/bin/python scripts/record_daily_market_snapshots.py --scope kept
  ./venv/bin/python scripts/record_daily_market_snapshots.py --scope kept --filter-version hard_filters_v8
  ./venv/bin/python scripts/record_daily_market_snapshots.py --scope all --limit 5000
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.snapshots.daily_market_snapshot import record_daily_market_snapshots  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Record one daily snapshot row per selected market.")
    p.add_argument("--scope", type=str, default="kept", choices=["kept", "all"])
    p.add_argument("--filter-version", type=str, default=None, help="Required for --scope kept if no pipeline run tracking exists.")
    p.add_argument("--snapshot-date", type=str, default=None, help="Optional UTC date YYYY-MM-DD (default: today UTC).")
    p.add_argument("--limit", type=int, default=None, help="Optional cap on markets snapshotted.")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = (get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    snap_d: date | None = None
    if args.snapshot_date:
        snap_d = date.fromisoformat(str(args.snapshot_date))

    out = record_daily_market_snapshots(
        db_url=db_url,
        snapshot_date=snap_d,
        scope=str(args.scope),  # type: ignore[arg-type]
        filter_version=args.filter_version,
        run_id=None,
        limit=args.limit,
    )
    print(
        "daily_market_snapshots:",
        {
            "snapshot_date": out.snapshot_date,
            "scope": out.scope,
            "filter_version": out.filter_version,
            "markets_selected": out.markets_selected,
            "rows_upserted": out.rows_upserted,
            "runtime_s": out.runtime_s,
        },
    )


if __name__ == "__main__":
    main()

