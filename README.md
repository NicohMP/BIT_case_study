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

### 0) Prereqs
- Python 3.11+ (recommended: 3.12/3.13; last tested with 3.14.3 on 2026-03-01)
- Supabase CLI installed (`supabase` in PATH)
- Postgres client optional (`psql`) for quick sanity checks
- Docker installed (only needed for the scheduled refresh)

### 1) Python (for one‑off runs + Web UI)
Fast path:
`bash scripts/bootstrap.sh`

Or manually:
`python3 -m venv venv`
`./venv/bin/pip install -r requirements.txt`

### 2) `.env`
If you ran `bash scripts/bootstrap.sh`, this is already created.

`cp .env.example .env`

Required:
- `DATABASE_URL`

If you use Supabase local, the default is:
- `DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres`

Optional (only if you enable embeddings):
- `EMBEDDING_DEVICE`: `cpu` (default), `mps` (macOS), `cuda`/`cuda:0` (Linux/NVIDIA)
- Linux/NVIDIA: install a CUDA-enabled PyTorch first, then `./venv/bin/pip install -r requirements-nontorch.txt`

### 3) Local DB (Supabase)
`supabase start`
`supabase db reset`

Sanity check (optional but recommended):
`./venv/bin/python scripts/doctor.py`

### 4) One‑off refresh (Steps 1→4b)
Basic run (no embeddings):
`./venv/bin/python scripts/refresh_basic.py`

Smoke test (fast, small ingest):
`./venv/bin/python scripts/refresh_basic.py --ingest-max-pages 2 --match-limit 500`

Run with embeddings:
`./venv/bin/python scripts/refresh_embeddings.py`

### 5) Scheduled refresh (cross‑OS via Docker)
Runs the refresh pipeline on an interval (default: every 2 hours) in a background Docker container.
This is intended as the “scheduled pipeline, not a one‑off script” mode from the case study instructions.

Prereq: make sure Supabase is running (`supabase start`) and your `.env` has a working `DATABASE_URL`.

Start:
`bash ops/docker/install.sh`

Defaults (without any extra config):
- embeddings enabled
- daily snapshots enabled (`pm_market_daily_snapshot`)
- pipeline audit disabled (to keep logs/artifacts small)

Configure (optional, in `.env`):
- `REFRESH_INTERVAL_SECONDS=7200`
- `REFRESH_USE_EMBEDDINGS=true` (default: `true`)
- `REFRESH_RECORD_DAILY_SNAPSHOTS=false` (disable daily snapshot upserts)
- `REFRESH_SNAPSHOT_SCOPE=kept` (or `all`)

Note: the scheduled Docker refresh forces `EMBEDDING_DEVICE=cpu` (Docker doesn’t support macOS `mps`).

Logs:
`cd ops/docker && docker compose logs -f refresh_scheduler`

Stop:
`bash ops/docker/uninstall.sh`

### 6) Launch the Web UI
`./venv/bin/python scripts/run_webui.py`

More (flags/versions, audits, report generation): `docs/reviewer/reproducibility.md`.
