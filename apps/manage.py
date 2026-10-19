#!/usr/bin/env python3
"""Optional application themes. Run as the desktop user; no root/package writes."""
import argparse
import configparser
import shlex
from html.parser import HTMLParser
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime

PACKAGE=Path(__file__).resolve().parent
sys.path.insert(0,str(PACKAGE.parent))
import adapter_assets
SELECTED_THEME="plague-tale"

def theme_source(adapter):
    return PACKAGE/adapter if SELECTED_THEME=="plague-tale" else adapter_assets.source(SELECTED_THEME,adapter)

HOME=Path.home()
CONFIG=Path(os.environ.get('XDG_CONFIG_HOME',HOME/'.config'))
DATA=Path(os.environ.get('XDG_DATA_HOME',HOME/'.local/share'))
STATE=Path(os.environ.get('XDG_STATE_HOME',HOME/'.local/state'))/'desktop-style-apps'
SPOTIFY=DATA/'desktop-style-apps/spotify'

def run(args,**kw):
    # Spicetify writes its apply progress to stderr even on success.
    result=subprocess.run(list(map(str,args)),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180,**kw)
    if result.returncode:raise RuntimeError(result.stdout.strip() or 'Command failed: '+str(args[0]))
    return result.stdout.strip()

def version_tuple(value):
    match=re.search(r'(\d+)\.(\d+)\.(\d+)',value)
    if not match:raise RuntimeError('Could not read application version: '+value)
    return tuple(map(int,match.groups()))

def spotify_versions(spice):
    pacman=shutil.which('pacman')
    if not pacman:raise RuntimeError('This native Spotify adapter requires pacman package version information.')
    package=run([pacman,'-Q','spotify']).split()
    if len(package)!=2 or package[0]!='spotify':raise RuntimeError('Could not read the native Spotify package version.')
    cli=run([spice,'--version'])
    version_tuple(package[1]);parsed=version_tuple(cli)
    return {'spotify':package[1],'spicetify':'.'.join(map(str,parsed))}

def check_spotify_compatibility(versions):
    # Published release ranges are advisory: the user reports a working client
    # outside v2.45.3's listed Linux range. Validate actual output instead.
    spotify=version_tuple(versions['spotify']);spice=version_tuple(versions['spicetify'])
    if spice==(2,45,3):
        if not (1,2,14)<=spotify<=(1,2,96):
            print('Warning: Spicetify 2.45.3 documents Linux Spotify support from 1.2.14 through 1.2.96; installed package is '+versions['spotify']+'. Continuing with generated theme output validation.')
    else:
        print('Warning: Spicetify '+versions['spicetify']+' compatibility is not recorded here; verify its Linux release notes. Generated theme files will still be checked.')

def atomic(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    mode=stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.'+path.name+'.')
    try:
        with os.fdopen(fd,'w') as out:out.write(text)
        os.chmod(tmp,mode);os.replace(tmp,path)
    finally:Path(tmp).unlink(missing_ok=True)

def key_value(text,group,key):
    current=''
    for line in text.splitlines():
        if line.strip().startswith('['):current=line.strip()
        elif current=='['+group+']' and re.match(r'^\s*'+re.escape(key)+r'\s*=',line):return line.split('=',1)[1].strip()
    return None

def set_key(text,group,key,value):
    lines=text.splitlines(keepends=True);head='['+group+']';start=next((i for i,l in enumerate(lines) if l.strip()==head),None)
    if start is None:
        return text if value is None else text.rstrip()+'\n\n'+head+'\n'+key+'='+value+'\n'
    end=next((i for i in range(start+1,len(lines)) if lines[i].lstrip().startswith('[')),len(lines))
    indices=[i for i in range(start+1,end) if re.match(r'^\s*'+re.escape(key)+r'\s*=',lines[i])]
    for i in reversed(indices):lines.pop(i);end-=1
    if value is not None:lines.insert(start+1,key+'='+value+'\n')
    return ''.join(lines)

def closed(app):
    for proc in Path('/proc').glob('[0-9]*'):
        try:
            if proc.stat().st_uid==os.getuid() and (proc/'comm').read_text().strip().lower()==app:
                raise RuntimeError('Close '+app+' completely, then run this command again.')
        except (FileNotFoundError,PermissionError,ProcessLookupError):pass

def snapshot(path,dest):
    item={'path':str(path),'exists':path.exists() or path.is_symlink(),'link':os.readlink(path) if path.is_symlink() else None}
    if path.exists():
        item['directory']=path.is_dir()
        if path.is_dir():shutil.copytree(path,dest,symlinks=True)
        else:shutil.copy2(path,dest)
    return item

def remove(path):
    if path.is_dir() and not path.is_symlink():shutil.rmtree(path)
    else:path.unlink(missing_ok=True)

def restore_item(item,source):
    target=Path(item['path']);remove(target)
    if item['exists']:
        target.parent.mkdir(parents=True,exist_ok=True)
        if item['link'] is not None:target.symlink_to(item['link'])
        elif item.get('directory'):shutil.copytree(source,target,symlinks=True)
        else:shutil.copy2(source,target)

def first_backup(app,targets):
    pointer=STATE/(app+'.json')
    if pointer.exists():return json.loads(pointer.read_text()),False
    folder=STATE/'backups'/(app+'-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f'));folder.mkdir(parents=True)
    record={'backup':str(folder),'files':[snapshot(path,folder/str(i)) for i,path in enumerate(targets)]}
    return record,True

