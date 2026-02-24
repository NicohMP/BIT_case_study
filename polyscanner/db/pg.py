"""Postgres helpers (psycopg).

This is intentionally tiny for the MVP:
- connect via DATABASE_URL
- fetch BIT domains from `bit_domain`

As the case study grows, this module also exposes read helpers for:
- DB-backed domain definitions (text for embeddings)
- transmission channels
- domain exposures to channels
"""

from __future__ import annotations

import json
from typing import Any

from polyscanner.models import (
    Domain,
    DomainChannelExposure,
    DomainDefinition,
    MacroDomain,
    SignalFamily,
    SignalFamilyDomainInfluence,
    TransmissionChannel,
)


def connect(db_url: str):
    try:
        import psycopg  # type: ignore

        return psycopg.connect(db_url)
    except Exception as e:
        raise RuntimeError("psycopg is required to connect to Postgres") from e


def fetch_bit_domains(db_url: str) -> list[Domain]:
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute("select id, name from bit_domain order by id;")
            rows = cur.fetchall()
        return [Domain(id=int(r[0]), name=str(r[1])) for r in rows]
    finally:
        conn.close()


def _as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value if x is not None]
    # psycopg might return tuples for arrays in some configurations
    if isinstance(value, tuple):
        return [str(x) for x in value if x is not None]
    return [str(value)]


def fetch_domain_definitions(db_url: str) -> list[DomainDefinition]:
    """Fetch domain definitions from `bit_domain` (requires definition migration)."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, name, description, keywords, exclusions
                from bit_domain
                order by id;
                """
            )
            rows = cur.fetchall()
        out: list[DomainDefinition] = []
        for r in rows:
            out.append(
                DomainDefinition(
                    id=int(r[0]),
                    name=str(r[1]),
                    description=str(r[2] or ""),
                    keywords=_as_list(r[3]),
                    exclusions=_as_list(r[4]),
                )
            )
        return out
    finally:
        conn.close()


def fetch_transmission_channels(db_url: str) -> list[TransmissionChannel]:
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select slug, label, description
                from transmission_channel
                order by slug;
                """
            )
            rows = cur.fetchall()
        return [TransmissionChannel(slug=str(r[0]), label=str(r[1]), description=str(r[2])) for r in rows]
    finally:
        conn.close()


def fetch_domain_channel_exposures(db_url: str) -> list[DomainChannelExposure]:
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select domain_id, channel_slug, exposure, rationale
                from bit_domain_channel_exposure
                order by domain_id, channel_slug;
                """
            )
            rows = cur.fetchall()
        return [
            DomainChannelExposure(
                domain_id=int(r[0]),
                channel_slug=str(r[1]),
                exposure=float(r[2]),
                rationale=str(r[3] or ""),
            )
            for r in rows
        ]
    finally:
        conn.close()


def exposure_matrix(exposures: list[DomainChannelExposure]) -> dict[int, dict[str, DomainChannelExposure]]:
    """Convenience: (domain_id, channel_slug) -> exposure."""
    out: dict[int, dict[str, DomainChannelExposure]] = {}
    for e in exposures:
        out.setdefault(e.domain_id, {})[e.channel_slug] = e
    return out


def fetch_macro_domains(db_url: str) -> list[MacroDomain]:
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute("select id, name, description from macro_domain order by id;")
            rows = cur.fetchall()
        return [MacroDomain(id=int(r[0]), name=str(r[1]), description=str(r[2] or "")) for r in rows]
    finally:
        conn.close()


def fetch_signal_families(db_url: str, *, active_only: bool = True) -> list[SignalFamily]:
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if active_only:
                cur.execute(
                    "select id, slug, title, description, is_active from signal_family where is_active = true order by id;"
                )
            else:
                cur.execute("select id, slug, title, description, is_active from signal_family order by id;")
            rows = cur.fetchall()
        return [
            SignalFamily(
                id=int(r[0]),
                slug=str(r[1]),
                title=str(r[2]),
                description=str(r[3] or ""),
                is_active=bool(r[4]),
            )
            for r in rows
        ]
    finally:
        conn.close()


