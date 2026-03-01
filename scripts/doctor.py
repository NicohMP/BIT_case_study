#!/usr/bin/env python3
"""Reviewer-facing sanity checks for local setup.

Run:
  ./venv/bin/python scripts/doctor.py
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_env_fallback(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def _print_kv(key: str, value: str, *, ok: bool | None = None) -> None:
    status = "OK" if ok is True else ("WARN" if ok is False else "INFO")
    print(f"[{status}] {key}: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Local setup checks (DB, env, deps).")
    parser.add_argument("--no-db", action="store_true", help="Skip database connectivity checks.")
    args = parser.parse_args()

    _print_kv("cwd", str(Path.cwd()))
    _print_kv("python", sys.version.splitlines()[0])

    if sys.version_info < (3, 11):
        _print_kv("python_version", "Expected Python 3.11+ (repo tested on newer versions).", ok=False)

    env_path = ROOT / ".env"
    _print_kv(".env", "present" if env_path.exists() else "missing (copy from .env.example)", ok=env_path.exists())

    # Prefer project loader if available; fall back to a tiny .env parser.
    try:
        from polyscanner.env import load_env  # type: ignore
    except Exception:
        load_env = None

    if load_env is not None:
        try:
            load_env()
        except Exception as e:
            _print_kv("load_env", f"failed: {e}", ok=False)
    else:
        _load_env_fallback(env_path)

    db_url = (os.environ.get("DATABASE_URL") or "").strip()
    if not db_url:
        _print_kv("DATABASE_URL", "missing", ok=False)
        _print_kv("hint", "Set DATABASE_URL in .env (Supabase local default is in .env.example).")
        return 2
    _print_kv("DATABASE_URL", "set", ok=True)

    if shutil.which("supabase"):
        _print_kv("supabase", "found", ok=True)
    else:
        _print_kv("supabase", "not found (optional; needed for `supabase start/db reset`)", ok=False)

    if shutil.which("docker"):
        _print_kv("docker", "found", ok=True)
    else:
        _print_kv("docker", "not found (optional; needed for ops/docker scheduler)", ok=False)

    # Web UI dependency: FastAPI requires python-multipart for form handling.
    try:
        import multipart  # type: ignore

        _print_kv("python-multipart", "installed", ok=True)
    except Exception:
        _print_kv("python-multipart", "missing (needed for Web UI forms)", ok=False)
        _print_kv("hint", "Install deps with `./venv/bin/pip install -r requirements.txt`.", ok=None)

    if args.no_db:
        return 0

    try:
        import psycopg  # type: ignore
    except Exception as e:
        _print_kv("psycopg", f"not importable: {e}", ok=False)
        _print_kv("hint", "Run `bash scripts/bootstrap.sh` (or install requirements.txt).")
        return 2

    try:
        with psycopg.connect(db_url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("select 1;")
                cur.fetchone()
    except Exception as e:
        _print_kv("db_connect", f"failed: {e}", ok=False)
        _print_kv("hint", "If using Supabase local: run `supabase start` then `supabase db reset`.", ok=None)
        return 2

    _print_kv("db_connect", "ok", ok=True)

    to_check = [
        ("pm_pipeline_run", "table"),
        ("pm_event", "table"),
        ("pm_market", "table"),
        ("pm_market_filter_decision", "table"),
        ("pm_market_signal_family_match", "table"),
        ("pm_market_security_relevance", "table"),
        ("pm_market_security_relevance_selection", "table"),
        ("v_pm_market_kept_latest", "view"),
        ("v_pm_security_market_relevance_selected_latest", "view"),
    ]

    missing: list[str] = []
    have: set[str] = set()
    with psycopg.connect(db_url, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            for relname, reltype in to_check:
                cur.execute("select to_regclass(%s);", (f"public.{relname}",))
                exists = cur.fetchone()[0] is not None
                _print_kv(f"db_{reltype}", relname, ok=exists)
                if not exists:
                    missing.append(relname)
                else:
                    have.add(relname)

            if missing:
                _print_kv("migrations", f"missing relations: {', '.join(missing)}", ok=False)
                _print_kv("hint", "Apply migrations (recommended: `supabase db reset`).")
                return 2

            if "pm_pipeline_run" in have:
                cur.execute("select count(*) from pm_pipeline_run;")
                run_count = int(cur.fetchone()[0])
                _print_kv("pm_pipeline_run_count", str(run_count), ok=run_count > 0)

            cur.execute("select count(*) from pm_market;")
            market_count = int(cur.fetchone()[0])
            _print_kv("pm_market_count", str(market_count), ok=market_count > 0)

            cur.execute("select count(*) from v_pm_market_kept_latest;")
            kept_latest_count = int(cur.fetchone()[0])
            _print_kv("kept_latest_count", str(kept_latest_count), ok=kept_latest_count > 0)

            cur.execute("select count(*) from v_pm_security_market_relevance_selected_latest;")
            selected_latest_count = int(cur.fetchone()[0])
            _print_kv("selected_latest_count", str(selected_latest_count), ok=selected_latest_count > 0)

            if market_count == 0:
                _print_kv("hint", "DB is initialized but empty. Run `./venv/bin/python scripts/refresh_basic.py`.")
            elif kept_latest_count == 0 or selected_latest_count == 0:
                _print_kv("hint", "Refresh ran but produced no kept/selected markets. Check the latest `reports/pipeline_audit_*.md`.", ok=None)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
