#!/usr/bin/env python3
"""Photo picker transport; all desktop changes remain owned by theme_core.Engine."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

import theme_core

ROOT = Path(__file__).resolve().parent


def catalog(engine):
    rows = []
    for folder in sorted((engine.root / 'themes').iterdir()):
        if not folder.is_dir():
            continue
        row = dict(id=folder.name, name=folder.name, version='', preview='', valid=False, error='')
        try:
            manifest, _ = engine.load(folder.name)
            row.update(name=manifest['name'], version=manifest['version'], valid=True,
                       preview=theme_core.safe(folder, manifest['preview']['source']).as_uri())
            if folder.name == 'deltarune':
                row['fontSource'] = theme_core.safe(folder, 'files/style/shell/assets/departure-mono.otf').as_uri()
        except (theme_core.ThemeError, OSError, ValueError) as exc:
            row['error'] = str(exc)
        rows.append(row)
    preferences = theme_core.load_module(ROOT / 'payload/style/scripts/preferences.py')
    try:
        values = preferences.read()
    except (OSError, ValueError):
        values = preferences.defaults()
    result = dict(themes=rows, active=None, canRollback=False, pending=False, stateError='',
                  reduceMotion=values['reduceMotion'], fontScale=values['fontScale'])
    try:
        active = engine.optional('active.json')
        if active is not None:
            if not isinstance(active.get('id'), str) or not isinstance(active.get('version'), str):
                raise theme_core.ThemeError('Invalid active theme record')
            result['active'] = dict(id=active['id'], version=active['version'])
        result['canRollback'] = engine.pointer() is not None
        result['pending'] = engine.optional('pending.json') is not None
    except (theme_core.ThemeError, OSError, ValueError) as exc:
        result['stateError'] = str(exc)
    return result


def dispatch(engine, action, theme=None):
    response = dict(action=action, theme=theme or '', ok=False, message='')
    try:
        if action == 'catalog':
            response['message'] = ''
        elif action == 'check':
            manifest = engine.check(theme)
            response['message'] = manifest['name'] + ' is ready. Apply to switch your desktop.'
        elif action == 'apply':
            transaction = engine.apply(theme)
            response['message'] = ('Desktop switched. Snapshot: ' + transaction if transaction
                                   else 'This theme is already active; no restart was needed.')
        elif action == 'rollback':
            # Same core validation/lease/snapshot path as the CLI, never a file-copy fallback.
            engine.rollback(check_only=True)
            transaction = engine.rollback()
            response['message'] = 'Previous desktop restored. Snapshot: ' + transaction
        else:
            raise theme_core.ThemeError('Unknown picker action')
        response['ok'] = True
    except (theme_core.ThemeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        response['message'] = str(exc)
    # Refresh after failure too: core recovery may have changed the active pointer.
    if action != 'check':
        try:
            response['catalog'] = catalog(engine)
        except (theme_core.ThemeError, OSError, ValueError) as exc:
            response['ok'] = False
            response['message'] += ('\n' if response['message'] else '') + str(exc)
    return response


def menu():
    quickshell = shutil.which('quickshell')
    if not quickshell:
        print('Stopped: QuickShell is required to open the theme rail.', file=sys.stderr)
        return 1
    path = str(ROOT / 'theme-picker/shell.qml')
    try:
        # Warm overlay: toggle the same layer immediately, without another app window.
        result = subprocess.run([quickshell, 'ipc', '-p', path, 'call', 'themes', 'toggle'],
                                capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            return 0
        return subprocess.call([quickshell, '--daemonize', '--no-duplicate', '-p', path])
    except (OSError, subprocess.SubprocessError) as exc:
        print('Stopped: ' + str(exc), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('menu', 'catalog', 'check', 'apply', 'rollback'))
    parser.add_argument('theme', nargs='?')
    args = parser.parse_args()
    if args.action in ('check', 'apply') and args.theme is None:
        parser.error('check/apply require a theme id')
    if args.action not in ('check', 'apply') and args.theme is not None:
        parser.error('this action does not accept a theme id')
    if args.action == 'menu':
        return menu()
    result = dispatch(theme_core.Engine(), args.action, args.theme)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
