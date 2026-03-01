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
from datetime import datetime, timedelta, timezone
import math
from typing import Any

from polyscanner.db.pg import connect, fetch_macro_domains, fetch_signal_families, fetch_signal_family_domain_influence
from polyscanner.filtering.hard_filters import load_hard_filter_rules
from polyscanner.relevance.rate_like import is_rate_like
from polyscanner.sentiment.market_intensity_v1 import (
    SentimentIntensityParamsV1,
    delta_p_abs,
    sentiment_intensity_g_v1_practical,
    tau_days_from_end_date,
)

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


def _best_match_rows_sql(*, trusted_only: bool) -> str:
    """Return a subquery selecting one row per (market_id, signal_family_id).

    Precision-first default for Step 4 is trusted-only: score using only strict
    Step-3 classifications (method='rule_classification').

    Discovery rows are higher-recall and noisier; they remain useful for Step-3
    audits/diagnostics and candidate generation, but should not drive Step-4
    relevance unless explicitly enabled.
    """
    if trusted_only:
        return """
            select distinct on (x.market_id, x.signal_family_id)
              x.market_id,
              x.signal_family_id,
              x.method,
              x.match_strength
            from pm_market_signal_family_match x
            where x.matcher_version = %(matcher_version)s
              and x.method = 'rule_classification'
              and x.match_strength > 0.0
            order by
              x.market_id,
              x.signal_family_id,
              x.match_strength desc
        """

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
    trusted_only: bool,
) -> dict[int, list[dict[str, Any]]]:
    """Return best family matches per market, only for requested market_ids."""
    if not market_ids:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            f"""
            with best as (
              {_best_match_rows_sql(trusted_only=bool(trusted_only))}
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


def _table_exists(conn, *, table_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("select to_regclass(%s);", (f"public.{table_name}",))
        return cur.fetchone()[0] is not None


def persist_relevance_selection(
    *,
    db_url: str,
    scoring_version: str,
    filter_version: str | None = None,
    selection_version: str = "selected_v2",
    top_k: int = 20,
    max_per_event: int = 1,
    max_rate_like: int = 3,
    limit_securities: int | None = None,
    candidate_pool: int = 500,
    use_sentiment_g_v1: bool = True,
    sentiment_alpha: float = 0.30,
    sentiment_params: SentimentIntensityParamsV1 | None = None,
    include_movement_in_g: bool = False,
) -> dict[str, Any]:
    """Persist a diversified top-K selection per security (Step 4b).

    This reads from `pm_market_security_relevance` (raw scores) and writes a
    deterministic selection into `pm_market_security_relevance_selection`.
    """
    if filter_version is None:
        filter_version = load_hard_filter_rules().filter_version

    now = datetime.now(tz=timezone.utc)
    prev_snapshot_date = (now.date() - timedelta(days=1)).isoformat()
    sparams = sentiment_params or SentimentIntensityParamsV1()

    conn = connect(db_url)
    try:
        if not _table_exists(conn, table_name="pm_market_security_relevance_selection"):
            log.warning(
                "Selection table missing: pm_market_security_relevance_selection. "
                "Apply migration 20260225183500_add_pm_market_security_relevance_selection.sql."
            )
            return {"table_exists": False, "securities_selected": 0, "rows_upserted": 0}

        securities = _fetch_securities(conn)
        if limit_securities is not None:
            securities = securities[: max(0, int(limit_securities))]

        exposures = _fetch_security_exposures(conn)
        use_structural_any = bool(str(selection_version) != "selected_v1")

        market_mean_base_by_id: dict[int, float] = {}
        market_coverage_n_by_id: dict[int, int] = {}
        n_securities_total = 0
        if use_structural_any:
            n_securities_total = len(_fetch_securities(conn))
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select market_id, avg(base_score)::double precision as mean_base
                    from pm_market_security_relevance
                    where scoring_version = %s
                    group by market_id;
                    """,
                    (str(scoring_version),),
                )
                for mid, mean_base in cur.fetchall():
                    if mid is None:
                        continue
                    try:
                        market_mean_base_by_id[int(mid)] = float(mean_base or 0.0)
                    except Exception:
                        continue

            with conn.cursor() as cur:
                cur.execute(
                    """
                    select market_id, count(distinct security_id)::int as n
                    from pm_market_security_relevance
                    where scoring_version = %s
                    group by market_id;
                    """,
                    (str(scoring_version),),
                )
                for mid, n in cur.fetchall():
                    if mid is None:
                        continue
                    try:
                        market_coverage_n_by_id[int(mid)] = int(n or 0)
                    except Exception:
                        continue

        params = {
            "top_k": int(top_k),
            "max_per_event": int(max_per_event),
            "max_rate_like": int(max_rate_like),
            "candidate_pool": int(candidate_pool),
            "use_sentiment_g_v1": bool(use_sentiment_g_v1),
            "sentiment_alpha": float(sentiment_alpha),
            "sentiment_prev_snapshot_date": str(prev_snapshot_date),
            "sentiment_tau0_days": float(sparams.tau0_days),
            "sentiment_delta_p_half_life": float(sparams.delta_p_half_life),
            "sentiment_include_movement_in_g": bool(include_movement_in_g),
            # Selection behavior:
            # - selected_v1 keeps the original greedy selection (event + rate caps only).
            # - selected_v2 (or any other version string) prioritizes structural relevance (base_score)
            #   and dampens the quality multiplier so the top lists don't collapse into the same
            #   handful of ultra-liquid macro markets for every stock.
            "domain_diversify": bool(str(selection_version) != "selected_v1"),
            "selection_use_structural_base_score": bool(str(selection_version) != "selected_v1"),
            "selection_quality_beta": 0.50 if str(selection_version) != "selected_v1" else None,
            "selection_use_relative_relevance": bool(str(selection_version) != "selected_v1"),
            "selection_relative_clip": [0.50, 2.00] if str(selection_version) != "selected_v1" else None,
            # New (selected_v2+): cap "global macro" markets that show up for almost every security.
            # This prevents the per-stock lists collapsing into the same handful of FOMC/politics
            # mega-markets, while still allowing a few of them through.
            "selection_max_high_coverage": 3 if str(selection_version) != "selected_v1" else None,
            "selection_high_coverage_ratio": 0.75 if str(selection_version) != "selected_v1" else None,
        }

        def _parse_score_breakdown_primary_domain_id(v: Any) -> int | None:
            try:
                if isinstance(v, str):
                    v = json.loads(v)
                if not isinstance(v, dict):
                    return None
                top = v.get("top_domains")
                if not isinstance(top, list) or not top:
                    return None
                first = top[0]
                if not isinstance(first, dict):
                    return None
                did = int(first.get("macro_domain_id") or 0)
                return did or None
            except Exception:
                return None

        def _domain_quotas_for_security(*, security_id: int, k: int, max_domains: int = 3) -> dict[int, int]:
            exp = exposures.get(int(security_id)) or {}
            items = [(int(d), float(w)) for d, w in exp.items() if float(w) > 0.0]
            items.sort(key=lambda t: (-t[1], t[0]))
            items = items[: max(0, int(max_domains))]
            if not items:
                return {}

            quotas: dict[int, int] = {}
            for did, w in items:
                quotas[did] = max(1, int(round(float(k) * float(w))))

            # If rounding overshoots K, reduce smallest quotas first (but keep >=1).
            while sum(quotas.values()) > int(k):
                did = min(quotas.keys(), key=lambda d: (quotas[d], d))
                if quotas[did] > 1:
                    quotas[did] -= 1
                else:
                    break
            return quotas

        rows_out: list[dict[str, Any]] = []
        sec_ids = [int(s["id"]) for s in securities]

        vol95_kept = _fetch_volume_p95_kept(conn, filter_version=str(filter_version)) or 1_000_000.0

        for s in securities:
            sid = int(s["id"])
            use_structural = bool(params.get("selection_use_structural_base_score"))
            order_col = "r.base_score" if use_structural else "r.final_score"
            max_high_cov = int(params.get("selection_max_high_coverage") or 0) if use_structural else 0
            cov_ratio = float(params.get("selection_high_coverage_ratio") or 0.0) if use_structural else 0.0
            cov_threshold = 0
            if use_structural and n_securities_total > 0 and cov_ratio > 0.0:
                cov_threshold = int(math.ceil(float(cov_ratio) * float(n_securities_total)))
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    select
                      r.base_score,
                      r.quality_multiplier,
                      r.final_score,
                      r.market_id,
                      r.score_breakdown,
                      m.event_id,
                      m.question,
                      m.volume_usd,
                      m.end_date,
                      m.probability
                    from pm_market_security_relevance r
                    join pm_market m on m.pm_market_id = r.market_id
                    where r.security_id = %s
                      and r.scoring_version = %s
                      and (m.end_date is null or m.end_date >= %s)
                    order by {order_col} desc
                    limit %s;
                    """,
                    (sid, str(scoring_version), now, int(candidate_pool)),
                )
                candidates = cur.fetchall()

            cand_ids = [int(mid) for _base, _qmult, _final, mid, _breakdown, _event_id, _question, _vol, _end_date, _prob in candidates]
            prev_probs = _fetch_daily_snapshot_probabilities(conn, market_ids=cand_ids, snapshot_date_iso=str(prev_snapshot_date))

            scored: list[dict[str, Any]] = []
            for base_score, qmult, relevance_final, mid, breakdown, event_id, question, volume_usd, end_date, probability in candidates:
                q = str(question or "")
                primary_domain_id = _parse_score_breakdown_primary_domain_id(breakdown)
                mean_base = market_mean_base_by_id.get(int(mid), 0.0)
                rel = (float(base_score) / float(mean_base + 1e-9)) if use_structural else 1.0
                rel_clip_min, rel_clip_max = (0.50, 2.00)
                try:
                    clip = params.get("selection_relative_clip") or [0.50, 2.00]
                    rel_clip_min, rel_clip_max = float(clip[0]), float(clip[1])
                except Exception:
                    pass
                rel_clipped = max(rel_clip_min, min(rel_clip_max, float(rel)))

                dp = None
                tau_days = None
                g = None
                g_components = None

                selection_score = float(base_score if use_structural else relevance_final)
                if use_sentiment_g_v1:
                    dp = delta_p_abs(
                        p_now=(float(probability) if probability is not None else None),
                        p_then=prev_probs.get(int(mid)),
                    )
                    tau_days = tau_days_from_end_date(
                        end_date_iso=(end_date.isoformat() if end_date is not None else None),
                        now=now,
                    )
                    g_full = sentiment_intensity_g_v1_practical(
                        volume_usd=(float(volume_usd) if volume_usd is not None else None),
                        vol95_usd=float(vol95_kept),
                        tau_days=tau_days,
                        delta_p=dp,
                        params=sparams,
                        include_movement=bool(include_movement_in_g),
                    )
                    g = float(g_full["g"])
                    g_components = g_full.get("components") if isinstance(g_full, dict) else None
                    g_with_movement = float(g_full.get("g_with_movement")) if isinstance(g_full, dict) and g_full.get("g_with_movement") is not None else None
                    a = float(max(0.0, min(1.0, float(sentiment_alpha))))
                    factor = float(a + (1.0 - a) * float(g))
                    if use_structural:
                        beta = float(params.get("selection_quality_beta") or 0.50)
                        qm = float(qmult or 1.0)
                        rr = rel_clipped if bool(params.get("selection_use_relative_relevance")) else 1.0
                        selection_score = float(base_score) * rr * (qm**beta) * factor
                    else:
                        selection_score = float(relevance_final) * factor
                else:
                    g_with_movement = None

                scored.append(
                    {
                        "selection_score": float(selection_score),
                        "relevance_base_score": float(base_score),
                        "relevance_quality_multiplier": float(qmult or 1.0),
                        "relevance_final_score": float(relevance_final),
                        "relative_relevance": float(rel_clipped),
                        "market_id": int(mid),
                        "event_id": int(event_id) if event_id is not None else None,
                        "question": q,
                        "is_rate_like": bool(is_rate_like(q)),
                        "primary_domain_id": primary_domain_id,
                        "sentiment_g_v1": g,
                        "sentiment_g_v1_with_movement": g_with_movement,
                        "sentiment_components": g_components,
                        "delta_p_abs": dp,
                        "tau_days": tau_days,
                    }
                )

            scored.sort(
                key=lambda x: (
                    -float(x.get("selection_score") or 0.0),
                    -float(x.get("relevance_final_score") or 0.0),
                    int(x.get("market_id") or 0),
                )
            )

            picked: list[dict[str, Any]] = []
            event_counts: dict[int, int] = {}
            rate_n = 0
            domain_counts: dict[int, int] = {}
            picked_market_ids: set[int] = set()
            high_cov_picked = 0

            def _can_pick(c: dict[str, Any]) -> bool:
                nonlocal high_cov_picked
                event_id = c.get("event_id")
                eid = int(event_id) if event_id is not None else -1
                rate_like = bool(c.get("is_rate_like"))
                if eid != -1 and event_counts.get(eid, 0) >= int(max_per_event):
                    return False
                if rate_like and rate_n >= int(max_rate_like):
                    return False
                if use_structural and max_high_cov > 0 and cov_threshold > 0:
                    mid = int(c.get("market_id") or 0)
                    cov_n = int(market_coverage_n_by_id.get(mid, 0))
                    if cov_n >= int(cov_threshold) and high_cov_picked >= int(max_high_cov):
                        return False
                return True

            def _can_pick_relaxed(c: dict[str, Any]) -> bool:
                event_id = c.get("event_id")
                eid = int(event_id) if event_id is not None else -1
                rate_like = bool(c.get("is_rate_like"))
                if eid != -1 and event_counts.get(eid, 0) >= int(max_per_event):
                    return False
                if rate_like and rate_n >= int(max_rate_like):
                    return False
                return True

            # Domain-aware first pass (selected_v2+): try to allocate some picks to the
            # security's top exposure domains, based on the market's primary domain contribution.
            if bool(params.get("domain_diversify")):
                quotas = _domain_quotas_for_security(security_id=sid, k=int(top_k))
                by_domain: dict[int, list[dict[str, Any]]] = {}
                for c in scored:
                    did = c.get("primary_domain_id")
                    if did is None:
                        continue
                    by_domain.setdefault(int(did), []).append(c)

                for did in list(by_domain.keys()):
                    by_domain[did].sort(
                        key=lambda x: (
                            -float(x.get("selection_score") or 0.0),
                            -float(x.get("relevance_final_score") or 0.0),
                            int(x.get("market_id") or 0),
                        )
                    )

                for did, quota in quotas.items():
                    want = int(quota)
                    if want <= 0:
                        continue
                    for c in by_domain.get(int(did), []):
                        if len(picked) >= int(top_k):
                            break
                        mid = int(c["market_id"])
                        if mid in picked_market_ids:
                            continue
                        if not _can_pick(c):
                            continue
                        picked.append(c)
                        picked_market_ids.add(mid)
                        event_id = c.get("event_id")
                        eid = int(event_id) if event_id is not None else -1
                        if eid != -1:
                            event_counts[eid] = event_counts.get(eid, 0) + 1
                        if bool(c.get("is_rate_like")):
                            rate_n += 1
                        if use_structural and max_high_cov > 0 and cov_threshold > 0:
                            cov_n = int(market_coverage_n_by_id.get(int(mid), 0))
                            if cov_n >= int(cov_threshold):
                                high_cov_picked += 1
                        domain_counts[int(did)] = domain_counts.get(int(did), 0) + 1
                        if domain_counts[int(did)] >= want:
                            break

            # Fill remaining slots greedily by score (v1 behavior).
            for c in scored:
                if len(picked) >= int(top_k):
                    break
                mid = int(c["market_id"])
                if mid in picked_market_ids:
                    continue
                if not _can_pick(c):
                    continue
                picked.append(c)
                picked_market_ids.add(mid)
                event_id = c.get("event_id")
                eid = int(event_id) if event_id is not None else -1
                if eid != -1:
                    event_counts[eid] = event_counts.get(eid, 0) + 1
                if bool(c.get("is_rate_like")):
                    rate_n += 1
                if use_structural and max_high_cov > 0 and cov_threshold > 0:
                    cov_n = int(market_coverage_n_by_id.get(int(mid), 0))
                    if cov_n >= int(cov_threshold):
                        high_cov_picked += 1
                did = c.get("primary_domain_id")
                if did is not None:
                    domain_counts[int(did)] = domain_counts.get(int(did), 0) + 1

            # Safety valve: if the market universe is extremely "global", the high-coverage cap
            # can prevent filling top_k. In that case, relax the cap but keep event/rate limits.
            if use_structural and len(picked) < int(top_k):
                for c in scored:
                    if len(picked) >= int(top_k):
                        break
                    mid = int(c["market_id"])
                    if mid in picked_market_ids:
                        continue
                    if not _can_pick_relaxed(c):
                        continue
                    picked.append(c)
                    picked_market_ids.add(mid)
                    event_id = c.get("event_id")
                    eid = int(event_id) if event_id is not None else -1
                    if eid != -1:
                        event_counts[eid] = event_counts.get(eid, 0) + 1
                    if bool(c.get("is_rate_like")):
                        rate_n += 1
                    did = c.get("primary_domain_id")
                    if did is not None:
                        domain_counts[int(did)] = domain_counts.get(int(did), 0) + 1

            for i, c in enumerate(picked, start=1):
                mid = int(c["market_id"])
                event_id = c.get("event_id")
                q = str(c.get("question") or "")
                rows_out.append(
                    {
                        "security_id": sid,
                        "market_id": int(mid),
                        "scoring_version": str(scoring_version),
                        "selection_version": str(selection_version),
                        "rank": int(i),
                        "final_score": float(c.get("selection_score") or 0.0),
                        "event_id": int(event_id) if event_id is not None else None,
                        "is_rate_like": bool(is_rate_like(q)),
                        "selection_params": json.dumps(params, ensure_ascii=False),
                        "selection_reason": json.dumps(
                            {
                                "event_counts": event_counts,
                                "rate_like_picked": int(rate_n),
                                "primary_domain_id": c.get("primary_domain_id"),
                                "primary_domain_counts": domain_counts,
                                "relevance_base_score": float(c.get("relevance_base_score") or 0.0),
                                "relevance_quality_multiplier": float(c.get("relevance_quality_multiplier") or 1.0),
                                "relevance_final_score": float(c.get("relevance_final_score") or 0.0),
                                "relative_relevance": float(c.get("relative_relevance") or 1.0),
                                "market_coverage_n": int(market_coverage_n_by_id.get(int(mid), 0)),
                                "high_coverage_threshold_n": int(cov_threshold) if use_structural else None,
                                "high_coverage_picked": int(high_cov_picked) if use_structural else None,
                                "selection_score": float(c.get("selection_score") or 0.0),
                                "sentiment_g_v1": c.get("sentiment_g_v1"),
                                "sentiment_g_v1_with_movement": c.get("sentiment_g_v1_with_movement"),
                                "sentiment_components": c.get("sentiment_components"),
                                "delta_p_abs": c.get("delta_p_abs"),
                                "tau_days": c.get("tau_days"),
                                "prev_snapshot_date": str(prev_snapshot_date),
                                "vol95_kept_usd": float(vol95_kept),
                            },
                            ensure_ascii=False,
                        ),
                    }
                )

        # Replace selections for this (scoring_version, selection_version) and these securities.
        with conn.cursor() as cur:
            cur.execute(
                """
                delete from pm_market_security_relevance_selection
                where security_id = any(%s)
                  and scoring_version = %s
                  and selection_version = %s;
                """,
                (sec_ids, str(scoring_version), str(selection_version)),
            )
            cur.executemany(
                """
                insert into pm_market_security_relevance_selection (
                  security_id,
                  market_id,
                  scoring_version,
                  selection_version,
                  rank,
                  final_score,
                  event_id,
                  is_rate_like,
                  selection_params,
                  selection_reason,
                  created_at,
                  updated_at
                ) values (
                  %(security_id)s,
                  %(market_id)s,
                  %(scoring_version)s,
                  %(selection_version)s,
                  %(rank)s,
                  %(final_score)s,
                  %(event_id)s,
                  %(is_rate_like)s,
                  %(selection_params)s::jsonb,
                  %(selection_reason)s::jsonb,
                  now(),
                  now()
                )
                on conflict (security_id, market_id, scoring_version, selection_version) do update set
                  rank = excluded.rank,
                  final_score = excluded.final_score,
                  event_id = excluded.event_id,
                  is_rate_like = excluded.is_rate_like,
                  selection_params = excluded.selection_params,
                  selection_reason = excluded.selection_reason,
                  updated_at = now();
                """,
                rows_out,
            )
        conn.commit()
        return {
            "table_exists": True,
            "securities_selected": int(len(securities)),
            "rows_upserted": int(len(rows_out)),
        }
    finally:
        conn.close()


def _fetch_volume_p95_kept(conn, *, filter_version: str) -> float:
    with conn.cursor() as cur:
        cur.execute(
            """
            select percentile_cont(0.95) within group (order by m.volume_usd)
            from pm_market m
            join pm_market_filter_decision d
              on d.market_id = m.pm_market_id
             and d.filter_version = %s
            where d.is_rejected = false
              and m.volume_usd is not null
              and m.volume_usd > 0;
            """,
            (str(filter_version),),
        )
        row = cur.fetchone()
    try:
        return float(row[0] or 0.0)
    except Exception:
        return 0.0


def _fetch_daily_snapshot_probabilities(
    conn,
    *,
    market_ids: list[int],
    snapshot_date_iso: str,
) -> dict[int, float]:
    if not market_ids:
        return {}
    if not _table_exists(conn, table_name="pm_market_daily_snapshot"):
        return {}
    with conn.cursor() as cur:
        cur.execute(
            """
            select market_id, probability
            from pm_market_daily_snapshot
            where snapshot_date = %s
              and market_id = any(%s);
            """,
            (str(snapshot_date_iso), market_ids),
        )
        rows = cur.fetchall()
    out: dict[int, float] = {}
    for mid, prob in rows:
        if mid is None or prob is None:
            continue
        try:
            out[int(mid)] = float(prob)
        except Exception:
            continue
    return out


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
    trusted_only: bool = False,
) -> RelevanceRunResult:
    """Compute and persist Step 4 relevance scores for all (security, market) pairs.

    This function only scores markets that are:
    - active via pm_event (active=true AND closed=false)
    - kept by hard filters for the given filter_version

    By default, Step 4 uses both strict matches and discovery matches from Step 3,
    but discovery matches are discounted to preserve precision.
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
            conn,
            matcher_version=str(matcher_version),
            market_ids=market_ids,
            trusted_only=bool(trusted_only),
        )
        discovery_match_discount = 0.50

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
                    method = str(mm.get("method") or "")
                    if not bool(trusted_only) and method and method != "rule_classification":
                        wmatch *= float(discovery_match_discount)
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
                            "method": method,
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
