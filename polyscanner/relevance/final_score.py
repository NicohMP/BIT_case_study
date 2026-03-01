"""Final relevance scoring combining domains + transmission channels (MVP).

Score definition:
For each market and each domain:
  final(market, domain) = domain_rel(market→domain) * sum_c(channel_rel(market→c) * exposure(domain,c))

We then pick the best domain per market (argmax final) and rank markets by that best score.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from polyscanner.models import DomainChannelExposure, DomainDefinition, PMMarket
from polyscanner.relevance.channels import ChannelRelevance, score_channels
from polyscanner.relevance.domain_relevance import DomainScore, EmbeddingDomainScorer, score_domains


@dataclass(frozen=True)
class ScoredMarket:
    market: PMMarket
    best_domain: DomainScore
    channel_relevance: ChannelRelevance
    exposure_by_channel: dict[str, float]
    exposure_dot: float
    final_score: float


def _dot(channel_scores: dict[str, float], exposure_by_channel: dict[str, float]) -> float:
    return float(sum(float(channel_scores.get(k, 0.0)) * float(v) for k, v in exposure_by_channel.items()))


def _exposure_vector(
    domain_id: int,
    exposure_matrix: dict[int, dict[str, DomainChannelExposure]],
) -> dict[str, float]:
    by_ch = exposure_matrix.get(domain_id, {})
    return {slug: float(e.exposure) for slug, e in by_ch.items()}


def score_market(
    market: PMMarket,
    domain_definitions: list[DomainDefinition],
    exposure_matrix: dict[int, dict[str, DomainChannelExposure]],
    *,
    prefer_embeddings: bool = True,
    embedding_model_name: str = "all-MiniLM-L6-v2",
    embedding_device: str | None = None,
    domain_scorer: EmbeddingDomainScorer | None = None,
) -> ScoredMarket:
    """Score a single market and select its best domain."""
    # If no exposure matrix is provided (or it is empty), treat channels as disabled:
    # final_score falls back to domain_relevance only.
    channels_enabled = any(exposure_matrix.values())
    channel_rel = score_channels(question=market.question, category=market.category) if channels_enabled else ChannelRelevance(scores={}, matched_terms={})
    dom_scores = score_domains(
        market,
        domain_definitions,
        prefer_embeddings=prefer_embeddings,
        model_name=embedding_model_name,
        device=embedding_device,
        scorer=domain_scorer,
    )
    if not dom_scores:
        raise RuntimeError("No domain definitions provided")

    best: ScoredMarket | None = None
    for ds in dom_scores:
        exp_vec = _exposure_vector(ds.domain_id, exposure_matrix) if channels_enabled else {}
        exp_dot = _dot(channel_rel.scores, exp_vec) if channels_enabled else 1.0
        final = float(ds.domain_relevance) * float(exp_dot)
        sm = ScoredMarket(
            market=market,
            best_domain=ds,
            channel_relevance=channel_rel,
            exposure_by_channel=exp_vec,
            exposure_dot=float(exp_dot),
            final_score=float(final),
        )
        if best is None or sm.final_score > best.final_score:
            best = sm

    assert best is not None
    return best


def rank_markets(
    markets: list[PMMarket],
    domain_definitions: list[DomainDefinition],
    exposure_matrix: dict[int, dict[str, DomainChannelExposure]],
    *,
    top_n: int = 10,
    prefer_embeddings: bool = True,
    embedding_model_name: str = "all-MiniLM-L6-v2",
    embedding_device: str | None = None,
) -> list[ScoredMarket]:
    """Score and rank markets by best final_score."""
    scored: list[ScoredMarket] = []
    domain_scorer = None
    if prefer_embeddings:
        try:
            domain_scorer = EmbeddingDomainScorer(
                domains=domain_definitions,
                model_name=embedding_model_name,
                device=embedding_device,
            )
        except Exception:
            domain_scorer = None
    for m in markets:
        try:
            scored.append(
                score_market(
                    m,
                    domain_definitions,
                    exposure_matrix,
                    prefer_embeddings=prefer_embeddings,
                    embedding_model_name=embedding_model_name,
                    embedding_device=embedding_device,
                    domain_scorer=domain_scorer,
                )
            )
        except Exception:
            continue

    scored.sort(key=lambda x: x.final_score, reverse=True)
    return scored[:top_n]


def to_jsonable(sm: ScoredMarket) -> dict[str, Any]:
    """Convert to a notebook/JSON-friendly dict."""
    return {
        "pm_market_id": sm.market.pm_market_id,
        "question": sm.market.question,
        "category": sm.market.category,
        "probability": sm.market.probability,
        "volume": sm.market.volume,
        "best_domain": sm.best_domain.domain_name,
        "domain_relevance": sm.best_domain.domain_relevance,
        "raw_domain_similarity": sm.best_domain.raw_similarity,
        "channel_relevance": sm.channel_relevance.scores,
        "channel_matched_terms": sm.channel_relevance.matched_terms,
        "domain_exposure": sm.exposure_by_channel,
        "exposure_dot": sm.exposure_dot,
        "final_score": sm.final_score,
    }
