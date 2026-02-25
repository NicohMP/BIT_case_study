#!/usr/bin/env python3
"""Seed/override `bit_security_macro_domain_exposure` from `security_domain_exposure_scores.md`.

This is the "authority" layer that determines how exposed each BIT security is to each
macro_domain (industry segment). Step 4 relevance scoring requires these weights.

The markdown file uses 0–3 scores; this script normalizes them into weights that sum to 1.0
per security and upserts them into Postgres.

Usage:
  ./venv/bin/python scripts/seed_security_domain_exposure.py
  ./venv/bin/python scripts/seed_security_domain_exposure.py --dry-run
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.db.pg import connect  # noqa: E402
from polyscanner.env import get_env, load_env  # noqa: E402

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExposureRow:
    company_name: str
    scores: dict[str, int]  # macro_domain.name -> 0..3 score


_HEADER_TO_DOMAIN_NAME = {
    "AI & Data Platforms": "AI & Big Tech",
    "Semiconductors & Compute": "Semis & Compute",
    "Cloud & Software Infra": "Cloud / Dev",
    "Crypto Mining & Infra": "Crypto Infra",
    "Fintech": "Fintech / CFP",
    "Digital Health": "Digital Health",
}


def _parse_md_table(md_text: str) -> list[ExposureRow]:
    lines = [ln.rstrip("\n") for ln in md_text.splitlines()]
    start_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("|") and "Company" in ln and "Digital Health" in ln:
            start_idx = i
            break
    if start_idx is None or start_idx + 2 >= len(lines):
        raise ValueError("Could not find markdown table header row in security_domain_exposure_scores.md")

    header_cells = [c.strip() for c in lines[start_idx].strip().strip("|").split("|")]
    if not header_cells or header_cells[0] != "Company":
        raise ValueError(f"Unexpected header row: {header_cells!r}")

    raw_headers = header_cells[1:]
    mapped_headers: list[str] = []
    for h in raw_headers:
        if h not in _HEADER_TO_DOMAIN_NAME:
            raise ValueError(f"Unrecognized exposure column header {h!r}; update _HEADER_TO_DOMAIN_NAME")
        mapped_headers.append(_HEADER_TO_DOMAIN_NAME[h])

    rows: list[ExposureRow] = []
    for ln in lines[start_idx + 2 :]:
        if not ln.strip().startswith("|"):
            break
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        company = cells[0]
        vals = cells[1 : 1 + len(mapped_headers)]
        if len(vals) != len(mapped_headers):
            continue
        scores: dict[str, int] = {}
        for dom_name, v in zip(mapped_headers, vals, strict=True):
            v = v.strip()
            if not re.fullmatch(r"\d+", v):
                raise ValueError(f"Non-integer exposure score for {company!r} / {dom_name!r}: {v!r}")
            scores[dom_name] = int(v)
        rows.append(ExposureRow(company_name=company, scores=scores))

    if not rows:
        raise ValueError("Parsed 0 exposure rows from security_domain_exposure_scores.md")
    return rows


def _normalize_scores_to_weights(scores: dict[str, int]) -> dict[str, float]:
    total = float(sum(max(0, int(v)) for v in scores.values()))
    if total <= 0.0:
        raise ValueError("All exposure scores are zero; cannot normalize to weights")
    out = {k: (float(v) / total) for k, v in scores.items() if int(v) > 0}
    s = sum(out.values())
    if not (0.999 <= s <= 1.001):
        raise ValueError(f"Normalized weights must sum to 1.0 (got {s})")
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Seed/override security→macro_domain exposure weights from markdown.")
    p.add_argument(
        "--scores-path",
        type=str,
        default="security_domain_exposure_scores.md",
        help="Path to markdown scores table (0–3).",
    )
    p.add_argument("--as-of-date", type=str, default=None, help="Optional YYYY-MM-DD for as_of_date.")
    p.add_argument("--source-ref", type=str, default="security_domain_exposure_scores.md", help="Audit source_ref.")
    p.add_argument("--dry-run", action="store_true", help="Parse + validate but do not write to DB.")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = get_env("DATABASE_URL")
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    as_of: date | None = None
    if args.as_of_date:
        as_of = date.fromisoformat(str(args.as_of_date))

    md_path = Path(args.scores_path)
    md_text = md_path.read_text(encoding="utf-8")
    exposure_rows = _parse_md_table(md_text)

    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute("select id, name from macro_domain order by id;")
            domain_id_by_name = {str(name): int(did) for did, name in cur.fetchall()}

            missing = sorted({dn for r in exposure_rows for dn in r.scores.keys()} - set(domain_id_by_name.keys()))
            if missing:
                raise SystemExit(f"Missing macro_domain rows for: {missing!r}")

            cur.execute("select id, company_name, ticker from bit_security order by id;")
            sec_ids_by_company: dict[str, list[int]] = {}
            for sid, cname, _ticker in cur.fetchall():
                sec_ids_by_company.setdefault(str(cname), []).append(int(sid))

        to_upsert: list[dict[str, object]] = []
        affected_security_ids: set[int] = set()
        missing_companies: list[str] = []

        for r in exposure_rows:
            sec_ids = sec_ids_by_company.get(r.company_name) or []
            if not sec_ids:
                missing_companies.append(r.company_name)
                continue
            weights = _normalize_scores_to_weights(r.scores)
            for sid in sec_ids:
                affected_security_ids.add(int(sid))
                for dom_name, w in weights.items():
                    to_upsert.append(
                        {
                            "security_id": int(sid),
                            "macro_domain_id": int(domain_id_by_name[dom_name]),
                            "weight": float(w),
                            "weight_basis": "custom",
                            "source_ref": str(args.source_ref),
                            "as_of_date": as_of,
                        }
                    )

        if missing_companies:
            raise SystemExit(
                "Company names in markdown not found in `bit_security.company_name`: "
                + ", ".join(sorted(missing_companies))
            )

        log.info(
            "Parsed %s company rows -> %s securities -> %s exposure rows",
            len(exposure_rows),
            len(affected_security_ids),
            len(to_upsert),
        )

        if args.dry_run:
            print({"dry_run": True, "securities": len(affected_security_ids), "rows": len(to_upsert)})
            return

        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "delete from bit_security_macro_domain_exposure where security_id = any(%s);",
                    (sorted(affected_security_ids),),
                )
                cur.executemany(
                    """
                    insert into bit_security_macro_domain_exposure (
                      security_id, macro_domain_id, weight, weight_basis, source_ref, as_of_date, created_at, updated_at
                    ) values (
                      %(security_id)s, %(macro_domain_id)s, %(weight)s, %(weight_basis)s, %(source_ref)s, %(as_of_date)s, now(), now()
                    )
                    on conflict (security_id, macro_domain_id) do update set
                      weight = excluded.weight,
                      weight_basis = excluded.weight_basis,
                      source_ref = excluded.source_ref,
                      as_of_date = excluded.as_of_date,
                      updated_at = now();
                    """,
                    to_upsert,
                )

        print({"securities_updated": len(affected_security_ids), "rows_upserted": len(to_upsert)})
    finally:
        conn.close()


if __name__ == "__main__":
    main()

