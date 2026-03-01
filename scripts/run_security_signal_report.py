#!/usr/bin/env python3
"""One-command Step-5 demo runner (pack → report → audit → markdown).

This script is meant for reviewer-friendly local demos:
- Builds and validates a deterministic context pack from the DB for a ticker
- Tries Gemini first (if available), and falls back to Ollama (local) on failure
- Audits grounding and renders analyst markdown
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polyscanner.env import get_env, load_env  # noqa: E402
from polyscanner.reporting.security_report_pack import build_security_context_pack  # noqa: E402
from polyscanner.reporting.security_report_validation import validate_context_pack  # noqa: E402


def _utc_ts() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")


def _run(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    subprocess.run(cmd, check=True, env=env)


def main() -> None:
    p = argparse.ArgumentParser(description="Run Step 5 end-to-end for one ticker (pack → LLM → audit → markdown).")
    p.add_argument("--ticker", type=str, required=True)
    p.add_argument("--exchange-mic", type=str, default=None)
    p.add_argument("--out-dir", type=str, default="reports")

    # Pack sizing
    p.add_argument("--top-k-markets", type=int, default=20)
    p.add_argument("--top-k-matches-per-market", type=int, default=5)

    # LLM generation parameters (passed through to generate_security_signal_report.py)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--timeout-s", type=int, default=180)
    p.add_argument("--max-retries", type=int, default=6)
    p.add_argument("--retry-base-s", type=float, default=1.5)
    p.add_argument("--retry-max-s", type=float, default=120.0)
    p.add_argument("--max-markets", type=int, default=10)
    p.add_argument("--max-rate-like", type=int, default=3)

    # Optional override: force a backend/model (otherwise: gemini → ollama fallback)
    p.add_argument("--backend", type=str, default=None, help="gemini|ollama (default: try gemini, then ollama).")
    p.add_argument("--model", type=str, default=None, help="Model name (backend-specific).")
    args = p.parse_args()

    load_env()
    db_url = (get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise SystemExit("Missing DATABASE_URL in environment/.env")

    out_dir = Path(str(args.out_dir))
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = _utc_ts()
    ticker = str(args.ticker).strip().upper()

    # ---- Build + validate pack ----
    pack = build_security_context_pack(
        db_url=db_url,
        ticker=ticker,
        exchange_mic=str(args.exchange_mic) if args.exchange_mic else None,
        top_k_markets=max(int(args.top_k_markets), int(args.max_markets)),
        top_k_matches_per_market=int(args.top_k_matches_per_market),
    )
    pack_path = out_dir / f"context_pack_{ticker}_{stamp}.json"
    pack_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")

    issues = validate_context_pack(pack)
    errors = [x for x in issues if x.level == "error"]
    if errors:
        for it in errors:
            loc = f" ({it.path})" if it.path else ""
            print(f"[ERROR] {it.message}{loc}")
        raise SystemExit(2)

    # ---- Generate report (Gemini → Ollama fallback) ----
    gen_cmd = [
        sys.executable,
        str(ROOT / "scripts" / "generate_security_signal_report.py"),
        "--pack",
        str(pack_path),
        "--temperature",
        str(float(args.temperature)),
        "--timeout-s",
        str(int(args.timeout_s)),
        "--max-retries",
        str(int(args.max_retries)),
        "--retry-base-s",
        str(float(args.retry_base_s)),
        "--retry-max-s",
        str(float(args.retry_max_s)),
        "--max-markets",
        str(int(args.max_markets)),
        "--max-rate-like",
        str(int(args.max_rate_like)),
    ]

    report_path = out_dir / f"security_signal_report_{ticker}_{stamp}.json"
    gen_cmd += ["--out", str(report_path)]

    forced_backend = str(args.backend).strip().lower() if args.backend else None
    forced_model = str(args.model).strip() if args.model else None

    if forced_backend:
        gen_env = os.environ.copy()
        gen_cmd += ["--backend", forced_backend]
        if forced_model:
            gen_cmd += ["--model", forced_model]
        _run(gen_cmd, env=gen_env)
    else:
        # Try Gemini first; if it fails (commonly 429), fallback to Ollama for offline demos.
        try:
            _run(gen_cmd + ["--backend", "gemini"], env=os.environ.copy())
        except subprocess.CalledProcessError:
            fallback_path = out_dir / f"security_signal_report_{ticker}_{stamp}_ollama.json"
            fallback_cmd = list(gen_cmd)
            fallback_cmd[fallback_cmd.index("--out") + 1] = str(fallback_path)
            fallback_cmd += ["--backend", "ollama"]
            _run(fallback_cmd, env=os.environ.copy())
            report_path = fallback_path

    # ---- Audit grounding + render markdown ----
    audit_path = out_dir / f"security_signal_report_audit_{ticker}_{stamp}.md"
    _run(
        [
            sys.executable,
            str(ROOT / "scripts" / "audit_security_signal_report.py"),
            "--pack",
            str(pack_path),
            "--report-json",
            str(report_path),
            "--max-markets",
            str(int(args.max_markets)),
            "--max-rate-like",
            str(int(args.max_rate_like)),
            "--out",
            str(audit_path),
        ]
    )

    md_path = out_dir / f"security_signal_report_{ticker}_{stamp}.md"
    _run(
        [
            sys.executable,
            str(ROOT / "scripts" / "render_security_signal_report_md.py"),
            "--report-json",
            str(report_path),
            "--out",
            str(md_path),
        ]
    )

    print(
        {
            "pack_json": str(pack_path),
            "report_json": str(report_path),
            "audit_md": str(audit_path),
            "report_md": str(md_path),
        }
    )


if __name__ == "__main__":
    main()

