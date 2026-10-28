"""Skin fonts: any licensed .ttf/.otf is allowed; a font without its licence file is refused."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import theme_core as theme


class FontLicenceTests(unittest.TestCase):
    def test_names(self):
        allowed = theme.allowed
        for name in ('departure-mono.otf', 'lora-italic.ttf', 'lora-license.txt', 'courier-prime-bold.ttf'):
            self.assertTrue(allowed('style/shell/assets/' + name), name)
        for name in ('Lora.ttf', 'font.woff2', 'run.sh', 'lora-italic.ttf.bak'):
            self.assertFalse(allowed('style/shell/assets/' + name), name)
        self.assertFalse(allowed('style/hyprlock/lora-italic.ttf'))

    def test_pairing(self):
        assets = 'style/shell/assets/'
        self.assertEqual(theme.unlicensed_fonts([assets + 'lora-italic.ttf', assets + 'lora-license.txt']), [])
        self.assertEqual(theme.unlicensed_fonts([assets + 'lorax.ttf', assets + 'lora-license.txt']), ['lorax.ttf'])
        self.assertEqual(theme.unlicensed_fonts([assets + 'marker.ttf']), ['marker.ttf'])

    def test_package_without_licence_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(ROOT / 'themes/deltarune', root / 'themes/deltarune')
            package = root / 'themes/deltarune'
            manifest = json.loads((package / 'manifest.json').read_text())
            manifest['files'] = [e for e in manifest['files'] if not e['target'].endswith('departure-mono-license.txt')]
            (package / 'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(theme.ThemeError, 'licence'):
                theme.Engine(root, root / 'style', root / 'state', root / 'hypr').load('deltarune')


if __name__ == '__main__':
    unittest.main()
