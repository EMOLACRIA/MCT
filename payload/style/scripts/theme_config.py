#!/usr/bin/env python3
"""Theme settings: shared window layout plus per-theme wallpaper, line and colours.

Settings live in $XDG_CONFIG_HOME/mct/theme-config.json, outside every theme
package. theme_core applies them on top of the integrity-checked package as a
normal theme transaction, so theme.sh rollback undoes an applied change and
"reset" returns a theme to its approved look. Standard library only, except an
optional Pillow/ImageMagick conversion when a JPEG/WebP wallpaper is imported.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import zlib

VERSION = 1
THEME_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
COLOR = re.compile(r"#(?:[0-9a-fA-F]{2})?[0-9a-fA-F]{6}")  # #RRGGBB or Qt's #AARRGGBB
# Interface name -> Theme.qml colour properties. Every MCT skin defines all of them.
ROLES = {
    "accent": ("brass",),
    "surface": ("background",),
    "raised": ("raised",),
    "selection": ("selectedSurface", "activeWorkspaceSurface"),
    "text": ("ink",),
    "secondary": ("muted",),
    "line": ("line",),
    "warning": ("danger",),
}
# Interface name -> (min, max, appearance.lua key). Blur/shadow/animation are deliberately absent.
LAYOUT = {"gapsIn": (0, 20, "gaps_in"), "gapsOut": (0, 40, "gaps_out"),
          "border": (0, 6, "border_size"), "rounding": (0, 20, "rounding")}
# Letters (any script), digits and plain punctuation: safe in Hyprlock labels and Fastfetch.
QUOTE_LINE = re.compile(r"[^\W_]|[ .,!?'’…:;()\-]")
QUOTE_MAX = 18
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_WALLPAPER = 16 * 1024 * 1024
MAX_QUOTE_IMAGE = 4 * 1024 * 1024
QUOTE_SIZE = (1536, 1280)


class SettingsError(ValueError):
    pass


# ---------------------------------------------------------------- paths

def config_dir(env=None):
    env = os.environ if env is None else env
    home = Path(env.get("HOME") or Path.home())
    config = Path(env.get("XDG_CONFIG_HOME") or home / ".config")
    if not config.is_absolute():
        config = home / ".config"
    return config / "mct"


def state_dir(env=None):
    env = os.environ if env is None else env
    home = Path(env.get("HOME") or Path.home())
    state = Path(env.get("XDG_STATE_HOME") or home / ".local/state")
    if not state.is_absolute():
        state = home / ".local/state"
    return state / "desktop-style"


def config_path(env=None):
    return config_dir(env) / "theme-config.json"


def wallpaper_path(theme, env=None):
    return config_dir(env) / "wallpapers" / (check_id(theme) + ".png")


def quote_image_path(theme, env=None):
    return config_dir(env) / "quotes" / (check_id(theme) + ".png")


def check_id(theme):
    if not isinstance(theme, str) or not THEME_ID.fullmatch(theme):
        raise SettingsError("Invalid theme id.")
    return theme


# ---------------------------------------------------------------- schema

def empty():
    return {"version": VERSION,
            "layout": {"themeOwn": True, "gapsIn": 5, "gapsOut": 14, "border": 2, "rounding": 8},
            "themes": {}}


def validate(config):
    if not isinstance(config, dict) or set(config) != {"version", "layout", "themes"}:
        raise SettingsError("Theme settings fields are missing or unknown.")
    if type(config["version"]) is not int or config["version"] != VERSION:
        raise SettingsError("Unsupported theme settings version.")
    layout = config["layout"]
    if not isinstance(layout, dict) or set(layout) != {"themeOwn", *LAYOUT}:
        raise SettingsError("Invalid layout settings.")
    if type(layout["themeOwn"]) is not bool:
        raise SettingsError("Invalid layout setting: themeOwn")
    for key, (low, high, _) in LAYOUT.items():
        if type(layout[key]) is not int or not low <= layout[key] <= high:
            raise SettingsError("Out of range: " + key)
    themes = config["themes"]
    if not isinstance(themes, dict) or len(themes) > 64:
        raise SettingsError("Invalid theme list.")
    for theme, entry in themes.items():
        check_id(theme)
        if not isinstance(entry, dict) or not set(entry) <= {"wallpaper", "quote", "colors", "quoteImage"}:
            raise SettingsError("Invalid settings for " + theme)
        if "wallpaper" in entry:
            value = entry["wallpaper"]
            if (not isinstance(value, dict) or set(value) != {"desktop", "lock"}
                    or not all(type(v) is bool for v in value.values())):
                raise SettingsError("Invalid wallpaper setting for " + theme)
        if "quote" in entry:
            check_quote(entry["quote"])
        if "colors" in entry:
            colors = entry["colors"]
            if not isinstance(colors, dict) or not set(colors) <= set(ROLES):
                raise SettingsError("Unknown colour role for " + theme)
            for role, value in colors.items():
                if not isinstance(value, str) or not COLOR.fullmatch(value):
                    raise SettingsError("Invalid colour for " + role)
        if "quoteImage" in entry:
            meta = entry["quoteImage"]
            if (not isinstance(meta, dict) or set(meta) != {"sha256", "lines", "color"}
                    or not isinstance(meta["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", meta["sha256"])
                    or not isinstance(meta["color"], str) or not re.fullmatch(r"#[0-9a-f]{6}", meta["color"])):
                raise SettingsError("Invalid Fastfetch line image record for " + theme)
            check_quote(meta["lines"])
    return config


def check_quote(lines):
    if not isinstance(lines, list) or not 1 <= len(lines) <= 2:
        raise SettingsError("The line needs one or two rows.")
    for line in lines:
        if not isinstance(line, str) or not line.strip() or len(line) > QUOTE_MAX:
            raise SettingsError("Each row needs 1-%d characters." % QUOTE_MAX)
        if line != line.strip() or "  " in line or not all(QUOTE_LINE.fullmatch(c) for c in line):
            raise SettingsError("Use letters, digits, spaces and . , ! ? ' - : ; ( ) only.")
    return lines


def read(env=None):
    path = config_path(env)
    if not path.exists():
        return empty()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 65536:
        raise SettingsError("Theme settings file is not a small regular file: " + str(path))
    try:
        return validate(json.loads(path.read_text()))
    except json.JSONDecodeError as error:
        raise SettingsError("Theme settings are not valid JSON: " + str(error)) from error


def atomic(path, data, mode=0o600):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(prefix="." + path.name + "-", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write(config, env=None):
    atomic(config_path(env), (json.dumps(validate(config), indent=2, ensure_ascii=False) + "\n").encode())


# ---------------------------------------------------------------- images

def png_size(data):
    if data[:8] != PNG_MAGIC or len(data) < 33 or data[12:16] != b"IHDR":
        raise SettingsError("Not a PNG image.")
    width, height = struct.unpack(">II", data[16:24])
    if not (1 <= width <= 8192 and 1 <= height <= 8192):
        raise SettingsError("Image dimensions are not supported.")
    # Walk the chunks so a truncated file is refused before it reaches Hyprland.
    offset = 8
    while offset < len(data):
        size = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + size
        if end > len(data) or zlib.crc32(data[offset + 4:end - 4]) & 0xffffffff != struct.unpack(">I", data[end - 4:end])[0]:
            raise SettingsError("Damaged PNG image.")
        if kind == b"IEND":
            return width, height
        offset = end
    raise SettingsError("Damaged PNG image.")


def convert_to_png(source):
    """JPEG/WebP -> PNG with Pillow, else ImageMagick. Never through a shell."""
    try:
        from PIL import Image  # optional
        import io
        with Image.open(source) as image:
            image = image.convert("RGB")
            if max(image.size) > 7680:
                image.thumbnail((7680, 7680))
            buffer = io.BytesIO()
            image.save(buffer, "PNG", optimize=False)
            return buffer.getvalue()
    except ImportError:
        pass
    for tool in (["magick"], ["convert"]):
        if shutil.which(tool[0]):
            result = subprocess.run(tool + [str(source) + "[0]", "png:-"], capture_output=True, timeout=60)
            if result.returncode == 0:
                return result.stdout
            raise SettingsError("ImageMagick could not read the image.")
    raise SettingsError("PNG works directly; JPEG/WebP needs python-pillow or imagemagick.")


def import_wallpaper(theme, source, env=None):
    path = Path(source).expanduser()
    if not path.is_absolute() or not path.is_file():
        raise SettingsError("Choose an existing image file.")
    if path.stat().st_size > 64 * 1024 * 1024:
        raise SettingsError("Image is larger than 64 MB.")
    data = path.read_bytes()
    if data[:8] != PNG_MAGIC:
        if not (data[:3] == b"\xff\xd8\xff" or (data[:4] == b"RIFF" and data[8:12] == b"WEBP")):
            raise SettingsError("Use a PNG, JPEG or WebP image.")
        data = convert_to_png(path)
    png_size(data)
    if len(data) > MAX_WALLPAPER:
        raise SettingsError("Converted wallpaper is larger than 16 MB; use a smaller image.")
    target = wallpaper_path(theme, env)
    atomic(target, data, 0o644)
    return target


def quote_image(theme, entry, accent, env=None):
    """The shell-rendered Fastfetch image, only while it matches the saved line and accent."""
    meta = entry.get("quoteImage")
    if not meta or "quote" not in entry or meta["lines"] != entry["quote"] or meta["color"] != accent.lower():
        return None
    path = quote_image_path(theme, env)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_QUOTE_IMAGE:
        return None
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != meta["sha256"]:
        return None
    try:
        if png_size(data) != QUOTE_SIZE:
            return None
    except SettingsError:
        return None
    return data


# ---------------------------------------------------------------- resolution

def _number(text):
    text = text.strip()
    if re.fullmatch(r"\d+(?:\.\d+)?/\d+(?:\.\d+)?", text):
        top, bottom = text.split("/")
        return float(top) / float(bottom)
    if re.fullmatch(r"\d*\.?\d+", text):
        return float(text)
    raise SettingsError("Unsupported surface colour expression.")


BACKGROUND = re.compile(r"(readonly\s+property\s+color\s+background\s*:\s*)Qt\.rgba\(([^,()]+),([^,()]+),([^,()]+),"
                        r"\s*(?:(\d*\.?\d+)\s*\*\s*)?preferences\.surfaceOpacity\s*\)")


def _role_pattern(prop):
    return re.compile(r"(readonly\s+property\s+color\s+" + prop + r"\s*:\s*)\"(#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?)\"")


def defaults(skin):
    """Approved colours of a skin as #RRGGBB or #AARRGGBB (Qt order)."""
    text = skin.decode() if isinstance(skin, bytes) else skin
    result = {}
    match = BACKGROUND.search(text)
    if not match:
        raise SettingsError("Theme.qml has no supported surface colour.")
    rgb = "".join("%02x" % round(_number(v) * 255) for v in match.group(2, 3, 4))
    factor = float(match.group(5)) if match.group(5) else 1.0
    result["surface"] = "#" + ("%02x" % round(factor * 255) if factor < 1 else "") + rgb
    for role, props in ROLES.items():
        if role == "surface":
            continue
        found = _role_pattern(props[0]).search(text)
        if not found:
            raise SettingsError("Theme.qml has no colour role: " + props[0])
        result[role] = found.group(2).lower()
    return result


