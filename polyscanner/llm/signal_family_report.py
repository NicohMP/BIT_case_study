"""LLM report generation for signal families (Gemini).

This module defines:
- the exact JSON payload we send to Gemini
- the expected JSON response schema

Goal (MVP):
- Convert matched markets (market -> signal_family) into a non-redundant, readable
  analyst report.
- Keep the output structured so it can be rendered to markdown deterministically.
"""

from __future__ import annotations

import json
from typing import Any

from polyscanner.llm.gemini import generate_json


_SYSTEM = (
    "You are a buy-side macro + tech equity research assistant. "
    "Return valid JSON only (no markdown). "
    "Do not invent markets, probabilities, volumes, or ids; use only the provided input JSON. "
    "Avoid redundancy: group near-duplicate markets (same underlying event with different thresholds/dates) "
    "and keep only the single best representative per group. "
    "If a market does not truly match the signal family, exclude it rather than forcing a narrative. "
    "When unsure, set fields to null and explain briefly in notes."
)


def _output_schema() -> dict[str, Any]:
    # Kept explicit for prompt clarity (and for future validation if needed).
    return {
        "title": "string",
        "as_of_utc": "string (ISO 8601)",
        "families": [
            {
                "slug": "string",
                "title": "string",
                "what_to_watch": ["string"],
                "top_markets": [
                    {
                        "pm_market_id": "int",
                        "headline": "string",
                        "question": "string",
                        "probability": "number | null",
                        "volume_usd": "number | null",
                        "dedupe_group": "string",
                        "why_it_matters": "string (1-3 sentences)",
                        "impacted_domains": [
                            {
                                "macro_domain": "string",
                                "influence_score": "int 0..5",
                                "explanation": "string (1 sentence)",
                            }
                        ],
                        "confidence": "number 0..1",
                    }
                ],
                "excluded_as_redundant": [
                    {
                        "pm_market_id": "int",
                        "reason": "string",
                    }
                ],
                "excluded_as_offtopic": [
                    {
                        "pm_market_id": "int",
                        "reason": "string",
                    }
                ],
            }
        ],
        "notes": ["string"],
    }


def generate_signal_family_report_with_gemini(*, input_json: dict[str, Any]) -> dict[str, Any]:
    """Generate a structured signal-family report using Gemini.

    `input_json` is expected to contain:
    - as_of_utc
    - signal_families (with influence scores)
    - candidate_markets (matched to families + evidence + heuristic rank score)
    - clusters (optional, helps dedupe)
    - TOP_K (selection cap per family)
    """
    prompt_obj = {
        "task": (
            "Produce a structured report organized by signal family. "
            "For each family: dedupe near-duplicate markets, select up to TOP_K representative markets, "
            "and explain why they matter using the provided influence scores."
        ),
        "rules": [
            "Return ONLY a single JSON object.",
            "Never invent ids, probabilities, volumes, or questions.",
            "Use `heuristic_rank_score` to choose representatives within a dedupe group (higher is better).",
            "Prefer higher volume_usd, then higher match_score, when choosing representatives.",
            "You MUST select at most one market per cluster_id.",
            "Use redundant_market_ids to populate excluded_as_redundant when applicable.",
            "If a market is off-topic for the family, put it in excluded_as_offtopic with a short reason.",
            "Do NOT include off-topic markets in top_markets.",
            "In why_it_matters, reference at least one concrete phrase from the market question or matched_terms.",
            "Use impacted_domains from the highest influence_score domains for that family (2-3 domains).",
            "confidence must be in [0,1] and should reflect match specificity + match_score evidence.",
        ],
        "output_schema": _output_schema(),
        "input": input_json,
    }

    return generate_json(
        prompt=json.dumps(prompt_obj, ensure_ascii=False),
        system=_SYSTEM,
        temperature=0.2,
    )
