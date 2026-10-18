#!/usr/bin/env python3
"""Install only SDDM theme files and theme selection; never restart the display manager."""
import argparse
from datetime import datetime
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0,str(PACKAGE.parent))
import adapter_assets
THEME_SOURCE=None

def theme_source():return THEME_SOURCE or PACKAGE/'theme'
CONFIG = Path('/etc/sddm.conf')
THEMES = Path('/usr/share/sddm/themes')
THEME = THEMES/'desktop-style'
STATE = Path('/var/lib/desktop-style-sddm')
DISPLAY_MANAGER = Path('/etc/systemd/system/display-manager.service')

def theme_config(text):
    """Preserve other sections, comments and original line endings."""
    newline = '\r\n' if '\r\n' in text else '\n'
    lines = text.splitlines(keepends=True)
    starts = [i for i,line in enumerate(lines) if re.match(r'^\s*\[Theme\]\s*$',line.strip())]
    if len(starts) > 1:
        raise RuntimeError('Duplicate [Theme] sections require adaptation.')
    values = {'Current':'desktop-style', 'ThemeDir':str(THEMES)}
    if not starts:
        return text.rstrip('\r\n') + newline + newline + '[Theme]' + newline + ''.join(k+'='+v+newline for k,v in values.items())
    start = starts[0]+1
    end = next((i for i in range(start,len(lines)) if re.match(r'^\s*\[',lines[i])),len(lines))
    found = set()
    for i in range(start,end):
        match = re.match(r'^(\s*)(Current|ThemeDir)\s*=.*$',lines[i].rstrip('\r\n'))
        if match:
            key = match.group(2)
            lines[i] = match.group(1)+key+'='+values[key]+newline
            found.add(key)
    if end and lines[end-1] and not lines[end-1].endswith(('\n','\r')):
        lines[end-1] += newline
    lines[end:end] = [k+'='+v+newline for k,v in values.items() if k not in found]
    return ''.join(lines)

def atomic(path, data, mode=0o644):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.'+path.name+'-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as output:
            output.write(data)
        os.chmod(temporary,mode)
        os.replace(temporary,path)
    finally:
        Path(temporary).unlink(missing_ok=True)

def check():
    if os.geteuid() != 0:
        raise RuntimeError('Use sudo bash sddm/install.sh; SDDM settings are system files.')
    if DISPLAY_MANAGER.resolve().name != 'sddm.service':
        raise RuntimeError('The selected display manager is not SDDM. Nothing changed.')
    exe = shutil.which('sddm-greeter-qt6')
    if not exe:
        exe = shutil.which('sddm-greeter')
        if not exe:
            raise RuntimeError('SDDM Qt6 greeter is missing.')
        result = subprocess.run(['ldd',exe],capture_output=True,text=True,timeout=5)
        if result.returncode or 'libQt6' not in result.stdout:
            raise RuntimeError('This theme requires a Qt6 SDDM greeter.')
    for name in ['Main.qml','LoginSkin.qml','metadata.desktop','wallpaper.png','tl.svg','tr.svg','bl.svg','br.svg']:
        if not (theme_source()/name).is_file():
            raise RuntimeError('Missing theme file: '+name)
    if (STATE/'current-backup').exists():
        raise RuntimeError('SDDM theme is already installed. Restore it before reinstalling.')
    return theme_config(CONFIG.read_bytes().decode('utf-8',errors='surrogateescape') if CONFIG.exists() else '')

def remove_theme():
    if THEME.is_symlink():
        THEME.unlink()
    elif THEME.exists():
        shutil.rmtree(THEME)

def restore_snapshot(dest, metadata):
    if metadata['config_link'] is not None:
        CONFIG.unlink(missing_ok=True)
        CONFIG.symlink_to(metadata['config_link'])
    elif metadata['config_exists']:
        atomic(CONFIG,(dest/'sddm.conf').read_bytes(),metadata['config_mode'])
    else:
        CONFIG.unlink(missing_ok=True)
    remove_theme()
    if metadata['theme_link'] is not None:
        THEME.symlink_to(metadata['theme_link'])
    elif metadata['theme_exists']:
        shutil.copytree(dest/'theme',THEME,symlinks=True)

def install(check_only=False):
    text = check()
    if check_only:
        print('SDDM and Qt6 greeter found. No files changed.')
        return
    STATE.mkdir(parents=True,exist_ok=True,mode=0o700)
    with (STATE/'install.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
        text = check()
        dest = STATE/'backups'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        dest.mkdir(parents=True,mode=0o700)
        metadata = {'config_exists':CONFIG.exists(), 'config_link':os.readlink(CONFIG) if CONFIG.is_symlink() else None,
                    'config_mode':CONFIG.stat().st_mode & 0o777 if CONFIG.exists() else 0o644,
                    'theme_exists':THEME.exists(), 'theme_link':os.readlink(THEME) if THEME.is_symlink() else None}
        if CONFIG.exists():
            shutil.copy2(CONFIG,dest/'sddm.conf')
        if THEME.is_dir() and not THEME.is_symlink():
            shutil.copytree(THEME,dest/'theme',symlinks=True)
        (dest/'manifest.json').write_text(json.dumps(metadata,indent=2))
        try:
            THEMES.mkdir(parents=True,exist_ok=True,mode=0o755)
            with tempfile.TemporaryDirectory(prefix='.desktop-style-',dir=THEMES) as td:
                stage = Path(td)/'theme'
                shutil.copytree(theme_source(),stage)
                stage.chmod(0o755)
                for file in stage.rglob('*'):
                    file.chmod(0o755 if file.is_dir() else 0o644)
                remove_theme()
                os.replace(stage,THEME)
            atomic(CONFIG,text.encode('utf-8',errors='surrogateescape'))
            atomic(STATE/'current-backup',str(dest).encode(),0o600)
        except Exception:
            restore_snapshot(dest,metadata)
            raise
    print('SDDM theme installed; it will load on the next login screen.')
    print('Your active session was not restarted. Backup: '+str(dest))
    print('Restore: sudo bash '+str(PACKAGE/'restore.sh'))

def restore():
    if os.geteuid() != 0:
        raise RuntimeError('Use sudo bash sddm/restore.sh.')
    pointer = STATE/'current-backup'
    if not pointer.is_file():
        raise RuntimeError('No SDDM theme installation to restore.')
    with (STATE/'install.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
        dest = Path(pointer.read_text().strip())
        metadata = json.loads((dest/'manifest.json').read_text())
        restore_snapshot(dest,metadata)
        pointer.unlink()
    print('Previous SDDM theme selection restored; no session was restarted.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',choices=['install','restore'])
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--theme',choices=adapter_assets.THEMES,default='plague-tale')
    args = parser.parse_args()
    try:
        if args.action == 'install':
            with tempfile.TemporaryDirectory(prefix='mct-greeter-source-') as folder:
                THEME_SOURCE=adapter_assets.stage_greeter(args.theme,Path(folder)/'theme')
                install(args.check)
        else: restore()
    except Exception as exc:
        print('Stopped: '+str(exc),file=sys.stderr)
        sys.exit(1)
