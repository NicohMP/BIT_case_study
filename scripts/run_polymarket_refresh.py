#!/usr/bin/env python3
"""Run the end-to-end Polymarket refresh pipeline (Steps 1→4b).

Usage:
  ./venv/bin/python scripts/run_polymarket_refresh.py --ingest-max-pages 200 --matcher-version matcher_v10
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
from polyscanner.db.pg import connect  # noqa: E402
from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.pipeline.polymarket_refresh import run_polymarket_refresh  # noqa: E402


def _parse_bool(x: str) -> bool:
    v = (x or "").strip().lower()
    return v in {"1", "true", "t", "yes", "y", "on"}


def main() -> None:
    p = argparse.ArgumentParser(description="Run Steps 1→4b: ingest → hard filters → family matching → relevance → selection.")
    # Step 1
    p.add_argument("--ingest-limit", type=int, default=100, help="Gamma /events page size (limit).")
    p.add_argument("--ingest-max-pages", type=int, default=None, help="Optional cap on number of /events pages.")
    p.add_argument("--ingest-sleep-s", type=float, default=0.2, help="Sleep seconds between /events pages.")
    p.add_argument("--since-ts", type=str, default=None, help="Optional ISO8601 timestamp for incremental ingest.")
    p.add_argument("--timeout-s", type=float, default=30.0, help="HTTP timeout per request.")
    # Step 2
    p.add_argument("--hard-filters-limit", type=int, default=None, help="Optional cap on markets evaluated in Step 2.")
    p.add_argument("--hard-filters-batch-size", type=int, default=1000, help="DB upsert batch size for Step 2.")
    # Step 3
    p.add_argument("--matcher-version", type=str, default="matcher_v1", help="Version label for Step 3 outputs.")
    p.add_argument("--match-limit", type=int, default=12000, help="Max kept markets to evaluate in Step 3.")
    p.add_argument("--use-embeddings", type=str, default="true", help="true/false to enable embedding discovery.")
    p.add_argument(
        "--embedding-model",
        type=str,
        default=None,
        help="Sentence-transformers model (default EMBEDDING_MODEL or sentence-transformers/all-MiniLM-L6-v2).",
    )
    p.add_argument("--embedding-device", type=str, default=None, help="Device for sentence-transformers (cpu, mps).")
    p.add_argument("--top-k", type=int, default=5, help="Top-K families per market from embeddings.")
    p.add_argument("--similarity-threshold", type=float, default=0.40, help="Min cosine similarity for embedding candidates.")
    p.add_argument("--lexical-min-score", type=float, default=0.30, help="Min lexical discovery score.")
    p.add_argument("--rule-threshold", type=float, default=0.70, help="Min strict rule score for match persistence.")
    # Step 4
    p.add_argument("--scoring-version", type=str, default="relevance_v1", help="Version label for Step 4 outputs.")
    p.add_argument("--trusted-only", type=str, default="true", help="true/false: score using only rule_classification matches.")
    p.add_argument("--min-base-score", type=float, default=0.0, help="Skip relevance rows with base_score <= this value.")
    # Step 4b
    p.add_argument("--persist-selection", type=str, default="true", help="true/false to store diversified top-K selections in DB.")
    p.add_argument("--selection-version", type=str, default="selected_v1", help="Version label for Step 4b outputs.")
    p.add_argument("--selection-k", type=int, default=20, help="K for stored diversified selection per security.")
    p.add_argument("--selection-max-per-event", type=int, default=1, help="Max markets per event_id in stored selection.")
    p.add_argument("--selection-max-rate-like", type=int, default=3, help="Max rate-like markets in stored selection.")
    # Daily snapshots
    p.add_argument("--record-daily-snapshots", type=str, default="false", help="true/false to snapshot current pricing once per UTC day.")
    p.add_argument("--snapshot-scope", type=str, default="kept", choices=["kept", "all"], help="Snapshot universe: kept (post Step 2) or all active.")
    p.add_argument("--snapshot-limit", type=int, default=None, help="Optional cap on markets snapshotted.")
    # Audit
    p.add_argument("--run-audit", type=str, default="true", help="true/false to write a pipeline audit markdown.")
    p.add_argument("--audit-top-n", type=int, default=20, help="Top-N to display per security in audit.")
    # Reliability: optional DB lock to prevent overlapping runs.
    p.add_argument(
        "--db-lock",
        type=str,
        default="none",
        choices=["none", "try", "wait"],
        help="Acquire a Postgres advisory lock before running (none|try|wait).",
    )
    p.add_argument("--db-lock-key", type=int, default=913274001, help="Advisory lock key (bigint).")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    base_url = get_env("POLYMARKET_API_BASE_URL") or GAMMA_BASE_URL_DEFAULT
    emb_model = args.embedding_model or get_env("EMBEDDING_MODEL") or "sentence-transformers/all-MiniLM-L6-v2"
    emb_device = args.embedding_device or get_env("EMBEDDING_DEVICE")

    lock_mode = str(args.db_lock or "none").strip().lower()
    lock_key = int(args.db_lock_key)
    lock_conn = None
    if lock_mode != "none":
        lock_conn = connect(db_url)
        try:
            with lock_conn.cursor() as cur:
                if lock_mode == "try":
                    cur.execute("select pg_try_advisory_lock(%s);", (lock_key,))
                    ok = bool(cur.fetchone()[0])
                    if not ok:
                        logging.warning("DB lock busy (another refresh is running); skipping this run.")
                        return
                else:
                    cur.execute("select pg_advisory_lock(%s);", (lock_key,))
            out = run_polymarket_refresh(
                db_url=db_url,
                base_url=base_url,
                ingest_limit=int(args.ingest_limit),
                ingest_max_pages=args.ingest_max_pages,
                ingest_sleep_s=float(args.ingest_sleep_s),
                ingest_since_ts=args.since_ts,
                ingest_timeout_s=float(args.timeout_s),
                hard_filters_limit=args.hard_filters_limit,
                hard_filters_batch_size=int(args.hard_filters_batch_size),
                matcher_version=str(args.matcher_version),
                match_limit=int(args.match_limit),
                use_embeddings=_parse_bool(args.use_embeddings),
                embedding_model=str(emb_model),
                embedding_device=emb_device,
                embedding_top_k=int(args.top_k),
                embedding_min_similarity=float(args.similarity_threshold),
                lexical_min_score=float(args.lexical_min_score),
                classification_min_score=float(args.rule_threshold),
                scoring_version=str(args.scoring_version),
                trusted_only=_parse_bool(args.trusted_only),
                min_base_score=float(args.min_base_score),
                persist_selection=_parse_bool(args.persist_selection),
                selection_version=str(args.selection_version),
                selection_k=int(args.selection_k),
                selection_max_per_event=int(args.selection_max_per_event),
                selection_max_rate_like=int(args.selection_max_rate_like),
                record_daily_snapshots=_parse_bool(args.record_daily_snapshots),
                snapshot_scope=str(args.snapshot_scope),
                snapshot_limit=args.snapshot_limit,
                run_audit=_parse_bool(args.run_audit),
                audit_top_n=int(args.audit_top_n),
                out_dir="reports",
            )
        finally:
            try:
                with lock_conn.cursor() as cur:
                    cur.execute("select pg_advisory_unlock(%s);", (lock_key,))
                lock_conn.commit()
            finally:
                lock_conn.close()
    else:
        out = run_polymarket_refresh(
            db_url=db_url,
            base_url=base_url,
            ingest_limit=int(args.ingest_limit),
            ingest_max_pages=args.ingest_max_pages,
            ingest_sleep_s=float(args.ingest_sleep_s),
            ingest_since_ts=args.since_ts,
            ingest_timeout_s=float(args.timeout_s),
            hard_filters_limit=args.hard_filters_limit,
            hard_filters_batch_size=int(args.hard_filters_batch_size),
            matcher_version=str(args.matcher_version),
            match_limit=int(args.match_limit),
            use_embeddings=_parse_bool(args.use_embeddings),
            embedding_model=str(emb_model),
            embedding_device=emb_device,
            embedding_top_k=int(args.top_k),
            embedding_min_similarity=float(args.similarity_threshold),
            lexical_min_score=float(args.lexical_min_score),
            classification_min_score=float(args.rule_threshold),
            scoring_version=str(args.scoring_version),
            trusted_only=_parse_bool(args.trusted_only),
            min_base_score=float(args.min_base_score),
            persist_selection=_parse_bool(args.persist_selection),
            selection_version=str(args.selection_version),
            selection_k=int(args.selection_k),
            selection_max_per_event=int(args.selection_max_per_event),
            selection_max_rate_like=int(args.selection_max_rate_like),
            record_daily_snapshots=_parse_bool(args.record_daily_snapshots),
            snapshot_scope=str(args.snapshot_scope),
            snapshot_limit=args.snapshot_limit,
            run_audit=_parse_bool(args.run_audit),
            audit_top_n=int(args.audit_top_n),
            out_dir="reports",
        )
    print(
        "polymarket_refresh:",
        {
            "run_id": out.run_id,
            "ingestion": out.ingestion,
            "hard_filters": out.hard_filters,
            "matching": out.matching,
            "daily_snapshots": out.daily_snapshots,
            "relevance_scoring": out.relevance_scoring,
            "relevance_selection": out.relevance_selection,
            "pipeline_audit": out.pipeline_audit,
        },
    )


if __name__ == "__main__":
    main()
