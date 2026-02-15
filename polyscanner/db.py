"""Database schema + access layer (skeleton).

This module will eventually define the Postgres schema for:
- `markets`: stable market metadata
- `market_snapshots`: time-series probability/price + volume
- `stocks`: tracked universe configured by analysts
- `signals`: relevance classification + rationale
- `signal_impacts`: mapping from signal -> ticker impacts
- `reports` / `report_items`: generated analyst reports and their supporting signals

Design goal: normalized, queryable, auditable (store raw API/LLM payloads).
"""

