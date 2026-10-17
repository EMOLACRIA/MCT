#!/usr/bin/env python3
"""Trusted local theme packages: validate, apply, rollback and interrupted-run recovery."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import stat
import struct
import subprocess
import sys
import tempfile
import time
import zlib

ROOT = Path(__file__).resolve().parent
ABI = "mct-shell-2.6"
VIEWS = frozenset(("ActionButton Bar Controls Feedback Glyph Hardware HintBubble Launcher "
    "LevelControl Media NotificationActions Notifications OrnamentFrame Overlay PanelHeader "
    "Power PreferenceChoice PreferenceSlider Settings SurfaceLayout Theme Toast ToastStack "
    "WindowSwitcher").split())
SHARED = ("shell/shell.qml", "shell/LiveContext.qml", "shell/validate.qml",
          "shell/ui/UiState.qml", "shell/ui/PreferencesState.qml",
          "shell/ui/WindowSwitcherState.qml", "shell/ui/NotificationWatcher.qml")
SURFACES = frozenset(("bar launcher switcher controls notifications media hardware osd "
                      "power settings lock terminal sddm dolphin spotify").split())


class ThemeError(RuntimeError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def unique(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ThemeError("Duplicate JSON key: " + key)
        obj[key] = value
    return obj


def read_json(path):
    try:
        return json.loads(path.read_text(), object_pairs_hook=unique)
    except (ValueError, OSError) as exc:
        raise ThemeError("Cannot read JSON: " + str(path)) from exc


def safe(root, relative):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ThemeError("Invalid relative path")
    parts = relative.split("/")
    if any(p in ("", ".", "..") for p in parts) or PurePosixPath(relative).is_absolute():
        raise ThemeError("Unsafe path: " + relative)
    root = Path(root).absolute()
    path = root.joinpath(*parts)
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ThemeError("Symlink needs adaptation: " + str(part))
    return path


def allowed(name):
    if name == "hypr/appearance.lua":
        return True
    if name in ("style/wallpaper.png", "style/kitty/theme.conf", "style/hyprlock/media.conf"):
        return True
    p = PurePosixPath(name)
    if str(p.parent) == "style/shell/ui" and p.suffix == ".qml" and p.stem in VIEWS:
        return True
    return (str(p.parent) in ("style/shell/assets", "style/hyprlock")
            and bool(re.fullmatch(r"[A-Za-z0-9_-]+\.(png|svg)", p.name)))


def png(data):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ThemeError("Invalid PNG")
    at = 8
    while at + 12 <= len(data):
        length = struct.unpack(">I", data[at:at+4])[0]
        end = at + 12 + length
        if end > len(data):
            raise ThemeError("Truncated PNG")
        block = data[at+4:end-4]
        if zlib.crc32(block) != struct.unpack(">I", data[end-4:end])[0]:
            raise ThemeError("PNG checksum mismatch")
        if block[:4] == b"IEND":
            if length or end != len(data):
                raise ThemeError("Invalid PNG end")
            return
        at = end
    raise ThemeError("Missing PNG end")


def atomic(path, data, mode=0o600):
    safe(path.parent, path.name)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(prefix="." + path.name + "-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def load_module(path):
    spec = importlib.util.spec_from_file_location("_mct_theme_session", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Native:
    """Commands are core-owned; a theme never supplies hooks or processes."""
    def __init__(self, engine):
        self.engine = engine
        self.session = None
        self.wallpaper_fits = {}

    def prepare_recovery(self):
        if os.geteuid() == 0:
            raise ThemeError("Run as your desktop user, without sudo.")
        if not os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"):
            raise ThemeError("Run inside your active Hyprland session.")
        for name in ("hyprctl", "quickshell", "busctl", "hyprpaper"):
            if not shutil.which(name):
                raise ThemeError("Missing command: " + name)
        result = self.run(["hyprctl", "version"])
        if "0.56.2" not in result.stdout:
            raise ThemeError("Hyprland 0.56.2 is required.")
        result = self.run(["quickshell", "--version"])
        if not re.search(r"\b0\.3\.1\b", result.stdout + result.stderr):
            raise ThemeError("This theme ABI was checked with QuickShell 0.3.1.")
        config = (self.engine.hypr / "hyprpaper.conf").read_text()
        if re.search(r"(?m)^\s*source\s*=", config):
            raise ThemeError("Sourced hyprpaper configuration needs adapter adaptation.")
        fits = {}
        for block in re.findall(r"wallpaper\s*\{([^{}]*)\}", config):
            values = dict(re.findall(r"(?m)^\s*(monitor|fit_mode)\s*=\s*([^#\n]*)", block))
            monitor = values.get("monitor", "").strip()
            fit = values.get("fit_mode", "cover").strip()
            if fit not in ("cover", "contain", "tile", "fill"):
                raise ThemeError("Unknown wallpaper fit mode")
            fits[monitor] = fit
        self.wallpaper_fits = fits
        self.monitors()
        self.session = load_module(self.engine.root / "payload/style/scripts/session.py")

    def preflight(self):
        self.prepare_recovery()
        self.clean()
        if not self.session.feedback_ready():
            raise ThemeError("The installed MCT shell must be running and own notifications.")

    def run(self, args):
        result = subprocess.run(args, capture_output=True, text=True, timeout=20)
        if result.returncode:
            raise ThemeError("Command failed: " + " ".join(args) + "\n" + result.stdout + result.stderr)
        return result

    def clean(self):
        if self.run(["hyprctl", "configerrors"]).stdout.strip():
            raise ThemeError("Resolve the existing Hyprland config errors first.")

    def validate(self, style, appearance):
        # Compile without instantiating the candidate shell/services.
        self.run(["quickshell", "-p", str(style / "shell/validate.qml")])
        # appearance.lua is trusted package code; reload errors also trigger rollback.

    def stop(self):
        targets = [(pid, args) for pid, args in self.session.processes() if self.session.is_shell(args)]
        for pid, _ in targets:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        deadline = time.monotonic() + 4
        while time.monotonic() < deadline:
            if not any(self.session.is_shell(args) for _, args in self.session.processes()):
                return
            time.sleep(.05)
        raise ThemeError("MCT shell did not stop; another instance was not started.")

    def start(self):
        if not any(self.session.is_shell(args) for _, args in self.session.processes()):
            self.session.launch(["quickshell", "-p", str(self.engine.style / "shell")], "shell.log")
        self.session.wait_feedback()

    def monitors(self):
        result = self.run(["hyprctl", "hyprpaper", "listactive"])
        names = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            monitor, separator, _ = line.partition(": ")
            if not separator or not re.fullmatch(r"[A-Za-z0-9_.-]+", monitor):
                raise ThemeError("Cannot parse hyprpaper listactive output")
            names.append(monitor)
        if not names:
            raise ThemeError("No active hyprpaper wallpaper")
        return names

    def reload(self):
        self.run(["hyprctl", "reload"])
        self.clean()
        # The selected monitor, fit mode and GPU settings are not changed.
        data = (self.engine.style / "wallpaper.png").read_bytes()
        cached = safe(self.engine.data, "wallpapers/" + digest(data) + ".png")
        if not cached.is_file() or cached.read_bytes() != data:
            atomic(cached, data, 0o644)
        for monitor in self.monitors():
            fit = self.wallpaper_fits.get(monitor, self.wallpaper_fits.get("", "cover"))
            self.run(["hyprctl", "hyprpaper", "wallpaper",
                      monitor + "," + str(cached) + "," + fit])


class Engine:
    def __init__(self, root=ROOT, style=None, state=None, hypr=None, runtime=None):
        home = Path.home()
        self.root = Path(root).absolute()
        self.style = Path(style or home / ".config/desktop-style").absolute()
        self.state = Path(state or home / ".local/state/desktop-style").absolute()
        self.hypr = Path(hypr or home / ".config/hypr").absolute()
        self.data = self.state / "theme-core"
        self.runtime = runtime or Native(self)

    def path(self, target):
        if not allowed(target):
            raise ThemeError("Not a theme-owned target: " + str(target))
        kind, relative = target.split("/", 1)
        return safe(self.style if kind == "style" else self.hypr, relative)

    def load(self, name):
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ThemeError("Invalid theme id")
        folder = safe(self.root, "themes/" + name)
        manifest = read_json(safe(folder, "manifest.json"))
        if not isinstance(manifest, dict) or set(manifest) != {
                "schema", "id", "name", "version", "shellAbi", "preview", "surfaces", "files", "adapters"}:
            raise ThemeError("Invalid manifest fields")
        if type(manifest["schema"]) is not int or manifest["schema"] != 1:
            raise ThemeError("Unsupported manifest schema")
        if manifest["id"] != name or manifest["shellAbi"] != ABI:
            raise ThemeError("Theme id / shell ABI mismatch")
        if not all(isinstance(manifest[k], str) and 0 < len(manifest[k]) <= 100
                   for k in ("name", "version")):
            raise ThemeError("Invalid theme metadata")
        if (not isinstance(manifest["surfaces"], list)
                or not all(isinstance(s, str) for s in manifest["surfaces"])
                or set(manifest["surfaces"]) != SURFACES):
            raise ThemeError("Theme does not declare every required surface")
        if manifest["adapters"] != {"sddm": "separate-installer", "dolphin": "separate-installer",
                                   "spotify": "separate-installer"}:
            raise ThemeError("Unsupported external adapter; no theme hooks are executed")
        preview = manifest["preview"]
        if not isinstance(preview, dict) or set(preview) != {"source", "gitBlob"}:
            raise ThemeError("A real screenshot preview is required")
        preview_path = safe(folder, preview["source"])
        if not preview_path.is_file() or preview_path.stat().st_size > 16 * 1024 * 1024:
            raise ThemeError("Missing or oversized preview")
        image = preview_path.read_bytes()
        if git_blob(image) != preview["gitBlob"]:
            raise ThemeError("Preview integrity mismatch")
        png(image)
        entries = manifest["files"]
        if not isinstance(entries, list) or not 1 <= len(entries) <= 128:
            raise ThemeError("Invalid file inventory")
        output = {}
        total = 0
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != {"source", "target", "gitBlob"}:
                raise ThemeError("Invalid file entry")
            target = entry["target"]
            if not isinstance(target, str) or target in output or not allowed(target):
                raise ThemeError("Duplicate or forbidden target")
            file = safe(folder, entry["source"])
            if not file.is_file() or file.stat().st_size > 16 * 1024 * 1024:
                raise ThemeError("Missing or oversized package file")
            data = file.read_bytes()
            if git_blob(data) != entry["gitBlob"]:
                raise ThemeError("Package integrity mismatch: " + target)
            if file.suffix == ".png":
                png(data)
            if target == "style/hyprlock/media.conf":
                data = data.replace(b"@STYLE@", str(self.style).encode())
            total += len(data)
            output[target] = data
        required = {"hypr/appearance.lua", "style/wallpaper.png", "style/kitty/theme.conf",
                    "style/hyprlock/media.conf", "style/shell/ui/Theme.qml",
                    "style/shell/ui/SurfaceLayout.qml"}
        if not required <= output.keys() or total > 64 * 1024 * 1024:
            raise ThemeError("Incomplete or oversized theme package")
        return manifest, output

    def optional(self, name):
        path = safe(self.data, name)
        if not path.exists():
            return None
        value = read_json(path)
        if not isinstance(value, dict):
            raise ThemeError("Invalid state object: " + name)
        return value

    def pointer(self):
        value = self.optional("last.json")
        if value is not None and (not isinstance(value, dict) or set(value) != {"transaction"}
                or not isinstance(value["transaction"], str)
                or not re.fullmatch(r"[0-9]{8}T[0-9]{12}Z-[0-9a-f]{8}", value["transaction"])):
            raise ThemeError("Invalid theme transaction pointer")
        return value

    def verify_installed(self):
        for p in (self.style, self.state, self.hypr, self.data):
            safe(p.parent, p.name)
        if not (self.state / "current-backup").is_file():
            raise ThemeError("Install MCT first; the original restore point is required.")
        shared = set(SHARED)
        for source in (self.root / "payload/style/shell").rglob("*"):
            if source.is_file():
                relative = str(source.relative_to(self.root / "payload/style"))
                if not allowed("style/" + relative):
                    shared.add(relative)
        for relative in sorted(shared):
            source = safe(self.root, "payload/style/" + relative)
            current = safe(self.style, relative)
            if not current.is_file() or current.read_bytes() != source.read_bytes():
                raise ThemeError("Shared shell ABI differs; update MCT before applying a theme: " + relative)

    def installation(self):
        return safe(self.state, "current-backup").read_text().strip()

    def ownership(self, targets):
        active = self.optional("active.json")
        if active is not None and active.get("installation") != self.installation():
            raise ThemeError("Theme state belongs to a previous MCT installation; archive it before reuse.")
        if active is not None and (active.get("schema") != 1 or not isinstance(active.get("files"), dict)
                or not all(isinstance(k, str) and allowed(k) and isinstance(v, str)
                           and re.fullmatch(r"[0-9a-f]{64}", v) for k, v in active["files"].items())):
            raise ThemeError("Invalid active theme inventory")
        known = active["files"] if active is not None else {}
        for name in set(targets) | set(known):
            path = self.path(name)
            if name in known:
                if not path.is_file() or digest(path.read_bytes()) != known[name]:
                    raise ThemeError("Theme file changed manually; kept unchanged: " + name)
            elif path.exists():
                if not path.is_file():
                    raise ThemeError("Not a regular theme file: " + name)
                base = safe(self.root / "payload", name)
                expected = base.read_bytes().replace(b"@STYLE@", str(self.style).encode()) if base.is_file() else None
                if expected is None or path.read_bytes() != expected:
                    raise ThemeError("Untracked custom file needs adaptation: " + name)
        return active, known

    @contextmanager
    def lock(self):
        safe(self.state, "update.lock")
        with (self.state / "update.lock").open("a") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise ThemeError("Another update/theme operation is running.") from exc
            yield

    def stage(self, output, remove):
        stage = tempfile.TemporaryDirectory(prefix="mct-theme-check-")
        root = Path(stage.name)
        try:
            shutil.copytree(self.style, root / "style", symlinks=True)
            for name in remove:
                if name.startswith("style/"):
                    safe(root, name).unlink(missing_ok=True)
            for name, data in output.items():
                path = safe(root, name)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            appearance = root / "hypr/appearance.lua"
            if not appearance.is_file():
                appearance.parent.mkdir(exist_ok=True)
                appearance.write_bytes((self.hypr / "appearance.lua").read_bytes())
            self.runtime.validate(root / "style", appearance)
        finally:
            stage.cleanup()

    def prepare(self, name):
        self.verify_installed()
        if self.optional("pending.json") is not None:
            raise ThemeError("Interrupted theme transaction found. Run theme.sh recover first.")
        self.runtime.preflight()
        manifest, output = self.load(name)
        _, known = self.ownership(output)
        self.stage(output, set(known) - output.keys())
        return manifest, output, known

    def check(self, name):
        return self.prepare(name)[0]

    def read_transaction(self, pointer):
        dest = safe(self.data, "transactions/" + pointer["transaction"])
        record = read_json(safe(dest, "manifest.json"))
        if not isinstance(record, dict) or record.get("schema") != 1:
            raise ThemeError("Invalid transaction record")
        if record.get("installation") != self.installation():
            raise ThemeError("Snapshot belongs to a previous MCT installation; it was not restored.")
        for name, item in record["before"].items():
            self.path(name)
            if item is not None:
                data = safe(dest, "before/" + name).read_bytes()
                if digest(data) != item["sha256"]:
                    raise ThemeError("Snapshot integrity mismatch: " + name)
        return dest, record

    def restore_record(self, dest, record):
        for name, item in record["before"].items():
            path = self.path(name)
            if item is None:
                path.unlink(missing_ok=True)
            else:
                atomic(path, safe(dest, "before/" + name).read_bytes(), item["mode"])
        for file, value in (("active.json", record["beforeActive"]), ("last.json", record["beforeLast"])):
            path = safe(self.data, file)
            if value is None:
                path.unlink(missing_ok=True)
            else:
                atomic(path, json_bytes(value))

    def transact(self, output, remove, after_active, after_last, kind, modes=None):
        before_active = self.optional("active.json")
        before_last = self.pointer()
        ident = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ-") + os.urandom(4).hex()
        dest = safe(self.data, "transactions/" + ident)
        dest.mkdir(parents=True, mode=0o700)
        record = {"schema": 1, "installation": self.installation(), "kind": kind, "status": "prepared", "beforeActive": before_active,
                  "beforeLast": before_last, "before": {}, "after": {}}
        for name in sorted(set(output) | set(remove)):
            path = self.path(name)
            if path.exists():
                data = path.read_bytes()
                atomic(safe(dest, "before/" + name), data)
                record["before"][name] = {"sha256": digest(data), "mode": stat.S_IMODE(path.stat().st_mode)}
            else:
                record["before"][name] = None
            record["after"][name] = digest(output[name]) if name in output else None
        atomic(dest / "manifest.json", json_bytes(record))
        atomic(self.data / "pending.json", json_bytes({"transaction": ident}))
        try:
            self.runtime.stop()
            for name in remove:
                self.path(name).unlink(missing_ok=True)
            for name, data in output.items():
                atomic(self.path(name), data, (modes or {}).get(name, 0o644))
            self.runtime.reload()
            self.runtime.start()
            if after_active is None:
                (self.data / "active.json").unlink(missing_ok=True)
            else:
                atomic(self.data / "active.json", json_bytes(after_active))
            desired_last = {"transaction": ident} if kind == "apply" else after_last
            if desired_last is None:
                (self.data / "last.json").unlink(missing_ok=True)
            else:
                atomic(self.data / "last.json", json_bytes(desired_last))
            record["status"] = "committed"
            atomic(dest / "manifest.json", json_bytes(record))
            (self.data / "pending.json").unlink()
        except Exception as original:
            try:
                self.runtime.stop()
                self.restore_record(dest, record)
                self.runtime.reload()
                self.runtime.start()
                (self.data / "pending.json").unlink(missing_ok=True)
                record["status"] = "rolled-back"
                atomic(dest / "manifest.json", json_bytes(record))
            except Exception as recovery:
                raise ThemeError("Recovery incomplete; snapshot retained at " + str(dest)
                                 + ". Run recover after resolving: " + str(recovery)) from original
            raise ThemeError("Theme operation failed; previous state restored: " + str(original)) from original
        return ident

    def guard_update(self):
        """Stop a source update from silently resetting a managed skin.

        A byte-identical update is safe; a changed presentation needs an explicit
        rollback/apply, keeping the original installer restore point untouched.
        """
        if self.optional("pending.json") is not None:
            raise ThemeError("Recover the interrupted theme transaction before updating.")
        active = self.optional("active.json")
        if active is None:
            return
        _, known = self.ownership(())
        for name in known:
            source = safe(self.root / "payload", name)
            data = source.read_bytes().replace(b"@STYLE@", str(self.style).encode()) if source.is_file() else None
            if data is None or digest(data) != known[name]:
                raise ThemeError("Update would replace the active theme. Run 'bash theme.sh rollback' "
                                 "until no active theme remains, update, then apply the theme again.")

    def apply(self, name):
        with self.lock():
            manifest, output, known = self.prepare(name)
            active = {"schema": 1, "installation": self.installation(), "id": name, "version": manifest["version"],
                      "files": {key: digest(data) for key, data in output.items()},
                      "adapters": {key: "separate-installer" for key in manifest["adapters"]}}
            if self.optional("active.json") == active:
                return None
            return self.transact(output, set(known) - output.keys(), active, None, "apply")

    def rollback(self, check_only=False):
        self.verify_installed()
        with self.lock():
            if self.optional("pending.json"):
                raise ThemeError("Run recover before rollback.")
            pointer = self.pointer()
            if pointer is None:
                raise ThemeError("No theme application to roll back.")
            dest, record = self.read_transaction(pointer)
            if record["status"] != "committed":
                raise ThemeError("Last transaction is not committed.")
            self.runtime.preflight()
            for name, expected in record["after"].items():
                path = self.path(name)
                actual = digest(path.read_bytes()) if path.is_file() else None
                if actual != expected:
                    raise ThemeError("Theme file changed after apply; rollback kept your edits: " + name)
            output = {name: safe(dest, "before/" + name).read_bytes()
                      for name, item in record["before"].items() if item is not None}
            remove = {name for name, item in record["before"].items() if item is None}
            self.stage(output, remove)
            if check_only:
                return pointer["transaction"]
            modes = {name: item["mode"] for name, item in record["before"].items() if item is not None}
            return self.transact(output, remove, record["beforeActive"], record["beforeLast"], "rollback", modes)

    def recover(self):
        self.verify_installed()
        with self.lock():
            pending = self.optional("pending.json")
            if pending is None:
                raise ThemeError("No interrupted theme transaction.")
            # Reuse the strict transaction-id parser without trusting arbitrary paths.
            token = pending.get("transaction") if isinstance(pending, dict) else None
            if not isinstance(token, str) or not re.fullmatch(r"[0-9]{8}T[0-9]{12}Z-[0-9a-f]{8}", token):
                raise ThemeError("Invalid recovery pointer")
            dest, record = self.read_transaction(pending)
            for name, before in record["before"].items():
                path = self.path(name)
                actual = digest(path.read_bytes()) if path.is_file() else None
                expected = before["sha256"] if before else None
                if actual not in (expected, record["after"][name]):
                    raise ThemeError("File edited after interruption; recovery kept edits: " + name)
            if record["status"] == "committed":
                for name, expected in record["after"].items():
                    path = self.path(name)
                    actual = digest(path.read_bytes()) if path.is_file() else None
                    if actual != expected:
                        raise ThemeError("Committed file changed; journal retained: " + name)
                (self.data / "pending.json").unlink()
                return token
            # Recovery must work when the candidate cannot answer IPC.
            self.runtime.prepare_recovery()
            self.runtime.stop()
            self.restore_record(dest, record)
            self.runtime.reload()
            self.runtime.start()
            record["status"] = "recovered"
            atomic(dest / "manifest.json", json_bytes(record))
            (self.data / "pending.json").unlink()
            return token


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("list")
    sub.add_parser("status")
    for command in ("check", "apply"):
        sub.add_parser(command).add_argument("theme")
    rollback = sub.add_parser("rollback")
    rollback.add_argument("--check", action="store_true")
    sub.add_parser("recover")
    args = parser.parse_args()
    engine = Engine()
    try:
        if args.action == "list":
            rows = []
            for folder in sorted((ROOT / "themes").iterdir()):
                if folder.is_dir():
                    manifest, _ = engine.load(folder.name)
                    rows.append({"id": manifest["id"], "name": manifest["name"], "version": manifest["version"],
                                 "preview": str(folder / manifest["preview"]["source"])})
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        elif args.action == "status":
            print(json.dumps({"active": engine.optional("active.json"),
                              "last": engine.pointer(), "pending": engine.optional("pending.json")}, indent=2))
        elif args.action == "check":
            manifest = engine.check(args.theme)
            print("Theme check passed: " + manifest["name"] + ". No installed files changed.")
        elif args.action == "apply":
            ident = engine.apply(args.theme)
            print("Theme applied. Snapshot: " + ident if ident else "Theme is already active; no restart needed.")
            print("SDDM, Dolphin and Spotify use separate installers; they were not reinstalled.")
        elif args.action == "rollback":
            print("Rollback check passed." if args.check and engine.rollback(True)
                  else "Previous theme restored. Snapshot: " + engine.rollback())
        else:
            print("Interrupted transaction recovered: " + engine.recover())
    except (ThemeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print("Stopped: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
