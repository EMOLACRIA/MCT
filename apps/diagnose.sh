#!/usr/bin/env bash
# Read-only diagnostics: no account/prefs data, no cache removal.
set -u
base="${XDG_DATA_HOME:-$HOME/.local/share}/desktop-style-apps/spotify"
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
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
printf '%s\n' '--- Private theme verification (read-only) ---'
python3 -B - "$base" "$script_dir" <<'PY'
import importlib.util
import json
from pathlib import Path
import shutil
import sys

base=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('app_diagnostics',Path(sys.argv[2])/'manage.py')
apps=importlib.util.module_from_spec(spec);spec.loader.exec_module(apps)
try:
    info=json.loads((base/'versions.json').read_text())
    print('Private copy versions: Spotify '+info['spotify']+'; Spicetify '+info['spicetify'])
except (OSError,ValueError,KeyError,TypeError):
    print('Private copy versions: not recorded by the previous installer; installed package versions above do not identify this copy.')
try:
    spice=shutil.which('spicetify')
    if spice:apps.check_spotify_compatibility(apps.spotify_versions(spice))
except (RuntimeError,OSError) as exc:print('Compatibility: '+str(exc))
try:
    index=base/'client/Apps/xpui/index.html'
    tags=apps.ScriptTags();tags.feed(index.read_text())
    print('Startup scripts: '+', '.join(src.split('?')[0].rsplit('/',1)[-1] for src in tags.sources))
    print('Stylesheets: '+', '.join(src.split('?')[0].rsplit('/',1)[-1] for src in tags.stylesheets))
    apps.verify_spotify_theme(base/'client')
    print('Theme files: verified against this checkout (not a native UI/adblock test).')
except (RuntimeError,OSError) as exc:print('Theme files: '+str(exc))
PY
