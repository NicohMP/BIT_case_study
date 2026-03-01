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
                select pm_market_id, question, category, probability, volume_usd, raw_market
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
    """Upsert rows into Step-3 `pm_market_signal_family_match` table.

    Expected keys per row:
    - market_id
    - signal_family_id
    - method
    - matcher_version
    - match_strength
    - evidence (json-serializable; optional)
    - rationale (optional)
    """
    if not rows:
        return 0
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.executemany(
                """
                insert into pm_market_signal_family_match (
                    market_id,
                    signal_family_id,
                    method,
                    matcher_version,
                    match_strength,
                    evidence,
                    rationale,
                    created_at,
                    updated_at
                ) values (
                    %(market_id)s,
                    %(signal_family_id)s,
                    %(method)s,
                    %(matcher_version)s,
                    %(match_strength)s,
                    %(evidence)s::jsonb,
                    %(rationale)s,
                    now(),
                    now()
                )
                on conflict (market_id, signal_family_id, method, matcher_version) do update set
                    match_strength = excluded.match_strength,
                    evidence = excluded.evidence,
                    rationale = excluded.rationale,
                    updated_at = now();
                """,
                [
                    {
                        **r,
                        "evidence": json.dumps(r.get("evidence") or {}, ensure_ascii=False),
                        "rationale": r.get("rationale"),
                    }
                    for r in rows
                ],
            )
        conn.commit()
        return len(rows)
    finally:
        conn.close()


