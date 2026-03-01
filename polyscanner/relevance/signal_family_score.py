"""Deterministic relevance scoring using signal families.

This module implements an auditable scoring function:

relevance(market, security) =
  Σ_family Σ_domain match(market→family) × influence(family→domain) × exposure(security→domain)

Design goals:
- Deterministic (no LLM in the core score)
- Debuggable (returns a full breakdown trace)
- Cheap enough for notebook iteration
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


INFLUENCE_CALIBRATION: dict[int, float] = {
    0: 0.00,
    1: 0.05,
    2: 0.20,
    3: 0.45,
    4: 0.70,
    5: 1.00,
}


def influence_to_weight(score: int) -> float:
    """Map ordinal influence score (0..5) to a calibrated weight in [0,1]."""
    try:
        s = int(score)
    except Exception:
        s = 0
    s = max(0, min(5, s))
    return float(INFLUENCE_CALIBRATION[s])


def volume_norm(volume_usd: float | None, *, max_ref: float = 1e7) -> float:
    """Normalize volume to [0,1] using a log scale."""
    if volume_usd is None:
        return 0.0
    v = max(0.0, float(volume_usd))
    denom = math.log1p(float(max_ref))
    if denom <= 0:
        return 0.0
    x = math.log1p(v) / denom
    return float(max(0.0, min(1.0, x)))


@dataclass(frozen=True)
class FamilyMatch:
    signal_family_id: int
    signal_family_slug: str
    match_score: float  # 0..1


@dataclass(frozen=True)
class DomainExposure:
    macro_domain_id: int
    macro_domain_name: str
    weight: float  # 0..1


@dataclass(frozen=True)
class InfluenceCell:
    signal_family_id: int
    macro_domain_id: int
    score: int  # 0..5 (ordinal)


def keep_top_k_family_matches(matches: list[FamilyMatch], *, k: int = 2) -> list[FamilyMatch]:
    """Keep top-k family matches by match_score to avoid double-counting."""
    ms = sorted(matches, key=lambda m: float(m.match_score), reverse=True)
    return ms[: max(0, int(k))]


def score_market_for_security(
    *,
    market: dict[str, Any],
    security_id: int,
    family_matches: list[FamilyMatch],
    domain_exposures: list[DomainExposure],
    influence_cells: list[InfluenceCell],
    top_k_families: int = 2,
    use_volume_boost: bool = True,
) -> dict[str, Any]:
    """Compute final_score and a full contribution breakdown for one market + one security."""
    # Index influences: family_id -> domain_id -> ordinal score
    infl: dict[int, dict[int, int]] = {}
    for c in influence_cells:
        infl.setdefault(int(c.signal_family_id), {})[int(c.macro_domain_id)] = int(c.score)

    matches_k = keep_top_k_family_matches(family_matches, k=top_k_families)

    breakdown: list[dict[str, Any]] = []
    relevance = 0.0
    for m in matches_k:
        fam_infl = infl.get(int(m.signal_family_id), {})
        for d in domain_exposures:
            iw = influence_to_weight(fam_infl.get(int(d.macro_domain_id), 0))
            dw = float(d.weight)
            ms = float(m.match_score)
            contrib = ms * iw * dw
            if contrib <= 0.0:
                continue
            relevance += contrib
            breakdown.append(
                {
                    "security_id": int(security_id),
                    "pm_market_id": int(market.get("pm_market_id")),
                    "signal_family": m.signal_family_slug,
                    "domain": d.macro_domain_name,
                    "match_score": ms,
                    "influence_weight": iw,
                    "domain_weight": dw,
                    "contribution": contrib,
                }
            )

    vol_val = market.get("volume_usd")
    if vol_val is None:
        vol_val = market.get("volume")
    vol = float(vol_val) if vol_val is not None else 0.0
    vol_n = volume_norm(vol)
    final = float(relevance)
    if use_volume_boost:
        final = float(relevance) * (0.3 + 0.7 * vol_n)

    breakdown.sort(key=lambda x: float(x.get("contribution", 0.0)), reverse=True)

    return {
        "pm_market_id": int(market.get("pm_market_id")),
        "question": market.get("question"),
        "probability": market.get("probability"),
        "volume_usd": market.get("volume_usd") if market.get("volume_usd") is not None else market.get("volume"),
        "security_id": int(security_id),
        "relevance": float(relevance),
        "volume_norm": float(vol_n),
        "final_score": float(final),
        "breakdown": breakdown,
    }


def score_markets_for_security(
    *,
    markets: list[dict[str, Any]],
    security_id: int,
    matches_by_market_id: dict[int, list[FamilyMatch]],
    domain_exposures: list[DomainExposure],
    influence_cells: list[InfluenceCell],
    top_k_families: int = 2,
    use_volume_boost: bool = True,
) -> list[dict[str, Any]]:
    """Score many markets for one security and return sorted scored items."""
    scored: list[dict[str, Any]] = []
    for m in markets:
        pm_market_id = m.get("pm_market_id")
        if pm_market_id is None:
            continue
        mid = int(pm_market_id)
        fam_matches = matches_by_market_id.get(mid, [])
        if not fam_matches:
            continue
        scored.append(
            score_market_for_security(
                market=m,
                security_id=security_id,
                family_matches=fam_matches,
                domain_exposures=domain_exposures,
                influence_cells=influence_cells,
                top_k_families=top_k_families,
                use_volume_boost=use_volume_boost,
            )
        )
    scored.sort(key=lambda x: float(x.get("final_score", 0.0)), reverse=True)
    return scored
