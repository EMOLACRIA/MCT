"""Real Qt signal/debounce checks; PySide6 required, no native notification bus."""
import os
from pathlib import Path
import sys
import tempfile
import unittest

os.environ['QT_QPA_PLATFORM']='offscreen'
os.environ['QT_QUICK_BACKEND']='software'
if os.environ.get('MCT_QT_TEST_PATH'):sys.path.insert(0,os.environ['MCT_QT_TEST_PATH'])
from PySide6.QtCore import QObject,Property,Signal,QUrl,qInstallMessageHandler
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlComponent,QQmlEngine,QQmlExpression,qmlRegisterType
from PySide6.QtTest import QTest

ROOT=Path(__file__).resolve().parents[1]
APP=QGuiApplication.instance() or QGuiApplication([])
WARNINGS=[]
qInstallMessageHandler(lambda kind,context,message:WARNINGS.append(message))


class TestNotification(QObject):
    # "transient" is reserved in QML declarations; the native API exposes it
    # as a C++ property, so provide the same shape through Qt's meta-object.
    transientChanged=Signal()
    def __init__(self,parent=None):super().__init__(parent);self._transient=False
    def read_transient(self):return self._transient
    def write_transient(self,value):
        if self._transient!=value:self._transient=value;self.transientChanged.emit()
    transient=Property(bool,read_transient,write_transient,notify=transientChanged)


qmlRegisterType(TestNotification,'MCT.Test',1,0,'TestNotification')

class WatcherTests(unittest.TestCase):
    def setUp(self):
        WARNINGS.clear()
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        folder=Path(self.tmp.name);(folder/'ui').symlink_to(ROOT/'payload/style/shell/ui',target_is_directory=True)
        self.engine=QQmlEngine();self.component=QQmlComponent(self.engine)
        self.component.setData(b'''
import QtQuick
import MCT.Test 1.0
import "ui"
Item {
    id:root
    property int updates:0
    property alias note:sample
    TestNotification {
        id:sample
        property string summary:"Before"
        property string body:"Before"
        property string appName:"Files"
        property var actions:[]
        property int expireTimeout:5000
        signal closed(int reason)
    }
    Component {
        id:factory
        NotificationWatcher {objectName:"testWatcher";onUpdated:root.updates++}
    }
    Component.onCompleted:factory.createObject(root,{notification:sample})
}
''',QUrl.fromLocalFile(str(folder/'Harness.qml')))
        self.assertEqual(self.component.status(),QQmlComponent.Ready,[e.toString() for e in self.component.errors()])
        self.root=self.component.create();self.assertIsNotNone(self.root)
        self.context=QQmlEngine.contextForObject(self.root)

    def tearDown(self):
        self.root.deleteLater();QTest.qWait(10)
        self.engine.deleteLater();QTest.qWait(10)
        self.assertFalse(WARNINGS,WARNINGS)

    def js(self,code):
        expression=QQmlExpression(self.context,self.root,code)
        result=expression.evaluate()
        self.assertFalse(expression.hasError(),expression.error().toString())
        return result

    def test_grouped_title_body_and_app_updates_refresh_once(self):
        self.js('note.summary="Copy 75%";note.body="Updated";note.appName="Transfer";')
        QTest.qWait(30)
        self.assertEqual(self.root.property('updates'),1)

    def test_actions_timeout_and_transient_changes_are_observed(self):
        for index,code in enumerate(['note.actions=[{identifier:"open",text:"Open"}]','note.expireTimeout=100','note.transient=true'],start=1):
            self.js(code);QTest.qWait(30)
            self.assertEqual(self.root.property('updates'),index)

    def test_close_cancels_pending_refresh_and_destroys_watcher(self):
        self.js('note.summary="Pending";note.closed(1);')
        QTest.qWait(30)
        self.assertEqual(self.root.property('updates'),0)
        self.assertIsNone(self.root.findChild(QObject,'testWatcher'))

    def test_updates_after_close_do_not_refresh(self):
        self.js('note.closed(1)');QTest.qWait(30)
        self.js('note.summary="Closed";note.expireTimeout=100;');QTest.qWait(30)
        self.assertEqual(self.root.property('updates'),0)


if __name__=='__main__':unittest.main()
