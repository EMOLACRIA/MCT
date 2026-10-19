"""Theme-aware adapters use temporary homes and mocked clients/greeters only."""
import configparser
import contextlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import adapter_assets as assets
import test_spotify_install as spotify
import test_terminal_medallion as terminal
import test_sddm_install as greeter


class ThemeAdapterTests(unittest.TestCase):
    def test_active_selection_and_invalid_state(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'XDG_STATE_HOME':folder}):
            self.assertEqual(assets.selected(), 'plague-tale')
            p=Path(folder)/'desktop-style/theme-core/active.json';p.parent.mkdir(parents=True)
            p.write_text('{"id":"deltarune"}')
            self.assertEqual(assets.selected(), 'deltarune')
            self.assertEqual(assets.selected('plague-tale'), 'plague-tale')
            p.write_text('{"id":"deltarune-snowgrave"}')
            self.assertEqual(assets.selected(),'deltarune-snowgrave')
            p.write_text('{"id":"unknown"}')
            with self.assertRaises(ValueError):assets.selected()
            with self.assertRaises(ValueError):assets.source('../bad','spotify')

    def test_dolphin_switch_and_restore_keep_white_text_and_original_backup(self):
        app=spotify.apps
        with tempfile.TemporaryDirectory() as folder, contextlib.ExitStack() as stack:
            root=Path(folder)
            for name in ('CONFIG','DATA','STATE'):
                path=root/name;path.mkdir();stack.enter_context(patch.object(app,name,path))
            stack.enter_context(patch.object(app,'closed'))
            stack.enter_context(patch.object(app.shutil,'which',side_effect=lambda n:'/fixture' if n in ('dolphin','qt6ct') else None))
            stack.enter_context(patch.dict(os.environ,{'XDG_DATA_DIRS':str(root/'system')}))
            original='[UiSettings]\nColorScheme=Original\n[Other]\nKeep=true\n'
            (app.CONFIG/'dolphinrc').write_text(original)
            original_icon=app.DATA/'icons/DesktopStyle/scalable/places/folder.svg'
            original_icon.parent.mkdir(parents=True)
            original_icon.write_text('<svg><!-- original user icon --></svg>')
            first=None
            for theme in ('plague-tale','deltarune','deltarune-snowgrave','plague-tale'):
                with patch.object(app,'SELECTED_THEME',theme):app.dolphin()
                record=json.loads((app.STATE/'dolphin.json').read_text())
                first=first or record['backup'];self.assertEqual(record['backup'],first)
                self.assertEqual(record['theme'],theme)
                self.assertIn('#ffffff', (app.DATA/'color-schemes/DesktopStyle-Qt.conf').read_text())
                palette=configparser.ConfigParser();palette.read(app.DATA/'color-schemes/DesktopStyle.colors')
                for section in ('Colors:View','Colors:Selection','Colors:Window'):
                    self.assertEqual(palette[section]['ForegroundNormal'],'255,255,255')
                source=assets.source(theme,'dolphin')
                for path in (source/'icons').rglob('*'):
                    if path.is_file():
                        self.assertEqual((app.DATA/'icons/DesktopStyle'/path.relative_to(source/'icons')).read_bytes(),path.read_bytes())
                if theme=='deltarune':
                    self.assertNotEqual(original_icon.read_bytes(),(assets.source('plague-tale','dolphin')/'icons/scalable/places/folder.svg').read_bytes())
                self.assertIn('QT_QPA_PLATFORMTHEME=qt6ct',(app.DATA/'applications/org.kde.dolphin.desktop').read_text())
            app.dolphin(restore=True)
            self.assertIn('ColorScheme=Original',(app.CONFIG/'dolphinrc').read_text())
            self.assertIn('Keep=true',(app.CONFIG/'dolphinrc').read_text())
            self.assertEqual(original_icon.read_text(),'<svg><!-- original user icon --></svg>')

    def test_spotify_switch_preserves_adblock_private_client_and_first_backup(self):
        fixture=spotify.SpotifyTests();fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        app=spotify.apps
        def apply(args,**kwargs):
            fixture.apply(args,**kwargs)
            xpui=app.SPOTIFY/'client/Apps/xpui'
            (xpui/'user.css').write_bytes((app.theme_source('spotify')/'user.css').read_bytes())
            palette=configparser.ConfigParser();palette.read(app.theme_source('spotify')/'color.ini')
            (xpui/'colors.css').write_text(':root {'+''.join('--spice-'+k+': #'+v+';' for k,v in palette['Ash'].items())+'}')
            return 'mock apply'
        first=None
        for theme in ('plague-tale','deltarune','deltarune-snowgrave','plague-tale'):
            with patch.object(app,'SELECTED_THEME',theme),patch.object(app,'run',side_effect=apply):
                app.spotify();app.verify_spotify_theme(app.SPOTIFY/'client')
            record=json.loads((app.STATE/'spotify.json').read_text())
            first=first or record['backup'];self.assertEqual(record['backup'],first)
            self.assertEqual(record['theme'],theme)
            self.assertIn('LD_PRELOAD=/usr/lib/spotify-adblock.so',fixture.adblock.read_text())
            self.assertEqual((fixture.source/'Apps/xpui.spa').read_text(),'stock archive')
        app.spotify(restore=True)
        self.assertEqual(fixture.adblock.read_text(),fixture.adtext)

    def test_terminal_switch_retains_modules_and_cp437_roundtrip(self):
        fixture=terminal.MedallionTests();fixture.setUp();self.addCleanup(fixture.doCleanups)
        m=terminal.medallion;first=None
        for theme in ('plague-tale','deltarune','deltarune-snowgrave','plague-tale'):
            fixture.args.theme=theme;m.install(fixture.args)
            first=first or fixture.marker()['backup'];self.assertEqual(fixture.marker()['backup'],first)
            self.assertEqual(m.parsed(fixture.config.read_text())['modules'],m.parsed(fixture.original)['modules'])
        m.restore(fixture.args);self.assertEqual(fixture.config.read_text(),fixture.original)
        for theme in ('deltarune','deltarune-snowgrave'):
          for name in ('medallion','medallion-compact'):
            base=assets.source(theme,'terminal')
            text=(base/(name+'.txt')).read_text().replace('$1','')
            self.assertEqual((base/(name+'.cp437')).read_bytes().decode('cp437').replace('\r\n','\n'),text)
            self.assertNotIn('\x1b',text)

    def test_deltarune_greeter_uses_common_login_controller_and_restores(self):
        fixture=greeter.GreeterInstallTests();fixture.setUp();self.addCleanup(fixture.doCleanups)
        m=greeter.greeter
        for theme,accent in [('deltarune','#f32baf'),('deltarune-snowgrave','#d8b779')]:
          with tempfile.TemporaryDirectory() as folder:
            source=assets.stage_greeter(theme,Path(folder)/'theme')
            self.assertEqual((source/'Main.qml').read_bytes(),(ROOT/'sddm/theme/Main.qml').read_bytes())
            with patch.object(m,'THEME_SOURCE',source):m.install()
            self.assertIn(accent,(m.THEME/'LoginSkin.qml').read_text())
            self.assertTrue((m.THEME/'departure-mono.otf').is_file())
            m.restore();self.assertFalse(m.CONFIG.exists())


if __name__ == '__main__':unittest.main()