def app_paths():
    return [CONFIG/'dolphinrc',DATA/'color-schemes/DesktopStyle.colors',DATA/'icons/DesktopStyle',
            CONFIG/'qt6ct/qt6ct.conf',DATA/'color-schemes/DesktopStyle-Qt.conf',DATA/'applications/org.kde.dolphin.desktop']

DOLPHIN_KEYS=[('UiSettings','ColorScheme','DesktopStyle'),('Icons','Theme','DesktopStyle')]

def qt_palette():
    if SELECTED_THEME!='plague-tale':return (theme_source('dolphin')/'Qt.conf').read_text()
    # QPalette ColorRole order, including PlaceholderText and Qt 6.6 Accent.
    colors=['#ffffff','#292a23','#666454','#454638','#10110f','#777766','#ffffff','#ffffff',
            '#ffffff','#191a18','#191a18','#080907','#514b3a','#ffffff','#d3bd8d','#c3ae95',
            '#22231e','#000000','#292a23','#ffffff','#cdcdcd','#b5a37c']
    disabled=colors.copy()
    for i in [0,6,7,8,13,14,15,19,20]:disabled[i]='#a4a4a4'
    return '[ColorScheme]\n'+'\n'.join(name+'='+', '.join(values) for name,values in [('active_colors',colors),('inactive_colors',colors),('disabled_colors',disabled)])+'\n'

def extend_backup(record,targets):
    for i in range(len(record['files']),len(targets)):
        record['files'].append(snapshot(targets[i],Path(record['backup'])/str(i)))

