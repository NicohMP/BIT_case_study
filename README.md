# Polymarket Signal Scanner

This repo implements a versioned, auditable data pipeline for scanning Polymarket:

- **Step 1 (Ingestion)**: ingest *all* active events + markets from the Gamma `/events` endpoint (pagination) into Postgres.
- **Step 2 (Hard filters)**: deterministically reject template/junk markets and store explainable filter decisions.
- **Step 3 (Signal-family matching)**: high-recall discovery (lexical + local embeddings) + high-precision deterministic rules, persisted with evidence for auditability.

Downstream components (LLM enrichment and/or a web UI) should query the Postgres tables produced by Steps 1–3 rather than calling the Gamma API directly.

## Supabase (local)

Start Supabase and apply migrations + seed:
`supabase start`
`supabase db reset`

## Environment

Create `.env` with at least:
- `DATABASE_URL` pointing to Supabase Postgres (local typically uses `127.0.0.1:54322`).

Optional:
- `POLYMARKET_API_BASE_URL` (default: `https://gamma-api.polymarket.com`)
- `EMBEDDING_MODEL` (default: `sentence-transformers/all-MiniLM-L6-v2`)
- `EMBEDDING_DEVICE` (e.g. `mps` or `cpu`)

## Ingest Polymarket events + markets into Postgres (coverage-first)

After applying migrations (e.g. `supabase db reset`), ingest all **active, non-closed** events (and their embedded markets)
via the Gamma `/events` endpoint pagination. This upserts into `pm_event` and `pm_market`:

`./venv/bin/python scripts/ingest_active_events.py --limit 100 --max-pages 200`

## Step 2: Hard filters (cheap precision)

Run deterministic hard filters to reject template/junk markets and store auditable decisions:

- Config (edit patterns + bump version when you change rules): `polyscanner/filtering/hard_filter_rules.yaml`
- Run: `./venv/bin/python scripts/run_hard_filters.py`
- Outputs:
  - DB upserts into `pm_market_filter_decision` (keyed by `(market_id, filter_version)`)
  - Markdown audit report in `reports/hard_filter_audit_*.md`

## Step 3: Signal-family matching (high recall → high precision)

Two-stage matcher:
1) **Discovery** (high recall): lexical keywords + optional embeddings
2) **Classification** (high precision): deterministic gated rules

Run:
`./venv/bin/python scripts/run_family_matching.py --filter-version hard_filters_v8 --matcher-version matcher_v1 --limit 5000 --use-embeddings true`

Config inputs:
- `polyscanner/matching/family_keywords.yaml` (discovery keywords/synonyms per family)
- `polyscanner/signal_family_rules.py` (strict deterministic family rules)

Outputs:
- DB upserts into `pm_market_signal_family_match` (versioned by `matcher_version` + `method`)
- Optional embedding cache in `pm_text_embedding_cache`
- Audit artifacts in `reports/`:
  - `family_coverage_*.csv`
  - `false_positive_audit_*.md`
  - `missing_family_diagnosis_*.md`

## One-command refresh (Steps 1→3)

For scheduled runs (cron/job runner) and downstream consumers, run Steps 1–3 in a single command:

`./venv/bin/python scripts/run_polymarket_refresh.py --ingest-max-pages 200 --matcher-version matcher_v1`

This:
- ingests Gamma `/events` into `pm_event` + `pm_market`
- writes filter decisions into `pm_market_filter_decision`
- writes matches into `pm_market_signal_family_match`
- writes audit artifacts into `reports/`

## Data contract (downstream LLM / web UI)

Primary tables produced by this pipeline:
- `pm_event` / `pm_market`: raw + normalized Polymarket universe (active events + markets).
- `pm_market_filter_decision`: per-market keep/reject decision, keyed by `filter_version`.
- `pm_market_signal_family_match`: per-market family matches (methods + evidence), keyed by `matcher_version`.
- `pm_text_embedding_cache`: cached sentence-transformer embeddings (jsonb list of floats).

Downstream services typically:
- join `pm_market` ↔ `pm_event` (context)
- join `pm_market_filter_decision` (choose a `filter_version`)
- join `pm_market_signal_family_match` (choose a `matcher_version`, prefer `method='rule_classification'`)

## Code layout

- `scripts/ingest_active_events.py`: Step 1 CLI runner
- `scripts/run_hard_filters.py`: Step 2 CLI runner
- `scripts/run_family_matching.py`: Step 3 CLI runner
- `scripts/run_polymarket_refresh.py`: Steps 1→3 orchestration
- `polyscanner/ingestion/gamma_events_ingest.py`: Step 1 implementation
- `polyscanner/filtering/hard_filters.py`: Step 2 filter logic + config loader
- `polyscanner/filtering/runner.py`: Step 2 runner (DB streaming + persistence + audits)
- `polyscanner/matching/matcher.py`: Step 3 runner (discovery + classification + persistence + audits)
