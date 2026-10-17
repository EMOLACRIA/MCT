#!/usr/bin/env python3
"""Own the desktop shell process and verify its IPC and notification bus."""
import fcntl
import json
import os
from pathlib import Path
import re
import signal
import shutil
import subprocess
import sys
import time

STYLE=Path.home()/'.config/desktop-style'
STATE=Path.home()/'.local/state/desktop-style'
FEEDBACK=str(STYLE/'feedback')
SHELL=str(STYLE/'shell')

def shell_selector(args):
    """Identify a launched profile, never an IPC/list/kill command targeting it."""
    if not args or not all(isinstance(arg,str) for arg in args) or Path(args[0]).name not in {'quickshell','qs'}:
        return None
    selectors=[];index=1
    while index<len(args):
        arg=args[index]
        if arg in {'ipc','msg','log','list','kill','--help','-h','--version','-V'}:
            return None
        option,separator,value=arg.partition('=')
        if option in {'-p','--path','-c','--config'}:
            if not separator:
                index+=1
                if index>=len(args):return None
                value=args[index]
            if option in {'-p','--path'}:
                path=Path(value)
                if not path.is_absolute():return None
                path=path.resolve()
                if path.name=='shell.qml':path=path.parent
                selectors.append(('path',str(path)))
            else:selectors.append(('config',value))
        index+=1
    return selectors[0] if len(selectors)==1 else None

def legacy_shell_selectors():
    """Use existing conventional profiles or exact commands saved by our backup."""
    home=Path.home()
    config=Path(os.environ.get('XDG_CONFIG_HOME') or home/'.config')
    if not config.is_absolute():config=home/'.config'
    profile=config/'quickshell/HyprCade'
    candidates=[home/'Programs/HyprCade/config/quickshell/HyprCade',profile]
    selectors={('path',str(path.resolve())) for path in candidates if (path/'shell.qml').is_file()}
    if (profile/'shell.qml').is_file():selectors.add(('config','HyprCade'))
    try:
        backup=Path((STATE/'current-backup').read_text().strip())
        record=json.loads((backup/'manifest.json').read_text())
        commands=record.get('processes',[]) if isinstance(record,dict) else []
        if isinstance(commands,list):
            for command in commands:
                if isinstance(command,list):
                    selector=shell_selector(command)
                    if selector is not None:selectors.add(selector)
    except (OSError,ValueError):pass
    return selectors

def is_legacy_shell(args):
    selector=shell_selector(args)
    return selector is not None and selector in legacy_shell_selectors()

def processes():
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():continue
        try:
            if entry.stat().st_uid!=os.getuid():continue
            args=[a.decode(errors='replace') for a in (entry/'cmdline').read_bytes().split(b'\0') if a]
            if args:yield int(entry.name),args
        except (OSError,ValueError):pass

def is_shell(args):
    return shell_selector(args)==('path',str(Path(SHELL).resolve()))

def is_feedback(args):
    return is_shell(args) or shell_selector(args)==('path',str(Path(FEEDBACK).resolve()))

def managed(args,wallpaper=False):
    if not args:return False
    name=Path(args[0]).name
    return name in {'waybar','dunst'} or (wallpaper and name=='hyprpaper') or is_feedback(args) or is_legacy_shell(args) or (name=='wofi' and any(str(STYLE/'wofi'/n) in args for n in ['config','launcher.conf','power.conf'])) or str(STYLE/'scripts/menu.py') in args

def ipc(method):
    exe=shutil.which('quickshell') or shutil.which('qs')
    if not exe:return None
    try:return subprocess.run([exe,'ipc','-p',SHELL,'call','desktop',method],capture_output=True,text=True,timeout=2)
    except (OSError,subprocess.TimeoutExpired):return None

def notification_owner_pid():
    try:
        r=subprocess.run(['busctl','--user','call','org.freedesktop.DBus','/org/freedesktop/DBus','org.freedesktop.DBus','GetNameOwner','s','org.freedesktop.Notifications'],capture_output=True,text=True,timeout=2)
        match=re.fullmatch(r's "(:[0-9.]+)"\s*',r.stdout)
        if r.returncode or not match:return None
        r=subprocess.run(['busctl','--user','call','org.freedesktop.DBus','/org/freedesktop/DBus','org.freedesktop.DBus','GetConnectionUnixProcessID','s',match.group(1)],capture_output=True,text=True,timeout=2)
        match=re.fullmatch(r'u ([0-9]+)\s*',r.stdout)
        return int(match.group(1)) if not r.returncode and match else None
    except (OSError,subprocess.TimeoutExpired):return None

