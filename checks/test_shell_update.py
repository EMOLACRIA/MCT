import importlib.util,json,os,shutil,sys,tempfile
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch
package=Path('build/desktop-style').resolve();sys.path.insert(0,str(package));import update as u
m=u.m
class Session:
 def __init__(self,style,fail=False):
  self.commands=[['waybar','old-profile'],['dunst','-conf',str(style/'dunst/dunstrc')],['quickshell','-p',str(style/'feedback')]]
  self.original=self.commands[:];self.services={'dunst.service':{'enabled':'enabled','active':True}};self.fail=fail;self.suppressed=False;self.ready=False
 def processes(self):return [(200+i,a) for i,a in enumerate(self.commands)]
 def managed(self,args):return args in self.commands or args in self.original or args[0]=='quickshell'
 def read_services(self):return json.loads(json.dumps(self.services))
 def suppress_services(self,record):self.suppressed=True
 def restore_services(self,record):self.services=record;self.suppressed=False
 def stop_panel(self):self.commands=[];self.ready=False
 def launch(self,args,log):self.commands.append(args)
 def start(self):
  if self.fail:raise RuntimeError('simulated startup failure')
  self.commands=[['quickshell','-p','new-shell']];self.ready=True
 def feedback_ready(self):return self.ready

def run(args):
 if args==['hyprctl','version']:return CompletedProcess(args,0,'Hyprland 0.56.2','')
 if args==['quickshell','--version']:return CompletedProcess(args,0,'quickshell 0.3.1','')
 return CompletedProcess(args,0,'','')

def digest(root):return {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
with patch.object(os,'geteuid',return_value=1000),patch.dict(os.environ,{'HYPRLAND_INSTANCE_SIGNATURE':'fixture'}),patch.object(shutil,'which',return_value='/usr/bin/fixture'),patch.object(m,'run',side_effect=run),patch.object(u.time,'sleep'):
 for case in ['check','success','startup-failure','custom-key']:
  with tempfile.TemporaryDirectory() as td:
   base=Path(td);m.BASE=base;m.STYLE=base/'.config/desktop-style';m.STATE=base/'.local/state/desktop-style';m.HYPR=base/'.config/hypr'
   shutil.copytree('build/desktop-style-v1.4/payload/style',m.STYLE);m.HYPR.mkdir();m.STATE.mkdir(parents=True)
   old=Path('build/desktop-style-v1.4/payload/hypr/keybinds.lua').read_text()+'\n-- custom binding kept\nhl.bind(mainMod .. " + Z", hl.dsp.exec_cmd("kitty"))\n'
   if case=='custom-key':old=old.replace('styleCommand("feedback.sh") .. " volume up"','"custom-volume-command"')
   kb=m.HYPR/'keybinds.lua';kb.write_text(old)
   (m.HYPR/'hyprlock.conf').write_text('general {\n hide_cursor = true\n}\n# user lock settings\n')
   for n in ['monitors.lua','environment.lua','input.lua','system.lua','hyprland.lua']:(m.HYPR/n).write_text('keep '+n)
   (m.STYLE/'wofi/config').write_text('xoffset=30\nyoffset=30\n# user offset\n')
   original=m.STATE/'backups/original';original.mkdir(parents=True);(original/'manifest.json').write_text('{"status":"installed","files":[]}')
   (m.STATE/'current-backup').write_text(str(original));pointer=(m.STATE/'current-backup').read_bytes();baseline=digest(m.STYLE);core={p.name:p.read_bytes() for p in m.HYPR.iterdir() if p.name not in ['keybinds.lua','hyprlock.conf']}
   session=Session(m.STYLE,case=='startup-failure')
   with patch.object(m,'load_session',return_value=session):
    if case=='check':u.update(True);assert digest(m.STYLE)==baseline and kb.read_text()==old and not session.suppressed
    elif case in ['startup-failure','custom-key']:
     try:u.update();raise AssertionError('must reject')
     except RuntimeError:pass
     assert digest(m.STYLE)==baseline and kb.read_text()==old
     assert session.commands==session.original and not session.suppressed
     assert json.loads((original/'manifest.json').read_text())=={'status':'installed','files':[]}
    else:
     u.update();assert (m.STYLE/'shell/shell.qml').is_file();assert 'notifications.sh' in kb.read_text() and '-- custom binding kept' in kb.read_text()
     assert (m.STYLE/'wofi/config').read_bytes()==baseline['wofi/config']
     assert json.loads((original/'manifest.json').read_text())['desktop_services']==session.services
     assert 'hardware.sh' in kb.read_text()
     assert (m.HYPR/'hyprlock.conf').read_text().count('# desktop-style media begin')==1
     assert 'hide_cursor = false' in (m.HYPR/'hyprlock.conf').read_text()
     assert '@STYLE@' not in (m.STYLE/'hyprlock/media.conf').read_text()
     assert u.lock_config((m.HYPR/'hyprlock.conf').read_text())==(m.HYPR/'hyprlock.conf').read_text()
     assert (m.STATE/'last-update').is_file();u.rollback(True);u.rollback()
     assert (m.HYPR/'hyprlock.conf').read_text()=='general {\n hide_cursor = true\n}\n# user lock settings\n'
     assert digest(m.STYLE)==baseline and kb.read_text()==old
     assert session.commands==session.original and not session.suppressed
    assert (m.STATE/'current-backup').read_bytes()==pointer
    for name,content in core.items():assert (m.HYPR/name).read_bytes()==content
   print('PASS:',case,'offsets/core settings/custom binds/original restore point preserved')
print('PASS: update preflight, complete migration, startup failure rollback and revision rollback')
