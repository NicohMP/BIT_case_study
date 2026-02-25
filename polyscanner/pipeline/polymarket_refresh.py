"""End-to-end refresh pipeline for Polymarket scanning.

This is the operational glue for scheduled runs (cron, job runner, web backend):
1) Step 1: ingest active events + markets from Gamma `/events`
2) Step 2: run hard filters and persist `pm_market_filter_decision`
3) Step 3: run signal-family matching and persist `pm_market_signal_family_match`

Downstream services (LLM and/or web UI) should query the Postgres tables produced
by these steps rather than re-hitting the Gamma API.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from polyscanner.clients.gamma import GAMMA_BASE_URL_DEFAULT
from polyscanner.filtering.runner import HardFilterRunResult, run_hard_filters
from polyscanner.ingestion.gamma_events_ingest import ingest_active_events_and_markets
from polyscanner.matching.matcher import run_family_matching


@dataclass(frozen=True)
class RefreshResult:
    ingestion: dict[str, Any]
    hard_filters: dict[str, Any]
    matching: dict[str, Any]


def run_polymarket_refresh(
    *,
    db_url: str,
    base_url: str | None = None,
    # Step 1 (ingestion)
    ingest_limit: int = 100,
    ingest_max_pages: int | None = None,
    ingest_sleep_s: float = 0.2,
    ingest_since_ts: str | None = None,
    ingest_timeout_s: float = 30.0,
    # Step 2 (hard filters)
    hard_filters_limit: int | None = None,
    hard_filters_batch_size: int = 1000,
    # Step 3 (family matching)
    matcher_version: str = "matcher_v1",
    match_limit: int = 5000,
    use_embeddings: bool = True,
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    embedding_device: str | None = None,
    embedding_top_k: int = 5,
    embedding_min_similarity: float = 0.40,
    lexical_min_score: float = 0.30,
    classification_min_score: float = 0.70,
    out_dir: str = "reports",
) -> RefreshResult:
    """Run Steps 1→3 sequentially and return a structured summary."""
    base_url = (base_url or GAMMA_BASE_URL_DEFAULT).strip()

    ing = ingest_active_events_and_markets(
        limit=int(ingest_limit),
        max_pages=ingest_max_pages,
        sleep_s=float(ingest_sleep_s),
        since_ts=ingest_since_ts,
        db_url=db_url,
        base_url=base_url,
        timeout_s=float(ingest_timeout_s),
    )

    hf: HardFilterRunResult = run_hard_filters(
        db_url=db_url,
        limit=hard_filters_limit,
        batch_size=int(hard_filters_batch_size),
        out_dir=out_dir,
    )

    matching = run_family_matching(
        db_url=db_url,
        filter_version=str(hf.filter_version),
        matcher_version=str(matcher_version),
        limit=int(match_limit),
        use_embeddings=bool(use_embeddings),
        embedding_model=str(embedding_model),
        embedding_device=embedding_device,
        embedding_top_k=int(embedding_top_k),
        embedding_min_similarity=float(embedding_min_similarity),
        lexical_min_score=float(lexical_min_score),
        classification_min_score=float(classification_min_score),
        out_dir=str(out_dir),
    )

    return RefreshResult(
        ingestion={
            "events_upserted": ing.events_upserted,
            "markets_upserted": ing.markets_upserted,
            "pages": ing.pages,
            "last_offset": ing.last_offset,
            "runtime_s": ing.runtime_s,
        },
        hard_filters=asdict(hf),
        matching=dict(matching),
    )