def rgb_of(color):
    return color.lower()[-6:]


def alpha_of(color):
    return int(color[1:3], 16) / 255 if len(color) == 9 else 1.0


def _replace_once(pattern, replacement, text, what):
    result, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SettingsError("Cannot apply " + what + " to this theme.")
    return result


def swap_color(data, old, new):
    """Replace one colour wherever an adapter spells it as hex or as r,g,b."""
    text = data.decode()
    # Also rgba(RRGGBBAA): the colour may be followed by exactly one alpha byte.
    text = re.sub(r"(?i)(?<![0-9a-f])" + old + r"(?=(?:[0-9a-f]{2})?(?![0-9a-f]))", new, text)
    triplet = lambda h: ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    text = re.sub(r"(?<![\d,])" + re.escape(triplet(old)) + r"(?![\d])", triplet(new), text)
    return text.encode()


def accent_of(theme, output, config):
    entry = config["themes"].get(theme, {})
    skin = output["style/shell/ui/Theme.qml"]
    old = rgb_of(defaults(skin)["accent"])
    new = rgb_of(entry.get("colors", {}).get("accent", "#" + old))
    return old, new


def resolve(theme, output, config, default_quote=None, env=None):
    """Package files + settings -> the files theme_core installs. Pure; no writes."""
    check_id(theme)
    validate(config)
    output = dict(output)
    entry = config["themes"].get(theme, {})
    skin_key = "style/shell/ui/Theme.qml"
    skin = output[skin_key].decode()
    colors = entry.get("colors", {})
    if colors:
        approved = defaults(skin)
        for role, value in colors.items():
            if role == "surface":
                r, g, b = (int(rgb_of(value)[i:i + 2], 16) / 255 for i in (0, 2, 4))
                factor = alpha_of(value) if len(value) == 9 else alpha_of(approved["surface"])
                skin = _replace_once(BACKGROUND, lambda m: "%sQt.rgba(%.3f,%.3f,%.3f,%.3f*preferences.surfaceOpacity)"
                                     % (m.group(1), r, g, b, factor), skin, "the surface colour")
                continue
            for prop in ROLES[role]:
                skin = _replace_once(_role_pattern(prop), lambda m: m.group(1) + '"' + value.lower() + '"', skin, role)
        output[skin_key] = skin.encode()
        old, new = rgb_of(approved["accent"]), rgb_of(colors.get("accent", approved["accent"]))
        if old != new:
            for key in ("hypr/appearance.lua", "style/kitty/theme.conf",
                        "style/hyprlock/layout.conf", "style/hyprlock/media.conf"):
                output[key] = swap_color(output[key], old, new)
    layout = config["layout"]
    if not layout["themeOwn"]:
        text = output["hypr/appearance.lua"].decode()
        for key, (_, _, name) in LAYOUT.items():
            text = _replace_once(re.compile(r"(\b" + name + r"\s*=\s*)\d+"), lambda m: m.group(1) + str(layout[key]),
                                 text, "the " + name + " layout value")
        output["hypr/appearance.lua"] = text.encode()
    choice = entry.get("wallpaper")
    if choice and (choice["desktop"] or choice["lock"]):
        path = wallpaper_path(theme, env)
        if path.is_symlink() or not path.is_file():
            raise SettingsError("Custom wallpaper for " + theme + " is missing; choose it again or reset the theme.")
        custom = path.read_bytes()
        png_size(custom)
        approved = output["style/wallpaper.png"]
        desktop = custom if choice["desktop"] else approved
        lock = custom if choice["lock"] else approved
        output["style/wallpaper.png"] = output["style/shell/assets/wallpaper.png"] = desktop
        if lock is not desktop:
            output["style/hyprlock/lock-wallpaper.png"] = lock
            conf = output["style/hyprlock/layout.conf"].decode()
            block = re.search(r"background\s*\{[^{}]*\}", conf)
            if not block:
                raise SettingsError("This theme's lock screen has no background block.")
            inner, count = re.subn(r"(?m)^(\s*path\s*=\s*\S*/)wallpaper\.png\s*$", r"\1hyprlock/lock-wallpaper.png",
                                   block.group(0))
            if count != 1:
                raise SettingsError("This theme's lock screen does not use the theme wallpaper.")
            output["style/hyprlock/layout.conf"] = (conf[:block.start()] + inner + conf[block.end():]).encode()
    if "quote" in entry and default_quote:
        conf = output["style/hyprlock/layout.conf"].decode()
        old_line = re.compile(r"(?m)^(\s*text\s*=\s*)" + re.escape(" ".join(default_quote)) + r"\s*$")
        conf = old_line.sub(lambda m: m.group(1) + " ".join(entry["quote"]), conf)
        output["style/hyprlock/layout.conf"] = conf.encode()
    return output


