"""Legacy wrapper for tag selection.

Historical context
------------------
This repo started with an embedding-heavy tag selection experiment living in this file.
We now prefer a simpler, data-driven approach:

  - discover tags from active events
  - sample markets per tag
  - compute per-family "yield" using keyword rules
  - select an allowlist under tunable thresholds

The new implementation lives in `polyscanner/ingestion/tag_selection.py`.

This module keeps backwards-compatible function names used in notebooks:
- `discover_tag_stats_from_active_events`
- `run_alternative_tag_selection`
"""

from __future__ import annotations

from polyscanner.ingestion.tag_selection import (  # re-export
    TagStat,
    TagYield,
    compute_tag_yield,
    discover_tag_stats_from_active_events,
    run_data_driven_tag_selection,
    select_allowlist_from_yield_rows,
    yield_rows_long,
)


# A small denylist for tags that are almost always too broad/noisy for market discovery.
# Keep minimal; expand only after inspecting outputs.
GENERIC_TAG_SLUGS: set[str] = {
    "business",
    "finance",
    "parlays",
    "politics",
    "sports",
    "movies",
    "news",
    "economy",
    "world",
    "usa",
}


def _filter_kwargs_for_data_driven(kwargs: dict) -> dict:
    """Drop parameters from older experiments that aren't used in the data-driven selector."""
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

    # Accept older parameter names (keep stable notebook calls).
    alias = {
        "tags_max_pages": "events_max_pages",
        "tags_page_size": "events_page_size",
    }

    out: dict = {}
    for k, v in kwargs.items():
        k2 = alias.get(k, k)
        if k2 in allowed:
            out[k2] = v
    return out


def run_alternative_tag_selection(**kwargs):
    """Compatibility alias for `run_data_driven_tag_selection`.

    We pass a default `generic_slugs` denylist unless the caller overrides it.
    """
    if "generic_slugs" not in kwargs:
        kwargs["generic_slugs"] = set(GENERIC_TAG_SLUGS)
    return run_data_driven_tag_selection(**_filter_kwargs_for_data_driven(kwargs))
