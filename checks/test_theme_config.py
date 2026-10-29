"""Theme settings: validation, resolution on top of real packages, and a sandboxed apply."""
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "checks"))
import theme_core as theme
import test_theme_core as core

tc = theme.load_module(ROOT / "payload/style/scripts/theme_config.py")
QUOTES = theme.load_module(ROOT / "fastfetch_quotes.py").QUOTES
THEMES = sorted(p.name for p in (ROOT / "themes").iterdir() if (p / "manifest.json").is_file())


def png(width=4, height=3):
    from PIL import Image
    buffer = io.BytesIO()
    Image.new("RGB", (width, height), (10, 200, 30)).save(buffer, "PNG")
    return buffer.getvalue()


class Settings(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = {"HOME": self.temp.name}
        self.engine = theme.Engine(ROOT)

    def files(self, name):
        return self.engine.load(name)[1]

    def config(self, **theme_entry):
        value = tc.empty()
        if theme_entry:
            value["themes"]["little-prince"] = theme_entry
        return value

    def test_validation(self):
        tc.validate(tc.empty())
        for bad in ({"version": 2}, {"layout": {"themeOwn": False, "gapsIn": 99, "gapsOut": 1, "border": 1, "rounding": 1}},
                    {"themes": {"Bad Id": {}}}, {"themes": {"x": {"colors": {"accent": "red"}}}},
                    {"themes": {"x": {"colors": {"glow": "#ffffff"}}}}, {"themes": {"x": {"blur": True}}}):
            value = tc.empty(); value.update(bad)
            with self.assertRaises(tc.SettingsError, msg=str(bad)):
                tc.validate(value)
        for ok in (["TEND THE ROSE"], ["Gül, seçtiğin!", "(o tilki)"]):
            tc.check_quote(ok)
        for bad in ([], ["a", "b", "c"], ["x" * 19], ["$TIME"], ["<b>x</b>"], [" lead"], ["a&b"]):
            with self.assertRaises(tc.SettingsError, msg=str(bad)):
                tc.check_quote(bad)

    def test_storage_round_trip(self):
        value = self.config(colors={"accent": "#123456"})
        tc.write(value, self.env)
        self.assertEqual(tc.read(self.env), value)
        self.assertEqual(oct(tc.config_path(self.env).stat().st_mode & 0o777), "0o600")
        tc.config_path(self.env).write_text("{")
        with self.assertRaises(tc.SettingsError):
            tc.read(self.env)

    def test_every_theme_exposes_all_roles_and_empty_settings_change_nothing(self):
        for name in THEMES:
            files = self.files(name)
            approved = tc.defaults(files["style/shell/ui/Theme.qml"])
            self.assertEqual(set(approved), set(tc.ROLES), name)
            self.assertEqual(tc.resolve(name, files, tc.empty(), QUOTES.get(name), self.env), files, name)

    def test_colours_reach_shell_and_accent_reaches_apps(self):
        files = self.files("little-prince")
        out = tc.resolve("little-prince", files, self.config(colors={
            "accent": "#00aaff", "surface": "#99102030", "selection": "#445566", "text": "#ffffff"}), None, self.env)
        skin = out["style/shell/ui/Theme.qml"].decode()
        self.assertIn('brass:"#00aaff"', skin)
        self.assertIn("Qt.rgba(0.063,0.125,0.188,0.600*preferences.surfaceOpacity)", skin)
        self.assertIn('selectedSurface:"#445566"', skin)
        self.assertIn('activeWorkspaceSurface:"#445566"', skin)
        self.assertEqual(tc.defaults(skin)["accent"], "#00aaff")
        for key in ("hypr/appearance.lua", "style/kitty/theme.conf", "style/hyprlock/layout.conf"):
            self.assertNotIn("f2c35a", out[key].decode().lower(), key)
            self.assertIn("00aaff", out[key].decode().lower(), key)
        self.assertIn("rgba(00aaffff)", out["hypr/appearance.lua"].decode())
        # Untouched roles and other files keep the approved package bytes.
        self.assertIn('danger:"#ff8f7c"', skin)
        self.assertEqual(out["style/shell/ui/SurfaceLayout.qml"], files["style/shell/ui/SurfaceLayout.qml"])

    def test_surface_without_alpha_keeps_the_theme_translucency(self):
        out = tc.resolve("little-prince", self.files("little-prince"), self.config(colors={"surface": "#102030"}), None, self.env)
        self.assertIn("0.800*preferences.surfaceOpacity", out["style/shell/ui/Theme.qml"].decode())
        out = tc.resolve("plague-tale", self.files("plague-tale"), {**tc.empty(), "themes": {"plague-tale": {"colors": {"surface": "#102030"}}}}, None, self.env)
        self.assertIn("1.000*preferences.surfaceOpacity", out["style/shell/ui/Theme.qml"].decode())

    def test_layout_is_shared_and_optional(self):
        config = tc.empty()
        config["layout"].update(themeOwn=False, gapsIn=0, gapsOut=30, border=3, rounding=12)
        for name in ("plague-tale", "spider-punk"):
            files = self.files(name)
            text = tc.resolve(name, files, config, None, self.env)["hypr/appearance.lua"].decode()
            for line in ("gaps_in = 0", "gaps_out = 30", "border_size = 3", "rounding = 12"):
                self.assertIn(line, text, name)
            self.assertIn("blur = { enabled = false", text)
            self.assertEqual(tc.layout_defaults(files)["gapsOut"], 14)

    def test_wallpaper_targets(self):
        files = self.files("little-prince")
        tc.atomic(tc.wallpaper_path("little-prince", self.env), png(), 0o644)
        both = tc.resolve("little-prince", files, self.config(wallpaper={"desktop": True, "lock": True}), None, self.env)
        self.assertEqual(both["style/wallpaper.png"], png())
        self.assertEqual(both["style/shell/assets/wallpaper.png"], png())
        self.assertNotIn("style/hyprlock/lock-wallpaper.png", both)
        desktop = tc.resolve("little-prince", files, self.config(wallpaper={"desktop": True, "lock": False}), None, self.env)
        self.assertEqual(desktop["style/hyprlock/lock-wallpaper.png"], files["style/wallpaper.png"])
        self.assertIn("/hyprlock/lock-wallpaper.png", desktop["style/hyprlock/layout.conf"].decode())
        self.assertTrue(theme.allowed("style/hyprlock/lock-wallpaper.png"))
        lock = tc.resolve("little-prince", files, self.config(wallpaper={"desktop": False, "lock": True}), None, self.env)
        self.assertEqual(lock["style/wallpaper.png"], files["style/wallpaper.png"])
        self.assertEqual(lock["style/hyprlock/lock-wallpaper.png"], png())
        tc.wallpaper_path("little-prince", self.env).unlink()
        with self.assertRaisesRegex(tc.SettingsError, "missing"):
            tc.resolve("little-prince", files, self.config(wallpaper={"desktop": True, "lock": True}), None, self.env)

    def test_line_on_lock_screen_only_where_the_theme_has_one(self):
        files = self.files("little-prince")
        out = tc.resolve("little-prince", files, self.config(quote=["SEÇTİĞİN GÜLE", "BAK."]), QUOTES["little-prince"], self.env)
        self.assertIn("text = SEÇTİĞİN GÜLE BAK.", out["style/hyprlock/layout.conf"].decode())
        self.assertTrue(tc.lock_has_quote(files, QUOTES["little-prince"]))
        self.assertFalse(tc.lock_has_quote(self.files("plague-tale"), QUOTES["plague-tale"]))

    def test_import_wallpaper(self):
        source = Path(self.temp.name) / "pic.jpg"
        from PIL import Image
        Image.new("RGB", (40, 20), (1, 2, 3)).save(source, "JPEG")
        target = tc.import_wallpaper("little-prince", str(source), self.env)
        self.assertEqual(tc.png_size(target.read_bytes()), (40, 20))
        (Path(self.temp.name) / "text.png").write_text("not an image")
        with self.assertRaises(tc.SettingsError):
            tc.import_wallpaper("little-prince", str(Path(self.temp.name) / "text.png"), self.env)
        with self.assertRaises(tc.SettingsError):
            tc.png_size(png()[:-6])

    def test_quote_image_must_match_line_and_accent(self):
        from PIL import Image
        buffer = io.BytesIO(); Image.new("RGBA", tc.QUOTE_SIZE).save(buffer, "PNG"); data = buffer.getvalue()
        tc.atomic(tc.quote_image_path("little-prince", self.env), data)
        entry = {"quote": ["A"], "quoteImage": {"sha256": hashlib.sha256(data).hexdigest(), "lines": ["A"], "color": "#00aaff"}}
        self.assertEqual(tc.quote_image("little-prince", entry, "#00AAFF", self.env), data)
        self.assertIsNone(tc.quote_image("little-prince", entry, "#f2c35a", self.env))
        self.assertIsNone(tc.quote_image("little-prince", {**entry, "quote": ["B"]}, "#00aaff", self.env))

    def test_accent_reaches_dolphin_and_spotify_but_dolphin_text_stays_white(self):
        import configparser
        for name in THEMES:
            files = self.files(name)
            old = tc.rgb_of(tc.defaults(files["style/shell/ui/Theme.qml"])["accent"])
            base = ROOT / "apps" if name == "plague-tale" else ROOT / "themes" / name / "adapters"
            ini = (base / "spotify/color.ini").read_bytes()
            self.assertIn(b"010203", tc.swap_color(ini, old, "010203"), name)
            colors = tc.swap_color((base / "dolphin/DesktopStyle.colors").read_bytes(), old, "010203")
            self.assertIn(b"1,2,3", colors, name)
            palette = configparser.ConfigParser(interpolation=None); palette.read_string(colors.decode())
            for section in ("Colors:View", "Colors:Selection", "Colors:Window"):
                self.assertEqual(palette[section]["ForegroundNormal"].replace(" ", ""), "255,255,255", name)

    def test_helper_describe_and_save(self):
        env = {"HOME": self.temp.name}
        self.assertIn("Super+G", tc.describe(env)["error"])
        data = tc.state_dir(env) / "theme-core"
        data.mkdir(parents=True)
        (data / "source.json").write_text(json.dumps({"root": str(ROOT)}))
        files = self.files("little-prince")
        (data / "active.json").write_text(json.dumps({"id": "little-prince", "version": "0.1.0",
            "files": {k: hashlib.sha256(v).hexdigest() for k, v in files.items()}}))
        state = tc.describe(env)
        self.assertTrue(state["ok"], state["error"])
        self.assertEqual(state["active"]["name"], "Little Prince")
        self.assertEqual(state["defaults"]["colors"]["accent"], "#f2c35a")
        self.assertEqual(state["defaults"]["quote"], ["TEND THE ROSE", "YOU CHOSE."])
        self.assertTrue(state["lockQuote"]); self.assertTrue(state["applied"])
        config = tc.empty(); config["themes"]["little-prince"] = {"colors": {"accent": "#00aaff"}, "quote": ["ROSE"]}
        from PIL import Image
        buffer = io.BytesIO(); Image.new("RGBA", tc.QUOTE_SIZE).save(buffer, "PNG")
        tc.atomic(tc.quote_image_path("little-prince", env), buffer.getvalue())
        saved = tc.save(config, rendered=True, env=env)
        meta = saved["themes"]["little-prince"]["quoteImage"]
        self.assertEqual((meta["lines"], meta["color"]), (["ROSE"], "#00aaff"))
        self.assertIsNotNone(tc.quote_image("little-prince", saved["themes"]["little-prince"], "#00aaff", env))
        self.assertFalse(tc.describe(env)["applied"])
        config["themes"]["little-prince"] = {}
        self.assertEqual(tc.save(config, env=env)["themes"], {})


class SandboxApply(core.CoreTests):
    """Settings travel through the normal transaction: apply, change, rollback."""
    def settings(self, value):
        tc.write(value, self.engine.settings_env)

    def test_apply_with_settings_then_rollback(self):
        for name in ("payload/style/scripts/theme_config.py",):
            self.assertTrue((self.package / name).is_file())
        config = tc.empty()
        config["layout"].update(themeOwn=False, gapsIn=1, gapsOut=2, border=3, rounding=4)
        config["themes"]["little-prince"] = {"colors": {"accent": "#00aaff"}, "quote": ["HELLO", "ROSE."]}
        self.settings(config)
        self.engine.apply("little-prince")
        style = self.engine.style
        self.assertIn('brass:"#00aaff"', (style / "shell/ui/Theme.qml").read_text())
        self.assertIn("text = HELLO ROSE.", (style / "hyprlock/layout.conf").read_text())
        self.assertIn("gaps_out = 2", (self.engine.hypr / "appearance.lua").read_text())
        self.assertEqual(json.loads((self.engine.data / "source.json").read_text())["root"], str(self.package))
        # Same settings again: no new transaction. Changed settings: a new, reversible one.
        self.assertIsNone(self.engine.apply("little-prince"))
        config["themes"]["little-prince"]["colors"]["accent"] = "#ff00ff"
        self.settings(config)
        self.assertIsNotNone(self.engine.apply("little-prince"))
        self.assertIn('brass:"#ff00ff"', (style / "shell/ui/Theme.qml").read_text())
        self.engine.rollback()
        self.assertIn('brass:"#00aaff"', (style / "shell/ui/Theme.qml").read_text())

    def test_broken_settings_block_apply_without_changes(self):
        tc.config_path(self.engine.settings_env).parent.mkdir(parents=True, exist_ok=True)
        tc.config_path(self.engine.settings_env).write_text('{"version": 9}')
        (self.engine.state / "update.lock").touch()  # the lease file itself is expected
        before = self.state()
        with self.assertRaisesRegex(core.theme.ThemeError, "Theme settings"):
            self.engine.apply("little-prince")
        self.assertTrue(before == self.state(), "a refused apply changed files")


def load_tests(loader, tests, pattern):
    # SandboxApply reuses the core fixture; run only its own tests, not the inherited suite.
    suite = unittest.TestSuite(loader.loadTestsFromTestCase(Settings))
    for name in ("test_apply_with_settings_then_rollback", "test_broken_settings_block_apply_without_changes"):
        suite.addTest(SandboxApply(name))
    return suite


if __name__ == "__main__":
    unittest.main()
