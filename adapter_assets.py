"""Resolve reviewed theme assets; adapters retain their own install/restore lifecycle."""
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
THEMES = ('plague-tale', 'deltarune', 'deltarune-snowgrave', 'deltarune-adventure')


def selected(explicit=None):
    if explicit is not None:
        if explicit not in THEMES:
            raise ValueError('Unknown theme: ' + str(explicit))
        return explicit
    # The desktop core currently uses its HOME state directory. Also support
    # explicitly relocated adapter environments, without choosing conflicting records.
    states = {Path.home()/'.local/state', Path(os.environ.get('XDG_STATE_HOME', str(Path.home()/'.local/state')))}
    values = []
    for state in states:
        path = state/'desktop-style/theme-core/active.json'
        if path.exists():
            value = json.loads(path.read_text())
            if not isinstance(value, dict) or value.get('id') not in THEMES:
                raise ValueError('Cannot determine the active theme; use --theme explicitly.')
            values.append(value['id'])
    if not values:
        return 'plague-tale'
    if len(set(values)) != 1:
        raise ValueError('Conflicting active themes; use --theme explicitly.')
    return values[0]


def source(theme, adapter):
    if theme not in THEMES or adapter not in ('dolphin', 'spotify', 'sddm', 'terminal'):
        raise ValueError('Unknown theme/adapter')
    if theme == 'plague-tale':
        return {'dolphin':ROOT/'apps/dolphin', 'spotify':ROOT/'apps/spotify',
                'sddm':ROOT/'sddm/theme', 'terminal':ROOT/'terminal-medallion'}[adapter]
    path = ROOT/'themes'/theme/'adapters'/adapter
    if not path.is_dir() or path.is_symlink():
        raise ValueError('Missing adapter: ' + str(path))
    return path


def stage_greeter(theme, destination):
    """One login controller; the selected adapter overrides only presentation assets."""
    destination = Path(destination)
    shutil.copytree(ROOT/'sddm/theme', destination)
    if theme != 'plague-tale':
        for path in source(theme, 'sddm').iterdir():
            if path.is_symlink() or not path.is_file() or path.name == 'Main.qml':
                raise ValueError('Only regular greeter presentation assets may be overlaid')
            shutil.copy2(path, destination/path.name)
    return destination
