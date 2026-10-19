"""Filesystem/transaction tests use temporary roots and a fake runtime only."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("theme_core", ROOT / "theme_core.py")
theme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(theme)


class Runtime:
    def __init__(self):
        self.events = []
        self.fail = {}

    def call(self, name):
        self.events.append(name)
        if self.fail.get(name, 0):
            self.fail[name] -= 1
            raise theme.ThemeError("fixture " + name)

    def preflight(self): self.call("preflight")
    def prepare_recovery(self): self.call("recover-preflight")
    def validate(self, style, appearance):
        self.call("validate")
        assert (style / "shell/ui/Theme.qml").is_file()
        assert appearance.is_file()
    def stop(self): self.call("stop")
    def start(self): self.call("start")
    def reload(self): self.call("reload")
    def snapshot(self): return {"fixture": {"path": "/original.png", "fit": "contain"}}
    def restore(self, snapshot):
        assert snapshot == {"fixture": {"path": "/original.png", "fit": "contain"}}
        self.call("reload")


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.package = self.base / "source"
        shutil.copytree(ROOT / "themes", self.package / "themes")
        self.runtime = Runtime()
        self.engine = theme.Engine(self.package, self.base / "config/desktop-style",
                                  self.base / "state/desktop-style", self.base / "config/hypr", self.runtime)
        self.engine.state.mkdir(parents=True)
        (self.engine.state / "current-backup").write_text("/original-backup")
        self.engine.hypr.mkdir(parents=True)
        (self.engine.hypr/"hyprlock.conf").write_text("source = "+str(self.engine.style/"hyprlock/layout.conf")+"\n")
        self.protected = {
            self.base / "config/mct/preferences.json": b'{"schema":1,"fontScale":1.2}',
            self.engine.state / "notifications.json": b'{"history":["keep"]}',
            self.engine.hypr / "keybinds.lua": b"-- my bindings",
            self.engine.hypr / "monitors.lua": b"-- my monitor and GPU settings",
            self.engine.hypr / "hyprpaper.conf": b"wallpaper {\n monitor =\n fit_mode = contain\n}\n",
            self.base / "original-backup": b"keep original backup",
        }
        for path, data in self.protected.items():
            path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        manifest = theme.read_json(ROOT / "themes/plague-tale/manifest.json")
        for entry in manifest["files"]:
            name = entry["target"]
            data = (ROOT / "payload" / name).read_bytes()
            source = self.package / "payload" / name
            source.parent.mkdir(parents=True, exist_ok=True); source.write_bytes(data)
            path = self.engine.path(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data.replace(b"@STYLE@", str(self.engine.style).encode()))
        for destination in (self.package/'payload/style/shell',self.engine.style/'shell'):
            shutil.copytree(ROOT/'payload/style/shell',destination,dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__','*.pyc'))

    def tearDown(self):
        for path, data in self.protected.items():
            self.assertEqual(path.read_bytes(), data, str(path))

    def state(self):
        return {str(p.relative_to(self.base)): p.read_bytes() for p in self.base.rglob("*")
                if p.is_file() and not p.is_symlink()}

    def variant(self):
        folder = self.package / "themes/fixture-variant"
        shutil.copytree(self.package / "themes/plague-tale", folder)
        manifest = theme.read_json(folder / "manifest.json")
        manifest["id"] = "fixture-variant"; manifest["name"] = "Fixture"
        for entry in manifest["files"]:
            if entry["target"] == "style/shell/ui/Theme.qml":
                path = folder / entry["source"]
                data = path.read_bytes().replace(b"#b5a37c", b"#aa9966")
                path.write_bytes(data); entry["gitBlob"] = theme.git_blob(data)
        (folder / "manifest.json").write_bytes(theme.json_bytes(manifest))
        return folder, manifest

    def test_builtin_package_integrity_and_screenshot(self):
        manifest, output = self.engine.load("plague-tale")
        self.assertEqual(set(manifest["surfaces"]), theme.SURFACES)
        self.assertGreater(len(output), 30)
        for entry in manifest["files"]:
            self.assertEqual((self.package / "themes/plague-tale" / entry["source"]).read_bytes(),
                             (ROOT / "payload" / entry["target"]).read_bytes(), entry["target"])
        self.assertIn(str(self.engine.style).encode(), output["style/hyprlock/media.conf"])
        self.assertNotIn(b"@STYLE@", output["style/hyprlock/media.conf"])

    def test_check_is_readonly_and_does_not_stop_or_start(self):
        before = self.state()
        self.assertEqual(self.engine.check("plague-tale")["id"], "plague-tale")
        self.assertEqual(before, self.state())
        self.assertEqual(self.runtime.events, ["preflight", "validate"])

    def test_shared_interaction_template_is_protected_from_theme_mutation(self):
        path=self.engine.style/'shell/surfaces/LauncherSurface.qml'
        path.write_text(path.read_text()+'\n// edited interaction\n')
        before=self.state()
        with self.assertRaisesRegex(theme.ThemeError,'Shared shell ABI differs'):
            self.engine.check('deltarune')
        self.assertEqual(before,self.state())
        self.assertFalse(theme.allowed('style/shell/surfaces/LauncherSurface.qml'))

    def test_custom_lock_config_requires_explicit_visual_adaptation(self):
        path=self.engine.hypr/'hyprlock.conf'
        path.write_text('general {\n ignore_empty_input = true\n}\n# My custom layout\n')
        before=self.state()
        with self.assertRaisesRegex(theme.ThemeError,'Hyprlock layout source'):
            self.engine.check('deltarune')
        self.assertEqual(before,self.state())
        self.assertFalse(self.runtime.events)
        path.write_text("  source  =  "+str(self.engine.style/'hyprlock/layout.conf')+"  # visual source\n")
        self.engine.check('deltarune')

    def test_deltarune_apply_switch_back_and_rollback_restore_theme_only_assets(self):
        self.engine.apply("deltarune")
        portrait = self.engine.style / "shell/assets/kris.png"
        font = self.engine.style / "shell/assets/departure-mono.otf"
        self.assertTrue(portrait.is_file()); self.assertTrue(font.is_file())
        first = self.engine.optional("active.json")
        self.engine.apply("plague-tale")
        self.assertFalse(portrait.exists()); self.assertFalse(font.exists())
        self.engine.rollback()
        self.assertTrue(portrait.is_file()); self.assertTrue(font.is_file())
        self.assertEqual(self.engine.optional("active.json"), first)
        self.engine.rollback()
        self.assertFalse(portrait.exists()); self.assertFalse(font.exists())

    def test_third_theme_cycle_noop_and_rollback_preserve_shared_state(self):
        states={}
        for name in ('deltarune','plague-tale','deltarune-snowgrave'):
            self.engine.apply(name)
            states[name]=self.engine.optional('active.json')
        before=self.state();events=list(self.runtime.events)
        self.assertIsNone(self.engine.apply('deltarune-snowgrave'))
        self.assertEqual(self.state(),before)
        # Mandatory validation still runs on noop; only the desktop restart is skipped.
        self.assertEqual(self.runtime.events[len(events):],['preflight','validate'])
        self.engine.rollback()
        self.assertEqual(self.engine.optional('active.json'),states['plague-tale'])
        self.engine.rollback()
        self.assertEqual(self.engine.optional('active.json'),states['deltarune'])

    def test_apply_variant_and_chained_rollback_preserve_original_backup(self):
        self.engine.apply("plague-tale")
        first = self.engine.pointer()
        original = self.engine.optional("active.json")
        self.variant(); self.engine.apply("fixture-variant")
        self.assertEqual(self.engine.optional("active.json")["id"], "fixture-variant")
        before = self.state(); self.engine.rollback(True)
        self.assertEqual(before, self.state())
        self.engine.rollback()
        self.assertEqual(self.engine.optional("active.json"), original)
        self.assertEqual(self.engine.pointer(), first)
        self.engine.rollback()
        self.assertIsNone(self.engine.optional("active.json"))
        self.assertIsNone(self.engine.pointer())

    def test_original_file_mode_is_restored(self):
        file = self.engine.style / "kitty/theme.conf"
        file.chmod(0o600)
        self.engine.apply("plague-tale"); self.engine.rollback()
        self.assertEqual(stat.S_IMODE(file.stat().st_mode), 0o600)

    def test_failed_validation_changes_no_installed_files(self):
        self.runtime.fail["validate"] = 1
        before = self.state()
        with self.assertRaisesRegex(theme.ThemeError, "validate"): self.engine.check("plague-tale")
        self.assertEqual(before, self.state())
        self.assertNotIn("stop", self.runtime.events)

    def test_reload_and_readiness_failures_automatically_restore(self):
        for failure in ("reload", "start"):
            with self.subTest(failure=failure):
                self.runtime.fail[failure] = 1
                before = {e["target"]: self.engine.path(e["target"]).read_bytes()
                          for e in theme.read_json(self.package / "themes/plague-tale/manifest.json")["files"]}
                with self.assertRaisesRegex(theme.ThemeError, "previous state restored"):
                    self.engine.apply("plague-tale")
                self.assertIsNone(self.engine.optional("active.json"))
                self.assertIsNone(self.engine.optional("pending.json"))
                for name, data in before.items(): self.assertEqual(self.engine.path(name).read_bytes(), data)

    def test_manual_edits_block_first_adoption_apply_and_rollback(self):
        file = self.engine.style / "shell/ui/Theme.qml"
        saved = file.read_bytes()
        file.write_bytes(saved + b"\n// my edits")
        with self.assertRaisesRegex(theme.ThemeError, "Untracked custom"):
            self.engine.check("plague-tale")
        file.write_bytes(saved); self.engine.apply("plague-tale")
        file.write_bytes(saved + b"\n// later edits")
        for action in (lambda: self.engine.apply("plague-tale"), self.engine.rollback):
            with self.assertRaisesRegex(theme.ThemeError, "changed"): action()
        self.assertTrue(file.read_bytes().endswith(b"// later edits"))

    def test_target_and_parent_symlinks_are_refused_without_touching_target(self):
        file = self.engine.style / "kitty/theme.conf"; data = file.read_bytes()
        external = self.base / "external"; external.write_bytes(data)
        file.unlink(); file.symlink_to(external)
        with self.assertRaisesRegex(theme.ThemeError, "Symlink"): self.engine.check("plague-tale")
        self.assertEqual(external.read_bytes(), data)
        file.unlink(); file.write_bytes(data)
        folder = self.engine.style / "kitty"
        folder.rename(self.engine.style / "real-kitty")
        folder.symlink_to("real-kitty", target_is_directory=True)
        with self.assertRaisesRegex(theme.ThemeError, "Symlink"): self.engine.check("plague-tale")

    def test_duplicate_json_unsupported_schema_missing_surface_hooks_and_traversal(self):
        path = self.package / "themes/plague-tale/manifest.json"
        original = path.read_bytes()
        variants = []
        good = json.loads(original)
        for key, value in (("schema", 99), ("shellAbi", "other"), ("surfaces", ["bar"]), ("hooks", ["rm -rf ~"])):
            item = json.loads(original); item[key] = value; variants.append(theme.json_bytes(item))
        item = json.loads(original); item["files"][0]["source"] = "../escape"; variants.append(theme.json_bytes(item))
        item = json.loads(original); item["files"][0]["target"] = "style/scripts/start.sh"; variants.append(theme.json_bytes(item))
        variants.append(original.replace(b'"schema": 1', b'"schema": 1, "schema": 1'))
        for data in variants:
            path.write_bytes(data)
            with self.assertRaises(theme.ThemeError): self.engine.load("plague-tale")
        path.write_bytes(original)

    def test_corrupt_package_preview_and_missing_asset_are_refused(self):
        folder = self.package / "themes/plague-tale"
        manifest = theme.read_json(folder / "manifest.json")
        file = folder / manifest["files"][0]["source"]
        saved = file.read_bytes(); file.write_bytes(saved + b"x")
        with self.assertRaisesRegex(theme.ThemeError, "integrity"): self.engine.load("plague-tale")
        file.write_bytes(saved)
        preview = folder / manifest["preview"]["source"]
        saved = preview.read_bytes(); preview.write_bytes(saved[:-50])
        manifest["preview"]["gitBlob"] = theme.git_blob(preview.read_bytes())
        (folder / "manifest.json").write_bytes(theme.json_bytes(manifest))
        with self.assertRaisesRegex(theme.ThemeError, "PNG"): self.engine.load("plague-tale")

    def test_shared_abi_mismatch_and_corrupt_state_are_refused(self):
        file = self.engine.style / theme.SHARED[0]; saved = file.read_bytes(); file.write_bytes(b"old shell")
        with self.assertRaisesRegex(theme.ThemeError, "ABI"): self.engine.check("plague-tale")
        file.write_bytes(saved)
        self.engine.data.mkdir()
        (self.engine.data / "active.json").write_text("null")
        with self.assertRaisesRegex(theme.ThemeError, "state object"): self.engine.check("plague-tale")

    def test_snapshot_corruption_blocks_rollback_before_stop(self):
        self.engine.apply("plague-tale")
        dest, record = self.engine.read_transaction(self.engine.pointer())
        name = next(iter(record["before"]))
        (dest / "before" / name).write_bytes(b"corrupted")
        self.runtime.events.clear()
        with self.assertRaisesRegex(theme.ThemeError, "Snapshot integrity"): self.engine.rollback()
        self.assertNotIn("stop", self.runtime.events)

    def test_state_commit_failure_restores_files_and_active_marker(self):
        atomic = theme.atomic
        failed = False
        def fail_once(path, *args, **kwargs):
            nonlocal failed
            if path == self.engine.data / "active.json" and not failed:
                failed = True; raise OSError("fixture disk full")
            return atomic(path, *args, **kwargs)
        with patch.object(theme, "atomic", side_effect=fail_once):
            with self.assertRaisesRegex(theme.ThemeError, "previous state restored"):
                self.engine.apply("plague-tale")
        self.assertIsNone(self.engine.optional("active.json"))
        self.assertIsNone(self.engine.optional("pending.json"))

    def interrupt(self, committed=False):
        atomic = theme.atomic
        def crash(path, data, *args, **kwargs):
            atomic(path, data, *args, **kwargs)
            if (committed and path.name == "manifest.json" and b'"status": "committed"' in data
                    or not committed and path == self.engine.style / "wallpaper.png"):
                raise KeyboardInterrupt("simulated process interruption")
        with patch.object(theme, "atomic", side_effect=crash):
            with self.assertRaises(KeyboardInterrupt): self.engine.apply("plague-tale")

    def test_interrupted_apply_recovers_original_and_clears_pending(self):
        self.interrupt()
        self.assertIsNotNone(self.engine.optional("pending.json"))
        with self.assertRaisesRegex(theme.ThemeError, "Interrupted"): self.engine.check("plague-tale")
        self.engine.recover()
        self.assertIsNone(self.engine.optional("pending.json"))
        self.assertIsNone(self.engine.optional("active.json"))

    def test_committed_interruption_only_finishes_journal(self):
        self.interrupt(True)
        active = self.engine.optional("active.json")
        self.runtime.events.clear(); self.engine.recover()
        self.assertEqual(self.engine.optional("active.json"), active)
        self.assertIsNone(self.engine.optional("pending.json"))
        self.assertEqual(self.runtime.events, [])

    def test_manual_edit_after_interruption_is_preserved(self):
        self.interrupt()
        file = self.engine.style / "wallpaper.png"; file.write_bytes(b"my changed image")
        with self.assertRaisesRegex(theme.ThemeError, "edited after interruption"): self.engine.recover()
        self.assertEqual(file.read_bytes(), b"my changed image")

    def test_failed_automatic_recovery_retains_journal_for_retry(self):
        self.runtime.fail["start"] = 2
        with self.assertRaisesRegex(theme.ThemeError, "Recovery incomplete"): self.engine.apply("plague-tale")
        self.assertIsNotNone(self.engine.optional("pending.json"))
        self.engine.recover()
        self.assertIsNone(self.engine.optional("pending.json"))

    def test_concurrent_updater_lock_blocks_mutation(self):
        with (self.engine.state / "update.lock").open("a") as lock:
            theme.fcntl.flock(lock, theme.fcntl.LOCK_EX | theme.fcntl.LOCK_NB)
            before = self.state()
            with self.assertRaisesRegex(theme.ThemeError, "Another update"): self.engine.apply("plague-tale")
            self.assertEqual(before, self.state())

    def test_native_wallpaper_adapter_preserves_monitor_fit(self):
        native = theme.Native(self.engine); native.wallpaper_fits = {"eDP-1": "contain", "": "tile"}
        calls = []
        def run(args):
            calls.append(args)
            output = "eDP-1: /old.png\nDP-2: /old.png\n" if args[-1] == "listactive" else ""
            return subprocess.CompletedProcess(args, 0, output, "")
        with patch.object(native, "run", side_effect=run): native.reload()
        commands = [c[-1] for c in calls if "wallpaper" in c]
        cached = self.engine.data / "wallpapers" / (theme.digest((self.engine.style / "wallpaper.png").read_bytes()) + ".png")
        self.assertEqual(commands, ["eDP-1," + str(cached) + ",contain", "DP-2," + str(cached) + ",tile"])
        self.assertEqual(cached.read_bytes(), (self.engine.style / "wallpaper.png").read_bytes())

    def test_native_preflight_accepts_same_quickshell_versions_as_updater(self):
        for version in ("Quickshell 0.3.1 (revision abc, distributed by Arch)",
                        "Quickshell v0.3.1", "Quickshell 0.3.2", "Quickshell 0.3.10", "Quickshell 0.4.0"):
            for stderr in (False, True):
                with self.subTest(version=version, stderr=stderr):
                    native = theme.Native(self.engine)
                    def run(args):
                        output = version if args[0] == "quickshell" else "Hyprland 0.56.2"
                        return subprocess.CompletedProcess(args, 0,
                            "" if stderr and args[0] == "quickshell" else output,
                            output if stderr and args[0] == "quickshell" else "")
                    with patch.object(theme.os, "geteuid", return_value=1000), \
                         patch.dict(theme.os.environ, {"HYPRLAND_INSTANCE_SIGNATURE": "fixture"}), \
                         patch.object(theme.shutil, "which", return_value="/fixture/bin"), \
                         patch.object(native, "run", side_effect=run), \
                         patch.object(native, "monitors", return_value=["eDP-1"]), \
                         patch.object(theme, "load_module", return_value=object()):
                        native.prepare_recovery()

    def test_native_preflight_rejects_old_or_unknown_version_with_actual_output(self):
        for version in ("Quickshell 0.3.0", "Quickshell 0.2.1", "unrecognized version", ""):
            native = theme.Native(self.engine)
            def run(args):
                return subprocess.CompletedProcess(args, 0,
                    version if args[0] == "quickshell" else "Hyprland 0.56.2", "")
            with patch.object(theme.os, "geteuid", return_value=1000), \
                 patch.dict(theme.os.environ, {"HYPRLAND_INSTANCE_SIGNATURE": "fixture"}), \
                 patch.object(theme.shutil, "which", return_value="/fixture/bin"), \
                 patch.object(native, "run", side_effect=run):
                with self.assertRaisesRegex(theme.ThemeError, "0.3.1 or newer") as error:
                    native.prepare_recovery()
                self.assertIn(version or "<empty output>", str(error.exception))

    def test_reapply_same_package_does_not_restart_or_add_snapshot(self):
        self.engine.apply("plague-tale")
        before = self.state(); self.runtime.events.clear()
        self.assertIsNone(self.engine.apply("plague-tale"))
        self.assertEqual(before, self.state())
        self.assertNotIn("stop", self.runtime.events)

    def test_update_allows_identical_payload_and_blocks_theme_loss(self):
        self.engine.apply("plague-tale"); self.engine.guard_update()
        source = self.package / "payload/style/shell/ui/Theme.qml"
        source.write_bytes(source.read_bytes() + b"\n// source update")
        before = self.state()
        with self.assertRaisesRegex(theme.ThemeError, "would replace"): self.engine.guard_update()
        self.assertEqual(before, self.state())

    def test_update_guard_blocks_variant_and_interrupted_transaction(self):
        self.variant(); self.engine.apply("fixture-variant")
        with self.assertRaisesRegex(theme.ThemeError, "would replace"): self.engine.guard_update()
        self.engine.rollback()
        self.interrupt()
        with self.assertRaisesRegex(theme.ThemeError, "interrupted"): self.engine.guard_update()

    def test_old_installation_snapshot_is_never_restored_into_a_fresh_install(self):
        self.engine.apply("plague-tale")
        marker = self.engine.state / "current-backup"
        original = marker.read_bytes()
        try:
            marker.write_text("/a-new-original-backup")
            for action in (lambda: self.engine.check("plague-tale"), self.engine.rollback):
                with self.assertRaisesRegex(theme.ThemeError, "previous MCT installation"): action()
        finally:
            marker.write_bytes(original)

    def test_real_updater_rechecks_theme_guard_inside_its_lock(self):
        sys.path.insert(0, str(ROOT))
        import update as updater
        self.variant(); self.engine.apply("fixture-variant")
        before = self.state()
        with patch.object(updater, "check", return_value="fixture binds"), \
             patch.object(updater.m, "STATE", self.engine.state), \
             patch.object(updater.m, "STYLE", self.engine.style), \
             patch.object(updater.m, "HYPR", self.engine.hypr), \
             patch.object(updater.m, "PACKAGE", self.package):
            with self.assertRaisesRegex(RuntimeError, "would replace"):
                updater.update()
        self.assertEqual(before, self.state())

    def test_native_stop_only_targets_this_shell(self):
        import types
        rows = [(101, ["quickshell", "-p", "mct"]), (102, ["quickshell", "-p", "another"]),
                (103, ["dunst"])]
        native = theme.Native(self.engine)
        native.session = types.SimpleNamespace(processes=lambda: iter(rows),
                    is_shell=lambda args: args == ["quickshell", "-p", "mct"])
        killed = []
        def kill(pid, sig):
            killed.append(pid)
            rows[:] = [(p, a) for p, a in rows if p != pid]
        with patch.object(theme.os, "kill", side_effect=kill): native.stop()
        self.assertEqual(killed, [101])
        self.assertEqual([p for p, _ in rows], [102, 103])

    def test_native_restore_uses_each_saved_wallpaper_and_configured_fit(self):
        native = theme.Native(self.engine); native.wallpaper_fits = {"": "cover"}
        old = self.base / "old photo.png"; old.write_bytes(b"fixture")
        other = self.base / "another.png"; other.write_bytes(b"fixture 2")
        calls = []
        def run(args):
            calls.append(args)
            output = "eDP-1: /current.png\nDP-2: /current.png\n" if args[-1] == "listactive" else ""
            return subprocess.CompletedProcess(args, 0, output, "")
        snapshot = {"eDP-1": {"path": str(old), "fit": "contain"},
                    "DP-2": {"path": str(other), "fit": "tile"}}
        with patch.object(native, "run", side_effect=run): native.restore(snapshot)
        self.assertEqual([c[-1] for c in calls if "wallpaper" in c],
                         ["eDP-1," + str(old) + ",contain", "DP-2," + str(other) + ",tile"])

    def test_theme_snapshot_records_runtime_wallpaper_state(self):
        self.engine.apply("plague-tale")
        _, record = self.engine.read_transaction(self.engine.pointer())
        self.assertEqual(record["beforeRuntime"],
                         {"fixture": {"path": "/original.png", "fit": "contain"}})

    def test_cli_list_and_status_need_no_native_session(self):
        for action in ("list", "status"):
            env = dict(os.environ); env["HOME"] = str(self.base)
            result = subprocess.run([sys.executable, str(ROOT / "theme_core.py"), action],
                                    capture_output=True, text=True, env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            value = json.loads(result.stdout)
            if action == "list":
                self.assertEqual({row["id"] for row in value}, {"plague-tale", "deltarune", "deltarune-snowgrave"})
            else:
                self.assertIsNone(value["active"])


if __name__ == "__main__":
    unittest.main()
