"""Real Qt picker input/photos/bounds; helper requests are captured, never executed."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import theme_picker
import test_preferences_ui as qt
from PySide6.QtCore import QUrl

ROOT = Path(__file__).resolve().parents[1]


class PickerUiTests(unittest.TestCase):
    def setUp(self):
        qt.WARNINGS.clear()
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        wrapper = self.folder/'PickerTest.qml'
        wrapper.write_text('import QtQuick\nimport "'+(ROOT/'theme-picker').as_uri()+'" as Picker\nItem {\nproperty alias model: state\nPicker.PickerState {id:state;objectName:"pickerState"}\nPicker.PickerView {id:page;objectName:"pickerView";anchors.fill:parent;state:state}\n}\n')
        self.view = qt.QQuickView(); self.view.setResizeMode(qt.QQuickView.SizeRootObjectToView)
        self.view.setSource(QUrl.fromLocalFile(str(wrapper)))
        self.assertEqual(self.view.status(), qt.QQuickView.Ready, [e.toString() for e in self.view.errors()])
        self.view.resize(1080, 760); self.view.show(); self.view.requestActivate()
        self.root = self.view.rootObject(); self.model = self.root.findChild(qt.QObject, 'pickerState')
        self.page = self.root.findChild(qt.QObject, 'pickerView')
        self.requests = []; self.model.requested.connect(lambda action, theme:self.requests.append((action,theme)))
        engine = theme_picker.theme_core.Engine(style=self.folder/'style', state=self.folder/'state', hypr=self.folder/'hypr')
        self.catalog = theme_picker.catalog(engine)
        self.catalog['active'] = dict(id='deltarune',version='0.2.0'); self.catalog['canRollback'] = True
        self.js('model.run("catalog")')
        self.reply('catalog', catalog=self.catalog)
        qt.evaluate(self.page,'forceActiveFocus()'); qt.QTest.qWait(160)

    def tearDown(self):
        self.view.setSource(QUrl()); self.view.close(); self.view.deleteLater(); qt.QTest.qWait(1)
        self.assertFalse(qt.WARNINGS, qt.WARNINGS)

    def js(self, code):return qt.evaluate(self.root, code)
    def reply(self, action, ok=True, **values):
        values.setdefault('message', '')
        self.js('model.accept('+json.dumps(dict(action=action,ok=ok,**values))+')')
        qt.QTest.qWait(10)
    def item(self, name):
        result = qt.visual_child(self.root, name); self.assertIsNotNone(result, name); return result
    def click(self, name):
        item = self.item(name)
        qt.QTest.mouseClick(self.view, qt.Qt.LeftButton, pos=item.mapToScene(item.boundingRect().center()).toPoint())
        qt.QTest.qWait(10)
    def select_other(self):self.click('chooseTheme-plague-tale')

    def test_photos_selection_keyboard_and_apply_guard(self):
        self.assertEqual(self.js('model.selectedId'), 'deltarune')
        self.assertFalse(self.item('applyTheme').isEnabled())
        for theme in ('plague-tale','deltarune'):
            self.assertEqual(qt.evaluate(self.item('themeImage-'+theme),'status'), 1)
        qt.QTest.keyClick(self.view, qt.Qt.Key_Right)
        self.assertEqual(self.js('model.selectedId'), 'plague-tale')
        self.click('checkTheme')
        self.assertEqual(self.requests[-1], ('check','plague-tale'))
        self.assertFalse(self.item('chooseTheme-deltarune').isEnabled())
        self.js('model.run("apply");model.choose("deltarune")')
        self.assertEqual(self.js('model.selectedId'), 'plague-tale')
        self.reply('check', theme='plague-tale')
        self.assertTrue(self.item('applyTheme').isEnabled())
        self.click('applyTheme')
        self.assertEqual(self.requests[-1], ('apply','plague-tale'))
        changed=dict(self.catalog,active=dict(id='plague-tale',version='2.9.0'))
        self.reply('apply', theme='plague-tale', catalog=changed)
        self.assertTrue(self.js('model.isActive')); self.assertFalse(self.item('applyTheme').isEnabled())

    def test_check_is_invalidated_and_error_keeps_retry_available(self):
        self.select_other(); self.click('checkTheme'); self.reply('check',theme='plague-tale')
        self.click('chooseTheme-deltarune'); self.select_other()
        self.assertFalse(self.item('applyTheme').isEnabled())
        self.click('checkTheme'); self.reply('check',ok=False,theme='plague-tale',message='fixture modified file')
        self.assertIn('fixture',self.item('pickerStatus').property('text'))
        self.assertFalse(self.item('applyTheme').isEnabled()); self.assertTrue(self.item('checkTheme').isEnabled())
        self.click('checkTheme'); self.reply('check',theme='deltarune')
        self.assertTrue(self.js('model.failed')); self.assertFalse(self.js('model.busy'))

    def test_restore_needs_confirmation_escape_cancels(self):
        self.click('rollbackTheme')
        self.assertTrue(self.js('model.rollbackArmed')); self.assertEqual(self.requests, [('catalog','')])
        qt.QTest.keyClick(self.view, qt.Qt.Key_Escape)
        self.assertFalse(self.js('model.rollbackArmed'))
        self.click('rollbackTheme'); self.click('rollbackTheme')
        self.assertEqual(self.requests[-1],('rollback',''))
        self.reply('rollback',catalog=dict(self.catalog,active=None,canRollback=False))
        self.assertFalse(self.item('rollbackTheme').isEnabled())

    def test_enlarged_photo_escape_and_responsive_scroll(self):
        self.click('enlargeTheme-deltarune')
        self.assertTrue(qt.evaluate(self.page,'enlarged !== null'))
        qt.QTest.keyClick(self.view, qt.Qt.Key_Escape)
        self.assertTrue(qt.evaluate(self.page,'enlarged === null'))
        for width,height in [(1080,760),(640,480),(480,400)]:
            self.view.resize(width,height); qt.QTest.qWait(30)
            scroll=self.item('themePickerScroll')
            self.assertGreaterEqual(scroll.x(),0); self.assertLessEqual(scroll.x()+scroll.width(),width)
            for name in ('chooseTheme-deltarune','chooseTheme-plague-tale'):
                button=self.item(name); self.assertLessEqual(button.mapToScene(button.boundingRect().bottomRight()).x(),width)
            for name in ('checkTheme','applyTheme','rollbackTheme'):
                button=self.item(name); bottom=button.mapToScene(button.boundingRect().bottomRight())
                self.assertLessEqual(bottom.x(),width); self.assertLessEqual(bottom.y(),height)
            self.assertFalse(self.view.grabWindow().isNull())
        if os.environ.get('MCT_PICKER_PREVIEW'):
            self.assertTrue(self.view.grabWindow().save(str(Path(os.environ['MCT_PICKER_PREVIEW']).with_stem('theme-picker-small'))))
        self.js('model.choose("plague-tale")'); qt.QTest.qWait(20)
        card=self.item('chooseTheme-plague-tale').parentItem().parentItem().parentItem()
        self.assertLess(card.mapToScene(card.boundingRect().topLeft()).y(), 100)
        self.view.resize(1080,760); qt.QTest.qWait(30)
        if os.environ.get('MCT_PICKER_PREVIEW'):
            self.assertTrue(self.view.grabWindow().save(os.environ['MCT_PICKER_PREVIEW']))

    def test_pending_invalid_or_empty_catalog_blocks_changes(self):
        for changes in [dict(pending=True),dict(stateError='fixture bad state'),dict(themes=[])]:
            self.js('model.run("catalog")'); self.reply('catalog',catalog=dict(self.catalog,**changes))
            self.assertFalse(self.item('applyTheme').isEnabled()); self.assertFalse(self.item('checkTheme').isEnabled())
        invalid=[dict(entry,valid=False,error='fixture broken preview',preview='') for entry in self.catalog['themes']]
        self.js('model.run("catalog")'); self.reply('catalog',catalog=dict(self.catalog,themes=invalid))
        self.js('model.choose("plague-tale")')
        self.assertFalse(self.item('checkTheme').isEnabled()); self.assertFalse(self.item('enlargeTheme-plague-tale').isEnabled())


if __name__ == '__main__':unittest.main()
