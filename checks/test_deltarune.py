"""Run the existing interaction contract against a staged skin, plus the current panel/wallpaper revisions.

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


class DeltaruneRevisionTests(qt.PreferenceUiTests):
    def test_controls_right_launcher_left_and_center_preference_preserved(self):
        self.change('reduceMotion', True)
        self.change('centerPanels', False)
        for width,height in [(1600,1000),(900,600),(640,480)]:
            self.view.resize(width,height)
            for panel in ['launcher','controls']:
                self.js('uiState.close();uiState.toggle("'+panel+'","preview")')
                qt.QTest.qWait(20)
                frame=qt.visual_child(self.root,'activePanelFrame')
                expected=width-frame.width()-16 if panel=='controls' else 16
                self.assertAlmostEqual(frame.x(),expected)
                self.assertGreaterEqual(frame.x(),0)
                self.assertLessEqual(frame.x()+frame.width(),width)
        self.change('centerPanels', True)
        qt.QTest.qWait(20)
        self.assertAlmostEqual(frame.x(),(self.view.width()-frame.width())/2)

    def test_bottom_strip_removed_font_and_wallpaper_preserved(self):
        from PySide6.QtGui import QImage
        self.js('uiState.close();uiState.toggle("launcher","preview")')
        qt.QTest.qWait(30)
        self.assertIsNone(qt.visual_child(self.root,'partyStrip'))
        frame=qt.visual_child(self.root,'activePanelFrame')
        self.assertFalse(qt.evaluate(frame,'Theme.partyStripEnabled'))
        self.assertEqual(qt.evaluate(frame,'Theme.loadedFont.status'),1)
        self.assertIn('Departure',qt.evaluate(frame,'Theme.bodyFont'))
        source=QImage(str(ROOT/'themes/deltarune/wallpaper-source.jpeg'))
        wallpaper=QImage(str(qt.ROOT/'payload/style/wallpaper.png'))
        self.assertEqual((wallpaper.width(),wallpaper.height()),(1200,675))
        self.assertEqual(source.convertToFormat(QImage.Format_RGBA8888),wallpaper.convertToFormat(QImage.Format_RGBA8888))


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
        suite=unittest.TestSuite(DeltaruneRevisionTests(name) for name in [
            'test_controls_right_launcher_left_and_center_preference_preserved',
            'test_bottom_strip_removed_font_and_wallpaper_preserved'])
        result=unittest.TextTestRunner(verbosity=1).run(suite);passed=passed and result.wasSuccessful()
    return 0 if passed else 1


if __name__=='__main__':sys.exit(main())
