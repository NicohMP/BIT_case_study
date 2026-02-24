"""Gamma API helpers for tag-based market discovery (MVP).

This module is intentionally *low-level*:
- HTTP helpers for the Polymarket Gamma API
- Iterators for `/tags` and `/events`
- `tag_id -> markets` retrieval via `/events?tag_id=...`

Tag selection strategy
----------------------
The recommended tag selection approach is **data-driven** and lives in:
`polyscanner/ingestion/tag_selection.py`.

We keep a small wrapper here (`run_tag_selection`) because early notebooks used to
call `tag_base.run_tag_selection(...)`.
"""

from __future__ import annotations

import os
import re
import time
from typing import Any, Iterable


DEFAULT_GAMMA_BASE_URL = "https://gamma-api.polymarket.com"


# --------------------------------------------------------------------------------------
# Optional: seed helpers (still useful for debugging / curation)
# --------------------------------------------------------------------------------------


def _tokenize(s: str) -> list[str]:
    """Lowercase alphanumeric tokenization used for holding-name seeds."""
    return re.findall(r"[a-z0-9]+", s.lower())


def build_holding_seeds_from_db(db_url: str) -> set[str]:
    """Derive seed terms from BIT holdings stored in Postgres (tickers + name tokens)."""
    try:
        import psycopg  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError("psycopg is required to build holding seeds") from e

    db_url = db_url.strip().replace("postgresql+psycopg://", "postgresql://")
    conn = psycopg.connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select s.company_name, s.ticker
                from bit_holding h
                join bit_security s on s.id = h.security_id
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    seeds: set[str] = set()
    for company_name, ticker in rows:
        if ticker:
            seeds.add(str(ticker).strip().lower())
        if company_name:
            name = str(company_name).strip().lower()
            seeds.add(name)
            for tok in _tokenize(name):
                if len(tok) >= 4:
                    seeds.add(tok)
    return seeds


def build_seed_terms(
    *,
    macro_seeds: Iterable[str],
    include_holdings: bool = True,
    db_url: str | None = None,
    exclude: Iterable[str] | None = None,
) -> set[str]:
    """Build a seed term set used for optional lexical diagnostics."""
    seeds = {str(s).strip().lower() for s in macro_seeds if s and str(s).strip()}
    if include_holdings:
        db_url = db_url or os.getenv("DATABASE_URL")
        if db_url:
            seeds |= build_holding_seeds_from_db(db_url)
    if exclude:
        excluded = {str(s).strip().lower() for s in exclude if s and str(s).strip()}
        seeds -= excluded
    return {s for s in seeds if s}


def count_seed_hits(text: str, seeds: set[str]) -> tuple[int, list[str]]:
    """Count substring matches of seeds within `text` (lowercased)."""
    text_l = (text or "").lower()
    hits = [s for s in seeds if s in text_l]
    return len(hits), hits


# --------------------------------------------------------------------------------------
# Gamma API HTTP helpers
# --------------------------------------------------------------------------------------


def gamma_base_url() -> str:
    """Return the Gamma API base URL (env override supported)."""
    return (os.getenv("POLYMARKET_API_BASE_URL") or DEFAULT_GAMMA_BASE_URL).strip()


def _session():
    """Return a cached `requests.Session` with a user-agent."""
    import requests  # lazy import

    if not hasattr(_session, "_cached"):
        s = requests.Session()
        s.headers.update({"User-Agent": "BIT-CaseStudy/0.1"})
        _session._cached = s  # type: ignore[attr-defined]
    return _session._cached  # type: ignore[attr-defined]


def get_json(
    path: str,
    params: dict[str, Any] | None = None,
    *,
    base_url: str | None = None,
    timeout_s: int = 30,
) -> Any:
    """GET JSON from a Gamma endpoint."""
    base_url = (base_url or gamma_base_url()).rstrip("/")
    url = f"{base_url}{path}"
    sess = _session()
    r = sess.get(url, params=params or {}, timeout=timeout_s)
    r.raise_for_status()
    return r.json()


def try_get_json(
    path: str,
    params: dict[str, Any] | None = None,
    *,
    base_url: str | None = None,
    timeout_s: int = 30,
) -> tuple[bool, Any]:
    """Wrapper around `get_json` that returns `(ok, data_or_error)` instead of raising."""
    import requests  # lazy import

    try:
        return True, get_json(path, params=params, base_url=base_url, timeout_s=timeout_s)
    except requests.HTTPError as e:
        return False, {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None),
            "path": path,
            "params": params,
        }


# --------------------------------------------------------------------------------------
# Iterators for tag/event discovery
# --------------------------------------------------------------------------------------


