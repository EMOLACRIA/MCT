"""Real Qt greeter UI with fake SDDM models. Never authenticates or powers off."""
import os
from pathlib import Path
import unittest
import test_preferences_ui as qt
from PySide6.QtCore import QObject, QUrl, Qt
from PySide6.QtQml import QQmlComponent
from PySide6.QtQuick import QQuickView
from PySide6.QtTest import QTest

ROOT = Path(__file__).resolve().parents[1]


class GreeterTests(unittest.TestCase):
    def setUp(self):
        qt.WARNINGS.clear()
        self.view = QQuickView()
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.component = QQmlComponent(self.view.engine())
        self.component.setData(b'''import QtQuick
Item {
    property alias users: users
    property alias sessions: sessions
    property alias service: service
    QtObject { id: users; objectName: "users"; property string lastUser: "emo" }
    ListModel {
        id: sessions; objectName: "sessions"; property int lastIndex: 0
        ListElement { name: "Hyprland" }
        ListElement { name: "An unusually long alternative Wayland session name" }
    }
    QtObject {
        id: service
        objectName: "service"
        property bool canReboot: true
        property bool canPowerOff: true
        property var logins: []
        property int reboots: 0
        property int shutdowns: 0
        signal loginFailed()
        signal loginSucceeded()
        function login(user, password, session) { logins = logins.concat([[user, password, session]]) }
        function reboot() { reboots++ }
        function powerOff() { shutdowns++ }
    }
}''', QUrl('file:///GreeterFixture.qml'))
        self.assertEqual(self.component.status(), QQmlComponent.Ready, self.component.errors())
        self.fake = self.component.create()
        for name, prop in [('userModel', 'users'), ('sessionModel', 'sessions'), ('sddm', 'service')]:
            self.view.rootContext().setContextProperty(name, self.fake.findChild(QObject, prop))
        self.service = self.fake.findChild(QObject, 'service')
        self.view.setSource(QUrl.fromLocalFile(str(ROOT/'sddm/theme/Main.qml')))
        self.assertEqual(self.view.status(), QQuickView.Ready, self.view.errors())
        self.root = self.view.rootObject()
        self.view.resize(1600, 1000)
        self.view.show(); self.view.requestActivate(); QTest.qWait(100)

    def tearDown(self):
        self.view.setSource(QUrl()); self.fake.deleteLater()
        self.view.close(); self.view.deleteLater(); QTest.qWait(1)
        self.assertFalse(qt.WARNINGS, qt.WARNINGS)

    def field(self, name):
        obj = self.root.findChild(QObject, name)
        self.assertIsNotNone(obj, name)
        return obj

    def test_login_failure_retry_and_success_clear_password(self):
        password = self.field('password')
        self.assertTrue(password.hasActiveFocus())
        password.setProperty('text', 'secret')
        QTest.keyClick(self.view, Qt.Key_Return)
        qt.evaluate(self.root, 'login()')  # A second activation while busy is ignored.
        self.assertEqual(qt.evaluate(self.service, 'logins'), [['emo', 'secret', 0]])
        self.assertTrue(self.root.property('busy'))
        qt.evaluate(self.service, 'loginFailed()'); QTest.qWait(10)
        self.assertFalse(self.root.property('busy'))
        self.assertEqual(password.property('text'), '')
        self.assertTrue(password.hasActiveFocus())
        password.setProperty('text', 'retry')
        QTest.keyClick(self.view, Qt.Key_Return)
        qt.evaluate(self.service, 'loginSucceeded()')
        self.assertEqual(password.property('text'), '')

    def test_missing_user_or_session_never_attempts_login(self):
        self.field('username').setProperty('text', '  ')
        qt.evaluate(self.root, 'login()')
        self.assertEqual(qt.evaluate(self.service, 'logins'), [])
        self.field('username').setProperty('text', 'emo')
        qt.evaluate(self.fake, 'sessions.clear()'); QTest.qWait(10)
        qt.evaluate(self.root, 'login()')
        self.assertEqual(qt.evaluate(self.service, 'logins'), [])
        self.assertFalse(self.field('signIn').property('enabled'))

    def test_power_escape_cancels_without_action(self):
        qt.evaluate(self.field('restart'), 'clicked()'); QTest.qWait(20)
        self.assertTrue(self.field('powerConfirmation').property('visible'))
        QTest.keyClick(self.view, Qt.Key_Escape); QTest.qWait(150)
        self.assertFalse(self.field('powerConfirmation').property('visible'))
        self.assertEqual(self.service.property('reboots'), 0)
        self.assertEqual(self.service.property('shutdowns'), 0)

    def test_keyboard_focus_reveals_bottom_action_on_small_screen(self):
        self.view.resize(640, 480); QTest.qWait(30)
        button = self.field('powerOff')
        qt.evaluate(button, 'forceActiveFocus()'); QTest.qWait(30)
        scroll = self.field('loginScroll')
        point = button.mapToItem(scroll, button.boundingRect().topLeft())
        self.assertGreaterEqual(point.y(), 0)
        self.assertLessEqual(point.y()+button.height(), scroll.height())

    def test_card_and_clock_fit_small_screens_with_failure(self):
        for width, height in [(1600, 1000), (900, 600), (640, 480)]:
            self.view.resize(width, height)
            self.root.setProperty('failure', 'Sign in failed. Please try again.')
            QTest.qWait(50)
            card = self.field('loginCard')
            clock = self.field('loginClock')
            self.assertGreaterEqual(card.y(), 0, (width, height))
            self.assertLessEqual(card.y()+card.height(), height, (width, height))
            self.assertLessEqual(clock.y()+clock.height()+16, card.y(), (width, height))
            if os.environ.get('MCT_GREETER_PREVIEW_DIR'):
                dest = Path(os.environ['MCT_GREETER_PREVIEW_DIR']); dest.mkdir(parents=True, exist_ok=True)
                self.view.grabWindow().save(str(dest/f'greeter-{width}.png'))


if __name__ == '__main__': unittest.main()
