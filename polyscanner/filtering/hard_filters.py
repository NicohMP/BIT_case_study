"""Hard filters (cheap precision) for Polymarket markets + auditable decisions.

Why this exists (Step 2):
- Gamma "complete discovery" pulls in a huge universe, including many repeated
  "template factories" (sports, winner/champion templates, app-store charts,
  gossip/entertainment, meme/trivia, pure price targets).
- These are high-volume sources of false positives for equity-relevant scanning.
- We want a deterministic filter layer that is:
    (a) high precision on junk/template markets
    (b) configurable without code changes
    (c) explainable (explicit reasons)
    (d) measurable (can be audited and iterated)

This module intentionally does NOT use embeddings/LLMs. It is meant to be cheap,
fast, and auditable.
"""

from __future__ import annotations

import hashlib
import logging
import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger(__name__)


HARD_FILTER_CONFIG_PATH = Path(__file__).resolve().parent / "hard_filter_rules.yaml"


@dataclass(frozen=True)
class FilterDecision:
    market_id: int
    is_rejected: bool
    rejection_reasons: list[str]
    keep_reasons: list[str]
    quality_score: float  # 0..1
    template_score: float  # 0..1
    equity_relevance_score: float  # 0..1


@dataclass(frozen=True)
class CompiledRuleSet:
    filter_version: str
    config_sha256: str
    non_overridable_reject_groups: set[str]
    reject_patterns_by_group: dict[str, list[re.Pattern[str]]]
    keep_override_patterns_by_group: dict[str, list[re.Pattern[str]]]
    equity_relevance_patterns_by_group: dict[str, list[re.Pattern[str]]]
    weights: dict[str, Any]


_RULES_CACHE: CompiledRuleSet | None = None