def dolphin(check=False,restore=False):
    pointer=STATE/'dolphin.json';targets=app_paths()
    if not shutil.which('dolphin'):raise RuntimeError('Dolphin is not installed.')
    closed('dolphin')
    if restore:
        if not pointer.is_file():raise RuntimeError('No Dolphin theme installation to restore.')
        record=json.loads(pointer.read_text());text=targets[0].read_text() if targets[0].exists() else ''
        for group,key,value in DOLPHIN_KEYS:
            if key_value(text,group,key)==value:text=set_key(text,group,key,record['keys'][group])
        if record.get('launcher') and targets[5].exists() and targets[5].read_text()!=record['launcher']:
            raise RuntimeError('Dolphin launcher was edited; review it before restoring: '+str(targets[5]))
        if check:print('Dolphin restore check passed.');return
        atomic(targets[0],text)
        for i in [1,2]:restore_item(record['files'][i],Path(record['backup'])/str(i))
        if 'qt_keys' in record:
            text=targets[3].read_text() if targets[3].exists() else ''
            for key,value in record['qt_installed'].items():
                if key_value(text,'Appearance',key)==value:text=set_key(text,'Appearance',key,record['qt_keys'][key])
            atomic(targets[3],text)
            for i in [4,5]:restore_item(record['files'][i],Path(record['backup'])/str(i))
        pointer.unlink();print('Dolphin colors/icons/launcher restored; other settings kept.');return
    if not shutil.which('qt6ct'):raise RuntimeError('Install qt6ct first: sudo pacman -S --needed qt6ct breeze-icons')
    if check:print('Dolphin check passed. Startup Qt palette and dark icons; launch from Super+R after applying.');return
    text=targets[0].read_text() if targets[0].exists() else ''
    record,new=first_backup('dolphin',targets)
    if record.get('launcher') and targets[5].exists() and targets[5].read_text()!=record['launcher']:
        raise RuntimeError('Dolphin launcher was edited; nothing changed: '+str(targets[5]))
    if new:record['keys']={group:key_value(text,group,key) for group,key,_ in DOLPHIN_KEYS}
    extend_backup(record,targets)
    qt_text=targets[3].read_text() if targets[3].exists() else ''
    qt_values={'color_scheme_path':str(targets[4]),'custom_palette':'true','icon_theme':'DesktopStyle','style':'Fusion','standard_dialogs':'default'}
    if 'qt_keys' not in record:record['qt_keys']={key:key_value(qt_text,'Appearance',key) for key in qt_values}
    record['qt_installed']=qt_values
    with tempfile.TemporaryDirectory(dir=STATE,prefix='dolphin-') as tmp:
        tmp=Path(tmp);current=[snapshot(path,tmp/str(i)) for i,path in enumerate(targets)]
        try:
            atomic(targets[1],(theme_source('dolphin')/'DesktopStyle.colors').read_text())
            remove(targets[2]);shutil.copytree(theme_source('dolphin')/'icons',targets[2])
            for group,key,value in DOLPHIN_KEYS:text=set_key(text,group,key,value)
            atomic(targets[0],text)
            for key,value in qt_values.items():qt_text=set_key(qt_text,'Appearance',key,value)
            atomic(targets[3],qt_text);atomic(targets[4],qt_palette())
            template=original_file(record,5) or system_desktop('org.kde.dolphin.desktop')
            if not template:template='[Desktop Entry]\nType=Application\nName=Dolphin\nIcon=system-file-manager\nExec=dolphin %u\n'
            desktop=redirect_desktop(template,{'dolphin','/usr/bin/dolphin'},['env','QT_QPA_PLATFORMTHEME=qt6ct','QT_STYLE_OVERRIDE=Fusion','dolphin'])
            desktop=re.sub(r'^DBusActivatable=.*$','DBusActivatable=false',desktop,flags=re.M)
            atomic(targets[5],desktop);record['launcher']=desktop
            record['theme']=SELECTED_THEME
            atomic(pointer,json.dumps(record,indent=2))
        except Exception:
            for i,item in enumerate(current):restore_item(item,tmp/str(i))
            raise
    refresh_desktop_database()
    print('Dolphin theme installed. Open from Super+R (startup palette). Backup: '+record['backup'])

def original_file(record,index):
    item=record['files'][index]
    path=Path(record['backup'])/str(index)
    return path.read_text() if item['exists'] and path.is_file() else None

def system_desktop(name):
    for directory in os.environ.get('XDG_DATA_DIRS','/usr/local/share:/usr/share').split(':'):
        path=Path(directory)/'applications'/name
        if path.is_file():return path.read_text()
    return None

def exec_quote(token):
    if re.fullmatch(r'[A-Za-z0-9_./:=@%+,-]+',token):return token
    return '"'+token.replace('\\','\\\\').replace('"','\\"').replace('`','\\`').replace('$','\\$')+'"'

def redirect_desktop(text,executables,replacement):
    def edit(match):
        tokens=shlex.split(match.group(1))
        pos=0
        if tokens and tokens[0] in ['env','/usr/bin/env']:
            pos=1
            while pos<len(tokens) and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=',tokens[pos]):pos+=1
        if pos>=len(tokens) or tokens[pos] not in executables:
            raise RuntimeError('Unsupported launcher command; kept unchanged: '+match.group(1))
        return 'Exec='+' '.join(exec_quote(t) for t in tokens[:pos]+replacement+tokens[pos+1:])
    if not re.search(r'^Exec=',text,re.M):raise RuntimeError('Launcher has no Exec command.')
    result=re.sub(r'^Exec=(.*)$',edit,text,flags=re.M)
    result=re.sub(r'^TryExec=.*\n?','',result,flags=re.M)
    return re.sub(r'^DBusActivatable=.*$','DBusActivatable=false',result,flags=re.M)

