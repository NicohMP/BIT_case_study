"""Ingest Polymarket markets into Postgres (Supabase).

Writes:
- `pm_market` (upsert latest state per market)
"""

from __future__ import annotations

import json
from typing import Any

from polyscanner.clients.polymarket_gamma import fetch_and_normalize_active_markets, normalize_market
from polyscanner.db.pg import connect
from polyscanner.models import PMMarket


def _normalize_db_url(db_url: str) -> str:
    return db_url.strip().replace("postgresql+psycopg://", "postgresql://")


def _market_row(m: PMMarket) -> dict[str, Any]:
    return {
        "pm_market_id": int(m.pm_market_id),
        "question": m.question,
        "category": m.category,
        "probability": m.probability,
        "volume_usd": m.volume,
        "raw_json": json.dumps(m.raw, ensure_ascii=False),
    }


def upsert_pm_markets(*, db_url: str, markets: list[PMMarket]) -> int:
    if not markets:
        return 0

    conn = connect(_normalize_db_url(db_url))
    try:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO pm_market (
                    pm_market_id,
                    question,
                    category,
                    probability,
                    volume_usd,
                    raw
                ) VALUES (
                    %(pm_market_id)s,
                    %(question)s,
                    %(category)s,
                    %(probability)s,
                    %(volume_usd)s,
                    %(raw_json)s::jsonb
                )
                ON CONFLICT (pm_market_id) DO UPDATE SET
                    question = EXCLUDED.question,
                    category = EXCLUDED.category,
                    probability = EXCLUDED.probability,
                    volume_usd = EXCLUDED.volume_usd,
                    raw = EXCLUDED.raw,
                    last_seen_at = NOW(),
                    updated_at = NOW()
                """,
                [_market_row(m) for m in markets],
            )
        conn.commit()
        return len(markets)
    finally:
        conn.close()


def ingest_active_pm_markets(
    *,
    db_url: str,
    base_url: str,
    limit: int = 200,
    offset: int = 0,
    timeout_s: int = 30,
) -> dict[str, Any]:
    markets = fetch_and_normalize_active_markets(
        base_url=base_url,
        limit=limit,
        offset=offset,
        timeout_s=timeout_s,
    )
    upserted = upsert_pm_markets(db_url=db_url, markets=markets)
    return {"fetched": len(markets), "upserted": upserted}


def ingest_markets_from_tag_ids(
    *,
    db_url: str,
    base_url: str,
    tag_ids: list[int],
    markets_cap_per_tag: int = 50,
    max_events_pages: int = 5,
    events_page_size: int = 50,
    sleep_s: float = 0.05,
) -> dict[str, Any]:
    """Fetch active markets for a curated tag allowlist and upsert into `pm_market`.

    Role in the pipeline:
    - The Gamma `/markets` listing is broad/noisy (sports/celebs dominate).
    - A curated tag allowlist provides a higher-signal retrieval set for macro/tech themes.
    - This function pulls markets *via tags* (using `/events?tag_id=...`) and stores the
      normalized markets into `pm_market` for downstream matching/reporting.
    """
    if not tag_ids:
        return {"tags": 0, "fetched_raw": 0, "normalized": 0, "upserted": 0}

    # Lazy import: `tag_base` is notebook-heavy (embeddings). Fetching by tag does not
    # require sentence-transformers, but keeping the import local avoids surprises.
    from polyscanner.ingestion.tag_base import fetch_markets_for_tag  # noqa: WPS433

    raw_by_market_id: dict[int, dict[str, Any]] = {}
    per_tag_counts: dict[int, int] = {}

    for tid in tag_ids:
        raw_markets = fetch_markets_for_tag(
            int(tid),
            base_url=base_url,
            markets_cap=int(markets_cap_per_tag),
            max_events_pages=int(max_events_pages),
            events_page_size=int(events_page_size),
            sleep_s=float(sleep_s),
        )
        per_tag_counts[int(tid)] = len(raw_markets)

        for rm in raw_markets:
            if not isinstance(rm, dict):
                continue
            mid = rm.get("id")
            if mid is None:
                continue
            try:
                mid_i = int(mid)
            except Exception:
                continue
            # Annotate provenance for debugging (stored inside raw JSONB).
            rm2 = dict(rm)
            rm2["_retrieved_by_tag_id"] = int(tid)
            raw_by_market_id.setdefault(mid_i, rm2)

    normalized: list[PMMarket] = []
    for rm in raw_by_market_id.values():
        try:
            nm = normalize_market(rm)
        except Exception:
            continue
        if nm.question:
            normalized.append(nm)

    upserted = upsert_pm_markets(db_url=db_url, markets=normalized)
    return {
        "tags": len(tag_ids),
        "per_tag_fetched": per_tag_counts,
        "fetched_raw": sum(per_tag_counts.values()),
        "unique_markets": len(raw_by_market_id),
        "normalized": len(normalized),
        "upserted": upserted,
    }