def fetch_signal_family_domain_influence(db_url: str) -> list[SignalFamilyDomainInfluence]:
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select signal_family_id, macro_domain_id, score, rationale_md, sources
                from signal_family_domain_influence
                order by signal_family_id, macro_domain_id;
                """
            )
            rows = cur.fetchall()
        out: list[SignalFamilyDomainInfluence] = []
        for r in rows:
            sources = r[4]
            if sources is None:
                sources_list: list[dict[str, Any]] = []
            elif isinstance(sources, (list, tuple)):
                sources_list = [s for s in sources if isinstance(s, dict)]
            elif isinstance(sources, str):
                try:
                    parsed = json.loads(sources)
                    sources_list = parsed if isinstance(parsed, list) else []
                except Exception:
                    sources_list = []
            else:
                sources_list = []
            out.append(
                SignalFamilyDomainInfluence(
                    signal_family_id=int(r[0]),
                    macro_domain_id=int(r[1]),
                    score=int(r[2]),
                    rationale_md=str(r[3] or ""),
                    sources=sources_list,
                )
            )
        return out
    finally:
        conn.close()


def fetch_pm_markets(db_url: str, *, limit: int = 500) -> list[dict[str, Any]]:
    """Fetch latest Polymarket markets from `pm_market` table (normalized + raw)."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select pm_market_id, question, category, probability, volume_usd, raw
                from pm_market
                order by last_seen_at desc
                limit %s;
                """,
                (int(limit),),
            )
            rows = cur.fetchall()
        markets: list[dict[str, Any]] = []
        for r in rows:
            raw = r[5] if isinstance(r[5], dict) else {}
            markets.append(
                {
                    "pm_market_id": int(r[0]),
                    "question": str(r[1]),
                    "category": str(r[2]) if r[2] is not None else None,
                    "probability": float(r[3]) if r[3] is not None else None,
                    "volume": float(r[4]) if r[4] is not None else None,
                    "raw": raw,
                }
            )
        return markets
    finally:
        conn.close()


def upsert_pm_market_signal_family_matches(
    db_url: str,
    rows: list[dict[str, Any]],
) -> int:
    """Upsert rows into `pm_market_signal_family_match`."""
    if not rows:
        return 0
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.executemany(
                """
                insert into pm_market_signal_family_match (
                    pm_market_id,
                    signal_family_id,
                    match_method,
                    match_score,
                    matched_terms,
                    match_rationale,
                    matched_at,
                    updated_at
                ) values (
                    %(pm_market_id)s,
                    %(signal_family_id)s,
                    %(match_method)s,
                    %(match_score)s,
                    %(matched_terms)s::jsonb,
                    %(match_rationale)s,
                    now(),
                    now()
                )
                on conflict (pm_market_id, signal_family_id) do update set
                    match_method = excluded.match_method,
                    match_score = excluded.match_score,
                    matched_terms = excluded.matched_terms,
                    match_rationale = excluded.match_rationale,
                    matched_at = now(),
                    updated_at = now();
                """,
                rows,
            )
        conn.commit()
        return len(rows)
    finally:
        conn.close()


def fetch_top_markets_for_signal_family(
    db_url: str,
    *,
    signal_family_id: int,
    top_n: int = 10,
) -> list[dict[str, Any]]:
    """Return joined (match + pm_market) rows for report rendering."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select
                  m.pm_market_id,
                  m.question,
                  m.category,
                  m.probability,
                  m.volume_usd,
                  x.match_score,
                  x.matched_terms
                from pm_market_signal_family_match x
                join pm_market m on m.pm_market_id = x.pm_market_id
                where x.signal_family_id = %s
                order by x.match_score desc, m.volume_usd desc nulls last
                limit %s;
                """,
                (int(signal_family_id), int(top_n)),
            )
            rows = cur.fetchall()
        out: list[dict[str, Any]] = []
        for r in rows:
            matched_terms = r[6]
            if isinstance(matched_terms, list):
                mt = matched_terms
            elif isinstance(matched_terms, str):
                try:
                    mt = json.loads(matched_terms)
                except Exception:
                    mt = []
            else:
                mt = []
            out.append(
                {
                    "pm_market_id": int(r[0]),
                    "question": str(r[1]),
                    "category": str(r[2]) if r[2] is not None else None,
                    "probability": float(r[3]) if r[3] is not None else None,
                    "volume": float(r[4]) if r[4] is not None else None,
                    "match_score": float(r[5]) if r[5] is not None else 0.0,
                    "matched_terms": mt,
                }
            )
        return out
    finally:
        conn.close()


def delete_pm_market_signal_family_matches(
    db_url: str,
    *,
    signal_family_ids: list[int],
    match_method: str | None = None,
) -> int:
    """Delete matches for the given signal families.

    Why:
    - The MVP pipeline recomputes matches each run.
    - Without deletion, stale rows from older keyword rules can remain and pollute
      the candidate set (e.g., false positives that no longer match after rules change).
    """
    if not signal_family_ids:
        return 0
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if match_method is None:
                cur.execute(
                    """
                    delete from pm_market_signal_family_match
                    where signal_family_id = any(%s);
                    """,
                    (signal_family_ids,),
                )
            else:
                cur.execute(
                    """
                    delete from pm_market_signal_family_match
                    where signal_family_id = any(%s)
                      and match_method = %s;
                    """,
                    (signal_family_ids, str(match_method)),
                )
            deleted = int(cur.rowcount or 0)
        conn.commit()
        return deleted
    finally:
        conn.close()


def fetch_security(db_url: str, *, security_id: int) -> dict[str, Any] | None:
    """Fetch one BIT security row."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, company_name, ticker, exchange_mic, isin, country_iso2, currency_iso3
                from bit_security
                where id = %s;
                """,
                (int(security_id),),
            )
            row = cur.fetchone()
        if not row:
            return None
        return {
            "id": int(row[0]),
            "company_name": str(row[1]),
            "ticker": str(row[2]),
            "exchange_mic": str(row[3]),
            "isin": str(row[4]) if row[4] is not None else None,
            "country_iso2": str(row[5]) if row[5] is not None else None,
            "currency_iso3": str(row[6]) if row[6] is not None else None,
        }
    finally:
        conn.close()


def fetch_security_by_ticker(
    db_url: str,
    *,
    ticker: str,
    exchange_mic: str | None = None,
) -> dict[str, Any] | None:
    """Fetch one BIT security row by (ticker, optional exchange)."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if exchange_mic:
                cur.execute(
                    """
                    select id, company_name, ticker, exchange_mic, isin, country_iso2, currency_iso3
                    from bit_security
                    where upper(ticker) = upper(%s) and exchange_mic = %s
                    limit 1;
                    """,
                    (str(ticker), str(exchange_mic)),
                )
            else:
                cur.execute(
                    """
                    select id, company_name, ticker, exchange_mic, isin, country_iso2, currency_iso3
                    from bit_security
                    where upper(ticker) = upper(%s)
                    order by exchange_mic
                    limit 1;
                    """,
                    (str(ticker),),
                )
            row = cur.fetchone()
        if not row:
            return None
        return {
            "id": int(row[0]),
            "company_name": str(row[1]),
            "ticker": str(row[2]),
            "exchange_mic": str(row[3]),
            "isin": str(row[4]) if row[4] is not None else None,
            "country_iso2": str(row[5]) if row[5] is not None else None,
            "currency_iso3": str(row[6]) if row[6] is not None else None,
        }
    finally:
        conn.close()