def refresh_desktop_database():
    if shutil.which('update-desktop-database'):
        subprocess.run(['update-desktop-database',str(DATA/'applications')],capture_output=True,timeout=15)

class ScriptTags(HTMLParser):
    def __init__(self):super().__init__();self.sources=[];self.stylesheets=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='script':
            source=attrs.get('src')
            if source:self.sources.append(source)
        if tag=='link' and 'stylesheet' in (attrs.get('rel') or '').split():
            href=attrs.get('href')
            if href:self.stylesheets.append(href)

def verify_spotify_theme(client):
    """Read-only checks: a zero exit status alone does not prove theme output."""
    xpui=client/'Apps/xpui';index=xpui/'index.html'
    if not index.is_file():raise RuntimeError('Spotify theme output missing: index.html')
    tags=ScriptTags();tags.feed(index.read_text())
    links={src.split('?')[0].lstrip('/') for src in tags.stylesheets}
    for name in ['user.css','colors.css']:
        if name not in links or not (xpui/name).is_file() or not (xpui/name).stat().st_size:
            raise RuntimeError('Spotify theme output missing or not linked: '+name)
    if (xpui/'user.css').read_bytes()!=(theme_source('spotify')/'user.css').read_bytes():
        raise RuntimeError('Spotify theme output does not contain the requested user.css.')
    palette=configparser.ConfigParser();palette.read(theme_source('spotify')/'color.ini')
    colors=(xpui/'colors.css').read_text()
    for key,value in palette['Ash'].items():
        if not re.search(r'--spice-'+re.escape(key)+r'\s*:\s*#'+re.escape(value)+r'\s*;',colors,re.I):
            raise RuntimeError('Spotify theme output has an incorrect palette: '+key)
    try:config=json.loads((xpui/'spicetify-config.json').read_text())
    except (OSError,ValueError) as exc:raise RuntimeError('Spotify theme metadata is missing or invalid.') from exc
    if not isinstance(config,dict) or config.get('theme_name')!='DesktopStyle' or config.get('scheme_name')!='Ash':
        raise RuntimeError('Spotify theme metadata does not match DesktopStyle/Ash.')

def repair_spotify_bootstrap(client):
    # Spicetify 2.x htmlMod returns early for CSS-only configs, before it adds
    # the externalized V8 module script. Restore that dependency explicitly.
    xpui=client/'Apps/xpui';index=xpui/'index.html'
    if not index.is_file():raise RuntimeError('Spicetify did not produce Apps/xpui/index.html.')
    html=index.read_text();tags=ScriptTags();tags.feed(html)
    names=[src.split('?')[0].rsplit('/',1)[-1] for src in tags.sources]
    if 'xpui-snapshot.js' in names and (xpui/'xpui-modules.js').is_file():
        if not (xpui/'xpui-modules.js').stat().st_size:raise RuntimeError('Extracted Spotify modules are empty; update Spicetify.')
        if 'xpui-modules.js' not in names:
            pattern=r'<script\b[^>]*\bsrc=["\'][^"\']*xpui-snapshot\.js(?:\?[^"\']*)?["\'][^>]*>'
            html,count=re.subn(pattern,lambda m:'<script defer="defer" src="/xpui-modules.js"></script>'+m.group(),html,count=1)
            if count!=1:raise RuntimeError('Could not repair Spotify snapshot script order.')
            atomic(index,html);print('Repaired Spotify snapshot module loading for CSS-only mode.')
    tags=ScriptTags();tags.feed(html)
    for src in tags.sources:
        if '://' in src or src.startswith('//') or src.startswith('data:'):continue
        asset=xpui/src.split('?')[0].lstrip('/')
        if not asset.is_file():raise RuntimeError('Spotify startup asset missing: '+str(asset))


def spotify_source():
    candidates=[p for p in [Path('/opt/spotify'),Path('/usr/share/spotify'),Path('/usr/lib/spotify')] if (p/'Apps').is_dir() and (p/'spotify').is_file()]
    if len(candidates)!=1:raise RuntimeError('Could not uniquely locate the native Spotify package under /opt or /usr. Nothing changed.')
    return candidates[0]