def lock_has_quote(output, default_quote):
    if not default_quote:
        return False
    conf = output["style/hyprlock/layout.conf"].decode()
    return bool(re.search(r"(?m)^\s*text\s*=\s*" + re.escape(" ".join(default_quote)) + r"\s*$", conf))


def layout_defaults(output):
    text = output["hypr/appearance.lua"].decode()
    values = {}
    for key, (low, high, name) in LAYOUT.items():
        match = re.search(r"\b" + name + r"\s*=\s*(\d+)", text)
        values[key] = min(high, max(low, int(match.group(1)))) if match else empty()["layout"][key]
    return values


# ---------------------------------------------------------------- shell helper

def source_root(env=None):
    """The MCT checkout recorded by theme_core on the last theme check/apply."""
    pointer = state_dir(env) / "theme-core/source.json"
    if not pointer.is_file():
        raise SettingsError("Apply a theme once with Super+G so these settings can find MCT.")
    root = Path(json.loads(pointer.read_text()).get("root", ""))
    if not root.is_absolute() or not (root / "theme_core.py").is_file() or not (root / "theme.sh").is_file():
        raise SettingsError("The recorded MCT folder moved; apply a theme once with Super+G.")
    return root


def engine_for(root, env=None):
    sys.path.insert(0, str(root))
    import theme_core  # noqa: E402  (the checkout's own engine)
    return theme_core, theme_core.Engine(root, state=state_dir(env), settings_env=env)


