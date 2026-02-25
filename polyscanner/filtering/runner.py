"""Step 2 runner: execute hard filters over the active Polymarket universe.

This module is the programmatic entrypoint for Step 2. The CLI wrapper lives in
`scripts/run_hard_filters.py`.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from polyscanner.db.pg import connect
from polyscanner.filtering.hard_filters import (
    FilterDecision,
    evaluate_market_filter,
    load_hard_filter_rules,
)

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class HardFilterRunResult:
    run_id: str
    filter_version: str
    config_sha256: str
    evaluated: int
    rejected: int
    audit_report: str
    runtime_s: float
    top_rejection_reasons: dict[str, int]
    top_kept_by_volume_usd: list[str]
    top_rejected_by_volume_usd: list[str]
    kept_high_relevance_examples: list[str]
    kept_low_quality_examples: list[str]


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def _as_market_dict(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "pm_market_id": row.get("pm_market_id"),
        "event_id": row.get("event_id"),
        "question": row.get("question"),
        "slug": row.get("slug"),
        "category": row.get("category"),
        "probability": row.get("probability"),
        "volume_usd": row.get("volume_usd"),
        "liquidity_usd": row.get("liquidity_usd"),
        "end_date": row.get("end_date"),
        "tags": row.get("market_tags") if isinstance(row.get("market_tags"), list) else [],
        "raw_market": row.get("raw_market") if isinstance(row.get("raw_market"), dict) else {},
    }


def _as_event_dict(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": row.get("event_id"),
        "title": row.get("event_title"),
        "slug": row.get("event_slug"),
        "tags": row.get("event_tags") if isinstance(row.get("event_tags"), list) else [],
        "raw_event": row.get("raw_event") if isinstance(row.get("raw_event"), dict) else {},
    }


def _fetch_active_universe(conn, *, limit: int | None = None):
    """Stream rows for active events/markets joined universe."""
    cursor_name = f"hard_filters_{int(time.time())}"
    cur = conn.cursor(name=cursor_name)
    params: list[Any] = []
    sql = """
        select
          m.pm_market_id,
          m.event_id,
          m.question,
          m.slug,
          m.category,
          m.probability,
          m.volume_usd,
          m.liquidity_usd,
          m.end_date,
          m.tags as market_tags,
          m.raw_market,

          e.title as event_title,
          e.slug as event_slug,
          e.tags as event_tags,
          e.raw_event
        from pm_market m
        join pm_event e on e.event_id = m.event_id
        where e.active = true and e.closed = false
        order by m.pm_market_id;
    """
    if limit is not None:
        sql = sql.rstrip().rstrip(";") + " limit %s;"
        params.append(int(limit))

    cur.execute(sql, params)
    return cur


def _upsert_decisions(conn, *, decisions: list[FilterDecision], filter_version: str) -> int:
    if not decisions:
        return 0
    rows = []
    for d in decisions:
        rows.append(
            {
                "market_id": int(d.market_id),
                "filter_version": str(filter_version),
                "is_rejected": bool(d.is_rejected),
                "template_score": float(d.template_score),
                "equity_relevance_score": float(d.equity_relevance_score),
                "quality_score": float(d.quality_score),
                "rejection_reasons": list(d.rejection_reasons),
                "keep_reasons": list(d.keep_reasons),
            }
        )

    with conn.cursor() as cur:
        cur.executemany(
            """
            insert into pm_market_filter_decision (
              market_id,
              filter_version,
              is_rejected,
              template_score,
              equity_relevance_score,
              quality_score,
              rejection_reasons,
              keep_reasons,
              decided_at
            ) values (
              %(market_id)s,
              %(filter_version)s,
              %(is_rejected)s,
              %(template_score)s,
              %(equity_relevance_score)s,
              %(quality_score)s,
              %(rejection_reasons)s,
              %(keep_reasons)s,
              now()
            )
            on conflict (market_id, filter_version) do update set
              is_rejected = excluded.is_rejected,
              template_score = excluded.template_score,
              equity_relevance_score = excluded.equity_relevance_score,
              quality_score = excluded.quality_score,
              rejection_reasons = excluded.rejection_reasons,
              keep_reasons = excluded.keep_reasons,
              decided_at = now();
            """,
            rows,
        )
    conn.commit()
    return len(rows)


def _insert_stats(
    conn,
    *,
    run_id: str,
    filter_version: str,
    config_sha256: str,
    n_evaluated: int,
    n_rejected: int,
    top_reasons: dict[str, int],
) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            insert into pm_market_filter_stats (
              run_id,
              filter_version,
              config_sha256,
              n_evaluated,
              n_rejected,
              top_reasons
            ) values (
              %(run_id)s::uuid,
              %(filter_version)s,
              %(config_sha256)s,
              %(n_evaluated)s,
              %(n_rejected)s,
              %(top_reasons)s::jsonb
            );
            """,
            {
                "run_id": run_id,
                "filter_version": filter_version,
                "config_sha256": config_sha256,
                "n_evaluated": int(n_evaluated),
                "n_rejected": int(n_rejected),
                "top_reasons": json.dumps(top_reasons),
            },
        )
    conn.commit()


