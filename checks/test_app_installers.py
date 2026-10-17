import importlib.util,json,tempfile,shutil
from pathlib import Path
from unittest.mock import patch
from test_spotify_install import SUPPORTED,theme_output
p=Path(__file__).resolve().parents[1]/'apps/manage.py';spec=importlib.util.spec_from_file_location('apps',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as td:
 root=Path(td);m.HOME=root;m.CONFIG=root/'config';m.DATA=root/'data';m.STATE=root/'state';m.SPOTIFY=m.DATA/'desktop-style-apps/spotify'
 for d in [m.CONFIG,m.DATA,m.STATE]:d.mkdir()
 rc=m.CONFIG/'dolphinrc';original='# retained\n[General]\nRememberOpenedTabs=true\n[UiSettings]\nColorScheme=OldColors\n[Icons]\nTheme=OldIcons\n'
 rc.write_text(original)
 with patch.object(m,'closed'),patch.object(m.shutil,'which',side_effect=lambda n:'/fixture' if n in ['dolphin','qt6ct'] else None):
  m.dolphin(True);assert rc.read_text()==original
  m.dolphin();assert 'ColorScheme=DesktopStyle' in rc.read_text() and 'RememberOpenedTabs=true' in rc.read_text()
  first=(m.STATE/'dolphin.json').read_bytes();m.dolphin();assert (m.STATE/'dolphin.json').read_bytes()==first
  rc.write_text(rc.read_text()+'\n[Custom]\nValue=keep\n')
  m.dolphin(restore=True);assert 'ColorScheme=OldColors' in rc.read_text() and 'Theme=OldIcons' in rc.read_text() and 'Value=keep' in rc.read_text()
  assert not (m.DATA/'icons/DesktopStyle').exists()
 print('PASS: Dolphin preflight, apply, repeat keeps first backup, restore preserves unrelated new preferences')
 source=root/'package';(source/'Apps').mkdir(parents=True);(source/'spotify').write_text('binary-fixture');(source/'Apps/xpui.spa').write_text('archive-fixture')
 (m.CONFIG/'spotify').mkdir();(m.CONFIG/'spotify/prefs').write_text('app.last-launched-version="1.2.96.518"\n')
 launcher=m.DATA/'applications/spotify.desktop';launcher.parent.mkdir(exist_ok=True);launcher.write_text('[Desktop Entry]\nName=Spotify\nExec=spotify %U\n')
 baseline=launcher.read_bytes();calls=[]
 def fake_run(args,**kw):
  calls.append((args,kw));env=kw['env']
  assert env['SPICETIFY_CONFIG']==str(m.SPOTIFY/'config/spicetify') and env['XDG_STATE_HOME']==str(m.SPOTIFY/'state') and 'SPICETIFY_STATE' not in env
  config=(m.SPOTIFY/'config/spicetify/config-xpui.ini').read_text()
  assert 'inject_theme_js = 0' in config and str(m.SPOTIFY/'client') in config
  (m.SPOTIFY/'client/Apps/xpui.spa').write_text('themed fixture')
  theme_output(m.SPOTIFY/'client')
  return 'Spicetify fixture success'
 def which(name):return '/fixture/spicetify' if name=='spicetify' else None
 with patch.object(m,'closed'),patch.object(m,'spotify_source',return_value=source),patch.object(m,'spotify_versions',return_value=SUPPORTED),patch.object(m.shutil,'which',side_effect=which),patch.object(m,'run',side_effect=fake_run):
  m.spotify(True);assert launcher.read_bytes()==baseline and not m.SPOTIFY.exists()
  m.spotify();assert 'launch.sh' in launcher.read_text() and (source/'Apps/xpui.spa').read_text()=='archive-fixture'
  first=json.loads((m.STATE/'spotify.json').read_text())['backup'];m.spotify();assert json.loads((m.STATE/'spotify.json').read_text())['backup']==first
  saved=launcher.read_bytes();current=(m.SPOTIFY/'client/Apps/xpui.spa').read_bytes()
  with patch.object(m,'run',side_effect=RuntimeError('incompatible Spotify fixture')):
   try:m.spotify();raise AssertionError('must fail')
   except RuntimeError:pass
  assert launcher.read_bytes()==saved and (m.SPOTIFY/'client/Apps/xpui.spa').read_bytes()==current
  m.spotify(restore=True);assert launcher.read_bytes()==baseline and not m.SPOTIFY.exists()
 print('PASS: private Spotify client/config/state, source untouched, repeated apply, failed apply rollback and original launcher restore')