def describe(env=None):
    result = {"ok": False, "error": "", "path": str(config_path(env)), "config": empty(), "active": None,
              "defaults": None, "lockQuote": False, "applied": None, "lastApply": None,
              "wallpaper": "", "customWallpaper": "", "quoteImagePath": ""}
    try:
        result["config"] = read(env)
    except (SettingsError, OSError) as error:
        result["error"] = str(error)
        return result
    last = state_dir(env) / "theme-config-last.json"
    if last.is_file():
        try:
            result["lastApply"] = json.loads(last.read_text())
        except (ValueError, OSError):
            pass
    try:
        core, engine = engine_for(source_root(env), env)
        active = engine.optional("active.json")
        if not active:
            raise SettingsError("No MCT theme is active; choose one with Super+G first.")
        theme = active["id"]
        manifest, files = engine.load(theme)
        quotes = core.load_module(engine.root / "fastfetch_quotes.py").QUOTES
        approved = dict(colors=defaults(files["style/shell/ui/Theme.qml"]), quote=list(quotes.get(theme, ())),
                        layout=layout_defaults(files))
        result.update(active=dict(id=theme, name=manifest["name"], version=manifest["version"]), defaults=approved,
                      lockQuote=lock_has_quote(files, quotes.get(theme)),
                      wallpaper=str(engine.root / "themes" / theme / "files/style/wallpaper.png"),
                      customWallpaper=str(wallpaper_path(theme, env)) if wallpaper_path(theme, env).is_file() else "",
                      quoteImagePath=str(quote_image_path(theme, env)))
        try:
            wanted = resolve(theme, files, result["config"], quotes.get(theme), env)
            result["applied"] = active.get("files") == {k: hashlib.sha256(v).hexdigest() for k, v in wanted.items()}
        except SettingsError as error:
            result["applied"] = False
            result["error"] = str(error)
            return result
        result["ok"] = True
    except (SettingsError, OSError, ValueError, KeyError) as error:
        result["error"] = str(error)
    return result