def spotify_launchers(source,record=None):
    normal=DATA/'applications/spotify.desktop'
    known={item['path']:i for i,item in enumerate(record['files'])} if record else {}
    paths={normal.name:normal}
    for directory in [*(Path(x)/'applications' for x in os.environ.get('XDG_DATA_DIRS','/usr/local/share:/usr/share').split(':')),DATA/'applications']:
        if directory.is_dir():
            for path in directory.glob('*.desktop'):
                try:
                    if 'spotify' in path.read_text().lower():paths[path.name]=path
                except (UnicodeDecodeError,OSError):pass
    fallback='[Desktop Entry]\nType=Application\nName=Spotify\nIcon=spotify\nTerminal=false\nCategories=AudioVideo;Audio;Player;\nMimeType=x-scheme-handler/spotify;\nExec=spotify %U\n'
    entries=[]
    executables={'spotify','/usr/bin/spotify',str(source/'spotify')}
    for name,path in sorted(paths.items(),key=lambda x:(x[0]!='spotify.desktop',x[0])):
        target=DATA/'applications'/name
        text=(original_file(record,known[str(target)]) if str(target) in known else None)
        if text is None:text=system_desktop(name) if str(target) in known else (path.read_text() if path.is_file() else None)
        if text is None and name=='spotify.desktop':text=fallback
        if text is None:continue
        if name!='spotify.desktop' and ('flatpak' in text or 'spotify' not in text.lower()):continue
        try:desktop=redirect_desktop(text,executables,[str(SPOTIFY/'launch.sh')])
        except (ValueError,RuntimeError) as exc:
            if name=='spotify.desktop':raise
            print('Skipped unsupported Spotify launcher '+name+': '+str(exc));continue
        entries.append((target,desktop))
    return entries

