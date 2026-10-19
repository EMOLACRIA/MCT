#!/usr/bin/env python3
"""Install the UTF-8 representation of a CP437 logo; retain an exact restore backup."""
import argparse
from datetime import datetime
import fcntl
import hashlib
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
adapter_assets=None
if (PACKAGE.parent/"adapter_assets.py").is_file():
    import adapter_assets
STATE = Path(os.environ.get('XDG_STATE_HOME', str(Path.home()/'.local/state'))) / 'terminal-medallion'
ASSET = Path(os.environ.get('XDG_DATA_HOME', str(Path.home()/'.local/share'))) / 'terminal-medallion/medallion.txt'


def tokens(text):
    """Token offsets retain every comment and all unrelated formatting."""
    result = []
    pattern = re.compile(r'\s+|//[^\r\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|[{}\[\]:,]|true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[Ee][+-]?\d+)?')
    offset = 0
    for match in pattern.finditer(text):
        if match.start() != offset:
            raise ValueError('Invalid JSONC near character ' + str(offset))
        offset = match.end()
        value = match.group()
        if value.isspace() or value.startswith(('//', '/*')):
            continue
        result.append((value, match.start(), match.end()))
    if offset != len(text):
        raise ValueError('Invalid JSONC near character ' + str(offset))
    return result


def parsed(text):
    stream = tokens(text)
    # Fastfetch accepts comments and trailing commas. Strings remain untouched.
    clean = ''.join(t[0] for i, t in enumerate(stream)
                    if not (t[0] == ',' and i+1 < len(stream) and stream[i+1][0] in ('}', ']')))
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError('Duplicate JSONC key: ' + key)
            out[key] = value
        return out
    value = json.loads(clean, object_pairs_hook=unique)
    if not isinstance(value, dict):
        raise ValueError('Fastfetch configuration must be a JSONC object.')
    return value


def with_field(text, name, replacement):
    before = parsed(text)
    stream = tokens(text)
    depth = 0
    for i, (value, start, end) in enumerate(stream):
        if value in ('{', '['):
            depth += 1
        elif value in ('}', ']'):
            depth -= 1
        elif depth == 1 and value == json.dumps(name) and stream[i+1][0] == ':':
            begin = stream[i+2][1]
            j = i+2
            if stream[j][0] in ('{', '['):
                nested = 0
                while j < len(stream):
                    nested += stream[j][0] in ('{', '[')
                    nested -= stream[j][0] in ('}', ']')
                    if nested == 0:
                        break
                    j += 1
            finish = stream[j][2]
            updated = text[:begin] + json.dumps(replacement, ensure_ascii=False, indent=4) + text[finish:]
            break
    else:
        opening = stream[0][2]
        separator = ',' if before else ''
        updated = text[:opening] + '\n    ' + json.dumps(name) + ': ' + json.dumps(replacement, ensure_ascii=False, indent=4) + separator + text[opening:]
    after = parsed(updated)
    if {k:v for k,v in before.items() if k != name} != {k:v for k,v in after.items() if k != name}:
        raise ValueError('Unrelated configuration changed; installation cancelled.')
    return updated


def with_logo(text, value):
    return with_field(text, 'logo', value)


def ensure_modules(text):
    current = parsed(text)
    if current.get('modules'):
        if not isinstance(current['modules'], list):
            raise RuntimeError('Fastfetch modules must be an array.')
        return text
    # A logo-only JSONC file does NOT inherit Fastfetch's implicit defaults.
    # Ask the installed version for its normal module list instead of guessing.
    with tempfile.TemporaryDirectory(prefix='terminal-medallion-defaults-') as td:
        generated = Path(td)/'config.jsonc'
        result = subprocess.run(['fastfetch','--gen-config',str(generated)],
                                capture_output=True, text=True, timeout=15)
        if result.returncode or not generated.is_file():
            raise RuntimeError('Cannot recover default Fastfetch information modules: ' + result.stderr)
        modules = parsed(generated.read_text()).get('modules')
    if not isinstance(modules, list) or not modules:
        raise RuntimeError('Fastfetch generated no information modules. Nothing changed.')
    return with_field(text, 'modules', modules)


