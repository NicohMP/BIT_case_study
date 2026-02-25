"""Pipeline run tracking (DB-backed).

This is intentionally lightweight and defensive:
- If the tracking table doesn't exist, callers can proceed without metadata.
- Updates are small JSON blobs per step for observability/debugging.
"""

from __future__ import annotations

import uuid
from typing import Any

try:
    from psycopg.types.json import Jsonb  # type: ignore
except Exception:  # pragma: no cover
    Jsonb = None  # type: ignore[assignment]


def new_run_id() -> str:
    return str(uuid.uuid4())


def _jsonb(value: Any) -> Any:
    if Jsonb is None:
        return value
    return Jsonb(value)


def pipeline_run_table_exists(conn) -> bool:
    with conn.cursor() as cur:
        cur.execute("select to_regclass(%s);", ("public.pm_pipeline_run",))
        return cur.fetchone()[0] is not None


def create_pipeline_run(
    conn,
    *,
    run_id: str,
    params: dict[str, Any],
    status: str = "running",
    filter_version: str | None = None,
    matcher_version: str | None = None,
    scoring_version: str | None = None,
    selection_version: str | None = None,
) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            insert into pm_pipeline_run (
              run_id,
              status,
              filter_version,
              matcher_version,
              scoring_version,
              selection_version,
              params,
              started_at,
              created_at,
              updated_at
            ) values (
              %(run_id)s,
              %(status)s,
              %(filter_version)s,
              %(matcher_version)s,
              %(scoring_version)s,
              %(selection_version)s,
              %(params)s,
              now(),
              now(),
              now()
            );
            """,
            {
                "run_id": str(run_id),
                "status": str(status),
                "filter_version": str(filter_version) if filter_version is not None else None,
                "matcher_version": str(matcher_version) if matcher_version is not None else None,
                "scoring_version": str(scoring_version) if scoring_version is not None else None,
                "selection_version": str(selection_version) if selection_version is not None else None,
                "params": _jsonb(params or {}),
            },
        )
    conn.commit()


_UPDATEABLE_FIELDS = {
    "status",
    "finished_at",
    "filter_version",
    "matcher_version",
    "scoring_version",
    "selection_version",
    "ingestion_summary",
    "hard_filters_summary",
    "matching_summary",
    "scoring_summary",
    "selection_summary",
    "audit_summary",
    "error",
}

_JSON_FIELDS = {
    "ingestion_summary",
    "hard_filters_summary",
    "matching_summary",
    "scoring_summary",
    "selection_summary",
    "audit_summary",
}


def update_pipeline_run(conn, *, run_id: str, **fields: Any) -> None:
    if not fields:
        return

    unknown = set(fields.keys()) - _UPDATEABLE_FIELDS
    if unknown:
        raise ValueError(f"Unknown pm_pipeline_run fields: {sorted(unknown)}")

    set_clauses: list[str] = []
    params: dict[str, Any] = {"run_id": str(run_id)}
    for k, v in fields.items():
        if k in _JSON_FIELDS:
            params[k] = _jsonb(v or {})
        else:
            params[k] = v
        if k == "finished_at" and v == "now":
            set_clauses.append("finished_at = now()")
            params.pop("finished_at", None)
        else:
            set_clauses.append(f"{k} = %({k})s")

    set_clauses.append("updated_at = now()")

    with conn.cursor() as cur:
        cur.execute(
            f"""
            update pm_pipeline_run
            set {", ".join(set_clauses)}
            where run_id = %(run_id)s;
            """,
            params,
        )
    conn.commit()

