# Polymarket Signal Scanner (MVP wiring)

This repo contains a **minimal end-to-end skeleton**:
- Read BIT domains from Postgres (Supabase local)
- Fetch active markets from Polymarket (Gamma API)
- Score markets vs BIT domains (embeddings, with keyword fallback)
- Rank markets by domain relevance (channels are optional/disabled for now)
- (Optional) Ask Gemini to map each market to a BIT domain (structured JSON)
- Write a markdown report to `reports/`

## Supabase (local)

Start Supabase and apply migrations + seed:
`supabase start`
`supabase db reset`

## Environment

Create `.env` with at least:
- `DATABASE_URL` pointing to local Supabase Postgres (typically `127.0.0.1:54322`)
- `GOOGLE_API_KEY` (Gemini API key)

Optional:
- `GEMINI_MODEL` (default: `gemini-2.0-flash`)
- `EMBEDDING_MODEL` (default: `all-MiniLM-L6-v2`)
- `EMBEDDING_DEVICE` (e.g. `mps` or `cpu`)

## Run from a notebook

```python
from polyscanner.pipeline.minimal import run_minimal_pipeline

result = run_minimal_pipeline(top_n=10, use_llm=True)
result["report_path"]
```

## Ingest Polymarket markets into Postgres

After applying migrations (e.g. `supabase db reset`), you can ingest the latest active markets into `pm_market`:

`./venv/bin/python scripts/ingest_pm_markets.py`

## Code layout (MVP)

- `polyscanner/pipeline/minimal.py`: orchestrates the end-to-end run
- `polyscanner/db/pg.py`: Postgres read helpers (`bit_domain`, signal families, etc.)
- `polyscanner/clients/polymarket_gamma.py`: Polymarket market ingestion
- `polyscanner/relevance/domain_relevance.py`: domain relevance (embeddings with fallback)
- `polyscanner/relevance/channels.py`: (optional) channel relevance heuristics
- `polyscanner/relevance/final_score.py`: combines components (falls back to domain-only when exposures are absent)
- `polyscanner/llm/gemini.py`: Gemini HTTP client
- `polyscanner/llm/domain_mapping.py`: prompt that maps markets → domains
- `polyscanner/reporting/markdown.py`: render + write the markdown report
