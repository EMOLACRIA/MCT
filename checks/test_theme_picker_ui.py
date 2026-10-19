"""Real Qt rail hover/one-click/keyboard/bounds; no native theme operation runs."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import theme_picker
import test_preferences_ui as qt
from PySide6.QtCore import QUrl, QPoint

ROOT = Path(__file__).resolve().parents[1]


class PickerUiTests(unittest.TestCase):
    def setUp(self):
        qt.WARNINGS.clear(); self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)
        wrapper=self.folder/'PickerTest.qml'
        backdrop=(ROOT/'themes/deltarune/files/style/wallpaper.png').as_uri()
        wrapper.write_text('import QtQuick\nimport "'+(ROOT/'theme-picker').as_uri()+'" as Picker\nItem {\nproperty alias model: state\nImage {anchors.fill:parent;source:"'+backdrop+'";fillMode:Image.PreserveAspectCrop}\nPicker.PickerState {id:state;objectName:"pickerState"}\nPicker.PickerView {id:page;objectName:"pickerView";anchors.fill:parent;state:state}\n}\n')
        self.view=qt.QQuickView(); self.view.setResizeMode(qt.QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl.fromLocalFile(str(wrapper)))
        self.assertEqual(self.view.status(),qt.QQuickView.Ready,[e.toString() for e in self.view.errors()])
        self.view.resize(1600,1000); self.view.show(); self.view.requestActivate()
        self.root=self.view.rootObject(); self.model=self.root.findChild(qt.QObject,'pickerState')
        self.page=self.root.findChild(qt.QObject,'pickerView')
        self.requests=[]; self.closed=[]
        self.model.requested.connect(lambda action,theme:self.requests.append((action,theme)))
        self.page.closeRequested.connect(lambda:self.closed.append(True))
        engine=theme_picker.theme_core.Engine(style=self.folder/'style',state=self.folder/'state',hypr=self.folder/'hypr')
        self.catalog=theme_picker.catalog(engine)
        version=next(entry['version'] for entry in self.catalog['themes'] if entry['id']=='deltarune')
        self.catalog.update(active=dict(id='deltarune',version=version),canRollback=True,reduceMotion=True,fontScale=1)
        self.js('model.run("catalog")'); self.reply('catalog',catalog=self.catalog)
        qt.evaluate(self.page,'forceActiveFocus()'); qt.QTest.qWait(160)

    def tearDown(self):
        self.view.setSource(QUrl()); self.view.close(); self.view.deleteLater(); qt.QTest.qWait(1)
        self.assertFalse(qt.WARNINGS,qt.WARNINGS)
    def js(self,code):return qt.evaluate(self.root,code)
    def reply(self,action,ok=True,**values):
        values.setdefault('message','')
        self.js('model.accept('+json.dumps(dict(action=action,ok=ok,**values))+')'); qt.QTest.qWait(20)
    def item(self,name):
        result=qt.visual_child(self.root,name); self.assertIsNotNone(result,name); return result
    def center(self,name):
        item=self.item(name);return item.mapToScene(item.boundingRect().center()).toPoint()
    def click(self,name):
        qt.QTest.mouseClick(self.view,qt.Qt.LeftButton,pos=self.center(name));qt.QTest.qWait(20)

    def test_hover_expands_photo_without_switch_then_one_click_applies(self):
        self.assertEqual(self.js('model.selectedId'),'deltarune')
        self.assertFalse(self.js('model.canApply'))
        for theme in ('deltarune','plague-tale'):
            for _ in range(100):
                if qt.evaluate(self.item('themeImage-'+theme),'status') != 2:break
                qt.QTest.qWait(20)
            self.assertEqual(qt.evaluate(self.item('themeImage-'+theme),'status'),1)
        qt.QTest.mouseMove(self.view,self.center('selectTheme-plague-tale')); qt.QTest.qWait(40)
        self.assertEqual(self.js('model.selectedId'),'plague-tale')
        self.assertEqual(self.requests,[('catalog','')])
        self.assertGreater(self.item('themePhoto-plague-tale').height(),100)
        self.assertEqual(self.item('themePhoto-deltarune').height(),0)
        self.click('selectTheme-plague-tale')
        self.assertEqual(self.requests[-1],('apply','plague-tale'))
        self.js('model.activate("deltarune");model.activate("plague-tale")')
        self.assertEqual(len(self.requests),2)
        self.reply('apply',theme='plague-tale',catalog=dict(self.catalog,active=dict(id='plague-tale',version='2.9.0')))
        self.assertTrue(self.js('model.isActive')); self.assertFalse(self.js('model.canApply'))

    def test_error_keeps_real_active_theme_and_allows_one_click_retry(self):
        self.js('model.activate("plague-tale")')
        self.reply('apply',ok=False,theme='plague-tale',message='fixture manually changed file',catalog=self.catalog)
        self.assertEqual(self.js('model.activeTheme.id'),'deltarune')
        self.assertIn('fixture',self.item('pickerStatus').property('text'))
        self.assertTrue(self.js('model.canApply'))
        self.js('model.activate("plague-tale")')
        self.assertEqual(self.requests[-1],('apply','plague-tale'))
        self.reply('apply',theme='deltarune')
        self.assertTrue(self.js('model.failed'));self.assertFalse(self.js('model.busy'))

    def test_same_theme_new_version_can_be_applied_without_switching_away(self):
        self.js('model.run("catalog")')
        self.reply('catalog',catalog=dict(self.catalog,active=dict(id='deltarune',version='0.2.0')))
        self.assertEqual(self.js('model.selectedId'),'deltarune')
        self.assertTrue(self.js('model.canApply'))
        self.click('selectTheme-deltarune')
        self.assertEqual(self.requests[-1],('apply','deltarune'))
        self.reply('apply',theme='deltarune',catalog=self.catalog)
        self.assertTrue(self.js('model.isActive'));self.assertFalse(self.js('model.canApply'))

    def test_keyboard_enter_switch_escape_and_restore_confirmation(self):
        qt.QTest.keyClick(self.view,qt.Qt.Key_Right)
        self.assertEqual(self.js('model.selectedId'),'plague-tale')
        qt.QTest.keyClick(self.view,qt.Qt.Key_Return)
        self.assertEqual(self.requests[-1],('apply','plague-tale'))
        qt.QTest.keyClick(self.view,qt.Qt.Key_Escape)
        self.assertTrue(self.closed);self.assertTrue(self.js('model.busy'))
        self.reply('apply',ok=False,theme='plague-tale',message='fixture',catalog=self.catalog)
        self.click('rollbackTheme');self.assertTrue(self.js('model.rollbackArmed'))
        qt.QTest.keyClick(self.view,qt.Qt.Key_Escape);self.assertFalse(self.js('model.rollbackArmed'))
        self.click('rollbackTheme');self.click('rollbackTheme');self.assertEqual(self.requests[-1],('rollback',''))

    def test_spine_preview_and_scale_bounds_and_animation(self):
        for scale in (0.9,1.2):
            self.js('model.fontScale='+str(scale))
            for width,height in ((1600,1000),(900,600),(640,480),(480,400)):
                self.view.resize(width,height);qt.QTest.qWait(30)
                spine=self.item('themeSpine')
                self.assertAlmostEqual(spine.y(),round(height*.5),delta=1)
                self.assertGreaterEqual(spine.x(),0);self.assertLessEqual(spine.x()+spine.width(),width)
                for theme in ('deltarune','plague-tale'):
                    self.js('model.choose('+json.dumps(theme)+')');qt.QTest.qWait(30)
                    photo=self.item('themePhoto-'+theme)
                    self.assertGreaterEqual(photo.mapToScene(photo.boundingRect().topLeft()).y(),0)
                    self.assertLessEqual(photo.mapToScene(photo.boundingRect().bottomRight()).y(),height)
                self.assertFalse(self.view.grabWindow().isNull())
        self.view.resize(1600,1000);self.js('model.fontScale=1;model.reduceMotion=false;model.choose("deltarune")');qt.QTest.qWait(260)
        if os.environ.get('MCT_PICKER_PREVIEW'):self.assertTrue(self.view.grabWindow().save(os.environ['MCT_PICKER_PREVIEW']))

    def test_pending_invalid_and_empty_catalog_prevent_apply(self):
        for changes in (dict(pending=True),dict(stateError='fixture bad state'),dict(themes=[])):
            self.js('model.run("catalog")');self.reply('catalog',catalog=dict(self.catalog,**changes))
            count=len(self.requests);self.js('model.activate("plague-tale")');self.assertEqual(len(self.requests),count)
        invalid=[dict(entry,valid=False,error='fixture broken preview',preview='') for entry in self.catalog['themes']]
        self.js('model.run("catalog")');self.reply('catalog',catalog=dict(self.catalog,themes=invalid))
        self.js('model.activate("plague-tale")');self.assertFalse(self.js('model.canApply'))


if __name__=='__main__':unittest.main()
