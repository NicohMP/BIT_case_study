#!/usr/bin/env python3
"""CLI helper: coverage-first ingestion from Gamma `/events`.

Usage:
  python scripts/ingest_active_events.py --limit 100 --max-pages 200
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.clients.gamma import GAMMA_BASE_URL_DEFAULT
from polyscanner.db.pg import connect
from polyscanner.env import get_env, load_env
from polyscanner.ingestion.gamma_events_ingest import ingest_active_events_and_markets


def _count_active_events(conn) -> int:
    with conn.cursor() as cur:
        cur.execute("select count(*) from pm_event where active = true and closed = false;")
        row = cur.fetchone()
    return int(row[0] or 0) if row else 0


def _count_active_markets_joined(conn) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            select count(*)
            from pm_market m
            join pm_event e on e.event_id = m.event_id
            where e.active = true and e.closed = false;
            """
        )
        row = cur.fetchone()
    return int(row[0] or 0) if row else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest all active Polymarket events and markets via /events.")
    parser.add_argument("--limit", type=int, default=100, help="Pagination page size (limit).")
    parser.add_argument("--max-pages", type=int, default=None, help="Optional cap on pages ingested.")
    parser.add_argument("--sleep-s", type=float, default=0.2, help="Sleep seconds between pages.")
    parser.add_argument("--since-ts", type=str, default=None, help="Optional ISO8601 timestamp for incremental ingest.")
    parser.add_argument("--timeout-s", type=float, default=30.0, help="HTTP timeout per request.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    base_url = get_env("POLYMARKET_API_BASE_URL") or GAMMA_BASE_URL_DEFAULT

    result = ingest_active_events_and_markets(
        int(args.limit),
        max_pages=args.max_pages,
        sleep_s=float(args.sleep_s),
        since_ts=args.since_ts,
        db_url=db_url,
        base_url=base_url,
        timeout_s=float(args.timeout_s),
    )

    print(
        "ingest_active_events_and_markets:",
        {
            "events_upserted": result.events_upserted,
            "markets_upserted": result.markets_upserted,
            "pages": result.pages,
            "last_offset": result.last_offset,
            "runtime_s": round(result.runtime_s, 3),
        },
    )

    conn = connect(db_url)
    try:
        n_events = _count_active_events(conn)
        n_markets = _count_active_markets_joined(conn)
        print("qc:", {"active_events": n_events, "active_markets_joined": n_markets})
    finally:
        conn.close()


if __name__ == "__main__":
    main()
