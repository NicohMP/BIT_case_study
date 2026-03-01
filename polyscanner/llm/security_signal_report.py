"""LLM report for a single security using deterministic relevance scores (Gemini)."""

from __future__ import annotations

import json
from typing import Any

from polyscanner.llm.gemini import generate_json


_SYSTEM = (
    "You are a buy-side macro + tech equity research assistant. "
    "Return valid JSON only (no markdown). "
    "Do not invent markets, probabilities, volumes, ids, or scores; use only the provided input JSON. "
    "Do not include off-topic markets: if a market does not truly match the signal family, exclude it. "
    "Avoid redundancy: keep at most one representative market per cluster_id."
)


def _output_schema() -> dict[str, Any]:
    return {
        "title": "string",
        "as_of_utc": "string (ISO 8601)",
        "security": {
            "security_id": "int",
            "ticker": "string",
            "company_name": "string",
            "exchange_mic": "string",
        },
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
                        "final_score": "number",
                        "dedupe_group": "string",
                        "why_it_matters": "string (1-3 sentences, grounded in provided breakdown terms)",
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
                "excluded_as_redundant": [{"pm_market_id": "int", "reason": "string"}],
                "excluded_as_offtopic": [{"pm_market_id": "int", "reason": "string"}],
            }
        ],
        "notes": ["string"],
    }


def generate_security_signal_report_with_gemini(*, input_json: dict[str, Any]) -> dict[str, Any]:
    """Generate a security-focused report grouped by signal family."""
    prompt_obj = {
        "task": (
            "Given a single security, its macro-domain exposures, a set of matched Polymarket markets, and "
            "deterministic final_score values, produce a report grouped by signal family."
        ),
        "rules": [
            "Return ONLY one JSON object.",
            "Use final_score to choose markets (higher is better).",
            "Select up to TOP_K markets per family.",
            "You MUST select at most one market per cluster_id.",
            "Use redundant_market_ids to populate excluded_as_redundant when applicable.",
            "If a market is off-topic for the family, put it in excluded_as_offtopic with a short reason (do not include it in top_markets).",
            "In why_it_matters, reference at least one concrete phrase from the market question and one element from contributions_top.",
            "impacted_domains must reflect the family's influence scores (pick 2-3 highest).",
            "confidence should reflect match_score specificity and the clarity of the market question.",
        ],
        "output_schema": _output_schema(),
        "input": input_json,
    }
    return generate_json(prompt=json.dumps(prompt_obj, ensure_ascii=False), system=_SYSTEM, temperature=0.2)

