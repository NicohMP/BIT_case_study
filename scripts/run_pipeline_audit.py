#!/usr/bin/env python3
"""Audit the end-to-end pipeline and write a single markdown report.

Canonical implementation lives in `polyscanner.pipeline.audit`.

Usage:
  ./venv/bin/python scripts/run_pipeline_audit.py \
    --filter-version hard_filters_v8 \
    --matcher-version matcher_v10 \
    --scoring-version relevance_v5 \
    --selection-version selected_v1
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
from polyscanner.pipeline.audit import run_pipeline_audit  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Audit the end-to-end pipeline and write a markdown report.")
    p.add_argument("--filter-version", type=str, default=None, help="Hard filter version (defaults to YAML version).")
    p.add_argument("--matcher-version", type=str, required=True, help="matcher_version to audit (Step 3).")
    p.add_argument("--scoring-version", type=str, default=None, help="scoring_version to audit (Step 4).")
    p.add_argument("--selection-version", type=str, default=None, help="selection_version to audit (Step 4b).")
    p.add_argument("--top-n", type=int, default=20, help="Top-N rows to display per security.")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    out = run_pipeline_audit(
        db_url=db_url,
        filter_version=args.filter_version,
        matcher_version=str(args.matcher_version),
        scoring_version=args.scoring_version,
        selection_version=args.selection_version,
        out_dir="reports",
        top_n=int(args.top_n),
    )
    print("pipeline_audit:", {"markdown_path": out.markdown_path})


if __name__ == "__main__":
    main()

