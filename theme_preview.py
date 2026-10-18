#!/usr/bin/env python3
"""Compile a package into a disposable preview; never install or contact the live shell."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile
import sys
import theme_core


def stage(name, destination):
    engine = theme_core.Engine()
    manifest, files = engine.load(name)
    destination = Path(destination)
    shutil.copytree(theme_core.ROOT / 'payload/style', destination / 'style')
    for name, data in files.items():
        if name.startswith('style/'):
            path = theme_core.safe(destination, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    return destination / 'style/shell/preview.qml'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('theme')
    args = parser.parse_args()
    try:
        with tempfile.TemporaryDirectory(prefix='mct-theme-preview-') as folder:
            entry = stage(args.theme, folder)
            # Foreground child keeps assets alive until the preview exits.
            try:
                return subprocess.call(['quickshell', '-p', str(entry)])
            except KeyboardInterrupt:
                return 130
    except (theme_core.ThemeError, OSError) as exc:
        print('Stopped: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