def save(candidate, rendered=False, env=None):
    config = validate(candidate)
    if rendered:
        # The shell has just written the Fastfetch image for the active theme's line.
        core, engine = engine_for(source_root(env), env)
        theme = (engine.optional("active.json") or {}).get("id")
        entry = config["themes"].get(theme or "", {})
        path = quote_image_path(theme, env) if theme else None
        if theme and "quote" in entry and path.is_file():
            _, files = engine.load(theme)
            accent = "#" + rgb_of(entry.get("colors", {}).get("accent", defaults(files["style/shell/ui/Theme.qml"])["accent"]))
            data = path.read_bytes()
            if png_size(data) == QUOTE_SIZE and len(data) <= MAX_QUOTE_IMAGE:
                entry["quoteImage"] = {"sha256": hashlib.sha256(data).hexdigest(), "lines": entry["quote"], "color": accent}
    for entry in config["themes"].values():
        if "quote" not in entry:
            entry.pop("quoteImage", None)
    config["themes"] = {k: v for k, v in config["themes"].items() if v}
    write(config, env)
    return config


def pick_file():
    """Ask the desktop's own file chooser; no chooser means paste the path instead."""
    home = str(Path.home())
    for command in (["kdialog", "--getopenfilename", home, "Images (*.png *.jpg *.jpeg *.webp)"],
                    ["zenity", "--file-selection", "--file-filter=Images | *.png *.jpg *.jpeg *.webp"],
                    ["yad", "--file", "--file-filter=Images | *.png *.jpg *.jpeg *.webp"]):
        if shutil.which(command[0]):
            result = subprocess.run(command, capture_output=True, text=True, timeout=600)
            return result.stdout.strip()
    raise SettingsError("No file chooser (kdialog or zenity) found; paste the image path instead.")


