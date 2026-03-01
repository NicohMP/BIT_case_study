from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from polyscanner.db.pg import connect


@dataclass(frozen=True)
class DbConfig:
    db_url: str


def fetch_one(conn, sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        if row is None:
            return None
        cols = [c.name for c in cur.description]  # type: ignore[union-attr]
    return {cols[i]: row[i] for i in range(len(cols))}


def fetch_all(conn, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
        cols = [c.name for c in cur.description]  # type: ignore[union-attr]
    return [{cols[i]: r[i] for i in range(len(cols))} for r in rows]


def latest_pipeline_run(*, db_url: str) -> dict[str, Any] | None:
    conn = connect(db_url)
    try:
        return fetch_one(conn, "select * from v_pm_latest_pipeline_run;")
    finally:
        conn.close()


def pipeline_counts(*, db_url: str) -> dict[str, int]:
    conn = connect(db_url)
    try:
        rows = fetch_all(
            conn,
            """
            select 'pm_event'::text as name, (select count(*) from pm_event)::int as n
            union all
            select 'pm_market'::text as name, (select count(*) from pm_market)::int as n
            union all
            select 'kept_latest'::text as name, (select count(*) from v_pm_market_kept_latest)::int as n
            union all
            select 'selected_latest'::text as name, (select count(*) from v_pm_security_market_relevance_selected_latest)::int as n
            union all
            select 'reports'::text as name, (select count(*) from pm_security_signal_report)::int as n
            ;
            """,
        )
        return {str(r["name"]): int(r["n"]) for r in rows}
    finally:
        conn.close()


def list_securities(*, db_url: str) -> list[dict[str, Any]]:
    conn = connect(db_url)
    try:
        return fetch_all(
            conn,
            """
            select id as security_id, ticker, company_name, exchange_mic
            from bit_security
            order by ticker;
            """,
        )
    finally:
        conn.close()


def list_macro_domains(*, db_url: str) -> list[dict[str, Any]]:
    conn = connect(db_url)
    try:
        return fetch_all(conn, "select id as macro_domain_id, name from macro_domain order by id;")
    finally:
        conn.close()


def security_exposures(*, db_url: str, security_id: int) -> list[dict[str, Any]]:
    conn = connect(db_url)
    try:
        return fetch_all(
            conn,
            """
            select
              e.macro_domain_id,
              d.name as macro_domain_name,
              e.weight,
              e.weight_basis,
              e.source_ref,
              e.as_of_date
            from bit_security_macro_domain_exposure e
            join macro_domain d on d.id = e.macro_domain_id
            where e.security_id = %s
            order by e.weight desc, d.id;
            """,
            (int(security_id),),
        )
    finally:
        conn.close()


def selected_markets_for_ticker(
    *,
    db_url: str,
    ticker: str,
    limit: int = 20,
) -> list[dict[str, Any]]:
    conn = connect(db_url)
    try:
        run = fetch_one(conn, "select * from v_pm_latest_pipeline_run;") or {}
        scoring_version = str(run.get("scoring_version") or "")
        selection_version = str(run.get("selection_version") or "")
        if not scoring_version:
            return []

        # Prefer selected_v2 if it exists for this scoring_version (even if the latest pipeline
        # run metadata still points at selected_v1). This avoids confusing UI behavior where
        # Step 4b improvements exist in the DB but aren't visible until a new run is recorded.
        effective_selection_version = selection_version
        if selection_version != "selected_v2":
            has_v2 = fetch_one(
                conn,
                """
                select 1 as ok
                from pm_market_security_relevance_selection
                where scoring_version = %s
                  and selection_version = 'selected_v2'
                limit 1;
                """,
                (scoring_version,),
            )
            if has_v2:
                effective_selection_version = "selected_v2"

        rows = fetch_all(
            conn,
            """
            select
              sel.security_id,
              s.ticker,
              s.company_name,
              sel.rank,
              sel.market_id,
              sel.event_id,
              sel.is_rate_like,
              sel.final_score as selection_score,
              sel.selection_reason,
              m.question,
              m.probability,
              m.end_date,
              m.volume_usd,
              m.liquidity_usd,
              e.title as event_title,
              r.base_score,
              r.quality_multiplier,
              r.final_score as relevance_final_score,
              r.score_breakdown
            from pm_market_security_relevance_selection sel
            join bit_security s on s.id = sel.security_id
            join pm_market m on m.pm_market_id = sel.market_id
            left join pm_event e on e.event_id = sel.event_id
            join pm_market_security_relevance r
              on r.security_id = sel.security_id
             and r.market_id = sel.market_id
             and r.scoring_version = sel.scoring_version
            where s.ticker = %s
              and sel.scoring_version = %s
              and sel.selection_version = %s
              and (m.end_date is null or m.end_date >= now())
            order by sel.rank asc
            limit %s;
            """,
            (str(ticker).upper(), scoring_version, effective_selection_version, int(limit)),
        )

        # Parse json fields for template convenience.
        out: list[dict[str, Any]] = []
        for r in rows:
            rr = dict(r)
            for k in ("selection_reason", "score_breakdown"):
                v = rr.get(k)
                if isinstance(v, str):
                    try:
                        rr[k] = json.loads(v)
                    except Exception:
                        pass
            out.append(rr)
        return out
    finally:
        conn.close()


def kept_markets(
    *,
    db_url: str,
    q: str | None,
    limit: int = 200,
    offset: int = 0,
) -> list[dict[str, Any]]:
    conn = connect(db_url)
    try:
        if q:
            return fetch_all(
                conn,
                """
                select pm_market_id as market_id, event_id, question, probability, end_date, volume_usd, liquidity_usd,
                       filter_version, quality_score, template_score, equity_relevance_score
                from v_pm_market_kept_latest
                where question ilike %s
                order by volume_usd desc nulls last
                limit %s offset %s;
                """,
                (f"%{q}%", int(limit), int(offset)),
            )
        return fetch_all(
            conn,
            """
            select pm_market_id as market_id, event_id, question, probability, end_date, volume_usd, liquidity_usd,
                   filter_version, quality_score, template_score, equity_relevance_score
            from v_pm_market_kept_latest
            order by volume_usd desc nulls last
            limit %s offset %s;
            """,
            (int(limit), int(offset)),
        )
    finally:
        conn.close()


def list_reports(*, db_url: str, limit: int = 50) -> list[dict[str, Any]]:
    conn = connect(db_url)
    try:
        return fetch_all(
            conn,
            """
            select
              r.report_id,
              r.created_at,
              r.prompt_version,
              r.model,
              s.ticker,
              s.company_name
            from pm_security_signal_report r
            join bit_security s on s.id = r.security_id
            order by r.created_at desc
            limit %s;
            """,
            (int(limit),),
        )
    finally:
        conn.close()


def fetch_report(*, db_url: str, report_id: str) -> dict[str, Any] | None:
    conn = connect(db_url)
    try:
        row = fetch_one(
            conn,
            """
            select
              r.report_id,
              r.created_at,
              r.prompt_version,
              r.model,
              r.report_json,
              r.report_md,
              s.ticker,
              s.company_name
            from pm_security_signal_report r
            join bit_security s on s.id = r.security_id
            where r.report_id = %s;
            """,
            (str(report_id),),
        )
        if not row:
            return None
        if isinstance(row.get("report_json"), str):
            try:
                row["report_json"] = json.loads(row["report_json"])
            except Exception:
                pass
        return row
    finally:
        conn.close()


def watchlist_securities(*, db_url: str) -> list[dict[str, Any]]:
    """Return the currently tracked securities (using `bit_holding` as a watchlist)."""
    conn = connect(db_url)
    try:
        return fetch_all(
            conn,
            """
            select
              s.id as security_id,
              s.ticker,
              s.company_name,
              s.exchange_mic,
              h.as_of,
              h.shares,
              h.total_value,
              h.value_currency
            from bit_holding h
            join bit_security s on s.id = h.security_id
            order by s.ticker;
            """,
        )
    finally:
        conn.close()


def latest_reports_for_security_ids(*, db_url: str, security_ids: list[int]) -> dict[int, dict[str, Any]]:
    ids = sorted({int(x) for x in (security_ids or [])})
    if not ids:
        return {}
    conn = connect(db_url)
    try:
        rows = fetch_all(
            conn,
            """
            select distinct on (r.security_id)
              r.security_id,
              r.report_id,
              r.created_at,
              r.prompt_version,
              r.model
            from pm_security_signal_report r
            where r.security_id = any(%s::bigint[])
            order by r.security_id, r.created_at desc;
            """,
            (ids,),
        )
        return {int(r["security_id"]): r for r in rows}
    finally:
        conn.close()


def selected_market_for_ticker_and_market_id(*, db_url: str, ticker: str, market_id: int) -> dict[str, Any] | None:
    conn = connect(db_url)
    try:
        run = fetch_one(conn, "select * from v_pm_latest_pipeline_run;") or {}
        scoring_version = str(run.get("scoring_version") or "")
        selection_version = str(run.get("selection_version") or "")
        if not scoring_version:
            return None

        effective_selection_version = selection_version
        if selection_version != "selected_v2":
            has_v2 = fetch_one(
                conn,
                """
                select 1 as ok
                from pm_market_security_relevance_selection
                where scoring_version = %s
                  and selection_version = 'selected_v2'
                limit 1;
                """,
                (scoring_version,),
            )
            if has_v2:
                effective_selection_version = "selected_v2"

        rows = fetch_all(
            conn,
            """
            select
              sel.security_id,
              s.ticker,
              s.company_name,
              sel.rank,
              sel.market_id,
              sel.event_id,
              sel.is_rate_like,
              sel.final_score as selection_score,
              sel.selection_reason,
              m.question,
              m.probability,
              m.end_date,
              m.volume_usd,
              m.liquidity_usd,
              e.title as event_title,
              r.base_score,
              r.quality_multiplier,
              r.final_score as relevance_final_score,
              r.score_breakdown
            from pm_market_security_relevance_selection sel
            join bit_security s on s.id = sel.security_id
            join pm_market m on m.pm_market_id = sel.market_id
            left join pm_event e on e.event_id = sel.event_id
            join pm_market_security_relevance r
              on r.security_id = sel.security_id
             and r.market_id = sel.market_id
             and r.scoring_version = sel.scoring_version
            where s.ticker = %s
              and sel.market_id = %s
              and sel.scoring_version = %s
              and sel.selection_version = %s
            limit 1;
            """,
            (str(ticker).upper(), int(market_id), scoring_version, effective_selection_version),
        )
        if not rows:
            return None
        rr = dict(rows[0])
        for k in ("selection_reason", "score_breakdown"):
            v = rr.get(k)
            if isinstance(v, str):
                try:
                    rr[k] = json.loads(v)
                except Exception:
                    pass
        return rr
    finally:
        conn.close()


def market_detail(*, db_url: str, market_id: int) -> dict[str, Any] | None:
    conn = connect(db_url)
    try:
        row = fetch_one(
            conn,
            """
            select
              m.pm_market_id as market_id,
              m.event_id,
              m.question,
              m.probability,
              m.volume_usd,
              m.liquidity_usd,
              m.end_date,
              m.slug as market_slug,
              e.title as event_title,
              e.slug as event_slug
            from pm_market m
            left join pm_event e on e.event_id = m.event_id
            where m.pm_market_id = %s;
            """,
            (int(market_id),),
        )
        return row
    finally:
        conn.close()


def market_filter_decision_latest(*, db_url: str, market_id: int) -> dict[str, Any] | None:
    conn = connect(db_url)
    try:
        run = fetch_one(conn, "select * from v_pm_latest_pipeline_run;") or {}
        fv = run.get("filter_version")
        if not fv:
            return None
        row = fetch_one(
            conn,
            """
            select
              filter_version,
              is_rejected,
              rejection_reasons,
              keep_reasons,
              quality_score,
              template_score,
              equity_relevance_score,
              decided_at
            from pm_market_filter_decision
            where market_id = %s and filter_version = %s;
            """,
            (int(market_id), str(fv)),
        )
        return row
    finally:
        conn.close()


def market_family_matches_latest(*, db_url: str, market_id: int, limit: int = 20) -> list[dict[str, Any]]:
    conn = connect(db_url)
    try:
        run = fetch_one(conn, "select * from v_pm_latest_pipeline_run;") or {}
        mv = run.get("matcher_version")
        if not mv:
            return []
        rows = fetch_all(
            conn,
            """
            select
              x.signal_family_id,
              sf.slug,
              sf.title,
              x.method,
              x.match_strength,
              x.evidence
            from pm_market_signal_family_match x
            join signal_family sf on sf.id = x.signal_family_id
            where x.matcher_version = %s
              and x.market_id = %s
            order by x.match_strength desc
            limit %s;
            """,
            (str(mv), int(market_id), int(limit)),
        )
        out: list[dict[str, Any]] = []
        for r in rows:
            rr = dict(r)
            ev = rr.get("evidence")
            if isinstance(ev, str):
                try:
                    rr["evidence"] = json.loads(ev)
                except Exception:
                    pass
            out.append(rr)
        return out
    finally:
        conn.close()


def set_watchlist(*, db_url: str, security_ids: list[int]) -> dict[str, int]:
    """Upsert/delete `bit_holding` rows to match the selected security_ids."""
    ids = sorted({int(x) for x in (security_ids or [])})
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if ids:
                cur.execute("delete from bit_holding where not (security_id = any(%s::bigint[]));", (ids,))
            else:
                cur.execute("delete from bit_holding;")

            inserted = 0
            if ids:
                cur.execute(
                    """
                    insert into bit_holding (security_id, shares, source_note)
                    select x::bigint, 0, 'webui watchlist'
                    from unnest(%s::bigint[]) as x
                    where not exists (select 1 from bit_holding h where h.security_id = x::bigint);
                    """,
                    (ids,),
                )
                inserted = int(cur.rowcount or 0)
        conn.commit()
        return {"selected": len(ids), "inserted": inserted}
    finally:
        conn.close()


def add_to_watchlist(*, db_url: str, security_id: int) -> bool:
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into bit_holding (security_id, shares, source_note)
                values (%s, 0, 'webui watchlist')
                on conflict (security_id) do nothing;
                """,
                (int(security_id),),
            )
            inserted = int(cur.rowcount or 0)
        conn.commit()
        return inserted > 0
    finally:
        conn.close()


def add_security_with_primary_domain(
    *,
    db_url: str,
    company_name: str,
    ticker: str,
    exchange_mic: str,
    primary_macro_domain_id: int,
    isin: str | None = None,
) -> dict[str, Any]:
    """Create a new security and seed a minimal exposure vector.

    For v1 simplicity, we seed a single exposure row with weight=1.0 to a chosen domain
    (so Step 4 scoring can produce relevance rows immediately after the next refresh).
    """
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into bit_security (company_name, ticker, exchange_mic, isin)
                values (%s, %s, %s, %s)
                returning id;
                """,
                (company_name.strip(), ticker.strip().upper(), exchange_mic.strip().upper(), (isin or None)),
            )
            security_id = int(cur.fetchone()[0])

            cur.execute(
                """
                insert into bit_security_macro_domain_exposure (
                  security_id,
                  macro_domain_id,
                  weight,
                  weight_basis,
                  source_ref
                )
                values (%s, %s, 1.0, 'custom', 'webui primary-domain seed')
                on conflict (security_id, macro_domain_id) do update set
                  weight = excluded.weight,
                  weight_basis = excluded.weight_basis,
                  source_ref = excluded.source_ref,
                  updated_at = now();
                """,
                (int(security_id), int(primary_macro_domain_id)),
            )
        conn.commit()
        return {"security_id": security_id}
    finally:
        conn.close()
