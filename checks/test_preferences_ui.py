"""Real Qt preference UI/model. Preview does not write the user's settings."""
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
import unittest

os.environ['QT_QPA_PLATFORM']='offscreen';os.environ['QT_QUICK_BACKEND']='software'
if os.environ.get('MCT_QT_TEST_PATH'):sys.path.insert(0,os.environ['MCT_QT_TEST_PATH'])
from PySide6.QtCore import QObject,QUrl,Qt,qInstallMessageHandler
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlComponent,QQmlEngine,QQmlExpression
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QTest
ROOT=Path(__file__).resolve().parents[1]
APP=QGuiApplication.instance() or QGuiApplication([]);WARNINGS=[]
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


class PreferenceUiTests(unittest.TestCase):
    def setUp(self):
        WARNINGS.clear();self.view=QQuickView();self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl.fromLocalFile(str(ROOT/'payload/style/shell/PreviewScene.qml')))
        self.assertEqual(self.view.status(),QQuickView.Ready,[e.toString() for e in self.view.errors()])
        self.view.resize(1600,1000);self.view.show();self.view.requestActivate()
        self.root=self.view.rootObject();self.js('uiState.toggle("settings","preview")');QTest.qWait(180)
        self.prefs=self.root.findChild(QObject,'preferencesState');self.assertIsNotNone(self.prefs)
    def tearDown(self):
        self.view.setSource(QUrl());self.view.close();self.view.deleteLater();QTest.qWait(1)
        self.assertFalse(WARNINGS,WARNINGS)
    def js(self,code):return evaluate(self.root,code)
    def state(self,code):return evaluate(self.prefs,code)
    def change(self,key,value):self.state('request('+json.dumps(key)+','+json.dumps(value)+')');QTest.qWait(5)
    def click(self,name):
        button=visual_child(self.root,name);self.assertIsNotNone(button,name)
        QTest.mouseClick(self.view,Qt.LeftButton,pos=button.mapToScene(button.boundingRect().center()).toPoint());QTest.qWait(20)

    def test_controls_button_single_panel_and_escape(self):
        self.js('uiState.toggle("controls","preview")');QTest.qWait(150)
        self.click('openSettings');self.assertEqual(self.js('uiState.activePanel'),'settings')
        QTest.keyClick(self.view,Qt.Key_Escape);self.assertEqual(self.js('uiState.activePanel'),'')

    def test_shared_font_opacity_motion_date_and_osd_preferences(self):
        self.change('fontScale',1.2);self.change('surfaceOpacity',0.75);self.change('reduceMotion',True);self.change('barShowDate',False)
        panel=self.root.findChild(QObject,'settingsPanel')
        self.assertEqual(evaluate(panel,'Theme.fontSize(20)'),24)
        self.assertEqual(evaluate(panel,'Theme.duration(140)'),0)
        self.assertAlmostEqual(evaluate(panel,'Theme.background.a'),0.75,places=2)
        self.assertFalse(self.root.findChild(QObject,'barDate').property('visible'))
        self.change('osdPosition','top');self.js('backend.setVolume(30)');QTest.qWait(10)
        slider=self.root.findChild(QObject,'feedbackSlider');self.assertLess(slider.mapToScene(slider.boundingRect().center()).y(),250)

    def test_slider_keyboard_commits_preview_value(self):
        slider=self.root.findChild(QObject,'fontScaleSlider');self.assertIsNotNone(slider)
        evaluate(slider,'forceActiveFocus()')
        for _ in range(4):QTest.keyClick(self.view,Qt.Key_Right)
        QTest.qWait(20)
        self.assertEqual(self.state('values.fontScale'),1.2)
        self.assertFalse(self.prefs.property('saving'))

    def test_choice_popup_keyboard_changes_position(self):
        scroll=self.root.findChild(QObject,'settingsScroll');evaluate(scroll,'contentY=Math.min(contentHeight-height,350)');QTest.qWait(20)
        choice=visual_child(self.root,'osdPositionChoice');self.assertIsNotNone(choice)
        evaluate(choice,'forceActiveFocus()');QTest.keyClick(self.view,Qt.Key_Space);QTest.qWait(20)
        QTest.keyClick(self.view,Qt.Key_End);QTest.keyClick(self.view,Qt.Key_Return);QTest.qWait(20)
        self.assertEqual(self.state('values.osdPosition'),'top')

    def test_invalid_model_values_and_failed_response_preserve_active_values(self):
        self.change('fontScale',2);self.assertEqual(self.state('values.fontScale'),1)
        self.assertTrue(self.prefs.property('error'))
        self.state('accept({ok:false,action:"save",values:{fontScale:2},error:"fixture write failed"})')
        self.assertEqual(self.state('values.fontScale'),1);self.assertIn('fixture',self.prefs.property('error'))
        self.state('sourceValid=false;request("fontScale",1.1)')
        self.assertEqual(self.state('values.fontScale'),1);self.assertIn('Reset',self.prefs.property('error'))

    def test_reset_requires_two_clicks_and_diagnostics_are_preview_only(self):
        self.change('barFloating',False);QTest.qWait(40)
        scroll=self.root.findChild(QObject,'settingsScroll');evaluate(scroll,'contentY=contentHeight-height');QTest.qWait(20)
        self.click('resetPreferences');self.assertFalse(self.state('values.barFloating'))
        # Confirmation text increases the scroll content; keep its button visible.
        QTest.qWait(40);evaluate(scroll,'contentY=contentHeight-height');QTest.qWait(40)
        self.click('resetPreferences');self.assertTrue(self.state('values.barFloating'))
        self.js('backend.diagnosePreferences()');self.assertIn('no native',self.prefs.property('diagnostics'))

    def test_maximum_scale_render_and_small_screen_bounds(self):
        self.change('fontScale',1.2);self.change('reduceMotion',True);QTest.qWait(30)
        image=self.view.grabWindow();self.assertFalse(image.isNull())
        if os.environ.get('MCT_PREFERENCES_PREVIEW'):image.save(os.environ['MCT_PREFERENCES_PREVIEW'])
        self.view.resize(900,600);QTest.qWait(30)
        frame=self.root.findChild(QObject,'activePanelFrame')
        self.assertLessEqual(frame.width(),900);self.assertLessEqual(frame.height(),500)
        self.assertGreaterEqual(frame.x(),0);self.assertGreaterEqual(frame.y(),0)


class PreferenceModelStorageTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0,str(ROOT/'payload/style/scripts'));import preferences
        self.helper=preferences;self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.env={'HOME':self.tmp.name,'XDG_CONFIG_HOME':self.tmp.name+'/config','PATH':'/fixture/bin'}
        self.engine=QQmlEngine();self.component=QQmlComponent(self.engine,QUrl.fromLocalFile(str(ROOT/'payload/style/shell/ui/PreferencesState.qml')))
        self.assertEqual(self.component.status(),QQmlComponent.Ready,[e.toString() for e in self.component.errors()])
        self.model=self.component.create();self.requests=[]
        self.model.writeRequested.connect(lambda action,candidate:self.requests.append((action,candidate.toVariant())))
    def tearDown(self):
        self.model.deleteLater();QTest.qWait(1);self.engine.deleteLater();QTest.qWait(1)
    def js(self,code):return evaluate(self.model,code)
    def accept(self,packet):self.js('accept('+json.dumps(packet)+')')
    def request(self,key,value):self.js('request('+json.dumps(key)+','+json.dumps(value)+')')

    def test_write_only_becomes_active_after_success_and_survives_model_reload(self):
        self.request('fontScale',1.1);self.assertTrue(self.model.property('saving'))
        self.assertEqual(self.js('values.fontScale'),1)
        action,values=self.requests.pop()
        with patch.object(self.helper.shutil,'which',return_value='/fixture/kitty'):packet=self.helper.handle(action,values,self.env)
        self.accept(packet);self.assertEqual(self.js('values.fontScale'),1.1)
        self.js('values={};ready=false');self.accept(self.helper.handle('read',env=self.env))
        self.assertEqual(self.js('values.fontScale'),1.1);self.assertTrue(self.model.property('ready'))

    def test_failed_atomic_write_does_not_activate_candidate(self):
        self.helper.atomic_write(self.helper.preference_path(self.env),self.helper.defaults())
        self.request('fontScale',1.1);action,values=self.requests.pop()
        with patch.object(self.helper.shutil,'which',return_value='/fixture/kitty'),patch.object(self.helper.os,'replace',side_effect=OSError('fixture denied')):
            self.accept(self.helper.handle(action,values,self.env))
        self.assertEqual(self.js('values.fontScale'),1);self.assertIn('not saved',self.model.property('error'))

    def test_invalid_source_requires_explicit_reset_and_keeps_backup(self):
        path=self.helper.preference_path(self.env);path.parent.mkdir(parents=True);path.write_text('{broken')
        self.accept(self.helper.handle('read',env=self.env));self.assertFalse(self.model.property('sourceValid'))
        self.request('fontScale',1.1);self.assertFalse(self.requests)
        self.js('reset()');action,values=self.requests.pop();packet=self.helper.handle(action,values,self.env)
        self.accept(packet);self.assertTrue(self.model.property('sourceValid'));self.assertEqual(Path(packet['backup']).read_text(),'{broken')


if __name__=='__main__':unittest.main()
