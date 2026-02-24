"""Data-driven Polymarket tag selection (notebook-friendly).

This module implements the "evidence-first" tag-selection approach:

- Discover tag candidates from *active events* (what is in use right now).
- For each tag, sample a small set of markets via `/events?tag_id=...`.
- Compute a per-tag "yield vector" over signal families using transparent
  keyword rules (see `polyscanner/signal_family_rules.py`).
- Select a compact allowlist under simple, tunable constraints that balance:
  - recall (enough tags per family)
  - diversity (avoid overly-generic / overlapping tags)

Why this exists
---------------
Gamma tag labels/slugs are often opaque entities ("jto", "grok").
Embedding similarity against theme strings can miss these (low recall) or pick
generic tags (low precision). Instead we judge tags by *what markets they retrieve*.

This file is intentionally pure-Python (no pandas required) so it can be reused
both from notebooks and from lightweight scripts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable

from polyscanner.signal_family_rules import RULES_BY_SLUG, SignalFamilyRule


def _norm(text: str) -> str:
    """Lowercase + whitespace normalize for matching."""
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _hits(text: str, terms: list[str]) -> list[str]:
    """Return matched terms in `text` using phrase or token-boundary matching."""
    t = _norm(text)
    out: list[str] = []
    for term in terms:
        term_l = (term or "").lower().strip()
        if not term_l:
            continue
        if " " in term_l:
            if term_l in t:
                out.append(term)
        else:
            # If the term contains non-word characters (e.g., "#1"), token boundaries
            # are unreliable; fall back to substring matching.
            if re.search(r"[^a-z0-9_]", term_l):
                if term_l in t:
                    out.append(term)
            else:
                if re.search(rf"\b{re.escape(term_l)}\b", t):
                    out.append(term)
    return out


def match_text_to_rule(*, text: str, rule: SignalFamilyRule) -> tuple[float, list[str]]:
    """Return (match_score, matched_terms) for a rule against a text.

    Scoring:
    - requires >= rule.min_hits keyword hits
    - returns len(matched)/len(keywords), capped at 1.0
    """
    matched = _hits(text, rule.keywords)
    if rule.exclusions and _hits(text, rule.exclusions):
        return 0.0, []
    if len(matched) < int(rule.min_hits):
        return 0.0, []
    denom = max(1, len(rule.keywords))
    score = min(1.0, float(len(matched)) / float(denom))
    return float(score), matched


def family_keyword_evidence(text: str) -> dict[str, int]:
    """Count keyword hits per signal family in `text` (event title or market question)."""
    out: dict[str, int] = {}
    for slug, rule in RULES_BY_SLUG.items():
        score, matched = match_text_to_rule(text=text, rule=rule)
        if score > 0 and matched:
            out[slug] = int(len(matched))
    return out


def market_text(m: dict[str, Any]) -> str:
    """Return the canonical market text used throughout selection."""
    return str(m.get("question") or m.get("title") or "").strip()


@dataclass(frozen=True)
class TagStat:
    """Lightweight per-tag stats derived from active events."""

    tag_id: int
    label: str | None
    slug: str | None
    event_count: int
    family_hit_counts: dict[str, int]


def _safe_int(x: Any) -> int | None:
    try:
        return int(x)
    except Exception:
        return None


def _safe_str(x: Any) -> str | None:
    return str(x).strip() if isinstance(x, str) and str(x).strip() else None


def discover_tag_stats_from_active_events(
    *,
    base_url: str | None = None,
    events_page_size: int = 100,
    events_max_pages: int = 200,
    sleep_s: float = 0.05,
) -> list[TagStat]:
    """Scan active events and compute per-tag frequency + family keyword evidence.

    Single responsibility:
    - Use active events as the candidate universe so we bias toward tags in use now.
    - Use only event titles/questions for keyword evidence (cheap, no market fetch).
    """
    from polyscanner.ingestion.tag_base import iter_active_events  # noqa: WPS433

    counts: dict[int, int] = {}
    label_by_id: dict[int, str | None] = {}
    slug_by_id: dict[int, str | None] = {}
    family_hits_by_tag: dict[int, dict[str, int]] = {}

    for ev in iter_active_events(
        limit=int(events_page_size),
        max_pages=int(events_max_pages),
        sleep_s=float(sleep_s),
        base_url=base_url,
    ):
        if not isinstance(ev, dict):
            continue

        ev_text = str(ev.get("title") or ev.get("question") or "").strip()
        if not ev_text:
            continue

        ev_evidence = family_keyword_evidence(ev_text)
        tags = ev.get("tags") or []
        if not isinstance(tags, list):
            continue

        for t in tags:
            if not isinstance(t, dict):
                continue
            tid = _safe_int(t.get("id"))
            if tid is None:
                continue

            counts[tid] = counts.get(tid, 0) + 1
            label_by_id[tid] = _safe_str(t.get("label")) or label_by_id.get(tid)
            slug_by_id[tid] = _safe_str(t.get("slug")) or slug_by_id.get(tid)

            if ev_evidence:
                fh = family_hits_by_tag.setdefault(tid, {})
                for fam, c in ev_evidence.items():
                    fh[fam] = fh.get(fam, 0) + int(c)

    out: list[TagStat] = []
    for tid, cnt in counts.items():
        out.append(
            TagStat(
                tag_id=int(tid),
                label=label_by_id.get(tid),
                slug=slug_by_id.get(tid),
                event_count=int(cnt),
                family_hit_counts=family_hits_by_tag.get(tid, {}),
            )
        )
    out.sort(key=lambda x: (x.event_count, sum(x.family_hit_counts.values())), reverse=True)
    return out


@dataclass(frozen=True)
class TagYield:
    """Per-tag yield vector over signal families, computed from sampled markets."""

    tag_id: int
    n_markets: int
    family_counts: dict[str, int]
    family_mean_scores: dict[str, float]
    matched_market_ids: dict[str, list[int]]
    top_family: str | None
    top_count: int
    top_minus_second: int


def compute_tag_yield(
    *,
    tag_id: int,
    markets: list[dict[str, Any]],
    rules_by_slug: dict[str, SignalFamilyRule] = RULES_BY_SLUG,
) -> TagYield:
    """Compute a tag→signal-family yield vector from a sampled market set."""
    family_counts = {slug: 0 for slug in rules_by_slug.keys()}
    family_scores: dict[str, list[float]] = {slug: [] for slug in rules_by_slug.keys()}
    matched_market_ids: dict[str, list[int]] = {slug: [] for slug in rules_by_slug.keys()}

    for m in markets:
        q = market_text(m)
        if not q:
            continue

        for slug, rule in rules_by_slug.items():
            score, _terms = match_text_to_rule(text=q, rule=rule)
            if score <= 0:
                continue
            family_counts[slug] += 1
            family_scores[slug].append(float(score))

            mid = m.get("id")
            if mid is None:
                continue
            try:
                matched_market_ids[slug].append(int(mid))
            except Exception:
                continue

    family_mean_scores = {
        slug: (sum(scores) / float(len(scores)) if scores else 0.0)
        for slug, scores in family_scores.items()
    }
    for slug in matched_market_ids:
        matched_market_ids[slug] = sorted(set(matched_market_ids[slug]))

    top_family = max(family_counts, key=lambda k: family_counts[k]) if family_counts else None
    top_count = family_counts[top_family] if top_family else 0
    second_count = sorted(family_counts.values(), reverse=True)[1] if len(family_counts) > 1 else 0

    return TagYield(
        tag_id=int(tag_id),
        n_markets=int(len(markets)),
        family_counts=family_counts,
        family_mean_scores=family_mean_scores,
        matched_market_ids=matched_market_ids,
        top_family=top_family,
        top_count=int(top_count),
        top_minus_second=int(top_count - second_count),
    )


def yield_rows_long(
    *,
    tag_stats: Iterable[TagStat],
    tag_yields: Iterable[TagYield],
) -> list[dict[str, Any]]:
    """Return a long-form list of dict rows for notebook analysis (tag×family)."""
    stats_by_id = {int(s.tag_id): s for s in tag_stats}
    rows: list[dict[str, Any]] = []
    for ty in tag_yields:
        s = stats_by_id.get(int(ty.tag_id))
        for fam, cnt in ty.family_counts.items():
            rows.append(
                {
                    "tag_id": int(ty.tag_id),
                    "label": (s.label if s else None),
                    "slug": (s.slug if s else None),
                    "event_count": int(s.event_count if s else 0),
                    "family": fam,
                    "yield_count": int(cnt),
                    "yield_rate": float(cnt) / float(max(1, int(ty.n_markets))),
                    "mean_match_score": float(ty.family_mean_scores.get(fam, 0.0)),
                    "top_family": ty.top_family,
                    "top_minus_second": int(ty.top_minus_second),
                    "n_markets": int(ty.n_markets),
                }
            )
    return rows


def select_allowlist_from_yield_rows(
    *,
    yield_rows: list[dict[str, Any]],
    min_yield_count: int = 2,
    min_top_minus_second: int = 1,
    top_k_per_family: int = 25,
    generic_slugs: set[str] | None = None,
) -> tuple[dict[str, list[dict[str, Any]]], list[int]]:
    """Select tag_ids per family under simple, explainable rules.

    Returns:
    - selected_by_family: family_slug -> list[rows] (sorted best-first)
    - allowlist_tag_ids: union of selected tag_ids (sorted)
    """
    generic_slugs = {s.strip().lower() for s in (generic_slugs or set()) if str(s).strip()}

    by_family: dict[str, list[dict[str, Any]]] = {}
    for r in yield_rows:
        fam = str(r.get("family") or "").strip()
        if not fam:
            continue
        by_family.setdefault(fam, []).append(dict(r))

    selected_by_family: dict[str, list[dict[str, Any]]] = {}
    for fam, rows in by_family.items():
        # Filter obvious generic tags by slug (label-based generic filtering is too risky).
        rows2 = []
        for r in rows:
            slug_l = str(r.get("slug") or "").strip().lower()
            if slug_l and slug_l in generic_slugs:
                continue
            if int(r.get("yield_count") or 0) < int(min_yield_count):
                continue
            if int(r.get("top_minus_second") or 0) < int(min_top_minus_second):
                continue
            rows2.append(r)

        rows2.sort(
            key=lambda x: (
                float(x.get("yield_count") or 0),
                float(x.get("yield_rate") or 0),
                float(x.get("event_count") or 0),
            ),
            reverse=True,
        )
        selected_by_family[fam] = rows2[: int(top_k_per_family)]

    allowlist_tag_ids = sorted({int(r["tag_id"]) for rows in selected_by_family.values() for r in rows})
    return selected_by_family, allowlist_tag_ids


def run_data_driven_tag_selection(
    *,
    base_url: str | None = None,
    # Candidate universe
    events_page_size: int = 100,
    events_max_pages: int = 200,
    sleep_s: float = 0.05,
    max_tag_candidates: int = 600,
    # Evidence sampling
    markets_per_tag: int = 20,
    min_markets_per_tag: int = 5,
    # Selection knobs
    min_yield_count: int = 2,
    min_top_minus_second: int = 1,
    top_k_per_family: int = 25,
    generic_slugs: set[str] | None = None,
) -> dict[str, Any]:
    """End-to-end data-driven tag selection (discover → sample → yield → select)."""
    from polyscanner.ingestion.tag_base import fetch_markets_for_tag  # noqa: WPS433

    stats = discover_tag_stats_from_active_events(
        base_url=base_url,
        events_page_size=events_page_size,
        events_max_pages=events_max_pages,
        sleep_s=sleep_s,
    )

    # Candidate shortlist (what we will pay to sample markets for).
    stats2 = stats[: int(max_tag_candidates)]

    tag_yields: list[TagYield] = []
    markets_cache: dict[int, list[dict[str, Any]]] = {}

    for s in stats2:
        mkts = fetch_markets_for_tag(
            int(s.tag_id),
            markets_cap=int(markets_per_tag),
            base_url=base_url,
        )
        markets_cache[int(s.tag_id)] = mkts
        if len(mkts) < int(min_markets_per_tag):
            continue
        tag_yields.append(compute_tag_yield(tag_id=int(s.tag_id), markets=mkts))

    rows = yield_rows_long(tag_stats=stats2, tag_yields=tag_yields)
    selected_by_family, allowlist_tag_ids = select_allowlist_from_yield_rows(
        yield_rows=rows,
        min_yield_count=min_yield_count,
        min_top_minus_second=min_top_minus_second,
        top_k_per_family=top_k_per_family,
        generic_slugs=generic_slugs,
    )

    return {
        "tag_stats": stats2,
        "markets_cache": markets_cache,
        "tag_yields": tag_yields,
        "yield_rows": rows,
        "selected_by_family": selected_by_family,
        "allowlist_tag_ids": allowlist_tag_ids,
        "rules_by_slug": RULES_BY_SLUG,
    }
