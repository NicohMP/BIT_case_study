#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found in PATH" >&2
  exit 1
fi

if [[ ! -d "venv" ]]; then
  python3 -m venv venv
fi

./venv/bin/python -m pip install --upgrade pip >/dev/null
./venv/bin/pip install -r requirements.txt

mkdir -p logs reports

if [[ ! -f ".env" ]]; then
  cp .env.example .env
  echo "Created .env from .env.example (edit DATABASE_URL / API keys as needed)."
fi

echo "Bootstrap complete."
echo "Next:"
echo "  ./venv/bin/python scripts/doctor.py"
echo "  supabase start && supabase db reset   # if using Supabase local"
echo "  ./venv/bin/python scripts/refresh_basic.py"
