"""Both reviewed skins use one interaction implementation; no live services."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import theme_preview
import test_preferences_ui as qt

ROOT = Path(__file__).resolve().parents[1]


class SharedSurfaceTests(unittest.TestCase):
    def test_skin_wrappers_do_not_copy_commands_or_input_handlers(self):
        names = [p.stem.removesuffix('Surface') for p in
                 (ROOT/'payload/style/shell/surfaces').glob('*Surface.qml')]
        for theme in ('plague-tale', 'deltarune', 'deltarune-snowgrave'):
            for name in names:
                text = (ROOT/'themes'/theme/'files/style/shell/ui'/f'{name}.qml').read_text()
                self.assertIn(name+'Surface {', text)
                for forbidden in ('function ', 'Keys.', 'onClicked:', 'onCommit:',
                                  'onMoved:', 'sessionAction(', 'copyText('):
                    self.assertNotIn(forbidden, text, (theme, name))

    def test_repeated_panels_keep_one_instance_and_clear_confirmation(self):
        old_root = qt.ROOT
        self.addCleanup(setattr, qt, 'ROOT', old_root)
        for theme in ('plague-tale', 'deltarune', 'deltarune-snowgrave'):
            with self.subTest(theme=theme), tempfile.TemporaryDirectory() as folder:
                theme_preview.stage(theme, Path(folder)/'payload')
                qt.ROOT = Path(folder)
                fixture = qt.PreferenceUiTests()
                fixture.setUp()
                try:
                    instances = {}
                    for cycle in range(12):
                        fixture.view.resize(640 if cycle % 2 else 1600, 480 if cycle % 2 else 1000)
                        for panel, name in [('launcher','applicationSearch'), ('controls','openSettings'),
                                            ('power','sessionAction-poweroff'), ('settings','settingsScroll')]:
                            fixture.js('uiState.close();uiState.toggle("'+panel+'","preview")')
                            qt.QTest.qWait(25)
                            item = qt.visual_child(fixture.root, name)
                            self.assertIsNotNone(item, (theme, cycle, panel))
                            if panel in instances:
                                self.assertEqual(item, instances[panel])
                            instances[panel] = item
                    fixture.js('uiState.close();uiState.toggle("power","preview");uiState.confirmation="poweroff"')
                    fixture.js('uiState.close();uiState.toggle("power","preview")')
                    qt.QTest.qWait(25)
                    self.assertEqual(fixture.js('uiState.confirmation'), '')
                    fixture.js('uiState.close();uiState.toggle("settings","preview")')
                    qt.QTest.qWait(25)
                    settings = qt.visual_child(fixture.root, 'settingsPanel')
                    scroll = qt.visual_child(fixture.root, 'settingsScroll')
                    qt.evaluate(scroll, 'contentY=contentHeight-height')
                    qt.QTest.qWait(25)
                    fixture.click('resetPreferences')
                    self.assertTrue(settings.property('resetPending'))
                    fixture.js('uiState.close();uiState.toggle("settings","preview")')
                    qt.QTest.qWait(25)
                    settings = qt.visual_child(fixture.root, 'settingsPanel')
                    self.assertFalse(settings.property('resetPending'))
                    self.assertEqual(fixture.js('backend.lastAction'), '')
                finally:
                    fixture.tearDown()


if __name__ == '__main__':
    unittest.main()
