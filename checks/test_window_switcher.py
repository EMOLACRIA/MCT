"""Real Qt switcher state and keyboard tests. No compositor/window activation."""
import json
import os
from pathlib import Path
import sys
import unittest

os.environ['QT_QPA_PLATFORM']='offscreen';os.environ['QT_QUICK_BACKEND']='software'
if os.environ.get('MCT_QT_TEST_PATH'):sys.path.insert(0,os.environ['MCT_QT_TEST_PATH'])
from PySide6.QtCore import QObject,QUrl,Qt,QEvent,QCoreApplication,qInstallMessageHandler
from PySide6.QtGui import QGuiApplication,QKeyEvent
from PySide6.QtQml import QQmlComponent,QQmlEngine,QQmlExpression
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QTest

ROOT=Path(__file__).resolve().parents[1]
APP=QGuiApplication.instance() or QGuiApplication([])
WARNINGS=[]
qInstallMessageHandler(lambda kind,context,message:WARNINGS.append(message))
WINDOWS=[{'id':'0x'+str(i),'title':'Window '+str(i),'appName':'App','icon':'','workspaceLabel':str(ws),'monitor':'eDP-1','focusOrder':i-1} for i,ws in [(1,4),(2,9),(3,2),(4,10)]]


def evaluate(obj,code):
    e=QQmlExpression(QQmlEngine.contextForObject(obj),obj,code);result=e.evaluate()[0]
    if e.hasError():raise AssertionError(e.error().toString())
    return result.toVariant() if hasattr(result,'toVariant') else result


class StateTests(unittest.TestCase):
    def setUp(self):
        WARNINGS.clear();self.engine=QQmlEngine()
        self.component=QQmlComponent(self.engine,QUrl.fromLocalFile(str(ROOT/'payload/style/shell/ui/WindowSwitcherState.qml')))
        self.assertEqual(self.component.status(),QQmlComponent.Ready,[e.toString() for e in self.component.errors()])
        self.state=self.component.create();self.commits=[];self.state.committed.connect(self.commits.append)
        self.js('windows='+json.dumps(WINDOWS)+';activeWindowId="0x1";')
    def tearDown(self):
        self.state.deleteLater();QTest.qWait(1);self.engine.deleteLater();QTest.qWait(1)
        self.assertFalse(WARNINGS,WARNINGS)
    def js(self,code):return evaluate(self.state,code)

    def test_forward_reverse_and_cross_workspace_commit(self):
        self.js('begin(1,"eDP-1")');self.assertEqual(self.js('selectedId'),'0x2')
        self.assertEqual(self.js('selected.workspaceLabel'),'9')
        self.js('step(1);step(-1);commit();commit()')
        self.assertEqual(self.commits,['0x2']);self.assertFalse(self.js('active'))
        self.js('begin(-1,"eDP-1")');self.assertEqual(self.js('selectedId'),'0x4')

    def test_mru_and_snapshot_order_are_stable(self):
        self.js('activeWindowId="0x3";activeWindowId="0x1";begin(1,"eDP-1")')
        self.assertEqual(self.js('selectedId'),'0x3')
        before=self.js('JSON.stringify(order)')
        self.js('windows=windows.slice().reverse()')
        self.assertEqual(self.js('JSON.stringify(order)'),before)

    def test_closed_selected_window_is_replaced_without_stale_activation(self):
        self.js('begin(1,"eDP-1");windows=windows.filter(w=>w.id!=="0x2")')
        self.assertEqual(self.js('selectedId'),'0x3')
        self.js('commit()');self.assertEqual(self.commits,['0x3'])

    def test_new_window_is_appended_and_title_updates_preserve_selection(self):
        self.js('begin(1,"eDP-1");windows=windows.map(w=>Object.assign({},w,{title:"Changed"})).concat([{id:"0x5",title:"New",focusOrder:0}])')
        self.assertEqual(self.js('selectedId'),'0x2');self.assertEqual(self.js('selected.title'),'Changed')
        self.assertEqual(self.js('order[order.length-1]'),'0x5')

    def test_external_focus_cancels_and_layer_focus_does_not(self):
        self.js('begin(1,"eDP-1");activeWindowId=""');self.assertTrue(self.js('active'))
        self.js('activeWindowId="0x3"');self.assertFalse(self.js('active'));self.assertFalse(self.commits)

    def test_repeated_cycle_keeps_initial_screen_and_reverse_wraps(self):
        self.js('begin(1,"eDP-1");begin(1,"DP-1")')
        self.assertEqual(self.js('screenName'),'eDP-1')
        self.assertEqual(self.js('selectedId'),'0x3')
        self.js('step(-1);step(-1);step(-1)')
        self.assertEqual(self.js('selectedId'),'0x4')

    def test_empty_and_single_window_states(self):
        self.js('windows=[];begin(1,"eDP-1")');self.assertFalse(self.js('active'))
        self.js('windows='+json.dumps(WINDOWS[:1])+';begin(1,"eDP-1");commit()')
        self.assertEqual(self.commits,['0x1'])
        self.js('begin(1,"eDP-1");windows=[]');self.assertFalse(self.js('active'))

    def test_cancel_and_invalid_selection_do_not_activate(self):
        self.js('begin(1,"eDP-1");choose("unknown");cancel();commit()')
        self.assertFalse(self.commits)


