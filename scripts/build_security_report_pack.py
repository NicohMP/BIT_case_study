#!/usr/bin/env python3
"""Step 5a: Build a deterministic context pack for the LLM (single security).

Usage:
  ./venv/bin/python scripts/build_security_report_pack.py --ticker NVDA
  ./venv/bin/python scripts/build_security_report_pack.py --security-id 12
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.reporting.security_report_pack import Versions, build_security_context_pack  # noqa: E402


def _utc_ts() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")


def main() -> None:
    p = argparse.ArgumentParser(description="Build Step-5 LLM context pack for one security (deterministic).")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--ticker", type=str, default=None, help="Security ticker (e.g. NVDA).")
    g.add_argument("--security-id", type=int, default=None, help="bit_security.id")
    p.add_argument("--exchange-mic", type=str, default=None, help="Exchange MIC (required if ticker is ambiguous).")

    p.add_argument("--top-k-markets", type=int, default=20, help="How many selected markets to include (from Step 4b).")
    p.add_argument("--top-k-matches-per-market", type=int, default=5, help="How many family matches per market to include.")
    p.add_argument("--out", type=str, default=None, help="Output JSON file path (default: reports/context_pack_*.json).")

    # Optional explicit version override (otherwise uses latest successful pm_pipeline_run)
    p.add_argument("--filter-version", type=str, default=None)
    p.add_argument("--matcher-version", type=str, default=None)
    p.add_argument("--scoring-version", type=str, default=None)
    p.add_argument("--selection-version", type=str, default=None)
    p.add_argument("--run-id", type=str, default=None)

    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = (get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    versions = None
    if any([args.filter_version, args.matcher_version, args.scoring_version, args.selection_version]):
        missing = [k for k in ("filter_version", "matcher_version", "scoring_version", "selection_version") if getattr(args, k) is None]
        if missing:
            raise SystemExit(f"When overriding versions, you must provide all: {', '.join(missing)}")
        versions = Versions(
            run_id=args.run_id,
            filter_version=str(args.filter_version),
            matcher_version=str(args.matcher_version),
            scoring_version=str(args.scoring_version),
            selection_version=str(args.selection_version),
        )

    pack = build_security_context_pack(
        db_url=db_url,
        security_id=args.security_id,
        ticker=args.ticker,
        exchange_mic=args.exchange_mic,
        versions=versions,
        top_k_markets=int(args.top_k_markets),
        top_k_matches_per_market=int(args.top_k_matches_per_market),
    )

    out = args.out
    if not out:
        sec = pack.get("security") or {}
        ticker = str(sec.get("ticker") or "SEC")
        out = str(Path("reports") / f"context_pack_{ticker}_{_utc_ts()}.json")

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")

    pack_hash = (pack.get("report_meta") or {}).get("pack_sha256")
    print(
        "context_pack:",
        {
            "out_path": str(out_path),
            "pack_sha256": pack_hash,
            "security": pack.get("security"),
            "versions": (pack.get("report_meta") or {}).get("versions"),
            "n_markets": len(pack.get("markets") or []),
        },
    )


if __name__ == "__main__":
    main()

