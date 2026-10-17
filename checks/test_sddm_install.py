"""SDDM filesystem transactions in a temporary root. No services are started."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('greeter_install', ROOT/'sddm/manage.py')
greeter = importlib.util.module_from_spec(spec); spec.loader.exec_module(greeter)


class GreeterInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        paths = dict(CONFIG=self.root/'etc/sddm.conf', THEMES=self.root/'themes',
                     THEME=self.root/'themes/desktop-style', STATE=self.root/'state',
                     DISPLAY_MANAGER=self.root/'display-manager.service')
        for name, value in paths.items():
            p = patch.object(greeter, name, value); p.start(); self.addCleanup(p.stop)
        greeter.DISPLAY_MANAGER.symlink_to(self.root/'sddm.service')
        for p in [patch.object(greeter.os, 'geteuid', return_value=0),
                  patch.object(greeter.shutil, 'which', return_value='/fixture/sddm-greeter-qt6')]:
            p.start(); self.addCleanup(p.stop)
        p = patch.object(greeter.subprocess, 'run', side_effect=AssertionError('No real processes allowed'))
        p.start(); self.addCleanup(p.stop)

    def test_config_preserves_sections_comments_and_crlf(self):
        original = '[General]\r\nNumlock=on\r\n[Theme]\r\n# Keep\r\nCurrent=breeze\r\n[Users]\r\nRememberLastUser=true\r\n'
        result = greeter.theme_config(original)
        self.assertIn('[General]\r\nNumlock=on\r\n', result)
        self.assertIn('# Keep\r\nCurrent=desktop-style\r\n', result)
        self.assertIn('[Users]\r\nRememberLastUser=true\r\n', result)
        self.assertEqual(result, greeter.theme_config(result))

    def test_fresh_check_install_restore_no_original_files(self):
        greeter.install(True)
        self.assertFalse(greeter.STATE.exists())
        greeter.install()
        self.assertTrue((greeter.THEME/'Main.qml').is_file())
        greeter.restore()
        self.assertFalse(greeter.CONFIG.exists())
        self.assertFalse(greeter.THEME.exists())

    def test_symlink_config_and_existing_theme_restored_exactly(self):
        original = self.root/'original.conf'; original.write_text('# custom\n[Theme]\nCurrent=old\n')
        greeter.CONFIG.parent.mkdir(); greeter.CONFIG.symlink_to(original)
        greeter.THEME.mkdir(parents=True); (greeter.THEME/'custom').write_bytes(b'original theme')
        greeter.install()
        self.assertFalse(greeter.CONFIG.is_symlink())
        self.assertEqual(original.read_text(), '# custom\n[Theme]\nCurrent=old\n')
        greeter.restore()
        self.assertTrue(greeter.CONFIG.is_symlink())
        self.assertEqual((greeter.THEME/'custom').read_bytes(), b'original theme')

    def test_failed_config_write_rolls_back_theme_and_config(self):
        greeter.CONFIG.parent.mkdir(); greeter.CONFIG.write_text('[Theme]\nCurrent=old\n')
        greeter.THEME.mkdir(parents=True); (greeter.THEME/'custom').write_bytes(b'keep')
        atomic = greeter.atomic
        def fail_once(path, *args, **kwargs):
            if path == greeter.CONFIG and not hasattr(fail_once, 'failed'):
                fail_once.failed = True; raise OSError('fixture write failure')
            return atomic(path, *args, **kwargs)
        with patch.object(greeter, 'atomic', side_effect=fail_once):
            with self.assertRaisesRegex(OSError, 'write failure'): greeter.install()
        self.assertEqual(greeter.CONFIG.read_text(), '[Theme]\nCurrent=old\n')
        self.assertEqual((greeter.THEME/'custom').read_bytes(), b'keep')
        self.assertFalse((greeter.STATE/'current-backup').exists())


if __name__ == '__main__': unittest.main()
