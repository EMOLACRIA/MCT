"""Migrate only the known visual layout; preserve custom configuration and auth behavior."""
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import update


class LockLayoutTests(unittest.TestCase):
    def test_published_legacy_migrates_and_new_config_is_idempotent(self):
        style=str(update.m.STYLE)
        old=(ROOT/'legacy-hyprlock.conf').read_text().replace('@STYLE@',style)
        new=(ROOT/'payload/hypr/hyprlock.conf').read_text().replace('@STYLE@',style)
        self.assertEqual(update.lock_config(old),new)
        self.assertEqual(update.lock_config(new),new)
        self.assertEqual(new.count('ignore_empty_input = true'),1)

    def test_custom_visual_and_auth_configuration_are_preserved(self):
        custom='general {\n ignore_empty_input = true\n}\nauth {\n pam:enabled = true\n}\n# My custom clock\n'
        self.assertEqual(update.lock_config(custom),custom)

    def test_skin_changes_do_not_modify_password_behavior(self):
        def fields(text):
            body=re.search(r'input-field\s*\{([^}]+)\}',text).group(1)
            return dict(re.findall(r'^\s*([\w_]+)\s*=\s*(.*?)\s*$',body,re.M))
        baseline=fields((ROOT/'payload/style/hyprlock/layout.conf').read_text())
        for theme in ('plague-tale','deltarune'):
            text=(ROOT/'themes'/theme/'files/style/hyprlock/layout.conf').read_text()
            actual=fields(text)
            for key in ('dots_center','fade_on_empty','check_text','fail_text'):
                self.assertEqual(actual[key],baseline[key])
            self.assertNotRegex(text,r'(?m)^\s*(general|auth)\s*\{')
            self.assertEqual(re.findall(r'cmd\[[^\]]+\].*',text),re.findall(r'cmd\[[^\]]+\].*',(ROOT/'payload/style/hyprlock/layout.conf').read_text()))


if __name__=='__main__':unittest.main()