def spotify(check=False,restore=False):
    pointer=STATE/'spotify.json';launcher=DATA/'applications/spotify.desktop'
    closed('spotify')
    record=json.loads(pointer.read_text()) if pointer.exists() else None
    if record:
        installed=record.get('launchers',{str(launcher):record['launcher']})
        for path,text in installed.items():
            if Path(path).exists() and Path(path).read_text()!=text:
                raise RuntimeError('Your Spotify launcher changed after installation; review before updating: '+path)
    if restore:
        if not record:raise RuntimeError('No Spotify theme installation to restore.')
        if check:print('Spotify restore check passed.');return
        for i,item in enumerate(record['files']):restore_item(item,Path(record['backup'])/str(i))
        remove(SPOTIFY);pointer.unlink();refresh_desktop_database()
        print('Original Spotify launchers restored.');return
    spice=shutil.which('spicetify')
    if not spice:raise RuntimeError('Install spicetify-cli first (paru -S --needed spicetify-cli or yay -S --needed spicetify-cli).')
    versions=spotify_versions(spice);check_spotify_compatibility(versions)
    source=spotify_source();prefs=CONFIG/'spotify/prefs'
    if not prefs.is_file():raise RuntimeError('Open Spotify, sign in, wait a minute, then close it before applying the theme.')
    if SPOTIFY.exists() and not record:raise RuntimeError('Unmanaged Spotify theme folder exists: '+str(SPOTIFY))
    entries=spotify_launchers(source,record)
    size=sum(f.stat().st_size for f in source.rglob('*') if f.is_file())
    free=shutil.disk_usage(DATA if DATA.exists() else HOME).free
    if free<size*3+100*1024**2:raise RuntimeError('Not enough space for the client copy and Spicetify working files.')
    for path,text in entries:
        print('Launcher: '+path.name+(' (LD_PRELOAD preserved)' if 'LD_PRELOAD=' in text else ''))
    if check:
        print('Spotify check passed. Source: '+str(source)+'; private copy, approx '+str(round(size/1024**2))+' MiB plus Spicetify working files.');return
    if not record:record,_=first_backup('spotify',[path for path,_ in entries])
    else:
        targets=[Path(item['path']) for item in record['files']]
        targets.extend(path for path,_ in entries if path not in targets)
        extend_backup(record,targets)
    SPOTIFY.parent.mkdir(parents=True,exist_ok=True)
    previous=SPOTIFY.with_name('spotify.previous')
    if previous.exists():raise RuntimeError('Previous interrupted update exists: '+str(previous))
    recovery=Path(tempfile.mkdtemp(dir=STATE,prefix='spotify-recovery-'))
    current=[snapshot(path,recovery/str(i)) for i,(path,_) in enumerate(entries)]
    if SPOTIFY.exists():SPOTIFY.rename(previous)
    try:
        client=SPOTIFY/'client';shutil.copytree(source,client,symlinks=False)
        for f in [client,*client.rglob('*')]:os.chmod(f,stat.S_IMODE(f.stat().st_mode)|stat.S_IWUSR)
        spice_config=SPOTIFY/'config';theme=spice_config/'spicetify/Themes/DesktopStyle';shutil.copytree(theme_source('spotify'),theme)
        config='[Setting]\nspotify_path = '+str(client)+'\nprefs_path = '+str(prefs)+'\ncurrent_theme = DesktopStyle\ncolor_scheme = Ash\ninject_css = 1\nreplace_colors = 1\ninject_theme_js = 0\ncheck_spicetify_update = 0\n\n[Preprocesses]\ndisable_sentry = 0\ndisable_ui_logging = 0\nremove_rtl_rule = 0\nexpose_apis = 0\n\n[AdditionalOptions]\nexperimental_features = 0\nhome_config = 0\nsidebar_config = 0\nextensions = \ncustom_apps = \n'
        atomic(spice_config/'spicetify/config-xpui.ini',config)
        env={**os.environ,'SPICETIFY_CONFIG':str(spice_config/'spicetify'),'XDG_CONFIG_HOME':str(spice_config),'XDG_STATE_HOME':str(SPOTIFY/'state')}
        env.pop('SPICETIFY_STATE',None)
        output=run([spice,'backup','apply','--no-restart'],env=env);print(output)
        atomic(SPOTIFY/'apply.log',output+'\n')
        repair_spotify_bootstrap(client)
        verify_spotify_theme(client)
        atomic(SPOTIFY/'versions.json',json.dumps(versions,indent=2)+'\n')
        wrapper=Path('/usr/bin/spotify');launch=SPOTIFY/'launch.sh'
        launch_text='#!/usr/bin/env bash\nexec '+shlex.quote(str(client/'spotify'))+' "$@"\n'
        if wrapper.is_file() and not wrapper.is_symlink():
            try:
                original=wrapper.read_text()
                if original.startswith('#!') and str(source) in original:launch_text=original.replace(str(source),str(client))
            except UnicodeDecodeError:pass
        atomic(launch,launch_text);launch.chmod(0o755)
        record.setdefault('launchers',{})
        for path,desktop in entries:
            atomic(path,desktop);record['launchers'][str(path)]=desktop
        record['launcher']=dict(entries)[launcher]
        record['theme']=SELECTED_THEME
        atomic(pointer,json.dumps(record,indent=2))
    except Exception:
        remove(SPOTIFY)
        if previous.exists():previous.rename(SPOTIFY)
        for i,item in enumerate(current):restore_item(item,recovery/str(i))
        raise
    finally:shutil.rmtree(recovery)
    remove(previous);refresh_desktop_database()
    print('Spotify theme installed. Open the same Spotify/adblock entry from Super+R. Original package remains untouched.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('app',choices=['dolphin','spotify']);parser.add_argument('--check',action='store_true');parser.add_argument('--restore',action='store_true');parser.add_argument('--theme',choices=adapter_assets.THEMES);args=parser.parse_args()
    global SELECTED_THEME
    choice=args.theme or ("plague-tale" if args.restore else None)
    SELECTED_THEME=adapter_assets.selected(choice)
    if os.geteuid()==0:raise RuntimeError('Run as your normal user, without sudo.')
    if args.check:(dolphin if args.app=='dolphin' else spotify)(True,args.restore);return
    STATE.mkdir(parents=True,exist_ok=True,mode=0o700)
    with (STATE/'install.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        (dolphin if args.app=='dolphin' else spotify)(False,args.restore)

if __name__=='__main__':
    try:main()
    except Exception as exc:print('Stopped: '+str(exc),file=sys.stderr);sys.exit(1)
