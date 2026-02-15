"""Ingestion tasks (skeleton).

This module will eventually implement an idempotent scheduled pipeline:
- Fetch active markets from Polymarket on an interval
- Upsert `markets`
- Append `market_snapshots` for probability/volume
"""

