"""Signal-family MVP pipeline (notebook-friendly).

End-to-end (pre-scoring) flow:
1) Read `signal_family` + `signal_family_domain_influence` from Postgres (Supabase)
2) Read Step-3 matcher outputs from `pm_market_signal_family_match`
3) Render a markdown report with top markets per signal family

This is intentionally simple. It lets you validate that:
- the authority layer exists and is queryable
- the matching logic is sane
- you can produce a report end-to-end
"""

from __future__ import annotations

import json
import re
import hashlib
import math
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from polyscanner.db.pg import (
    fetch_macro_domains,
    fetch_signal_families,
    fetch_signal_family_domain_influence,
    fetch_top_markets_for_signal_family,
)
from polyscanner.env import get_env, load_env
from polyscanner.llm.signal_family_report import generate_signal_family_report_with_gemini
from polyscanner.reporting.signal_family_markdown import render_signal_family_llm_report_markdown
from polyscanner.filtering.hard_filters import load_hard_filter_rules


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def render_signal_family_report_markdown(
    *,
    as_of: datetime,
    signal_families: list[dict[str, Any]],
    macro_domains: list[dict[str, Any]],
    influence_rows: list[dict[str, Any]],
    top_markets_by_family: dict[int, list[dict[str, Any]]],
) -> str:
    lines: list[str] = []
    lines.append("# Signal Family Report (MVP)")
    lines.append("")
    lines.append(f"- Generated at: `{as_of.isoformat()}`")
    lines.append("")

    # Build influence lookup: family_id -> {domain_id -> score}
    infl: dict[int, dict[int, dict[str, Any]]] = {}
    for r in influence_rows:
        infl.setdefault(int(r["signal_family_id"]), {})[int(r["macro_domain_id"])] = r

    lines.append("## Signal families")
    lines.append("")
    for sf in signal_families:
        sf_id = int(sf["id"])
        lines.append(f"## {sf['title']}")
        lines.append(f"- `slug`: `{sf['slug']}`")

        # Influence row (context, not used for matching yet)
        scores = []
        for d in macro_domains:
            d_id = int(d["id"])
            score = infl.get(sf_id, {}).get(d_id, {}).get("score")
            scores.append((d["name"], score))
        lines.append("- influence_scores: " + ", ".join([f"{name}={score}" for name, score in scores]))
        lines.append("")

        mkts = top_markets_by_family.get(sf_id, [])
        if not mkts:
            lines.append("_No matches._")
            lines.append("")
            continue

        for m in mkts:
            lines.append(f"### {m['question']}")
            lines.append(f"- `pm_market_id`: {m['pm_market_id']}")
            if m.get("probability") is not None:
                lines.append(f"- probability: {m['probability']}")
            if m.get("volume") is not None:
                lines.append(f"- volume: {m['volume']}")
            lines.append(f"- match_score: {m.get('match_score')}")
            mt = m.get("matched_terms") or []
            lines.append(f"- matched_terms: {json.dumps(mt, ensure_ascii=False)}")
            lines.append("")

    return "\n".join(lines)


_MONTHS = (
    "january|february|march|april|may|june|july|august|september|october|november|december|"
    "jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec"
)


def _dedupe_key(question: str) -> str:
    """Best-effort key for clustering near-duplicate markets.

    Role:
    - Collapse templated markets that differ only by date/threshold/direction
      (e.g., central bank decision ladders).
    """
    q = _norm(question)
    # Drop dates/months/years and numeric thresholds.
    q = re.sub(rf"\b({_MONTHS})\b", " ", q)
    q = re.sub(r"\b20\d{2}\b", " ", q)  # years
    q = re.sub(r"\b\d+(\.\d+)?\b", " ", q)  # numbers
    q = q.replace("bps", " ")

    # Drop common direction/ladder words to cluster outcomes for the same event.
    q = re.sub(
        r"\b(increase|increases|decrease|decreases|no change|make no change|cut|cuts|hike|hikes|raise|raises|lower|lowers)\b",
        " ",
        q,
    )
    q = re.sub(r"[^a-z\s]+", " ", q)
    q = re.sub(r"\s+", " ", q).strip()

    # Remove high-frequency glue words to reduce template variance.
    stop = {
        "will",
        "the",
        "a",
        "an",
        "in",
        "on",
        "at",
        "by",
        "of",
        "to",
        "for",
        "after",
        "before",
        "between",
        "and",
        "or",
        "be",
        "is",
        "are",
        "s",
        "v",
        "vs",
        "meeting",
        "decision",
        "option",
        "uses",
        "use",
    }
    toks = [t for t in q.split() if t and t not in stop]
    q2 = " ".join(toks).strip()
    return q2[:200] if q2 else q[:200]


