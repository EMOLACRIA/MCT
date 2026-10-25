"""Core-owned theme participants. No package commands, privileged paths or hooks are accepted."""
import argparse
import configparser
from contextlib import contextmanager, ExitStack
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
from types import SimpleNamespace
import uuid

_quote_spec=importlib.util.spec_from_file_location('_mct_fastfetch_quotes',Path(__file__).with_name('fastfetch_quotes.py'))
_quotes=importlib.util.module_from_spec(_quote_spec);_quote_spec.loader.exec_module(_quotes)
QUOTES=_quotes.QUOTES;quote_asset=_quotes.quote_asset;quote_png=_quotes.quote_png;image_logo=_quotes.image_logo

HELPER=Path('/usr/lib/desktop-style/theme-sddm')

def sha(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
def load(path):
    spec=importlib.util.spec_from_file_location('_mct_integration_'+path.stem,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def safe_file(path):
    path=Path(path)
    if not path.is_absolute():raise ValueError('Integration target must be absolute.')
    for part in (path,*path.parents):
        if part.is_symlink():raise ValueError('Linked integration target needs adaptation: '+str(part))
    if path.exists() and not path.is_file():raise ValueError('Non-file integration target kept: '+str(path))
    return path


class Sddm:
    def call(self,*args):
        if not HELPER.is_file() or HELPER.is_symlink():raise ValueError('Run the one-time SDDM sync setup first: sudo python3 sddm/sync_setup.py install --user "$USER"')
        st=HELPER.stat()
        if st.st_uid!=0 or st.st_mode&0o022:raise ValueError('SDDM system helper ownership needs repair.')
        p=subprocess.run(['pkexec','--disable-internal-agent',str(HELPER),*args],capture_output=True,text=True,timeout=25)
        try:value=json.loads(p.stdout)
        except ValueError:raise ValueError('SDDM helper did not answer. Use an active local desktop session; check the one-time setup.')
        if p.returncode or not value.get('ok'):raise ValueError(value.get('error','SDDM operation was rejected.'))
        return value


class SpotifySession:
    def __init__(self,client,launch):self.client=Path(client);self.launch=Path(launch)
    def processes(self):
        result=[]
        for proc in Path('/proc').glob('[0-9]*'):
            try:
                if proc.stat().st_uid!=os.getuid():continue
                args=[x.decode('utf-8',errors='surrogateescape') for x in (proc/'cmdline').read_bytes().split(b'\0') if x]
                if not args or Path(args[0]).name!='spotify' or any(x.startswith('--type=') for x in args[1:]):continue
                exe=(proc/'exe').resolve()
                if exe!=self.client/'spotify':raise ValueError('An unmanaged Spotify instance is open. Close it and open your themed Spotify/adblock launcher first.')
                preload=next((x.split(b'=',1)[1].decode() for x in (proc/'environ').read_bytes().split(b'\0') if x.startswith(b'LD_PRELOAD=')),None)
                result.append(dict(pid=int(proc.name),args=args[1:],preload=preload))
            except (FileNotFoundError,PermissionError,ProcessLookupError):pass
        return result
    def player(self,*args):
        try:
            p=subprocess.run(['playerctl','-p','spotify',*args],capture_output=True,text=True,timeout=2)
            return p.stdout.strip() if p.returncode==0 else None
        except (OSError,subprocess.SubprocessError):return None
    def capture(self):
        processes=self.processes()
        if len(processes)>1:raise ValueError('Multiple Spotify main processes are open; close extra instances before switching.')
        if not processes:return None
        result=processes[0];result['status']=self.player('status');result['position']=self.player('position');result['uri']=self.player('metadata','xesam:url');return result
    def stop(self):
        processes=self.processes()
        for p in processes:os.kill(p['pid'],signal.SIGTERM)
        deadline=time.monotonic()+5
        while self.processes():
            if time.monotonic()>deadline:raise ValueError('Spotify did not close; no new instance was forced.')
            time.sleep(.05)
    def restart(self,saved):
        if not saved:return
        if self.processes():return
        env=dict(os.environ)
        if saved.get('preload'):env['LD_PRELOAD']=saved['preload']
        elif 'LD_PRELOAD' in env:env.pop('LD_PRELOAD')
        args=list(saved.get('args',[]));uri=saved.get('uri')
        if uri and re.fullmatch(r'(?:spotify:(?:track|episode|album|playlist):[A-Za-z0-9]+|https://open.spotify.com/(?:track|episode)/[A-Za-z0-9]+)',uri):
            args=[x for x in args if not x.startswith(('spotify:','https://open.spotify.com/'))]+[uri]
        subprocess.Popen([str(self.launch),*args],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
        deadline=time.monotonic()+8
        while not self.processes():
            if time.monotonic()>deadline:raise ValueError('The themed Spotify client did not start again.')
            time.sleep(.1)
        # MPRIS recovery is best-effort; no debug port, JS injection or new external API.
        if saved.get('status'):
            deadline=time.monotonic()+4
            while not self.player('status') and time.monotonic()<deadline:time.sleep(.1)
            self.player('pause')
            position=saved.get('position')
            if position and re.fullmatch(r'\d+(?:\.\d+)?',position):self.player('position',position)
            if saved['status']=='Playing':self.player('play')


class Integrations:
    def __init__(self,engine,sddm=None,session=None):
        self.engine=engine;self.data=engine.data/'integrations';self.profile=self.data/'profile.json';self.sddm=sddm or Sddm()
        home=Path.home();self.config=Path(os.environ.get('XDG_CONFIG_HOME',home/'.config'));self.userdata=Path(os.environ.get('XDG_DATA_HOME',home/'.local/share'));self.state=Path(os.environ.get('XDG_STATE_HOME',home/'.local/state'))
        self.spotify=self.userdata/'desktop-style-apps/spotify';self.session=session or SpotifySession(self.spotify/'client',self.spotify/'launch.sh')
        self.cached=None
    def settings(self):
        if not self.profile.exists():return None
        value=json.loads(safe_file(self.profile).read_text())
        if value.get('schema')!=1 or type(value.get('enabled')) is not bool or not isinstance(value.get('fastfetchConfig'),str) or type(value.get('dolphin',False)) is not bool:raise ValueError('Invalid integration settings.')
        safe_file(Path(value['fastfetchConfig']));return value
    @contextmanager
    def lease(self):
        if self.settings() is None:
            yield;return
        terminal=self.terminal()
        with ExitStack() as stack:
            for directory in (terminal.STATE,self.state/'desktop-style-apps'):
                safe_file(directory/'install.lock');directory.mkdir(parents=True,exist_ok=True,mode=0o700)
                handle=stack.enter_context((directory/'install.lock').open('a'))
                try:fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
                except BlockingIOError:raise ValueError('A manual application/Fastfetch install is running. Try the theme switch again when it finishes.')
            yield
    def enabled(self):
        p=self.settings();return bool(p and p['enabled'])
    def dolphin_enabled(self):
        p=self.settings();return bool(p and p.get('dolphin'))
    def terminal(self):return load(self.engine.root/'terminal-medallion/terminal.py')
    def source(self,theme,adapter):
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',theme):raise ValueError('Invalid adapter theme id.')
        if theme=='plague-tale':return {'terminal':self.engine.root/'terminal-medallion','spotify':self.engine.root/'apps/spotify','sddm':self.engine.root/'sddm/theme','dolphin':self.engine.root/'apps/dolphin'}[adapter]
        return self.engine.root/'themes'/theme/'adapters'/adapter
    def greeter_fingerprint(self,theme):
        common=self.engine.root/'sddm/theme';files={p.name:p for p in common.iterdir() if p.is_file()}
        if theme!='plague-tale':
            for p in self.source(theme,'sddm').iterdir():
                if p.is_symlink() or not p.is_file() or p.name=='Main.qml':raise ValueError('Invalid SDDM visual source.')
                files[p.name]=p
        h=hashlib.sha256()
        for name,p in sorted(files.items()):
            safe_file(p);h.update(name.encode()+b'\0'+hashlib.sha256(p.read_bytes()).digest())
        return h.hexdigest()
    def spotify_paths(self):
        base=self.spotify/'config/spicetify/Themes/DesktopStyle'
        return [self.spotify/'client/Apps/xpui/colors.css',self.spotify/'client/Apps/xpui/user.css',base/'color.ini',base/'user.css',self.state/'desktop-style-apps/spotify.json']
    def paths(self):
        profile=self.settings()
        if profile is None:raise ValueError('Integration settings are missing; restore them before recovering.')
        terminal=self.terminal()
        return [Path(profile['fastfetchConfig']),terminal.ASSET,terminal.STATE/'current.json',*self.spotify_paths(),self.data/'owned.json']
    def verify_owned(self):
        p=self.data/'owned.json'
        if not p.is_file():raise ValueError('Integration ownership record is missing.')
        owned=json.loads(p.read_text());expected={str(p) for p in self.paths() if p!=self.data/'owned.json'}
        if set(owned)!=expected:raise ValueError('Integration ownership inventory differs.')
        for name,want in owned.items():
            p=safe_file(Path(name));actual=sha(p.read_bytes()) if p.is_file() else None
            if actual!=want:raise ValueError('Integrated file was edited; changes kept: '+name)
        self.verify_quote_owned()
    def quote_path(self):return self.terminal().ASSET.with_name('quote.png')
    def verify_quote_owned(self):
        path=safe_file(self.quote_path());marker=self.terminal().STATE/'current.json'
        record=json.loads(marker.read_text()) if marker.is_file() else {}
        expected=record.get('image_sha256')
        if record.get('image') not in (None,str(path)):raise ValueError('Fastfetch quote image path changed.')
        actual=sha(path.read_bytes()) if path.is_file() else None
        if actual!=expected:raise ValueError('Fastfetch quote image was edited or is untracked; changes kept: '+str(path))
    def spotify_plan(self,theme):
        paths=self.spotify_paths();pointer=paths[-1]
        if not pointer.is_file() or not (self.spotify/'client/spotify').is_file() or not (self.spotify/'launch.sh').is_file():raise ValueError('Install the managed Spotify adapter once before enabling theme sync: bash apps/install.sh spotify --theme '+theme)
        record=json.loads(pointer.read_text())
        for path,text in record.get('launchers',{}).items():
            if not Path(path).is_file() or Path(path).read_text()!=text:raise ValueError('Spotify launcher changed; it was kept: '+path)
        xpui=self.spotify/'client/Apps/xpui'
        meta=json.loads((xpui/'spicetify-config.json').read_text())
        if meta.get('theme_name')!='DesktopStyle' or meta.get('scheme_name')!='Ash':raise ValueError('Spotify private client is not the reviewed DesktopStyle/Ash installation.')
        app=load(self.engine.root/'apps/manage.py');tags=app.ScriptTags();tags.feed((xpui/'index.html').read_text())
        if not {'colors.css','user.css'}<={s.split('?')[0].lstrip('/') for s in tags.stylesheets}:raise ValueError('Spotify CSS entry points are missing.')
        source=self.source(theme,'spotify');ini=(source/'color.ini').read_bytes();css=(source/'user.css').read_bytes()
        palette=configparser.ConfigParser(interpolation=None);palette.read_string(ini.decode());lines=[]
        for key,value in palette['Ash'].items():
            if not re.fullmatch(r'[a-z][a-z0-9-]*',key) or not re.fullmatch(r'[0-9a-fA-F]{6}',value):raise ValueError('Unsupported Spotify palette value.')
            rgb=', '.join(str(int(value[i:i+2],16)) for i in (0,2,4));lines.extend(['--spice-'+key+': #'+value+';','--spice-rgb-'+key+': '+rgb+';'])
        colors=(':root {\n'+ '\n'.join(lines)+'\n}\n').encode();record['theme']=theme
        return dict(zip(paths,[colors,css,ini,css,encoded(record)]))
    def fastfetch_plan(self,theme):
        t=self.terminal();profile=self.settings();marker=t.STATE/'current.json'
        if not marker.is_file():raise ValueError('The Fastfetch adapter must be enrolled once: bash theme.sh integrations enable')
        record=json.loads(marker.read_text());compact=record.get('variant')=='compact'
        args=SimpleNamespace(config=profile['fastfetchConfig'],compact=compact,theme=theme,check=True)
        target,_,updated=t.preflight(args);asset=quote_asset(theme)
        image=None
        if asset is None:
            asset=t.source_asset(args).read_bytes();record.pop('image',None);record.pop('image_sha256',None)
        else:
            color=t.logo(args,t.ASSET).get('color',{}).get('1','#ffffff')
            image=quote_png(theme,color);updated=t.with_logo(updated,image_logo(self.quote_path(),compact,theme=theme))
            record.update(image=str(self.quote_path()),image_sha256=sha(image))
        record.update(asset=str(t.ASSET),variant='compact' if compact else 'detailed',revision='quote-png-1' if image else 'cp437-1.3',theme=theme,asset_sha256=sha(asset),installed_sha256=sha(updated.encode()))
        return {target:updated.encode(),t.ASSET:asset,marker:encoded(record),self.quote_path():image}
    def dolphin_paths(self):
        icons=self.engine.root/'apps/dolphin/icons'
        files=sorted(p.relative_to(icons) for p in icons.rglob('*') if p.is_file())
        if any(p.is_symlink() for p in icons.rglob('*')):raise ValueError('Linked Dolphin icon source was kept.')
        return [self.userdata/'color-schemes/DesktopStyle.colors',self.userdata/'color-schemes/DesktopStyle-Qt.conf',
                *(self.userdata/'icons/DesktopStyle'/p for p in files),self.state/'desktop-style-apps/dolphin.json',self.data/'dolphin-owned.json']
    def dolphin_plan(self,theme):
        paths=self.dolphin_paths();pointer=paths[-2]
        if not pointer.is_file():raise ValueError('Install the Dolphin adapter once with Dolphin closed: bash apps/install.sh dolphin --theme '+theme)
        record=json.loads(safe_file(pointer).read_text());app=load(self.engine.root/'apps/manage.py')
        rc=safe_file(self.config/'dolphinrc').read_text();qt=safe_file(self.config/'qt6ct/qt6ct.conf').read_text()
        for group,key,value in app.DOLPHIN_KEYS:
            if app.key_value(rc,group,key)!=value:raise ValueError('Dolphin appearance settings changed; they were kept.')
        for key,value in {'color_scheme_path':str(paths[1]),'custom_palette':'true','icon_theme':'DesktopStyle','style':'Fusion'}.items():
            if app.key_value(qt,'Appearance',key)!=value:raise ValueError('Dolphin qt6ct settings changed; they were kept.')
        launcher=safe_file(self.userdata/'applications/org.kde.dolphin.desktop')
        if not record.get('launcher') or not launcher.is_file() or launcher.read_text()!=record['launcher']:raise ValueError('Dolphin launcher changed; it was kept.')
        source=self.source(theme,'dolphin');source_files={p.relative_to(source/'icons') for p in (source/'icons').rglob('*') if p.is_file()}
        expected={p.relative_to(self.userdata/'icons/DesktopStyle') for p in paths[2:-2]}
        if source_files!=expected:raise ValueError('Dolphin icon inventory changed; review the adapter before enrolling it.')
        colors=safe_file(source/'DesktopStyle.colors').read_bytes()
        palette=configparser.ConfigParser(interpolation=None);palette.read_string(colors.decode())
        for section in ('Colors:View','Colors:Selection','Colors:Window'):
            if palette[section]['ForegroundNormal'].replace(' ','')!='255,255,255':raise ValueError('Dolphin text must remain white.')
        app.SELECTED_THEME=theme
        # Use the existing first-theme palette; other themes supply their own Qt.conf.
        qt_palette=app.qt_palette().encode() if theme=='plague-tale' else safe_file(source/'Qt.conf').read_bytes()
        output={paths[0]:colors,paths[1]:qt_palette}
        for p in paths[2:-2]:output[p]=safe_file(source/'icons'/p.relative_to(self.userdata/'icons/DesktopStyle')).read_bytes()
        record['theme']=theme;output[pointer]=encoded(record)
        for p in output:safe_file(p)
        output[paths[-1]]=encoded({str(p):sha(data) for p,data in output.items()})
        return output
    def verify_dolphin_owned(self):
        owner=self.data/'dolphin-owned.json'
        if not owner.is_file():raise ValueError('Dolphin ownership is missing; run integrations enable --dolphin once.')
        expected={str(p) for p in self.dolphin_paths() if p!=owner};owned=json.loads(safe_file(owner).read_text())
        if set(owned)!=expected:raise ValueError('Dolphin ownership inventory differs.')
        for name,want in owned.items():
            p=safe_file(Path(name));actual=sha(p.read_bytes()) if p.is_file() else None
            if actual!=want:raise ValueError('Dolphin managed file was edited; changes kept: '+name)
    def notify_dolphin(self):
        # qt6ct watches its configuration DIRECTORY, debounces for 3 seconds,
        # reapplies the palette and invalidates its icon loader. No process kill.
        import tempfile
        directory=safe_file(self.config/'qt6ct/qt6ct.conf').parent
        fd,name=tempfile.mkstemp(prefix='.mct-refresh-',dir=directory)
        os.close(fd);Path(name).unlink()
    def plan(self,theme):
        self.engine.load(theme)
        fastfetch=self.fastfetch_plan(theme);quote={self.quote_path():fastfetch.pop(self.quote_path())}
        output={**fastfetch,**self.spotify_plan(theme)}
        for path in output:safe_file(path)
        output[self.data/'owned.json']=encoded({str(p):sha(data) for p,data in output.items()})
        fingerprint=self.greeter_fingerprint(theme)
        return dict(output=output,theme=theme,fingerprint=fingerprint,quote=quote,dolphin=self.dolphin_plan(theme) if self.dolphin_enabled() else None)
    def preflight(self,theme):
        if not self.enabled():return
        self.verify_owned()
        if self.dolphin_enabled():self.verify_dolphin_owned()
        self.cached=self.plan(theme)
        self.sddm.call('check',theme,self.cached['fingerprint']);self.session.capture()
    def fingerprint(self,theme):
        if not self.enabled():return None
        plan=self.cached if self.cached and self.cached['theme']==theme else self.plan(theme)
        h=hashlib.sha256(plan['fingerprint'].encode())
        for p,data in sorted(plan['output'].items(),key=lambda item:str(item[0])):h.update(str(p).encode()+b'\0'+data)
        for p,data in sorted((plan.get('dolphin') or {}).items(),key=lambda item:str(item[0])):h.update(str(p).encode()+b'\0'+data)
        for p,data in plan['quote'].items():h.update(str(p).encode()+b'\0'+(data or b''))
        return h.hexdigest()
    def capture(self,dest,theme=None,restore=None):
        if not self.enabled() and restore is None:return None
        self.verify_owned()
        if restore is None:
            plan=self.cached if self.cached and self.cached['theme']==theme else self.plan(theme)
            output=plan['output'];fingerprint=plan['fingerprint'];restore_token=None
            dolphin=plan.get('dolphin')
            quote=plan['quote']
        else:
            previous,meta=restore;self.verify_snapshot(previous,meta,expect_after=True)
            output={Path(row['path']):(previous/row['before']).read_bytes() if row['before'] is not None else None for row in meta['files']}
            # 0.1.0 transactions have no Dolphin journal: sync their prior theme
            # while retaining the original core/application rollback contract.
            if meta.get('dolphin') is not None:
                dolphin={Path(row['path']):(previous/row['before']).read_bytes() if row['before'] is not None else None for row in meta['dolphin']}
            else:dolphin=self.dolphin_plan(theme) if self.dolphin_enabled() else None
            quote={Path(row['path']):(previous/row['before']).read_bytes() if row['before'] is not None else None for row in meta['quote']} if meta.get('quote') is not None else {self.quote_path():None}
            theme=None;fingerprint=None;restore_token=meta['rootToken']
        allowed=set(self.paths())
        if set(output)!=allowed:raise ValueError('Unexpected integration snapshot paths.')
        files=self.capture_files(dest,output,'integrations')
        dolphin_files=None
        if dolphin is not None:
            self.verify_dolphin_owned();dolphin_files=self.capture_files(dest,dolphin,'dolphin')
        quote_files=self.capture_files(dest,quote,'quote')
        return dict(schema=1,rootToken=uuid.uuid4().hex,restoreToken=restore_token,theme=theme,fingerprint=fingerprint,files=files,quote=quote_files,dolphin=dolphin_files,spotify=self.session.capture())
    def capture_files(self,dest,output,prefix):
        folder=dest/prefix;folder.mkdir(mode=0o700)
        files=[]
        for i,(path,after) in enumerate(sorted(output.items(),key=lambda item:str(item[0]))):
            path=safe_file(path);before=path.read_bytes() if path.is_file() else None
            row=dict(path=str(path),before=None,after=None,beforeSha=sha(before) if before is not None else None,afterSha=sha(after) if after is not None else None,mode=path.stat().st_mode&0o777 if path.exists() else 0o644)
            for label,data in [('before',before),('after',after)]:
                if data is not None:
                    name=prefix+'/'+str(i)+'.'+label;self.engine_atomic(dest/name,data);row[label]=name
            files.append(row)
        return files
    def engine_atomic(self,path,data,mode=0o600):
        # Keep the core's safe path / fsync implementation without importing a second Engine.
        import tempfile
        safe_file(path);path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        fd,name=tempfile.mkstemp(prefix='.sync-',dir=path.parent)
        try:
            with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
            os.chmod(name,mode);os.replace(name,path)
        finally:Path(name).unlink(missing_ok=True)
    def verify_snapshot(self,dest,meta,expect_after=False):
        if not isinstance(meta,dict):raise ValueError('Invalid integration transaction.')
        if meta.get('schema')!=1 or not re.fullmatch(r'[0-9a-f]{32}',meta.get('rootToken','')):raise ValueError('Invalid integration transaction.')
        self.verify_files(dest,meta.get('files'),self.paths(),'integrations',expect_after)
        if meta.get('dolphin') is not None:self.verify_files(dest,meta['dolphin'],self.dolphin_paths(),'dolphin',expect_after)
        if meta.get('quote') is not None:self.verify_files(dest,meta['quote'],[self.quote_path()],'quote',expect_after)
    def verify_files(self,dest,files,allowed,prefix,expect_after):
        if not isinstance(files,list) or len(files)!=len(allowed) or not all(isinstance(r,dict) and isinstance(r.get('path'),str) and type(r.get('mode')) is int and 0<=r['mode']<=0o777 for r in files):raise ValueError('Invalid integration file inventory.')
        if {Path(r['path']) for r in files}!=set(allowed):raise ValueError('Integration recovery target inventory changed.')
        for row in files:
            path=safe_file(Path(row['path']));actual=sha(path.read_bytes()) if path.exists() else None
            valid=(row['afterSha'],) if expect_after else (row['beforeSha'],row['afterSha'])
            if actual not in valid:raise ValueError('Integration recovery kept a later edit: '+str(path))
            for key in ('before','after'):
                name=row[key]
                if name is None:continue
                if not re.fullmatch(prefix+r'/\d+\.(before|after)',name):raise ValueError('Unsafe integration snapshot name.')
                if sha(safe_file(dest/name).read_bytes())!=row[key+'Sha']:raise ValueError('Integration snapshot checksum mismatch.')
    def write_side(self,dest,meta,side):
        for row in [*meta['files'],*(meta.get('quote') or []),*(meta.get('dolphin') or [])]:
            path=Path(row['path'])
            if row[side] is None:path.unlink(missing_ok=True)
            else:self.engine_atomic(path,(dest/row[side]).read_bytes(),row['mode'])
    def apply(self,dest,meta):
        if meta is None:return
        self.verify_snapshot(dest,meta)
        if meta['restoreToken'] is None:self.sddm.call('prepare',meta['rootToken'],meta['theme'],meta['fingerprint'])
        else:self.sddm.call('prepare-restore',meta['rootToken'],meta['restoreToken'])
        spotify_paths={str(p) for p in self.spotify_paths()[:2]}
        css_changed=any(r['path'] in spotify_paths and r['beforeSha']!=r['afterSha'] for r in meta['files'])
        if css_changed:self.session.stop()
        self.write_side(dest,meta,'after');self.sddm.call('apply',meta['rootToken'])
        if meta.get('dolphin'):self.notify_dolphin()
        if css_changed:self.session.restart(meta['spotify'])
    def finish(self,dest,meta):
        if meta is not None:self.sddm.call('finish',meta['rootToken'])
    def undo(self,dest,meta):
        if meta is None:return
        self.verify_snapshot(dest,meta)
        self.sddm.call('rollback',meta['rootToken'])
        css_paths={str(p) for p in self.spotify_paths()[:2]}
        changed=any(r['path'] in css_paths and (sha(Path(r['path']).read_bytes()) if Path(r['path']).exists() else None)!=r['beforeSha'] for r in meta['files'])
        if changed:self.session.stop()
        self.write_side(dest,meta,'before')
        if meta.get('dolphin'):self.notify_dolphin()
        self.session.restart(meta['spotify'])
    def committed(self,dest,meta):
        if meta is not None:self.verify_snapshot(dest,meta,expect_after=True);self.sddm.call('finish',meta['rootToken'])
    def enable(self,dolphin=False):
        with self.engine.lock():
            if self.engine.optional('pending.json'):raise ValueError('Recover the pending theme operation before enabling integration.')
            active=self.engine.optional('active.json');theme=active['id'] if active else 'plague-tale'
            self.engine.verify_installed();self.engine.load(theme)
            self.spotify_plan(theme);self.sddm.call('check',theme,self.greeter_fingerprint(theme))
            current=self.settings();dolphin=dolphin or bool(current and current.get('dolphin'))
            if dolphin:
                self.dolphin_plan(theme)
                if (self.data/'dolphin-owned.json').exists():self.verify_dolphin_owned()
            t=self.terminal();marker=t.STATE/'current.json'
            if not marker.is_file():
                t.STATE.mkdir(parents=True,exist_ok=True,mode=0o700)
                with (t.STATE/'install.lock').open('a') as lock:
                    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                    t.install(SimpleNamespace(config=None,compact=False,theme=theme,check=False))
            record=json.loads(marker.read_text());profile=dict(schema=1,enabled=True,fastfetchConfig=record['target'],dolphin=dolphin)
            if self.profile.exists():
                current=self.settings()
                if current['fastfetchConfig']!=profile['fastfetchConfig']:raise ValueError('Fastfetch target changed; keep the existing integration profile for recovery.')
                self.verify_owned()
            self.engine_atomic(self.profile,encoded(profile))
            # Baseline adoption is explicit and occurs only on first enrollment.
            if not (self.data/'owned.json').exists():self.engine_atomic(self.data/'owned.json',encoded({str(p):sha(p.read_bytes()) if p.exists() else None for p in self.paths() if p!=self.data/'owned.json'}))
            if dolphin and not (self.data/'dolphin-owned.json').exists():self.engine_atomic(self.data/'dolphin-owned.json',encoded({str(p):sha(p.read_bytes()) if p.exists() else None for p in self.dolphin_paths() if p!=self.data/'dolphin-owned.json'}))
            self.cached=None
        self.engine.apply(theme)


def main():
    import theme_core
    p=argparse.ArgumentParser();p.add_argument('action',choices=['enable','disable','status']);p.add_argument('--dolphin',action='store_true',help='Enroll the existing Dolphin adapter in theme switching');a=p.parse_args()
    if a.dolphin and a.action!='enable':p.error('--dolphin is only valid with enable')
    engine=theme_core.Engine();sync=engine.integrations
    if a.action=='status':print(json.dumps(dict(enabled=sync.enabled(),settings=sync.settings()),indent=2));return
    if os.geteuid()==0:raise ValueError('Run as your desktop user, without sudo.')
    if a.action=='enable':sync.enable(dolphin=a.dolphin);print('Fastfetch, Spotify, Hyprlock and SDDM now follow the theme selector.'+(' Dolphin follows too; qt6ct refresh takes about 3 seconds.' if sync.dolphin_enabled() else '')+' Spotify restarts briefly if open.');return
    with engine.lock():
        if engine.optional('pending.json'):raise ValueError('Recover the pending theme operation before disabling sync.')
        profile=sync.settings()
        if profile:profile['enabled']=False;sync.engine_atomic(sync.profile,encoded(profile))
    print('Automatic application/SDDM sync disabled. Current appearance was kept.')

if __name__=='__main__':
    try:main()
    except Exception as exc:print('Stopped: '+str(exc),file=sys.stderr);sys.exit(1)
