"""Regression fixtures for palette initialization, launcher migration and bootstrap order."""
import importlib.util,json,os,subprocess,tempfile,sys,shutil
from pathlib import Path
from unittest.mock import patch
from test_spotify_install import SUPPORTED,theme_output
ROOT=Path(__file__).resolve().parents[1]
NODE=shutil.which('node');assert NODE,'Node.js is required for this bootstrap check.'
spec=importlib.util.spec_from_file_location('apps',ROOT/'apps/manage.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(prefix='apps23-') as td:
 root=Path(td);m.HOME=root;m.CONFIG=root/'config';m.DATA=root/'data';m.STATE=root/'state';m.SPOTIFY=m.DATA/'desktop-style-apps/spotify'
 for p in [m.CONFIG,m.DATA,m.STATE]:p.mkdir()
 # Upgrade a real-shaped 2.2.0 Dolphin record without moving the original restore point.
 rc=m.CONFIG/'dolphinrc';rc.write_text('[UiSettings]\nColorScheme=Before\n[Icons]\nTheme=breeze\n')
 original,new=m.first_backup('dolphin',m.app_paths()[:3]);original['keys']={'UiSettings':'Before','Icons':'breeze'}
 (m.STATE/'dolphin.json').write_text(json.dumps(original));rc.write_text('[UiSettings]\nColorScheme=DesktopStyle\n[Icons]\nTheme=DesktopStyle\n')
 qt=m.CONFIG/'qt6ct/qt6ct.conf';qt.parent.mkdir();qt.write_text('[Appearance]\nstyle=ExistingStyle\n[Fonts]\ngeneral=UserFont\n')
 with patch.object(m,'closed'),patch.object(m.shutil,'which',side_effect=lambda n:'/fixture' if n in ['dolphin','qt6ct'] else None):
  m.dolphin();record=json.loads((m.STATE/'dolphin.json').read_text());assert record['backup']==original['backup'] and len(record['files'])==6
  desktop=m.DATA/'applications/org.kde.dolphin.desktop';assert 'QT_QPA_PLATFORMTHEME=qt6ct' in desktop.read_text()
  qt.write_text(qt.read_text()+'\n[New]\nkeep=true\n')
  m.dolphin(restore=True);assert 'ColorScheme=Before' in rc.read_text();assert 'style=ExistingStyle' in qt.read_text() and 'keep=true' in qt.read_text();assert not desktop.exists()
 print('PASS: 2.2.0 Dolphin migration keeps original restore point and later preferences')
 # Multiple launchers, including upstream spotify-adblock syntax and desktop actions.
 source=root/'source';(source/'Apps').mkdir(parents=True);(source/'spotify').write_text('fixture');(source/'Apps/xpui.spa').write_text('stock')
 prefs=m.CONFIG/'spotify/prefs';prefs.parent.mkdir();prefs.write_text('fixture')
 applications=m.DATA/'applications';applications.mkdir(exist_ok=True)
 normal=applications/'spotify.desktop';normal.write_text('[Desktop Entry]\nName=Spotify\nExec=spotify --ozone-platform=wayland %U\n')
 adblock=applications/'spotify-adblock.desktop';adtext='[Desktop Entry]\nName=Spotify (adblock)\nExec=env LD_PRELOAD=/usr/lib/spotify-adblock.so spotify --foo %U\n\n[Desktop Action Play]\nExec=env LD_PRELOAD=/usr/lib/spotify-adblock.so spotify --play\n';adblock.write_text(adtext)
 def apply(args,**kwargs):
  theme_output(m.SPOTIFY/'client')
  return 'fixture'
 with patch.object(m,'closed'),patch.object(m,'spotify_source',return_value=source),patch.object(m,'spotify_versions',return_value=SUPPORTED),patch.object(m.shutil,'which',side_effect=lambda n:'/fixture' if n=='spicetify' else None),patch.object(m,'run',side_effect=apply),patch.dict(os.environ,{'XDG_DATA_DIRS':str(root/'system')}):
  m.spotify();assert adblock.read_text().count('LD_PRELOAD=/usr/lib/spotify-adblock.so')==2;assert '--foo %U' in adblock.read_text() and '--play' in adblock.read_text();assert 'launch.sh' in adblock.read_text()
  xpui=m.SPOTIFY/'client/Apps/xpui';tags=m.ScriptTags();tags.feed((xpui/'index.html').read_text());assert tags.sources==['/xpui-modules.js','/xpui-snapshot.js']
  node=NODE
  bad=subprocess.run([node,'-e',(xpui/'xpui-snapshot.js').read_text()],capture_output=True);assert bad.returncode
  good=subprocess.run([node,'-e','\n'.join((xpui/src.lstrip('/')).read_text() for src in tags.sources)],capture_output=True);assert good.returncode==0,good.stderr
  before=(xpui/'index.html').read_bytes();m.repair_spotify_bootstrap(m.SPOTIFY/'client');assert (xpui/'index.html').read_bytes()==before
  legacy=json.loads((m.STATE/'spotify.json').read_text());legacy.pop('launchers');legacy['files']=legacy['files'][:1];(m.STATE/'spotify.json').write_text(json.dumps(legacy));adblock.write_text(adtext)
  backup=legacy['backup'];m.spotify();assert json.loads((m.STATE/'spotify.json').read_text())['backup']==backup
  original_launcher=adblock.read_bytes()
  def broken(args,**kwargs):
   apply(args,**kwargs);(m.SPOTIFY/'client/Apps/xpui/xpui-snapshot.js').unlink();return 'fixture missing asset'
  with patch.object(m,'run',side_effect=broken):
   try:m.spotify();raise AssertionError('missing startup asset accepted')
   except RuntimeError as e:assert 'asset missing' in str(e)
  assert adblock.read_bytes()==original_launcher
  assert (m.SPOTIFY/'client/Apps/xpui/xpui-snapshot.js').is_file()
  m.spotify(restore=True);assert adblock.read_text()==adtext;assert '--ozone-platform=wayland' in normal.read_text()
 print('PASS: adblock env, arguments/actions, bootstrap JavaScript order/idempotence, failed-update rollback, original multi-launcher restore')
 # Parse exactly as qt6ct does, using real Qt QSettings + QPalette and a graphics view.
 if os.environ.get('MCT_QT_TEST_PATH'):sys.path.insert(0,os.environ['MCT_QT_TEST_PATH'])
 os.environ['QT_QPA_PLATFORM']='offscreen'
 from PySide6.QtCore import QSettings
 from PySide6.QtGui import QPalette,QColor
 from PySide6.QtWidgets import QApplication,QGraphicsScene,QGraphicsView,QGraphicsWidget
 app=QApplication.instance() or QApplication([])
 palfile=root/'palette.conf';palfile.write_text(m.qt_palette());settings=QSettings(str(palfile),QSettings.IniFormat);palette=QPalette()
 for name,group in [('active_colors',QPalette.Active),('inactive_colors',QPalette.Inactive),('disabled_colors',QPalette.Disabled)]:
  values=settings.value('ColorScheme/'+name);assert len(values)==QPalette.NColorRoles.value
  for i,color in enumerate(values):palette.setColor(group,QPalette.ColorRole(i),QColor(color))
 def luminance(c):
  values=[c.redF(),c.greenF(),c.blueF()];values=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values];return sum(v*w for v,w in zip(values,[.2126,.7152,.0722]))
 for group in [QPalette.Active,QPalette.Inactive,QPalette.Disabled]:
  for fg,bg in [(QPalette.Text,QPalette.Base),(QPalette.ButtonText,QPalette.Button),(QPalette.WindowText,QPalette.Window),(QPalette.HighlightedText,QPalette.Highlight)]:
   lights=sorted([luminance(palette.color(group,r)) for r in [fg,bg]]);contrast=(lights[1]+.05)/(lights[0]+.05);assert contrast>=(3 if group==QPalette.Disabled else 4.5),(group,fg,contrast)
 app.setPalette(palette);scene=QGraphicsScene();view=QGraphicsView(scene);widget=QGraphicsWidget();scene.addItem(widget)
 assert widget.palette().color(QPalette.Text).name()=='#ffffff';assert widget.palette().color(QPalette.Inactive,QPalette.Text).name()=='#ffffff'
 print('PASS: real Qt palette parsing, all text-role contrast pairs, active/inactive graphics item text initialization')
