#!/usr/bin/env bash
# Read-only diagnostics: no account/prefs data, no cache removal.
set -u
base="${XDG_DATA_HOME:-$HOME/.local/share}/desktop-style-apps/spotify"
printf '%s\n' '--- Application versions ---'
pacman -Q spotify spotify-adblock spicetify-cli dolphin qt6ct qt6ct-kde breeze-icons 2>/dev/null || true
printf '%s\n' '--- Spotify launcher commands ---'
python3 - <<'PY'
import os
from pathlib import Path
roots=[Path(os.environ.get('XDG_DATA_HOME',str(Path.home()/'.local/share')))/'applications',Path('/usr/share/applications')]
for root in roots:
 for path in sorted(root.glob('*spotify*.desktop')):
  print(path)
  for line in path.read_text().splitlines():
   if line.startswith(('Name=','Exec=','TryExec=','Hidden=')):print('  '+line)
PY
printf '%s\n' '--- Last private Spicetify apply ---'
tail -n 45 "$base/apply.log" 2>/dev/null || true
printf '%s\n' '--- Startup files ---'
for file in index.html xpui.js xpui-modules.js xpui-snapshot.js; do
  if [[ -f "$base/client/Apps/xpui/$file" ]]; then wc -c "$base/client/Apps/xpui/$file"; fi
done
