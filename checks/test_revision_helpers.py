import importlib.util,json,sys,tempfile,re
from pathlib import Path
from unittest.mock import patch
from subprocess import CompletedProcess

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
base=Path('build/desktop-style/payload/style');hardware=load('hardware',base/'shell/hardware.py');media=load('lock_media',base/'scripts/lock-media.py');feedback=load('feedback',base/'scripts/feedback.py')
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 def put(name,text):
  f=p/name.lstrip('/');f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text);return f
 put('/proc/meminfo','MemTotal: 33554432 kB\nMemAvailable: 25165824 kB\n')
 put('/proc/cpuinfo','model name : Test CPU\n');put('/proc/uptime','3600 0')
 put('/sys/class/hwmon/hwmon0/name','coretemp');put('/sys/class/hwmon/hwmon0/temp1_input','54000');put('/sys/class/hwmon/hwmon0/temp1_label','Package id 0')
 put('/sys/class/hwmon/hwmon0/fan1_input','1600')
 for device in ['sys/bus/pci/devices/test','sys/class/drm/card1/device']:
  put(device+'/vendor','0x10de');put(device+'/class','0x030000');put(device+'/power/runtime_status','suspended')
 def redirected(path):return p/str(path).lstrip('/') if str(path).startswith(('/sys/','/proc/')) else Path(path)
 redirected.home=lambda:p
 with patch.object(hardware,'Path',redirected),patch.object(hardware,'cpu_ticks',side_effect=[(1000,700),(1100,780)]),patch.object(hardware.time,'sleep'),patch.object(hardware.subprocess,'run') as run:
  data=hardware.snapshot();assert data['cpuUsage']==20 and data['cpuTemp']==54
  assert data['memoryUsed']==8 and data['memoryTotal']==32
  assert data['fans'][0]['value']==1600 and data['gpus'][0]['state']=='Sleeping';run.assert_not_called()
 for device in ['sys/bus/pci/devices/test','sys/class/drm/card1/device']:put(device+'/power/runtime_status','active')
 with patch.object(hardware,'Path',redirected),patch.object(hardware,'cpu_ticks',side_effect=[(1000,700),(1100,780)]),patch.object(hardware.time,'sleep'),patch.object(hardware.shutil,'which',return_value='/usr/bin/nvidia-smi'),patch.object(hardware.subprocess,'run',return_value=CompletedProcess([],0,'NVIDIA RTX Test, 51, 12, 1024, 8192\n','')) as run:
  data=hardware.snapshot();assert data['gpus'][0]['state']=='51°C · 12% load · 1024/8192 MiB';run.assert_called_once()
 media.CACHE=p/'cache';media.STYLE=p/'style'
 assert media.plain('<b>A & B</b>',100)=='&lt;b&gt;A &amp; B&lt;/b&gt;'
 with patch.object(media,'ipc',return_value=json.dumps({'title':'Test','artist':'Artist','art':'','playing':True})) as ipc:
  assert media.metadata()['title']=='Test';assert media.metadata()['playing'];ipc.assert_called_once()
 local=put('cover.png','fixture')
 assert media.cover_path(local.as_uri())==local
 with patch.object(media.subprocess,'Popen') as spawn:
  assert media.cover_path('https://example.test/art.png')==media.STYLE/'hyprlock/cover.png'
  media.cover_path('https://example.test/art.png');spawn.assert_called_once()
 assert media.cover_path('javascript:alert(1)')==media.STYLE/'hyprlock/cover.png'
 feedback.STATE=p/'state'
 with patch.object(sys,'argv',['feedback.py','volume','up']),patch.object(feedback,'change',return_value=(42,False)),patch.object(feedback,'show',side_effect=RuntimeError('fixture IPC failure')),patch.object(feedback.subprocess,'run') as run:
  try:feedback.main();raise AssertionError('must report OSD failure')
  except RuntimeError as e:assert 'OSD unavailable' in str(e)
  run.assert_not_called();assert 'fixture IPC failure' in (feedback.STATE/'feedback.log').read_text()
print('PASS: CPU/memory/temp/fan readings, GPU sleep preservation, active NVIDIA metrics, media cache/escaping/cover deduplication, OSD never falls back to notifications')
# Check every generated Hyprlock setting against the actual 0.9.6 declaration.
source=Path('tmp/hyprlock-0.9.6/ConfigManager.cpp').read_text()
for kind,body in re.findall(r'(shape|label|image)\s*\{([^}]+)\}',(base/'hyprlock/media.conf').read_text()):
 for line in body.splitlines():
  if '=' not in line:continue
  key=line.strip().split('=',1)[0].strip()
  assert 'addSpecialConfigValue("'+kind+'", "'+key+'"' in source or key=='onclick' and 'CLICKABLE("'+kind+'")' in source,(kind,key)
print('PASS: lockscreen media fragment uses supported Hyprlock 0.9.6 properties')
