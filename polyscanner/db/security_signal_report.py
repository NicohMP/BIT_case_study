"""DB helpers for Step 5 (LLM report-time) artifacts."""

from __future__ import annotations

import json
from typing import Any


def upsert_pm_security_signal_report(
    conn,
    *,
    report_id: str,
    run_id: str | None,
    security_id: int,
    filter_version: str | None,
    matcher_version: str | None,
    scoring_version: str,
    selection_version: str,
    prompt_version: str,
    model: str,
    context_pack_hash: str,
    report_json: dict[str, Any],
    report_md: str | None,
) -> None:
    """Idempotent upsert keyed by (security_id, context_pack_hash, prompt_version, model)."""
    if not isinstance(report_json, dict):
        raise TypeError("report_json must be a dict")

    with conn.cursor() as cur:
        cur.execute(
            """
            insert into pm_security_signal_report (
              report_id,
              run_id,
              security_id,
              filter_version,
              matcher_version,
              scoring_version,
              selection_version,
              prompt_version,
              model,
              context_pack_hash,
              report_json,
              report_md
            )
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s)
            on conflict (security_id, context_pack_hash, prompt_version, model)
            do update set
              run_id = excluded.run_id,
              filter_version = excluded.filter_version,
              matcher_version = excluded.matcher_version,
              scoring_version = excluded.scoring_version,
              selection_version = excluded.selection_version,
              report_json = excluded.report_json,
              report_md = excluded.report_md,
              updated_at = now();
            """,
            (
                str(report_id),
                str(run_id) if run_id is not None else None,
                int(security_id),
                str(filter_version) if filter_version is not None else None,
                str(matcher_version) if matcher_version is not None else None,
                str(scoring_version),
                str(selection_version),
                str(prompt_version),
                str(model),
                str(context_pack_hash),
                json.dumps(report_json, ensure_ascii=False),
                report_md,
            ),
        )
    conn.commit()

