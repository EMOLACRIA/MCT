import json,os,shutil,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from subprocess import CompletedProcess
sys.path.insert(0,str(Path('build/desktop-style').resolve()));import manage as m
class Session:
 OLD_SHELL='old-shell'
 def __init__(self):self.cmd=[['quickshell','-p','old-shell']];self.services={};self.ready=False
 def processes(self):return [(200+i,a) for i,a in enumerate(self.cmd)]
 def read_services(self):return self.services
 def suppress_services(self,s):pass
 def restore_services(self,s):pass
 def stop_ui(self):self.cmd=[];self.ready=False
 def launch(self,args,log):self.cmd.append(args)
 def start(self):self.cmd.append(['quickshell','-p','new-shell']);self.ready=True
 def feedback_ready(self):return self.ready

def run(args):
 return CompletedProcess(args,0,'Hyprland 0.56.2' if args==['hyprctl','version'] else 'quickshell 0.3.1' if args==['quickshell','--version'] else '','')
with tempfile.TemporaryDirectory() as td,patch.object(os,'geteuid',return_value=1000),patch.dict(os.environ,{'HYPRLAND_INSTANCE_SIGNATURE':'fixture'}),patch.object(shutil,'which',return_value='/fixture'),patch.object(m,'run',side_effect=run),patch.object(m.time,'sleep'):
 base=Path(td);m.BASE=base;m.STYLE=base/'.config/desktop-style';m.STATE=base/'.local/state/desktop-style';m.HYPR=base/'.config/hypr'
 shutil.copytree('original/hypr',m.HYPR);kitty=base/'.config/kitty/kitty.conf';kitty.parent.mkdir();kitty.write_text('font_size 11\n')
 prior={p.name:p.read_bytes() for p in m.HYPR.iterdir() if p.is_file()};session=Session()
 with patch.object(m,'load_session',return_value=session):
  m.install(True);assert not m.STYLE.exists()
  m.install();assert (m.STYLE/'shell/shell.qml').is_file();assert 'notifications.sh' in (m.HYPR/'keybinds.lua').read_text();assert (m.STATE/'current-backup').is_file()
  m.restore();assert not m.STYLE.exists() and not (m.STATE/'current-backup').exists();assert kitty.read_text()=='font_size 11\n'
  for name,data in prior.items():assert (m.HYPR/name).read_bytes()==data,name
print('PASS: fresh installation/check and exact full original restoration, including Kitty and untouched Hyprland core settings.')
