#!/usr/bin/env python3
"""Seed signal_family_domain_influence scores + rationales from markdown authority files.

Source-of-truth files:
- event_domain_scores.md: influence scores (0..5) matrix
- event_domain_rationale.md: rationale text per (family, domain) cell

This script makes Step 5 reports materially better by populating
signal_family_domain_influence.rationale_md so the LLM can cite the "why"
in the Market → Family → Domain → Stock chain.
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.db.pg import connect  # noqa: E402
from polyscanner.env import get_env, load_env  # noqa: E402


def _parse_md_table_row(line: str) -> list[str]:
    # Expect: | col1 | col2 | ... |
    return [p.strip() for p in line.strip().strip("|").split("|")]


def _load_md_table(*, md_path: str) -> tuple[list[str], list[list[str]]]:
    p = Path(md_path)
    if not p.exists():
        raise FileNotFoundError(f"Missing file: {md_path}")
    lines = p.read_text(encoding="utf-8").splitlines()

    header_idx = None
    for i, ln in enumerate(lines[:40]):
        if ln.strip().startswith("|") and "Signal family" in ln:
            header_idx = i
            break
    if header_idx is None:
        raise RuntimeError(f"Could not find markdown table header in {md_path}")
    if header_idx + 2 >= len(lines):
        raise RuntimeError(f"Malformed markdown table in {md_path}")

    headers = _parse_md_table_row(lines[header_idx])
    rows: list[list[str]] = []
    for ln in lines[header_idx + 2 :]:
        if not ln.strip().startswith("|"):
            continue
        cols = _parse_md_table_row(ln)
        if len(cols) != len(headers):
            continue
        rows.append(cols)
    return headers, rows


@dataclass(frozen=True)
class InfluenceCell:
    family_title: str
    domain_name: str
    score: int


@dataclass(frozen=True)
class RationaleCell:
    family_title: str
    domain_name: str
    rationale_md: str


def _load_scores(*, md_path: str) -> dict[tuple[str, str], int]:
    headers, rows = _load_md_table(md_path=md_path)
    # Expect columns: #, Signal family, <domains...>
    if len(headers) < 3:
        raise RuntimeError(f"Unexpected score table header: {headers}")
    domain_headers = headers[2:]

    out: dict[tuple[str, str], int] = {}
    for cols in rows:
        family = cols[1].strip()
        if not family:
            continue
        for j, dom in enumerate(domain_headers, start=2):
            raw = (cols[j] or "").strip()
            if raw == "":
                continue
            try:
                score = int(raw)
            except ValueError:
                continue
            out[(family, dom)] = score
    return out


def _load_rationales(*, md_path: str) -> dict[tuple[str, str], str]:
    headers, rows = _load_md_table(md_path=md_path)
    if len(headers) < 3:
        raise RuntimeError(f"Unexpected rationale table header: {headers}")
    domain_headers = headers[2:]

    out: dict[tuple[str, str], str] = {}
    for cols in rows:
        family = cols[1].strip()
        if not family:
            continue
        for j, dom in enumerate(domain_headers, start=2):
            rat = (cols[j] or "").strip()
            out[(family, dom)] = rat
    return out


def _fetch_macro_domain_ids(conn) -> dict[str, int]:
    with conn.cursor() as cur:
        cur.execute("select id, name from macro_domain;")
        rows = cur.fetchall()
    return {str(name): int(i) for i, name in rows}


def _fetch_signal_family_ids(conn) -> dict[str, int]:
    with conn.cursor() as cur:
        cur.execute("select id, title from signal_family;")
        rows = cur.fetchall()
    return {str(title): int(i) for i, title in rows}


def main() -> None:
    p = argparse.ArgumentParser(description="Seed signal_family_domain_influence rationales from markdown authority.")
    p.add_argument("--scores-md", type=str, default="event_domain_scores.md")
    p.add_argument("--rationale-md", type=str, default="event_domain_rationale.md")
    p.add_argument("--only-missing", type=str, default="true", help="If true, only fill rows where rationale_md is empty.")
    p.add_argument("--dry-run", type=str, default="false", help="If true, do not write to DB.")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    def as_bool(x: str) -> bool:
        return (x or "").strip().lower() in {"1", "true", "t", "yes", "y", "on"}

    only_missing = as_bool(args.only_missing)
    dry_run = as_bool(args.dry_run)

    load_env()
    db_url = (get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    scores = _load_scores(md_path=str(args.scores_md))
    rats = _load_rationales(md_path=str(args.rationale_md))

    conn = connect(db_url)
    try:
        dom_id = _fetch_macro_domain_ids(conn)
        fam_id = _fetch_signal_family_ids(conn)

        missing_fams = sorted({f for (f, _) in rats.keys() if f not in fam_id})
        missing_doms = sorted({d for (_, d) in rats.keys() if d not in dom_id})
        if missing_fams:
            logging.warning("Missing signal_family titles in DB: %s", missing_fams[:20])
        if missing_doms:
            logging.warning("Missing macro_domain names in DB: %s", missing_doms[:20])

        upserts = 0
        skips = 0
        no_score = 0

        with conn.cursor() as cur:
            for (family, domain), rat in rats.items():
                if family not in fam_id or domain not in dom_id:
                    continue
                sfid = fam_id[family]
                did = dom_id[domain]
                score = scores.get((family, domain))
                if score is None:
                    no_score += 1
                    score = 0

                if only_missing:
                    cur.execute(
                        """
                        select rationale_md
                        from signal_family_domain_influence
                        where signal_family_id = %s and macro_domain_id = %s;
                        """,
                        (sfid, did),
                    )
                    row = cur.fetchone()
                    if row and (row[0] or "").strip():
                        skips += 1
                        continue

                if dry_run:
                    upserts += 1
                    continue

                cur.execute(
                    """
                    insert into signal_family_domain_influence (
                      signal_family_id,
                      macro_domain_id,
                      score,
                      rationale_md
                    )
                    values (%s,%s,%s,%s)
                    on conflict (signal_family_id, macro_domain_id)
                    do update set
                      score = excluded.score,
                      rationale_md = excluded.rationale_md,
                      updated_at = now();
                    """,
                    (sfid, did, int(score), str(rat or "")),
                )
                upserts += 1

        if not dry_run:
            conn.commit()

        print(
            {
                "dry_run": dry_run,
                "only_missing": only_missing,
                "cells_in_rationale_file": len(rats),
                "cells_with_scores": len(scores),
                "rows_upserted": upserts,
                "rows_skipped_existing": skips,
                "cells_missing_score_defaulted_to_0": no_score,
            }
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()

