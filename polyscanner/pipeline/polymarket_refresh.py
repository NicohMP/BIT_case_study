"""End-to-end refresh pipeline for Polymarket scanning.

This is the operational glue for scheduled runs (cron, job runner, web backend):
1) Step 1: ingest active events + markets from Gamma `/events`
2) Step 2: run hard filters and persist `pm_market_filter_decision`
3) Step 3: run signal-family matching and persist `pm_market_signal_family_match`
4) Step 4: compute security relevance and persist `pm_market_security_relevance`
5) Step 4b: persist diversified top-K per security in `pm_market_security_relevance_selection`
6) (Optional) write a single pipeline audit markdown

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
from polyscanner.pipeline.audit import run_pipeline_audit
from polyscanner.pipeline.run_tracking import (
    create_pipeline_run,
    new_run_id,
    pipeline_run_table_exists,
    update_pipeline_run,
)
from polyscanner.relevance.security_market_relevance import compute_market_security_relevance, persist_relevance_selection
from polyscanner.snapshots.daily_market_snapshot import record_daily_market_snapshots
from polyscanner.db.pg import connect


@dataclass(frozen=True)
class RefreshResult:
    run_id: str | None
    ingestion: dict[str, Any]
    hard_filters: dict[str, Any]
    matching: dict[str, Any]
    daily_snapshots: dict[str, Any] | None
    relevance_scoring: dict[str, Any] | None
    relevance_selection: dict[str, Any] | None
    pipeline_audit: dict[str, Any] | None


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
    match_limit: int = 12000,
    use_embeddings: bool = True,
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    embedding_device: str | None = None,
    embedding_top_k: int = 5,
    embedding_min_similarity: float = 0.40,
    lexical_min_score: float = 0.30,
    classification_min_score: float = 0.70,
    # Step 4 (relevance)
    scoring_version: str = "relevance_v1",
    trusted_only: bool = True,
    min_base_score: float = 0.0,
    # Step 4b (selection)
    persist_selection: bool = True,
    selection_version: str = "selected_v1",
    selection_k: int = 20,
    selection_max_per_event: int = 1,
    selection_max_rate_like: int = 3,
    # Daily snapshots (for later Δp / sentiment intensity)
    record_daily_snapshots: bool = False,
    snapshot_scope: str = "kept",  # kept | all
    snapshot_limit: int | None = None,
    # Optional pipeline audit
    run_audit: bool = True,
    audit_top_n: int = 20,
    out_dir: str = "reports",
) -> RefreshResult:
    """Run Steps 1→4b sequentially and return a structured summary."""
    base_url = (base_url or GAMMA_BASE_URL_DEFAULT).strip()

    run_id: str | None = None
    conn = connect(db_url)
    try:
        # Optional DB-backed run metadata.
        if pipeline_run_table_exists(conn):
            run_id = new_run_id()
            create_pipeline_run(
                conn,
                run_id=str(run_id),
                params={
                    "base_url": base_url,
                    "ingest_limit": int(ingest_limit),
                    "ingest_max_pages": ingest_max_pages,
                    "ingest_sleep_s": float(ingest_sleep_s),
                    "ingest_since_ts": ingest_since_ts,
                    "ingest_timeout_s": float(ingest_timeout_s),
                    "hard_filters_limit": hard_filters_limit,
                    "hard_filters_batch_size": int(hard_filters_batch_size),
                    "matcher_version": str(matcher_version),
                    "match_limit": int(match_limit),
                    "use_embeddings": bool(use_embeddings),
                    "embedding_model": str(embedding_model),
                    "embedding_device": embedding_device,
                    "embedding_top_k": int(embedding_top_k),
                    "embedding_min_similarity": float(embedding_min_similarity),
                    "lexical_min_score": float(lexical_min_score),
                    "classification_min_score": float(classification_min_score),
                    "scoring_version": str(scoring_version),
                    "trusted_only": bool(trusted_only),
                    "min_base_score": float(min_base_score),
                    "persist_selection": bool(persist_selection),
                    "selection_version": str(selection_version),
                    "selection_k": int(selection_k),
                    "selection_max_per_event": int(selection_max_per_event),
                    "selection_max_rate_like": int(selection_max_rate_like),
                    "run_audit": bool(run_audit),
                    "audit_top_n": int(audit_top_n),
                },
                status="running",
                matcher_version=str(matcher_version),
                scoring_version=str(scoring_version),
                selection_version=str(selection_version) if persist_selection else None,
            )

        ing = ingest_active_events_and_markets(
            limit=int(ingest_limit),
            max_pages=ingest_max_pages,
            sleep_s=float(ingest_sleep_s),
            since_ts=ingest_since_ts,
            db_url=db_url,
            base_url=base_url,
            timeout_s=float(ingest_timeout_s),
        )
        ingestion_summary = {
            "events_upserted": ing.events_upserted,
            "markets_upserted": ing.markets_upserted,
            "pages": ing.pages,
            "last_offset": ing.last_offset,
            "runtime_s": ing.runtime_s,
        }
        if run_id is not None:
            update_pipeline_run(conn, run_id=str(run_id), ingestion_summary=ingestion_summary)

        hf: HardFilterRunResult = run_hard_filters(
            db_url=db_url,
            limit=hard_filters_limit,
            batch_size=int(hard_filters_batch_size),
            out_dir=out_dir,
        )
        hard_filters_summary = asdict(hf)
        if run_id is not None:
            update_pipeline_run(
                conn,
                run_id=str(run_id),
                hard_filters_summary=hard_filters_summary,
                filter_version=str(hf.filter_version),
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
        matching_summary = dict(matching)
        if run_id is not None:
            update_pipeline_run(conn, run_id=str(run_id), matching_summary=matching_summary)

        daily_snapshots_summary: dict[str, Any] | None = None
        if record_daily_snapshots:
            snap = record_daily_market_snapshots(
                db_url=db_url,
                snapshot_date=None,
                scope=("kept" if str(snapshot_scope).strip().lower() != "all" else "all"),  # type: ignore[arg-type]
                filter_version=str(hf.filter_version) if str(snapshot_scope).strip().lower() != "all" else None,
                run_id=str(run_id) if run_id is not None else None,
                limit=snapshot_limit,
            )
            daily_snapshots_summary = {
                "snapshot_date": snap.snapshot_date,
                "scope": snap.scope,
                "filter_version": snap.filter_version,
                "markets_selected": snap.markets_selected,
                "rows_upserted": snap.rows_upserted,
                "runtime_s": snap.runtime_s,
            }

        rel = compute_market_security_relevance(
            db_url=db_url,
            matcher_version=str(matcher_version),
            scoring_version=str(scoring_version),
            filter_version=str(hf.filter_version),
            min_base_score=float(min_base_score),
            trusted_only=bool(trusted_only),
        )
        relevance_scoring_summary = {
            "scoring_version": rel.scoring_version,
            "filter_version": rel.filter_version,
            "matcher_version": rel.matcher_version,
            "securities_scored": rel.securities_scored,
            "markets_considered": rel.markets_considered,
            "rows_upserted": rel.rows_upserted,
            "runtime_s": rel.runtime_s,
        }
        if run_id is not None:
            update_pipeline_run(conn, run_id=str(run_id), scoring_summary=relevance_scoring_summary, scoring_version=str(rel.scoring_version))

        relevance_selection_summary: dict[str, Any] | None = None
        if persist_selection:
            relevance_selection_summary = persist_relevance_selection(
                db_url=db_url,
                scoring_version=str(rel.scoring_version),
                filter_version=str(hf.filter_version),
                selection_version=str(selection_version),
                top_k=int(selection_k),
                max_per_event=int(selection_max_per_event),
                max_rate_like=int(selection_max_rate_like),
            )
            if run_id is not None:
                update_pipeline_run(
                    conn,
                    run_id=str(run_id),
                    selection_summary=relevance_selection_summary,
                    selection_version=str(selection_version),
                )

        audit_summary: dict[str, Any] | None = None
        if run_audit:
            audit = run_pipeline_audit(
                db_url=db_url,
                filter_version=str(hf.filter_version),
                matcher_version=str(matcher_version),
                scoring_version=str(rel.scoring_version),
                selection_version=str(selection_version) if persist_selection else None,
                out_dir=str(out_dir),
                top_n=int(audit_top_n),
            )
            audit_summary = {"markdown_path": audit.markdown_path}
            if run_id is not None:
                update_pipeline_run(conn, run_id=str(run_id), audit_summary=audit_summary)

        if run_id is not None:
            update_pipeline_run(conn, run_id=str(run_id), status="success", finished_at="now")

        return RefreshResult(
            run_id=run_id,
            ingestion=ingestion_summary,
            hard_filters=hard_filters_summary,
            matching=matching_summary,
            daily_snapshots=daily_snapshots_summary,
            relevance_scoring=relevance_scoring_summary,
            relevance_selection=relevance_selection_summary,
            pipeline_audit=audit_summary,
        )
    except Exception as e:
        if run_id is not None:
            try:
                update_pipeline_run(conn, run_id=str(run_id), status="failed", finished_at="now", error=str(e))
            except Exception:
                pass
        raise
    finally:
        conn.close()
