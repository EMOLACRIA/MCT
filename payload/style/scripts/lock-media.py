#!/usr/bin/env python3
"""Hyprlock labels and controls, using the same selected MPRIS player as the shell."""
import fcntl
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import unicodedata
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request

STYLE=Path.home()/'.config/desktop-style'
CACHE=Path.home()/'.cache/desktop-style/lock-media'
EMPTY={'title':'','artist':'Start music before locking','art':'','playing':False}

def ipc(method,*args):
    exe=shutil.which('quickshell') or shutil.which('qs')
    if not exe:raise RuntimeError('QuickShell is unavailable')
    result=subprocess.run([exe,'ipc','-p',str(STYLE/'shell'),'call','desktop',method,*args],capture_output=True,text=True,timeout=2)
    if result.returncode:raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()

def metadata():
    CACHE.mkdir(parents=True,exist_ok=True,mode=0o700)
    with (CACHE/'metadata.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        path=CACHE/'metadata.json'
        try:
            if time.time()-path.stat().st_mtime<.8:return json.loads(path.read_text())
        except (OSError,ValueError):pass
        try:
            data=json.loads(ipc('mediaInfo'))
            if not isinstance(data,dict):data=EMPTY
        except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired):data=EMPTY
        path.write_text(json.dumps(data))
        return data

def cover_path(url):
    fallback=STYLE/'hyprlock/cover.png'
    parsed=urlparse(url)
    if parsed.scheme=='file' and parsed.netloc in {'','localhost'}:
        path=Path(unquote(parsed.path))
        return path if path.is_file() else fallback
    if parsed.scheme not in {'http','https'}:return fallback
    key=hashlib.sha256(url.encode()).hexdigest();path=CACHE/(key+'.img')
    if path.is_file():return path
    # Downloads never block the lock screen's synchronous reload command.
    marker=CACHE/(key+'.attempt')
    try:
        if time.time()-marker.stat().st_mtime<60:return fallback
    except OSError:pass
    marker.touch()
    subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'fetch-cover',url],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
    return fallback

def fetch_cover(url):
    if urlparse(url).scheme not in {'http','https'}:return
    CACHE.mkdir(parents=True,exist_ok=True,mode=0o700)
    target=CACHE/(hashlib.sha256(url.encode()).hexdigest()+'.img')
    with urlopen(Request(url,headers={'User-Agent':'DesktopMedia/1.0'}),timeout=4) as response:
        if not response.headers.get('Content-Type','').startswith('image/'):return
        data=response.read(8*1024*1024+1)
        if len(data)>8*1024*1024:return
    temp=target.with_suffix('.tmp');temp.write_bytes(data);temp.replace(target)
    for old in sorted(CACHE.glob('*.img'),key=lambda p:p.stat().st_mtime,reverse=True)[40:]:old.unlink(missing_ok=True)

def plain(value,limit):
    text=' '.join(str(value or '').split())
    size=0;kept=[]
    for ch in text:
        weight=2 if unicodedata.east_asian_width(ch) in {'W','F'} else 1.6 if ch in 'MW@' else 1
        if size+weight>limit:return html.escape(''.join(kept)+'…')
        kept.append(ch);size+=weight
    return html.escape(text)

def main():
    action=sys.argv[1] if len(sys.argv)>1 else 'title'
    if action=='fetch-cover':fetch_cover(sys.argv[2]);return
    if action in {'toggle','previous','next'}:
        ipc('mediaControl',action)
        (CACHE/'metadata.json').unlink(missing_ok=True)
        return
    data=metadata()
    if action=='title':print(plain(data.get('title') or 'No active player',22))
    elif action=='artist':print(plain(data.get('artist') or '',36))
    elif action=='state':print('NOW PLAYING' if data.get('playing') else 'PAUSED' if data.get('title') else 'MUSIC')
    elif action=='cover':print(cover_path(data.get('art') or ''))
    elif action=='button':print(STYLE/'hyprlock'/('pause.png' if data.get('playing') else 'play.png'))
    else:raise ValueError('Unknown media action')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
