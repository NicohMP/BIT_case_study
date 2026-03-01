#!/usr/bin/env python3
"""Run a default end-to-end refresh (Steps 1→4b) with embeddings enabled.

This is intended as the "best discovery coverage" command:
  ./venv/bin/python scripts/refresh_embeddings.py

Embeddings use sentence-transformers locally. Set `EMBEDDING_DEVICE` in `.env`:
- macOS: `mps`
- Linux/NVIDIA: `cuda` (requires CUDA-enabled PyTorch)
- otherwise: `cpu`
"""

from __future__ import annotations

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
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = (get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    base_url = (get_env("POLYMARKET_API_BASE_URL") or GAMMA_BASE_URL_DEFAULT).strip()

    emb_model = (get_env("EMBEDDING_MODEL") or "sentence-transformers/all-MiniLM-L6-v2").strip()
    emb_device = (get_env("EMBEDDING_DEVICE") or "").strip() or None

    out = run_polymarket_refresh(
        db_url=db_url,
        base_url=base_url,
        ingest_max_pages=200,
        matcher_version="matcher_v10",
        scoring_version="relevance_v5",
        trusted_only=True,
        persist_selection=True,
        selection_version="selected_v1",
        use_embeddings=True,
        embedding_model=emb_model,
        embedding_device=emb_device,
        run_audit=True,
    )

    print(
        "refresh_embeddings:",
        {
            "run_id": out.run_id,
            "embedding_model": emb_model,
            "embedding_device": emb_device,
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
