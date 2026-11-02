"""Hyprland gate: tested series only, parsed from real `hyprctl version` layouts."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import theme_core as theme


class HyprlandVersionTests(unittest.TestCase):
    def test_tested_series_pass_others_are_named(self):
        for text in ("Hyprland 0.56.2 built from branch v0.56.2 at commit abc",
                     "Hyprland 0.57.0 built from branch  at commit 1a2b (version: bump to 0.57.0).",
                     "Hyprland, built from branch main at commit 1a2b\nTag: v0.57.3, commits: 6100"):
            self.assertTrue(theme.hyprland_supported(text), text)
        for text, shown in (("Hyprland 0.56.1", "0.56.1"), ("Hyprland 0.58.0", "0.58.0"), ("", "unrecognised")):
            self.assertFalse(theme.hyprland_supported(text), text)
            self.assertIn(shown, theme.hyprland_requirement(text))


if __name__ == "__main__":
    unittest.main()
