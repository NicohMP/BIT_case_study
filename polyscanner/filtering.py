"""Relevance filtering (skeleton).

This is the highest-priority part of the case study.

Planned approach (multi-stage):
1) Cheap heuristics to down-select markets (keywords, entities, categories)
2) LLM classification to decide equity relevance and event type
3) Mapping to impacted tickers (direction/confidence/thesis) for tracked stocks

Every decision should be explainable to analysts (store rationale + provenance).
"""

