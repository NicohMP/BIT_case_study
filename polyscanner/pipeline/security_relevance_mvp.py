"""Security-focused relevance pipeline (MVP).

Goal:
- Given a single BIT security, rank Polymarket markets by deterministic relevance using:
  - pm_market -> signal_family matches (keyword matcher)
  - signal_family -> macro_domain influence matrix (0..5)
  - security -> macro_domain exposure weights (sum=1.0)

Then:
- Pass the top candidates to Gemini to produce a readable report grouped by signal family.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from polyscanner.db.pg import (
    delete_pm_market_signal_family_matches,
    fetch_macro_domains,
    fetch_pm_markets_for_scoring,
    fetch_security,
    fetch_security_by_ticker,
    fetch_security_macro_domain_exposures,
    fetch_signal_families,
    fetch_signal_family_domain_influence,
    fetch_top_family_matches_per_market,
    upsert_pm_market_signal_family_matches,
)
from polyscanner.env import get_env, load_env
from polyscanner.ingestion.pm_markets import ingest_markets_from_tag_ids
from polyscanner.llm.security_signal_report import generate_security_signal_report_with_gemini
from polyscanner.reporting.signal_family_markdown import render_signal_family_llm_report_markdown
from polyscanner.relevance.signal_family_score import (
    DomainExposure,
    FamilyMatch,
    InfluenceCell,
    score_markets_for_security,
)
from polyscanner.signal_family_rules import RULES_BY_SLUG
from polyscanner.pipeline.signal_family_mvp import match_market_to_rule


def _dedupe_group(question: str) -> str:
    # Keep identical to the clustering intent: normalize and hash to a stable id.
    q = (question or "").strip().lower()
    q = " ".join(q.split())
    return q[:200]


def _cluster_id(*, family_slug: str, group: str) -> str:
    digest = hashlib.sha1(f"{family_slug}:{group}".encode("utf-8")).hexdigest()[:12]
    return f"{family_slug}:{digest}"


def _write_report(*, out_dir: str, as_of: datetime, md: str, ticker: str) -> str:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    fname = f"security_signal_report_{ticker}_{as_of.strftime('%Y%m%d_%H%M%S')}.md"
    p = out_path / fname
    p.write_text(md, encoding="utf-8")
    return str(p)


def run_security_relevance_mvp(
    *,
    security_id: int | None = None,
    ticker: str | None = None,
    exchange_mic: str | None = None,
    db_url: str | None = None,
    tag_ids: list[int] | None = None,
    ingest_from_tags: bool = True,
    tag_markets_cap_per_tag: int = 60,
    markets_limit: int = 3000,
    min_volume_usd: float | None = None,
    match_min_score: float = 0.0,
    top_k_families_per_market: int = 2,
    top_n_markets_total: int = 80,
    top_k_per_family_for_llm: int = 5,
    out_dir: str = "reports",
    use_llm: bool = True,
) -> dict[str, Any]:
    """Run the deterministic relevance engine for a single security and write a report."""
    load_env()
    db_url = (db_url or get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise RuntimeError("DATABASE_URL is required")
    db_url = db_url.replace("postgresql+psycopg://", "postgresql://")

    if security_id is None:
        if not ticker:
            raise ValueError("Provide security_id or ticker")
        sec = fetch_security_by_ticker(db_url, ticker=ticker, exchange_mic=exchange_mic)
        if not sec:
            raise RuntimeError(f"Unknown security ticker={ticker!r}")
        security_id = int(sec["id"])
    else:
        sec = fetch_security(db_url, security_id=int(security_id))
        if not sec:
            raise RuntimeError(f"Unknown security_id={security_id}")

    # Optional: ingest more relevant markets using curated tags first.
    ingestion_summary: dict[str, Any] | None = None
    if tag_ids and ingest_from_tags:
        base_url = (get_env("POLYMARKET_API_BASE_URL") or "https://gamma-api.polymarket.com").strip()
        ingestion_summary = ingest_markets_from_tag_ids(
            db_url=db_url,
            base_url=base_url,
            tag_ids=[int(x) for x in tag_ids],
            markets_cap_per_tag=int(tag_markets_cap_per_tag),
        )

    # Load authority layer
    signal_families = fetch_signal_families(db_url, active_only=True)
    macro_domains = fetch_macro_domains(db_url)
    influence_rows = fetch_signal_family_domain_influence(db_url)

    exposures_rows = fetch_security_macro_domain_exposures(db_url, security_id=int(security_id))
    if not exposures_rows:
        raise RuntimeError(
            "No security exposures found in bit_security_macro_domain_exposure for this security. "
            "Seed or insert exposure weights first."
        )

    domain_exposures = [
        DomainExposure(
            macro_domain_id=int(r["macro_domain_id"]),
            macro_domain_name=str(r["macro_domain_name"]),
            weight=float(r["weight"]),
        )
        for r in exposures_rows
    ]

    influence_cells = [
        InfluenceCell(
            signal_family_id=int(r.signal_family_id),
            macro_domain_id=int(r.macro_domain_id),
            score=int(r.score),
        )
        for r in influence_rows
    ]

    # Market universe (volume-ordered for scoring)
    markets = fetch_pm_markets_for_scoring(db_url, limit=int(markets_limit), min_volume_usd=min_volume_usd)
    if not markets:
        raise RuntimeError("No pm_market rows found; run ingestion first.")

    # Recompute keyword matches with current rules (clear stale rows first).
    deleted = delete_pm_market_signal_family_matches(
        db_url,
        signal_family_ids=[int(sf.id) for sf in signal_families],
        match_method="keyword",
    )

    match_rows: list[dict[str, Any]] = []
    for m in markets:
        for sf in signal_families:
            rule = RULES_BY_SLUG.get(sf.slug)
            if rule is None:
                continue
            score, matched_terms = match_market_to_rule(question=m["question"], category=m.get("category"), rule=rule)
            if score <= 0.0:
                continue
            match_rows.append(
                {
                    "pm_market_id": int(m["pm_market_id"]),
                    "signal_family_id": int(sf.id),
                    "match_method": "keyword",
                    "match_score": float(score),
                    "matched_terms": json.dumps(matched_terms, ensure_ascii=False),
                    "match_rationale": "",
                }
            )
    upserted = upsert_pm_market_signal_family_matches(db_url, match_rows)

    # Fetch top-k family matches per market for scoring (prevents stacking).
    market_ids = [int(m["pm_market_id"]) for m in markets]
    top_matches_rows = fetch_top_family_matches_per_market(
        db_url,
        market_ids=market_ids,
        top_k=int(top_k_families_per_market),
        min_match_score=float(match_min_score),
    )

    matches_by_market_id: dict[int, list[FamilyMatch]] = {}
    for r in top_matches_rows:
        matches_by_market_id.setdefault(int(r["pm_market_id"]), []).append(
            FamilyMatch(
                signal_family_id=int(r["signal_family_id"]),
                signal_family_slug=str(r["signal_family_slug"]),
                match_score=float(r["match_score"]),
            )
        )

    scored = score_markets_for_security(
        markets=markets,
        security_id=int(security_id),
        matches_by_market_id=matches_by_market_id,
        domain_exposures=domain_exposures,
        influence_cells=influence_cells,
        top_k_families=int(top_k_families_per_market),
        use_volume_boost=True,
    )

    scored = scored[: max(1, int(top_n_markets_total))]

    as_of = datetime.now(timezone.utc)

    if not use_llm:
        # Minimal deterministic dump (no LLM): write JSON for inspection.
        md = "# Security relevance (deterministic)\n\n"
        md += f"- Generated at: `{as_of.isoformat()}`\n"
        md += f"- Security: `{sec['ticker']}` ({sec['company_name']})\n\n"
        md += "```json\n"
        md += json.dumps({"security": sec, "exposures": exposures_rows, "top_markets": scored}, ensure_ascii=False, indent=2)
        md += "\n```\n"
        report_path = _write_report(out_dir=out_dir, as_of=as_of, md=md, ticker=str(sec["ticker"]))
        return {
            "report_path": report_path,
            "security": sec,
            "ingestion_summary": ingestion_summary,
            "deleted_previous_matches": deleted,
            "upserted_matches": upserted,
            "top_scored_markets": scored,
        }

    # Prepare LLM input grouped by signal family with dedupe clusters.
    # Assign each scored market to its best family (highest match_score).
    family_title_by_slug = {sf.slug: sf.title for sf in signal_families}
    influence_by_slug: dict[str, dict[str, int]] = {}
    domain_name_by_id = {int(d.id): str(d.name) for d in macro_domains}
    infl_lookup: dict[int, dict[int, int]] = {}
    for r in influence_rows:
        infl_lookup.setdefault(int(r.signal_family_id), {})[int(r.macro_domain_id)] = int(r.score)
    for sf in signal_families:
        influence_by_slug[sf.slug] = {domain_name_by_id[k]: v for k, v in infl_lookup.get(int(sf.id), {}).items()}

    # Cluster within each family by a lightweight normalized key and keep one representative.
    clusters: list[dict[str, Any]] = []
    candidate_markets: list[dict[str, Any]] = []
    seen_cluster_rep: set[str] = set()

    for it in scored:
        pm_market_id = int(it["pm_market_id"])
        fams = matches_by_market_id.get(pm_market_id, [])
        if not fams:
            continue
        best = max(fams, key=lambda x: float(x.match_score))
        fam_slug = str(best.signal_family_slug)

        group = _dedupe_group(str(it.get("question") or ""))
        cid = _cluster_id(family_slug=fam_slug, group=group)

        # Build redundant list within this family cluster from the DB matches list (best-effort).
        # For MVP, we only know about the representative itself; redundancy is handled earlier in the family pipeline.
        redundant_ids: list[int] = []

        if cid not in seen_cluster_rep:
            seen_cluster_rep.add(cid)
            clusters.append(
                {
                    "cluster_id": cid,
                    "signal_family_slug": fam_slug,
                    "dedupe_key": group,
                    "representative_pm_market_id": pm_market_id,
                    "member_market_ids": [pm_market_id],
                }
            )

            contributions_top = []
            for b in (it.get("breakdown") or [])[:6]:
                if isinstance(b, dict):
                    contributions_top.append(b)

            candidate_markets.append(
                {
                    "pm_market_id": pm_market_id,
                    "question": it.get("question"),
                    "category": None,
                    "probability": it.get("probability"),
                    "volume_usd": it.get("volume_usd"),
                    "signal_family_slug": fam_slug,
                    "match_score": float(best.match_score),
                    "final_score": float(it.get("final_score") or 0.0),
                    "cluster_id": cid,
                    "dedupe_group": group,
                    "redundant_market_ids": redundant_ids,
                    "contributions_top": contributions_top,
                }
            )

    input_json = {
        "as_of_utc": as_of.isoformat(),
        "TOP_K": int(top_k_per_family_for_llm),
        "security": {
            "security_id": int(sec["id"]),
            "ticker": sec["ticker"],
            "company_name": sec["company_name"],
            "exchange_mic": sec["exchange_mic"],
        },
        "security_domain_exposures": exposures_rows,
        "signal_families": [
            {
                "slug": sf.slug,
                "title": sf.title,
                "description": sf.description,
                "influence_scores": influence_by_slug.get(sf.slug, {}),
            }
            for sf in signal_families
        ],
        "candidate_markets": candidate_markets,
        "clusters": clusters,
    }

    llm_report = generate_security_signal_report_with_gemini(input_json=input_json)
    md = render_signal_family_llm_report_markdown(as_of=as_of, llm_report=llm_report)
    report_path = _write_report(out_dir=out_dir, as_of=as_of, md=md, ticker=str(sec["ticker"]))

    llm_report_no_raw = dict(llm_report)
    llm_report_no_raw.pop("_raw", None)

    return {
        "report_path": report_path,
        "security": sec,
        "ingestion_summary": ingestion_summary,
        "deleted_previous_matches": deleted,
        "upserted_matches": upserted,
        "top_scored_markets": scored,
        "llm_report": llm_report_no_raw,
    }