def atomic(path, data, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    staged = Path(name)
    try:
        with os.fdopen(fd, 'wb') as output:
            output.write(data)
        staged.chmod(mode)
        os.replace(staged, path)  # Detach a file symlink; never write through it.
    finally:
        staged.unlink(missing_ok=True)


def discover(explicit):
    if explicit:
        target = Path(os.path.abspath(os.path.expanduser(explicit)))
        if not target.is_file():
            raise RuntimeError('Config file not found: ' + str(target))
        return target, target
    result = subprocess.run(['fastfetch', '--list-config-paths'], capture_output=True, text=True, timeout=10)
    paths = [Path(line.strip()) for line in result.stdout.splitlines() if line.strip().startswith('/')]
    if result.returncode or not paths:
        raise RuntimeError('Cannot find Fastfetch config paths. Use --config /path/to/config.jsonc.')
    target = paths[0]/'config.jsonc'
    source = next((p/'config.jsonc' for p in paths if (p/'config.jsonc').is_file()), None)
    return target, source


def logo(args, source):
    accent={'plague-tale':'#b5a37c','deltarune':'#f32baf','deltarune-snowgrave':'#d8b779','deltarune-adventure':'#ffcf77'}[getattr(args,'theme','plague-tale')]
    return {'type':'file', 'source':str(source), 'position':'left',
            'padding':{'top':1, 'left':1, 'right':5}, 'color':{'1':accent}}


def source_asset(args):
    theme=getattr(args,'theme','plague-tale')
    directory=adapter_assets.source(theme,'terminal') if adapter_assets and theme!='plague-tale' else PACKAGE
    return directory/('medallion-compact.txt' if getattr(args, 'compact', False) else 'medallion.txt')


def preflight(args):
    if os.geteuid() == 0:
        raise RuntimeError('Run as your normal desktop user, without sudo.')
    if not shutil.which('fastfetch'):
        raise RuntimeError('fastfetch is not installed.')
    if not source_asset(args).is_file():
        raise RuntimeError(str(source_asset(args)) + ' is missing; extract the complete ZIP.')
    selected = args.config
    marker = STATE/'current.json'
    if not selected and marker.is_file():
        selected = json.loads(marker.read_text())['target']
    target, source = discover(selected)
    if target.is_symlink() and not target.is_file():
        raise RuntimeError('Broken config link: ' + str(target))
    for parent in [target.parent, *target.parent.parents, ASSET.parent, *ASSET.parent.parents]:
        if parent.is_symlink():
            raise RuntimeError('Linked config/data directory needs adaptation: ' + str(parent))
    text = source.read_bytes().decode('utf-8') if source else '{}\n'
    updated = with_logo(ensure_modules(text), logo(args, ASSET))
    if marker.is_file():
        record = json.loads(marker.read_text())
        if str(target) != record['target'] or target.is_symlink() or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != record['installed_sha256']:
            raise RuntimeError('Fastfetch config changed after installation. Backup retained at ' + record['backup'])
        if ASSET.is_symlink() or ((ASSET.exists()) and (record['asset'] != str(ASSET) or not ASSET.is_file())):
            raise RuntimeError('Untracked text logo needs adaptation: ' + str(ASSET))
    return target, source, updated


def preview(args):
    _, _, updated = preflight(args)
    # Preview the complete corrected configuration, including recovered modules.
    updated = with_logo(updated, logo(args, source_asset(args)))
    with tempfile.TemporaryDirectory(prefix='terminal-medallion-preview-') as td:
        config = Path(td)/'config.jsonc'
        config.write_text(updated)
        return subprocess.call(['fastfetch','--config',str(config)])


def install(args):
    target, source, updated = preflight(args)
    desired_asset = source_asset(args).read_bytes()
    variant = 'compact' if getattr(args, 'compact', False) else 'detailed'
    if args.check:
        print('Check passed. ' + variant.capitalize() + ' CP437 medallion and information modules are ready: ' + str(target))
        return
    marker = STATE/'current.json'
    if marker.exists():
        record = json.loads(marker.read_text())
        if str(target) == record['target'] and target.is_file() and target.read_bytes() == updated.encode() and hashlib.sha256(target.read_bytes()).hexdigest() == record['installed_sha256'] and ASSET.is_file() and ASSET.read_bytes() == desired_asset:
            print('The medallion is already installed. Open a new Kitty terminal with Super+Q.')
            return
        previous = dict(record)
        previous_asset = ASSET.read_bytes() if ASSET.is_file() else None
        snapshot = STATE/'revisions'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        snapshot.mkdir(parents=True, mode=0o700)
        shutil.copy2(target, snapshot/'config.previous')
        if previous_asset is not None:
            (snapshot/'medallion.previous.txt').write_bytes(previous_asset)
        (snapshot/'current.previous.json').write_text(json.dumps(previous, indent=2))
        record = {**previous, 'asset':str(ASSET), 'revision':'cp437-1.3', 'variant':variant,
                  'asset_sha256':hashlib.sha256(desired_asset).hexdigest(),
                  'installed_sha256':hashlib.sha256(updated.encode()).hexdigest()}
        try:
            atomic(ASSET, desired_asset)
            atomic(target, updated.encode(), record['mode'])
            atomic(marker, json.dumps(record, indent=2).encode(), 0o600)
        except Exception:
            atomic(target, (snapshot/'config.previous').read_bytes(), record['mode'])
            atomic(marker, json.dumps(previous, indent=2).encode(), 0o600)
            if previous_asset is not None:
                atomic(ASSET, previous_asset)
            else:
                ASSET.unlink(missing_ok=True)
            raise
        print('Updated to ' + variant + ' CP437 art. Original restore backup preserved: ' + record['backup'])
        print('Open a NEW terminal with Super+Q.')
        return
    if ASSET.exists() or ASSET.is_symlink():
        raise RuntimeError('Untracked medallion asset already exists: ' + str(ASSET))
    backup = STATE/'backups'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True, mode=0o700)
    record = {'target':str(target), 'exists':target.exists(),
              'link':os.readlink(target) if target.is_symlink() else None,
              'mode':target.stat().st_mode & 0o777 if target.exists() else 0o644,
              'backup':str(backup), 'asset':str(ASSET),
              'revision':'cp437-1.3', 'variant':variant,
              'asset_sha256':hashlib.sha256(desired_asset).hexdigest(),
              'installed_sha256':hashlib.sha256(updated.encode()).hexdigest()}
    if record['exists']:
        shutil.copy2(target, backup/'config.original')
    (backup/'manifest.json').write_text(json.dumps(record, indent=2))
    changed = False
    try:
        atomic(ASSET, desired_asset)
        atomic(target, updated.encode(), record['mode'])
        changed = True
        atomic(marker, json.dumps(record, indent=2).encode(), 0o600)
    except Exception:
        if changed:
            restore_file(record)
        ASSET.unlink(missing_ok=True)
        raise
    print('Installed. Backup: ' + str(backup))
    print('Open a NEW Kitty terminal with Super+Q. Restore with: bash restore.sh')


