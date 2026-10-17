#!/usr/bin/env python3
"""Local, reversible desktop configuration installer. No downloads or sudo."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import importlib.util
import tempfile
import re
from datetime import datetime

PACKAGE = Path(__file__).resolve().parent
BASE = Path.home()
STYLE = BASE / '.config/desktop-style'
STATE = BASE / '.local/state/desktop-style'
HYPR = BASE / '.config/hypr'
TARGETS = ['appearance.lua', 'autostart.lua', 'keybinds.lua', 'misc.lua', 'hyprpaper.conf', 'hyprlock.conf']
REQUIRED = ['hyprctl', 'kitty', 'hyprlock', 'hyprpaper', 'brightnessctl', 'wpctl', 'quickshell', 'busctl', 'gio']

def run(args):
    return subprocess.run(args, text=True, capture_output=True, timeout=15)

def check_quickshell():
    version = run(['quickshell','--version'])
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', version.stdout + version.stderr)
    if version.returncode or not match or tuple(map(int,match.groups())) < (0,3,1):
        raise RuntimeError('QuickShell 0.3.1 or newer is required.')
    result = run(['quickshell','-p',str(PACKAGE/'payload/style/shell/validate.qml')])
    if result.returncode:
        raise RuntimeError('QuickShell rejected the new QML before installation:\n'+result.stdout+result.stderr)

def check():
    if os.geteuid() == 0:
        raise RuntimeError('Run as your normal desktop user; do not use sudo.')
    missing = [cmd for cmd in REQUIRED if shutil.which(cmd) is None]
    if missing:
        raise RuntimeError('Missing commands: ' + ', '.join(missing))
    if not os.environ.get('HYPRLAND_INSTANCE_SIGNATURE'):
        raise RuntimeError('Run from a terminal inside your active Hyprland session.')
    result = run(['hyprctl', 'version'])
    if result.returncode or '0.56.2' not in result.stdout:
        raise RuntimeError('This package targets the supplied Hyprland 0.56.2 Lua configuration.')
    baseline = run(['hyprctl', 'configerrors'])
    if baseline.returncode or baseline.stdout.strip():
        raise RuntimeError('Resolve existing Hyprland config errors first:\n' + baseline.stdout + baseline.stderr)
    expected = json.loads((PACKAGE/'expected.json').read_text())
    for name, digest in expected.items():
        file = HYPR/name
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise RuntimeError('Live configuration differs from the supplied archive: ' + str(file) + '\nNothing was changed. Send the current file so the package can be updated.')
    # File links and linked app folders are detached locally, never written through.
    if (BASE/'.config').is_symlink():
        raise RuntimeError('The entire .config directory is linked; this requires a separate installation layout.')
    for directory in [HYPR, BASE/'.config/kitty']:
        if directory.is_symlink() and not directory.is_dir():
            raise RuntimeError('Broken directory link: ' + str(directory))
    if STYLE.exists() or STYLE.is_symlink():
        raise RuntimeError(str(STYLE) + ' already exists. Restore the previous installation before installing again.')
    if '"' in str(BASE) or '\n' in str(BASE) or '\\' in str(BASE):
        raise RuntimeError('Unsupported characters in home directory.')
    for config in (PACKAGE/'payload/style').rglob('*.json'):
        json.loads(config.read_text())
    check_quickshell()
    print('Preflight passed: Lua configuration and required programs match.')

def load_session(file):
    spec = importlib.util.spec_from_file_location('desktop_session', file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def backup():
    dest = STATE/'backups'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    dest.mkdir(parents=True, mode=0o700)
    records = []
    for index, path in enumerate([*[HYPR/n for n in TARGETS], BASE/'.config/kitty/kitty.conf']):
        exists = path.exists()
        item = {'path': str(path), 'exists': exists, 'copy': str(index),
                'link': os.readlink(path) if path.is_symlink() else None}
        if exists:
            shutil.copy2(path, dest/str(index))
        records.append(item)
    directories = [{'path': str(path), 'link': os.readlink(path) if path.is_symlink() else None}
                   for path in [HYPR, BASE/'.config/kitty']]
    metadata = {'files': records, 'directories': directories, 'style': str(STYLE), 'status': 'prepared'}
    (dest/'manifest.json').write_text(json.dumps(metadata, indent=2))
    return dest, metadata

def replace_text(path, text, mode=None):
    replace_bytes(path, text.encode(), mode)

def replace_bytes(path, data, mode=None):
    """Replace the directory entry, rather than following a file symlink."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode is None:
        mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, 'wb') as output:
            output.write(data)
        temporary.chmod(mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)

def detach_directories(metadata):
    for item in metadata.get('directories', []):
        if item.get('link') is None:
            continue
        path = Path(item['path'])
        with tempfile.TemporaryDirectory(prefix='.desktop-style-stage-', dir=path.parent) as td:
            clone = Path(td)/'copy'
            shutil.copytree(path, clone, symlinks=True)
            # Relative links inside the source folder refer to its original location.
            # Resolve copied links there before moving the clone to .config.
            for copied in clone.rglob('*'):
                if copied.is_symlink():
                    target = (path/copied.relative_to(clone)).resolve()
                    copied.unlink()
                    copied.symlink_to(target)
            path.unlink()
            os.replace(clone, path)

