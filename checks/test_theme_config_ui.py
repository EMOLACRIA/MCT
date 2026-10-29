"""Theme settings tabs in the real Preferences panel (preview backend: nothing is written)."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_preferences_ui as base
from test_preferences_ui import QObject, QTest, Qt, evaluate, visual_child


class ThemeConfigUiTests(base.PreferenceUiTests):
    def setUp(self):
        super().setUp()
        self.model = self.root.findChild(QObject, 'themeConfigState')
        self.assertIsNotNone(self.model)
        QTest.qWait(30)

    def m(self, code):
        return evaluate(self.model, code)

    def tab(self, index):
        self.click('settingsTab' + str(index)); QTest.qWait(30)

    def type_into(self, name, text):
        field = visual_child(self.root, name); self.assertIsNotNone(field, name)
        evaluate(field, 'selectAll()'); field.forceActiveFocus()
        QTest.mouseClick(self.view, Qt.LeftButton, pos=field.mapToScene(field.boundingRect().center()).toPoint())
        QTest.keyClick(self.view, Qt.Key_A, Qt.ControlModifier); QTest.keyClick(self.view, Qt.Key_Backspace)
        for ch in text: QTest.keyClick(self.view, ch)
        QTest.qWait(20)

    def test_tabs_show_shell_layout_and_theme(self):
        self.assertIsNotNone(visual_child(self.root, 'settingsScroll'))
        self.tab(1)
        self.assertIsNone(visual_child(self.root, 'settingsScroll'))
        self.assertIsNotNone(visual_child(self.root, 'layout-gapsIn'))
        self.tab(2)
        self.assertIsNotNone(visual_child(self.root, 'themeScroll'))
        self.assertFalse(self.m('canApply'))

    def test_layout_switch_seeds_theme_values_and_enables_apply(self):
        self.tab(1)
        self.click('layoutThemeOwn')
        self.assertFalse(self.m('draft.layout.themeOwn'))
        self.assertEqual(self.m('draft.layout.gapsOut'), 14)
        self.m('setLayout("gapsOut",30)')
        self.assertTrue(self.m('dirty')); self.assertTrue(self.m('canApply'))
        self.click('discardThemeConfig')
        self.assertFalse(self.m('dirty'))

    def test_colour_editor_quote_and_reset(self):
        self.tab(2)
        self.click('swatch-accent')
        self.type_into('colorHex', '#00aaff')
        self.assertEqual(self.m('draft.themes.preview.colors.accent'), '#00aaff')
        self.assertTrue(self.m('isChanged("accent")'))
        self.type_into('quoteFirst', 'HELLO ROSE')
        self.assertEqual(self.m('draft.themes.preview.quote'), ['HELLO ROSE', 'YOU CHOSE.'])
        self.assertEqual(self.m('changeCount'), 2)
        self.type_into('quoteSecond', 'a$b')
        self.assertNotEqual(self.m('quoteProblem'), '')
        self.assertFalse(self.m('canApply'))
        self.type_into('quoteSecond', 'NOW.')
        self.assertTrue(self.m('canApply'))
        self.click('applyThemeConfig'); QTest.qWait(40)
        self.assertEqual(self.m('config.themes.preview.colors.accent'), '#00aaff')
        self.assertFalse(self.m('dirty'))
        scroll = visual_child(self.root, 'themeScroll'); evaluate(scroll, 'contentY=contentHeight-height'); QTest.qWait(20)
        self.click('resetThemeConfig')
        self.assertEqual(self.m('changeCount'), 0)
        self.assertTrue(self.m('dirty'))

    def test_surface_opacity_keeps_alpha_in_qt_order(self):
        self.tab(2)
        self.click('swatch-surface')
        self.type_into('colorHex', '#102030')
        value = self.m('draft.themes.preview.colors.surface')
        self.assertTrue(value.endswith('102030') and len(value) == 9, value)

    def test_fastfetch_image_is_rendered_before_apply(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'quote.png'
            # Act as the live store would: not ephemeral, with a real image path.
            self.m('ephemeral=false'); self.m('quoteImagePath=' + json.dumps(str(target)))
            self.tab(2)
            self.type_into('quoteFirst', 'ROSE')
            seen = []
            self.model.requested.connect(lambda action, args: seen.append((action, args.toVariant() if hasattr(args, 'toVariant') else args)))
            self.click('applyThemeConfig')
            for _ in range(100):
                if seen: break
                QTest.qWait(20)
            self.assertTrue(seen, 'apply was not requested')
            action, args = seen[-1]
            self.assertEqual(action, 'apply'); self.assertEqual(list(args)[-1], 'rendered')
            data = target.read_bytes()
            self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
            import struct
            self.assertEqual(struct.unpack('>II', data[16:24]), (1536, 1280))


def load_tests(loader, tests, pattern):
    # Only this class's own tests; the inherited preference tests run in their own file.
    own = [n for n in vars(ThemeConfigUiTests) if n.startswith('test_')]
    return unittest.TestSuite(ThemeConfigUiTests(n) for n in own)


if __name__ == '__main__':
    unittest.main()
