#!/usr/bin/env python3
"""Fixed desktop actions. No shell interpolation and no config rewriting."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

STYLE = Path.home()/'.config/desktop-style'

def ipc(target, method, *args):
    exe = shutil.which('quickshell') or shutil.which('qs')
    if exe:
        subprocess.run([exe,'ipc','-p',str(STYLE/'shell'),'call',target,method,*map(str,args)],
                       capture_output=True,timeout=3)

def action(kind, value):
    if kind == 'brightness':
        percent = max(1,min(100,int(value)))
        result = subprocess.run(['brightnessctl','-c','backlight','set',str(percent)+'%'],capture_output=True,text=True,timeout=5)
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or 'Brightness could not be changed.')
        subprocess.run(['bash',str(STYLE/'scripts/feedback.sh'),'brightness','show'],timeout=8)
        return
    if kind == 'network':
        command = ['nm-connection-editor']
    else:
        command = {'lock':['hyprlock'], 'suspend':['systemctl','suspend'],
                   'logout':['hyprctl','dispatch','hl.dsp.exit()'],
                   'restart':['systemctl','reboot'], 'poweroff':['systemctl','poweroff']}[value]
    if kind == 'network' or (kind == 'session' and value == 'lock'):
        subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
        return
    result = subprocess.run(command,capture_output=True,text=True,timeout=20)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'The requested action failed.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('kind',choices=['brightness','session','network'])
    parser.add_argument('value',nargs='?',default='')
    args = parser.parse_args()
    try:
        action(args.kind,args.value)
    except Exception as exc:
        ipc('desktop','error',str(exc))
        print(str(exc),file=sys.stderr)
        sys.exit(1)
