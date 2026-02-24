"""CLI helper: ingest Polymarket markets into Postgres.

Usage:
  python3 scripts/ingest_pm_markets.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.env import get_env, load_env
from polyscanner.ingestion.pm_markets import ingest_active_pm_markets


def main() -> None:
    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    base_url = get_env("POLYMARKET_API_BASE_URL") or "https://gamma-api.polymarket.com"

    out = ingest_active_pm_markets(db_url=db_url, base_url=base_url, limit=int(get_env("PM_MARKETS_LIMIT") or "200"))
    print(out)


if __name__ == "__main__":
    main()
