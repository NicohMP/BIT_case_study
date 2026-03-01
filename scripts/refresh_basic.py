#!/usr/bin/env python3
"""Run a default end-to-end refresh (Steps 1→4b) with embeddings disabled.

This is intended as the simplest "first run" command:
  ./venv/bin/python scripts/refresh_basic.py
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.clients.gamma import GAMMA_BASE_URL_DEFAULT  # noqa: E402
from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.pipeline.polymarket_refresh import run_polymarket_refresh  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Run Steps 1→4b with embeddings disabled (first-run friendly).")
    p.add_argument("--ingest-limit", type=int, default=100, help="Gamma /events page size (limit).")
    p.add_argument("--ingest-max-pages", type=int, default=200, help="Cap on number of /events pages.")
    p.add_argument("--ingest-sleep-s", type=float, default=0.2, help="Sleep seconds between /events pages.")
    p.add_argument("--timeout-s", type=float, default=30.0, help="HTTP timeout per request.")
    p.add_argument("--match-limit", type=int, default=12000, help="Max kept markets to evaluate in Step 3.")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = (get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    base_url = (get_env("POLYMARKET_API_BASE_URL") or GAMMA_BASE_URL_DEFAULT).strip()

    out = run_polymarket_refresh(
        db_url=db_url,
        base_url=base_url,
        ingest_limit=int(args.ingest_limit),
        ingest_max_pages=int(args.ingest_max_pages),
        ingest_sleep_s=float(args.ingest_sleep_s),
        ingest_timeout_s=float(args.timeout_s),
        matcher_version="matcher_v10",
        match_limit=int(args.match_limit),
        scoring_version="relevance_v5",
        trusted_only=True,
        persist_selection=True,
        selection_version="selected_v1",
        use_embeddings=False,
        run_audit=True,
    )

    print(
        "refresh_basic:",
        {
            "run_id": out.run_id,
            "ingestion": out.ingestion,
            "hard_filters": out.hard_filters,
            "matching": out.matching,
            "relevance_scoring": out.relevance_scoring,
            "relevance_selection": out.relevance_selection,
            "pipeline_audit": out.pipeline_audit,
        },
    )


if __name__ == "__main__":
    main()