def fetch_top_markets_for_signal_family(
    db_url: str,
    *,
    signal_family_id: int,
    matcher_version: str,
    method: str = "rule_classification",
    min_strength: float = 0.70,
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
                  x.match_strength,
                  x.evidence
                from pm_market_signal_family_match x
                join pm_market m on m.pm_market_id = x.market_id
                where x.signal_family_id = %s
                  and x.matcher_version = %s
                  and x.method = %s
                  and x.match_strength >= %s
                order by x.match_strength desc, m.volume_usd desc nulls last
                limit %s;
                """,
                (int(signal_family_id), str(matcher_version), str(method), float(min_strength), int(top_n)),
            )
            rows = cur.fetchall()
        out: list[dict[str, Any]] = []
        for r in rows:
            evidence = r[6] if isinstance(r[6], dict) else {}
            matched_terms = evidence.get("matched_terms") if isinstance(evidence, dict) else None
            mt = matched_terms if isinstance(matched_terms, list) else []
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
    matcher_version: str,
    methods: list[str] | None = None,
) -> int:
    """Delete Step-3 matches for one matcher_version (for recompute)."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if methods:
                cur.execute(
                    """
                    delete from pm_market_signal_family_match
                    where matcher_version = %s
                      and method = any(%s);
                    """,
                    (str(matcher_version), [str(m) for m in methods]),
                )
            else:
                cur.execute(
                    """
                    delete from pm_market_signal_family_match
                    where matcher_version = %s;
                    """,
                    (str(matcher_version),),
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
    matcher_version: str,
    method: str = "rule_classification",
    top_k: int = 2,
    min_match_score: float = 0.70,
) -> list[dict[str, Any]]:
    """Fetch top-k signal-family matches per market (ranked by match_strength)."""
    top_k = max(1, int(top_k))
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if market_ids:
                cur.execute(
                    """
                    with ranked as (
                      select
                        x.market_id,
                        x.signal_family_id,
                        x.match_strength,
                        x.evidence,
                        row_number() over (
                          partition by x.market_id
                          order by x.match_strength desc
                        ) as rn
                      from pm_market_signal_family_match x
                      where x.market_id = any(%s)
                        and x.matcher_version = %s
                        and x.method = %s
                        and x.match_strength >= %s
                    )
                    select
                      r.market_id,
                      r.signal_family_id,
                      sf.slug,
                      sf.title,
                      r.match_strength,
                      r.evidence
                    from ranked r
                    join signal_family sf on sf.id = r.signal_family_id
                    where r.rn <= %s
                    order by r.market_id, r.match_strength desc;
                    """,
                    (market_ids, str(matcher_version), str(method), float(min_match_score), int(top_k)),
                )
            else:
                cur.execute(
                    """
                    with ranked as (
                      select
                        x.market_id,
                        x.signal_family_id,
                        x.match_strength,
                        x.evidence,
                        row_number() over (
                          partition by x.market_id
                          order by x.match_strength desc
                        ) as rn
                      from pm_market_signal_family_match x
                      where x.matcher_version = %s
                        and x.method = %s
                        and x.match_strength >= %s
                    )
                    select
                      r.market_id,
                      r.signal_family_id,
                      sf.slug,
                      sf.title,
                      r.match_strength,
                      r.evidence
                    from ranked r
                    join signal_family sf on sf.id = r.signal_family_id
                    where r.rn <= %s
                    order by r.market_id, r.match_strength desc;
                    """,
                    (str(matcher_version), str(method), float(min_match_score), int(top_k)),
                )
            rows = cur.fetchall()

        out: list[dict[str, Any]] = []
        for r in rows:
            evidence = r[5] if isinstance(r[5], dict) else {}
            matched_terms = evidence.get("matched_terms") if isinstance(evidence, dict) else None
            mt = matched_terms if isinstance(matched_terms, list) else []
            out.append(
                {
                    "pm_market_id": int(r[0]),
                    "signal_family_id": int(r[1]),
                    "signal_family_slug": str(r[2]),
                    "signal_family_title": str(r[3]),
                    "match_score": float(r[4]),
                    "matched_terms": mt,
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


def fetch_pm_active_markets_for_scoring(
    db_url: str,
    *,
    limit: int = 3000,
    min_volume_usd: float | None = None,
    hard_filter_version: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch active markets ordered by volume, with event+tag context.

    Intended for Step-3 matching + downstream scoring. If `hard_filter_version`
    is provided, only returns markets kept by the hard filters.
    """
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            params: list[Any] = []
            where = ["e.active = true and e.closed = false"]
            join_filter = ""
            if hard_filter_version:
                join_filter = """
                    join pm_market_filter_decision d
                      on d.market_id = m.pm_market_id
                     and d.filter_version = %s
                     and d.is_rejected = false
                """
                params.append(str(hard_filter_version))

            if min_volume_usd is not None:
                where.append("m.volume_usd is not null and m.volume_usd >= %s")
                params.append(float(min_volume_usd))

            params.append(int(limit))

            cur.execute(
                f"""
                select
                  m.pm_market_id,
                  m.question,
                  m.category,
                  m.probability,
                  m.volume_usd,
                  m.slug as market_slug,
                  m.tags as market_tags,
                  e.event_id,
                  e.title as event_title,
                  e.slug as event_slug,
                  e.tags as event_tags
                from pm_market m
                join pm_event e on e.event_id = m.event_id
                {join_filter}
                where {" and ".join(where)}
                order by m.volume_usd desc nulls last, m.last_seen_at desc
                limit %s;
                """,
                tuple(params),
            )
            rows = cur.fetchall()

        out: list[dict[str, Any]] = []
        for r in rows:
            out.append(
                {
                    "pm_market_id": int(r[0]),
                    "question": str(r[1] or ""),
                    "category": (str(r[2]) if r[2] is not None else None),
                    "probability": (float(r[3]) if r[3] is not None else None),
                    "volume_usd": (float(r[4]) if r[4] is not None else None),
                    "market_slug": (str(r[5]) if r[5] is not None else None),
                    "market_tags": (r[6] if isinstance(r[6], list) else []),
                    "event_id": int(r[7]) if r[7] is not None else None,
                    "event_title": (str(r[8]) if r[8] is not None else None),
                    "event_slug": (str(r[9]) if r[9] is not None else None),
                    "event_tags": (r[10] if isinstance(r[10], list) else []),
                }
            )
        return out
    finally:
        conn.close()


def fetch_pm_active_markets_for_matching(
    db_url: str,
    *,
    limit: int = 50_000,
    hard_filter_version: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch active, non-closed markets joined with event context for Step-3 matching.

    If `hard_filter_version` is provided, only returns markets that are *kept*
    (`pm_market_filter_decision.is_rejected = false`) for that version.
    """
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            if hard_filter_version:
                cur.execute(
                    """
                    select
                      m.pm_market_id,
                      m.event_id,
                      m.question,
                      m.category,
                      m.slug as market_slug,
                      m.tags as market_tags,
                      m.probability,
                      m.volume_usd,
                      m.liquidity_usd,
                      e.title as event_title,
                      e.slug as event_slug,
                      e.tags as event_tags
                    from pm_market m
                    join pm_event e on e.event_id = m.event_id
                    join pm_market_filter_decision d
                      on d.market_id = m.pm_market_id
                     and d.filter_version = %s
                     and d.is_rejected = false
                    where e.active = true and e.closed = false
                    order by m.volume_usd desc nulls last, m.pm_market_id
                    limit %s;
                    """,
                    (str(hard_filter_version), int(limit)),
                )
            else:
                cur.execute(
                    """
                    select
                      m.pm_market_id,
                      m.event_id,
                      m.question,
                      m.category,
                      m.slug as market_slug,
                      m.tags as market_tags,
                      m.probability,
                      m.volume_usd,
                      m.liquidity_usd,
                      e.title as event_title,
                      e.slug as event_slug,
                      e.tags as event_tags
                    from pm_market m
                    join pm_event e on e.event_id = m.event_id
                    where e.active = true and e.closed = false
                    order by m.volume_usd desc nulls last, m.pm_market_id
                    limit %s;
                    """,
                    (int(limit),),
                )
            rows = cur.fetchall()

        out: list[dict[str, Any]] = []
        for r in rows:
            out.append(
                {
                    "pm_market_id": int(r[0]),
                    "event_id": int(r[1]) if r[1] is not None else None,
                    "question": str(r[2] or ""),
                    "category": (str(r[3]) if r[3] is not None else None),
                    "market_slug": (str(r[4]) if r[4] is not None else None),
                    "market_tags": (r[5] if isinstance(r[5], list) else []),
                    "probability": (float(r[6]) if r[6] is not None else None),
                    "volume_usd": (float(r[7]) if r[7] is not None else None),
                    "liquidity_usd": (float(r[8]) if r[8] is not None else None),
                    "event_title": (str(r[9]) if r[9] is not None else None),
                    "event_slug": (str(r[10]) if r[10] is not None else None),
                    "event_tags": (r[11] if isinstance(r[11], list) else []),
                }
            )
        return out
    finally:
        conn.close()
