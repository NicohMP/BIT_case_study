#!/usr/bin/env python3
"""Step 5c: Generate a security signal report via Gemini from a context pack.

This script:
- loads a deterministic context pack JSON
- validates it
- calls Gemini to produce a JSON report (no markdown)
- validates basic grounding constraints
- upserts the JSON into pm_security_signal_report
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.db.pg import connect  # noqa: E402
from polyscanner.db.security_signal_report import upsert_pm_security_signal_report  # noqa: E402
from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.llm.gemini import get_model  # noqa: E402
from polyscanner.llm.security_signal_report_v1 import PROMPT_VERSION, generate_security_signal_report_v1  # noqa: E402
from polyscanner.reporting.security_report_pack import hash_pack  # noqa: E402
from polyscanner.reporting.security_report_validation import validate_context_pack, validate_security_report_json  # noqa: E402


def _utc_ts() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _build_report_id(*, security_id: int, pack_hash: str, prompt_version: str, model: str) -> str:
    return _sha256(f"{security_id}:{pack_hash}:{prompt_version}:{model}")[:32]


def _ensure_meta_fields(*, report: dict[str, Any], pack: dict[str, Any], model: str) -> None:
    report.setdefault("as_of_utc", (pack.get("report_meta") or {}).get("as_of_utc"))
    report.setdefault("security", pack.get("security") or {})
    versions = report.get("versions")
    if not isinstance(versions, dict):
        versions = {}
    pack_versions = (pack.get("report_meta") or {}).get("versions") or {}
    # Always stamp authoritative meta from our runner, even if the model filled placeholders like "string".
    versions["run_id"] = (pack.get("report_meta") or {}).get("run_id")
    for k in ("filter_version", "matcher_version", "scoring_version", "selection_version"):
        if k in pack_versions and pack_versions.get(k) is not None:
            versions[k] = pack_versions.get(k)
    versions["prompt_version"] = PROMPT_VERSION
    versions["model"] = model
    report["versions"] = versions


def main() -> None:
    p = argparse.ArgumentParser(description="Generate Step-5 security signal report JSON via Gemini.")
    p.add_argument("--pack", type=str, required=True, help="Path to context pack JSON.")
    p.add_argument("--out", type=str, default=None, help="Output report JSON path (default: reports/security_report_*.json).")
    p.add_argument("--model", type=str, default=None, help="Gemini model name (default GEMINI_MODEL/LLM_MODEL).")
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--max-markets", type=int, default=10)
    p.add_argument("--max-rate-like", type=int, default=3)
    p.add_argument("--persist", type=str, default="true", help="true/false to upsert into Postgres.")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    load_env()
    db_url = (get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    pack_path = Path(args.pack)
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    pack_issues = validate_context_pack(pack)
    pack_errors = [x for x in pack_issues if x.level == "error"]
    if pack_errors:
        for e in pack_errors:
            loc = f" ({e.path})" if e.path else ""
            logging.error("Invalid pack: %s%s", e.message, loc)
        raise SystemExit(2)

    model = args.model or get_model()
    report = generate_security_signal_report_v1(
        pack=pack,
        model=model,
        temperature=float(args.temperature),
        max_markets=int(args.max_markets),
        max_rate_like=int(args.max_rate_like),
    )
    report.pop("_raw", None)  # avoid persisting huge raw HTTP response
    _ensure_meta_fields(report=report, pack=pack, model=model)

    rep_issues = validate_security_report_json(report, pack=pack)
    rep_errors = [x for x in rep_issues if x.level == "error"]
    for it in rep_issues:
        loc = f" ({it.path})" if it.path else ""
        lvl = logging.ERROR if it.level == "error" else logging.WARNING
        logging.log(lvl, "Report issue: %s%s", it.message, loc)
    if rep_errors:
        raise SystemExit(3)

    out = args.out
    if not out:
        sec = pack.get("security") or {}
        ticker = str(sec.get("ticker") or "SEC")
        out = str(Path("reports") / f"security_signal_report_{ticker}_{_utc_ts()}.json")
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    do_persist = str(args.persist).strip().lower() in {"1", "true", "t", "yes", "y", "on"}
    rows_upserted = 0
    report_id = None
    if do_persist:
        pack_hash = (pack.get("report_meta") or {}).get("pack_sha256") or hash_pack(pack)
        sec = pack.get("security") or {}
        security_id = int(sec.get("security_id"))
        report_id = _build_report_id(security_id=security_id, pack_hash=str(pack_hash), prompt_version=PROMPT_VERSION, model=model)
        pv = (pack.get("report_meta") or {}).get("versions") or {}
        conn = connect(db_url)
        try:
            upsert_pm_security_signal_report(
                conn,
                report_id=str(report_id),
                run_id=(pack.get("report_meta") or {}).get("run_id"),
                security_id=int(security_id),
                filter_version=pv.get("filter_version"),
                matcher_version=pv.get("matcher_version"),
                scoring_version=str(pv.get("scoring_version") or ""),
                selection_version=str(pv.get("selection_version") or ""),
                prompt_version=PROMPT_VERSION,
                model=str(model),
                context_pack_hash=str(pack_hash),
                report_json=report,
                report_md=None,
            )
            rows_upserted = 1
        finally:
            conn.close()

    print(
        "security_signal_report:",
        {
            "out_path": str(out_path),
            "persisted": bool(do_persist),
            "rows_upserted": rows_upserted,
            "report_id": report_id,
            "prompt_version": PROMPT_VERSION,
            "model": model,
        },
    )


if __name__ == "__main__":
    main()
