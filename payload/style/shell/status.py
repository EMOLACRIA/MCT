#!/usr/bin/env python3
"""Read backlight and connectivity without changing either."""
import json
import os
from pathlib import Path
import shutil
import subprocess

def run(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=2,
                           env={**os.environ, 'LC_ALL':'C'})
        return p.stdout.strip() if p.returncode == 0 else ''
    except (OSError, subprocess.TimeoutExpired):
        return ''

def read_status():
    brightness = -1
    if shutil.which('brightnessctl'):
        try:
            current = int(run(['brightnessctl','-c','backlight','get']))
            maximum = int(run(['brightnessctl','-c','backlight','max']))
            if maximum > 0:
                brightness = round(current*100/maximum)
        except ValueError:
            pass
    network = 'Offline'
    if shutil.which('nmcli'):
        # Tab separators are avoided; terse escaping safely keeps punctuation.
        raw = run(['nmcli','-t','--escape','no','-f','TYPE,STATE,CONNECTION','device'])
        for line in raw.splitlines():
            fields = line.split(':',2)
            if len(fields) == 3 and fields[1] == 'connected' and fields[0] != 'loopback':
                network = fields[2] or 'Connected'
                break
    return {'brightness':brightness, 'network':network,
            'networkSettingsAvailable':bool(shutil.which('nm-connection-editor'))}

if __name__ == '__main__':
    print(json.dumps(read_status(),ensure_ascii=False))
