#!/bin/zsh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PYTHON="$REPO_ROOT/venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  echo "ERROR: venv python not found at: $PYTHON" >&2
  echo "Create the venv first (or update ops/launchd/install.sh)." >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/logs"

LA_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$LA_DIR"

install_one() {
  local label="$1"
  local tmpl="$2"
  local dest="$3"

  sed \
    -e "s|__REPO_ROOT__|$REPO_ROOT|g" \
    -e "s|__PYTHON__|$PYTHON|g" \
    "$tmpl" > "$dest"

  # (Re)load for this user session (modern launchctl flow).
  launchctl bootout "gui/$UID" "$dest" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$UID" "$dest"
  launchctl kickstart -k "gui/$UID/$label" || true
}

install_one \
  "com.bit.polymarket_refresh" \
  "$REPO_ROOT/ops/launchd/com.bit.polymarket_refresh.plist.template" \
  "$LA_DIR/com.bit.polymarket_refresh.plist"

install_one \
  "com.bit.daily_snapshot" \
  "$REPO_ROOT/ops/launchd/com.bit.daily_snapshot.plist.template" \
  "$LA_DIR/com.bit.daily_snapshot.plist"

echo "Installed LaunchAgents:"
echo "- $LA_DIR/com.bit.polymarket_refresh.plist"
echo "- $LA_DIR/com.bit.daily_snapshot.plist"
echo ""
echo "Check status:"
echo "  launchctl list | rg 'com\\.bit\\.(polymarket_refresh|daily_snapshot)'"
echo "Tail logs:"
echo "  tail -f \"$REPO_ROOT/logs\"/*.log"

