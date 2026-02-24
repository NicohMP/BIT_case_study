"""Audit runner for the deterministic signal-family engine (Day 1 deliverable).

What it does
------------
- Ingest markets into Postgres from a curated Polymarket tag allowlist
- Recompute keyword matches (markets -> signal families) and persist them
- Write 2 audit artifacts:
  1) family coverage table (CSV)
  2) false-positive audit snapshot (Markdown)

Usage
-----
  ./venv/bin/python scripts/audit_signal_engine.py

Env vars
--------
- DATABASE_URL (required)
- POLYMARKET_API_BASE_URL (optional)
- PM_TAG_ALLOWLIST (optional; comma-separated tag_ids)

If PM_TAG_ALLOWLIST is not provided, this script will try to read
`notebooks/notebooks/exports/allowlist_tag_ids.csv` (created from notebooks).
"""

from __future__ import annotations

import csv
import json
import os
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.db.pg import connect, fetch_signal_families
from polyscanner.env import get_env, load_env
from polyscanner.pipeline.signal_family_mvp import run_signal_family_mvp


def _normalize_db_url(db_url: str) -> str:
    return db_url.strip().replace("postgresql+psycopg://", "postgresql://")


def _load_tag_allowlist_from_csv(path: Path) -> list[int]:
    with path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if "tag_id" not in (r.fieldnames or []):
            raise ValueError("CSV must contain a 'tag_id' column")
        out: list[int] = []
        for row in r:
            try:
                out.append(int(str(row.get("tag_id") or "").strip()))
            except Exception:
                continue
    return sorted({int(x) for x in out})


def load_tag_ids() -> list[int]:
    """Load tag_ids from env or notebook export."""
    env_val = (os.getenv("PM_TAG_ALLOWLIST") or "").strip()
    if env_val:
        parts = [p.strip() for p in env_val.split(",") if p.strip()]
        return sorted({int(p) for p in parts})

    repo_allow = Path("data/tag_allowlist_v1.csv")
    if repo_allow.exists():
        return _load_tag_allowlist_from_csv(repo_allow)

    nb_export = Path("notebooks/notebooks/exports/allowlist_tag_ids.csv")
    if nb_export.exists():
        return _load_tag_allowlist_from_csv(nb_export)

    raise RuntimeError(
        "No tag allowlist found. Set PM_TAG_ALLOWLIST or create notebooks/notebooks/exports/allowlist_tag_ids.csv"
    )


def fetch_family_coverage(db_url: str) -> list[dict[str, Any]]:
    """Return coverage rows: one per family with matched market count."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select
                  sf.slug,
                  sf.title,
                  count(distinct x.pm_market_id) as matched_markets
                from signal_family sf
                left join pm_market_signal_family_match x
                  on x.signal_family_id = sf.id
                 and x.match_method = 'keyword'
                where sf.is_active = true
                group by sf.slug, sf.title
                order by matched_markets desc, sf.slug asc;
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return [
        {"slug": str(r[0]), "title": str(r[1]), "matched_markets": int(r[2] or 0)}
        for r in rows
    ]


def fetch_match_samples(
    db_url: str,
    *,
    signal_family_id: int,
    n_top: int = 12,
    n_bottom: int = 12,
) -> dict[str, list[dict[str, Any]]]:
    """Fetch top + bottom samples for one family for manual false-positive audit."""
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select
                  m.pm_market_id,
                  m.question,
                  m.category,
                  m.probability,
                  m.volume_usd,
                  x.match_score,
                  x.matched_terms
                from pm_market_signal_family_match x
                join pm_market m on m.pm_market_id = x.pm_market_id
                where x.signal_family_id = %s
                  and x.match_method = 'keyword'
                order by x.match_score desc, m.volume_usd desc nulls last
                limit %s;
                """,
                (int(signal_family_id), int(n_top)),
            )
            top_rows = cur.fetchall()

            cur.execute(
                """
                select
                  m.pm_market_id,
                  m.question,
                  m.category,
                  m.probability,
                  m.volume_usd,
                  x.match_score,
                  x.matched_terms
                from pm_market_signal_family_match x
                join pm_market m on m.pm_market_id = x.pm_market_id
                where x.signal_family_id = %s
                  and x.match_method = 'keyword'
                order by x.match_score asc, m.volume_usd desc nulls last
                limit %s;
                """,
                (int(signal_family_id), int(n_bottom)),
            )
            bottom_rows = cur.fetchall()
    finally:
        conn.close()

    def _row(r) -> dict[str, Any]:
        mt = r[6]
        if mt is None:
            mt2: list[Any] = []
        elif isinstance(mt, list):
            mt2 = mt
        elif isinstance(mt, str):
            try:
                mt2 = json.loads(mt)
            except Exception:
                mt2 = []
        else:
            mt2 = []
        return {
            "pm_market_id": int(r[0]),
            "question": str(r[1]),
            "category": (str(r[2]) if r[2] is not None else None),
            "probability": (float(r[3]) if r[3] is not None else None),
            "volume_usd": (float(r[4]) if r[4] is not None else None),
            "match_score": (float(r[5]) if r[5] is not None else 0.0),
            "matched_terms": mt2,
        }

    return {
        "top": [_row(r) for r in top_rows],
        "bottom": [_row(r) for r in bottom_rows],
    }


