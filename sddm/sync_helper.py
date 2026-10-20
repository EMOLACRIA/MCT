#!/usr/bin/python3 -I
"""Privileged boundary: select only root-installed SDDM skins, with root-owned undo records."""
import base64
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

STATE=Path('/var/lib/desktop-style-theme-sync')
CATALOG=Path('/usr/share/sddm/themes/desktop-style-sync')
CONFIG=Path('/etc/sddm.conf')
HELPER=Path('/usr/lib/desktop-style/theme-sddm')
LIVE=Path('/usr/share/sddm/themes/desktop-style')
ID=re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
TOKEN=re.compile(r'[0-9a-f]{32}\Z')


def read(path):
    if path.is_symlink(): raise ValueError('Symlinked system state is unsupported.')
    return json.loads(path.read_text())


def atomic(path,data,mode=0o600):
    if path.is_symlink(): raise ValueError('Symlinked system file kept: '+str(path))
    fd,name=tempfile.mkstemp(prefix='.mct-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.chmod(name,mode);os.replace(name,path)
    finally:Path(name).unlink(missing_ok=True)


def write(path,obj):atomic(path,(json.dumps(obj,sort_keys=True)+'\n').encode())


def selection(text,theme,catalog):
    lines=text.splitlines(keepends=True);starts=[i for i,x in enumerate(lines) if x.strip()=='[Theme]']
    if len(starts)>1: raise ValueError('Duplicate SDDM [Theme] sections need adaptation.')
    values={'Current':theme,'ThemeDir':str(catalog)}
    if not starts:return text.rstrip()+'\n\n[Theme]\n'+''.join(k+'='+v+'\n' for k,v in values.items())
    start=starts[0]+1;end=next((i for i in range(start,len(lines)) if lines[i].lstrip().startswith('[')),len(lines))
    for key,value in values.items():
        indices=[i for i in range(start,end) if re.match(r'^\s*'+key+r'\s*=',lines[i])]
        if len(indices)>1:raise ValueError('Duplicate SDDM theme key needs adaptation.')
        if indices:lines[indices[0]]=key+'='+value+'\n'
        else:lines.insert(end,key+'='+value+'\n');end+=1
    return ''.join(lines)


class Backend:
    def __init__(self,state=STATE,catalog=CATALOG,config=CONFIG,live=None):
        self.state=Path(state);self.catalog=Path(catalog);self.config=Path(config);self.live=Path(live) if live else self.catalog.parent/"desktop-style"
    @contextmanager
    def locked(self):
        with (self.state/'operation.lock').open('a') as f:
            fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);yield
    def settings(self,uid):
        data=read(self.state/'catalog.json')
        if data.get('schema')!=1 or data.get('uid')!=uid or uid==0:raise ValueError('This desktop user is not enrolled for SDDM theme switching.')
        return data
    def snapshot(self):
        p=self.config
        if p.is_symlink() or (p.exists() and not p.is_file()):raise ValueError('Custom SDDM config path kept.')
        data=p.read_bytes() if p.exists() else None
        return dict(exists=data is not None,body=base64.b64encode(data).decode() if data is not None else '',
                    sha=hashlib.sha256(data).hexdigest() if data is not None else None,
                    mode=stat.S_IMODE(p.stat().st_mode) if p.exists() else 0o644)
    def live_target(self):
        if not self.live.is_symlink():raise ValueError('Stable SDDM theme path needs the one-time sync setup.')
        target=Path(os.readlink(self.live))
        if target.parent!=self.catalog or not (target/'Main.qml').is_file():raise ValueError('SDDM theme link is outside the root-installed catalogue.')
        return str(target)
    def set_live(self,target):
        target=Path(target)
        if target.parent!=self.catalog or not (target/'Main.qml').is_file():raise ValueError('Invalid installed SDDM target.')
        if self.live.exists() and not self.live.is_symlink():raise ValueError('Custom SDDM theme directory was kept.')
        temp=self.live.with_name('.mct-theme-'+os.urandom(8).hex())
        try:temp.symlink_to(target);os.replace(temp,self.live)
        finally:temp.unlink(missing_ok=True)
    def guard(self):
        state=read(self.state/'current.json')
        if self.live_target()!=state['live']:raise ValueError('SDDM theme link changed outside the switcher; edits kept.')
        if self.snapshot()['sha']!=state['sha']:raise ValueError('SDDM configuration changed outside the theme switcher; edits kept.')
        return state
    def theme(self,data,theme,fingerprint):
        if not ID.fullmatch(theme) or theme not in data['themes']:raise ValueError('SDDM theme was not installed by the system setup.')
        if fingerprint!=data['themes'][theme]['fingerprint']:raise ValueError('SDDM skin cache is outdated. Run the one-time SDDM sync setup again.')
        if not (self.catalog/theme/'Main.qml').is_file():raise ValueError('Installed SDDM skin is incomplete.')
    def transaction(self,uid,token):
        self.settings(uid)
        if not TOKEN.fullmatch(token):raise ValueError('Invalid SDDM transaction id.')
        p=self.state/'transactions'/ (token+'.json')
        if not p.exists():return p,None
        record=read(p)
        if record['uid']!=uid:raise ValueError('SDDM snapshot belongs to another desktop user.')
        return p,record
    def check(self,uid,theme,fingerprint):
        data=self.settings(uid);self.theme(data,theme,fingerprint);self.guard()
        if (self.state/'pending.json').exists():raise ValueError('An SDDM theme operation needs recovery.')
        return dict(ok=True)
    def prepare(self,uid,token,theme=None,fingerprint=None,restore=None):
        if not TOKEN.fullmatch(token):raise ValueError('Invalid SDDM transaction id.')
        data=self.settings(uid);beforestate=self.guard()
        pending=self.state/'pending.json'
        if pending.exists():
            value=read(pending)
            if value['token']==token and value['uid']==uid:return dict(ok=True,token=token)
            raise ValueError('Another SDDM theme operation needs recovery.')
        dest,old=self.transaction(uid,token)
        if old is not None:raise ValueError('SDDM transaction id already used.')
        before=self.snapshot();beforelive=self.live_target()
        if restore is not None:
            _,original=self.transaction(uid,restore)
            if original is None or original['status'] not in ('committed','applied','rolled-back'):raise ValueError('SDDM undo snapshot not found.')
            after=original['beforeConfig'];selected=original['beforeState']['theme'];afterlive=original['beforeLive']
        else:
            self.theme(data,theme,fingerprint)
            body=selection(base64.b64decode(before['body']).decode('utf-8',errors='surrogateescape'),'desktop-style',self.catalog.parent).encode('utf-8',errors='surrogateescape')
            after=dict(exists=True,body=base64.b64encode(body).decode(),sha=hashlib.sha256(body).hexdigest(),mode=before['mode']);selected=theme;afterlive=str(self.catalog/theme)
        record=dict(uid=uid,token=token,beforeConfig=before,beforeState=beforestate,afterConfig=after,beforeLive=beforelive,afterLive=afterlive,theme=selected,status='prepared')
        write(dest,record);write(pending,dict(uid=uid,token=token));return dict(ok=True,token=token)
    def restore_config(self,value):
        if value['exists']:atomic(self.config,base64.b64decode(value['body']),value['mode'])
        else:self.config.unlink(missing_ok=True)
    def apply(self,uid,token):
        path,r=self.transaction(uid,token)
        if r is None:raise ValueError('Missing SDDM preparation.')
        pending=read(self.state/'pending.json')
        if pending!={'uid':uid,'token':token}:raise ValueError('SDDM operation owner changed.')
        actual=self.snapshot()['sha']
        if actual not in (r['beforeConfig']['sha'],r['afterConfig']['sha']):raise ValueError('SDDM edited during the switch; edits kept.')
        if self.live_target() not in (r['beforeLive'],r['afterLive']):raise ValueError('SDDM link was edited during the switch.')
        self.set_live(r['afterLive']);self.restore_config(r['afterConfig'])
        write(self.state/'current.json',dict(theme=r['theme'],sha=r['afterConfig']['sha'],live=r['afterLive'],token=token))
        r['status']='applied';write(path,r);return dict(ok=True)
    def finish(self,uid,token):
        path,r=self.transaction(uid,token)
        if r is None or r['status'] not in ('applied','committed'):raise ValueError('SDDM operation is not applied.')
        state=self.guard()
        if state['token']!=token:raise ValueError('SDDM operation no longer owns the selection.')
        r['status']='committed';write(path,r)
        pending=self.state/'pending.json'
        if pending.exists() and read(pending)=={'uid':uid,'token':token}:pending.unlink()
        return dict(ok=True)
    def rollback(self,uid,token):
        path,r=self.transaction(uid,token)
        if r is None:return dict(ok=True,status='not-started')
        if r['status']=='rolled-back':return dict(ok=True)
        actual=self.snapshot()['sha'];state=read(self.state/'current.json')
        if actual not in (r['beforeConfig']['sha'],r['afterConfig']['sha']):raise ValueError('SDDM recovery kept your later configuration edits.')
        # An interrupted atomic config write may precede the state-file update.
        if state['token'] not in (token,r['beforeState']['token']):raise ValueError('A newer SDDM selection is present; it was kept.')
        if self.live_target() not in (r['beforeLive'],r['afterLive']):raise ValueError('SDDM recovery kept a later theme link edit.')
        self.set_live(r['beforeLive']);self.restore_config(r['beforeConfig']);write(self.state/'current.json',r['beforeState'])
        r['status']='rolled-back';write(path,r)
        pending=self.state/'pending.json'
        if pending.exists() and read(pending)=={'uid':uid,'token':token}:pending.unlink()
        return dict(ok=True)


