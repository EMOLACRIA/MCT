#!/usr/bin/env python3
"""Move the installed desktop to QuickShell, with a revision rollback."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import re
from datetime import datetime
import manage as m

LEGACY_LOGOUT_ERROR='return hl.dispatch(exit):1: hl.dispatch: expected a dispatcher (e.g. hl.dsp.window.close())'

def ensure_clean_config():
    errors=m.run(['hyprctl','configerrors'])
    if errors.returncode==0 and errors.stdout.strip()==LEGACY_LOGOUT_ERROR:
        result=m.run(['hyprctl','reload'])
        if result.returncode:raise RuntimeError('Configuration refresh failed: '+result.stdout+result.stderr)
        errors=m.run(['hyprctl','configerrors'])
    if errors.returncode or errors.stdout.strip():raise RuntimeError('Resolve existing config errors first: '+errors.stdout+errors.stderr)

def patch_file_manager(text):
    # Only migrate our stock binding/command, including the published manual fix.
    # A user's different file manager or custom Super+E remains their choice.
    standard = 'hl.bind(mainMod .. " + E", hl.dsp.exec_cmd(fileManager))'
    if sum(line.strip() == standard for line in text.splitlines()) != 1:
        return text
    pattern = r'(?m)^(local fileManager\s*=\s*)("(?:dolphin|env QT_QPA_PLATFORMTHEME=qt6ct QT_STYLE_OVERRIDE=Fusion dolphin)")(\s*(?:--[^\n]*)?)$'
    if len(re.findall(pattern, text)) != 1:
        return text
    return re.sub(pattern, lambda match: match[1] + 'styleCommand("file-manager.sh")' + match[3], text)


def patch_terminal(text):
    standard='hl.bind(mainMod .. " + Q", hl.dsp.exec_cmd(terminal))'
    if sum(line.strip()==standard for line in text.splitlines())!=1:return text
    pattern=r'(?m)^(local terminal\s*=\s*)"kitty"(\s*(?:--[^\n]*)?)$'
    if len(re.findall(pattern,text))!=1:return text
    return re.sub(pattern,lambda match:match[1]+'styleCommand("terminal.sh")'+match[2],text)


def patch_switcher_bindings(text):
    block=(m.PACKAGE/'switcher-bindings.lua').read_text().strip()
    pattern=r'-- desktop-style window switcher begin\n.*?-- desktop-style window switcher end'
    owned=re.findall(pattern,text,re.S)
    if 'desktop-style window switcher' in text and (len(owned)!=1 or owned[0]!=block):
        print('Custom window-switcher block kept unchanged.');return text
    remainder=re.sub(pattern,'',text,flags=re.S) if owned else text
    for expression in re.findall(r'(?m)^[^\S\n]*hl\.bind\s*\(\s*([^,]+),',remainder):
        literal=re.fullmatch(r'''(["'])(.*?)\1''',expression.strip(),re.S)
        key=literal.group(2).upper().replace(' ','') if literal else expression.upper()
        conflict=('ALT_L' in key or 'ALT_R' in key or ('TAB' in key and (not literal or 'ALT' in key or 'MOD1' in key)))
        if conflict:
            print('Custom Alt/Tab bindings kept; window switcher shortcuts not added.')
            return remainder if owned else text
    return text if owned else text.rstrip()+'\n\n'+block+'\n'


def patch_bindings(text):
    mapping=json.loads((m.PACKAGE/'feedback-bindings.json').read_text())
    for before,action in mapping.items():text=text.replace('"'+before+'"','styleCommand("feedback.sh") .. " '+action+'"')
    if 'local function styleCommand(name)' not in text:raise RuntimeError('Current keybinds.lua needs adaptation to this appearance package.')
    text=text.replace('"dunstctl history-pop"','styleCommand("notifications.sh")')
    for key,action in [('XF86AudioRaiseVolume','volume up'),('XF86AudioLowerVolume','volume down'),('XF86AudioMute','volume mute'),('XF86AudioMicMute','microphone mute'),('XF86MonBrightnessUp','brightness up'),('XF86MonBrightnessDown','brightness down')]:
        matches=[line for line in text.splitlines() if 'hl.bind("'+key+'"' in line]
        if len(matches)!=1 or 'styleCommand("feedback.sh")' not in matches[0] or action not in matches[0]:raise RuntimeError('Custom media binding needs adaptation: '+key+'. Nothing changed.')
    b=[line for line in text.splitlines() if 'mainMod .. " + B"' in line]
    if len(b)!=1 or 'styleCommand("notifications.sh")' not in b[0]:raise RuntimeError('Super+B needs adaptation. Nothing changed.')
    lines=text.splitlines(keepends=True)
    matches=[i for i,line in enumerate(lines) if 'mainMod .. " + T"' in line]
    if len(matches)!=1:raise RuntimeError('Expected one Super+T binding. Nothing changed.')
    index=matches[0]
    if not any('styleCommand("'+name+'")' in lines[index] for name in ['applications.sh','hardware.sh']):
        raise RuntimeError('Custom Super+T binding needs adaptation. Nothing changed.')
    lines[index]=lines[index].replace('styleCommand("applications.sh")','styleCommand("hardware.sh")')
    return patch_switcher_bindings(patch_terminal(patch_file_manager(''.join(lines))))

def lock_config(text):
    block='# desktop-style media begin\nsource = '+str(m.STYLE/'hyprlock/media.conf')+'\n# desktop-style media end'
    text=re.sub(r'(?m)^(\s*hide_cursor\s*=\s*)true\s*$',r'\1false',text)
    if '# desktop-style media begin' in text:
        text=re.sub(r'# desktop-style media begin.*?# desktop-style media end',lambda _:block,text,flags=re.S)
    else:text=text.rstrip()+'\n\n'+block+'\n'
    return text

def check():
    if os.geteuid()==0:raise RuntimeError('Run as your normal desktop user, without sudo.')
    if not os.environ.get('HYPRLAND_INSTANCE_SIGNATURE'):raise RuntimeError('Run inside your active Hyprland session.')
    if not (m.STATE/'current-backup').is_file() or not m.STYLE.is_dir():raise RuntimeError('No installed appearance found. Use install.sh for a fresh installation.')
    if m.STYLE.is_symlink() or m.HYPR.is_symlink():raise RuntimeError('Linked installed app folders need adaptation.')
    for part in ['scripts','shell','hyprlock']:
        if (m.STYLE/part).is_symlink():raise RuntimeError('Linked theme folder needs adaptation: '+part)
    missing=[n for n in m.REQUIRED if shutil.which(n) is None]
    if missing:raise RuntimeError('Missing commands: '+', '.join(missing))
    version=m.run(['hyprctl','version'])
    if version.returncode or '0.56.2' not in version.stdout:raise RuntimeError('This package targets the supplied Hyprland 0.56.2 Lua configuration.')
    original=Path((m.STATE/'current-backup').read_text().strip())/'manifest.json'
    if not original.is_file():raise RuntimeError('The original restore manifest is missing.')
    ensure_clean_config();m.check_quickshell()
    return patch_bindings((m.HYPR/'keybinds.lua').read_text())

def original_manifest():return Path((m.STATE/'current-backup').read_text().strip())/'manifest.json'

def legacy_history(session):
    if (m.STATE/'notifications.json').exists() or not shutil.which('dunstctl'):
        return []
    if not any(Path(a[0]).name=='dunst' for _,a in session.processes()):
        return []
    try:
        result=m.run(['dunstctl','history'])
        if result.returncode:return []
        data=json.loads(result.stdout).get('data',[])
        rows=[entry for group in data for entry in (group if isinstance(group,list) else [group])]
        def field(row,name):
            value=row.get(name,'')
            return value.get('data','') if isinstance(value,dict) else value
        return [{'key':'legacy:'+str(field(row,'id') or index),'sourceId':None,
                 'app':str(field(row,'appname') or 'Notification')[:200],
                 'title':str(field(row,'summary'))[:300],
                 'body':re.sub(r'<[^>]*>','',str(field(row,'body')))[:2000],
                 'time':'Earlier','actions':[]}
                for index,row in enumerate(rows[:100]) if isinstance(row,dict) and field(row,'summary')]
    except (ValueError,TypeError,AttributeError):return []

def restart_previous(session,record):
    session.restore_services(record.get('services',{}))
    running=[a for _,a in session.processes()]
    for args in record['processes']:
        if args not in running:session.launch(args,'update-rollback.log')

def restore_snapshot(dest,record,session):
    session.stop_panel()
    shutil.rmtree(m.STYLE)
    shutil.copytree(dest/'style',m.STYLE,symlinks=True)
    keybinds=m.HYPR/'keybinds.lua'
    if record.get('keybinds_link') is not None:
        keybinds.unlink(missing_ok=True);keybinds.symlink_to(record['keybinds_link'])
    else:m.replace_bytes(keybinds,(dest/'keybinds.lua').read_bytes())
    lockfile=m.HYPR/'hyprlock.conf'
    if 'hyprlock_exists' in record:
        lockfile.unlink(missing_ok=True)
        if record.get('hyprlock_link') is not None:lockfile.symlink_to(record['hyprlock_link'])
        elif record['hyprlock_exists']:m.replace_bytes(lockfile,(dest/'hyprlock.conf').read_bytes(),(dest/'hyprlock.conf').stat().st_mode & 0o777)
    m.replace_bytes(original_manifest(),(dest/'original-manifest.json').read_bytes(),0o600)
    m.run(['hyprctl','reload'])
    restart_previous(session,record)

def update(check_only=False):
    text=check()
    if check_only:
        print('Update check passed. QuickShell QML compiled; original restore point and other desktop settings will be preserved.')
        return
    m.STATE.mkdir(parents=True,exist_ok=True)
    with (m.STATE/'update.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        dest=m.STATE/'revisions'/datetime.now().strftime('%Y%m%d-%H%M%S-%f');dest.mkdir(parents=True,mode=0o700)
        shutil.copytree(m.STYLE,dest/'style',symlinks=True)
        keybinds=m.HYPR/'keybinds.lua';shutil.copy2(keybinds,dest/'keybinds.lua')
        lockfile=m.HYPR/'hyprlock.conf'
        if lockfile.exists():shutil.copy2(lockfile,dest/'hyprlock.conf')
        shutil.copy2(original_manifest(),dest/'original-manifest.json')
        session=m.load_session(m.PACKAGE/'payload/style/scripts/session.py')
        imported_history=legacy_history(session)
        record={'hyprlock_exists':lockfile.exists(),'hyprlock_link':os.readlink(lockfile) if lockfile.is_symlink() else None,
                'keybinds_link':os.readlink(keybinds) if keybinds.is_symlink() else None,
                'processes':[a for _,a in session.processes() if session.managed(a)],
                'services':session.read_services(),'status':'prepared'}
        (dest/'manifest.json').write_text(json.dumps(record,indent=2))
        stopped=False;written=False
        try:
            stopped=True;session.suppress_services(record['services']);session.stop_panel()
            written=True
            for part in ['scripts','shell','hyprlock']:
                target=m.STYLE/part
                if target.exists():shutil.rmtree(target)
                shutil.copytree(m.PACKAGE/'payload/style'/part,target)
            for script in (m.STYLE/'scripts').glob('*.sh'):script.chmod(0o755)
            fragment=m.STYLE/'hyprlock/media.conf'
            m.replace_text(fragment,fragment.read_text().replace('@STYLE@',str(m.STYLE)))
            m.replace_text(keybinds,text)
            m.replace_text(lockfile,lock_config(lockfile.read_text() if lockfile.exists() else ''))
            original=json.loads(original_manifest().read_text())
            if 'desktop_services' not in original:
                original['desktop_services']=record['services']
                m.replace_text(original_manifest(),json.dumps(original,indent=2),0o600)
            result=m.run(['hyprctl','reload'])
            if result.returncode:raise RuntimeError('Reload failed: '+result.stdout+result.stderr)
            ensure_clean_config()
            if imported_history and not (m.STATE/'notifications.json').exists():
                m.replace_text(m.STATE/'notifications.json',json.dumps({'version':1,'dnd':False,'unread':0,'history':imported_history},ensure_ascii=False),0o600)
            session.start();time.sleep(.5)
            if not session.feedback_ready():raise RuntimeError('Shell readiness was lost after the update.')
        except Exception:
            if written:restore_snapshot(dest,record,session)
            elif stopped:restart_previous(session,record)
            record['status']='rolled-back';(dest/'manifest.json').write_text(json.dumps(record,indent=2))
            print('Update cancelled; previous desktop restored. Snapshot: '+str(dest),file=sys.stderr)
            raise
        record['status']='installed';record['installed_keybinds_sha256']=hashlib.sha256(keybinds.read_bytes()).hexdigest()
        record['installed_hyprlock_sha256']=hashlib.sha256(lockfile.read_bytes()).hexdigest()
        (dest/'manifest.json').write_text(json.dumps(record,indent=2))
        m.replace_text(m.STATE/'last-update',str(dest),0o600)
        print('Updated. QuickShell owns the bar, application/session menus, controls, notifications, media and feedback.')
        print('Original restore point retained. Revision snapshot: '+str(dest))
        print('Undo this update: bash '+str(m.PACKAGE/'rollback-update.sh'))

def rollback(check_only=False):
    if os.geteuid()==0:raise RuntimeError('Run without sudo.')
    pointer=m.STATE/'last-update'
    if not pointer.is_file():raise RuntimeError('No update revision to roll back.')
    dest=Path(pointer.read_text().strip());record=json.loads((dest/'manifest.json').read_text())
    keybinds=m.HYPR/'keybinds.lua'
    if hashlib.sha256(keybinds.read_bytes()).hexdigest()!=record.get('installed_keybinds_sha256'):
        raise RuntimeError('keybinds.lua changed after the update. Your changes were kept; adapt the rollback first.')
    if record.get('installed_hyprlock_sha256'):
        lockfile=m.HYPR/'hyprlock.conf'
        if not lockfile.is_file() or hashlib.sha256(lockfile.read_bytes()).hexdigest()!=record['installed_hyprlock_sha256']:
            raise RuntimeError('hyprlock.conf changed after the update. Your changes were kept; adapt the rollback first.')
    if check_only:print('Rollback check passed.');return
    with (m.STATE/'update.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        saved=dest/'before-rollback'
        if not saved.exists():shutil.copytree(m.STYLE,saved,symlinks=True)
        session=m.load_session(m.PACKAGE/'payload/style/scripts/session.py')
        restore_snapshot(dest,record,session)
        pointer.unlink();print('Previous desktop revision restored. Current edits retained at '+str(saved))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--rollback',action='store_true');args=parser.parse_args()
    try:(rollback if args.rollback else update)(args.check)
    except Exception as exc:print('Stopped: '+str(exc),file=sys.stderr);sys.exit(1)
