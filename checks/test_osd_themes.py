"""Run the existing real mouse/OSD contract in each staged skin; no device changes."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import theme_preview


class OsdThemeTests(unittest.TestCase):
    def test_each_skin_uses_live_drag_hover_and_centered_icons(self):
        for theme in ('plague-tale','deltarune'):
            with self.subTest(theme=theme),tempfile.TemporaryDirectory() as folder:
                root=Path(folder)
                theme_preview.stage(theme,root/'payload')
                (root/'checks').mkdir()
                script=root/'checks/test_shell_revisions.py'
                shutil.copy2(ROOT/'checks/test_shell_revisions.py',script)
                result=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,env=os.environ,timeout=30)
                self.assertEqual(result.returncode,0,theme+'\n'+result.stdout+result.stderr)


if __name__=='__main__':unittest.main()
