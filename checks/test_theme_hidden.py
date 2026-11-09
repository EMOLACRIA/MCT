"""Hidden themes stay in the repo and applicable, but leave the Super+G rail."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import theme_core
import theme_picker

HIDDEN = {'deltarune', 'deltarune-adventure', 'deltarune-guardian', 'deltarune-snowgrave', 'plague-tale'}


class HiddenThemes(unittest.TestCase):
    def ids(self, active=None):
        engine = theme_core.Engine(ROOT)
        record = {'id': active, 'version': '1'} if active else None
        with patch.object(engine, 'optional', side_effect=lambda name: record if name == 'active.json' else None):
            return [row['id'] for row in theme_picker.catalog(engine)['themes']]

    def test_rail_shows_only_visible_themes(self):
        self.assertEqual(theme_picker.hidden_ids(ROOT), HIDDEN)
        self.assertEqual(self.ids(), ['gravity-falls', 'little-prince', 'spider-punk'])

    def test_active_hidden_theme_stays_visible_and_loadable(self):
        self.assertIn('plague-tale', self.ids('plague-tale'))
        for name in HIDDEN:
            theme_core.Engine(ROOT).load(name)

    def test_bad_list_hides_nothing(self):
        import json, tempfile
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / 'theme-picker').mkdir()
            (Path(folder) / 'theme-picker/hidden.json').write_text('[1, 2')
            self.assertEqual(theme_picker.hidden_ids(Path(folder)), set())
            (Path(folder) / 'theme-picker/hidden.json').write_text(json.dumps({'hidden': ['ok-id', '../x', 3]}))
            self.assertEqual(theme_picker.hidden_ids(Path(folder)), {'ok-id'})


if __name__ == '__main__':
    unittest.main()
