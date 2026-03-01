"""Step-3 classification stage: strict, deterministic gated rules."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from polyscanner.signal_family_rules import SignalFamilyRule


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _hits(text: str, terms: list[str]) -> list[str]:
    t = _norm(text)
    out: list[str] = []
    for term in terms:
        term_l = str(term or "").lower().strip()
        if not term_l:
            continue
        if " " in term_l:
            if term_l in t:
                out.append(term)
        else:
            if re.search(r"[^a-z0-9_]", term_l):
                if term_l in t:
                    out.append(term)
            else:
                if re.search(rf"\b{re.escape(term_l)}\b", t):
                    out.append(term)
    return out


@dataclass(frozen=True)
class ClassificationDecision:
    signal_family_id: int
    slug: str
    is_match: bool
    rule_score: float
    evidence: dict[str, Any]


def classify_with_rule(
    *,
    market_text: str,
    family_slug: str,
    family_id: int,
    rule: SignalFamilyRule,
    min_score: float = 0.70,
) -> ClassificationDecision:
    text = market_text or ""
    exclusions_hit = _hits(text, rule.exclusions or [])
    if exclusions_hit:
        return ClassificationDecision(
            signal_family_id=int(family_id),
            slug=family_slug,
            is_match=False,
            rule_score=0.0,
            evidence={
                "exclusions_hit": exclusions_hit,
                "min_score": float(min_score),
            },
        )

    anchors = getattr(rule, "anchors", []) or []
    overrides = getattr(rule, "overrides", []) or []
    min_anchor_hits = int(getattr(rule, "min_anchor_hits", 0) or 0)

    anchor_hits = _hits(text, list(anchors)) if anchors else []
    if anchors and min_anchor_hits > 0 and len(anchor_hits) < min_anchor_hits:
        return ClassificationDecision(
            signal_family_id=int(family_id),
            slug=family_slug,
            is_match=False,
            rule_score=0.0,
            evidence={
                "anchors_hit": anchor_hits,
                "min_anchor_hits": int(min_anchor_hits),
                "min_score": float(min_score),
                "anchor_mode": "required",
            },
        )

    override_hits = _hits(text, list(overrides)) if overrides else []
    keyword_hits = _hits(text, rule.keywords or [])

    min_hits = int(rule.min_hits or 1)
    # Strict: require min_hits OR an override hit.
    if len(keyword_hits) < min_hits and not override_hits:
        return ClassificationDecision(
            signal_family_id=int(family_id),
            slug=family_slug,
            is_match=False,
            rule_score=0.0,
            evidence={
                "keyword_hits": keyword_hits,
                "override_hits": override_hits,
                "min_hits": int(min_hits),
                "min_score": float(min_score),
                "anchor_mode": "none" if not anchors else ("optional" if min_anchor_hits <= 0 else "required"),
            },
        )

    # Scoring: anchors dominate credibility; overrides add a small boost.
    #
    # Important nuance:
    # - If a family rule defines no anchors, we treat the anchor channel as "satisfied"
    #   (anchor_score=1.0). Otherwise, rules without anchors could never reach the
    #   default threshold (e.g., 0.7), which would destroy recall for families that
    #   are already keyword-precise (FOMC, Taiwan, yields, etc.).
    kw_denom = max(min_hits, 3)
    keyword_score = min(1.0, float(len(set(keyword_hits))) / float(kw_denom))
    if not anchors:
        anchor_score = 1.0
    else:
        anchor_score = (
            1.0
            if len(anchor_hits) >= max(1, min_anchor_hits)
            else (0.5 if anchor_hits else 0.0)
        )
    override_bonus = 0.20 if override_hits else 0.0

    rule_score = min(1.0, (0.55 * anchor_score) + (0.45 * keyword_score) + override_bonus)
    is_match = float(rule_score) >= float(min_score)

    matched_terms: list[str] = []
    matched_terms.extend([f"anchor:{t}" for t in anchor_hits])
    matched_terms.extend([f"override:{t}" for t in override_hits])
    matched_terms.extend(keyword_hits)

    return ClassificationDecision(
        signal_family_id=int(family_id),
        slug=family_slug,
        is_match=bool(is_match),
        rule_score=float(rule_score),
        evidence={
            "anchors_hit": anchor_hits,
            "override_hits": override_hits,
            "keyword_hits": keyword_hits,
            "exclusions_hit": exclusions_hit,
            "min_hits": int(min_hits),
            "min_anchor_hits": int(min_anchor_hits),
            "min_score": float(min_score),
            "anchor_mode": "none" if not anchors else ("optional" if min_anchor_hits <= 0 else "required"),
            "matched_terms": matched_terms,
        },
    )