def spawn_apply(env=None):
    root = source_root(env)
    log = state_dir(env) / "theme-config-apply.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("ab") as handle:
        # A new session: the theme switch restarts the shell that asked for it.
        subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "run-apply", str(root)],
                         stdin=subprocess.DEVNULL, stdout=handle, stderr=handle, start_new_session=True)


def run_apply(root, env=None):
    core, engine = engine_for(Path(root), env)
    record = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "ok": False, "message": ""}
    try:
        active = engine.optional("active.json")
        if not active:
            raise core.ThemeError("No MCT theme is active.")
        transaction = engine.apply(active["id"])
        record.update(ok=True, message="Theme settings applied." if transaction else "Nothing to change; already applied.")
    except (core.ThemeError, SettingsError, OSError, ValueError, subprocess.SubprocessError) as error:
        record["message"] = "Not applied; previous desktop kept: " + str(error)
    atomic(state_dir(env) / "theme-config-last.json", (json.dumps(record) + "\n").encode())
    if shutil.which("notify-send"):
        subprocess.run(["notify-send", "-a", "MCT", "Theme settings", record["message"]], timeout=10, check=False)
    print(json.dumps(record))
    return 0 if record["ok"] else 1


def main(arguments):
    action = arguments[0] if arguments else "read"
    try:
        if action == "read":
            print(json.dumps(describe(), ensure_ascii=False))
            return 0
        if action == "run-apply" and len(arguments) == 2:
            return run_apply(arguments[1])
        if action == "save" and len(arguments) in (2, 3):
            save(json.loads(arguments[1]), rendered=arguments[2:] == ["rendered"])
        elif action == "apply" and len(arguments) in (2, 3):
            save(json.loads(arguments[1]), rendered=arguments[2:] == ["rendered"])
            spawn_apply()
        elif action == "wallpaper" and len(arguments) == 3:
            import_wallpaper(arguments[1], arguments[2])
        elif action == "pick" and len(arguments) == 1:
            result = describe()
            result.update(action="pick", picked=pick_file())
            print(json.dumps(result, ensure_ascii=False))
            return 0
        else:
            raise SettingsError("Unknown theme settings operation.")
        result = describe()
        result.update(action=action, ok=not result["error"] or action == "save")
        print(json.dumps(result, ensure_ascii=False))
    except (SettingsError, OSError, ValueError, subprocess.SubprocessError) as error:
        result = describe()
        result.update(action=action, ok=False, error=str(error))
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
