"""Check native QML bindings against the actual QuickShell v0.3.1 sources.

This supplements qmlcachegen syntax checks; it is a source-contract check,
not a substitute for loading the configuration in the user's native runtime.
"""
import os
import re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
src=Path(os.environ.get('MCT_QS_SOURCE',str(root/'tmp/qs-docs/quickshell-0.3.1')))/'src'
shell=root/'payload/style/shell'
assert src.is_dir(), 'Set MCT_QS_SOURCE to a QuickShell v0.3.1 source checkout.'

# Include real inherited base declarations and FileView's QML wrapper.
contracts={
 'GlobalShortcut':['wayland/hyprland/global_shortcuts/qml.hpp','core/reload.hpp'],
 'ScreencopyView':['wayland/screencopy/view.hpp'],
 'Variants':['core/variants.hpp','core/reload.hpp'],
 'PanelWindow':['window/panelinterface.hpp','window/windowinterface.hpp','core/types.hpp'],
 'PopupWindow':['window/popupwindow.hpp','window/windowinterface.hpp'],
 'Region':['core/region.hpp'],
 'ShellRoot':['core/shell.hpp','core/reload.hpp'],
 'FloatingWindow':['window/floatingwindow.hpp','window/windowinterface.hpp'],
 'Scope':['core/reload.hpp'],
 'IpcHandler':['io/ipchandler.hpp'],
 'Process':['io/process.hpp'],
 'StdioCollector':['io/datastream.hpp'],
 'FileView':['io/fileview.hpp','io/FileView.qml'],
 'PwObjectTracker':['services/pipewire/qml.hpp'],
 'NotificationServer':['services/notifications/qml.hpp'],
 'WlrLayershell':['wayland/wlr_layershell/wlr_layershell.hpp'],
}

def source_for(paths):
 return '\n'.join((src/p).read_text() for p in paths)

def properties(paths):
 text=source_for(paths)
 found=set(re.findall(r'Q_PROPERTY\(.*?\b(\w+)\s+(?:READ|MEMBER)\b',text))
 found.update(re.findall(r'\bproperty\s+(?:\w+\s+)(\w+)\s*:',text))
 return found

def handlers(paths):
 # Qt signals are declared as void methods; this check does not infer runtime behavior.
 return {'on'+n[0].upper()+n[1:] for n in re.findall(r'\bvoid\s+(\w+)\s*\(',source_for(paths))}

def flat_body(text,start):
 depth=1;pos=start;out=[]
 while pos<len(text):
  c=text[pos]
  if c in '\"\'':
   quote=c;out.append(' ');pos+=1
   while pos<len(text):
    if text[pos]=='\\':pos+=2;continue
    if text[pos]==quote:pos+=1;break
    pos+=1
   continue
  if text.startswith('//',pos):
   end=text.find('\n',pos)
   if end<0:break
   pos=end;continue
  if c=='{':depth+=1;out.append(' ')
  elif c=='}':
   depth-=1
   if depth==0:return ''.join(out)
   out.append(' ')
  else:out.append(c if depth==1 else ('\n' if c=='\n' else ' '))
  pos+=1
 raise AssertionError('Unbalanced object')

checked=[]

def inspect(text,filename):
 failures=[]
 for kind,paths in contracts.items():
  for match in re.finditer(r'\b'+kind+r'\s*\{',text):
   body=flat_body(text,match.end())
   names=set(re.findall(r'(?:^|[;\n])\s*([A-Za-z_][\w.]*)\s*:',body))
   names.update(re.findall(r'(?:^|[;\n])\s*(anchors|margins)\s+(?= )',body))
   custom=set(re.findall(r'\bproperty\s+\w+\s+(\w+)\s*:',body))
   allowed=properties(paths)|handlers(paths)|custom|{'on'+n[0].upper()+n[1:]+'Changed' for n in custom}|{'id','Component.onCompleted'}
   # PanelWindow's attached WlrLayershell properties belong to its own source.
   for name in names:
    if kind=='ScreencopyView' and name in {'anchors.centerIn','width','height'}:
     valid=True # inherited QtQuick.Item properties
    elif name.startswith('WlrLayershell.'):
     valid=name.split('.',1)[1] in properties(contracts['WlrLayershell'])
    elif kind=='PopupWindow' and name.startswith('anchor.'):
     parts=name.split('.')[1:]
     valid=parts[0] in properties(['core/popupanchor.hpp'])
     if len(parts)>1:valid=valid and parts[0]=='rect' and len(parts)==2 and parts[1] in properties(['core/types.hpp'])
    elif name.startswith(('anchors.','margins.')):
     group,leaf=name.split('.',1)
     valid=group in allowed and leaf in properties(paths)
    else:valid=name in allowed
    checked.append((filename,kind,name))
    if not valid:failures.append(f'{filename}: {kind}.{name} absent from source contract')
 return failures

text=(shell/'shell.qml').read_text()
assert 'model:Quickshell.screens' in text
negative=text.replace('model:Quickshell.screens','variants:Quickshell.screens',1)
failures=inspect(negative,'old-shell.qml')
assert any('Variants.variants absent' in f for f in failures),failures
print('Reproduced old Variants.variants mismatch against native header.',flush=True)
checked.clear()
for file in sorted(shell.rglob('*.qml')) + sorted((root/'theme-picker').glob('*.qml')):
 failures=inspect(file.read_text(),str(file.relative_to(root)))
 assert not failures,'\n'.join(failures)
print(f'PASS: {len(checked)} native property/handler bindings match QuickShell 0.3.1 source declarations.',flush=True)

menu_source=(src/'core/qsmenuanchor.cpp').read_text()
assert 'UseQApplication' in menu_source and 'QApplication' in menu_source
for entry in ['shell.qml','preview.qml','validate.qml']:
 assert (shell/entry).read_text().startswith('//@ pragma UseQApplication\n')
upower=(src/'services/upower/device.hpp').read_text()
assert 'Charging = 1' in upower and 'FullyCharged = 4' in upower
print('PASS: native tray menu QApplication requirement and battery state enum names')

clipboard=(src/'core/qmlglobal.hpp').read_text()
assert 'Q_PROPERTY(QString clipboardText READ clipboardText WRITE setClipboardText NOTIFY clipboardTextChanged)' in clipboard
clipboard_impl=(src/'core/qmlglobal.cpp').read_text()
assert 'void QuickshellGlobal::setClipboardText(const QString& text)' in clipboard_impl and '->setText(text)' in clipboard_impl
assert 'Quickshell.clipboardText=text' in (shell/'LiveContext.qml').read_text()
print('PASS: writable QuickShell clipboardText routes to Qt clipboard; native Wayland focus remains a target-session check')

entries=(src/'core/desktopentry.hpp').read_text()
assert 'Q_PROPERTY(QVector<QString> categories' in entries
assert 'Q_PROPERTY(QString id' in entries
print('PASS: native DesktopEntry categories/id declarations used by file-manager choices')

popup=(shell/'HintPopup.qml').read_text()
assert 'mask:Region {width:0;height:0}' in popup and 'grabFocus:false' in popup
proxy=(src/'window/proxywindow.cpp').read_text()
assert 'Qt::WindowTransparentForInput, this->mMask != nullptr && mask.isEmpty()' in proxy
assert 'this->bWantsGrab ? Qt::Popup : Qt::ToolTip' in (src/'window/popupwindow.cpp').read_text()
print('PASS: native hint empty mask maps to WindowTransparentForInput; grabFocus false selects ToolTip window flag')
