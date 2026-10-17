"""Portable regression checks for PT-001; stdlib only, no desktop session changes."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
from subprocess import CompletedProcess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import update as updater
manager = updater.m
spec = importlib.util.spec_from_file_location('file_manager', ROOT/'payload/style/scripts/file-manager.py')
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LaunchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='mct paths ')
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.env = {'HOME':str(self.home), 'XDG_DATA_HOME':str(self.home/'data'),
                    'XDG_DATA_DIRS':str(self.home/'system'), 'PATH':'/fixture/bin'}

    def entry(self, directory):
        path = directory/'applications/org.kde.dolphin.desktop'
        path.parent.mkdir(parents=True)
        path.write_text('[Desktop Entry]\nType=Application\nName=Dolphin\nExec=env QT_QPA_PLATFORMTHEME=qt6ct QT_STYLE_OVERRIDE=Fusion dolphin %U\n')
        return path

    def test_user_entry_wins_and_arguments_stay_separate(self):
        user = self.entry(self.home/'data')
        self.entry(self.home/'system')
        arguments = [str(self.home/'a folder'), 'sftp://example.invalid/share', 'literal;not-a-command']
        with patch.object(launcher.shutil, 'which', return_value='/fixture/gio'):
            self.assertEqual(launcher.launch_command(arguments,self.env), ['/fixture/gio','launch',str(user),*arguments])
        self.assertIn('QT_QPA_PLATFORMTHEME=qt6ct',user.read_text())

    def test_theme_restore_is_observed_on_next_launch(self):
        user = self.entry(self.home/'data'); system = self.entry(self.home/'system')
        with patch.object(launcher.shutil,'which',return_value='/fixture/gio'):
            self.assertEqual(launcher.launch_command([],self.env)[2],str(user))
            user.unlink()  # app restore removes its previously absent override
            self.assertEqual(launcher.launch_command([],self.env)[2],str(system))

    def test_no_entry_falls_back_to_installed_dolphin(self):
        with patch.object(launcher.shutil,'which',return_value='/fixture/dolphin') as which:
            self.assertEqual(launcher.launch_command(['folder'],self.env),['/fixture/dolphin','folder'])
        which.assert_called_once_with('dolphin',path='/fixture/bin')

    def test_configured_entry_without_gio_does_not_drop_theme(self):
        self.entry(self.home/'data')
        with patch.object(launcher.shutil,'which',return_value=None):
            with self.assertRaisesRegex(RuntimeError,'Missing gio'):
                launcher.launch_command([],self.env)

    def test_exec_failure_does_not_launch_plain_dolphin(self):
        with patch.object(launcher,'launch_command',return_value=['/fixture/gio','launch','entry']), patch.object(launcher.os,'execvpe',side_effect=OSError('fixture')) as execute, patch('sys.stderr'):
            self.assertEqual(launcher.main([]),1)
        execute.assert_called_once()

    def test_xdg_empty_or_relative_values_use_spec_defaults(self):
        env={'HOME':str(self.home),'XDG_DATA_HOME':'relative','XDG_DATA_DIRS':':relative:/absolute::'}
        self.assertEqual(list(launcher.data_directories(env)),[self.home/'.local/share',Path('/absolute')])


class BindingTests(unittest.TestCase):
    def baseline(self,command='"dolphin"'):
        source=(ROOT/'payload/hypr/keybinds.lua').read_text()
        return source.replace('local fileManager = styleCommand("file-manager.sh")','local fileManager = '+command)+'\n-- user setting kept\n'

    def test_stock_and_published_manual_fix_migrate_idempotently(self):
        for command in ['"dolphin"','"env QT_QPA_PLATFORMTHEME=qt6ct QT_STYLE_OVERRIDE=Fusion dolphin"']:
            with self.subTest(command=command):
                result=updater.patch_bindings(self.baseline(command))
                self.assertIn('local fileManager = styleCommand("file-manager.sh")',result)
                self.assertTrue(result.endswith('-- user setting kept\n'))
                self.assertEqual(updater.patch_bindings(result),result)

    def test_custom_file_manager_or_binding_is_preserved(self):
        source=self.baseline('"thunar --new-window"')
        self.assertEqual(updater.patch_file_manager(source),source)
        source=self.baseline().replace('hl.dsp.exec_cmd(fileManager))','hl.dsp.exec_cmd("my-files"))')
        self.assertEqual(updater.patch_file_manager(source),source)

    def test_duplicate_declaration_is_not_guessed(self):
        source=self.baseline()+'local fileManager = "dolphin"\n'
        self.assertEqual(updater.patch_file_manager(source),source)


class Session:
    OLD_SHELL='old-shell'
    def __init__(self,fail=False):
        self.original=[['quickshell','-p',self.OLD_SHELL]]
        self.commands=self.original.copy();self.fail=fail;self.ready=False
    def processes(self):return [(100+i,args) for i,args in enumerate(self.commands)]
    def managed(self,args,wallpaper=False):return args[0]=='quickshell'
    def read_services(self):return {}
    def suppress_services(self,record):pass
    def restore_services(self,record):pass
    def stop_panel(self):self.commands=[];self.ready=False
    stop_ui=stop_panel
    def launch(self,args,log):self.commands.append(args)
    def start(self):
        if self.fail:raise RuntimeError('simulated startup failure')
        self.commands.append(['quickshell','-p','new-shell']);self.ready=True
    def feedback_ready(self):return self.ready


def run_stub(args):
    output='Hyprland 0.56.2' if args==['hyprctl','version'] else ''
    return CompletedProcess(args,0,output,'')


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        for name,value in [('BASE',self.base),('STYLE',self.base/'config/desktop-style'),('STATE',self.base/'state'),('HYPR',self.base/'config/hypr')]:
            p=patch.object(manager,name,value);p.start();self.addCleanup(p.stop)
        for p in [patch.object(os,'geteuid',return_value=1000),patch.dict(os.environ,{'HYPRLAND_INSTANCE_SIGNATURE':'fixture'}),patch.object(manager.shutil,'which',return_value='/fixture'),patch.object(manager,'run',side_effect=run_stub),patch.object(manager,'check_quickshell'),patch.object(manager.time,'sleep')]:
            p.start();self.addCleanup(p.stop)
        manager.HYPR.mkdir(parents=True)
        self.keybinds=BindingTests().baseline().replace((ROOT/"switcher-bindings.lua").read_text().strip(),"")
        (manager.HYPR/'keybinds.lua').write_text(self.keybinds)
        (manager.HYPR/'hyprlock.conf').write_text('general {\n hide_cursor = true\n}\n')
        (manager.HYPR/'monitors.lua').write_text('user monitor settings\n')

    def legacy_installation(self):
        (manager.STYLE/'scripts').mkdir(parents=True)
        (manager.STYLE/'scripts/original.sh').write_text('original')
        (manager.STYLE/'wofi').mkdir();(manager.STYLE/'wofi/config').write_text('xoffset=30\nyoffset=30\n')
        original=manager.STATE/'backups/original';original.mkdir(parents=True)
        (original/'manifest.json').write_text('{"status":"installed","files":[]}')
        pointer=manager.STATE/'current-backup';pointer.write_text(str(original))
        return pointer

    def test_update_preflight_is_read_only_then_update_and_rollback(self):
        pointer=self.legacy_installation();original=pointer.read_bytes();session=Session()
        with patch.object(manager,'load_session',return_value=session):
            updater.update(True)
            self.assertEqual((manager.HYPR/'keybinds.lua').read_text(),self.keybinds)
            self.assertFalse((manager.STYLE/'scripts/file-manager.sh').exists())
            updater.update()
            self.assertTrue((manager.STYLE/'scripts/file-manager.py').is_file())
            self.assertTrue((manager.STYLE/'scripts/file-manager.sh').stat().st_mode&0o111)
            self.assertIn('styleCommand("file-manager.sh")',(manager.HYPR/'keybinds.lua').read_text())
            self.assertIn('desktop-style:window-next',(manager.HYPR/'keybinds.lua').read_text())
            self.assertEqual((manager.STYLE/'wofi/config').read_text(),'xoffset=30\nyoffset=30\n')
            updater.rollback()
        self.assertEqual((manager.HYPR/'keybinds.lua').read_text(),self.keybinds)
        self.assertFalse((manager.STYLE/'scripts/file-manager.sh').exists())
        self.assertEqual(pointer.read_bytes(),original)
        self.assertEqual((manager.HYPR/'monitors.lua').read_text(),'user monitor settings\n')

    def test_failed_update_restores_binding_and_original_backup(self):
        pointer=self.legacy_installation();original=pointer.read_bytes();session=Session(fail=True)
        with patch.object(manager,'load_session',return_value=session):
            with self.assertRaisesRegex(RuntimeError,'simulated startup failure'):updater.update()
        self.assertEqual((manager.HYPR/'keybinds.lua').read_text(),self.keybinds)
        self.assertFalse((manager.STYLE/'scripts/file-manager.sh').exists())
        self.assertEqual(pointer.read_bytes(),original)
        self.assertEqual(session.commands,session.original)

    def test_fresh_install_and_full_restore(self):
        original={p.name:p.read_bytes() for p in manager.HYPR.iterdir()}
        kitty=self.base/'.config/kitty/kitty.conf';kitty.parent.mkdir(parents=True);kitty.write_text('font_size 11\n')
        session=Session()
        with patch.object(manager,'check'),patch.object(manager,'load_session',return_value=session):
            manager.install()
            self.assertTrue((manager.STYLE/'scripts/file-manager.py').is_file())
            self.assertIn('styleCommand("file-manager.sh")',(manager.HYPR/'keybinds.lua').read_text())
            self.assertIn('desktop-style:window-next',(manager.HYPR/'keybinds.lua').read_text())
            manager.restore()
        self.assertFalse(manager.STYLE.exists())
        self.assertEqual(kitty.read_text(),'font_size 11\n')
        for name,content in original.items():self.assertEqual((manager.HYPR/name).read_bytes(),content)


if __name__=='__main__':unittest.main()
