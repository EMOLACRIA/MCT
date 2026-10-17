"""Real CLI11 parse regression using QuickShell 0.3.1's IPC command declarations."""
import importlib.util,subprocess
from pathlib import Path
from unittest.mock import patch
binary=Path('tmp/apps22/ipc-parser').resolve()
old=subprocess.run([str(binary),'ipc','-p','/test','call','feedback','show','volume','55','false'],capture_output=True,text=True)
assert old.returncode and 'arguments were not expected' in old.stderr
p=Path('build/desktop-style/payload/style/scripts/feedback.py')
spec=importlib.util.spec_from_file_location('feedback',p);feedback=importlib.util.module_from_spec(spec);spec.loader.exec_module(feedback)
with patch.object(feedback.shutil,'which',return_value=str(binary)):
 for kind,level,muted in [('volume',55,False),('brightness',95,False),('microphone',0,True)]:feedback.show(kind,level,muted)
qml=Path('build/desktop-style/payload/style/shell/shell.qml').read_text()
assert 'function present(kind:string,level:int,muted:bool)' in qml
assert 'function show(' not in qml
for line in qml.splitlines():
 if 'visible:' in line:assert '&& screen' not in line,line
assert 'shellState.feedbackVisible && root.focusedScreen!==null' in qml
assert 'shellState.activePanel!=="" && root.panelScreen!==null' in qml
print('PASS: reproduces reserved show collision; production volume/brightness/microphone IPC calls parse; visible bindings use external screen state')
