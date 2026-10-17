#!/usr/bin/env python3
"""Common schema, atomic preference storage and read-only diagnostics. No shell execution."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

SPEC=Path(__file__).resolve().parents[1]/'shell/logic/Preferences.js'
SCHEMA=json.loads(re.search(r'// schema begin\s*var schema =\s*(.*?)\s*;\s*// schema end',SPEC.read_text(),re.S)[1])


def defaults():return {key:rule['default'] for key,rule in SCHEMA['fields'].items()}


def preference_path(env=None):
    env=os.environ if env is None else env
    home=Path(env.get('HOME') or Path.home())
    config=Path(env.get('XDG_CONFIG_HOME') or home/'.config')
    if not config.is_absolute():config=home/'.config'
    return config/'mct/preferences.json'


def validate(values):
    if not isinstance(values,dict) or set(values)!=set(SCHEMA['fields']):raise ValueError('Preference fields are missing or unknown.')
    for key,rule in SCHEMA['fields'].items():
        value=values[key];kind=rule['type']
        if kind=='boolean' and type(value) is not bool:raise ValueError('Invalid preference: '+key)
        if kind=='number' and (type(value) not in (int,float) or not rule['min']<=value<=rule['max']):raise ValueError('Out of range: '+key)
        if kind=='string' and (not isinstance(value,str) or len(value)>180):raise ValueError('Invalid preference: '+key)
        if 'enum' in rule and value not in rule['enum']:raise ValueError('Unsupported preference: '+key)
        if 'pattern' in rule and not re.fullmatch(rule['pattern'],value):raise ValueError('Invalid application ID.')
    return dict(values)


def read(env=None):
    path=preference_path(env)
    if not path.exists():return defaults()
    if path.stat().st_size>16384:raise ValueError('Preference file is too large.')
    data=json.loads(path.read_text())
    if not isinstance(data,dict) or type(data.get('version')) is not int or data.get('version')!=SCHEMA['version']:raise ValueError('Unsupported preference version.')
    values=defaults();supplied=data.get('values')
    if not isinstance(supplied,dict):raise ValueError('Missing preference values.')
    # A future release can add defaults without discarding older valid preferences.
    values.update(supplied);return validate(values)


def effective(env=None):
    try:return read(env)
    except (ValueError,OSError) as error:
        print('Preferences unreadable; using default applications: '+str(error),file=sys.stderr)
        return defaults()


def atomic_write(path,values):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.preferences-',dir=path.parent)
    temporary=Path(name)
    try:
        with os.fdopen(fd,'w') as f:
            json.dump({'version':SCHEMA['version'],'values':validate(values)},f,indent=2,allow_nan=False)
            f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(temporary,path)
    finally:temporary.unlink(missing_ok=True)


def capabilities(env=None):
    env=os.environ if env is None else env
    return [{'id':key,'name':key.title(),'available':bool(shutil.which(key,path=env.get('PATH')))} for key in SCHEMA['fields']['terminal']['enum']]


def handle(action,values=None,env=None):
    path=preference_path(env);result={'action':action,'path':str(path),'terminals':capabilities(env),'ok':False,'sourceValid':True,'error':''}
    try:
        current=read(env)
    except (ValueError,OSError) as error:
        result.update(values=defaults(),sourceValid=False,error='Preferences could not be read: '+str(error))
        if action!='reset':return result
        current=defaults()
    try:
        if action=='save':
            checked=validate(values)
            if not next(t['available'] for t in result['terminals'] if t['id']==checked['terminal']):raise ValueError('Selected terminal is not installed.')
            atomic_write(path,checked);current=checked
        elif action=='reset':
            if path.is_file():
                backup=path.with_name('preferences-before-reset-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.json')
                shutil.copyfile(path,backup);backup.chmod(0o600);result['backup']=str(backup)
            current=defaults();atomic_write(path,current)
        elif action=='diagnose':
            lines=['Preferences: '+str(path),'Schema: '+str(SCHEMA['version']), 'Terminal: '+current['terminal'],'File manager: '+current['fileManager']]
            for cmd in [['hyprctl','version'],['quickshell','--version']]:
                try:
                    p=subprocess.run(cmd,text=True,capture_output=True,timeout=3,env=env)
                    lines.append(cmd[0]+': '+(p.stdout or p.stderr).strip().split('\n')[0])
                except (OSError,subprocess.TimeoutExpired):lines.append(cmd[0]+': unavailable')
            result['diagnostics']='\n'.join(lines)
        elif action!='read':raise ValueError('Unknown preference operation.')
        result.update(ok=True,sourceValid=True,values=current,error='')
    except (OSError,ValueError) as error:result.update(values=current,error='Preferences were not saved: '+str(error))
    return result


def main(arguments):
    try:
        action=arguments[0] if arguments else 'read'
        values=json.loads(arguments[1]) if action=='save' and len(arguments)==2 else None
        print(json.dumps(handle(action,values),allow_nan=False))
    except (ValueError,OSError) as error:print(json.dumps({'ok':False,'error':str(error)}))
    return 0


if __name__=='__main__':sys.exit(main(sys.argv[1:]))
