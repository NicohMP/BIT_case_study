# Polymarket Signal Scanner

Versioned pipeline that ingests Polymarket markets into Postgres, applies deterministic filtering, and serves an analyst Web UI.

## Pipeline steps (nomenclature)
- **Step 1 (Ingestion):** ingest all active events + markets from Gamma `/events` into Postgres (`pm_event`, `pm_market`).
- **Step 2 (Hard filters):** deterministically reject template/junk markets and store explainable decisions (`pm_market_filter_decision`).
- **Step 3 (Signal-family matching):** high-recall discovery (lexical + optional local embeddings) + strict rules, persisted with evidence (`pm_market_signal_family_match`).
- **Step 4 (Relevance scoring):** deterministic market relevance per BIT security using the authority matrices (`pm_market_security_relevance`).
- **Step 4b (Selection):** persisted diversified top‑K per security for downstream consumption (`pm_market_security_relevance_selection`).
- **Step 5 (LLM report, on-demand):** build a deterministic context pack from DB outputs, then generate a grounded report (does not run during refresh).

## Repo structure
- `polyscanner/`: core library (ingestion, filtering, matching/scoring, web UI)
- `scripts/`: runnable entrypoints (pipeline refresh, UI launcher)
- `supabase/`: local DB migrations + seeds
- `data/authorities/`: source-of-truth “authority” markdown inputs (priors)
- `docs/`: reviewer notes and deeper documentation

## Quickstart (minimal steps)

### 1) Python
`python3 -m venv venv`
`./venv/bin/pip install -r requirements.txt`

### 2) `.env`
`cp .env.example .env`

Required:
- `DATABASE_URL`

Optional (only if you enable embeddings):
- `EMBEDDING_DEVICE`: `cpu` (default), `mps` (macOS), `cuda`/`cuda:0` (Linux/NVIDIA)
- Linux/NVIDIA: install a CUDA-enabled PyTorch first, then `./venv/bin/pip install -r requirements-nontorch.txt`

### 3) Local DB (Supabase)
`supabase start`
`supabase db reset`

### 4) Ingest + filter (+ rest of pipeline)
Basic run (no embeddings):
`./venv/bin/python scripts/refresh_basic.py`

Run with embeddings:
`./venv/bin/python scripts/refresh_embeddings.py`

### 5) Launch the Web UI
`./venv/bin/python scripts/run_webui.py`

More (flags/versions, audits, report generation): `docs/reviewer/reproducibility.md`.