def fetch_security_macro_domain_exposures(
    db_url: str,
    *,
    security_id: int,
) -> list[dict[str, Any]]:
    """Fetch security → macro_domain exposure weights."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select
                  x.security_id,
                  x.macro_domain_id,
                  d.name as macro_domain_name,
                  x.weight,
                  x.weight_basis,
                  x.source_ref,
                  x.as_of_date
                from bit_security_macro_domain_exposure x
                join macro_domain d on d.id = x.macro_domain_id
                where x.security_id = %s
                order by x.weight desc, d.name;
                """,
                (int(security_id),),
            )
            rows = cur.fetchall()
        out: list[dict[str, Any]] = []
        for r in rows:
            out.append(
                {
                    "security_id": int(r[0]),
                    "macro_domain_id": int(r[1]),
                    "macro_domain_name": str(r[2]),
                    "weight": float(r[3]),
                    "weight_basis": str(r[4]),
                    "source_ref": str(r[5] or ""),
                    "as_of_date": r[6].isoformat() if r[6] is not None else None,
                }
            )
        return out
    finally:
        conn.close()


def fetch_top_family_matches_per_market(
    db_url: str,
    *,
    market_ids: list[int] | None = None,
    top_k: int = 2,
    min_match_score: float = 0.0,
) -> list[dict[str, Any]]:
    """Fetch top-k signal-family matches per market (ranked by match_score)."""
    top_k = max(1, int(top_k))
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if market_ids:
                cur.execute(
                    """
                    with ranked as (
                      select
                        x.pm_market_id,
                        x.signal_family_id,
                        x.match_score,
                        x.matched_terms,
                        row_number() over (
                          partition by x.pm_market_id
                          order by x.match_score desc
                        ) as rn
                      from pm_market_signal_family_match x
                      where x.pm_market_id = any(%s)
                        and x.match_score >= %s
                    )
                    select
                      r.pm_market_id,
                      r.signal_family_id,
                      sf.slug,
                      sf.title,
                      r.match_score,
                      r.matched_terms
                    from ranked r
                    join signal_family sf on sf.id = r.signal_family_id
                    where r.rn <= %s
                    order by r.pm_market_id, r.match_score desc;
                    """,
                    (market_ids, float(min_match_score), int(top_k)),
                )
            else:
                cur.execute(
                    """
                    with ranked as (
                      select
                        x.pm_market_id,
                        x.signal_family_id,
                        x.match_score,
                        x.matched_terms,
                        row_number() over (
                          partition by x.pm_market_id
                          order by x.match_score desc
                        ) as rn
                      from pm_market_signal_family_match x
                      where x.match_score >= %s
                    )
                    select
                      r.pm_market_id,
                      r.signal_family_id,
                      sf.slug,
                      sf.title,
                      r.match_score,
                      r.matched_terms
                    from ranked r
                    join signal_family sf on sf.id = r.signal_family_id
                    where r.rn <= %s
                    order by r.pm_market_id, r.match_score desc;
                    """,
                    (float(min_match_score), int(top_k)),
                )
            rows = cur.fetchall()

        out: list[dict[str, Any]] = []
        for r in rows:
            out.append(
                {
                    "pm_market_id": int(r[0]),
                    "signal_family_id": int(r[1]),
                    "signal_family_slug": str(r[2]),
                    "signal_family_title": str(r[3]),
                    "match_score": float(r[4]),
                    "matched_terms": r[5] if isinstance(r[5], list) else [],
                }
            )
        return out
    finally:
        conn.close()


def fetch_pm_markets_for_scoring(
    db_url: str,
    *,
    limit: int = 2000,
    min_volume_usd: float | None = None,
) -> list[dict[str, Any]]:
    """Fetch markets ordered by volume (better universe for relevance ranking)."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if min_volume_usd is None:
                cur.execute(
                    """
                    select pm_market_id, question, category, probability, volume_usd
                    from pm_market
                    order by volume_usd desc nulls last, last_seen_at desc
                    limit %s;
                    """,
                    (int(limit),),
                )
            else:
                cur.execute(
                    """
                    select pm_market_id, question, category, probability, volume_usd
                    from pm_market
                    where volume_usd is not null and volume_usd >= %s
                    order by volume_usd desc, last_seen_at desc
                    limit %s;
                    """,
                    (float(min_volume_usd), int(limit)),
                )
            rows = cur.fetchall()

        out: list[dict[str, Any]] = []
        for r in rows:
            out.append(
                {
                    "pm_market_id": int(r[0]),
                    "question": str(r[1]),
                    "category": str(r[2]) if r[2] is not None else None,
                    "probability": float(r[3]) if r[3] is not None else None,
                    "volume_usd": float(r[4]) if r[4] is not None else None,
                }
            )
        return out
    finally:
        conn.close()
