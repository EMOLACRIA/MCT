"""Run the same login interaction contract with both visual skins, without PAM."""
from pathlib import Path
import sys
import os
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import adapter_assets
import test_sddm_ui as greeter

passed = True
original = greeter.ROOT
preview_root=os.environ.get("MCT_GREETER_PREVIEW_DIR")
for theme in adapter_assets.THEMES:
    with tempfile.TemporaryDirectory() as folder:
        stage = Path(folder)/'sddm/theme'
        stage.parent.mkdir()
        adapter_assets.stage_greeter(theme, stage)
        greeter.ROOT = Path(folder)
        if preview_root:os.environ["MCT_GREETER_PREVIEW_DIR"]=str(Path(preview_root)/theme)
        result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromModule(greeter))
        passed = passed and result.wasSuccessful()
greeter.ROOT = original
sys.exit(0 if passed else 1)
