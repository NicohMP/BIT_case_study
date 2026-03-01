"""Coverage-first ingestion from Polymarket Gamma API `/events`.

This module implements "complete market discovery" by paginating the Gamma
`/events` endpoint with `active=true&closed=false`, then extracting the
associated `markets` embedded in each event payload.

Design goals:
- Deterministic pagination (limit/offset)
- Defensive normalization (schema may vary)
- Idempotent DB upserts (safe to rerun)
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import requests

from polyscanner.clients.gamma import GAMMA_BASE_URL_DEFAULT
from polyscanner.db.pg import connect
from polyscanner.env import get_env

try:
    from dateutil.parser import isoparse  # type: ignore
except Exception as e:  # pragma: no cover
    raise RuntimeError("python-dateutil is required for timestamp parsing") from e

try:
    from psycopg.types.json import Jsonb  # type: ignore
except Exception:  # pragma: no cover
    Jsonb = None  # type: ignore[assignment]

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class IngestResult:
    events_upserted: int
    markets_upserted: int
    pages: int
    last_offset: int
    runtime_s: float


def _safe_int(x: Any) -> int | None:
    if x is None:
        return None
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def _safe_float(x: Any) -> float | None:
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _safe_bool(x: Any) -> bool | None:
    if x is None:
        return None
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        return bool(x)
    if isinstance(x, str):
        v = x.strip().lower()
        if v in {"true", "t", "1", "yes", "y"}:
            return True
        if v in {"false", "f", "0", "no", "n"}:
            return False
    return None


def _parse_ts(x: Any) -> datetime | None:
    """Parse ISO8601 strings (and some common variants) into UTC datetimes."""
    if x is None:
        return None
    if isinstance(x, datetime):
        dt = x
    elif isinstance(x, (int, float)):
        # heuristic: treat huge numbers as ms epoch
        v = float(x)
        if v > 1e12:
            v = v / 1000.0
        try:
            dt = datetime.fromtimestamp(v, tz=timezone.utc)
        except Exception:
            return None
    elif isinstance(x, str):
        s = x.strip()
        if not s:
            return None
        try:
            dt = isoparse(s)
        except Exception:
            return None
    else:
        return None

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _jsonb(value: Any) -> Any:
    """Adapt Python objects for JSONB parameters (psycopg v3)."""
    if Jsonb is None:
        return value
    return Jsonb(value)


def _coerce_json_container(x: Any) -> Any:
    """If x is a JSON-encoded string, parse it. Otherwise return x.

    Gamma sometimes returns list/dict fields as strings like '["Yes","No"]'.
    """
    if not isinstance(x, str):
        return x
    s = x.strip()
    if not s:
        return x
    if not (s.startswith("[") or s.startswith("{")):
        return x
    try:
        return json.loads(s)
    except Exception:
        return x


def _get_with_retries(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any],
    timeout_s: float,
    max_retries: int = 7,
    base_backoff_s: float = 0.5,
) -> Any:
    last_err: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            resp = session.get(url, params=params, timeout=timeout_s)
            status = int(resp.status_code)

            if status == 200:
                return resp.json()

            if status == 429 or 500 <= status <= 599:
                retry_after = resp.headers.get("Retry-After")
                if retry_after:
                    try:
                        sleep_s = max(0.0, float(retry_after))
                    except Exception:
                        sleep_s = base_backoff_s * (2**attempt)
                else:
                    sleep_s = base_backoff_s * (2**attempt)
                sleep_s = min(30.0, sleep_s)
                log.warning("Gamma API retryable status=%s attempt=%s sleep_s=%.2f", status, attempt + 1, sleep_s)
                time.sleep(sleep_s)
                continue

            # Non-retryable 4xx
            body_preview = (resp.text or "")[:500]
            raise RuntimeError(f"Gamma API non-retryable status={status}: {body_preview}")

        except (requests.Timeout, requests.ConnectionError) as e:
            last_err = e
            sleep_s = min(30.0, base_backoff_s * (2**attempt))
            log.warning("Gamma API request error attempt=%s sleep_s=%.2f err=%r", attempt + 1, sleep_s, e)
            time.sleep(sleep_s)
            continue
        except Exception as e:
            last_err = e
            break

    raise RuntimeError("Gamma API request failed after retries") from last_err


def _extract_event_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("events", "data", "results"):
            v = payload.get(key)
            if isinstance(v, list):
                return [x for x in v if isinstance(x, dict)]
    raise TypeError(f"Unexpected /events payload type: {type(payload)}")


def _normalize_event(raw: dict[str, Any]) -> dict[str, Any]:
    event_id = _safe_int(raw.get("id"))
    if event_id is None:
        raise ValueError("Event missing integer id")

    slug = (raw.get("slug") or raw.get("eventSlug") or "") if isinstance(raw.get("slug") or raw.get("eventSlug"), str) else ""
    title = raw.get("title") or raw.get("name") or raw.get("question") or ""
    if not isinstance(title, str):
        title = str(title)
    title = title.strip()

    active = _safe_bool(raw.get("active"))
    closed = _safe_bool(raw.get("closed"))

    start_date = _parse_ts(raw.get("start_date") or raw.get("startDate") or raw.get("start_time") or raw.get("startTime"))
    end_date = _parse_ts(raw.get("end_date") or raw.get("endDate") or raw.get("end_time") or raw.get("endTime"))

    updated_at = _parse_ts(raw.get("updated_at") or raw.get("updatedAt") or raw.get("lastUpdatedAt") or raw.get("last_updated_at"))
    if updated_at is None:
        updated_at = _parse_ts(raw.get("created_at") or raw.get("createdAt"))

    volume_usd = _safe_float(raw.get("volumeUsd") or raw.get("volumeUSD") or raw.get("volume") or raw.get("volumeNum"))
    liquidity_usd = _safe_float(
        raw.get("liquidityUsd") or raw.get("liquidityUSD") or raw.get("liquidity") or raw.get("liquidityNum")
    )

    tags = raw.get("tags")
    if not isinstance(tags, list):
        tags = raw.get("tag") if isinstance(raw.get("tag"), list) else []

    return {
        "event_id": int(event_id),
        "slug": str(slug).strip() or None,
        "title": title or None,
        "active": active,
        "closed": closed,
        "start_date": start_date,
        "end_date": end_date,
        "volume_usd": volume_usd,
        "liquidity_usd": liquidity_usd,
        "tags": tags if isinstance(tags, list) else [],
        "raw_event": raw,
        "updated_at": updated_at,
    }


def _normalize_market(raw: dict[str, Any], *, event_id: int, event_tags: list[Any] | None) -> dict[str, Any] | None:
    market_id = _safe_int(raw.get("id"))
    if market_id is None:
        return None

    question = raw.get("question") or raw.get("title") or raw.get("name") or ""
    if not isinstance(question, str):
        question = str(question)
    question = question.strip()

    slug_val = raw.get("slug") or raw.get("marketSlug") or ""
    slug = str(slug_val).strip() if isinstance(slug_val, str) else ""

    active = _safe_bool(raw.get("active"))
    closed = _safe_bool(raw.get("closed"))

    end_date = _parse_ts(raw.get("end_date") or raw.get("endDate") or raw.get("expiry") or raw.get("expiration"))

    updated_at = _parse_ts(raw.get("updated_at") or raw.get("updatedAt") or raw.get("lastUpdatedAt") or raw.get("last_updated_at"))
    if updated_at is None:
        updated_at = _parse_ts(raw.get("created_at") or raw.get("createdAt"))

    volume_usd = _safe_float(raw.get("volumeUsd") or raw.get("volumeUSD") or raw.get("volume") or raw.get("volumeNum"))
    liquidity_usd = _safe_float(
        raw.get("liquidityUsd") or raw.get("liquidityUSD") or raw.get("liquidity") or raw.get("liquidityNum")
    )

    # Outcomes vs prices:
    # - Gamma commonly provides outcome labels in `outcomes` and outcome prices in `outcomePrices`.
    # - For binary markets, the "Yes" price is effectively the implied probability.
    outcomes = _coerce_json_container(raw.get("outcomes") or raw.get("outcome"))
    if not isinstance(outcomes, list):
        outcomes = None

    outcome_prices = _coerce_json_container(raw.get("outcomePrices") or raw.get("outcome_prices"))
    if not isinstance(outcome_prices, list):
        outcome_prices = None

    tokens = raw.get("clobTokenIds") or raw.get("clob_token_ids") or raw.get("tokens")

    prices = raw.get("prices") or raw.get("priceHistory") or raw.get("price_history")
    probabilities = _coerce_json_container(raw.get("probabilities") or raw.get("impliedProbabilities") or raw.get("implied_probabilities"))
    if probabilities is None and outcome_prices is not None:
        # For most Polymarket market types, "price" is the implied probability.
        parsed = [_safe_float(x) for x in outcome_prices]
        probabilities = parsed if any(p is not None for p in parsed) else None

    # Common "current probability"/price fields (binary convenience)
    probability = _safe_float(raw.get("probability"))
    if probability is None:
        probability = _safe_float(raw.get("yesPrice") or raw.get("yes_price") or raw.get("price"))
    if probability is None and outcomes and isinstance(probabilities, list) and len(outcomes) == len(probabilities):
        # If this is a Yes/No market, derive the Yes probability from the outcome vector.
        try:
            idx = None
            for i, o in enumerate(outcomes):
                label = None
                if isinstance(o, str):
                    label = o
                elif isinstance(o, dict):
                    label = o.get("outcome") or o.get("name") or o.get("title")
                label = (str(label) if label is not None else "").strip().lower()
                if label == "yes":
                    idx = i
                    break
            if idx is not None:
                probability = _safe_float(probabilities[idx])
        except Exception:
            pass

    tags = raw.get("tags")
    if not isinstance(tags, list):
        tags = event_tags if isinstance(event_tags, list) else []

    category: str | None = None
    if isinstance(raw.get("category"), str):
        category = raw.get("category")
    elif isinstance(tags, list) and tags:
        first = tags[0]
        if isinstance(first, dict):
            category = first.get("label") or first.get("slug")
        elif isinstance(first, str):
            category = first

    return {
        "pm_market_id": int(market_id),
        "event_id": int(event_id),
        "question": question or None,
        "slug": slug or None,
        "active": active,
        "closed": closed,
        "end_date": end_date,
        "category": category,
        "probability": probability,
        "volume_usd": volume_usd,
        "liquidity_usd": liquidity_usd,
        "outcomes": outcomes,
        "tokens": tokens,
        "prices": prices,
        "probabilities": probabilities,
        "tags": tags if isinstance(tags, list) else [],
        "raw_market": raw,
        "updated_at": updated_at,
    }


def _upsert_events(cur, events: list[dict[str, Any]]) -> int:
    if not events:
        return 0
    cur.executemany(
        """
        insert into pm_event (
          event_id,
          slug,
          title,
          active,
          closed,
          start_date,
          end_date,
          volume_usd,
          liquidity_usd,
          tags,
          raw_event,
          updated_at,
          ingested_at
        ) values (
          %(event_id)s,
          %(slug)s,
          %(title)s,
          %(active)s,
          %(closed)s,
          %(start_date)s,
          %(end_date)s,
          %(volume_usd)s,
          %(liquidity_usd)s,
          %(tags)s,
          %(raw_event)s,
          %(updated_at)s,
          now()
        )
        on conflict (event_id) do update set
          slug = excluded.slug,
          title = excluded.title,
          active = excluded.active,
          closed = excluded.closed,
          start_date = excluded.start_date,
          end_date = excluded.end_date,
          volume_usd = excluded.volume_usd,
          liquidity_usd = excluded.liquidity_usd,
          tags = excluded.tags,
          raw_event = excluded.raw_event,
          updated_at = coalesce(excluded.updated_at, pm_event.updated_at),
          ingested_at = now();
        """,
        [
            {
                **e,
                "tags": _jsonb(e.get("tags") or []),
                "raw_event": _jsonb(e.get("raw_event") or {}),
            }
            for e in events
        ],
    )
    return len(events)


def _upsert_markets(cur, markets: list[dict[str, Any]]) -> int:
    if not markets:
        return 0
    cur.executemany(
        """
        insert into pm_market (
          pm_market_id,
          event_id,
          question,
          slug,
          active,
          closed,
          end_date,
          category,
          probability,
          volume_usd,
          liquidity_usd,
          outcomes,
          tokens,
          prices,
          probabilities,
          tags,
          raw_market,
          last_seen_at,
          updated_at,
          ingested_at
        ) values (
          %(pm_market_id)s,
          %(event_id)s,
          coalesce(%(question)s, ''),
          %(slug)s,
          %(active)s,
          %(closed)s,
          %(end_date)s,
          %(category)s,
          %(probability)s,
          %(volume_usd)s,
          %(liquidity_usd)s,
          %(outcomes)s,
          %(tokens)s,
          %(prices)s,
          %(probabilities)s,
          %(tags)s,
          %(raw_market)s,
          now(),
          coalesce(%(updated_at)s, now()),
          now()
        )
        on conflict (pm_market_id) do update set
          event_id = excluded.event_id,
          question = excluded.question,
          slug = excluded.slug,
          active = excluded.active,
          closed = excluded.closed,
          end_date = excluded.end_date,
          category = excluded.category,
          probability = excluded.probability,
          volume_usd = excluded.volume_usd,
          liquidity_usd = excluded.liquidity_usd,
          outcomes = excluded.outcomes,
          tokens = excluded.tokens,
          prices = excluded.prices,
          probabilities = excluded.probabilities,
          tags = excluded.tags,
          raw_market = excluded.raw_market,
          last_seen_at = now(),
          updated_at = coalesce(excluded.updated_at, pm_market.updated_at),
          ingested_at = now();
        """,
        [
            {
                **m,
                "outcomes": _jsonb(m["outcomes"]) if m.get("outcomes") is not None else None,
                "tokens": _jsonb(m["tokens"]) if m.get("tokens") is not None else None,
                "prices": _jsonb(m["prices"]) if m.get("prices") is not None else None,
                "probabilities": _jsonb(m["probabilities"]) if m.get("probabilities") is not None else None,
                "tags": _jsonb(m.get("tags") or []),
                "raw_market": _jsonb(m.get("raw_market") or {}),
            }
            for m in markets
        ],
    )
    return len(markets)


def ingest_active_events_and_markets(
    limit: int = 100,
    max_pages: int | None = None,
    sleep_s: float = 0.2,
    since_ts: str | datetime | None = None,
    *,
    db_url: str | None = None,
    base_url: str = GAMMA_BASE_URL_DEFAULT,
    timeout_s: float = 30.0,
) -> IngestResult:
    """Ingest all active, non-closed events (and their markets) via `/events` pagination.

    Args:
        limit: Page size for Gamma `/events` pagination (limit/offset).
        max_pages: Optional cap on number of pages fetched.
        sleep_s: Sleep between pages to be polite with rate limits.
        since_ts: Optional timestamp filter (best-effort) if payloads include updated/created timestamps.
        db_url: Postgres connection string. Defaults to env `DATABASE_URL`.
        base_url: Gamma base URL; defaults to public Polymarket Gamma API.
        timeout_s: Requests timeout per HTTP call.
    """
    started = time.monotonic()
    base_url = (base_url or GAMMA_BASE_URL_DEFAULT).rstrip("/")

    if db_url is None:
        db_url = get_env("DATABASE_URL")
    if not db_url:
        raise ValueError("Missing db_url (or DATABASE_URL env var)")

    since_dt = _parse_ts(since_ts) if since_ts is not None else None
    if since_ts is not None and since_dt is None:
        raise ValueError("since_ts could not be parsed as a timestamp")

    session = requests.Session()
    session.headers.update({"User-Agent": "BIT-CaseStudy/0.1"})

    conn = connect(db_url)
    try:
        total_events = 0
        total_markets = 0
        offset = 0
        pages = 0

        saw_event_ts_field = False
        warned_partial_since = False
        total_events_seen = 0
        events_missing_ts = 0

        while True:
            if max_pages is not None and pages >= int(max_pages):
                log.info("Reached max_pages=%s; stopping", max_pages)
                break

            url = f"{base_url}/events"
            params = {
                "active": "true",
                "closed": "false",
                "limit": str(int(limit)),
                "offset": str(int(offset)),
            }

            payload = _get_with_retries(session, url, params=params, timeout_s=float(timeout_s))
            events_raw = _extract_event_list(payload)
            if not events_raw:
                log.info("No more events at offset=%s; stopping", offset)
                break

            norm_events: list[dict[str, Any]] = []
            norm_markets: list[dict[str, Any]] = []

            page_events_seen = 0
            page_events_missing_ts = 0
            page_saw_any_ts = False

            for ev in events_raw:
                try:
                    ne = _normalize_event(ev)
                except Exception:
                    continue

                page_events_seen += 1
                has_ts = ne.get("updated_at") is not None
                if has_ts:
                    saw_event_ts_field = True
                    page_saw_any_ts = True

                if since_dt is not None:
                    if not has_ts:
                        page_events_missing_ts += 1
                        events_missing_ts += 1
                        if not warned_partial_since:
                            warned_partial_since = True
                            # Important: mixed payloads (some have timestamps, some don't) make this filter partial.
                            # It's easy to mistakenly assume "incremental ingestion" is working when it isn't.
                            log.warning(
                                "since_ts=%s provided but some event payloads lack updated/created timestamps; "
                                "since filtering will be partial (missing_ts_seen>=1).",
                                since_dt.isoformat(),
                            )
                    else:
                        if ne["updated_at"] < since_dt:
                            continue

                norm_events.append(ne)

                event_id = int(ne["event_id"])
                event_tags = ne.get("tags") if isinstance(ne.get("tags"), list) else []
                markets_raw = ev.get("markets") or ev.get("Markets") or []
                if not isinstance(markets_raw, list):
                    markets_raw = []
                for m in markets_raw:
                    if not isinstance(m, dict):
                        continue
                    nm = _normalize_market(m, event_id=event_id, event_tags=event_tags)
                    if nm is None:
                        continue
                    norm_markets.append(nm)

            total_events_seen += page_events_seen
            if since_dt is not None and pages == 0 and not page_saw_any_ts:
                log.warning(
                    "since_ts=%s provided but no event timestamps were seen on the first page; "
                    "if subsequent pages also lack timestamps, since filtering will be ignored.",
                    since_dt.isoformat(),
                )

            with conn.cursor() as cur:
                events_up = _upsert_events(cur, norm_events)
                markets_up = _upsert_markets(cur, norm_markets)
            conn.commit()

            total_events += events_up
            total_markets += markets_up
            pages += 1

            log.info(
                "page=%s offset=%s n_events=%s n_markets=%s totals=(events=%s markets=%s)",
                pages,
                offset,
                len(norm_events),
                len(norm_markets),
                total_events,
                total_markets,
            )

            offset += int(limit)
            if sleep_s:
                time.sleep(float(sleep_s))

        runtime_s = time.monotonic() - started
        if since_dt is not None:
            if not saw_event_ts_field:
                log.warning(
                    "since_ts=%s provided but no event timestamps were found across all pages; since filtering was ignored.",
                    since_dt.isoformat(),
                )
            elif events_missing_ts > 0:
                log.warning(
                    "since_ts=%s applied partially: %s/%s events lacked timestamps and could not be filtered by time.",
                    since_dt.isoformat(),
                    events_missing_ts,
                    total_events_seen,
                )
        return IngestResult(
            events_upserted=total_events,
            markets_upserted=total_markets,
            pages=pages,
            last_offset=offset,
            runtime_s=runtime_s,
        )
    finally:
        conn.close()
