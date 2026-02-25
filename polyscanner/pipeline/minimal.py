"""Minimal end-to-end pipeline (notebook-friendly).

This file is only the orchestrator ("glue code").
Implementation details live in:
- `polyscanner.db.pg` (read BIT domains)
- `polyscanner.db.pg` (fetch ingested markets)
- `polyscanner.relevance.domain_relevance` (domain relevance)
- `polyscanner.relevance.channels` (channel relevance)
- `polyscanner.relevance.final_score` (combine relevance + exposures)
- `polyscanner.llm.domain_mapping` (LLM mapping prompt)
- `polyscanner.reporting.markdown` (render + write report)
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from polyscanner.db.pg import fetch_domain_definitions, fetch_pm_active_markets_for_scoring
from polyscanner.env import get_env, load_env
from polyscanner.filtering.hard_filters import load_hard_filter_rules
from polyscanner.llm.domain_mapping import assign_domains_with_gemini_from_scored
from polyscanner.models import PMMarket
from polyscanner.relevance.final_score import rank_markets, to_jsonable
from polyscanner.reporting.markdown import render_scored_signal_report_markdown, write_report_markdown


def run_minimal_pipeline(
    *,
    db_url: str | None = None,
    top_n: int = 10,
    markets_limit: int = 200,
    out_dir: str = "reports",
    use_llm: bool = True,
    prefer_embeddings: bool = True,
    hard_filter_version: str | None = None,
) -> dict[str, Any]:
    """Run the minimal pipeline and write a markdown report.

    Returns a dict containing:
    - report_path
    - report_md
    - domains
    - ranked_markets
    - llm_result
    """
    load_env()

    db_url = (db_url or get_env("DATABASE_URL"))
    if not db_url:
        raise RuntimeError("DATABASE_URL is required (pass db_url=... or set it in .env)")
    db_url = db_url.strip()
    # Accept SQLAlchemy-style URLs (common in local .env files).
    db_url = db_url.replace("postgresql+psycopg://", "postgresql://")

    domains = fetch_domain_definitions(db_url)
    if not domains:
        raise RuntimeError("No domains found in bit_domain; seed domains first.")
    if any((not d.description.strip()) for d in domains):
        raise RuntimeError("bit_domain.description is empty for some domains; run the domain definitions migration.")

    # Transmission channels are currently optional; we can rank on domain relevance only.
    exp_mx = {}

    # Market universe comes from the coverage-first ingestion tables (pm_event/pm_market),
    # optionally applying the Step-2 hard filters.
    if hard_filter_version is None:
        hard_filter_version = load_hard_filter_rules().filter_version

    rows = fetch_pm_active_markets_for_scoring(
        db_url,
        limit=int(markets_limit),
        min_volume_usd=None,
        hard_filter_version=hard_filter_version,
    )
    markets: list[PMMarket] = []
    for r in rows:
        markets.append(
            PMMarket(
                pm_market_id=int(r["pm_market_id"]),
                question=str(r.get("question") or ""),
                category=str(r["category"]) if r.get("category") is not None else None,
                probability=float(r["probability"]) if r.get("probability") is not None else None,
                volume=float(r["volume_usd"]) if r.get("volume_usd") is not None else None,
                raw={},
            )
        )
    if not markets:
        raise RuntimeError(
            "No active markets found in pm_event/pm_market for this hard_filter_version. "
            "Run `scripts/ingest_active_events.py` then `scripts/run_hard_filters.py` first."
        )
    scored = rank_markets(
        markets,
        domains,
        exp_mx,
        top_n=top_n,
        prefer_embeddings=prefer_embeddings,
        embedding_model_name=get_env("EMBEDDING_MODEL") or "all-MiniLM-L6-v2",
        embedding_device=get_env("EMBEDDING_DEVICE"),
    )
    scored_items = [to_jsonable(sm) for sm in scored]

    as_of = datetime.now(timezone.utc)
    if use_llm:
        llm_result = assign_domains_with_gemini_from_scored(scored_items, domains)
    else:
        llm_result = {
            "title": f"Signal Report — {as_of.date().isoformat()}",
            "items": [
                {
                    "pm_market_id": it["pm_market_id"],
                    "domain": it.get("best_domain") or "Unknown",
                    "confidence": 0.0,
                    "rationale": "Heuristic-only (LLM disabled).",
                }
                for it in scored_items
            ],
        }
    report_md = render_scored_signal_report_markdown(
        as_of=as_of,
        domains=domains,
        scored_items=scored_items,
        llm_result=llm_result,
    )
    report_path = write_report_markdown(report_md=report_md, out_dir=out_dir, as_of=as_of)

    return {
        "report_path": report_path,
        "report_md": report_md,
        "domains": [asdict(d) for d in domains],
        "scored_markets": scored_items,
        "llm_result": llm_result,
    }