class KeyboardTests(unittest.TestCase):
    def setUp(self):
        WARNINGS.clear();self.view=QQuickView();self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl.fromLocalFile(str(ROOT/'payload/style/shell/PreviewScene.qml')))
        self.assertEqual(self.view.status(),QQuickView.Ready,[e.toString() for e in self.view.errors()])
        self.view.resize(1600,1000);self.view.show();self.view.requestActivate();QTest.qWait(40)
        self.root=self.view.rootObject();self.state=self.root.findChild(QObject,'windowSwitcherState')
    def tearDown(self):
        self.view.setSource(QUrl());self.view.close();self.view.deleteLater();QTest.qWait(1)
        self.assertFalse(WARNINGS,WARNINGS)
    def js(self,code):return evaluate(self.root,code)

    def test_alt_release_commits_and_escape_cancels(self):
        QTest.keyPress(self.view,Qt.Key_Alt);QTest.keyPress(self.view,Qt.Key_Tab,Qt.AltModifier)
        # QTest.keyRelease synthesizes modifier-up events. Deliver only Tab-up
        # to represent holding Alt across multiple Tab presses.
        QCoreApplication.sendEvent(self.view,QKeyEvent(QEvent.KeyRelease,Qt.Key_Tab,Qt.AltModifier));QTest.qWait(30)
        self.assertTrue(self.state.property('active'))
        self.assertEqual(self.state.property('selectedId'),'0x102')
        QCoreApplication.sendEvent(self.view,QKeyEvent(QEvent.KeyPress,Qt.Key_Tab,Qt.AltModifier))
        QCoreApplication.sendEvent(self.view,QKeyEvent(QEvent.KeyRelease,Qt.Key_Tab,Qt.AltModifier))
        self.assertTrue(self.state.property('active'));self.assertEqual(self.state.property('selectedId'),'0x103')
        QTest.keyRelease(self.view,Qt.Key_Alt);QTest.qWait(20)
        self.assertFalse(self.state.property('active'))
        self.assertEqual(self.root.findChild(QObject,'demoContext').property('activeWindowId'),'0x103')
        self.js('cycleWindows(1)');QTest.qWait(20);QTest.keyClick(self.view,Qt.Key_Escape)
        self.assertFalse(self.state.property('active'))

    def test_keyboard_navigation_enter_and_small_screen_bounds(self):
        self.js('cycleWindows(1)');QTest.qWait(30)
        QTest.keyClick(self.view,Qt.Key_Tab);self.assertEqual(self.state.property('selectedId'),'0x103')
        QTest.keyClick(self.view,Qt.Key_Backtab,Qt.ShiftModifier);self.assertEqual(self.state.property('selectedId'),'0x102')
        self.view.resize(500,400);QTest.qWait(30)
        frame=self.root.findChild(QObject,'windowSwitcherFrame')
        self.assertLessEqual(frame.width(),460);self.assertLessEqual(frame.height(),320)
        QTest.keyClick(self.view,Qt.Key_Return);self.assertFalse(self.state.property('active'))

    def test_other_panel_closes_switcher_and_render_has_content(self):
        self.js('cycleWindows(1)');QTest.qWait(30)
        self.assertGreater(self.root.findChild(QObject,"windowSwitcherList").width(),200)
        image=self.view.grabWindow();self.assertFalse(image.isNull())
        if os.environ.get('MCT_SWITCHER_PREVIEW'):image.save(os.environ['MCT_SWITCHER_PREVIEW'])
        self.js('uiState.toggle("launcher","preview")')
        self.assertFalse(self.state.property('active'))


if __name__=='__main__':unittest.main()