def render_false_positive_audit_md(
    *,
    as_of: datetime,
    families: list[dict[str, Any]],
    coverage: list[dict[str, Any]],
    samples_by_slug: dict[str, dict[str, list[dict[str, Any]]]],
) -> str:
    lines: list[str] = []
    lines.append("# False Positive Audit Snapshot (keyword rules)")
    lines.append("")
    lines.append(f"- Generated at (UTC): `{as_of.isoformat()}`")
    lines.append("")

    cov_by_slug = {c["slug"]: c for c in coverage}

    for fam in families:
        slug = str(fam["slug"])
        lines.append(f"## {fam['title']}")
        lines.append(f"- slug: `{slug}`")
        lines.append(f"- matched_markets: {int((cov_by_slug.get(slug) or {}).get('matched_markets') or 0)}")
        lines.append("")

        samp = samples_by_slug.get(slug) or {}
        top = samp.get("top") or []
        bot = samp.get("bottom") or []

        lines.append("### Top matches (likely true positives)")
        if not top:
            lines.append("_No matches._")
        else:
            for r in top:
                lines.append(f"- ({r['match_score']:.3f}) `{r['pm_market_id']}` — {r['question']}")
                lines.append(f"  - matched_terms: `{json.dumps(r['matched_terms'], ensure_ascii=False)}`")
        lines.append("")

        lines.append("### Bottom matches (review for false positives)")
        if not bot:
            lines.append("_No matches._")
        else:
            for r in bot:
                lines.append(f"- ({r['match_score']:.3f}) `{r['pm_market_id']}` — {r['question']}")
                lines.append(f"  - matched_terms: `{json.dumps(r['matched_terms'], ensure_ascii=False)}`")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL")
    db_url = _normalize_db_url(db_url)

    tag_ids = load_tag_ids()
    as_of = datetime.now(timezone.utc)

    # Run ingestion + matching (no LLM).
    out = run_signal_family_mvp(
        db_url=db_url,
        tag_ids=tag_ids,
        ingest_from_tags=True,
        tag_markets_cap_per_tag=60,
        markets_limit=5000,
        top_n_per_family=10,
        out_dir="reports",
        use_llm=False,
    )

    # Coverage table across *all* matches.
    coverage = fetch_family_coverage(db_url)

    # False-positive snapshot: top and bottom examples per family.
    families = [asdict(sf) for sf in fetch_signal_families(db_url, active_only=True)]
    samples_by_slug: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for sf in fetch_signal_families(db_url, active_only=True):
        samples_by_slug[str(sf.slug)] = fetch_match_samples(
            db_url, signal_family_id=int(sf.id), n_top=12, n_bottom=12
        )

    # Write artifacts.
    out_dir = Path("reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = as_of.strftime("%Y%m%d_%H%M%S")

    cov_path = out_dir / f"family_coverage_{stamp}.csv"
    with cov_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["slug", "title", "matched_markets"])
        w.writeheader()
        for r in coverage:
            w.writerow(r)

    audit_md = render_false_positive_audit_md(
        as_of=as_of,
        families=families,
        coverage=coverage,
        samples_by_slug=samples_by_slug,
    )
    audit_path = out_dir / f"false_positive_audit_{stamp}.md"
    audit_path.write_text(audit_md, encoding="utf-8")

    # Persist the tag allowlist used for reproducibility.
    allow_path = out_dir / f"tag_allowlist_v1_{stamp}.json"
    allow_path.write_text(json.dumps({"tag_ids": tag_ids}, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "mvp_report_path": out.get("report_path"),
                "coverage_csv": str(cov_path),
                "false_positive_audit_md": str(audit_path),
                "tag_allowlist_json": str(allow_path),
                "deleted_previous_matches": out.get("deleted_previous_matches"),
                "upserted_matches": out.get("upserted_matches"),
                "ingestion_summary": out.get("ingestion_summary"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
