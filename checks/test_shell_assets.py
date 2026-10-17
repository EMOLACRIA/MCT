"""Asset regression: real QUrl resolution, QuickShell 0.3.1 boundary, Qt Image.Ready.

The resolver follows qsintercept.cpp's @/qs/ root and file URL conversion.
The independent image fixture avoids depending on a live QuickShell process.
Full shared-scene rendering is covered by test_shell_ui.py.
"""
import os
import sys
import re
import json
from pathlib import Path
os.environ['QT_QPA_PLATFORM']='offscreen'
os.environ['QT_QUICK_BACKEND']='software'
sys.path.insert(0,str(Path('build/qs-qt-check').resolve()))
from PySide6.QtCore import QObject,QUrl,QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlComponent,QQmlExpression,QQmlEngine
from PySide6.QtQuick import QQuickView

shell=Path('build/desktop-style/payload/style/shell').resolve()

def resolve(origin,relative):
    url=QUrl('qs:@/qs/'+origin).resolved(QUrl(relative))
    assert url.scheme()=='qs'
    path=url.path()
    if not path.startswith('@/qs/'):
        raise ValueError('qrc:/qs-blackhole: '+url.toString())
    target=(shell/path[5:]).resolve()
    assert target.is_relative_to(shell),target
    assert target.is_file(),target
    return QUrl.fromLocalFile(str(target)).toString()

for origin,relative in [('PreviewScene.qml','../wallpaper.png'),('ui/OrnamentFrame.qml','../../assets/tl.svg')]:
    try:
        resolve(origin,relative)
        raise AssertionError('Old path incorrectly accepted')
    except ValueError as exc:
        assert 'qs-blackhole' in str(exc)
print('Reproduced original wallpaper/corner paths crossing the QuickShell root.',flush=True)
urls=[]
for origin in ['PreviewScene.qml','ui/OrnamentFrame.qml']:
    for relative in re.findall(r'source\s*:\s*"([^"]+)"',(shell/origin).read_text()):
        urls.append(resolve(origin,relative))
assert len(urls)==5
assert {QUrl(u).fileName() for u in urls}=={'wallpaper.png','tl.svg','tr.svg','bl.svg','br.svg'}
app=QGuiApplication([])
view=QQuickView()
component=QQmlComponent(view.engine())
items=''.join(f'Image {{ x:{i*48}; width:40; height:40; source:{json.dumps(u)} }}' for i,u in enumerate(urls))
component.setData(('import QtQuick\nItem { width:260; height:60; '+items+' }').encode(),QUrl.fromLocalFile(str(shell/'AssetFixture.qml')))
assert component.status()==QQmlComponent.Ready,component.errors()
root=component.create()
assert root is not None,component.errors()
view.setContent(QUrl(),component,root)
view.show()

def verify():
    try:
        images=[o for o in root.findChildren(QObject) if o.metaObject().className().startswith('QQuickImage')]
        assert len(images)==5
        for image in images:
            expression=QQmlExpression(QQmlEngine.contextForObject(image),image,'status === Image.Ready')
            value=expression.evaluate()[0]
            assert not expression.hasError(),expression.error().toString()
            assert value,image.property('source').toString()
        print('PASS: all five URLs stay inside the shell root; real Qt image objects report Image.Ready.',flush=True)
        app.quit()
    except Exception as exc:
        print('FAIL:',repr(exc),flush=True)
        app.exit(1)
QTimer.singleShot(300,verify)
code=app.exec()
view.setSource(QUrl())
sys.exit(code)