def feedback_ready():
    ping=ipc('ping');pid=ipc('pid')
    if not ping or ping.returncode or ping.stdout.strip()!='ready' or not pid or pid.returncode:return False
    try:return notification_owner_pid()==int(pid.stdout.strip())
    except ValueError:return False

def wait_feedback():
    deadline=time.monotonic()+12
    while time.monotonic()<deadline:
        if feedback_ready():return
        time.sleep(.2)
    raise RuntimeError('Desktop shell did not become ready or own notifications. See '+str(STATE/'shell.log'))

def read_services():
    result={}
    for name in ['dunst.service','waybar.service']:
        try:
            enabled=subprocess.run(['systemctl','--user','is-enabled',name],capture_output=True,text=True,timeout=3).stdout.strip()
            active=subprocess.run(['systemctl','--user','is-active',name],capture_output=True,text=True,timeout=3).stdout.strip()=='active'
            if enabled in {'enabled','enabled-runtime','disabled','static','indirect','masked','masked-runtime','linked','linked-runtime'}:
                result[name]={'enabled':enabled,'active':active}
        except (OSError,subprocess.TimeoutExpired):pass
    return result

def suppress_services(record):
    for name,state in record.items():
        if state['enabled'] in {'enabled','enabled-runtime'}:
            args=['systemctl','--user','disable','--now']
            if state['enabled']=='enabled-runtime':args.append('--runtime')
            r=subprocess.run(args+[name],capture_output=True,text=True,timeout=5)
        elif state['active']:
            r=subprocess.run(['systemctl','--user','stop',name],capture_output=True,text=True,timeout=5)
        else:continue
        if r.returncode:raise RuntimeError('Could not stop desktop user service '+name+': '+r.stderr.strip())

def restore_services(record):
    for name,state in record.items():
        if state['enabled'] in {'enabled','enabled-runtime'}:
            args=['systemctl','--user','enable']
            if state['enabled']=='enabled-runtime':args.append('--runtime')
            subprocess.run(args+[name],capture_output=True,timeout=5)
        if state['active']:subprocess.run(['systemctl','--user','start',name],capture_output=True,timeout=5)

def stop_panel(wallpaper=False):
    targets=[(pid,args) for pid,args in processes() if managed(args,wallpaper)]
    for pid,args in targets:
        try:os.kill(pid,signal.SIGTERM)
        except ProcessLookupError:pass
    deadline=time.monotonic()+4
    while time.monotonic()<deadline:
        remaining=[(p,a) for p,a in processes() if managed(a,wallpaper)]
        if not remaining:return [a for _,a in targets]
        time.sleep(.05)
    raise RuntimeError('A desktop process is still running; another shell was not started.')

def stop_ui():return stop_panel(True)

def launch(args,log):
    STATE.mkdir(parents=True,exist_ok=True,mode=0o700)
    with (STATE/log).open('ab') as output:
        return subprocess.Popen(args,stdout=output,stderr=output,start_new_session=True,umask=0o077,cwd=str(Path.home()))

def start():
    STATE.mkdir(parents=True,exist_ok=True,mode=0o700)
    with (STATE/'start.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        services=read_services()
        if services and any(s['active'] or s['enabled'] in {'enabled','enabled-runtime'} for s in services.values()):
            record=STATE/'suppressed-services.json'
            if not record.exists():record.write_text(json.dumps(services,indent=2))
            suppress_services(services)
        running=list(processes())
        if not any(is_shell(a) for _,a in running):
            for pid,args in running:
                if Path(args[0]).name=='dunst':
                    try:os.kill(pid,signal.SIGTERM)
                    except ProcessLookupError:pass
            exe=shutil.which('quickshell') or shutil.which('qs')
            if not exe:raise RuntimeError('QuickShell is missing.')
            launch([exe,'-p',SHELL],'shell.log')
        wait_feedback()

if __name__=='__main__':
    try:
        if sys.argv[1:]==['start']:start()
        elif sys.argv[1:]==['stop']:stop_ui()
        else:raise RuntimeError('Use start or stop.')
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
