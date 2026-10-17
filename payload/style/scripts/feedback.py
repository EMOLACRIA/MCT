#!/usr/bin/env python3
"""Change a device value, then display its measured state through QuickShell IPC."""
import argparse
import fcntl
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

STYLE = Path.home() / '.config/desktop-style'
STATE = Path.home() / '.local/state/desktop-style'

def command(args):
    result = subprocess.run(args, text=True, capture_output=True, timeout=4,
                            env={**os.environ, 'LC_ALL': 'C'})
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'Command failed: ' + args[0])
    return result.stdout.strip()

def change(kind, action, step=5):
    if kind in {'volume', 'microphone'}:
        device = '@DEFAULT_AUDIO_SOURCE@' if kind == 'microphone' else '@DEFAULT_AUDIO_SINK@'
        if action == 'mute':
            command(['wpctl', 'set-mute', device, 'toggle'])
        elif action in {'up', 'down'}:
            command(['wpctl', 'set-volume', '-l', '1', device,
                     str(step) + ('%+' if action == 'up' else '%-')])
        value = command(['wpctl', 'get-volume', device])
        match = re.search(r'Volume:\s*([0-9.]+)', value)
        if not match:
            raise RuntimeError('Cannot read the audio device volume.')
        return min(100, max(0, round(float(match.group(1)) * 100))), '[MUTED]' in value
    if action == 'mute':
        raise RuntimeError('Brightness does not have a mute action.')
    if action in {'up', 'down'}:
        command(['brightnessctl', '-c', 'backlight', 'set',
                 '+' + str(step) + '%' if action == 'up' else str(step) + '%-'])
    current = int(command(['brightnessctl', '-c', 'backlight', 'get']))
    maximum = int(command(['brightnessctl', '-c', 'backlight', 'max']))
    if maximum <= 0:
        raise RuntimeError('Invalid backlight maximum.')
    return min(100, max(0, round(current * 100 / maximum))), False

def show(kind, level, muted):
    exe = shutil.which('quickshell') or shutil.which('qs')
    if not exe:
        raise RuntimeError('QuickShell is missing.')
    command([exe, 'ipc', '-p', str(STYLE/'shell'), 'call', 'feedback', 'present',
             kind, str(level), str(muted).lower()])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('kind', choices=['volume', 'microphone', 'brightness'])
    parser.add_argument('action', choices=['up', 'down', 'mute', 'show'])
    parser.add_argument('step', type=int, nargs='?', default=5, choices=range(1, 11))
    args = parser.parse_args()
    STATE.mkdir(parents=True, exist_ok=True)
    # Serialize repeats so mute toggles and displayed values remain consistent.
    with (STATE/'feedback.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        level, muted = change(args.kind, args.action, args.step)
        try:
            show(args.kind, level, muted)
        except Exception as exc:
            with (STATE/'feedback.log').open('a') as output:
                output.write(str(exc) + '\n')
            # Device changes still succeed; never turn an OSD into a notification.
            raise RuntimeError('OSD unavailable. Run bash ~/.config/desktop-style/scripts/start.sh; details: '+str(STATE/'feedback.log')) from exc


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
