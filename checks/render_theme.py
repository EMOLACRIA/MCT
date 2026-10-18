"""Render one staged theme surface in a fresh offscreen Qt process; no live services."""
import argparse
import os
from pathlib import Path
import sys
import tempfile

os.environ['QT_QPA_PLATFORM']='offscreen'
os.environ['QT_QUICK_BACKEND']='software'
if os.environ.get('MCT_QT_TEST_PATH'):sys.path.insert(0,os.environ['MCT_QT_TEST_PATH'])
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import theme_preview
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlExpression,QQmlEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QTest

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('theme')
parser.add_argument('output',type=Path)
parser.add_argument('--panel',default='launcher',choices=['desktop','launcher','media','hardware','controls','power','notifications','settings','osd','switcher'])
args=parser.parse_args()
app=QGuiApplication([])
with tempfile.TemporaryDirectory(prefix='mct-render-') as folder:
    path=theme_preview.stage(args.theme,folder).with_name('PreviewScene.qml')
    view=QQuickView();view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(QUrl.fromLocalFile(str(path)))
    assert view.status()==QQuickView.Ready,[e.toString() for e in view.errors()]
    view.resize(1600,1000);view.show()
    def js(code):
        expression=QQmlExpression(QQmlEngine.contextForObject(view.rootObject()),view.rootObject(),code)
        expression.evaluate()
        assert not expression.hasError(),expression.error().toString()
    js('backend.preferences.request("reduceMotion",true)')
    if args.panel=='osd':js('backend.setVolume(65)')
    elif args.panel=='switcher':js('cycleWindows(1)')
    elif args.panel!='desktop':js('uiState.toggle("'+args.panel+'","preview")')
    # Allow local font/image loads and scene-graph synchronization before capture.
    QTest.qWait(400)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    assert view.grabWindow().save(str(args.output))
    view.setSource(QUrl());view.close()
