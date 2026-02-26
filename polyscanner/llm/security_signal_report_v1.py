"""Step 5 (report-time) LLM report for a single security (v1).

This module is intentionally report-time only:
- It consumes a deterministic context pack produced from Steps 1–4b.
- It calls an LLM only to turn that pack into an analyst-ready report.
- It does NOT fetch market data, run matching, or compute scores.
"""

from __future__ import annotations

import json
from typing import Any

from polyscanner.llm.gemini import generate_json

PROMPT_VERSION = "security_signal_report_v1"


_SYSTEM = (
    "You are a buy-side equity + macro research assistant writing for professional analysts. "
    "Return ONLY valid JSON (no markdown, no surrounding text). "
    "You MUST NOT use external knowledge or assumptions; use only the provided input JSON pack. "
    "Do not invent numbers, ids, market details, domains, signal families, rationales, or scores. "
    "If something is missing from the pack, say so explicitly in notes rather than guessing. "
    "Avoid near-duplicates: at most one market per event_id. "
    "Avoid over-concentration in rate-like/FOMC markets: respect max_rate_like."
)


def _output_schema_v1() -> dict[str, Any]:
    return {
        "title": "string",
        "as_of_utc": "string (ISO 8601)",
        "top_take": "string (2-4 sentences; no raw numeric scores; PM-readable)",
        "versions": {
            "run_id": "string | null",
            "filter_version": "string",
            "matcher_version": "string",
            "scoring_version": "string",
            "selection_version": "string",
            "prompt_version": "string",
            "model": "string",
        },
        "security": {
            "security_id": "int",
            "ticker": "string",
            "company_name": "string",
            "exchange_mic": "string",
        },
        "top_markets": [
            {
                "market_id": "int",
                "event_id": "int | null",
                "question": "string",
                "event_title": "string | null",
                "probability": "number | null",
                "pricing": {
                    "kind": "binary|multi_outcome|unknown",
                    "yes_probability": "number | null",
                    "top_outcomes": [{"outcome": "string", "probability": "number"}],
                    "note": "string | null",
                },
                "end_date": "string | null (ISO 8601)",
                "volume_usd": "number | null",
                "liquidity_usd": "number | null",
                "scores": {
                    "final_score": "number",
                    "base_score": "number",
                    "quality_multiplier": "number",
                    "market_strength": "number (0..1)",
                },
                "structural_relevance": "string (1-3 sentences; use pack.buckets + provided rationales; avoid raw score numbers)",
                "actionability": "string (1-3 sentences; use pack.market_card + pack.buckets; avoid raw score numbers)",
                "transmission_chain": [
                    {
                        "signal_family_id": "int",
                        "slug": "string",
                        "title": "string",
                        "method": "string",
                        "match_strength": "number (0..1)",
                        "domains": [
                            {
                                "macro_domain_id": "int",
                                "macro_domain_name": "string",
                                "family_influence_score": "int (0..5)",
                                "security_exposure_weight": "number (0..1)",
                                "edge_rationale": "string (must be copied/paraphrased from pack rationale_md; no inventions)",
                                "exposure_rationale": "string | null (from pack exposure_vector rationale)",
                            }
                        ],
                    }
                ],
                "magnitude_bucket": "low|medium|high",
                "timeline_bucket": "days|weeks|months|quarters|years",
                "what_to_watch": ["string"],
                "key_unknowns": ["string"],
                "evidence_refs": [
                    {
                        "kind": "market|family_match|influence_edge|security_exposure",
                        "market_id": "int (for market/family_match)",
                        "signal_family_id": "int (for family_match/influence_edge)",
                        "macro_domain_id": "int (for influence_edge/security_exposure)",
                    }
                ],
                "confidence": "number (0..1)",
            }
        ],
        "themes": [{"title": "string", "why": "string", "market_ids": ["int"]}],
        "monitor_next": ["string"],
        "exclusions": {
            "dropped_due_to_duplicate_event": [{"market_id": "int", "reason": "string"}],
            "dropped_due_to_rate_cap": [{"market_id": "int", "reason": "string"}],
            "dropped_due_to_low_actionability": [{"market_id": "int", "reason": "string"}],
        },
        "notes": ["string"],
    }


def build_prompt(
    *,
    pack: dict[str, Any],
    max_markets: int = 10,
    max_rate_like: int = 3,
) -> tuple[str, str]:
    """Return (system_instruction, prompt_text) for Gemini."""
    prompt_obj: dict[str, Any] = {
        "task": (
            "Given a deterministic context pack for a single security, produce an analyst-ready signal report. "
            "The context pack already contains a diversified candidate set of markets with deterministic scores. "
            "You must explain the transmission chain Market → Signal Family → Macro Domain(s) → Stock, using ONLY "
            "the values and rationales provided in the pack."
        ),
        "hard_rules": [
            "Return ONLY one JSON object (no markdown).",
            "Use only markets present in pack.markets.",
            "Prefer lower market.rank (rank=1 is best), but enforce diversity: at most one market per event_id.",
            f"Select at most MAX_MARKETS={int(max_markets)} markets.",
            f"Select at most MAX_RATE_LIKE={int(max_rate_like)} markets where is_rate_like=true.",
            "Do not invent causal stories: for domain impact explanations, only use influence_matrix_slice.rationale_md and exposure_vector.rationale.",
            "For each selected market, include at least 1 family_match evidence and at least 1 influence_edge evidence ref.",
            "Do NOT include raw numeric scoring values (final_score/base_score/quality_multiplier/market_strength) inside narrative strings (top_take, structural_relevance, actionability, themes.why, monitor_next). Use market.buckets labels instead.",
            "Structural relevance must reference the transmission_chain and market.buckets.structural_relevance, not raw base_score numbers.",
            "Actionability must reference market.market_card (resolve/pricing/context) and market.buckets.actionability/urgency (not raw market_strength numbers).",
            "If a market is skipped due to constraints, record it in exclusions with a short reason.",
            "Create 2-3 themes. Every selected market_id must appear in at least one theme.market_ids.",
            "Keep prose professional and concise. Prefer short paragraphs over lists.",
        ],
        "output_schema": _output_schema_v1(),
        "input_pack": pack,
    }
    return _SYSTEM, json.dumps(prompt_obj, ensure_ascii=False)


def generate_security_signal_report_v1(
    *,
    pack: dict[str, Any],
    model: str | None = None,
    temperature: float = 0.2,
    max_markets: int = 10,
    max_rate_like: int = 3,
) -> dict[str, Any]:
    system, prompt = build_prompt(pack=pack, max_markets=max_markets, max_rate_like=max_rate_like)
    return generate_json(prompt=prompt, system=system, model=model, temperature=temperature)
