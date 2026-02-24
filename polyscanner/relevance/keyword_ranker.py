"""Simple keyword relevance scoring for the MVP pipeline.

Goal:
- Use the `bit_domain` table (domain names) as the only taxonomy input.
- Rank Polymarket markets against those domains using lightweight keyword matching.
"""

from __future__ import annotations

import math
import re
from typing import Iterable

from polyscanner.models import Domain, PMMarket, RankedMarket


_DOMAIN_KEYWORDS: dict[str, list[str]] = {
    # Minimal helper keywords to improve recall beyond literal domain name matching.
    "Digital Assets & Blockchain Infrastructure": ["bitcoin", "ethereum", "crypto", "stablecoin", "etf", "coinbase", "mining"],
    "Compute & Semiconductors": ["chip", "semiconductor", "gpu", "foundry", "tsmc", "nvidia", "asml", "memory", "export control"],
    "AI & Data": ["ai", "artificial intelligence", "llm", "openai", "chatgpt", "anthropic", "data", "observability"],
    "Cloud & Software Infrastructure": ["cloud", "aws", "azure", "gcp", "datacenter", "saas", "enterprise software"],
    "Consumer Internet & Digital Media": ["social", "ads", "advertising", "e-commerce", "marketplace", "tiktok", "instagram", "reddit"],
    "Fintech & Market Infrastructure": ["payments", "fintech", "brokerage", "trading", "exchange", "visa", "mastercard", "robinhood"],
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def score_market_against_domain(market: PMMarket, domain: Domain) -> float:
    text = f"{market.question} {market.category or ''}".strip().lower()
    tokens = set(_tokenize(text))

    # Start with literal domain-name tokens (e.g., "semiconductors").
    domain_tokens = [t for t in _tokenize(domain.name) if t not in {"and"} and len(t) >= 3]
    score = 0.0
    for t in domain_tokens:
        if t in tokens:
            score += 1.0

    # Add a few curated keywords for recall.
    for kw in _DOMAIN_KEYWORDS.get(domain.name, []):
        kw_l = kw.lower()
        if " " in kw_l:
            if kw_l in text:
                score += 1.0
        else:
            if kw_l in tokens:
                score += 1.0

    # Light volume weighting so we prefer liquid/active markets.
    vol = market.volume or 0.0
    score *= 1.0 + math.log10(1.0 + max(0.0, vol))
    return score


def rank_markets_for_domains(markets: Iterable[PMMarket], domains: list[Domain], top_n: int = 10) -> list[RankedMarket]:
    ranked: list[RankedMarket] = []
    for m in markets:
        best_domain: str | None = None
        best_score = 0.0
        for d in domains:
            s = score_market_against_domain(m, d)
            if s > best_score:
                best_score = s
                best_domain = d.name

        ranked.append(RankedMarket(market=m, score=best_score, heuristic_domain=best_domain if best_score > 0 else None))

    ranked.sort(key=lambda r: r.score, reverse=True)
    return ranked[:top_n]