def _format_market_line(row: dict[str, Any], decision: FilterDecision) -> str:
    q = (row.get("question") or "").strip().replace("\n", " ")
    q = q[:180] + ("…" if len(q) > 180 else "")
    return (
        f"- `{row.get('pm_market_id')}` (event `{row.get('event_id')}`) "
        f"q={q!r} vol={row.get('volume_usd')} liq={row.get('liquidity_usd')} "
        f"tmpl={decision.template_score:.2f} eq={decision.equity_relevance_score:.2f} qual={decision.quality_score:.2f} "
        f"rej={decision.is_rejected} reject={decision.rejection_reasons} keep={decision.keep_reasons}"
    )


def _write_audit_report(
    *,
    path: Path,
    rules_meta: dict[str, Any],
    n_evaluated: int,
    n_rejected: int,
    top_reasons: list[tuple[str, int]],
    per_reason_samples: dict[str, list[str]],
    kept_high_relevance_lines: list[str],
    kept_low_quality_lines: list[str],
    top_kept_by_volume: list[str],
    top_rejected_by_volume: list[str],
) -> None:
    lines: list[str] = []
    lines.append("# Hard Filter Audit\n")
    lines.append("## Run metadata\n")
    lines.append(f"- decided_at_utc: `{_utcnow().isoformat()}`")
    lines.append(f"- filter_version: `{rules_meta.get('filter_version')}`")
    lines.append(f"- config_sha256: `{rules_meta.get('config_sha256')}`")
    lines.append(f"- evaluated: `{n_evaluated}`")
    lines.append(f"- rejected: `{n_rejected}` ({(100.0 * n_rejected / max(1, n_evaluated)):.1f}%)\n")

    lines.append("## Top rejection reasons\n")
    for r, c in top_reasons[:20]:
        lines.append(f"- `{r}`: {c}")
    lines.append("")

    lines.append("## Samples by rejection reason\n")
    for r, _c in top_reasons[:12]:
        samples = per_reason_samples.get(r) or []
        if not samples:
            continue
        lines.append(f"### {r}\n")
        lines.extend(samples[:12])
        lines.append("")

    lines.append("## Kept high relevance (examples)\n")
    lines.extend(kept_high_relevance_lines[:20] or ["- (none)"])
    lines.append("")

    lines.append("## Kept low quality (examples)\n")
    lines.extend(kept_low_quality_lines[:20] or ["- (none)"])
    lines.append("")

    lines.append("## Top kept by volume_usd\n")
    lines.extend(top_kept_by_volume[:30] or ["- (none)"])
    lines.append("")

    lines.append("## Top rejected by volume_usd\n")
    lines.extend(top_rejected_by_volume[:30] or ["- (none)"])
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _fetch_top_by_volume(conn, *, filter_version: str, is_rejected: bool, limit: int = 30) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(
            """
            select
              d.market_id,
              d.is_rejected,
              d.rejection_reasons,
              d.keep_reasons,
              d.template_score,
              d.equity_relevance_score,
              d.quality_score,
              m.event_id,
              m.question,
              m.volume_usd,
              m.liquidity_usd
            from pm_market_filter_decision d
            join pm_market m on m.pm_market_id = d.market_id
            where d.filter_version = %s
              and d.is_rejected = %s
            order by m.volume_usd desc nulls last, m.liquidity_usd desc nulls last
            limit %s;
            """,
            (str(filter_version), bool(is_rejected), int(limit)),
        )
        rows = cur.fetchall()

    out: list[dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "market_id": int(r[0]),
                "is_rejected": bool(r[1]),
                "rejection_reasons": list(r[2]) if isinstance(r[2], (list, tuple)) else [],
                "keep_reasons": list(r[3]) if isinstance(r[3], (list, tuple)) else [],
                "template_score": float(r[4]) if r[4] is not None else None,
                "equity_relevance_score": float(r[5]) if r[5] is not None else None,
                "quality_score": float(r[6]) if r[6] is not None else None,
                "event_id": int(r[7]) if r[7] is not None else None,
                "question": str(r[8] or ""),
                "volume_usd": float(r[9]) if r[9] is not None else None,
                "liquidity_usd": float(r[10]) if r[10] is not None else None,
            }
        )
    return out


