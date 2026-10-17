"""Preference persistence/application helpers, isolated HOME and mocked process launch."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'payload/style/scripts'))
import preferences as prefs
import terminal
spec=importlib.util.spec_from_file_location('pref_file_manager',ROOT/'payload/style/scripts/file-manager.py')
files=importlib.util.module_from_spec(spec);spec.loader.exec_module(files)
sys.path.insert(0,str(ROOT));import update


class PreferenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.env={'HOME':self.tmp.name,'XDG_CONFIG_HOME':str(Path(self.tmp.name)/'config with spaces'),'XDG_DATA_HOME':str(Path(self.tmp.name)/'data'),'XDG_DATA_DIRS':str(Path(self.tmp.name)/'system'),'PATH':'/fixture/bin'}
        self.path=prefs.preference_path(self.env)
        self.which=patch.object(prefs.shutil,'which',side_effect=lambda key,path=None:'/fixture/'+key)
        self.which.start();self.addCleanup(self.which.stop)
    def save(self,**changes):
        value=prefs.read(self.env);value.update(changes);result=prefs.handle('save',value,self.env)
        self.assertTrue(result['ok'],result);return value

    def test_missing_preferences_use_defaults_without_writing(self):
        self.assertEqual(prefs.read(self.env),prefs.defaults());self.assertFalse(self.path.exists())
        self.assertTrue(prefs.handle('read',env=self.env)['ok']);self.assertFalse(self.path.exists())

    def test_atomic_roundtrip_private_mode_and_no_temporary_files(self):
        value=self.save(fontScale=1.2,barFloating=False,fileManager='thunar.desktop')
        self.assertEqual(prefs.read(self.env),value)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode),0o600)
        self.assertEqual(list(self.path.parent.glob('.preferences-*')),[])

    def test_missing_new_fields_merge_defaults_but_unknown_and_version_fail(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text(json.dumps({'version':1,'values':{'fontScale':1.1}}))
        self.assertEqual(prefs.read(self.env)['fontScale'],1.1)
        self.assertEqual(prefs.read(self.env)['osdPosition'],'bottom')
        for data in [{'version':2,'values':{}},{'version':True,'values':{}},{'version':1,'values':{'unknown':2}}]:
            self.path.write_text(json.dumps(data));self.assertFalse(prefs.handle('read',env=self.env)['ok'])

    def test_invalid_source_is_retained_until_explicit_reset(self):
        self.path.parent.mkdir(parents=True);self.path.write_bytes(b'{broken')
        packet=prefs.handle('read',env=self.env);self.assertFalse(packet['ok']);self.assertFalse(packet['sourceValid'])
        self.assertFalse(prefs.handle('save',prefs.defaults(),self.env)['ok']);self.assertEqual(self.path.read_bytes(),b'{broken')
        reset=prefs.handle('reset',env=self.env);self.assertTrue(reset['ok']);self.assertEqual(Path(reset['backup']).read_bytes(),b'{broken')
        self.assertEqual(prefs.read(self.env),prefs.defaults())

    def test_reset_retains_previous_valid_preferences(self):
        self.save(fontScale=1.1);before=self.path.read_bytes();result=prefs.handle('reset',env=self.env)
        self.assertEqual(Path(result['backup']).read_bytes(),before);self.assertEqual(prefs.read(self.env),prefs.defaults())

    def test_invalid_values_never_change_the_file(self):
        self.save();before=self.path.read_bytes()
        for key,value in [('fontScale',True),('fontScale',float('nan')),('fontScale',1.3),('surfaceOpacity',0.1),('reduceMotion',1),('terminal','kitty;echo bad'),('fileManager','../../bad.desktop'),('osdPosition','left')]:
            with self.subTest(key=key,value=value):
                candidate=prefs.defaults();candidate[key]=value
                self.assertFalse(prefs.handle('save',candidate,self.env)['ok']);self.assertEqual(self.path.read_bytes(),before)

    def test_unavailable_terminal_and_failed_write_preserve_previous_file(self):
        self.save();before=self.path.read_bytes()
        with patch.object(prefs.shutil,'which',return_value=None):self.assertFalse(prefs.handle('save',prefs.defaults(),self.env)['ok'])
        with patch.object(prefs.os,'replace',side_effect=OSError('read-only fixture')):self.assertFalse(prefs.handle('save',dict(prefs.defaults(),fontScale=1.1),self.env)['ok'])
        self.assertEqual(self.path.read_bytes(),before);self.assertEqual(list(self.path.parent.glob('.preferences-*')),[])

    def test_bad_file_keeps_core_application_shortcuts_usable(self):
        self.path.parent.mkdir(parents=True);self.path.write_text('{broken')
        with patch('sys.stderr'):
            self.assertEqual(terminal.launch_command([],env=self.env),['/fixture/kitty'])
            self.assertEqual(files.launch_command([],self.env),['/fixture/dolphin'])
        self.assertEqual(self.path.read_text(),'{broken')

    def test_xdg_path_relative_falls_back_to_home_config(self):
        self.env['XDG_CONFIG_HOME']='relative';self.assertEqual(prefs.preference_path(self.env),Path(self.tmp.name)/'.config/mct/preferences.json')

    def test_diagnostics_only_runs_read_only_version_commands(self):
        self.save();before=self.path.read_bytes()
        with patch.object(prefs.subprocess,'run',return_value=type('Result',(),{'stdout':'fixture v1\nmore','stderr':''})()) as run:
            packet=prefs.handle('diagnose',env=self.env)
        self.assertTrue(packet['ok']);self.assertIn('fixture v1',packet['diagnostics'])
        self.assertEqual([call.args[0] for call in run.call_args_list],[['hyprctl','version'],['quickshell','--version']])
        self.assertEqual(self.path.read_bytes(),before)

    def test_terminal_working_directory_and_arguments_stay_separate(self):
        arguments=['printf','hello; no shell','--literal']
        for key,flag,cwd_flag in [('kitty','--','--directory'),('alacritty','-e','--working-directory'),('foot','--','--working-directory')]:
            self.save(terminal=key)
            self.assertEqual(terminal.launch_command(arguments,'a folder',self.env),['/fixture/'+key,cwd_flag,'a folder',flag,*arguments])

    def test_selected_file_manager_uses_same_user_entry_as_launcher(self):
        self.save(fileManager='thunar.desktop')
        entry=Path(self.env['XDG_DATA_HOME'])/'applications/thunar.desktop';entry.parent.mkdir(parents=True);entry.write_text('[Desktop Entry]\nName=Thunar\nExec=custom %U\n')
        self.assertEqual(files.launch_command(['file with spaces','literal;data'],self.env),['/fixture/gio','launch',str(entry),'file with spaces','literal;data'])
        entry.unlink()
        with self.assertRaisesRegex(RuntimeError,'Selected file manager'):files.launch_command([],self.env)

    def test_nested_desktop_id_resolves_like_the_application_registry(self):
        self.save(fileManager='custom-files.desktop')
        entry=Path(self.env['XDG_DATA_HOME'])/'applications/custom/files.desktop';entry.parent.mkdir(parents=True);entry.write_text('[Desktop Entry]\nName=Files\nExec=custom %U\n')
        self.assertEqual(files.launch_command([],self.env),['/fixture/gio','launch',str(entry)])

    def test_terminal_migration_preserves_custom_commands_and_is_idempotent(self):
        base='local terminal = "kitty"\nhl.bind(mainMod .. " + Q", hl.dsp.exec_cmd(terminal))\n'
        patched=update.patch_terminal(base);self.assertIn('styleCommand("terminal.sh")',patched)
        self.assertEqual(update.patch_terminal(patched),patched)
        for text in [base.replace('"kitty"','"my-terminal --flag"'),base.replace('hl.dsp.exec_cmd(terminal)','hl.dsp.exec_cmd("custom")')]:self.assertEqual(update.patch_terminal(text),text)

    def test_preferences_survive_update_and_rollback_outside_theme_tree(self):
        sys.path.insert(0,str(ROOT/'checks'));import test_file_manager as fixtures
        fixture=fixtures.InstallationTests('test_update_preflight_is_read_only_then_update_and_rollback')
        fixture.setUp();self.addCleanup(fixture.doCleanups)
        env={'HOME':str(fixture.base),'XDG_CONFIG_HOME':str(fixture.base/'config'),'PATH':'/fixture/bin'}
        path=prefs.preference_path(env);prefs.atomic_write(path,dict(prefs.defaults(),fontScale=1.1));before=path.read_bytes()
        fixture.legacy_installation()
        with patch.object(fixtures.manager,'load_session',return_value=fixtures.Session()):
            fixtures.updater.update();self.assertEqual(path.read_bytes(),before)
            fixtures.updater.rollback();self.assertEqual(path.read_bytes(),before)


if __name__=='__main__':unittest.main()
