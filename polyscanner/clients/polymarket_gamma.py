"""Polymarket Gamma API client (minimal).

Purpose (MVP):
- Fetch active markets from Polymarket's public Gamma API
- Normalize a few fields we need downstream (question, probability, volume)
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from polyscanner.models import PMMarket


GAMMA_BASE_URL_DEFAULT = "https://gamma-api.polymarket.com"


def _safe_float(x: Any) -> float | None:
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _http_get_json(url: str, *, timeout_s: int = 30) -> Any:
    req = Request(url, headers={"User-Agent": "BIT-CaseStudy/0.1"})
    with urlopen(req, timeout=timeout_s) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def fetch_active_markets(
    *,
    base_url: str = GAMMA_BASE_URL_DEFAULT,
    limit: int = 200,
    offset: int = 0,
    closed: bool = False,
    timeout_s: int = 30,
) -> list[dict[str, Any]]:
    """Fetch a page of markets from `/markets`."""
    base_url = base_url.rstrip("/")
    qs = urlencode({"limit": str(limit), "offset": str(offset), "closed": "true" if closed else "false"})
    url = f"{base_url}/markets?{qs}"
    data = _http_get_json(url, timeout_s=timeout_s)
    if not isinstance(data, list):
        raise TypeError(f"Expected list from Gamma /markets, got {type(data)}")
    return data


def normalize_market(raw: dict[str, Any]) -> PMMarket:
    pm_market_id = int(raw.get("id"))
    question = str(raw.get("question") or raw.get("title") or "").strip()

    category: str | None = None
    if isinstance(raw.get("category"), str):
        category = raw.get("category")
    elif isinstance(raw.get("tags"), list) and raw["tags"]:
        first = raw["tags"][0]
        if isinstance(first, dict):
            category = first.get("label") or first.get("slug")

    probability = _safe_float(raw.get("probability"))
    if probability is None:
        probability = _safe_float(raw.get("yesPrice") or raw.get("yes_price") or raw.get("price"))

    volume = _safe_float(raw.get("volumeNum") or raw.get("volume") or raw.get("volumeUsd") or raw.get("volumeUSD"))

    return PMMarket(
        pm_market_id=pm_market_id,
        question=question,
        category=category,
        probability=probability,
        volume=volume,
        raw=raw,
    )


def fetch_and_normalize_active_markets(
    *,
    base_url: str = GAMMA_BASE_URL_DEFAULT,
    limit: int = 200,
    offset: int = 0,
    timeout_s: int = 30,
) -> list[PMMarket]:
    raw = fetch_active_markets(base_url=base_url, limit=limit, offset=offset, closed=False, timeout_s=timeout_s)
    markets: list[PMMarket] = []
    for m in raw:
        if not isinstance(m, dict):
            continue
        try:
            nm = normalize_market(m)
        except Exception:
            continue
        if nm.question:
            markets.append(nm)
    return markets

