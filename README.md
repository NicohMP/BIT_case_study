# Polymarket Signal Scanner

This repo implements a versioned, auditable data pipeline for scanning Polymarket:

- **Step 1 (Ingestion)**: ingest *all* active events + markets from the Gamma `/events` endpoint (pagination) into Postgres.
- **Step 2 (Hard filters)**: deterministically reject template/junk markets and store explainable filter decisions.
- **Step 3 (Signal-family matching)**: high-recall discovery (lexical + local embeddings) + high-precision deterministic rules, persisted with evidence for auditability.
- **Step 4 (Relevance scoring)**: deterministic market relevance per BIT security via the authority matrices.
- **Step 4b (Selection)**: persisted diversified top-K per security (the primary downstream feed).
- **Step 5 (LLM report, report-time only)**: build a deterministic context pack from Step 4b outputs, then use an LLM to write an analyst-ready report grounded in that pack.

Downstream components (LLM enrichment and/or a web UI) should query the Postgres tables/views produced by this pipeline rather than calling the Gamma API directly.

## Supabase (local)

Start Supabase and apply migrations + seed:
`supabase start`
`supabase db reset`

Apply a single new migration without a reset (local):
`psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f supabase/migrations/<migration>.sql`

## Environment

Create `.env` with at least:
- `DATABASE_URL` pointing to Supabase Postgres (local typically uses `127.0.0.1:54322`).

Important: `.env` must use `KEY=value` lines (so `python-dotenv` can load it), e.g.:
`DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres`

Optional:
- `POLYMARKET_API_BASE_URL` (default: `https://gamma-api.polymarket.com`)
- `EMBEDDING_MODEL` (default: `sentence-transformers/all-MiniLM-L6-v2`)
- `EMBEDDING_DEVICE` (e.g. `mps` or `cpu`)

## Seed security→domain exposures (authority)

Step 4 requires `bit_security_macro_domain_exposure` weights (must sum to 1.0 per security).

This repo keeps the authority weights in `security_domain_exposure_scores.md` and provides a
seed script that normalizes the 0–3 scores into weights and upserts them into Postgres:

`./venv/bin/python scripts/seed_security_domain_exposure.py`

## Seed family→domain influence rationales (authority)

Step 5 report quality depends on `signal_family_domain_influence.rationale_md` (the “why” for each edge).
The repo keeps the source-of-truth rationale matrix in `event_domain_rationale.md`.

Seed/upsert into Postgres:
`./venv/bin/python scripts/seed_signal_family_domain_influence_rationales.py`

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

Tip: matching coverage scales with `--limit`. If you want Step 4 rankings to diversify beyond
rate/FOMC markets, run Step 3 over *all* kept markets (10k+), not just the top 5k by volume.

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

## Step 4: Relevance scoring (markets → families → domains → securities)

Compute a deterministic relevance score for each (security, market) pair:
- market→family `match_strength` (Step 3)
- family→domain influence matrix (authority)
- security→domain exposure weights (authority)
- optional market quality multiplier (`pm_market_filter_decision.quality_score`)

Run:
`./venv/bin/python scripts/run_relevance_scoring.py --filter-version hard_filters_v8 --matcher-version matcher_v1 --scoring-version relevance_v1`

Optional (display-only): de-duplicate by event_id and cap rate/FOMC-like markets in printed top lists:

`./venv/bin/python scripts/run_relevance_scoring.py --filter-version hard_filters_v8 --matcher-version matcher_v1 --scoring-version relevance_v1 --diversify true`

Outputs:
- DB upserts into `pm_market_security_relevance` (keyed by `(security_id, market_id, scoring_version)`)

## Step 4b: Persisted diversified selection (downstream feed)

Step 4b stores a diversified top-K per security to avoid:
- the same `event_id` flooding the list
- rate/FOMC-like markets dominating every security

Run (also enabled by default in `scripts/run_relevance_scoring.py`):
`./venv/bin/python scripts/run_relevance_scoring.py --filter-version hard_filters_v8 --matcher-version matcher_v10 --scoring-version relevance_v5 --persist-selection true --selection-version selected_v1`

Outputs:
- DB upserts into `pm_market_security_relevance_selection` (keyed by `(security_id, market_id, scoring_version, selection_version)`)

## Step 5: LLM security report (report-time only)

The LLM is **not** used in ingestion/filtering/matching/scoring. It is only called at report time and only sees a
structured, deterministic context pack built from the DB.

