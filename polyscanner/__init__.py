"""Polymarket Signal Scanner.

Core pipeline:
- Step 1: ingest all active events + markets from Polymarket Gamma `/events`
- Step 2: apply deterministic hard filters and persist auditable decisions
- Step 3: match kept markets to signal families (discovery + strict rules)
"""
