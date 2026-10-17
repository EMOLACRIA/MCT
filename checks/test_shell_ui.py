import os,sys,json
from pathlib import Path
os.environ['QT_QPA_PLATFORM']='offscreen';os.environ['QT_QUICK_BACKEND']='software'
sys.path.insert(0,str(Path('build/qs-qt-check').resolve()))
from PySide6.QtCore import QObject,QUrl,QTimer,Qt,qInstallMessageHandler
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlExpression
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QTest
warnings=[]
def msg(kind,context,message):
 if 'file:' in message or 'QML' in message:
  warnings.append(message);print(message,flush=True)
qInstallMessageHandler(msg)
app=QGuiApplication([]);view=QQuickView();view.setResizeMode(QQuickView.SizeRootObjectToView)
view.setSource(QUrl.fromLocalFile(str(Path('build/desktop-style/payload/style/shell/PreviewScene.qml').resolve())))
assert view.status()==QQuickView.Ready,view.errors()
view.resize(1600,1000);view.show();root=view.rootObject();ctx=view.rootContext()
controller=root.findChild(QObject,'uiState');ctx.setContextProperty('testState',controller)
ctx.setContextProperty('testBackend',root.findChild(QObject,'demoContext'))
def js(code):
 e=QQmlExpression(ctx,root,code);v=e.evaluate();assert not e.hasError(),e.error().toString();return v[0]
out=Path('build/desktop-style/previews');out.mkdir(exist_ok=True)
steps=[('desktop',''),('launcher','launcher'),('power','power'),('controls','controls'),('notifications','notifications'),('media','media'),('hardware','hardware')]
index=0

def tick():
 global index
 if index<len(steps):
  name,panel=steps[index];index+=1
  js('testState.close();'+('testState.toggle('+json.dumps(panel)+',"preview");' if panel else ''))
  QTimer.singleShot(250,lambda n=name:capture(n))
 else:behavior()

def capture(name):
 assert view.grabWindow().save(str(out/(name+'.png')))
 if name in ['launcher','power','hardware']:
  f=root.findChild(QObject,'activePanelFrame');assert abs(f.property('x')-(1600-f.property('width'))/2)<1;assert abs(f.property('y')-(1000-f.property('height'))/2)<1
 print('Rendered',name,flush=True);QTimer.singleShot(20,tick)

def behavior():
 try:
  js('testState.toggle("launcher","preview");testState.toggle("launcher","preview");')
  assert controller.property('activePanel')==''
  js('testState.toggle("launcher","preview");testState.toggle("power","preview");')
  assert controller.property('activePanel')=='power'
  js('testState.confirmation="restart";testState.close();')
  assert controller.property('confirmation')==''
  js('testState.toggle("launcher","preview");testState.search="godot";')
  QTimer.singleShot(150,search_test)
 except Exception as e:print('FAIL',repr(e),flush=True);app.exit(1)

def search_test():
 try:
  lst=root.findChild(QObject,'applicationList');assert lst.property('count')==1
  js('testState.search="zzzznonexistent";')
  app.processEvents();assert lst.property('count')==0
  js('testState.close();testState.toggle("power","preview");')
  app.processEvents()
  power=root.findChild(QObject,'confirmPower');js('testState.confirmation="restart";')
  app.processEvents();power.clicked.emit();assert controller.property('activePanel')==''
  assert root.findChild(QObject,'demoContext').property('lastAction')=='Preview · restart selected'
  js('testBackend.setVolume(23);')
  assert controller.property('feedbackLevel')==23 and controller.property('feedbackVisible')
  view.resize(900,600);js('testState.toggle("launcher","preview");')
  QTimer.singleShot(180,small_test)
 except Exception as e:print('FAIL',repr(e),flush=True);app.exit(1)

def small_test():
 try:
  f=root.findChild(QObject,'activePanelFrame');assert f.property('width')<=852 and f.property('height')<=500
  QTest.keyClick(view,Qt.Key_Escape);app.processEvents();assert controller.property('activePanel')==''
  assert not warnings,warnings
  print('PASS: shared QML renders all seven views, keyboard Escape, filtering, repeated toggle, cross-menu transition, confirmed power action, OSD and small-screen bounds.',flush=True)
  app.quit()
 except Exception as e:print('FAIL',repr(e),flush=True);app.exit(1)
QTimer.singleShot(100,tick);code=app.exec();view.setSource(QUrl());sys.exit(code)
