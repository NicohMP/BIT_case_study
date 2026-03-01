#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT/ops/docker"

if [[ ! -f "$ROOT/.env" ]]; then
  echo "ERROR: missing $ROOT/.env (copy from .env.example and set DATABASE_URL)" >&2
  exit 1
fi

mkdir -p "$ROOT/logs" "$ROOT/reports"

docker compose -f docker-compose.yml up -d --build

echo "Scheduled refresh is running (Docker)."
echo "Logs:"
echo "  cd ops/docker && docker compose logs -f refresh_scheduler"
echo "Stop:"
echo "  cd ops/docker && docker compose down"