def main():
    if os.geteuid()!=0:raise ValueError('This helper must be invoked through its installed polkit action.')
    value=os.environ.get('PKEXEC_UID','')
    if not re.fullmatch(r'[1-9][0-9]*',value):raise ValueError('Missing authenticated desktop identity.')
    uid=int(value)
    for p in (HELPER,HELPER.parent,STATE,CATALOG,LIVE.parent):
        st=p.lstat()
        if stat.S_ISLNK(st.st_mode) or st.st_uid!=0 or stat.S_IMODE(st.st_mode)&0o022:raise ValueError('Untrusted system helper installation.')
    b=Backend();args=sys.argv[1:]
    with b.locked():
        if len(args)==3 and args[0]=='check':result=b.check(uid,args[1],args[2])
        elif len(args)==4 and args[0]=='prepare':result=b.prepare(uid,args[1],args[2],args[3])
        elif len(args)==3 and args[0]=='prepare-restore':result=b.prepare(uid,args[1],restore=args[2])
        elif len(args)==2 and args[0] in ('apply','finish','rollback'):result=getattr(b,args[0])(uid,args[1])
        else:raise ValueError('Only reviewed SDDM theme operations are accepted.')
    print(json.dumps(result))

if __name__=='__main__':
    try:main()
    except Exception as exc:print(json.dumps(dict(ok=False,error=str(exc))));sys.exit(1)
