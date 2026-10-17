"""Offscreen responsive regressions; no installation, IPC or native session actions."""
import base64
import json
import os
from pathlib import Path
import unittest

import test_preferences_ui as qt


class ResponsiveUiTests(unittest.TestCase):
    def setUp(self):
        self.fixture=qt.PreferenceUiTests();self.fixture.setUp()
        self.view=self.fixture.view;self.root=self.fixture.root
        self.fixture.change('reduceMotion',True)
        self.js('uiState.close()')
    def tearDown(self):self.fixture.tearDown()
    def js(self,code):return self.fixture.js(code)
    def item(self,name):
        item=qt.visual_child(self.root,name);self.assertIsNotNone(item,name);return item
    def open(self,panel,width=900,height=600):
        self.view.resize(width,height)
        self.js('uiState.close();uiState.toggle('+json.dumps(panel)+',"preview")');qt.QTest.qWait(30)
    def rect(self,item,relative):
        p=item.mapToItem(relative,item.boundingRect().topLeft())
        return p.x(),p.y(),item.width(),item.height()
    def assert_inside(self,item,viewport):
        x,y,w,h=self.rect(item,viewport)
        self.assertGreaterEqual(x,-1);self.assertGreaterEqual(y,-1)
        self.assertLessEqual(x+w,viewport.width()+1);self.assertLessEqual(y+h,viewport.height()+1)
    def capture(self,name):
        image=self.view.grabWindow();self.assertFalse(image.isNull())
        if os.environ.get('MCT_UI_PREVIEW_DIR'):
            out=Path(os.environ['MCT_UI_PREVIEW_DIR']);out.mkdir(parents=True,exist_ok=True)
            self.assertTrue(image.save(str(out/(name+'.png'))))

    def test_all_panel_bounds_at_supported_font_extremes(self):
        for scale in [0.9,1.2]:
            self.fixture.change('fontScale',scale)
            for width,height in [(1600,1000),(900,600),(640,480)]:
                for panel in ['launcher','power','controls','notifications','media','hardware','settings']:
                    with self.subTest(scale=scale,size=(width,height),panel=panel):
                        self.open(panel,width,height)
                        self.assert_inside(self.item('activePanelFrame'),self.root)
                        self.assertFalse(self.view.grabWindow().isNull())
                        qt.QTest.keyClick(self.view,qt.Qt.Key_Escape)
                        self.assertEqual(self.js('uiState.activePanel'),'')

    def test_crowded_tray_does_not_overlap_clock_or_core_actions(self):
        svg=b'<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17"><circle cx="8" cy="8" r="6" fill="#b5a37c"/></svg>'
        icon='data:image/svg+xml;base64,'+base64.b64encode(svg).decode()
        for width,height in [(1600,1000),(1132,700),(1200,800),(900,600)]:
            self.view.resize(width,height)
            for scale in [0.9,1.2]:
                self.fixture.change('fontScale',scale)
                for count in [0,1,12,40]:
                    self.js('backend.trayItems='+json.dumps([dict(icon=icon,title='Application '+str(i)) for i in range(count)]))
                    qt.QTest.qWait(20)
                    clock=self.item('barClock');actions=self.item('barActions')
                    if count:
                        tray=self.item('barTray')
                        self.assertGreaterEqual(tray.x(),clock.x()+clock.width()+4)
                        self.assertLessEqual(tray.x()+tray.width(),actions.x()-4)
                        self.assertGreaterEqual(self.item('trayViewport').width(),24)
        self.capture('tray-900-font120')
        # Navigation exposes the last icon without taking its wheel event away.
        for _ in range(45):self.fixture.click('trayNext')
        viewport=self.item('trayViewport');last=self.item('trayIcon-39')
        self.assert_inside(last,viewport)
        qt.QTest.mouseClick(self.view,qt.Qt.RightButton,pos=last.mapToScene(last.boundingRect().center()).toPoint())
        self.assertEqual(self.js('backend.lastAction'),'Preview · Tray 39 · button 2')
        self.js('backend.trayItems=[]');qt.QTest.qWait(20)
        self.assertEqual(qt.evaluate(viewport,'contentX'),0)
        self.assertFalse(self.root.findChild(qt.QObject,'barTray').property('visible'))

    def test_many_players_remain_reachable_and_selectable(self):
        self.fixture.change('fontScale',1.2)
        self.js('backend.mediaTitle="A long title that fills both available lines in the media panel";backend.players='+json.dumps([
            dict(id=str(i),name=('A long player identity '*8)+str(i),selected=i==0) for i in range(8)]))
        self.open('media',640,480)
        scroll=self.item('mediaScroll');last=self.item('mediaPlayer-7')
        self.assertGreater(qt.evaluate(scroll,'contentHeight'),scroll.height())
        self.assertLessEqual(last.width(),scroll.width())
        # Focusing an offscreen player must scroll it into view for keyboard use.
        qt.evaluate(last,'forceActiveFocus()');qt.QTest.qWait(20)
        self.assert_inside(last,scroll)
        qt.QTest.keyClick(self.view,qt.Qt.Key_Space);qt.QTest.qWait(20)
        self.assertEqual(self.js('backend.lastAction'),'Preview · Player 7')
        self.capture('media-640-font120')

    def test_small_session_menu_keyboard_reveals_last_action_and_keeps_confirmation(self):
        self.fixture.change('fontScale',1.2);self.open('power',640,480)
        scroll=self.item('powerScroll')
        for _ in range(4):qt.QTest.keyClick(self.view,qt.Qt.Key_Down)
        qt.QTest.qWait(20)
        self.assert_inside(self.item('sessionAction-poweroff'),scroll)
        self.assertGreater(qt.evaluate(scroll,'contentY'),0)
        self.capture('power-640-font120')
        qt.QTest.keyClick(self.view,qt.Qt.Key_Return)
        self.assertEqual(self.js('uiState.confirmation'),'poweroff')
        self.assertEqual(self.js('backend.lastAction'),'')
        qt.QTest.qWait(20)
        self.assert_inside(self.item('confirmPower'),self.item('activePanelFrame'))
        qt.QTest.keyClick(self.view,qt.Qt.Key_Escape)
        self.assertEqual(self.js('backend.lastAction'),'')

    def test_normal_session_actions_fit_without_scrolling(self):
        for scale in [1,1.2]:
            self.fixture.change('fontScale',scale);self.open('power',1600,1000)
            scroll=self.item('powerScroll')
            self.assertLessEqual(qt.evaluate(scroll,'contentHeight'),scroll.height()+1)
            self.assert_inside(self.item('sessionAction-poweroff'),scroll)

    def test_long_notification_actions_stay_inside_card(self):
        self.fixture.change('fontScale',1.2)
        self.js('backend.history='+json.dumps([dict(key='long',app='Application '*20,title='Transfer complete',body='',time='17:40',
            actions=[dict(id='open',text='Open the destination in a very long file manager application name')])]))
        self.open('notifications',640,480)
        button=self.item('notificationAction-open');history=self.item('notificationHistory')
        self.assert_inside(button,history)
        self.assertLessEqual(button.width(),history.width()-28)
        self.capture('notifications-long-action')

    def test_empty_apps_players_and_notifications_render_without_stale_content(self):
        self.js('backend.players=[];backend.mediaTitle="";backend.mediaArtist="";backend.history=[];backend.applications=[];backend.trayItems=[]')
        for panel in ['launcher','media','notifications']:
            self.open(panel)
            self.assertFalse(self.view.grabWindow().isNull())
        self.assertEqual(self.item('notificationHistory').property('count'),0)

    def test_shared_headers_close_each_panel_and_keep_extra_actions(self):
        for panel in ['launcher','power','controls','notifications','media','hardware','settings']:
            self.open(panel)
            self.assertTrue(self.item('panelHeader').property('title'))
            self.fixture.click('closePanel')
            self.assertEqual(self.js('uiState.activePanel'),'')
        self.open('controls');self.fixture.click('openSettings')
        self.assertEqual(self.js('uiState.activePanel'),'settings')
        self.fixture.click('returnToControls')
        self.assertEqual(self.js('uiState.activePanel'),'controls')

    def test_preview_toast_uses_shared_actions_and_hides_behind_panels(self):
        self.fixture.change('fontScale',1.2);self.view.resize(900,600)
        self.js('backend.toasts='+json.dumps([dict(key='toast-fixture',app='Files',title='Transfer complete',body='Ready to open.',
            actions=[dict(id='open-toast',text='Open the destination in the file manager with a very long name')])]))
        qt.QTest.qWait(30)
        stack=self.item('toastStack');button=self.item('notificationAction-open-toast')
        self.assert_inside(stack,self.root);self.assert_inside(button,stack)
        self.fixture.click('notificationAction-open-toast')
        self.assertEqual(self.js('backend.lastAction'),'Preview · Notification toast-fixture · open-toast')
        self.capture('toast-shared-actions')
        self.open('notifications')
        self.assertFalse(stack.property('visible'))
        self.fixture.click('closePanel');qt.QTest.qWait(20)
        self.fixture.click('dismissToast-toast-fixture')
        self.assertFalse(stack.property('visible'))


if __name__=='__main__':unittest.main()
