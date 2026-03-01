#!/bin/zsh
set -euo pipefail

LA_DIR="$HOME/Library/LaunchAgents"

uninstall_one() {
  local label="$1"
  local dest="$2"
  launchctl bootout "gui/$UID" "$dest" >/dev/null 2>&1 || true
  rm -f "$dest"
  echo "Removed: $label"
}

uninstall_one "com.bit.polymarket_refresh" "$LA_DIR/com.bit.polymarket_refresh.plist"
uninstall_one "com.bit.daily_snapshot" "$LA_DIR/com.bit.daily_snapshot.plist"

echo "Done."