def _format_top_volume_line(row: dict[str, Any]) -> str:
    q = (row.get("question") or "").strip().replace("\n", " ")
    q = q[:180] + ("…" if len(q) > 180 else "")
    reasons = row["rejection_reasons"] if row.get("is_rejected") else row["keep_reasons"]
    return (
        f"- `{row['market_id']}` (event `{row.get('event_id')}`) "
        f"vol={row.get('volume_usd')} liq={row.get('liquidity_usd')} "
        f"tmpl={row.get('template_score')} eq={row.get('equity_relevance_score')} qual={row.get('quality_score')} "
        f"reasons={reasons}"
        f" q={q!r}"
    )


def run_hard_filters(
    *,
    db_url: str,
    limit: int | None = None,
    batch_size: int = 1000,
    out_dir: str = "reports",
    config_path: Path | None = None,
) -> HardFilterRunResult:
    """Run deterministic hard filters and persist auditable decisions.

    Notes:
    - Streams the active universe using a server-side cursor (named cursor).
    - Uses a dedicated read connection (streaming) and a write connection
      (batched upserts/commits), because server-side cursors are closed on COMMIT.
    """
    rules = load_hard_filter_rules(config_path=config_path)
    filter_version = rules.filter_version
    config_sha256 = rules.config_sha256

    run_id = str(uuid.uuid4())
    started = time.monotonic()

    read_conn = connect(db_url)
    write_conn = connect(db_url)
    try:
        with read_conn.cursor() as cur0:
            cur0.execute("select current_database(), current_user, inet_server_addr(), inet_server_port();")
            ident = cur0.fetchone() or ("", "", None, None)
            cur0.execute("select count(*) from pm_event;")
            n_events = int((cur0.fetchone() or [0])[0] or 0)
            cur0.execute("select count(*) from pm_market;")
            n_markets = int((cur0.fetchone() or [0])[0] or 0)
            cur0.execute("select count(*) from pm_event where active = true and closed = false;")
            n_active_events = int((cur0.fetchone() or [0])[0] or 0)
            cur0.execute(
                """
                select count(*)
                from pm_market m
                join pm_event e on e.event_id = m.event_id
                where e.active = true and e.closed = false;
                """
            )
            n_active_join = int((cur0.fetchone() or [0])[0] or 0)

        log.info(
            "db_preflight: db=%s user=%s host=%s port=%s pm_event=%s pm_market=%s active_events=%s active_join=%s",
            ident[0],
            ident[1],
            ident[2],
            ident[3],
            n_events,
            n_markets,
            n_active_events,
            n_active_join,
        )
        if n_active_join == 0:
            raise RuntimeError(
                "No active markets found in pm_market joined to pm_event (active=true & closed=false). "
                "Run Step 1 ingestion first."
            )

        cur = _fetch_active_universe(read_conn, limit=limit)
        evaluated = 0
        rejected = 0

        reason_counts: Counter[str] = Counter()
        per_reason_samples: dict[str, list[str]] = {}

        kept_high_relevance: list[tuple[float, str]] = []
        kept_low_quality: list[tuple[float, str]] = []

        batch: list[FilterDecision] = []

        colnames = [d.name for d in cur.description]  # type: ignore[union-attr]
        while True:
            rows = cur.fetchmany(int(batch_size))
            if not rows:
                break

            for tup in rows:
                row = {colnames[i]: tup[i] for i in range(len(colnames))}
                market = _as_market_dict(row)
                event = _as_event_dict(row)

                d = evaluate_market_filter(market, event)
                evaluated += 1
                if d.is_rejected:
                    rejected += 1
                    for r in d.rejection_reasons:
                        reason_counts[r] += 1
                        per_reason_samples.setdefault(r, [])
                        if len(per_reason_samples[r]) < 15:
                            per_reason_samples[r].append(_format_market_line(row, d))
                else:
                    kept_high_relevance.append(
                        (d.equity_relevance_score - (0.25 * d.template_score), _format_market_line(row, d))
                    )
                    kept_low_quality.append((d.quality_score, _format_market_line(row, d)))

                batch.append(d)
                if len(batch) >= int(batch_size):
                    _upsert_decisions(write_conn, decisions=batch, filter_version=filter_version)
                    batch.clear()

        if batch:
            _upsert_decisions(write_conn, decisions=batch, filter_version=filter_version)

        top_reasons = dict(reason_counts.most_common(50))
        _insert_stats(
            write_conn,
            run_id=run_id,
            filter_version=filter_version,
            config_sha256=config_sha256,
            n_evaluated=evaluated,
            n_rejected=rejected,
            top_reasons=top_reasons,
        )

        kept_high_relevance_sorted = [x[1] for x in sorted(kept_high_relevance, key=lambda t: t[0], reverse=True)]
        kept_low_quality_sorted = [x[1] for x in sorted(kept_low_quality, key=lambda t: t[0])]

        top_kept = _fetch_top_by_volume(write_conn, filter_version=filter_version, is_rejected=False, limit=30)
        top_rejected = _fetch_top_by_volume(write_conn, filter_version=filter_version, is_rejected=True, limit=30)
        top_kept_lines = [_format_top_volume_line(r) for r in top_kept]
        top_rejected_lines = [_format_top_volume_line(r) for r in top_rejected]

        out_path = Path(out_dir)
        ts = _utcnow().strftime("%Y%m%d_%H%M%S")
        audit_path = out_path / f"hard_filter_audit_{ts}.md"
        _write_audit_report(
            path=audit_path,
            rules_meta={"filter_version": filter_version, "config_sha256": config_sha256},
            n_evaluated=evaluated,
            n_rejected=rejected,
            top_reasons=list(reason_counts.most_common(50)),
            per_reason_samples=per_reason_samples,
            kept_high_relevance_lines=kept_high_relevance_sorted,
            kept_low_quality_lines=kept_low_quality_sorted,
            top_kept_by_volume=top_kept_lines,
            top_rejected_by_volume=top_rejected_lines,
        )

        runtime_s = time.monotonic() - started
        return HardFilterRunResult(
            run_id=run_id,
            filter_version=filter_version,
            config_sha256=config_sha256,
            evaluated=evaluated,
            rejected=rejected,
            audit_report=str(audit_path),
            runtime_s=float(runtime_s),
            top_rejection_reasons=dict(reason_counts.most_common(50)),
            top_kept_by_volume_usd=top_kept_lines[:30],
            top_rejected_by_volume_usd=top_rejected_lines[:30],
            kept_high_relevance_examples=kept_high_relevance_sorted[:20],
            kept_low_quality_examples=kept_low_quality_sorted[:20],
        )
    finally:
        try:
            write_conn.close()
        finally:
            read_conn.close()
