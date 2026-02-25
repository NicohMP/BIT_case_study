#!/usr/bin/env python3
"""Step 4: compute deterministic market relevance per BIT security.

Usage:
  ./venv/bin/python scripts/run_relevance_scoring.py \
    --filter-version hard_filters_v8 \
    --matcher-version matcher_v4 \
    --scoring-version relevance_v1
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.db.pg import connect  # noqa: E402
from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.relevance.rate_like import is_rate_like  # noqa: E402
from polyscanner.relevance.security_market_relevance import (  # noqa: E402
    compute_market_security_relevance,
    persist_relevance_selection,
)

def _diversified_top_rows(
    rows: list[tuple[float, float, float, int, str, Any, Any]],
    *,
    k: int,
    max_per_event: int = 1,
    max_rate_like: int = 3,
) -> list[tuple[float, float, float, int, str, Any, Any]]:
    """Greedy diversity selection for display/UI.

    This does NOT change stored relevance scores; it only picks a less-redundant top-K
    for presentation. It helps avoid:
    - 10 markets from the same event_id
    - rate/FOMC markets flooding every security's list
    """
    picked: list[tuple[float, float, float, int, str, Any, Any]] = []
    event_counts: dict[int, int] = {}
    rate_n = 0
    for r in rows:
        _final, _base, _q, _mid, qtext, _vol, event_id = r
        eid = int(event_id) if event_id is not None else -1
        is_rate = is_rate_like(str(qtext or ""))
        if eid != -1 and event_counts.get(eid, 0) >= int(max_per_event):
            continue
        if is_rate and rate_n >= int(max_rate_like):
            continue
        picked.append(r)
        if eid != -1:
            event_counts[eid] = event_counts.get(eid, 0) + 1
        if is_rate:
            rate_n += 1
        if len(picked) >= int(k):
            break
    return picked


def main() -> None:
    p = argparse.ArgumentParser(description="Compute deterministic market relevance per BIT security (Step 4).")
    p.add_argument("--filter-version", type=str, default=None, help="Hard filter version (defaults to YAML version).")
    p.add_argument("--matcher-version", type=str, required=True, help="Step 3 matcher_version to read matches from.")
    p.add_argument("--scoring-version", type=str, default="relevance_v1", help="Version label for Step 4 outputs.")
    p.add_argument("--limit-markets", type=int, default=None, help="Optional cap on kept markets considered.")
    p.add_argument("--limit-securities", type=int, default=None, help="Optional cap on securities considered.")
    p.add_argument("--min-base-score", type=float, default=0.0, help="Skip rows with base_score <= this value.")
    p.add_argument(
        "--trusted-only",
        type=str,
        default="true",
        help="true/false: score using only rule_classification matches (recommended for precision).",
    )
    p.add_argument("--diversify", type=str, default="false", help="true/false to diversify printed top lists (does not change DB).")
    p.add_argument("--diversify-k", type=int, default=10, help="K for diversified printed top list.")
    p.add_argument("--max-per-event", type=int, default=1, help="Max markets per event_id in diversified display.")
    p.add_argument("--max-rate-like", type=int, default=3, help="Max rate/FOMC-like markets in diversified display.")
    p.add_argument("--persist-selection", type=str, default="true", help="true/false to store diversified top-K selections in DB.")
    p.add_argument("--selection-version", type=str, default="selected_v1", help="Version label for persisted selection (Step 4b).")
    p.add_argument("--selection-k", type=int, default=20, help="K for stored diversified selection per security.")
    p.add_argument("--selection-max-per-event", type=int, default=1, help="Max markets per event_id in stored selection.")
    p.add_argument("--selection-max-rate-like", type=int, default=3, help="Max rate-like markets in stored selection.")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    res = compute_market_security_relevance(
        db_url=db_url,
        matcher_version=str(args.matcher_version),
        scoring_version=str(args.scoring_version),
        filter_version=args.filter_version,
        limit_markets=args.limit_markets,
        limit_securities=args.limit_securities,
        min_base_score=float(args.min_base_score),
        trusted_only=(str(args.trusted_only).strip().lower() in {"1", "true", "t", "yes", "y", "on"}),
    )

    persist_selection = (str(args.persist_selection).strip().lower() in {"1", "true", "t", "yes", "y", "on"})
    if persist_selection:
        sel = persist_relevance_selection(
            db_url=db_url,
            scoring_version=str(res.scoring_version),
            selection_version=str(args.selection_version),
            top_k=int(args.selection_k),
            max_per_event=int(args.selection_max_per_event),
            max_rate_like=int(args.selection_max_rate_like),
            limit_securities=res.securities_scored,
        )
        persist_selection = bool(sel.get("table_exists"))
        print(
            "relevance_selection:",
            {
                "scoring_version": str(res.scoring_version),
                "selection_version": str(args.selection_version),
                "securities_selected": int(sel["securities_selected"]),
                "rows_upserted": int(sel["rows_upserted"]),
            },
        )

    print(
        "relevance_scoring:",
        {
            "scoring_version": res.scoring_version,
            "filter_version": res.filter_version,
            "matcher_version": res.matcher_version,
            "securities_scored": res.securities_scored,
            "markets_considered": res.markets_considered,
            "rows_upserted": res.rows_upserted,
            "runtime_s": round(res.runtime_s, 3),
        },
    )

    # Lightweight QC: show top 10 markets per security by final_score.
    diversify = (args.diversify or "").strip().lower() in {"1", "true", "t", "yes", "y", "on"}
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, company_name, ticker
                from bit_security
                order by company_name, exchange_mic, ticker;
                """
            )
            securities = [{"id": int(r[0]), "company_name": str(r[1]), "ticker": str(r[2])} for r in cur.fetchall()]

        for s in securities[: res.securities_scored]:
            with conn.cursor() as cur:
                rows: list[Any] = []
                if persist_selection:
                    cur.execute(
                        """
                        select
                          s.final_score,
                          r.base_score,
                          r.quality_multiplier,
                          m.pm_market_id,
                          m.question,
                          m.volume_usd,
                          m.event_id
                        from pm_market_security_relevance_selection s
                        join pm_market_security_relevance r
                          on r.security_id = s.security_id
                         and r.market_id = s.market_id
                         and r.scoring_version = s.scoring_version
                        join pm_market m on m.pm_market_id = s.market_id
                        where s.security_id = %s
                          and s.scoring_version = %s
                          and s.selection_version = %s
                        order by s.rank asc
                        limit %s;
                        """,
                        (int(s["id"]), str(res.scoring_version), str(args.selection_version), int(args.diversify_k)),
                    )
                    rows = cur.fetchall()
                else:
                    # Fetch more than we print so we can diversify without missing good candidates.
                    fetch_limit = 200 if diversify else 10
                    cur.execute(
                        """
                        select
                          r.final_score,
                          r.base_score,
                          r.quality_multiplier,
                          m.pm_market_id,
                          m.question,
                          m.volume_usd,
                          m.event_id
                        from pm_market_security_relevance r
                        join pm_market m on m.pm_market_id = r.market_id
                        where r.security_id = %s
                          and r.scoring_version = %s
                        order by r.final_score desc
                        limit %s;
                        """,
                        (int(s["id"]), str(res.scoring_version), int(fetch_limit)),
                    )
                    rows = cur.fetchall()

            print(f"\nTop markets for {s['company_name']} ({s['ticker']}):")
            if not rows:
                print("- (none)")
                continue
            shown = rows
            if diversify and not persist_selection:
                shown = _diversified_top_rows(
                    rows,
                    k=int(args.diversify_k),
                    max_per_event=int(args.max_per_event),
                    max_rate_like=int(args.max_rate_like),
                )
            for final_score, base_score, q, mid, qtext, vol, _event_id in shown:
                qt = (str(qtext or "").strip().replace("\n", " "))[:160]
                print(f"- score={float(final_score):.6f} base={float(base_score):.6f} q={float(q):.3f} id={int(mid)} vol={vol} q={qt!r}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
