"""PT-002: portable installer/rollback checks; no Spotify, account or network access."""
import configparser
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('spotify_apps',ROOT/'apps/manage.py')
apps=importlib.util.module_from_spec(spec);spec.loader.exec_module(apps)
SUPPORTED={'spotify':'1:1.2.96.518-2','spicetify':'2.45.3'}


def theme_output(client):
    xpui=client/'Apps/xpui';xpui.mkdir(parents=True,exist_ok=True)
    (xpui/'xpui-modules.js').write_text('var __webpack_modules__={value:42};')
    (xpui/'xpui-snapshot.js').write_text('globalThis.value=__webpack_modules__.value;')
    (xpui/'index.html').write_text('<body><link rel="stylesheet" href="colors.css"><link rel="stylesheet" href="/user.css?cache=1"><script defer="defer" src="/xpui-snapshot.js"></script></body>')
    (xpui/'user.css').write_bytes((ROOT/'apps/spotify/user.css').read_bytes())
    palette=configparser.ConfigParser();palette.read(ROOT/'apps/spotify/color.ini')
    (xpui/'colors.css').write_text(':root {'+''.join('--spice-'+key+': #'+value+';' for key,value in palette['Ash'].items())+'}')
    (xpui/'spicetify-config.json').write_text(json.dumps({'theme_name':'DesktopStyle','scheme_name':'Ash'}))
    return xpui


class SpotifyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='spotify paths ');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for name in ['HOME','CONFIG','DATA','STATE']:
            path=self.root/name.lower();path.mkdir()
            context=patch.object(apps,name,path);context.start();self.addCleanup(context.stop)
        context=patch.object(apps,'SPOTIFY',apps.DATA/'desktop-style-apps/spotify');context.start();self.addCleanup(context.stop)
        prefs=apps.CONFIG/'spotify/prefs';prefs.parent.mkdir();prefs.write_text('private fixture; do not include in diagnostics')
        self.source=self.root/'system-client';(self.source/'Apps').mkdir(parents=True)
        (self.source/'spotify').write_text('stock executable fixture');(self.source/'Apps/xpui.spa').write_text('stock archive')
        self.normal=apps.DATA/'applications/spotify.desktop';self.normal.parent.mkdir()
        self.original='[Desktop Entry]\nName=Spotify\nExec=spotify --ozone-platform=wayland %U\n'
        self.normal.write_text(self.original)
        self.adblock=self.normal.with_name('spotify-adblock.desktop')
        self.adtext='[Desktop Entry]\nName=Spotify (adblock)\nExec=env LD_PRELOAD=/usr/lib/spotify-adblock.so spotify --uri=%U\n\n[Desktop Action Play]\nExec=env LD_PRELOAD=/usr/lib/spotify-adblock.so spotify --play\n'
        self.adblock.write_text(self.adtext)
        self.stack=contextlib.ExitStack();self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(apps,'closed'))
        self.stack.enter_context(patch.object(apps,'spotify_source',return_value=self.source))
        self.versions=self.stack.enter_context(patch.object(apps,'spotify_versions',return_value=SUPPORTED.copy()))
        self.stack.enter_context(patch.object(apps.shutil,'which',side_effect=lambda name:'/fixture/'+name if name=='spicetify' else None))
        self.stack.enter_context(patch.dict(os.environ,{'XDG_DATA_DIRS':str(self.root/'system')}))
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))

    def apply(self,args,**kwargs):
        self.assertEqual(args[1:],['backup','apply','--no-restart'])
        self.assertEqual(kwargs['env']['SPICETIFY_CONFIG'],str(apps.SPOTIFY/'config/spicetify'))
        self.assertNotIn('SPICETIFY_STATE',kwargs['env'])
        theme_output(apps.SPOTIFY/'client')
        return 'fixture backup and apply output'

    def test_linux_compatibility_bounds_and_unknown_cli(self):
        for version in ['1:1.2.14.0-1','1:1.2.96.518-2']:
            apps.check_spotify_compatibility({'spotify':version,'spicetify':'2.45.3'})
        for version in ['1.2.13.0','1.2.97.0','1:1.3.4.258-2']:
            with self.subTest(version=version),self.assertRaisesRegex(RuntimeError,'Linux Spotify support'):
                apps.check_spotify_compatibility({'spotify':version,'spicetify':'2.45.3'})
        with contextlib.redirect_stdout(io.StringIO()) as output:
            apps.check_spotify_compatibility({'spotify':'1.3.4.258','spicetify':'2.45.4'})
        self.assertIn('compatibility is not recorded',output.getvalue())

    def test_unsupported_pair_stops_check_and_apply_before_mutation(self):
        self.versions.return_value={'spotify':'1:1.3.4.258-2','spicetify':'2.45.3'}
        for check in [True,False]:
            with self.subTest(check=check),patch.object(apps,'first_backup') as backup,patch.object(apps,'run') as run:
                with self.assertRaisesRegex(RuntimeError,'1.2.96'):apps.spotify(check=check)
                backup.assert_not_called();run.assert_not_called()
                self.assertEqual(self.normal.read_text(),self.original)
                self.assertEqual(self.adblock.read_text(),self.adtext)
                self.assertFalse(apps.SPOTIFY.exists())
                self.assertFalse((apps.STATE/'spotify.json').exists())

    def test_supported_check_is_read_only(self):
        with patch.object(apps,'run') as run:apps.spotify(check=True)
        run.assert_not_called();self.assertFalse(apps.SPOTIFY.exists())
        self.assertEqual(self.adblock.read_text(),self.adtext)

    def test_apply_repeat_and_restore_preserve_adblock_and_original_backup(self):
        with patch.object(apps,'run',side_effect=self.apply):
            apps.spotify();first=json.loads((apps.STATE/'spotify.json').read_text())['backup']
            self.assertEqual(json.loads((apps.SPOTIFY/'versions.json').read_text()),SUPPORTED)
            self.assertEqual(self.adblock.read_text().count('LD_PRELOAD=/usr/lib/spotify-adblock.so'),2)
            self.assertIn('--uri=%U',self.adblock.read_text());self.assertIn('--play',self.adblock.read_text())
            self.assertIn('--ozone-platform=wayland %U',self.normal.read_text())
            tags=apps.ScriptTags();tags.feed((apps.SPOTIFY/'client/Apps/xpui/index.html').read_text())
            self.assertEqual(tags.sources,['/xpui-modules.js','/xpui-snapshot.js'])
            apps.spotify();self.assertEqual(json.loads((apps.STATE/'spotify.json').read_text())['backup'],first)
            self.assertEqual((self.source/'Apps/xpui.spa').read_text(),'stock archive')
            # Restoring an unsupported current package must not require Spicetify compatibility.
            self.versions.side_effect=AssertionError('version query during restore')
            apps.spotify(restore=True)
        self.assertEqual(self.normal.read_text(),self.original);self.assertEqual(self.adblock.read_text(),self.adtext)
        self.assertFalse(apps.SPOTIFY.exists())

    def test_success_exit_without_theme_files_rolls_back_fresh_install(self):
        def incomplete(args,**kwargs):
            xpui=theme_output(apps.SPOTIFY/'client');(xpui/'colors.css').unlink()
            return 'Preprocessing completed'
        with patch.object(apps,'run',side_effect=incomplete),self.assertRaisesRegex(RuntimeError,'colors.css'):
            apps.spotify()
        self.assertEqual(self.normal.read_text(),self.original);self.assertEqual(self.adblock.read_text(),self.adtext)
        self.assertFalse(apps.SPOTIFY.exists());self.assertFalse((apps.STATE/'spotify.json').exists())

    def test_incomplete_reapply_restores_previous_client_launchers_and_record(self):
        with patch.object(apps,'run',side_effect=self.apply):apps.spotify()
        paths=[apps.SPOTIFY/'client/Apps/xpui/user.css',apps.SPOTIFY/'versions.json',self.normal,self.adblock,apps.STATE/'spotify.json']
        before={path:path.read_bytes() for path in paths}
        def incomplete(args,**kwargs):
            xpui=theme_output(apps.SPOTIFY/'client');(xpui/'user.css').write_text('wrong theme')
            return 'zero exit status'
        with patch.object(apps,'run',side_effect=incomplete),self.assertRaisesRegex(RuntimeError,'requested user.css'):
            apps.spotify()
        self.assertEqual({path:path.read_bytes() for path in paths},before)
        self.assertFalse(apps.SPOTIFY.with_name('spotify.previous').exists())

    def test_validation_rejects_unlinked_css_wrong_palette_and_wrong_metadata(self):
        xpui=theme_output(apps.SPOTIFY/'client');apps.verify_spotify_theme(apps.SPOTIFY/'client')
        for file,bad,error in [('index.html','<body></body>','not linked'),('colors.css',':root {--spice-main:#ffffff;}','incorrect palette'),('spicetify-config.json','{"theme_name":"Other"}','metadata'),('spicetify-config.json','[]','metadata')]:
            with self.subTest(file=file):
                original=(xpui/file).read_bytes();(xpui/file).write_text(bad)
                with self.assertRaisesRegex(RuntimeError,error):apps.verify_spotify_theme(apps.SPOTIFY/'client')
                (xpui/file).write_bytes(original)

    def test_command_log_includes_stderr_in_order(self):
        # Real subprocess; harmless Python output in place of the upstream CLI.
        output=apps.run([sys.executable,'-c','import os; os.write(1,b"preprocess\\n"); os.write(2,b"applied styles\\n")'])
        self.assertEqual(output,'preprocess\napplied styles')

    def test_version_query_reads_package_and_cli_without_launching_spotify(self):
        with patch.object(apps.shutil,'which',return_value='/fixture/pacman'),patch.object(apps,'run',side_effect=['spotify 1:1.3.4.258-2','2.45.3']) as run:
            versions=REAL_VERSION_QUERY('/fixture/spicetify')
        self.assertEqual(versions,{'spotify':'1:1.3.4.258-2','spicetify':'2.45.3'})
        self.assertEqual([call.args[0] for call in run.call_args_list],[['/fixture/pacman','-Q','spotify'],['/fixture/spicetify','--version']])

    def test_diagnostics_are_read_only_and_do_not_include_preferences(self):
        theme_output(apps.SPOTIFY/'client')
        binary=self.root/'bin';binary.mkdir()
        for name,text in [('pacman','spotify 1:1.3.4.258-2'),('spicetify','2.45.3')]:
            path=binary/name;path.write_text('#!/bin/sh\nprintf "%s\\n" "'+text+'"\n');path.chmod(0o755)
        env={**os.environ,'HOME':str(apps.HOME),'XDG_CONFIG_HOME':str(apps.CONFIG),'XDG_DATA_HOME':str(apps.DATA),'XDG_STATE_HOME':str(apps.STATE),'PATH':str(binary)+os.pathsep+os.environ['PATH']}
        before={path:path.read_bytes() for path in self.root.rglob('*') if path.is_file()}
        result=subprocess.run(['bash',str(ROOT/'apps/diagnose.sh')],env=env,text=True,capture_output=True,check=True)
        self.assertIn('not recorded by the previous installer',result.stdout)
        self.assertIn('Linux Spotify support',result.stdout)
        self.assertIn('Theme files: verified',result.stdout)
        self.assertNotIn('private fixture',result.stdout)
        self.assertEqual({path:path.read_bytes() for path in self.root.rglob('*') if path.is_file()},before)


REAL_VERSION_QUERY=apps.spotify_versions
if __name__=='__main__':unittest.main()
