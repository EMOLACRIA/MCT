"""Real Qt launcher interaction; DemoContext clipboard, no native Wayland session."""
import json
import os
from pathlib import Path
import sys
import unittest

os.environ['QT_QPA_PLATFORM']='offscreen';os.environ['QT_QUICK_BACKEND']='software'
if os.environ.get('MCT_QT_TEST_PATH'):sys.path.insert(0,os.environ['MCT_QT_TEST_PATH'])
from PySide6.QtCore import QObject,QUrl,Qt,qInstallMessageHandler
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlEngine,QQmlExpression
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QTest

ROOT=Path(__file__).resolve().parents[1]
APP=QGuiApplication.instance() or QGuiApplication([])
WARNINGS=[]
qInstallMessageHandler(lambda kind,context,message:WARNINGS.append(message))


def evaluate(obj,code):
    e=QQmlExpression(QQmlEngine.contextForObject(obj),obj,code);value=e.evaluate()[0]
    if e.hasError():raise AssertionError(e.error().toString())
    return value.toVariant() if hasattr(value,'toVariant') else value


def visual_child(item,name):
    if item.objectName()==name and item.isVisible():return item
    for child in item.childItems():
        found=visual_child(child,name)
        if found:return found
    return None


class LauncherTests(unittest.TestCase):
    def setUp(self):
        WARNINGS.clear();self.view=QQuickView();self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl.fromLocalFile(str(ROOT/'payload/style/shell/PreviewScene.qml')))
        self.assertEqual(self.view.status(),QQuickView.Ready,[e.toString() for e in self.view.errors()])
        self.view.resize(1600,1000);self.view.show();self.view.requestActivate()
        self.root=self.view.rootObject();self.js('uiState.toggle("launcher","preview")');QTest.qWait(40)
        self.launcher=self.root.findChild(QObject,'launcher');self.assertIsNotNone(self.launcher)
        self.backend=self.root.findChild(QObject,'demoContext');self.state=self.root.findChild(QObject,'uiState')
        self.list=self.root.findChild(QObject,'applicationList')
    def tearDown(self):
        self.view.setSource(QUrl());self.view.close();self.view.deleteLater();QTest.qWait(1)
        self.assertFalse(WARNINGS,WARNINGS)
    def js(self,code):return evaluate(self.root,code)
    def query(self,text):self.js('uiState.search='+json.dumps(text));QTest.qWait(20)
    def calc(self,code):return evaluate(self.launcher,code)

    def test_result_enter_copies_and_keeps_input_open(self):
        self.query('(12+3)*4');self.assertEqual(self.calc('calculation.text'),'60')
        self.assertEqual(self.list.property('count'),1)
        QTest.keyClick(self.view,Qt.Key_Return)
        self.assertEqual(self.backend.property('copiedText'),'60')
        self.assertEqual(self.state.property('activePanel'),'launcher')
        self.assertEqual(self.state.property('search'),'(12+3)*4')
        self.assertEqual(self.calc('copiedText'),'60')
        self.query('50%');self.assertEqual(self.calc('calculation.text'),'0.5');self.assertEqual(self.calc('copiedText'),'')

    def test_real_qml_parser_handles_commas_unary_power_and_messages(self):
        for query,value in [('1,5 + .25','1.75'),('-2^2','-4'),('200 * 10%','20'),('0.1+0.2','0.3')]:
            self.query(query);self.assertEqual(self.calc('calculation.text'),value)
        for query,state in [('2+','incomplete'),('(2+3','incomplete'),('1/0','error'),('=alert(1)','error')]:
            self.query(query);self.assertEqual(self.calc('calculation.state'),state)
            QTest.keyClick(self.view,Qt.Key_Return)
            self.assertEqual(self.backend.property('copiedText'),'')
            self.assertEqual(self.backend.property('lastAction'),'')

    def test_app_search_enter_and_escape_still_work(self):
        self.assertEqual(self.list.property('count'),7)
        self.query('godot');self.assertEqual(self.list.property('count'),1)
        QTest.keyClick(self.view,Qt.Key_Return);self.assertEqual(self.backend.property('lastAction'),'Preview · Open godot')
        self.assertEqual(self.state.property('activePanel'),'')
        self.js('uiState.toggle("launcher","preview")');QTest.qWait(30)
        QTest.keyClick(self.view,Qt.Key_Escape);self.assertEqual(self.state.property('activePanel'),'')

    def test_mixed_results_keyboard_selection_and_direct_copy(self):
        self.js('backend.applications=backend.applications.concat([{id:"number-app",name:"123",comment:"Numeric app",icon:""}])')
        self.query('123');self.assertEqual(self.list.property('count'),2)
        QTest.keyClick(self.view,Qt.Key_Down);self.assertEqual(self.list.property('currentIndex'),1)
        QTest.keyClick(self.view,Qt.Key_Return,Qt.ControlModifier)
        self.assertEqual(self.backend.property('copiedText'),'123')
        self.assertEqual(self.state.property('activePanel'),'launcher')
        self.assertNotIn('Open',self.backend.property('lastAction'))
        QTest.keyClick(self.view,Qt.Key_Down);QTest.keyClick(self.view,Qt.Key_Return)
        self.assertEqual(self.backend.property('lastAction'),'Preview · Open number-app')

    def test_mouse_copy_and_feedback_reset(self):
        self.query('12/5')
        button=visual_child(self.root,'copyCalculation');self.assertIsNotNone(button)
        p=button.mapToScene(button.boundingRect().center()).toPoint()
        QTest.mouseClick(self.view,Qt.LeftButton,pos=p);QTest.qWait(10)
        self.assertEqual(self.backend.property('copiedText'),'2.4');self.assertEqual(button.property('text'),'Copied')
        self.query('12/4');self.assertEqual(visual_child(self.root,'copyCalculation').property('text'),'Copy')
        self.assertTrue(self.root.findChild(QObject,'applicationSearch').property('activeFocus'))

    def test_ctrl_c_remains_text_copy_and_query_change_resets_selection(self):
        self.query('12+3')
        QTest.keyClick(self.view,Qt.Key_A,Qt.ControlModifier);QTest.keyClick(self.view,Qt.Key_C,Qt.ControlModifier)
        self.assertEqual(APP.clipboard().text(),'12+3');self.assertEqual(self.backend.property('copiedText'),'')
        self.query('blender');self.assertEqual(self.list.property('currentIndex'),0)
        self.query('godot');self.assertEqual(self.list.property('currentIndex'),0)
        QTest.keyClick(self.view,Qt.Key_Return);self.assertEqual(self.backend.property('lastAction'),'Preview · Open godot')

    def test_render_and_smaller_screen_bounds(self):
        self.query('(2400 * 15%) + 120');QTest.qWait(180)
        image=self.view.grabWindow();self.assertFalse(image.isNull())
        if os.environ.get('MCT_CALCULATOR_PREVIEW'):image.save(os.environ['MCT_CALCULATOR_PREVIEW'])
        self.view.resize(900,600);QTest.qWait(30)
        frame=self.root.findChild(QObject,'activePanelFrame')
        self.assertGreaterEqual(frame.x(),0);self.assertGreaterEqual(frame.y(),0)
        self.assertLessEqual(frame.width(),900);self.assertLessEqual(frame.height(),600)
        row=visual_child(self.root,'calculationRow');self.assertGreater(row.width(),300)
        self.assertTrue(visual_child(self.root,'copyCalculation').property('visible'))


if __name__=='__main__':unittest.main()