def _safe_str(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    return str(x)


def _safe_float(x: Any) -> float | None:
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def _extract_text_blob(market: dict[str, Any], event: dict[str, Any] | None) -> str:
    """Combine relevant text fields into a single lowercased blob for regex scans."""
    parts: list[str] = []
    for key in ("question", "title", "slug", "category"):
        parts.append(_safe_str(market.get(key)))
    if event:
        for key in ("title", "slug"):
            parts.append(_safe_str(event.get(key)))

    # Tags can be list[str] or list[dict] (often with slug/label)
    tags: list[Any] = []
    mt = market.get("tags")
    if isinstance(mt, list):
        tags.extend(mt)
    et = (event or {}).get("tags")
    if isinstance(et, list):
        tags.extend(et)
    for t in tags:
        if isinstance(t, str):
            parts.append(t)
        elif isinstance(t, dict):
            parts.append(_safe_str(t.get("slug")))
            parts.append(_safe_str(t.get("label")))
            parts.append(_safe_str(t.get("name")))

    return " ".join([p.strip() for p in parts if p and p.strip()]).lower()


def _compile_patterns(groups: dict[str, Any]) -> dict[str, list[re.Pattern[str]]]:
    out: dict[str, list[re.Pattern[str]]] = {}
    for group, patterns in (groups or {}).items():
        compiled: list[re.Pattern[str]] = []
        if isinstance(patterns, list):
            for pat in patterns:
                if not isinstance(pat, str) or not pat.strip():
                    continue
                compiled.append(re.compile(pat, flags=re.IGNORECASE))
        out[str(group)] = compiled
    return out


def load_hard_filter_rules(*, config_path: Path | None = None, reload: bool = False) -> CompiledRuleSet:
    """Load and compile hard-filter rules from YAML.

    Caches results by default for performance (regex compilation is expensive).
    """
    global _RULES_CACHE
    if _RULES_CACHE is not None and not reload:
        return _RULES_CACHE

    path = config_path or HARD_FILTER_CONFIG_PATH
    if not path.exists():
        raise FileNotFoundError(f"Hard-filter config not found: {path}")

    raw_bytes = path.read_bytes()
    config_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    cfg = yaml.safe_load(raw_bytes) or {}
    if not isinstance(cfg, dict):
        raise TypeError("hard_filter_rules.yaml must be a mapping")

    filter_version = _safe_str(cfg.get("filter_version") or "hard_filters_v1").strip() or "hard_filters_v1"
    non_overridable = cfg.get("non_overridable_reject_groups") or []
    non_overridable_set = {str(x) for x in non_overridable if x is not None}

    rules = CompiledRuleSet(
        filter_version=filter_version,
        config_sha256=config_sha256,
        non_overridable_reject_groups=non_overridable_set,
        reject_patterns_by_group=_compile_patterns(cfg.get("reject_patterns_by_group") or {}),
        keep_override_patterns_by_group=_compile_patterns(cfg.get("keep_override_patterns_by_group") or {}),
        equity_relevance_patterns_by_group=_compile_patterns(cfg.get("equity_relevance_patterns_by_group") or {}),
        weights=cfg.get("weights") or {},
    )

    _RULES_CACHE = rules
    log.info("Loaded hard filter rules version=%s sha256=%s", rules.filter_version, rules.config_sha256[:12])
    return rules


def _matches_any(patterns: list[re.Pattern[str]], text: str) -> bool:
    for p in patterns:
        if p.search(text):
            return True
    return False


def _score_from_groups(
    *,
    hits: set[str],
    weights_map: dict[str, Any],
) -> float:
    """Convert a set of hit group names to a 0..1 score using weights.

    We treat weights as additive evidence then clamp.
    """
    total = 0.0
    for g in hits:
        w = weights_map.get(g)
        try:
            total += float(w)
        except Exception:
            total += 0.0
    return _clamp01(total)


def _quality_score(market: dict[str, Any], *, weights: dict[str, Any]) -> tuple[float, list[str]]:
    """Compute 0..1 quality score + keep reasons.

    Quality is deliberately simple and deterministic:
    - Higher volume/liquidity => higher score (log-scaled)
    - Ended markets are penalized heavily (should not appear in active universe,
      but we guard anyway)
    """
    keep: list[str] = []

    vol = _safe_float(market.get("volume_usd") or market.get("volumeUsd") or market.get("volume"))
    liq = _safe_float(market.get("liquidity_usd") or market.get("liquidityUsd") or market.get("liquidity"))

    quality_cfg = (weights or {}).get("quality") if isinstance(weights, dict) else {}
    if not isinstance(quality_cfg, dict):
        quality_cfg = {}

    volume_log_cap = float(quality_cfg.get("volume_log_cap") or 14.0)
    liquidity_log_cap = float(quality_cfg.get("liquidity_log_cap") or 12.0)
    volume_weight = float(quality_cfg.get("volume_weight") or 0.55)
    liquidity_weight = float(quality_cfg.get("liquidity_weight") or 0.35)
    end_date_weight = float(quality_cfg.get("end_date_weight") or 0.10)
    ended_multiplier = float(quality_cfg.get("ended_multiplier") or 0.15)

    vol_score = 0.0
    if vol is not None and vol >= 0:
        vol_score = _clamp01(math.log1p(vol) / max(1e-9, volume_log_cap))
        if vol >= 10_000:
            keep.append("quality:volume_high")
        elif vol >= 1_000:
            keep.append("quality:volume_mid")

    liq_score = 0.0
    if liq is not None and liq >= 0:
        liq_score = _clamp01(math.log1p(liq) / max(1e-9, liquidity_log_cap))
        if liq >= 10_000:
            keep.append("quality:liquidity_high")
        elif liq >= 1_000:
            keep.append("quality:liquidity_mid")

    # End-date score: prefer markets that haven't already ended.
    now = _utcnow()
    end_date = market.get("end_date")
    ended = False
    if isinstance(end_date, datetime):
        ended = end_date < now
    elif isinstance(end_date, str) and end_date.strip():
        # Some callers may pass ISO strings; avoid pulling in dateutil here.
        try:
            ended = datetime.fromisoformat(end_date.replace("Z", "+00:00")) < now
        except Exception:
            ended = False

    end_score = 1.0 if not ended else ended_multiplier
    if ended:
        keep.append("quality:ended_penalty")

    score = (volume_weight * vol_score) + (liquidity_weight * liq_score) + (end_date_weight * end_score)
    return (_clamp01(score), keep)


def evaluate_market_filter(market: dict[str, Any], event: dict[str, Any] | None) -> FilterDecision:
    """Evaluate a single market with optional event context."""
    rules = load_hard_filter_rules()

    market_id = market.get("pm_market_id") or market.get("market_id") or market.get("id")
    try:
        market_id_int = int(market_id)
    except Exception as e:
        raise ValueError(f"Market missing integer id (got {market_id!r})") from e

    text = _extract_text_blob(market, event)

    reject_groups_hit: set[str] = set()
    rejection_reasons: list[str] = []

    # Hard rejects: high precision template/junk buckets.
    for group, patterns in rules.reject_patterns_by_group.items():
        if not patterns:
            continue
        if _matches_any(patterns, text):
            reject_groups_hit.add(group)

    # Keep overrides: if we match these, we can rescue borderline templates (e.g., price targets)
    # when there is explicit policy/macro/regulatory context.
    override_groups_hit: set[str] = set()
    keep_reasons: list[str] = []
    for group, patterns in rules.keep_override_patterns_by_group.items():
        if not patterns:
            continue
        if _matches_any(patterns, text):
            override_groups_hit.add(group)
            keep_reasons.append(f"override:{group}")

    # Equity relevance: this is NOT a hard keep; it is a soft scoring feature.
    relevance_groups_hit: set[str] = set()
    for group, patterns in rules.equity_relevance_patterns_by_group.items():
        if not patterns:
            continue
        if _matches_any(patterns, text):
            relevance_groups_hit.add(group)
            keep_reasons.append(f"relevance:{group}")

    # Build explicit reasons (stable strings for aggregation / stats).
    group_to_reason = {
        "sports": "reject:sports_market",
        "winner_template": "reject:winner_template",
        "appstore_charts": "reject:appstore_charts",
        "entertainment_gossip": "reject:entertainment_gossip",
        "meme_trivia": "reject:meme_trivia",
        "politics_polls": "reject:politics_polls",
        "political_leader_template": "reject:political_leader_template",
        "micro_price_bets": "reject:micro_price_bets",
        "price_target_template": "reject:price_target_template",
        "religion_prophecy": "reject:religion_prophecy",
    }
    template_hit_reasons: list[str] = [group_to_reason.get(g, f"reject:{g}") for g in sorted(reject_groups_hit)]

    # Decide rejection with overrides.
    non_overridable_hit = any(g in rules.non_overridable_reject_groups for g in reject_groups_hit)
    overridable_reject = bool(reject_groups_hit) and not non_overridable_hit
    has_override = bool(override_groups_hit)
    is_rejected = bool(reject_groups_hit) and (non_overridable_hit or not has_override)

    # Important invariant for auditability:
    # - `rejection_reasons` should be populated only when `is_rejected` is True.
    # - If a market matches template patterns but is kept (e.g., override applied),
    #   record that in `keep_reasons` instead.
    if is_rejected:
        rejection_reasons.extend(template_hit_reasons)
    else:
        for g in sorted(reject_groups_hit):
            keep_reasons.append(f"template:{g}")
        if overridable_reject and has_override:
            keep_reasons.append("kept:override_applied")

    # Scores
    w = rules.weights or {}
    template_weight_map = (w.get("template_group_weight") if isinstance(w, dict) else None) or {}
    relevance_weight_map = (w.get("relevance_group_weight") if isinstance(w, dict) else None) or {}

    template_score = _score_from_groups(hits=reject_groups_hit, weights_map=template_weight_map)
    equity_relevance_score = _score_from_groups(hits=relevance_groups_hit, weights_map=relevance_weight_map)
    quality_score, quality_keep = _quality_score(market, weights=w)
    keep_reasons.extend(quality_keep)

    # If we reject, keep/quality reasons still matter for audits (we want to see why we rejected
    # "high volume sports" etc.). Do not discard them.
    if is_rejected and not rejection_reasons:
        rejection_reasons.append("reject:rule_hit")

    return FilterDecision(
        market_id=market_id_int,
        is_rejected=bool(is_rejected),
        rejection_reasons=rejection_reasons,
        keep_reasons=keep_reasons,
        quality_score=_clamp01(quality_score),
        template_score=_clamp01(template_score),
        equity_relevance_score=_clamp01(equity_relevance_score),
    )
