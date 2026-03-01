"""Transmission channel relevance heuristics (MVP).

This module provides a lightweight, transparent classifier that maps a market's
text to a 4-vector over transmission channels:
- discount_rate
- demand
- supply
- regulation

Output is designed to be debuggable:
- scores are in [0, 1]
- matched_terms shows which keywords fired

This is intentionally simple and deterministic. An LLM-based classifier can be
added later if needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


CHANNELS = ("discount_rate", "demand", "supply", "regulation")


_TERMS: dict[str, list[str]] = {
    "discount_rate": [
        "fed",
        "fomc",
        "interest rate",
        "rates",
        "yield",
        "yields",
        "treasury",
        "inflation",
        "cpi",
        "pce",
        "tightening",
        "cut",
        "hike",
    ],
    "demand": [
        "recession",
        "growth",
        "gdp",
        "unemployment",
        "consumer spending",
        "consumer demand",
        "enterprise spending",
        "ad spend",
        "ad budgets",
        "sales",
        "demand",
        "adoption",
    ],
    "supply": [
        "export controls",
        "sanctions",
        "supply chain",
        "shortage",
        "capacity",
        "bottleneck",
        "manufacturing",
        "shipping",
        "tariff",
        "tariffs",
    ],
    "regulation": [
        "regulation",
        "regulatory",
        "ban",
        "approve",
        "approval",
        "sec",
        "ftc",
        "doj",
        "antitrust",
        "law",
        "policy",
        "compliance",
        "enforcement",
    ],
}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _count_matches(text: str, terms: list[str]) -> list[str]:
    text_l = _norm(text)
    hits: list[str] = []
    for t in terms:
        t_l = t.lower()
        if " " in t_l:
            if t_l in text_l:
                hits.append(t)
        else:
            if re.search(rf"\b{re.escape(t_l)}\b", text_l):
                hits.append(t)
    return hits


def _score_from_hits(n_hits: int) -> float:
    """Convert number of matches into a bounded score in [0, 1]."""
    if n_hits <= 0:
        return 0.0
    if n_hits == 1:
        return 0.35
    if n_hits == 2:
        return 0.65
    return 1.0


@dataclass(frozen=True)
class ChannelRelevance:
    scores: dict[str, float]
    matched_terms: dict[str, list[str]]


def score_channels(*, question: str, category: str | None = None) -> ChannelRelevance:
    """Compute channel relevance for a market.

    Inputs:
    - question: market question/title (primary signal)
    - category: optional tag/category label (secondary signal)
    """
    text = question if not category else f"{question} {category}"

    matched: dict[str, list[str]] = {}
    scores: dict[str, float] = {}
    for ch in CHANNELS:
        hits = _count_matches(text, _TERMS[ch])
        matched[ch] = hits
        scores[ch] = _score_from_hits(len(hits))
    return ChannelRelevance(scores=scores, matched_terms=matched)

