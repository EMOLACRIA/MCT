"""Live-bind adapter fixtures; no actual Hyprland/QS/config writes."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import theme_bindings as bindings
import test_theme_core as core


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.fixture=core.CoreTests();self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups);self.addCleanup(self.fixture.tearDown)
        self.module_patch=patch.object(bindings,'theme_core',core.theme);self.module_patch.start();self.addCleanup(self.module_patch.stop)
        self.env=patch.dict(bindings.os.environ,{'HYPRLAND_INSTANCE_SIGNATURE':'fixture'});self.env.start();self.addCleanup(self.env.stop)
        self.uid=patch.object(bindings.os,'geteuid',return_value=1000);self.uid.start();self.addCleanup(self.uid.stop)
        self.qs=patch.object(bindings.shutil,'which',return_value='/fixture/qs');self.qs.start();self.addCleanup(self.qs.stop)
        self.manager=bindings.Installer(self.fixture.engine)
        # The core fixture's protected unrelated files must remain byte-identical.
        self.fixture.protected.pop(self.manager.path)
        self.original='-- user keys\nhl.bind("SUPER + Q", hl.dsp.exec_cmd("kitty"))\n'
        self.manager.path.write_text(self.original)
        self.custom=[];self.events=[];self.error_after_reload=False;self.registry_ref='42'
        self.run_patch=patch.object(self.manager,'run',side_effect=self.fake_run);self.run_patch.start();self.addCleanup(self.run_patch.stop)

    def row(self,arg=None,**values):
        return dict(modmask=64,key='g',keycode=0,dispatcher='__lua',arg=arg or self.registry_ref,description=bindings.DESCRIPTION,**values)

    def fake_run(self,args):
        self.events.append(args)
        if args==['hyprctl','version']:return 'Hyprland 0.56.2'
        if args==['hyprctl','configerrors']:
            return 'fixture invalid bind' if self.error_after_reload and bindings.BEGIN in self.manager.path.read_text() else ''
        if args==['hyprctl','-j','binds']:
            rows=self.custom[:]
            if bindings.BEGIN in self.manager.path.read_text():rows.append(self.row())
            return json.dumps(rows)
        return ''

    def test_readonly_check_idempotent_install_and_restore_keep_later_keys(self):
        self.manager.apply(check=True)
        self.assertEqual(self.manager.path.read_text(),self.original);self.assertFalse(self.manager.pointer.exists())
        self.manager.apply();record=json.loads(self.manager.pointer.read_text())
        backup=record['backup'];self.assertEqual(Path(backup).read_text(),self.original)
        self.registry_ref='84'  # Lua closure registry IDs change after reload.
        self.manager.apply();self.assertEqual(json.loads(self.manager.pointer.read_text())['backup'],backup)
        added='hl.bind("SUPER + Z", hl.dsp.exec_cmd("custom"))\n'
        self.manager.path.write_text(self.manager.path.read_text()+added)
        self.manager.apply(restore=True)
        self.assertIn(added,self.manager.path.read_text());self.assertIn(self.original,self.manager.path.read_text())
        self.assertNotIn(bindings.BEGIN,self.manager.path.read_text());self.assertFalse(self.manager.pointer.exists())

    def test_existing_super_g_or_keycode_is_never_overwritten(self):
        for row in [self.row(arg='custom'),dict(modmask=64,key='',keycode=42,dispatcher='exec',arg='custom')]:
            self.custom=[row]
            with self.assertRaisesRegex(core.theme.ThemeError,'occupied'):self.manager.apply()
            self.assertEqual(self.manager.path.read_text(),self.original);self.assertFalse(self.manager.pointer.exists())

    def test_reload_error_restores_current_keys_and_record(self):
        self.error_after_reload=True
        with self.assertRaisesRegex(core.theme.ThemeError,'rejected'):self.manager.apply()
        self.assertEqual(self.manager.path.read_text(),self.original);self.assertFalse(self.manager.pointer.exists())
        self.assertGreaterEqual(self.events.count(['hyprctl','reload']),2)

    def test_manual_block_edit_or_new_conflict_is_preserved(self):
        self.manager.apply()
        edited=self.manager.path.read_text().replace('SUPER + G','SUPER + H');self.manager.path.write_text(edited)
        with self.assertRaisesRegex(core.theme.ThemeError,'changed'):self.manager.apply()
        self.assertEqual(self.manager.path.read_text(),edited)
        self.manager.path.write_text(edited.replace('SUPER + H','SUPER + G'))
        self.custom=[self.row(arg='another owner')]
        with self.assertRaisesRegex(core.theme.ThemeError,'occupied'):self.manager.apply()
        self.assertIn(bindings.block(),self.manager.path.read_text())

    def test_unreadable_live_rows_do_not_claim_key_is_free(self):
        with patch.object(self.manager,'bindings',return_value=[dict(key='g',modmask='64')]):
            with self.assertRaisesRegex(core.theme.ThemeError,'Cannot verify'):self.manager.apply()
        self.assertEqual(self.manager.path.read_text(),self.original)


if __name__=='__main__':unittest.main()