Migration (table to persist reports):
`psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f supabase/migrations/20260225210000_add_pm_security_signal_report.sql`

Build + validate a context pack for one security:
`./venv/bin/python scripts/build_security_report_pack.py --ticker NVDA`
`./venv/bin/python scripts/validate_security_report_pack.py --pack reports/context_pack_NVDA_<ts>.json`

If validation fails with “missing market_card/buckets”, rebuild the pack (older packs are not forward-compatible).

Generate report JSON via Gemini (requires `GOOGLE_API_KEY` in `.env`):
`./venv/bin/python scripts/generate_security_signal_report.py --pack reports/context_pack_NVDA_<ts>.json`

Render markdown + audit grounding:
`./venv/bin/python scripts/render_security_signal_report_md.py --report-json reports/security_signal_report_NVDA_<ts>.json`
`./venv/bin/python scripts/audit_security_signal_report.py --pack reports/context_pack_NVDA_<ts>.json --report-json reports/security_signal_report_NVDA_<ts>.json`

## Pipeline audit (debug bottlenecks)

To debug why rate/FOMC markets dominate and whether the bottleneck is filters, matching thresholds,
or relevance concentration, generate a single markdown report:

`./venv/bin/python scripts/run_pipeline_audit.py --filter-version hard_filters_v8 --matcher-version matcher_v1 --scoring-version relevance_v1`

This writes `reports/pipeline_audit_*.md`.

## One-command refresh (Steps 1→4b)

For scheduled runs (cron/job runner) and downstream consumers, run Steps 1–4b in a single command:

`./venv/bin/python scripts/run_polymarket_refresh.py --ingest-max-pages 200 --matcher-version matcher_v1`

This:
- ingests Gamma `/events` into `pm_event` + `pm_market`
- writes filter decisions into `pm_market_filter_decision`
- writes matches into `pm_market_signal_family_match`
- writes relevance rows into `pm_market_security_relevance`
- writes diversified selections into `pm_market_security_relevance_selection`
- optionally writes a `reports/pipeline_audit_*.md`

## Data contract (downstream LLM / web UI)

Primary tables produced by this pipeline:
- `pm_event` / `pm_market`: raw + normalized Polymarket universe (active events + markets).
- `pm_market_filter_decision`: per-market keep/reject decision, keyed by `filter_version`.
- `pm_market_signal_family_match`: per-market family matches (methods + evidence), keyed by `matcher_version`.
- `pm_text_embedding_cache`: cached sentence-transformer embeddings (jsonb list of floats).
- `pm_market_security_relevance`: per-(security, market) relevance scores, keyed by `scoring_version`.
- `pm_market_security_relevance_selection`: diversified per-security top-K (recommended downstream feed).
- `pm_pipeline_run`: run metadata (latest versions, artifacts, errors).

Recommended downstream query surfaces (views):
- `v_pm_security_market_relevance_selected_latest_enriched`: **one-stop** for WebUI/LLM (latest run only).
- `v_pm_market_kept_latest`: kept markets for the latest run (post Step 2).
- `v_pm_market_signal_family_match_latest_trusted`: strict market→family matches for the latest run (post Step 3).

## Code layout

- `scripts/ingest_active_events.py`: Step 1 CLI runner
- `scripts/run_hard_filters.py`: Step 2 CLI runner
- `scripts/run_family_matching.py`: Step 3 CLI runner
- `scripts/run_relevance_scoring.py`: Step 4 + Step 4b CLI runner
- `scripts/run_pipeline_audit.py`: end-to-end audit markdown
- `scripts/run_polymarket_refresh.py`: Steps 1→4b orchestration (scheduled job entry point)
- `polyscanner/ingestion/gamma_events_ingest.py`: Step 1 implementation
- `polyscanner/filtering/hard_filters.py`: Step 2 filter logic + config loader
- `polyscanner/filtering/runner.py`: Step 2 runner (DB streaming + persistence + audits)
- `polyscanner/matching/matcher.py`: Step 3 runner (discovery + classification + persistence + audits)
- `polyscanner/relevance/security_market_relevance.py`: Step 4 + Step 4b implementation
- `polyscanner/pipeline/polymarket_refresh.py`: end-to-end orchestrator (Steps 1→4b)
- `polyscanner/pipeline/audit.py`: end-to-end audit renderer (DB → markdown)
