"""Parse every shell QML file, including live-only entrypoints, using Qt.

qmlcachegen --only-bytecode checks QML/JS syntax without instantiating native
services. It does not replace the user's QuickShell validate.qml type check.
"""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

package=Path(__file__).resolve().parents[1]
shell=package/'payload/style/shell'
compiler=Path(os.environ.get('MCT_QMLCACHEGEN') or shutil.which('qmlcachegen') or '/missing-qmlcachegen')
assert compiler.is_file(), 'Qt qmlcachegen is required; set MCT_QMLCACHEGEN to its executable path.'
files=(sorted(shell.rglob('*.qml')) + sorted((package/'theme-picker').glob('*.qml'))
       + sorted((package/'themes').rglob('*.qml')))
assert shell/'shell.qml' in files and shell/'LiveContext.qml' in files

with tempfile.TemporaryDirectory(prefix='desktop-qml-syntax-') as out:
    out=Path(out)
    def compile_file(path,name):
        return subprocess.run([str(compiler),'--only-bytecode','-o',str(out/(name+'.qmlc')),str(path)],capture_output=True,text=True,timeout=20)
    # Prove this check catches both previously missed native-only failures.
    regressions=[('shell.qml','anchors {top:true;right:true}\n        margins','anchors {top:true;right:true};\n        margins'),('LiveContext.qml','property var extra:({brightness:-1,network:"Offline",networkSettingsAvailable:false})','property var extra:{brightness:-1,network:"Offline",networkSettingsAvailable:false}')]
    for index,(name,correct,broken) in enumerate(regressions):
        text=(shell/name).read_text()
        assert correct in text, name
        fixture=out/f'Broken{index}.qml'
        fixture.write_text(text.replace(correct,broken,1))
        result=compile_file(fixture,f'broken{index}')
        assert result.returncode, f'Compiler failed to detect old {name} error'
        print(f'Reproduced old {name} syntax failure.',flush=True)
    for i,path in enumerate(files):
        result=compile_file(path,str(i))
        assert result.returncode==0, str(path)+'\n'+result.stdout+result.stderr
print(f'PASS: all {len(files)} QML files compile to bytecode, including live shell and backend.',flush=True)
