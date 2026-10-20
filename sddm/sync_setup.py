#!/usr/bin/env python3
"""One-time root setup: cache reviewed skins and install a narrowly scoped SDDM selector."""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import adapter_assets
import theme_core
from sync_helper import Backend,STATE,CATALOG,CONFIG,HELPER,LIVE,atomic,write,read,selection
POLICY=Path('/usr/share/polkit-1/actions/org.mct.theme-sddm.policy')


def assets(root,theme):
    common=Path(root)/'sddm/theme'
    result={p.name:p for p in common.iterdir() if p.is_file()}
    if theme!='plague-tale':
        source=Path(root)/'themes'/theme/'adapters/sddm'
        for p in source.iterdir():
            if p.is_symlink() or not p.is_file() or p.name=='Main.qml':raise ValueError('Invalid SDDM presentation source.')
            result[p.name]=p
    for p in result.values():
        if p.is_symlink():raise ValueError('SDDM source links require adaptation.')
    return result


def fingerprint(files):
    h=hashlib.sha256()
    for name,p in sorted(files.items()):
        h.update(name.encode()+b'\0'+hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def trusted(path):
    return not path.is_symlink() and (not path.exists() or (path.stat().st_uid==0 and not path.stat().st_mode&0o022))

def install(user,check=False):
    if os.geteuid()!=0:raise ValueError('Run this one-time setup with sudo.')
    account=pwd.getpwnam(user)
    if account.pw_uid==0:raise ValueError('Select the normal desktop user with --user.')
    if Path('/etc/systemd/system/display-manager.service').resolve().name!='sddm.service':raise ValueError('The selected display manager is not SDDM.')
    if not shutil.which('pkexec'):raise ValueError('Missing required command: pkexec')
    if not shutil.which('sddm-greeter-qt6'):
        exe=shutil.which('sddm-greeter')
        if not exe:raise ValueError('Missing Qt6 SDDM greeter.')
        linked=subprocess.run(['ldd',exe],capture_output=True,text=True,timeout=5)
        if linked.returncode or 'libQt6' not in linked.stdout:raise ValueError('This integration needs the Qt6 SDDM greeter.')
    for path in (STATE,CATALOG,HELPER,HELPER.parent,POLICY,POLICY.parent,CONFIG):
        if not trusted(path):raise ValueError('Untrusted or linked system path kept: '+str(path))
    enrolled=(STATE/'catalog.json').exists()
    if not enrolled and LIVE.is_symlink():raise ValueError('Existing SDDM theme link needs adaptation before enrollment.')
    if not enrolled and LIVE.exists():
        for path in (LIVE,*LIVE.rglob('*')):
            if not trusted(path):raise ValueError('Custom or linked SDDM theme source kept: '+str(path))
    engine=theme_core.Engine(root=ROOT);themes={};sources={}
    for path in sorted((ROOT/'themes').iterdir()):
        if not path.is_dir():continue
        manifest,_=engine.load(path.name);sources[path.name]=assets(ROOT,path.name)
        themes[path.name]=dict(version=manifest['version'],fingerprint=fingerprint(sources[path.name]))
    b=Backend();snapshot=b.snapshot()
    if enrolled:
        old=read(STATE/'catalog.json')
        if old['uid']!=account.pw_uid:raise ValueError('SDDM theme switching is already assigned to another desktop user.')
        if (STATE/'pending.json').exists():raise ValueError('Recover the pending theme operation before refreshing SDDM setup.')
        b.guard()
    if check:
        print('SDDM sync setup check passed: '+str(len(themes))+' skins, desktop user '+user+'. No files changed.');return
    STATE.mkdir(mode=0o700,parents=True,exist_ok=True);(STATE/'transactions').mkdir(mode=0o700,exist_ok=True)
    with b.locked():
        if (STATE/'pending.json').exists():raise ValueError('Recover the pending operation before refreshing setup.')
        if enrolled:b.guard()
        if not (STATE/'original.json').exists():write(STATE/'original.json',snapshot)
        # Preserve the previous stable theme separately from its later read-only cache copy.
        if not (STATE/'original-live.json').exists():
            write(STATE/'original-live.json',dict(exists=LIVE.exists()))
            if LIVE.exists():shutil.copytree(LIVE,STATE/'original-live-theme')
        CATALOG.parent.mkdir(parents=True,exist_ok=True)
        previous=CATALOG.with_name('.desktop-style-sync-previous')
        if previous.exists():raise ValueError('An earlier system setup needs recovery: '+str(previous))
        mutable=[HELPER,STATE/'catalog.json',STATE/'current.json',POLICY,CONFIG]
        before={p:(p.read_bytes(),p.stat().st_mode&0o777) if p.exists() else None for p in mutable}
        oldlink=os.readlink(LIVE) if LIVE.is_symlink() else None
        olddir=LIVE.exists() and not LIVE.is_symlink()
        HELPER.parent.mkdir(mode=0o755,parents=True,exist_ok=True)
        swapped=False;livechanged=False
        try:
            with tempfile.TemporaryDirectory(prefix='.mct-skins-',dir=CATALOG.parent) as folder:
                stage=Path(folder)/'skins';stage.mkdir(mode=0o755)
                for theme,files in sources.items():
                    directory=stage/theme;directory.mkdir(mode=0o755)
                    for name,path in files.items():shutil.copyfile(path,directory/name);(directory/name).chmod(0o644)
                original=STATE/'original-live-theme'
                shutil.copytree(original if original.exists() else stage/'plague-tale',stage/'.baseline')
                for path in (stage/'.baseline',*(stage/'.baseline').rglob('*')):path.chmod(0o755 if path.is_dir() else 0o644)
                if enrolled and not (stage/Path(oldlink).name/'Main.qml').is_file():raise ValueError('The active login skin would be removed; select another skin before refreshing.')
                if CATALOG.exists():CATALOG.rename(previous)
                try:stage.rename(CATALOG);swapped=True
                except Exception:
                    if previous.exists():previous.rename(CATALOG)
                    raise
            if not enrolled:
                if olddir:shutil.rmtree(LIVE)
                b.set_live(str(CATALOG/'.baseline'));livechanged=True
                body=selection(base64.b64decode(snapshot['body']).decode('utf-8',errors='surrogateescape'),'desktop-style',CATALOG.parent).encode('utf-8',errors='surrogateescape')
                atomic(CONFIG,body,snapshot['mode'])
                write(STATE/'current.json',dict(theme=None,sha=hashlib.sha256(body).hexdigest(),live=str(CATALOG/'.baseline'),token=None))
            atomic(HELPER,(ROOT/'sddm/sync_helper.py').read_bytes(),0o755)
            write(STATE/'catalog.json',dict(schema=1,uid=account.pw_uid,themes=themes))
            policy='<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE policyconfig PUBLIC "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN" "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">\n<policyconfig>\n  <action id="org.mct.theme-sddm">\n    <description>Select a preinstalled desktop login skin</description>\n    <message>Select a reviewed MCT login skin</message>\n    <defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>yes</allow_active></defaults>\n    <annotate key="org.freedesktop.policykit.exec.path">/usr/lib/desktop-style/theme-sddm</annotate>\n  </action>\n</policyconfig>\n'
            atomic(POLICY,policy.encode(),0o644)
        except Exception:
            for path,item in before.items():
                if item is None:path.unlink(missing_ok=True)
                else:atomic(path,item[0],item[1])
            if livechanged or olddir:
                if LIVE.is_symlink():LIVE.unlink()
                if olddir and not LIVE.exists():shutil.copytree(STATE/'original-live-theme',LIVE)
                elif oldlink and not LIVE.exists():LIVE.symlink_to(oldlink)
            if swapped:
                shutil.rmtree(CATALOG)
                if previous.exists():previous.rename(CATALOG)
            raise
        if previous.exists():shutil.rmtree(previous)
    print('SDDM sync ready for '+user+': '+str(len(themes))+' root-installed skins. No display-manager restart.')
    print('Next, without sudo: bash theme.sh integrations enable')


def remove():
    if os.geteuid()!=0:raise ValueError('Use sudo for system SDDM sync removal.')
    b=Backend()
    with b.locked():
        if (STATE/'pending.json').exists():raise ValueError('Recover the pending operation first.')
        b.guard();b.restore_config(read(STATE/'original.json'))
        if LIVE.is_symlink():LIVE.unlink()
        if read(STATE/'original-live.json')['exists']:shutil.copytree(STATE/'original-live-theme',LIVE)
        POLICY.unlink(missing_ok=True);HELPER.unlink(missing_ok=True)
        if CATALOG.exists():shutil.rmtree(CATALOG)
        # Keep original.json and transaction records for audit; permit explicit re-enrollment.
        (STATE/'catalog.json').unlink();(STATE/'current.json').unlink()
    print('Original SDDM selection restored. No session was restarted.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['install','remove']);p.add_argument('--user',default=os.environ.get('SUDO_USER'));p.add_argument('--check',action='store_true');a=p.parse_args()
    try:
        if a.action=='remove':remove()
        elif not a.user:raise ValueError('Specify --user with the normal desktop account.')
        else:install(a.user,a.check)
    except Exception as e:print('Stopped: '+str(e),file=sys.stderr);sys.exit(1)
