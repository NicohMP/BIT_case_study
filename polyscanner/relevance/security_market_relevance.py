"""Step 4: deterministic relevance scoring for markets per BIT security.

Score definition:
base_score(S, M) = Σ_F w_match(M, F) * Σ_D w_infl(F, D) * w_exp(S, D)
final_score(S, M) = base_score(S, M) * q(M)

Where:
- w_match(M,F) is selected from `pm_market_signal_family_match` for a given matcher_version,
  preferring `method='rule_classification'` when present, else falling back to the strongest
  discovery match for that (market, family) pair.
- w_infl(F,D) is `signal_family_domain_influence.score / 5.0`.
- w_exp(S,D) is `bit_security_macro_domain_exposure.weight` (already normalized to sum to 1).
- q(M) is `pm_market_filter_decision.quality_score` (0..1), defaulting to 1.0 if missing.

All outputs are persisted to `pm_market_security_relevance` with `scoring_version` so runs are
auditable and idempotent.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from polyscanner.db.pg import connect, fetch_macro_domains, fetch_signal_families, fetch_signal_family_domain_influence
from polyscanner.filtering.hard_filters import load_hard_filter_rules

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RelevanceRunResult:
    scoring_version: str
    filter_version: str
    matcher_version: str
    securities_scored: int
    markets_considered: int
    rows_upserted: int
    runtime_s: float


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def _as_float(x: Any, default: float | None = None) -> float | None:
    if x is None:
        return default
    try:
        return float(x)
    except Exception:
        return default


def _best_match_rows_sql() -> str:
    # Select best match per (market_id, signal_family_id) with method preference:
    # rule_classification > discovery_* (highest match_strength).
    return """
        select distinct on (x.market_id, x.signal_family_id)
          x.market_id,
          x.signal_family_id,
          x.method,
          x.match_strength
        from pm_market_signal_family_match x
        where x.matcher_version = %(matcher_version)s
          and x.match_strength > 0.0
        order by
          x.market_id,
          x.signal_family_id,
          case when x.method = 'rule_classification' then 0 else 1 end,
          x.match_strength desc
    """


def _fetch_securities(conn) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(
            """
            select id, company_name, ticker, exchange_mic
            from bit_security
            order by company_name, exchange_mic, ticker;
            """
        )
        rows = cur.fetchall()
    return [{"id": int(r[0]), "company_name": str(r[1]), "ticker": str(r[2]), "exchange_mic": str(r[3])} for r in rows]


def _fetch_security_exposures(conn) -> dict[int, dict[int, float]]:
    """Return exposure weights by (security_id -> macro_domain_id -> weight)."""
    with conn.cursor() as cur:
        cur.execute(
            """
            select security_id, macro_domain_id, weight
            from bit_security_macro_domain_exposure
            order by security_id, macro_domain_id;
            """
        )
        rows = cur.fetchall()
    out: dict[int, dict[int, float]] = {}
    for sid, did, w in rows:
        out.setdefault(int(sid), {})[int(did)] = float(w)
    return out


def _fetch_kept_markets_quality(
    conn,
    *,
    filter_version: str,
    limit_markets: int | None,
) -> dict[int, dict[str, Any]]:
    """Return kept markets with quality multiplier and minimal metadata for audits."""
    params: dict[str, Any] = {"filter_version": str(filter_version)}
    limit_sql = ""
    if limit_markets is not None:
        params["limit_markets"] = int(limit_markets)
        limit_sql = " limit %(limit_markets)s"

    with conn.cursor() as cur:
        cur.execute(
            f"""
            select
              m.pm_market_id,
              m.event_id,
              m.question,
              m.volume_usd,
              m.liquidity_usd,
              coalesce(d.quality_score, 1.0) as quality_multiplier
            from pm_market m
            join pm_event e on e.event_id = m.event_id
            join pm_market_filter_decision d
              on d.market_id = m.pm_market_id
             and d.filter_version = %(filter_version)s
             and d.is_rejected = false
            where e.active = true and e.closed = false
            order by m.volume_usd desc nulls last, m.liquidity_usd desc nulls last, m.pm_market_id
            {limit_sql};
            """,
            params,
        )
        rows = cur.fetchall()
    out: dict[int, dict[str, Any]] = {}
    for r in rows:
        mid = int(r[0])
        out[mid] = {
            "market_id": mid,
            "event_id": int(r[1]) if r[1] is not None else None,
            "question": str(r[2] or ""),
            "volume_usd": _as_float(r[3]),
            "liquidity_usd": _as_float(r[4]),
            "quality_multiplier": float(r[5]) if r[5] is not None else 1.0,
        }
    return out


def _fetch_best_market_family_matches(
    conn,
    *,
    matcher_version: str,
    market_ids: list[int],
) -> dict[int, list[dict[str, Any]]]:
    """Return best family matches per market, only for requested market_ids."""
    if not market_ids:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            f"""
            with best as (
              {_best_match_rows_sql()}
            )
            select b.market_id, b.signal_family_id, b.method, b.match_strength
            from best b
            where b.market_id = any(%(market_ids)s)
            order by b.market_id, b.match_strength desc;
            """,
            {"matcher_version": str(matcher_version), "market_ids": market_ids},
        )
        rows = cur.fetchall()
    out: dict[int, list[dict[str, Any]]] = {}
    for mid, fid, method, strength in rows:
        out.setdefault(int(mid), []).append(
            {"signal_family_id": int(fid), "method": str(method), "match_strength": float(strength)}
        )
    return out


def _upsert_relevance_rows(conn, *, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    with conn.cursor() as cur:
        cur.executemany(
            """
            insert into pm_market_security_relevance (
              security_id,
              market_id,
              scoring_version,
              base_score,
              quality_multiplier,
              final_score,
              score_breakdown,
              created_at,
              updated_at
            ) values (
              %(security_id)s,
              %(market_id)s,
              %(scoring_version)s,
              %(base_score)s,
              %(quality_multiplier)s,
              %(final_score)s,
              %(score_breakdown)s::jsonb,
              now(),
              now()
            )
            on conflict (security_id, market_id, scoring_version) do update set
              base_score = excluded.base_score,
              quality_multiplier = excluded.quality_multiplier,
              final_score = excluded.final_score,
              score_breakdown = excluded.score_breakdown,
              updated_at = now();
            """,
            rows,
        )
    conn.commit()
    return len(rows)


def compute_market_security_relevance(
    *,
    db_url: str,
    matcher_version: str,
    scoring_version: str = "relevance_v1",
    filter_version: str | None = None,
    limit_markets: int | None = None,
    limit_securities: int | None = None,
    min_base_score: float = 0.0,
    top_families_in_breakdown: int = 8,
    include_domain_breakdown: bool = True,
) -> RelevanceRunResult:
    """Compute and persist Step 4 relevance scores for all (security, market) pairs.

    This function only scores markets that are:
    - active via pm_event (active=true AND closed=false)
    - kept by hard filters for the given filter_version
    """
    if filter_version is None:
        filter_version = load_hard_filter_rules().filter_version

    started = datetime.now(tz=timezone.utc)

    conn = connect(db_url)
    try:
        securities = _fetch_securities(conn)
        if limit_securities is not None:
            securities = securities[: max(0, int(limit_securities))]

        exposures = _fetch_security_exposures(conn)

        # Use all families for slug lookup, even if some were later deactivated.
        families = fetch_signal_families(db_url, active_only=False)
        family_slug_by_id = {int(f.id): str(f.slug) for f in families}
        influences = fetch_signal_family_domain_influence(db_url)
        macro_domains = fetch_macro_domains(db_url)
        domain_name_by_id = {int(d.id): str(d.name) for d in macro_domains}

        infl_w: dict[int, dict[int, float]] = {}
        for row in influences:
            infl_w.setdefault(int(row.signal_family_id), {})[int(row.macro_domain_id)] = float(row.score) / 5.0

        kept_markets = _fetch_kept_markets_quality(conn, filter_version=str(filter_version), limit_markets=limit_markets)
        market_ids = list(kept_markets.keys())

        best_matches_by_market = _fetch_best_market_family_matches(
            conn, matcher_version=str(matcher_version), market_ids=market_ids
        )

        # Precompute per-security per-family effect: Σ_D w_infl(F,D) * w_exp(S,D)
        family_effect_by_security: dict[int, dict[int, float]] = {}
        for sec in securities:
            sid = int(sec["id"])
            exp = exposures.get(sid) or {}
            fe: dict[int, float] = {}
            for fid, per_dom in infl_w.items():
                total = 0.0
                for did, infl in per_dom.items():
                    wexp = exp.get(int(did), 0.0)
                    if wexp:
                        total += float(infl) * float(wexp)
                if total > 0.0:
                    fe[int(fid)] = float(total)
            family_effect_by_security[sid] = fe

        rows_to_upsert: list[dict[str, Any]] = []
        upserted_total = 0
        flush_n = 5000

        for sec in securities:
            sid = int(sec["id"])
            fe = family_effect_by_security.get(sid) or {}
            exp = exposures.get(sid) or {}

            for mid, m in kept_markets.items():
                matches = best_matches_by_market.get(int(mid)) or []
                if not matches:
                    continue

                base = 0.0
                fam_contribs: list[dict[str, Any]] = []
                dom_contribs: dict[int, float] = {}

                for mm in matches:
                    fid = int(mm["signal_family_id"])
                    wmatch = float(mm["match_strength"])
                    if wmatch <= 0.0:
                        continue
                    effect = float(fe.get(fid, 0.0))
                    if effect <= 0.0:
                        continue
                    contrib = wmatch * effect
                    base += contrib
                    fam_contribs.append(
                        {
                            "signal_family_id": fid,
                            "slug": family_slug_by_id.get(fid),
                            "method": mm.get("method"),
                            "match_strength": wmatch,
                            "family_effect": effect,
                            "contribution": contrib,
                        }
                    )

                    if include_domain_breakdown:
                        per_dom = infl_w.get(fid) or {}
                        for did, infl in per_dom.items():
                            wexp = float(exp.get(int(did), 0.0))
                            if wexp <= 0.0:
                                continue
                            dom_contribs[int(did)] = dom_contribs.get(int(did), 0.0) + (wmatch * infl * wexp)

                if base <= float(min_base_score):
                    continue

                q = float(m.get("quality_multiplier") or 1.0)
                final = base * q

                fam_contribs.sort(key=lambda x: float(x["contribution"]), reverse=True)
                fam_top = fam_contribs[: max(1, int(top_families_in_breakdown))]

                dom_top: list[dict[str, Any]] = []
                if include_domain_breakdown and dom_contribs:
                    items = sorted(dom_contribs.items(), key=lambda t: float(t[1]), reverse=True)
                    for did, c in items[:10]:
                        dom_top.append({"macro_domain_id": int(did), "name": domain_name_by_id.get(int(did)), "contribution": c})

                breakdown = {
                    "as_of_utc": _utcnow().isoformat(),
                    "security": {"security_id": sid, "company_name": sec["company_name"], "ticker": sec["ticker"]},
                    "market": {"market_id": int(mid), "event_id": m.get("event_id"), "question": m.get("question")},
                    "versions": {
                        "scoring_version": str(scoring_version),
                        "filter_version": str(filter_version),
                        "matcher_version": str(matcher_version),
                    },
                    "top_families": fam_top,
                    "top_domains": dom_top,
                }

                rows_to_upsert.append(
                    {
                        "security_id": sid,
                        "market_id": int(mid),
                        "scoring_version": str(scoring_version),
                        "base_score": float(base),
                        "quality_multiplier": float(q),
                        "final_score": float(final),
                        "score_breakdown": json.dumps(breakdown, ensure_ascii=False),
                    }
                )

                if len(rows_to_upsert) >= flush_n:
                    upserted_total += _upsert_relevance_rows(conn, rows=rows_to_upsert)
                    rows_to_upsert.clear()

        if rows_to_upsert:
            upserted_total += _upsert_relevance_rows(conn, rows=rows_to_upsert)
        runtime_s = (datetime.now(tz=timezone.utc) - started).total_seconds()
        return RelevanceRunResult(
            scoring_version=str(scoring_version),
            filter_version=str(filter_version),
            matcher_version=str(matcher_version),
            securities_scored=len(securities),
            markets_considered=len(kept_markets),
            rows_upserted=int(upserted_total),
            runtime_s=float(runtime_s),
        )
    finally:
        conn.close()