def iter_tags(
    *,
    limit: int = 200,
    max_pages: int = 2000,
    sleep_s: float = 0.05,
    base_url: str | None = None,
):
    """Yield tags from `/tags` with offset pagination (best-effort).

    Stops early if the API appears to ignore `offset` (first id repeats).
    """
    first_id: str | None = None
    for page in range(max_pages):
        offset = page * limit
        data = get_json("/tags", {"limit": str(limit), "offset": str(offset)}, base_url=base_url)
        if not isinstance(data, list) or not data:
            break
        fid = str(data[0].get("id"))
        if page == 0:
            first_id = fid
        elif first_id is not None and fid == first_id:
            break
        for t in data:
            if isinstance(t, dict):
                yield t
        time.sleep(sleep_s)


def iter_active_events(
    *,
    limit: int = 100,
    max_pages: int = 200,
    sleep_s: float = 0.05,
    base_url: str | None = None,
):
    """Yield active events from `/events` with offset pagination (best-effort)."""
    first_id: str | None = None
    for page in range(max_pages):
        offset = page * limit
        data = get_json(
            "/events",
            {"limit": str(limit), "offset": str(offset), "closed": "false"},
            base_url=base_url,
        )
        if not isinstance(data, list) or not data:
            break
        fid = str(data[0].get("id"))
        if page == 0:
            first_id = fid
        elif first_id is not None and fid == first_id:
            break
        for ev in data:
            if isinstance(ev, dict):
                yield ev
        time.sleep(sleep_s)


def iter_active_event_tags(*, base_url: str | None = None, **kwargs):
    """Yield tag objects observed on active events (if present in payload)."""
    for ev in iter_active_events(base_url=base_url, **kwargs):
        for t in ev.get("tags") or []:
            if isinstance(t, dict):
                yield t


# --------------------------------------------------------------------------------------
# Tag -> markets retrieval
# --------------------------------------------------------------------------------------


def fetch_event_detail(event_id: Any, *, base_url: str | None = None) -> dict[str, Any] | None:
    """Fetch a single event by id (best-effort)."""
    ok, data = try_get_json(f"/events/{event_id}", base_url=base_url)
    return data if ok and isinstance(data, dict) else None


def extract_markets_from_event(ev: dict[str, Any], *, base_url: str | None = None) -> list[dict[str, Any]]:
    """Extract embedded markets from an event object (fallback to event detail if needed)."""
    mkts = ev.get("markets")
    if isinstance(mkts, list) and mkts:
        return [m for m in mkts if isinstance(m, dict)]
    detail = fetch_event_detail(ev.get("id"), base_url=base_url)
    if detail and isinstance(detail.get("markets"), list):
        return [m for m in detail["markets"] if isinstance(m, dict)]
    return []


def fetch_markets_for_tag(
    tag_id: int,
    *,
    max_events_pages: int = 5,
    events_page_size: int = 50,
    markets_cap: int = 25,
    sleep_s: float = 0.05,
    base_url: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch up to `markets_cap` active markets for a Polymarket `tag_id`.

    Why `/events`:
    - `GET /markets` doesn't consistently expose tags.
    - `GET /events?tag_id=...` is the most portable way to go tag_id → markets.
    """
    markets_by_id: dict[int, dict[str, Any]] = {}

    for page in range(max_events_pages):
        params = {
            "tag_id": str(tag_id),
            "closed": "false",
            "limit": str(events_page_size),
            "offset": str(page * events_page_size),
            "include_markets": "true",
        }
        ok, data = try_get_json("/events", params=params, base_url=base_url)
        if not ok:
            raise RuntimeError(f"Failed /events for tag_id={tag_id}: {data}")
        if not isinstance(data, list) or not data:
            break

        for ev in data:
            if not isinstance(ev, dict):
                continue
            for m in extract_markets_from_event(ev, base_url=base_url):
                mid = m.get("id")
                if mid is None:
                    continue
                try:
                    mid_i = int(mid)
                except Exception:
                    continue
                if mid_i not in markets_by_id and (m.get("question") or m.get("title")):
                    markets_by_id[mid_i] = m
                    if len(markets_by_id) >= markets_cap:
                        return list(markets_by_id.values())

        time.sleep(sleep_s)

    return list(markets_by_id.values())


# --------------------------------------------------------------------------------------
# Backwards-compatible selection wrapper
# --------------------------------------------------------------------------------------


def run_tag_selection(**kwargs) -> dict[str, Any]:
    """Compatibility wrapper around `run_data_driven_tag_selection`.

    Prefer importing from `polyscanner.ingestion.tag_selection` directly.
    """
    from polyscanner.ingestion.tag_selection import run_data_driven_tag_selection  # noqa: WPS433

    # Drop parameters from older embedding-based experiments to avoid breaking notebooks.
    allowed = {
        "base_url",
        "events_page_size",
        "events_max_pages",
        "sleep_s",
        "max_tag_candidates",
        "markets_per_tag",
        "min_markets_per_tag",
        "min_yield_count",
        "min_top_minus_second",
        "top_k_per_family",
        "generic_slugs",
    }
    filtered = {k: v for k, v in kwargs.items() if k in allowed}
    return run_data_driven_tag_selection(**filtered)
