#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

def toggle(panel):
    if panel not in {'launcher','power','controls','notifications','media','hardware'}:
        raise RuntimeError('Unknown panel.')
    exe=shutil.which('quickshell') or shutil.which('qs')
    if not exe:
        raise RuntimeError('QuickShell is missing.')
    path=str(Path.home()/'.config/desktop-style/shell')
    result=subprocess.run([exe,'ipc','-p',path,'call','desktop','toggle',panel],capture_output=True,text=True,timeout=4)
    if result.returncode:
        raise RuntimeError('Desktop shell is not ready. Run: bash ~/.config/desktop-style/scripts/start.sh')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('panel',choices=['launcher','power','controls','notifications','media','hardware']);a=p.parse_args()
    try:toggle(a.panel)
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
