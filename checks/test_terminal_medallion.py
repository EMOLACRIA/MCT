"""Isolated Fastfetch install/variant/restore checks; no user config is touched."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('medallion', ROOT/'terminal-medallion/terminal.py')
medallion = importlib.util.module_from_spec(spec); spec.loader.exec_module(medallion)


class MedallionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.config = self.home/'config.jsonc'
        self.original = '// Keep my comment\n{"modules":["os",{"type":"cpu","key":"Chip"}], "display":{"separator":" → "},"logo":"auto",}\n'
        self.config.write_text(self.original)
        for name, value in [('STATE', self.home/'state'), ('ASSET', self.home/'data/medallion.txt')]:
            p = patch.object(medallion, name, value); p.start(); self.addCleanup(p.stop)
        for p in [patch.object(medallion.os, 'geteuid', return_value=1000),
                  patch.object(medallion.shutil, 'which', return_value='/fixture/fastfetch')]:
            p.start(); self.addCleanup(p.stop)
        self.args = argparse.Namespace(config=str(self.config), check=False, compact=False)

    def marker(self): return json.loads((medallion.STATE/'current.json').read_text())

    def test_variants_keep_modules_comments_and_first_backup_then_restore(self):
        medallion.install(self.args); first = self.marker()['backup']
        self.assertIn('// Keep my comment', self.config.read_text())
        self.assertEqual(medallion.parsed(self.config.read_text())['modules'], medallion.parsed(self.original)['modules'])
        self.args.compact = True; medallion.install(self.args)
        self.assertEqual(self.marker()['backup'], first)
        self.assertEqual(medallion.ASSET.read_bytes(), (medallion.PACKAGE/'medallion-compact.txt').read_bytes())
        medallion.restore(self.args)
        self.assertEqual(self.config.read_text(), self.original)
        self.assertFalse(medallion.ASSET.exists())
        self.assertTrue(Path(first).is_dir())

    def test_missing_modules_recovered_from_installed_fastfetch(self):
        self.config.write_text('{"logo":"auto"}')
        def generate(argv, **kwargs):
            self.assertEqual(argv[:2], ['fastfetch', '--gen-config'])
            Path(argv[2]).write_text('{"modules":["os","kernel","terminal"]}')
            return subprocess.CompletedProcess(argv, 0, '', '')
        with patch.object(medallion.subprocess, 'run', side_effect=generate): medallion.install(self.args)
        self.assertEqual(medallion.parsed(self.config.read_text())['modules'], ['os', 'kernel', 'terminal'])

    def test_file_symlink_target_untouched_and_link_restored(self):
        target = self.home/'original.jsonc'; self.config.rename(target)
        self.config.symlink_to(target)
        medallion.install(self.args)
        self.assertFalse(self.config.is_symlink())
        self.assertEqual(target.read_text(), self.original)
        medallion.restore(self.args)
        self.assertTrue(self.config.is_symlink())
        self.assertEqual(self.config.resolve(), target)

    def test_manual_edits_block_update_and_restore(self):
        medallion.install(self.args)
        self.config.write_text(self.config.read_text()+'// User edit\n')
        before = self.config.read_bytes()
        for operation in [medallion.install, medallion.restore]:
            with self.assertRaisesRegex(RuntimeError, 'changed after installation'): operation(self.args)
        self.assertEqual(self.config.read_bytes(), before)

    def test_failed_fresh_marker_write_restores_original(self):
        atomic = medallion.atomic
        def fail_marker(path, *args, **kwargs):
            if path == medallion.STATE/'current.json': raise OSError('fixture disk full')
            return atomic(path, *args, **kwargs)
        with patch.object(medallion, 'atomic', side_effect=fail_marker):
            with self.assertRaisesRegex(OSError, 'disk full'): medallion.install(self.args)
        self.assertEqual(self.config.read_text(), self.original)
        self.assertFalse(medallion.ASSET.exists())

    def test_cp437_roundtrip_dimensions_and_no_escape_controls(self):
        for name, width, height in [('medallion', 61, 29), ('medallion-compact', 39, 17)]:
            raw = (medallion.PACKAGE/(name+'.cp437')).read_bytes()
            text = (medallion.PACKAGE/(name+'.txt')).read_text().replace('$1', '')
            self.assertEqual(raw.decode('cp437').replace('\r\n', '\n'), text)
            self.assertEqual(len(text.splitlines()), height)
            self.assertEqual(max(map(len, text.splitlines())), width)
            self.assertNotIn('\x1b', text)


if __name__ == '__main__': unittest.main()
