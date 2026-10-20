#!/usr/bin/env python3
"""Update Steam labels in the common launcher, preserving the active theme."""
import argparse,hashlib,importlib.util,json,os,shutil,tempfile
from pathlib import Path
from datetime import datetime,timezone

PACKAGE=Path(__file__).resolve().parent
SOURCE='payload/style/shell/LiveContext.qml'
def sha(data):return hashlib.sha256(data).hexdigest()
def safe(path):
 for item in (path,*path.parents):
  if item.is_symlink():raise ValueError('Linked target was kept: '+str(item))
 if path.exists() and not path.is_file():raise ValueError('Non-file target was kept: '+str(path))
 return path
def atomic(path,data,mode):
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,name=tempfile.mkstemp(prefix='.mct-steam-',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as out:out.write(data);out.flush();os.fsync(out.fileno())
  os.chmod(name,mode);os.replace(name,path)
 finally:Path(name).unlink(missing_ok=True)
def install(checkout,engine=None):
 checkout=Path(checkout).expanduser().resolve()
 if not (checkout/'.git').exists() or not (checkout/'theme_core.py').is_file():raise ValueError('Select the existing desktop-style checkout.')
 rows=json.loads((PACKAGE/'update.json').read_text())
 if set(rows)!={SOURCE,'checks/test_shell_backend.js'}:raise ValueError('Unknown update inventory.')
 files={}
 for name,row in rows.items():
  src=safe(PACKAGE/'source'/name);data=src.read_bytes()
  if sha(data)!=row['afterSha256']:raise ValueError('Update checksum differs: '+name)
  files[name]=data
 if engine is None:
  spec=importlib.util.spec_from_file_location('mct_steam_core',checkout/'theme_core.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);engine=module.Engine(root=checkout)
 with engine.lock():
  if engine.optional('pending.json'):raise ValueError('Run bash theme.sh recover before applying the launcher update.')
  runtime=safe(engine.style/'shell/LiveContext.qml');source=safe(checkout/SOURCE)
  current=source.read_bytes();live=runtime.read_bytes();row=rows[SOURCE]
  if sha(current)==row['afterSha256'] and live==current:print('Steam launcher labels are already installed.');return
  if sha(current)!=row['beforeSha256'] or live!=current:raise ValueError('Launcher sources differ or contain custom edits; all files were kept.')
  engine.verify_installed();engine.runtime.preflight()
  with tempfile.TemporaryDirectory(prefix='mct-steam-preview-') as temp:
   stage=Path(temp)/'style';shutil.copytree(engine.style,stage,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
   (stage/'shell/LiveContext.qml').write_bytes(files[SOURCE]);engine.runtime.validate(stage,engine.hypr/'appearance.lua')
  outputs={source:files[SOURCE],runtime:files[SOURCE]}
  tests=safe(checkout/'checks/test_shell_backend.js')
  if not tests.exists() or sha(tests.read_bytes()) not in {rows['checks/test_shell_backend.js']['beforeSha256'],rows['checks/test_shell_backend.js']['afterSha256']}:raise ValueError('Backend test source contains custom edits; all files were kept.')
  outputs[tests]=files['checks/test_shell_backend.js']
  for name in ['docs/STEAM_LAUNCHER.md','docs/decisions/steam-launcher-labels-20261020.md']:
   dest=safe(checkout/name);data=(PACKAGE/'source'/name).read_bytes()
   if dest.exists() and dest.read_bytes()!=data:raise ValueError('Custom documentation was kept: '+name)
   outputs[dest]=data
  status=safe(checkout/'STATUS.md');before_status=status.read_bytes();marker=b'<!-- steam-launcher-labels-0.1.0 -->'
  if marker not in before_status:outputs[status]=marker+b'\n'+(PACKAGE/'STATUS-NOTE.md').read_bytes()+b'\n\n'+before_status
  before={p:(p.read_bytes(),p.stat().st_mode&0o777) if p.exists() else (None,0o644) for p in outputs}
  backup=engine.data/'steam-launcher-backups'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');backup.mkdir(parents=True,mode=0o700)
  record=[]
  for index,(p,(data,mode)) in enumerate(before.items()):
   record.append({'path':str(p),'file':str(index),'existed':data is not None,'mode':mode})
   if data is not None:(backup/str(index)).write_bytes(data)
  (backup/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
  done=[]
  try:
   engine.runtime.stop()
   for p,data in outputs.items():
    safe(p);expected,mode=before[p]
    if (p.read_bytes() if p.is_file() else None)!=expected:raise ValueError('Target changed during update: '+str(p))
    atomic(p,data,mode);done.append(p)
   engine.runtime.start()
  except BaseException:
   engine.runtime.stop()
   for p in reversed(done):
    data,mode=before[p];safe(p)
    if p.read_bytes()!=outputs[p]:raise ValueError('Later edit was preserved; source backup: '+str(backup))
    if data is None:p.unlink()
    else:atomic(p,data,mode)
   engine.runtime.start();raise
 print('Steam (Native) and Steam (Flatpak) labels installed. Active theme kept.')
 print('Backup: '+str(backup))
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('checkout',type=Path);args=parser.parse_args()
 try:install(args.checkout)
 except Exception as error:parser.exit(1,'Stopped: '+str(error)+'\n')
