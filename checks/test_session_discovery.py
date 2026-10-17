"""PT-005: exact shell selection without a user-specific path or real process signals."""
import importlib.util
import json
from pathlib import Path
import signal
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import manage
spec=importlib.util.spec_from_file_location('session_discovery',ROOT/'payload/style/scripts/session.py')
session=importlib.util.module_from_spec(spec);spec.loader.exec_module(session)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='another user ');self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name);self.state=self.home/'state';self.state.mkdir()
        for context in [patch.object(session.Path,'home',return_value=self.home),patch.object(session,'STATE',self.state),patch.dict(session.os.environ,{'XDG_CONFIG_HOME':str(self.home/'config')})]:
            context.start();self.addCleanup(context.stop)
        self.profile=self.home/'Programs/HyprCade/config/quickshell/HyprCade'

    def profile_file(self,path):
        path.mkdir(parents=True);(path/'shell.qml').write_text('fixture')

    def backup(self,commands):
        folder=self.state/'backups/original';folder.mkdir(parents=True)
        (folder/'manifest.json').write_text(json.dumps({'processes':commands}))
        (self.state/'current-backup').write_text(str(folder))

    def test_other_username_and_shell_qml_path(self):
        self.profile_file(self.profile)
        for path in [self.profile,self.profile/'shell.qml']:
            with self.subTest(path=path):self.assertTrue(session.is_legacy_shell(['qs','-p',str(path)]))

    def test_absent_conventional_profile_is_not_assumed(self):
        self.assertFalse(session.is_legacy_shell(['qs','-p',str(self.profile)]))
        self.assertFalse(session.is_legacy_shell(['qs','-p','/home/emo/Programs/HyprCade/config/quickshell/HyprCade']))

    def test_xdg_named_profile_and_link_to_moved_installation(self):
        moved=self.home/'elsewhere/custom-shell';self.profile_file(moved)
        profile=self.home/'config/quickshell/HyprCade';profile.parent.mkdir(parents=True);profile.symlink_to(moved)
        self.assertTrue(session.is_legacy_shell(['quickshell','--config','HyprCade']))
        self.assertTrue(session.is_legacy_shell(['quickshell','--path='+str(moved)]))
        self.assertTrue(session.is_legacy_shell(['quickshell','--path',str(profile)]))
        self.assertFalse(session.is_legacy_shell(['qs','--config','another-profile']))

    def test_exact_recorded_moved_profile_without_default_location(self):
        moved=self.home/'old custom location/shell'
        self.backup([['/usr/bin/qs','--path',str(moved)],['kitty'],['qs','ipc','-p',str(self.home/'not-legacy'),'call','desktop','ping']])
        self.assertTrue(session.is_legacy_shell(['quickshell','-p',str(moved)]))
        self.assertFalse(session.is_legacy_shell(['qs','-p',str(self.home/'not-legacy')]))
        self.assertFalse(session.is_legacy_shell(['qs','-p',str(moved)+'-preview']))

    def test_management_commands_are_never_shells(self):
        self.profile_file(self.profile)
        for target in [str(self.profile),session.SHELL,session.FEEDBACK]:
            for command in ['ipc','list','log','kill','msg']:
                for args in [['qs',command,'-p',target],['qs','-p',target,command]]:
                    with self.subTest(args=args):
                        self.assertFalse(session.managed(args))
                        self.assertFalse(session.is_shell(args))

    def test_unrelated_and_ambiguous_commands_are_not_managed(self):
        self.profile_file(self.profile)
        for args in [[],['kitty','-p',str(self.profile)],['qs','--path',str(self.profile.parent)],['qs','-p','relative'],['qs','-p'],['qs','-p',str(self.profile),'-c','another'],['qs','a-title',str(self.profile)]]:
            with self.subTest(args=args):self.assertFalse(session.managed(args))

    def test_own_shell_and_legacy_feedback_are_still_managed(self):
        self.assertTrue(session.is_shell(['qs','--path='+session.SHELL+'/shell.qml']))
        self.assertTrue(session.managed(['quickshell','-p',session.FEEDBACK]))
        self.assertFalse(session.managed(['qs','-p',session.SHELL+'-preview']))

    def test_missing_or_malformed_manifest_is_ignored(self):
        self.assertFalse(session.is_legacy_shell(['qs','-p',str(self.profile)]))
        self.backup([]);folder=Path((self.state/'current-backup').read_text())
        for text in ['{broken','[]','{"processes":null}','{"processes":[null,42,"qs",[]]}']:
            (folder/'manifest.json').write_text(text)
            self.assertFalse(session.is_legacy_shell(['qs','-p',str(self.profile)]))

    def test_stop_only_signals_verified_shells(self):
        self.profile_file(self.profile)
        legacy=['qs','-p',str(self.profile)]
        own=['quickshell','-p',session.SHELL]
        foreign=['quickshell','-p',str(self.home/'another-theme')]
        ipc=['quickshell','ipc','-p',session.SHELL,'call','desktop','ping']
        rows=[(10,legacy),(11,own),(12,foreign),(13,ipc)];killed=[]
        def kill(pid,sig):killed.append((pid,sig))
        def processes():return [row for row in rows if row[0] not in {pid for pid,_ in killed}]
        with patch.object(session,'processes',side_effect=processes),patch.object(session.os,'kill',side_effect=kill):
            stopped=session.stop_panel()
        self.assertEqual(stopped,[legacy,own]);self.assertEqual(killed,[(10,signal.SIGTERM),(11,signal.SIGTERM)])

    def test_restore_restarts_only_recorded_commands(self):
        class Adapter:
            def __init__(self):self.launched=[]
            def processes(self):return []
            def launch(self,args,log):self.launched.append(args)
        adapter=Adapter();commands=[['qs','-p','/recorded/old-shell']]
        manage.launch_original(adapter,{'processes':commands});self.assertEqual(adapter.launched,commands)
        adapter.launched=[];manage.launch_original(adapter,{})
        self.assertEqual(adapter.launched,[['hyprpaper']])


if __name__=='__main__':unittest.main()
