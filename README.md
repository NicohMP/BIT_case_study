# Polymarket Signal Scanner (case study skeleton)

This repo keeps **structure only** (no implementation yet) so we don’t lock in framework/provider
choices prematurely.

## Requirements (from the consignes)
- Scheduled ingestion of active Polymarket markets
- Postgres database (Supabase allowed) with queryable schema
- Intelligent filtering to identify equity-relevant markets (most important)
- LLM-powered signal extraction mapped to selected stocks/sectors
- Automated, insight-focused reports stored in DB
- Small web interface:
  - configure sectors/stocks
  - browse signals and relevance labeling
  - view past reports

## Repository layout
- `polyscanner/`: core package placeholders
- `scripts/`: runnable entrypoints placeholders
- `db/`: DB layer placeholder

## Recommended build order
1) DB schema + migrations
2) Ingestion (idempotent upserts + time-series snapshots)
3) Filtering + LLM classification + ticker mapping
4) Report generation prompts + storage
5) Minimal web UI

