#!/usr/bin/env bash
set -euo pipefail

_iso_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

_bool() {
  local v="${1:-}"
  v="$(echo "$v" | tr '[:upper:]' '[:lower:]' | xargs)"
  [[ "$v" == "1" || "$v" == "true" || "$v" == "t" || "$v" == "yes" || "$v" == "y" || "$v" == "on" ]]
}

_fix_database_url_for_docker() {
  if [[ -z "${DATABASE_URL:-}" ]]; then
    echo "ERROR: DATABASE_URL is not set" >&2
    return 1
  fi
  DATABASE_URL="$(
    python - <<'PY'
import os
from urllib.parse import urlparse, urlunparse

u = (os.environ.get("DATABASE_URL") or "").strip()
p = urlparse(u)
host = p.hostname or ""
if host not in {"127.0.0.1", "localhost"}:
    print(u)
    raise SystemExit(0)

username = p.username or ""
password = p.password or ""
port = p.port
netloc = ""
if username:
    netloc += username
    if password:
        netloc += ":" + password
    netloc += "@"
netloc += "host.docker.internal"
if port:
    netloc += ":" + str(port)

fixed = urlunparse((p.scheme, netloc, p.path, p.params, p.query, p.fragment))
print(fixed)
PY
  )"
  export DATABASE_URL
  return 0
}

INTERVAL_SECONDS="${REFRESH_INTERVAL_SECONDS:-7200}"
INGEST_MAX_PAGES="${REFRESH_INGEST_MAX_PAGES:-200}"
MATCHER_VERSION="${REFRESH_MATCHER_VERSION:-matcher_v10}"
SCORING_VERSION="${REFRESH_SCORING_VERSION:-relevance_v5}"
SELECTION_VERSION="${REFRESH_SELECTION_VERSION:-selected_v1}"
USE_EMBEDDINGS="${REFRESH_USE_EMBEDDINGS:-true}"
TRUSTED_ONLY="${REFRESH_TRUSTED_ONLY:-true}"
RUN_AUDIT="${REFRESH_RUN_AUDIT:-false}"
RECORD_DAILY="${REFRESH_RECORD_DAILY_SNAPSHOTS:-true}"
SNAPSHOT_SCOPE="${REFRESH_SNAPSHOT_SCOPE:-kept}"
DB_LOCK="${REFRESH_DB_LOCK:-try}"
DB_LOCK_KEY="${REFRESH_DB_LOCK_KEY:-913274001}"
FAIL_FAST="${REFRESH_FAIL_FAST:-false}"

echo "[$(_iso_utc)] refresh_scheduler: starting"
echo "[$(_iso_utc)] refresh_scheduler: interval_seconds=${INTERVAL_SECONDS} use_embeddings=${USE_EMBEDDINGS} record_daily_snapshots=${RECORD_DAILY} db_lock=${DB_LOCK}"

_fix_database_url_for_docker

trap 'echo "[$(_iso_utc)] refresh_scheduler: received signal, exiting"; exit 0' INT TERM

while true; do
  echo "[$(_iso_utc)] refresh_scheduler: running refresh"

  set +e
  python scripts/run_polymarket_refresh.py \
    --ingest-max-pages "${INGEST_MAX_PAGES}" \
    --matcher-version "${MATCHER_VERSION}" \
    --scoring-version "${SCORING_VERSION}" \
    --selection-version "${SELECTION_VERSION}" \
    --use-embeddings "${USE_EMBEDDINGS}" \
    --trusted-only "${TRUSTED_ONLY}" \
    --record-daily-snapshots "${RECORD_DAILY}" \
    --snapshot-scope "${SNAPSHOT_SCOPE}" \
    --run-audit "${RUN_AUDIT}" \
    --db-lock "${DB_LOCK}" \
    --db-lock-key "${DB_LOCK_KEY}"
  ec=$?
  set -e

  if [[ $ec -ne 0 ]]; then
    echo "[$(_iso_utc)] refresh_scheduler: refresh failed (exit_code=$ec)" >&2
    if _bool "${FAIL_FAST}"; then
      exit "$ec"
    fi
  else
    echo "[$(_iso_utc)] refresh_scheduler: refresh ok"
  fi

  echo "[$(_iso_utc)] refresh_scheduler: sleeping ${INTERVAL_SECONDS}s"
  sleep "${INTERVAL_SECONDS}" || exit 0
done
