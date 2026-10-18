#!/usr/bin/env python3
"""Install Super+G only when the live Hyprland binding is free; preserve other keys."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys

import theme_core

ROOT = Path(__file__).resolve().parent
BEGIN = '-- desktop-style theme rail begin'
END = '-- desktop-style theme rail end'
DESCRIPTION = 'desktop-style:theme-rail'
PATTERN = re.compile(re.escape(BEGIN) + r'\n.*?\n' + re.escape(END), re.S)


def command():
    return shlex.join(['bash', str(ROOT/'theme.sh'), 'menu'])


def block():
    return BEGIN+'\nhl.bind("SUPER + G", hl.dsp.exec_cmd('+json.dumps(command(), ensure_ascii=False)+'), { description = "'+DESCRIPTION+'" })\n'+END


def is_super_g(row):
    mask = row.get('modmask')
    if type(mask) is not int:
        raise theme_core.ThemeError('Cannot verify a live binding modifier. Nothing changed.')
    # G can also be bound by hardware keycode; do not assume a keyboard layout.
    code = row.get('keycode', 0)
    return bool(mask & 64) and (str(row.get('key', '')).lower() == 'g' or bool(code))


def owned_live(row):
    # Lua binds are closures: Hyprland 0.56.2 reports __lua + a registry ref,
    # not exec + the command string. Source ownership and the unique description
    # identify ours; registry references may change on every config reload.
    return (row.get('modmask') == 64 and str(row.get('key','')).lower() == 'g'
            and row.get('keycode',0) == 0 and row.get('submap','') == ''
            and row.get('dispatcher') == '__lua' and str(row.get('arg','')).isdigit()
            and row.get('description') == DESCRIPTION)


class Installer:
    def __init__(self, engine=None):
        self.engine = engine or theme_core.Engine()
        self.path = self.engine.hypr/'keybinds.lua'
        self.pointer = self.engine.state/'theme-rail-binding.json'

    def run(self, args):
        result = subprocess.run(args, text=True, capture_output=True, timeout=20)
        if result.returncode:
            raise theme_core.ThemeError(result.stderr.strip() or result.stdout.strip() or 'Command failed: '+args[0])
        return result.stdout

    def bindings(self):
        rows = json.loads(self.run(['hyprctl', '-j', 'binds']))
        if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
            raise theme_core.ThemeError('Cannot read the live binding list. Nothing changed.')
        return rows

    def inspect(self, restoring=False):
        if os.geteuid() == 0 or not os.environ.get('HYPRLAND_INSTANCE_SIGNATURE'):
            raise theme_core.ThemeError('Run as your desktop user inside Hyprland, without sudo.')
        self.engine.verify_installed()
        if '0.56.2' not in self.run(['hyprctl', 'version']):
            raise theme_core.ThemeError('This binding adapter targets Hyprland 0.56.2 Lua.')
        if self.run(['hyprctl', 'configerrors']).strip():
            raise theme_core.ThemeError('Resolve existing Hyprland configuration errors first.')
        theme_core.safe(self.engine.hypr, 'keybinds.lua')
        if not self.path.is_file():
            raise theme_core.ThemeError('Expected the installed keybinds.lua; nothing changed.')
        theme_core.safe(self.engine.state, self.pointer.name)
        record = theme_core.read_json(self.pointer) if self.pointer.exists() else None
        if self.pointer.exists() and (not isinstance(record, dict) or not all(isinstance(record.get(k), str) for k in ('installation','block','command','backup'))):
            raise theme_core.ThemeError('Invalid theme-rail binding record; nothing changed.')
        if record and record.get('installation') != self.engine.installation():
            raise theme_core.ThemeError('The binding record belongs to a previous MCT installation.')
        text = self.path.read_text()
        owned = PATTERN.findall(text)
        if BEGIN in text or END in text or record:
            if not record or len(owned) != 1 or owned[0] != record.get('block'):
                raise theme_core.ThemeError('The theme-rail binding block was changed. Your edits were kept.')
        if restoring and not record:
            raise theme_core.ThemeError('No theme-rail binding is installed.')
        if not restoring:
            matches = [row for row in self.bindings() if is_super_g(row)]
            if len(matches) > 1 or any(not (record and owned_live(row)) for row in matches):
                raise theme_core.ThemeError('Super+G is occupied, or a Super keycode binding prevents proving it is free. Nothing changed.')
            quickshell = shutil.which('quickshell')
            if not quickshell:
                raise theme_core.ThemeError('QuickShell is required.')
            self.run([quickshell, '-p', str(ROOT/'theme-picker/validate.qml')])
        return text, record

    def apply(self, check=False, restore=False):
        text, record = self.inspect(restore)
        if check:
            print('Binding check passed: '+('owned Super+G can be removed.' if restore else 'Super+G is free or already owned; overlay QML compiled.'))
            return
        with self.engine.lock():
            text, record = self.inspect(restore)
            before_record = self.pointer.read_bytes() if self.pointer.exists() else None
            mode = self.path.stat().st_mode & 0o777
            if restore:
                new_text = text.replace(record['block'], '', 1)
                new_record = None
            else:
                if record is None:
                    backup = self.engine.state/'theme-rail-backups'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')/'keybinds.lua'
                    theme_core.atomic(backup, text.encode(), mode)
                    record = dict(backup=str(backup), installation=self.engine.installation())
                new_text = text.replace(record['block'], block(), 1) if 'block' in record else text.rstrip()+'\n\n'+block()+'\n'
                new_record = dict(record, block=block(), command=command())
            if self.path.read_text() != text:
                raise theme_core.ThemeError('Key bindings changed while preparing. Retry after reviewing them.')
            try:
                if new_record:
                    theme_core.atomic(self.pointer, theme_core.json_bytes(new_record))
                theme_core.atomic(self.path, new_text.encode(), mode)
                self.run(['hyprctl', 'reload'])
                if self.run(['hyprctl', 'configerrors']).strip():
                    raise theme_core.ThemeError('Hyprland rejected the binding; previous keys restored.')
                if not restore:
                    matches = [r for r in self.bindings() if is_super_g(r)]
                    if len(matches) != 1 or not owned_live(matches[0]):
                        raise theme_core.ThemeError('The new binding did not load uniquely; previous keys restored.')
                else:
                    self.pointer.unlink()
            except Exception:
                theme_core.atomic(self.path, text.encode(), mode)
                if before_record is None:
                    self.pointer.unlink(missing_ok=True)
                else:
                    theme_core.atomic(self.pointer, before_record)
                self.run(['hyprctl', 'reload'])
                raise
        print('Super+G removed; other key bindings kept.' if restore else 'Super+G installed. Press it to open or close the theme rail.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('bind','unbind'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        Installer().apply(check=args.check, restore=args.action == 'unbind')
        return 0
    except (theme_core.ThemeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print('Stopped: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':sys.exit(main())
