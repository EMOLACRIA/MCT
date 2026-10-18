"""Run the existing interaction contract against a staged skin, plus its optional strip.

Qt offscreen only. Does not install, run QuickShell, or contact the user's session.
"""
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import theme_preview
import test_preferences_ui as qt


class PartyStripTests(qt.PreferenceUiTests):
    def setUp(self):
        super().setUp()
        self.js('uiState.close()')

    def test_live_values_missing_sensors_mute_and_charging(self):
        self.js('backend.hardware={};backend.audioAvailable=false;backend.battery=-1')
        qt.QTest.qWait(10)
        for index, value in enumerate(['TEMP —', 'OFFLINE', 'AC']):
            self.assertEqual(qt.visual_child(self.root, 'partyValue-'+str(index)).property('text'), value)
        self.js('backend.hardware={cpuTemp:0,cpuUsage:0};backend.audioAvailable=true;backend.muted=true;backend.battery=42;backend.batteryCharging=true')
        qt.QTest.qWait(10)
        for index, value in enumerate(['0°C', 'MUTED', '42% +']):
            self.assertEqual(qt.visual_child(self.root, 'partyValue-'+str(index)).property('text'), value)
        self.js('backend.hardware={cpuTemp:null};backend.batteryCharging=false;backend.muted=false;backend.volume=73')
        qt.QTest.qWait(10)
        for index, value in enumerate(['TEMP —', '73%', '42%']):
            self.assertEqual(qt.visual_child(self.root, 'partyValue-'+str(index)).property('text'), value)

    def test_party_buttons_toggle_existing_panels_and_font_loads(self):
        self.click('partyCell-0'); self.assertEqual(self.js('uiState.activePanel'), 'hardware')
        self.js('uiState.close()')
        self.click('partyCell-1'); self.assertEqual(self.js('uiState.activePanel'), 'controls')
        panel=self.root.findChild(qt.QObject,'activePanelFrame')
        self.assertEqual(qt.evaluate(panel,'Theme.loadedFont.status'),1)
        self.assertIn('Departure',qt.evaluate(panel,'Theme.bodyFont'))



def main():
    # Reuse the exact shared settings, calculator, tray, power and Alt+Tab tests.
    import test_shell_ui as surfaces
    import test_launcher_calculator as launcher
    import test_window_switcher as switcher
    modules=[qt,surfaces,launcher,switcher]
    passed=True
    with tempfile.TemporaryDirectory(prefix='mct-deltarune-test-') as tmp:
        theme_preview.stage('deltarune',Path(tmp)/'payload')
        for module in modules:module.ROOT=Path(tmp)
        for module in modules:
            qt.qInstallMessageHandler(lambda kind,context,message,m=module: (m.WARNINGS if hasattr(m,'WARNINGS') else qt.WARNINGS).append(message))
            suite=unittest.defaultTestLoader.loadTestsFromModule(module)
            result=unittest.TextTestRunner(verbosity=1).run(suite);passed=passed and result.wasSuccessful()
        qt.qInstallMessageHandler(lambda kind,context,message:qt.WARNINGS.append(message))
        # Load only new checks; inherited settings cases have already run above.
        suite=unittest.TestSuite(PartyStripTests(name) for name in [
            'test_live_values_missing_sensors_mute_and_charging',
            'test_party_buttons_toggle_existing_panels_and_font_loads'])
        result=unittest.TextTestRunner(verbosity=1).run(suite);passed=passed and result.wasSuccessful()
    return 0 if passed else 1


if __name__=='__main__':sys.exit(main())
