"""Exercise Qt network directory imports, as used by QuickShell's qs: loader.

QuickShell synthesizes a qmldir only when one does not already exist. Local
file: imports can discover unlisted siblings and therefore mask incomplete
manifests; a network URL requires every component to be registered.
"""
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['QT_QUICK_BACKEND'] = 'software'
sys.path.insert(0, str(Path('build/qs-qt-check').resolve()))
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlComponent, QQmlEngine

style = Path('build/desktop-style/payload/style').resolve()
shell = style / 'shell'
old_manifest = 'singleton Theme 1.0 Theme.qml\n'
registered = {line.split()[-1] for line in (shell / 'ui/qmldir').read_text().splitlines() if line.strip()}
assert registered == {p.name for p in (shell / 'ui').glob('*.qml')}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        parts = unquote(self.path.split('?', 1)[0]).strip('/').split('/')
        mode, relative = parts[0], '/'.join(parts[1:])
        path = (style / relative).resolve()
        if not path.is_relative_to(style):
            self.send_error(403)
            return
        if path == shell / 'FeedbackProbe.qml':
            data = b'import QtQuick\nimport "ui"\nFeedback { uiState: null }\n'
        elif path == shell / 'qmldir':
            # Same entries that QuickShell 0.3.1 scanDir() synthesizes.
            body = 'module qs\n' + ''.join(f'{p.stem} 1.0 {p.name}\n' for p in sorted(shell.glob('[A-Z]*.qml')))
            data = body.encode()
        elif path == shell / 'ui/qmldir' and mode == 'old':
            data = old_manifest.encode()
        elif path.is_file():
            data = path.read_bytes()
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
app = QGuiApplication([])
base = f'http://127.0.0.1:{server.server_port}'
engines = []
components = []
objects = []


def load(mode, done):
    engine = QQmlEngine()
    engines.append(engine)
    component = QQmlComponent(engine)
    components.append(component)
    handled = False

    def changed(status):
        nonlocal handled
        if status in (QQmlComponent.Ready, QQmlComponent.Error) and not handled:
            handled = True
            try:
                done(component)
            except Exception as exc:
                print('FAIL:', repr(exc), flush=True)
                app.exit(1)

    component.statusChanged.connect(changed)
    filename = 'FeedbackProbe.qml' if mode == 'old' else 'PreviewScene.qml'
    component.loadUrl(QUrl(f'{base}/{mode}/shell/{filename}'))
    changed(component.status())


def verify_old(component):
    errors = '\n'.join(e.toString() for e in component.errors())
    assert component.status() == QQmlComponent.Error, 'Old manifest must fail with network imports'
    assert 'Feedback is not a type' in errors, errors
    print('Reproduced original failure: Feedback is not a type', flush=True)
    load('fixed', verify_fixed)


def verify_fixed(component):
    errors = '\n'.join(e.toString() for e in component.errors())
    assert component.status() == QQmlComponent.Ready, errors
    scene = component.create()
    assert scene is not None, '\n'.join(e.toString() for e in component.errors())
    objects.append(scene)
    print('PASS: complete qmldir loads and instantiates the shared scene using network directory imports.', flush=True)
    app.quit()

QTimer.singleShot(0, lambda: load('old', verify_old))
QTimer.singleShot(15000, lambda: app.exit(2))
code = app.exec()
server.shutdown()
sys.exit(code)
