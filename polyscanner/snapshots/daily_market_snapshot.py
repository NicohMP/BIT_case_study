"""Daily snapshots of market state for later Δp / sentiment-intensity features.

This module intentionally does NOT compute Δp yet. It only persists state so
Δp can be computed deterministically later from DB history.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any, Literal

from polyscanner.db.pg import connect

log = logging.getLogger(__name__)

Scope = Literal["kept", "all"]


def _utc_today(d: date | None = None) -> date:
    if d is not None:
        return d
    return datetime.now(tz=timezone.utc).date()


try:
    from psycopg.types.json import Jsonb  # type: ignore
except Exception:  # pragma: no cover
    Jsonb = None  # type: ignore[assignment]


def _jsonb(value: Any) -> Any:
    if Jsonb is None:
        return value
    return Jsonb(value)


@dataclass(frozen=True)
class DailySnapshotResult:
    snapshot_date: str
    scope: str
    filter_version: str | None
    markets_selected: int
    rows_upserted: int
    runtime_s: float


def _fetch_latest_filter_version(conn) -> str | None:
    # Use the latest successful run if run tracking exists.
    with conn.cursor() as cur:
        cur.execute("select to_regclass(%s);", ("public.v_pm_latest_pipeline_run",))
        ok = cur.fetchone()[0] is not None
    if not ok:
        return None
    with conn.cursor() as cur:
        cur.execute("select filter_version from v_pm_latest_pipeline_run;")
        row = cur.fetchone()
    if not row:
        return None
    fv = row[0]
    return str(fv) if fv else None


def record_daily_market_snapshots(
    *,
    db_url: str,
    snapshot_date: date | None = None,
    scope: Scope = "kept",
    filter_version: str | None = None,
    run_id: str | None = None,
    limit: int | None = None,
) -> DailySnapshotResult:
    """Upsert daily snapshots for the selected universe."""
    import time

    started = time.monotonic()
    snap_d = _utc_today(snapshot_date)

    conn = connect(db_url)
    try:
        if scope == "kept":
            fv = str(filter_version or _fetch_latest_filter_version(conn) or "").strip() or None
            if not fv:
                raise RuntimeError("filter_version is required for scope='kept' (or apply pm_pipeline_run migration to use latest run).")
        else:
            fv = None

        # Build market universe.
        params: list[Any] = []
        where = ["coalesce(m.active, true) = true", "coalesce(m.closed, false) = false"]
        join = ""
        select_is_kept = "null::boolean as is_kept"
        if scope == "kept":
            join = "join pm_market_filter_decision d on d.market_id = m.pm_market_id and d.filter_version = %s"
            params.append(fv)
            where.append("d.is_rejected = false")
            select_is_kept = "true as is_kept"

        lim_sql = ""
        if limit is not None:
            lim_sql = "limit %s"
            params.append(int(limit))

        with conn.cursor() as cur:
            cur.execute(
                f"""
                select
                  m.pm_market_id as market_id,
                  m.probability,
                  m.probabilities,
                  m.outcomes,
                  m.volume_usd,
                  m.liquidity_usd,
                  m.end_date,
                  m.active,
                  m.closed,
                  {select_is_kept}
                from pm_market m
                {join}
                where {" and ".join(where)}
                order by m.pm_market_id asc
                {lim_sql};
                """,
                tuple(params),
            )
            rows = cur.fetchall()

        markets_selected = len(rows)
        if not rows:
            log.warning("No markets selected for daily snapshot (scope=%s filter_version=%s)", scope, fv)

        # Upsert one row per (snapshot_date, market_id).
        with conn.cursor() as cur:
            cur.executemany(
                """
                insert into pm_market_daily_snapshot (
                  snapshot_date,
                  market_id,
                  probability,
                  probabilities,
                  outcomes,
                  volume_usd,
                  liquidity_usd,
                  end_date,
                  active,
                  closed,
                  filter_version,
                  is_kept,
                  run_id,
                  source,
                  created_at
                )
                values (
                  %(snapshot_date)s,
                  %(market_id)s,
                  %(probability)s,
                  %(probabilities)s,
                  %(outcomes)s,
                  %(volume_usd)s,
                  %(liquidity_usd)s,
                  %(end_date)s,
                  %(active)s,
                  %(closed)s,
                  %(filter_version)s,
                  %(is_kept)s,
                  %(run_id)s,
                  %(source)s,
                  now()
                )
                on conflict (snapshot_date, market_id)
                do update set
                  probability = excluded.probability,
                  probabilities = excluded.probabilities,
                  outcomes = excluded.outcomes,
                  volume_usd = excluded.volume_usd,
                  liquidity_usd = excluded.liquidity_usd,
                  end_date = excluded.end_date,
                  active = excluded.active,
                  closed = excluded.closed,
                  filter_version = excluded.filter_version,
                  is_kept = excluded.is_kept,
                  run_id = excluded.run_id;
                """,
                [
                    {
                        "snapshot_date": snap_d,
                        "market_id": int(r[0]),
                        "probability": float(r[1]) if r[1] is not None else None,
                        "probabilities": _jsonb(r[2]) if r[2] is not None else None,
                        "outcomes": _jsonb(r[3]) if r[3] is not None else None,
                        "volume_usd": float(r[4]) if r[4] is not None else None,
                        "liquidity_usd": float(r[5]) if r[5] is not None else None,
                        "end_date": r[6],
                        "active": r[7],
                        "closed": r[8],
                        "filter_version": fv,
                        "is_kept": bool(r[9]) if r[9] is not None else None,
                        "run_id": str(run_id) if run_id is not None else None,
                        "source": "pm_market",
                    }
                    for r in rows
                ],
            )
        conn.commit()

        return DailySnapshotResult(
            snapshot_date=str(snap_d),
            scope=str(scope),
            filter_version=fv,
            markets_selected=int(markets_selected),
            rows_upserted=int(markets_selected),
            runtime_s=float(time.monotonic() - started),
        )
    finally:
        conn.close()

