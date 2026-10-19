"""Photo catalog/transaction bridge; temporary roots and fake native runtime only."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import theme_picker as picker
import test_theme_core as core


class PickerTests(unittest.TestCase):
    def setUp(self):
        module_patch = patch.object(picker, 'theme_core', core.theme)
        module_patch.start(); self.addCleanup(module_patch.stop)
        self.fixture = core.CoreTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.engine = self.fixture.engine

    def test_catalog_is_readonly_and_isolates_invalid_package(self):
        before = self.fixture.state()
        reply = picker.dispatch(self.engine, 'catalog')
        self.assertTrue(reply['ok'])
        self.assertEqual({r['id'] for r in reply['catalog']['themes']}, {'plague-tale', 'deltarune', 'deltarune-snowgrave'})
        self.assertTrue(all(r['valid'] and r['preview'].startswith('file:///') for r in reply['catalog']['themes']))
        rows={row['id']:row for row in reply['catalog']['themes']}
        self.assertEqual(rows['deltarune-snowgrave']['accent'],'#d8b779')
        self.assertEqual(rows['deltarune']['accent'],'#f32baf')
        self.assertTrue(rows['deltarune-snowgrave']['fontSource'].endswith('.otf'))
        self.assertEqual(self.fixture.state(), before)
        self.assertEqual(self.fixture.runtime.events, [])
        (self.engine.root/'themes/deltarune/preview.png').write_bytes(b'broken')
        rows = {r['id']: r for r in picker.catalog(self.engine)['themes']}
        self.assertFalse(rows['deltarune']['valid'])
        self.assertEqual(rows['deltarune']['preview'], '')
        self.assertTrue(rows['plague-tale']['valid'])
        self.engine.data.mkdir()
        (self.engine.data/'active.json').write_text('{bad json')
        self.assertTrue(picker.catalog(self.engine)['stateError'])

    def test_check_apply_noop_and_restore_use_core_and_keep_preferences(self):
        before = self.fixture.state()
        result = picker.dispatch(self.engine, 'check', 'deltarune')
        self.assertTrue(result['ok'], result)
        self.assertEqual(self.fixture.state(), before)
        self.assertNotIn('stop', self.fixture.runtime.events)
        result = picker.dispatch(self.engine, 'apply', 'deltarune')
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['catalog']['active']['id'], 'deltarune')
        self.assertTrue(result['catalog']['canRollback'])
        events = self.fixture.runtime.events.count('stop')
        result = picker.dispatch(self.engine, 'apply', 'deltarune')
        self.assertTrue(result['ok'])
        self.assertEqual(self.fixture.runtime.events.count('stop'), events)
        result = picker.dispatch(self.engine, 'apply', 'plague-tale')
        self.assertTrue(result['ok'], result)
        result = picker.dispatch(self.engine, 'rollback')
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['catalog']['active']['id'], 'deltarune')

    def test_failed_apply_refreshes_actual_state_after_core_recovery(self):
        self.assertTrue(picker.dispatch(self.engine, 'apply', 'plague-tale')['ok'])
        self.fixture.runtime.fail['start'] = 1
        reply = picker.dispatch(self.engine, 'apply', 'deltarune')
        self.assertFalse(reply['ok'])
        self.assertIn('fixture start', reply['message'])
        self.assertEqual(reply['catalog']['active']['id'], 'plague-tale')
        self.assertFalse(reply['catalog']['pending'])
        # Reject a file changed by the user; the picker cannot bypass core ownership.
        edited = self.engine.style/'kitty/theme.conf'
        edited.write_text('# user edit\n')
        result = picker.dispatch(self.engine, 'apply', 'deltarune')
        self.assertFalse(result['ok'])
        self.assertEqual(edited.read_text(), '# user edit\n')
        self.assertFalse(picker.dispatch(self.engine, 'check', '../bad')['ok'])

    def test_menu_toggles_warm_overlay_and_only_launches_when_absent(self):
        with patch.object(picker.shutil, 'which', return_value='/fixture/quickshell'), patch.object(picker.subprocess, 'run') as ipc, patch.object(picker.subprocess, 'call', return_value=0) as launch:
            ipc.return_value.returncode = 0
            self.assertEqual(picker.menu(), 0)
            launch.assert_not_called()
            self.assertEqual(ipc.call_args.args[0][-3:], ['call','themes','toggle'])
            ipc.return_value.returncode = 1
            self.assertEqual(picker.menu(), 0)
            expected = ['/fixture/quickshell', '--daemonize', '--no-duplicate', '-p', str(picker.ROOT/'theme-picker/shell.qml')]
            self.assertEqual(launch.call_args.args[0], expected)
            session = core.theme.load_module(picker.ROOT/'payload/style/scripts/session.py')
            self.assertFalse(session.is_shell(expected))
            self.assertTrue(session.is_shell(['/fixture/quickshell','-p',session.SHELL]))
        self.assertEqual(self.fixture.runtime.events, [])


if __name__ == '__main__':
    unittest.main()