def restore_files(dest, metadata):
    linked_dirs = [Path(i['path']) for i in metadata.get('directories', []) if i.get('link') is not None]
    for item in metadata.get('directories', []):
        if item.get('link') is None:
            continue
        path = Path(item['path'])
        if path.is_symlink():
            path.unlink()
        elif path.exists():
            shutil.rmtree(path)
        path.symlink_to(item['link'])
    for item in metadata['files']:
        path = Path(item['path'])
        if any(parent in path.parents for parent in linked_dirs):
            continue  # The original linked folder and its contents were never edited.
        if item.get('link') is not None:
            path.unlink(missing_ok=True)
            path.symlink_to(item['link'])
        elif item['exists']:
            snapshot = dest/item['copy']
            replace_bytes(path, snapshot.read_bytes(), snapshot.stat().st_mode & 0o777)
        else:
            path.unlink(missing_ok=True)
    if STYLE.exists():
        shutil.rmtree(STYLE)

def launch_original(session, metadata):
    commands = metadata.get('processes', [['hyprpaper'], ['quickshell', '-p', session.OLD_SHELL]])
    running = [args for _, args in session.processes()]
    for args in commands:
        if args not in running:
            session.launch(args, 'restore-' + Path(args[0]).name + '.log')

def install(check_only=False):
    check()
    if check_only:
        return
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    session = load_session(PACKAGE/'payload/style/scripts/session.py')
    dest, metadata = backup()
    print('Backup: ' + str(dest))
    stopped = False
    written = False
    metadata['processes'] = [args for _, args in session.processes() if Path(args[0]).name in {'waybar', 'dunst', 'hyprpaper'} or (Path(args[0]).name in {'qs', 'quickshell'} and session.OLD_SHELL in args)]
    metadata['desktop_services'] = session.read_services()
    (dest/'manifest.json').write_text(json.dumps(metadata, indent=2))
    try:
        stopped = True
        session.suppress_services(metadata['desktop_services'])
        session.stop_ui()
        written = True
        detach_directories(metadata)
        shutil.copytree(PACKAGE/'payload/style', STYLE)
        # Absolute wallpaper paths; retain relative SVG paths inside CSS.
        for file in STYLE.rglob('*'):
            if file.is_file() and file.suffix in {'.json', '.conf', '.css'}:
                text = file.read_text()
                file.write_text(text.replace('@STYLE@', str(STYLE)))
        for name in TARGETS:
            replace_text(HYPR/name, (PACKAGE/'payload/hypr'/name).read_text().replace('@STYLE@', str(STYLE)))
        kitty = BASE/'.config/kitty/kitty.conf'
        kitty.parent.mkdir(parents=True, exist_ok=True)
        text = kitty.read_text() if kitty.exists() else ''
        replace_text(kitty, text.rstrip() + '\n\n# Desktop appearance\ninclude ' + str(STYLE/'kitty/theme.conf') + '\n')
        for script in (STYLE/'scripts').glob('*.sh'):
            script.chmod(0o755)
        result = run(['hyprctl', 'reload'])
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        errors = run(['hyprctl', 'configerrors'])
        if errors.returncode or errors.stdout.strip():
            raise RuntimeError('Hyprland rejected the configuration:\n' + errors.stdout + errors.stderr)
        session.launch(['hyprpaper'], 'hyprpaper.log')
        session.start()
        time.sleep(1)
        procs = [Path(args[0]).name for _, args in session.processes()]
        for exe in ['hyprpaper']:
            if exe not in procs:
                raise RuntimeError(exe + ' did not stay running. See ' + str(STATE/(exe+'.log')))
        if not session.feedback_ready():
            raise RuntimeError('Desktop shell readiness was lost after installation.')
        metadata['status'] = 'installed'
        (dest/'manifest.json').write_text(json.dumps(metadata, indent=2))
        (STATE/'current-backup').write_text(str(dest))
    except Exception:
        if written:
            try:
                session.stop_ui()
            finally:
                restore_files(dest, metadata)
                run(['hyprctl', 'reload'])
                if stopped:
                    session.restore_services(metadata.get('desktop_services',{}))
                    launch_original(session, metadata)
        elif stopped:
            session.restore_services(metadata.get('desktop_services',{}))
            launch_original(session, metadata)
        metadata['status'] = 'rolled-back'
        (dest/'manifest.json').write_text(json.dumps(metadata, indent=2))
        print('Original configuration restored. Backup: ' + str(dest), file=sys.stderr)
        raise
    print('Installed. Open a NEW terminal with Super+Q; open the menu with Super+R.')
    print('Restore: bash ' + str(PACKAGE/'restore.sh'))
    print('Diagnostics: hyprctl configerrors; logs in ' + str(STATE))

def restore():
    if os.geteuid() == 0:
        raise RuntimeError('Run as your normal desktop user; do not use sudo.')
    pointer = STATE/'current-backup'
    if not pointer.is_file():
        raise RuntimeError('No successful installation to restore.')
    dest = Path(pointer.read_text().strip())
    metadata = json.loads((dest/'manifest.json').read_text())
    session = load_session(PACKAGE/'payload/style/scripts/session.py')
    session.stop_ui()
    restore_files(dest, metadata)
    result = run(['hyprctl', 'reload'])
    session.restore_services(metadata.get('desktop_services',{}))
    launch_original(session, metadata)
    metadata['status'] = 'restored'
    (dest/'manifest.json').write_text(json.dumps(metadata, indent=2))
    pointer.unlink()
    if result.returncode:
        raise RuntimeError('Files restored; reload failed. Log out and in to load the original desktop.')
    print('Previous desktop restored. Backup retained: ' + str(dest))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['install', 'restore'])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        if args.action == 'install':
            install(args.check)
        else:
            restore()
    except Exception as exc:
        print('Stopped: ' + str(exc), file=sys.stderr)
        sys.exit(1)
