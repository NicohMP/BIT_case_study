"""LLM step for the minimal end-to-end pipeline.

For the MVP, the LLM only needs to do one thing:
- assign each candidate Polymarket market to one of the BIT domains

Output is structured JSON so it can be:
- rendered into a markdown report
- stored in Postgres later if desired
"""

from __future__ import annotations

import json
from typing import Any

from polyscanner.filtering import Domain, RankedMarket
from polyscanner.llm_gemini import generate_json


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

