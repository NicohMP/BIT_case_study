#!/usr/bin/env python3
"""Step 3: run 2-stage signal-family matching over kept markets.

Usage:
  ./venv/bin/python scripts/run_family_matching.py \
    --filter-version hard_filters_v8 \
    --matcher-version matcher_v1 \
    --limit 5000 \
    --use-embeddings true
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.matching.matcher import run_family_matching  # noqa: E402


def _parse_bool(x: str) -> bool:
    v = (x or "").strip().lower()
    return v in {"1", "true", "t", "yes", "y", "on"}


def main() -> None:
    p = argparse.ArgumentParser(description="Run Step-3 signal-family matching (discovery + rule classification).")
    p.add_argument("--filter-version", type=str, default=None, help="Hard filter version (defaults to config version).")
    p.add_argument("--matcher-version", type=str, default="matcher_v1", help="Matcher version label (required for audits).")
    p.add_argument("--limit", type=int, default=5000, help="Max kept markets to evaluate.")
    p.add_argument("--use-embeddings", type=str, default="true", help="true/false to enable embedding discovery.")
    p.add_argument(
        "--embedding-model",
        type=str,
        default=None,
        help="Sentence-transformers model (default EMBEDDING_MODEL or sentence-transformers/all-MiniLM-L6-v2).",
    )
    p.add_argument("--embedding-device", type=str, default=None, help="Device for sentence-transformers (e.g. cpu, mps).")
    # Preferred flags
    p.add_argument("--top-k", type=int, default=None, help="Top-K families per market from embeddings (alias of --embedding-top-k).")
    p.add_argument(
        "--similarity-threshold",
        type=float,
        default=None,
        help="Min cosine similarity for embedding candidates (alias of --embedding-min-sim).",
    )
    p.add_argument(
        "--rule-threshold",
        type=float,
        default=None,
        help="Min rule score for strict match (alias of --classification-min-score).",
    )
    # Back-compat flags
    p.add_argument("--embedding-top-k", type=int, default=5, help=argparse.SUPPRESS)
    p.add_argument("--embedding-min-sim", type=float, default=0.40, help=argparse.SUPPRESS)
    p.add_argument("--lexical-min-score", type=float, default=0.30, help="Min lexical discovery score.")
    p.add_argument("--classification-min-score", type=float, default=0.70, help=argparse.SUPPRESS)
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    emb_model = args.embedding_model or get_env("EMBEDDING_MODEL") or "sentence-transformers/all-MiniLM-L6-v2"
    emb_device = args.embedding_device or get_env("EMBEDDING_DEVICE")

    embedding_top_k = int(args.top_k) if args.top_k is not None else int(args.embedding_top_k)
    embedding_min_sim = float(args.similarity_threshold) if args.similarity_threshold is not None else float(args.embedding_min_sim)
    rule_threshold = float(args.rule_threshold) if args.rule_threshold is not None else float(args.classification_min_score)

    out = run_family_matching(
        db_url=db_url,
        filter_version=args.filter_version,
        matcher_version=str(args.matcher_version),
        limit=int(args.limit),
        use_embeddings=_parse_bool(args.use_embeddings),
        embedding_model=str(emb_model),
        embedding_device=emb_device,
        embedding_top_k=int(embedding_top_k),
        embedding_min_similarity=float(embedding_min_sim),
        lexical_min_score=float(args.lexical_min_score),
        classification_min_score=float(rule_threshold),
        out_dir="reports",
    )
    print("family_matching:", out)


if __name__ == "__main__":
    main()
