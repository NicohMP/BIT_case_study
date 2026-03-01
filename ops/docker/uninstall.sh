#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT/ops/docker"

docker compose -f docker-compose.yml down --remove-orphans

