#!/usr/bin/env python3
"""Audit the end-to-end Polymarket → filters → matching → relevance pipeline.

This produces a single markdown report that helps answer:
- Are we dominated by rate/FOMC markets because of scoring/influence, or because other markets are missing matches?
- Are Step 3 thresholds (lexical/cosine) too strict?
- Are strict family rules failing (gate/exclusion), causing low rule coverage?
- Are top lists overly concentrated in a single event (template factories / same event_id)?

Usage:
  ./venv/bin/python scripts/run_pipeline_audit.py \
    --filter-version hard_filters_v8 \
    --matcher-version matcher_v4 \
    --scoring-version relevance_v1
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.db.pg import connect  # noqa: E402
from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.filtering.hard_filters import load_hard_filter_rules  # noqa: E402
from polyscanner.relevance.rate_like import is_rate_like  # noqa: E402

log = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def _table_exists(conn, *, table_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("select to_regclass(%s);", (f"public.{table_name}",))
        return cur.fetchone()[0] is not None


def _pct(n: int, d: int) -> str:
    if d <= 0:
        return "0.0%"
    return f"{(100.0 * float(n) / float(d)):.2f}%"


def _quantiles(values: list[float], ps: list[float]) -> dict[str, float]:
    if not values:
        return {}
    xs = sorted(values)
    out: dict[str, float] = {}
    for p in ps:
        if p <= 0:
            out[f"p{int(p*100):02d}"] = float(xs[0])
            continue
        if p >= 1:
            out[f"p{int(p*100):02d}"] = float(xs[-1])
            continue
        idx = int(round((len(xs) - 1) * float(p)))
        out[f"p{int(p*100):02d}"] = float(xs[max(0, min(len(xs) - 1, idx))])
    return out


@dataclass(frozen=True)
class AuditPaths:
    markdown_path: str


def run_pipeline_audit(
    *,
    db_url: str,
    filter_version: str | None,
    matcher_version: str,
    scoring_version: str | None,
    selection_version: str | None = None,
    out_dir: str = "reports",
    top_n: int = 20,
) -> AuditPaths:
    if filter_version is None:
        filter_version = load_hard_filter_rules().filter_version

    now = _utcnow()
    stamp = now.strftime("%Y%m%d_%H%M%S")
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    md_path = out_path / f"pipeline_audit_{stamp}.md"

    lines: list[str] = []
    lines.append("# Pipeline Audit")
    lines.append("")
    lines.append(f"- as_of_utc: `{now.isoformat()}`")
    lines.append(f"- filter_version: `{filter_version}`")
    lines.append(f"- matcher_version: `{matcher_version}`")
    lines.append(f"- scoring_version: `{scoring_version or '(none provided)'}`")
    if selection_version is not None:
        lines.append(f"- selection_version: `{selection_version}`")
    lines.append("")

    conn = connect(db_url)
    try:
        # -----------------------
        # Step 1: ingestion sanity
        # -----------------------
        with conn.cursor() as cur:
            cur.execute("select count(*) from pm_event;")
            n_events = int(cur.fetchone()[0])
            cur.execute("select count(*) from pm_event where active = true and closed = false;")
            n_active_events = int(cur.fetchone()[0])
            cur.execute("select count(*) from pm_market;")
            n_markets = int(cur.fetchone()[0])
            cur.execute(
                """
                select count(*) as n, count(distinct m.event_id) as n_events
                from pm_market m
                join pm_event e on e.event_id = m.event_id
                where e.active = true and e.closed = false;
                """
            )
            n_active_markets, n_active_markets_events = [int(x) for x in cur.fetchone()]

        lines.append("## Step 1 — Ingestion")
        lines.append(f"- pm_event: {n_events} rows ({n_active_events} active & open)")
        lines.append(f"- pm_market: {n_markets} rows ({n_active_markets} linked to active & open events)")
        lines.append(f"- active events represented in pm_market: {n_active_markets_events}")
        lines.append("")

        with conn.cursor() as cur:
            cur.execute(
                """
                select m.event_id, count(*) as n
                from pm_market m
                join pm_event e on e.event_id = m.event_id
                where e.active = true and e.closed = false
                group by m.event_id
                order by n desc
                limit 20;
                """
            )
            top_events = [(int(r[0]), int(r[1])) for r in cur.fetchall()]

        lines.append("### Market concentration by event_id (top 20)")
        for eid, n in top_events:
            lines.append(f"- event_id={eid}: {n} markets")
        lines.append("")

        # -----------------------
        # Step 2: hard filters
        # -----------------------
        lines.append("## Step 2 — Hard filters")
        with conn.cursor() as cur:
            cur.execute(
                """
                select count(*) as n, sum((not is_rejected)::int) as kept
                from pm_market_filter_decision
                where filter_version = %s;
                """,
                (str(filter_version),),
            )
            r = cur.fetchone()
            n_decisions = int(r[0] or 0)
            n_kept = int(r[1] or 0)
        lines.append(f"- decisions: {n_decisions} (kept: {n_kept} = {_pct(n_kept, n_decisions)})")
        lines.append("")

        with conn.cursor() as cur:
            cur.execute(
                """
                select unnest(rejection_reasons) as reason, count(*) as n
                from pm_market_filter_decision
                where filter_version = %s and is_rejected = true
                group by 1
                order by n desc
                limit 20;
                """,
                (str(filter_version),),
            )
            top_reasons = [(str(r[0]), int(r[1])) for r in cur.fetchall()]
        if top_reasons:
            lines.append("### Top rejection reasons (top 20)")
            for reason, n in top_reasons:
                lines.append(f"- {reason}: {n}")
            lines.append("")

        # -----------------------
        # Step 3: matching coverage + threshold diagnostics
        # -----------------------
        lines.append("## Step 3 — Signal-family matching")
        with conn.cursor() as cur:
            cur.execute(
                """
                with kept as (
                  select market_id
                  from pm_market_filter_decision
                  where filter_version = %s and is_rejected = false
                )
                select
                  count(distinct k.market_id) as kept_markets,
                  count(distinct k.market_id) filter (where x.market_id is not null) as kept_with_any_match
                from kept k
                left join pm_market_signal_family_match x
                  on x.market_id = k.market_id and x.matcher_version = %s;
                """,
                (str(filter_version), str(matcher_version)),
            )
            kept_markets, kept_with_any_match = [int(x or 0) for x in cur.fetchone()]

            cur.execute(
                """
                select sf.slug, x.method, count(*) n
                from pm_market_signal_family_match x
                join signal_family sf on sf.id = x.signal_family_id
                where x.matcher_version = %s
                group by 1,2
                order by n desc;
                """,
                (str(matcher_version),),
            )
            by_family_method = [(str(r[0]), str(r[1]), int(r[2])) for r in cur.fetchall()]

        lines.append(f"- kept markets (filter): {kept_markets}")
        lines.append(f"- kept markets with ANY match row: {kept_with_any_match} ({_pct(kept_with_any_match, kept_markets)})")
        lines.append("")

        if by_family_method:
            lines.append("### Match rows by family + method")
            for slug, method, n in by_family_method[:50]:
                lines.append(f"- {slug} / {method}: {n}")
            lines.append("")

        # Rule pollution audit: do rate markets leak into unrelated families?
        with conn.cursor() as cur:
            cur.execute(
                """
                select sf.slug, m.question
                from pm_market_signal_family_match x
                join signal_family sf on sf.id = x.signal_family_id
                join pm_market m on m.pm_market_id = x.market_id
                where x.matcher_version = %s
                  and x.method = 'rule_classification';
                """,
                (str(matcher_version),),
            )
            rows = [(str(r[0]), str(r[1] or "")) for r in cur.fetchall()]
        fam_total = Counter()
        fam_rate = Counter()
        for slug, q in rows:
            fam_total[slug] += 1
            if is_rate_like(q):
                fam_rate[slug] += 1
        if fam_total:
            lines.append("### Rate/FOMC leakage into strict rule matches")
            for slug, n in fam_total.most_common():
                lines.append(f"- {slug}: {fam_rate[slug]}/{n} rate-like ({_pct(fam_rate[slug], n)})")
            lines.append("")

        # Threshold diagnostics, if Step 3 eval tables exist
        if _table_exists(conn, table_name="pm_market_family_match_run") and _table_exists(
            conn, table_name="pm_market_family_match_eval"
        ):
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select run_id, params, n_markets_evaluated, n_markets_with_embedding_candidate, n_markets_with_lexical_candidate
                    from pm_market_family_match_run
                    where filter_version = %s and matcher_version = %s
                    order by created_at desc
                    limit 1;
                    """,
                    (str(filter_version), str(matcher_version)),
                )
                rr = cur.fetchone()
            if rr:
                run_id = str(rr[0])
                params = rr[1] if isinstance(rr[1], dict) else (json.loads(rr[1]) if isinstance(rr[1], str) else {})
                lines.append("### Threshold diagnostics (latest Step-3 run)")
                lines.append(f"- run_id: `{run_id}`")
                lines.append(f"- params: `{json.dumps(params, ensure_ascii=False)}`")
                lines.append("")

                with conn.cursor() as cur:
                    cur.execute(
                        """
                        select
                          lexical_best_score,
                          embedding_best_similarity,
                          n_lexical_candidates,
                          n_embedding_candidates,
                          n_union_candidates
                        from pm_market_family_match_eval
                        where run_id = %s;
                        """,
                        (str(run_id),),
                    )
                    eval_rows = cur.fetchall()

                lex_best = [float(r[0] or 0.0) for r in eval_rows]
                emb_best = [float(r[1]) for r in eval_rows if r[1] is not None]
                n_lex_c = sum(1 for r in eval_rows if int(r[2] or 0) > 0)
                n_emb_c = sum(1 for r in eval_rows if int(r[3] or 0) > 0)
                n_any_c = sum(1 for r in eval_rows if int(r[4] or 0) > 0)

                lines.append(f"- markets evaluated: {len(eval_rows)}")
                lines.append(f"- markets with lexical candidates: {n_lex_c} ({_pct(n_lex_c, len(eval_rows))})")
                lines.append(f"- markets with embedding candidates: {n_emb_c} ({_pct(n_emb_c, len(eval_rows))})")
                lines.append(f"- markets with any candidates: {n_any_c} ({_pct(n_any_c, len(eval_rows))})")
                lines.append("")

                lines.append("#### Best lexical score distribution")
                ql = _quantiles(lex_best, [0.0, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 1.0])
                lines.append(f"- quantiles: `{json.dumps(ql)}`")
                lines.append("")

                if emb_best:
                    lines.append("#### Best embedding similarity distribution")
                    qe = _quantiles(emb_best, [0.0, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 1.0])
                    lines.append(f"- quantiles: `{json.dumps(qe)}`")
                    lines.append("")

                with conn.cursor() as cur:
                    cur.execute(
                        """
                        select sf.slug, count(*) as n
                        from pm_market_family_match_eval e
                        join signal_family sf on sf.id = e.embedding_best_signal_family_id
                        where e.run_id = %s and e.embedding_best_signal_family_id is not null
                        group by 1
                        order by n desc
                        limit 20;
                        """,
                        (str(run_id),),
                    )
                    emb_best_top = [(str(r[0]), int(r[1])) for r in cur.fetchall()]
                if emb_best_top:
                    lines.append("#### Most-common top-1 embedding family (top 20)")
                    for slug, n in emb_best_top:
                        lines.append(f"- {slug}: {n}")
                    lines.append("")

        # -----------------------
        # Step 4: relevance concentration
        # -----------------------
        if scoring_version:
            lines.append("## Step 4 — Relevance scoring")
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select count(*)
                    from pm_market_security_relevance
                    where scoring_version = %s;
                    """,
                    (str(scoring_version),),
                )
                n_rel = int(cur.fetchone()[0])
            lines.append(f"- pm_market_security_relevance rows for scoring_version={scoring_version!r}: {n_rel}")
            lines.append("")

            with conn.cursor() as cur:
                cur.execute(
                    """
                    select id, company_name, ticker
                    from bit_security
                    order by company_name, exchange_mic, ticker;
                    """
                )
                securities = [(int(r[0]), str(r[1]), str(r[2])) for r in cur.fetchall()]

            # For each security, audit concentration in top-N.
            for sid, cname, ticker in securities:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        select r.final_score, m.pm_market_id, m.event_id, m.question
                        from pm_market_security_relevance r
                        join pm_market m on m.pm_market_id = r.market_id
                        where r.security_id = %s and r.scoring_version = %s
                        order by r.final_score desc
                        limit %s;
                        """,
                        (int(sid), str(scoring_version), int(top_n)),
                    )
                    rows = cur.fetchall()
                if not rows:
                    continue
                event_counts = Counter(int(r[2]) for r in rows if r[2] is not None)
                n_unique_events = len(event_counts)
                n_rate_like = sum(1 for r in rows if is_rate_like(str(r[3] or "")))

                lines.append(f"### {cname} ({ticker}) — top {top_n}")
                lines.append(f"- unique events: {n_unique_events}/{len(rows)}")
                lines.append(f"- rate-like questions: {n_rate_like}/{len(rows)} ({_pct(n_rate_like, len(rows))})")
                if event_counts:
                    top_event_id, top_event_n = event_counts.most_common(1)[0]
                    lines.append(f"- most-common event_id: {top_event_id} ({top_event_n}/{len(rows)})")
                lines.append("")

                for final_score, mid, eid, q in rows[:10]:
                    lines.append(f"- ({float(final_score):.3f}) market_id={int(mid)} event_id={eid} — {str(q or '').strip()[:180]}")
                lines.append("")

            # If a selection table exists, report selection-quality diagnostics too.
            if selection_version and _table_exists(conn, table_name="pm_market_security_relevance_selection"):
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        select count(*)
                        from pm_market_security_relevance_selection
                        where scoring_version = %s and selection_version = %s;
                        """,
                        (str(scoring_version), str(selection_version)),
                    )
                    n_sel = int(cur.fetchone()[0])
                lines.append("## Step 4b — Stored diversified selection")
                lines.append(
                    f"- pm_market_security_relevance_selection rows for scoring_version={scoring_version!r} "
                    f"selection_version={selection_version!r}: {n_sel}"
                )
                lines.append("")

                for sid, cname, ticker in securities:
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            select s.rank, s.final_score, s.market_id, s.event_id, m.question
                            from pm_market_security_relevance_selection s
                            join pm_market m on m.pm_market_id = s.market_id
                            where s.security_id = %s
                              and s.scoring_version = %s
                              and s.selection_version = %s
                            order by s.rank asc
                            limit %s;
                            """,
                            (int(sid), str(scoring_version), str(selection_version), int(top_n)),
                        )
                        srows = cur.fetchall()
                    if not srows:
                        continue
                    event_counts = Counter(int(r[3]) for r in srows if r[3] is not None)
                    n_unique_events = len(event_counts)
                    n_rate_like = sum(1 for r in srows if is_rate_like(str(r[4] or "")))

                    lines.append(f"### {cname} ({ticker}) — selected top {top_n}")
                    lines.append(f"- unique events: {n_unique_events}/{len(srows)}")
                    lines.append(f"- rate-like questions: {n_rate_like}/{len(srows)} ({_pct(n_rate_like, len(srows))})")
                    if event_counts:
                        top_event_id, top_event_n = event_counts.most_common(1)[0]
                        lines.append(f"- most-common event_id: {top_event_id} ({top_event_n}/{len(srows)})")
                    lines.append("")

                    for rank, final_score, mid, eid, q in srows[:10]:
                        lines.append(
                            f"- ({int(rank):02d}) ({float(final_score):.3f}) market_id={int(mid)} event_id={eid} — {str(q or '').strip()[:180]}"
                        )
                    lines.append("")

    finally:
        conn.close()

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return AuditPaths(markdown_path=str(md_path))


def main() -> None:
    p = argparse.ArgumentParser(description="Audit Steps 1–4 for coverage + concentration + threshold health.")
    p.add_argument("--filter-version", type=str, default=None)
    p.add_argument("--matcher-version", type=str, required=True)
    p.add_argument("--scoring-version", type=str, default=None)
    p.add_argument("--selection-version", type=str, default=None)
    p.add_argument("--out-dir", type=str, default="reports")
    p.add_argument("--top-n", type=int, default=20)
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    out = run_pipeline_audit(
        db_url=db_url,
        filter_version=args.filter_version,
        matcher_version=str(args.matcher_version),
        scoring_version=args.scoring_version,
        selection_version=args.selection_version,
        out_dir=str(args.out_dir),
        top_n=int(args.top_n),
    )
    print("pipeline_audit:", {"markdown": out.markdown_path})


if __name__ == "__main__":
    main()
