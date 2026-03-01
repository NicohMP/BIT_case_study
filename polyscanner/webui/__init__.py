"""Minimal FastAPI Web UI for the Polymarket Signal Scanner.

This UI is intentionally thin:
- Reads from the Postgres tables/views produced by Steps 1–4b.
- Displays persisted Step-5 reports (JSON rendered to Markdown deterministically).
- LLM calls remain on-demand (not scheduled) and may be unavailable depending on API quotas.
"""

