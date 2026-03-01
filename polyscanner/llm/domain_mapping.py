"""LLM prompt: assign each Polymarket market to a BIT domain (MVP)."""

from __future__ import annotations

import json
from typing import Any

from polyscanner.llm.gemini import generate_json
from polyscanner.models import Domain, DomainDefinition, RankedMarket


_SYSTEM = (
    "You are an investment analyst. Your task is to map each prediction market to the most relevant "
    "BIT domain from the provided list. If none fit, use 'Unknown'. Return only JSON."
)


def assign_domains_with_gemini(
    ranked_markets: list[RankedMarket],
    domains: list[Domain],
) -> dict[str, Any]:
    domain_names = [d.name for d in domains]

    markets_payload = [
        {
            "pm_market_id": rm.market.pm_market_id,
            "question": rm.market.question,
            "category": rm.market.category,
            "probability": rm.market.probability,
            "volume": rm.market.volume,
            "heuristic_domain": rm.heuristic_domain,
        }
        for rm in ranked_markets
    ]

    prompt_obj = {
        "domains": domain_names,
        "markets": markets_payload,
        "output_schema": {
            "title": "string",
            "items": [
                {
                    "pm_market_id": "int",
                    "domain": "string (must be in domains or 'Unknown')",
                    "confidence": "number 0..1",
                    "rationale": "string (1-3 sentences)",
                }
            ],
        },
        "instructions": [
            "Return ONLY one JSON object.",
            "domain must exactly match one of the domains provided, or 'Unknown'.",
            "Use heuristic_domain only as a hint; override if wrong.",
        ],
    }

    return generate_json(
        prompt=json.dumps(prompt_obj, ensure_ascii=False),
        system=_SYSTEM,
        temperature=0.2,
    )


def assign_domains_with_gemini_from_scored(
    scored_items: list[dict[str, Any]],
    domains: list[DomainDefinition],
) -> dict[str, Any]:
    """Same mapping prompt, but driven by scored pipeline output."""
    domain_names = [d.name for d in domains]

    markets_payload = [
        {
            "pm_market_id": it.get("pm_market_id"),
            "question": it.get("question"),
            "category": it.get("category"),
            "probability": it.get("probability"),
            "volume": it.get("volume"),
            "heuristic_domain": it.get("best_domain"),
            "final_score": it.get("final_score"),
        }
        for it in scored_items
    ]

    prompt_obj = {
        "domains": domain_names,
        "markets": markets_payload,
        "output_schema": {
            "title": "string",
            "items": [
                {
                    "pm_market_id": "int",
                    "domain": "string (must be in domains or 'Unknown')",
                    "confidence": "number 0..1",
                    "rationale": "string (1-3 sentences)",
                }
            ],
        },
        "instructions": [
            "Return ONLY one JSON object.",
            "domain must exactly match one of the domains provided, or 'Unknown'.",
            "Use heuristic_domain only as a hint; override if wrong.",
        ],
    }

    return generate_json(
        prompt=json.dumps(prompt_obj, ensure_ascii=False),
        system=_SYSTEM,
        temperature=0.2,
    )