def _heuristic_rank_score(*, match_score: float, volume_usd: float | None) -> float:
    """Cheap 0..1 relevance proxy for ordering candidates passed to the LLM."""
    ms = max(0.0, min(1.0, float(match_score)))
    vol = float(volume_usd) if volume_usd is not None else 0.0
    # Log scale to keep 10k..10M in a usable range; cap at 1.0.
    vol_factor = math.log1p(max(0.0, vol)) / math.log1p(1_000_000.0)
    vol_factor = max(0.0, min(1.0, float(vol_factor)))
    return float(ms * (0.25 + 0.75 * vol_factor))


def _strip_raw(llm_report: dict[str, Any]) -> dict[str, Any]:
    """Avoid returning massive raw responses in notebooks by default."""
    out = dict(llm_report)
    out.pop("_raw", None)
    return out


def run_signal_family_mvp(
    *,
    db_url: str | None = None,
    markets_limit: int = 5000,
    top_n_per_family: int = 10,
    out_dir: str = "reports",
    use_llm: bool = False,
    llm_candidates_per_family: int = 20,
    llm_top_k_per_family: int = 5,
    hard_filter_version: str | None = None,
    matcher_version: str | None = None,
    method: str = "rule_classification",
    min_strength: float = 0.70,
) -> dict[str, Any]:
    """Render a signal-family report from existing Step-3 matcher outputs.

    Note: `markets_limit` is kept for backwards compatibility with older notebooks,
    but Step 3 matching is precomputed and read from the DB, so this parameter is
    no longer used to bound the universe.
    """
    load_env()
    db_url = (db_url or get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise RuntimeError("DATABASE_URL is required")
    db_url = db_url.replace("postgresql+psycopg://", "postgresql://")

    if hard_filter_version is None:
        hard_filter_version = load_hard_filter_rules().filter_version
    if matcher_version is None:
        matcher_version = (get_env("MATCHER_VERSION") or "").strip() or "matcher_v1"

    signal_families = fetch_signal_families(db_url, active_only=True)
    if not signal_families:
        raise RuntimeError("No signal families found; run migrations (signal_family).")

    macro_domains = fetch_macro_domains(db_url)
    influence = fetch_signal_family_domain_influence(db_url)

    # Build report payload from DB (so what you see matches persisted state)
    top_by_family: dict[int, list[dict[str, Any]]] = {}
    any_matches = False
    for sf in signal_families:
        top_by_family[sf.id] = fetch_top_markets_for_signal_family(
            db_url,
            signal_family_id=sf.id,
            matcher_version=str(matcher_version),
            method=str(method),
            min_strength=float(min_strength),
            top_n=top_n_per_family,
        )
        if top_by_family[sf.id]:
            any_matches = True
    if not any_matches:
        raise RuntimeError(
            f"No matches found for matcher_version={matcher_version!r} method={method!r}. "
            "Run `./venv/bin/python scripts/run_family_matching.py` first."
        )

    as_of = datetime.now(timezone.utc)
    llm_report: dict[str, Any] | None = None
    if use_llm:
        # Prepare compact authority context
        infl_by_family: dict[int, dict[str, int]] = {}
        infl_lookup: dict[int, dict[int, int]] = {}
        for r in influence:
            infl_lookup.setdefault(int(r.signal_family_id), {})[int(r.macro_domain_id)] = int(r.score)
        domain_name_by_id = {int(d.id): str(d.name) for d in macro_domains}
        for sf in signal_families:
            scores = {
                domain_name_by_id[d_id]: int(score)
                for d_id, score in (infl_lookup.get(int(sf.id), {}) or {}).items()
                if d_id in domain_name_by_id
            }
            infl_by_family[int(sf.id)] = scores

        # Candidate markets: fetch more per family to let the LLM dedupe/select.
        candidate_markets: list[dict[str, Any]] = []
        clusters: list[dict[str, Any]] = []

        for sf in signal_families:
            rows = fetch_top_markets_for_signal_family(
                db_url,
                signal_family_id=sf.id,
                matcher_version=str(matcher_version),
                method=str(method),
                min_strength=0.0,
                top_n=int(llm_candidates_per_family),
            )
            # Cluster within family
            by_key: dict[str, list[dict[str, Any]]] = {}
            for r in rows:
                key = _dedupe_key(str(r.get("question") or ""))
                by_key.setdefault(key, []).append(r)

            for key, members in by_key.items():
                # Choose representative by heuristic rank score (uses match_score + volume)
                for m in members:
                    m["_heuristic_rank_score"] = _heuristic_rank_score(
                        match_score=float(m.get("match_score") or 0.0),
                        volume_usd=m.get("volume"),
                    )

                members_sorted = sorted(
                    members,
                    key=lambda x: (float(x.get("_heuristic_rank_score") or 0.0), float(x.get("volume") or 0.0)),
                    reverse=True,
                )
                rep = members_sorted[0]
                digest = hashlib.sha1(f"{sf.slug}:{key}".encode("utf-8")).hexdigest()[:12]
                cluster_id = f"{sf.slug}:{digest}"

                member_ids = [int(x["pm_market_id"]) for x in members_sorted]
                clusters.append(
                    {
                        "cluster_id": cluster_id,
                        "signal_family_slug": sf.slug,
                        "dedupe_key": key,
                        "representative_pm_market_id": int(rep["pm_market_id"]),
                        "member_market_ids": member_ids,
                    }
                )

                # Only send the representative market to the LLM; provide the full
                # cluster membership separately for explainable redundancy removal.
                candidate_markets.append(
                    {
                        "pm_market_id": int(rep["pm_market_id"]),
                        "question": rep.get("question"),
                        "category": rep.get("category"),
                        "probability": rep.get("probability"),
                        "volume_usd": rep.get("volume"),
                        "signal_family_slug": sf.slug,
                        "match_method": str(method),
                        "match_score": float(rep.get("match_score") or 0.0),
                        "matched_terms": rep.get("matched_terms") or [],
                        "heuristic_rank_score": float(rep.get("_heuristic_rank_score") or 0.0),
                        "cluster_id": cluster_id,
                        "cluster_size": len(member_ids),
                        "redundant_market_ids": member_ids[1:],
                    }
                )

        input_json = {
            "as_of_utc": as_of.isoformat(),
            "TOP_K": int(llm_top_k_per_family),
            "signal_families": [
                {
                    "slug": sf.slug,
                    "title": sf.title,
                    "description": sf.description,
                    "influence_scores": infl_by_family.get(int(sf.id), {}),
                }
                for sf in signal_families
            ],
            "candidate_markets": candidate_markets,
            "clusters": clusters,
        }

        llm_report = generate_signal_family_report_with_gemini(input_json=input_json)
        report_md = render_signal_family_llm_report_markdown(as_of=as_of, llm_report=llm_report)
    else:
        report_md = render_signal_family_report_markdown(
            as_of=as_of,
            signal_families=[asdict(s) for s in signal_families],
            macro_domains=[asdict(d) for d in macro_domains],
            influence_rows=[asdict(i) for i in influence],
            top_markets_by_family=top_by_family,
        )

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    fname = f"signal_family_report_{as_of.strftime('%Y%m%d_%H%M%S')}.md"
    report_path = out_path / fname
    report_path.write_text(report_md, encoding="utf-8")

    counts_by_family = {sf.slug: len(top_by_family.get(sf.id, [])) for sf in signal_families}

    return {
        "report_path": str(report_path),
        "counts_by_family": counts_by_family,
        "hard_filter_version": hard_filter_version,
        "matcher_version": matcher_version,
        "method": method,
        "llm_report": _strip_raw(llm_report) if llm_report else None,
    }