def restore_file(record):
    target = Path(record['target'])
    if record['link'] is not None:
        target.unlink(missing_ok=True)
        target.symlink_to(record['link'])
    elif record['exists']:
        atomic(target, (Path(record['backup'])/'config.original').read_bytes(), record['mode'])
    else:
        target.unlink(missing_ok=True)


def restore(args):
    if os.geteuid() == 0:
        raise RuntimeError('Run without sudo.')
    marker = STATE/'current.json'
    if not marker.is_file():
        raise RuntimeError('No installed terminal medallion found.')
    record = json.loads(marker.read_text())
    target = Path(record['target'])
    if target.is_symlink() or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != record['installed_sha256']:
        raise RuntimeError('Fastfetch config changed after installation. Backup retained at ' + record['backup'])
    if args.check:
        print('Restore check passed.')
        return
    restore_file(record)
    Path(record['asset']).unlink(missing_ok=True)
    marker.unlink()
    print('Previous Fastfetch configuration restored. Backup retained: ' + record['backup'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['install','preview','restore'])
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--config', help='Explicit Fastfetch config used by a custom greeting')
    parser.add_argument('--compact', action='store_true', help='Use the smaller 39-column, 17-row drawing')
    parser.add_argument('--theme',choices=adapter_assets.THEMES if adapter_assets else ('plague-tale',))
    args = parser.parse_args()
    try:
        if adapter_assets:
            choice=args.theme or ("plague-tale" if args.action=="restore" else None)
            args.theme=adapter_assets.selected(choice)
        else:
            args.theme="plague-tale"
        if args.action == 'preview':
            return preview(args)
        if args.check:
            globals()[args.action](args)
        else:
            if os.geteuid() == 0:
                raise RuntimeError('Run as your normal desktop user, without sudo.')
            STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
            with (STATE/'install.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                globals()[args.action](args)
    except Exception as exc:
        print('Stopped: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
