# Polymarket Signal Scanner (MVP wiring)

This repo contains a **minimal end-to-end skeleton**:
- Read BIT domains from Postgres (Supabase local)
- Fetch active markets from Polymarket (Gamma API)
- Pick top-N relevant markets via simple heuristics
- Ask Gemini to map each market to a BIT domain (structured JSON)
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

## Run from a notebook

```python
from polyscanner.pipeline.minimal import run_minimal_pipeline

result = run_minimal_pipeline(top_n=10, use_llm=True)
result["report_path"]
```
