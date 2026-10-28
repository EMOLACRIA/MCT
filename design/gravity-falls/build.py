#!/usr/bin/env python3
"""Generate the gravity-falls theme package from Snowgrave Frost's structure.

Usage: python3 design/gravity-falls/build.py WALLPAPER_SOURCE_JPEG COURIER_REGULAR_TTF COURIER_BOLD_TTF COURIER_LICENSE
Re-running regenerates the package and its Fastfetch cipher image.
Colours follow the dusk palette taken from the user's wallpaper.
"""
import hashlib
import io
import json
import math
import re
import shutil
import string
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from theme_core import git_blob  # noqa: E402

TID = 'gravity-falls'
NAME = 'Gravity Falls'
VERSION = '0.1.0'
PLAIN = 'THE WOODS REMEMBER WHAT THE TOWN FORGETS.'


def caesar(text, shift=3):
    u = string.ascii_uppercase
    return ''.join(u[(u.index(c) + shift) % 26] if c in u else c for c in text)


CIPHER = caesar(PLAIN)  # WKH ZRRGV UHPHPEHU ZKDW WKH WRZQ IRUJHWV.
CIPHER_LINES = ('WKH ZRRGV UHPHPEHU', 'ZKDW WKH WRZQ', 'IRUJHWV.')

# Dusk palette (from the wallpaper: plum shade, sunlit logs, sign orange, pine).
P = dict(
    bg='140f12', deep='0a0709', card='1e1618', raised='2c1f1b', button='33241e',
    selected='3e2a1f', active='4a3020', line='4a3429', ink='f4e7d0', muted='b39e8c',
    mid='8a7566', accent='f0a84a', accent_bright='ffd08a', accent_deep='c47a3a',
    danger='e0574a', pine='9cc28a', neutral='e8c9a0',
)
# Frost colour -> dusk role
MAP = {
    '0b1421': P['bg'], '091421': P['bg'], '070f1a': P['deep'], '102236': P['card'],
    '162d45': P['raised'], '19394f': P['button'], '1b3852': '34251f', '224c6b': P['selected'],
    '2c6080': P['active'], '365873': P['line'], '6f94b4': P['mid'], '9fb8d0': P['muted'],
    '5a9cc7': P['accent_deep'], '9cdfff': P['accent'], 'd6f3ff': P['accent_bright'],
    'edf7ff': P['ink'], 'd9f0ff': P['ink'], 'e68a9d': P['danger'], 'b6e9e5': P['pine'],
    'b9d8ef': P['neutral'], 'd4eaff': P['neutral'],
}
FROST_LEFTOVERS = re.compile('|'.join(MAP), re.I)


def remap(text):
    def triplet(h):
        return ','.join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    out = FROST_LEFTOVERS.sub(lambda m: MAP[m.group(0).lower()], text)
    for src, dst in MAP.items():  # KDE colour files use r,g,b triplets
        out = re.sub(r'(?<![\d,])' + re.escape(triplet(src)) + r'(?![\d])', triplet(dst), out)
    return out


def tape_svg(color, opacity):
    """A strip of paper tape laid diagonally across a corner, torn ends."""
    length, width, teeth = 46, 13, 5
    pts = [(-length / 2 + (2.2 if i % 2 else 0), -width / 2 + width * i / teeth) for i in range(teeth + 1)]
    pts += [(length / 2 - (2.2 if i % 2 else 0), width / 2 - width * i / teeth) for i in range(teeth + 1)]
    a = math.radians(-45)
    pts = [(22 + x * math.cos(a) - y * math.sin(a), 22 + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    d = 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + ' Z'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 44 44">'
            f'<path d="{d}" fill="#{color}" fill-opacity="{opacity}"/></svg>\n')


EMPTY_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 44 44"/>\n'

THEME_QML = '''pragma Singleton
import QtQuick
import "../logic/Preferences.js" as Preferences
QtObject {{
    property var preferences:Preferences.defaults()
    readonly property bool partyStripEnabled:false
    readonly property real fontScale:preferences.fontScale
    readonly property bool reduceMotion:preferences.reduceMotion
    function applicationSymbol(name) {{return /kitty|terminal|alacritty/i.test(name) ? "terminal" : /dolphin|files/i.test(name) ? "folder" : /browser|firefox|zen/i.test(name) ? "browser" : /music|spotify/i.test(name) ? "music" : "windows";}}
    function fontSize(pixels) {{return Math.max(9,Math.round(pixels*fontScale));}}
    function duration(milliseconds) {{return reduceMotion ? 0 : milliseconds;}}
    // Gravity Falls: a dusk forest town. What you point at warms up, as if a
    // lamp or flashlight found it; the accent is the orange of the old sign.
    readonly property color background:Qt.rgba({r:.3f},{g:.3f},{b:.3f},preferences.surfaceOpacity)
    readonly property color raised:"#{raised}"
    readonly property color ink:"#{ink}"
    readonly property color muted:"#{muted}"
    readonly property color brass:"#{accent}"
    readonly property color line:"#{line}"
    readonly property color danger:"#{danger}"
    readonly property color selectedSurface:"#{selected}"
    readonly property color activeWorkspaceSurface:"#{active}"
    readonly property color inputSurface:"#{deep}"
    readonly property color panelScrim:"#10{bg}"
    readonly property color switcherScrim:"#b0{bg}"
    readonly property color previewStatusSurface:"#ed{bg}"
    readonly property color partyPink:"#{accent}"
    readonly property color partyGreen:"#{pine}"
    // Journal voice: typewriter (clock, headings). System voice: desktop sans-serif.
    readonly property FontLoader loadedFont:FontLoader {{source:Qt.resolvedUrl("../assets/courier-prime-regular.ttf")}}
    readonly property FontLoader loadedBold:FontLoader {{source:Qt.resolvedUrl("../assets/courier-prime-bold.ttf")}}
    readonly property string displayFont:loadedFont.status===FontLoader.Ready ? loadedFont.name : "monospace"
    readonly property string bodyFont:"sans-serif"
    readonly property int quickMotion:110
    readonly property int panelEnterMotion:140
    readonly property int ornamentSize:44
    readonly property url wallpaper:Qt.resolvedUrl("../assets/wallpaper.png")
    readonly property url kris:Qt.resolvedUrl("../assets/kris.png")
    readonly property url susie:Qt.resolvedUrl("../assets/susie.png")
    readonly property url ralsei:Qt.resolvedUrl("../assets/ralsei.png")
    readonly property url cornerTopLeft:Qt.resolvedUrl("../assets/tl.svg")
    readonly property url cornerTopRight:Qt.resolvedUrl("../assets/tr.svg")
    readonly property url cornerBottomLeft:Qt.resolvedUrl("../assets/bl.svg")
    readonly property url cornerBottomRight:Qt.resolvedUrl("../assets/br.svg")
    function portraitFor(symbol) {{return symbol==="music" || symbol==="power" ? susie : symbol==="search" || symbol==="bell" ? ralsei : kris;}}
}}
'''

ORNAMENT_QML = '''import QtQuick
// A journal page: plain panel with two strips of paper tape on opposite corners.
Item {
    id:root
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    Rectangle {anchors.fill:parent;radius:4;color:root.fillColor;border.width:1;border.color:root.frameColor}
    Image {x:-14;y:-14;width:Theme.ornamentSize;height:width;source:Theme.cornerTopLeft;sourceSize:Qt.size(width*2,height*2)}
    Image {x:parent.width-width+14;y:parent.height-height+14;width:Theme.ornamentSize;height:width;source:Theme.cornerBottomRight;sourceSize:Qt.size(width*2,height*2)}
}
'''

BAR_QML = '''import QtQuick
import "../surfaces"
BarSurface {
    clockSize:17;workspaceRadius:1
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:1;color:Theme.line}
    }}
}
'''

KITTY = f'''# Gravity Falls dusk palette; no prompt or terminal startup changes.
foreground #{P['ink']}
background #{P['bg']}
selection_foreground #{P['ink']}
selection_background #{P['selected']}
cursor #{P['accent']}
url_color #{P['pine']}
active_border_color #{P['accent']}
inactive_border_color #{P['line']}
color0 #{P['card']}
color1 #e0574a
color2 #8fb87a
color3 #f0a84a
color4 #6f9fc0
color5 #b48ad6
color6 #6fb3a8
color7 #e8dccb
color8 #6e5a50
color9 #f27a6b
color10 #b2d69a
color11 #ffd08a
color12 #9cc3dc
color13 #cfa9ec
color14 #9fd6cc
color15 #fff6e6
'''

APPEARANCE = f'''hl.config({{
    general = {{
        gaps_in = 5,
        gaps_out = 14,
        border_size = 2,
        col = {{
            active_border = {{ colors = {{ "rgba({P['accent']}ff)", "rgba({P['accent_deep']}ff)" }}, angle = 45 }},
            inactive_border = "rgba({P['line']}aa)",
        }},
        resize_on_border = false,
        allow_tearing = false,
        layout = "dwindle",
    }},
    decoration = {{
        rounding = 6,
        rounding_power = 2,
        active_opacity = 1.0,
        inactive_opacity = 1.0,
        shadow = {{
            enabled = false,
            range = 0,
            render_power = 3,
            color = 0x66{P['bg']},
        }},
        blur = {{ enabled = false, size = 3, passes = 1 }},
    }},
}})
'''

LAYOUT = f'''background {{
    monitor =
    path = @STYLE@/wallpaper.png
    blur_passes = 0
    brightness = 0.55
}}
label {{
    monitor =
    text = $TIME
    color = rgb({P['ink']})
    font_family = monospace
    font_size = 42
    position = 48, -44
    halign = left
    valign = top
}}
label {{
    monitor =
    text = cmd[update:60000] date '+%d %B %Y'
    color = rgb({P['muted']})
    font_family = monospace
    font_size = 10
    position = 50, -108
    halign = left
    valign = top
}}
# Caesar +3. Shift every letter three back to read it.
label {{
    monitor =
    text = {CIPHER}
    color = rgb({P['accent']})
    font_family = monospace
    font_size = 11
    position = 0, 168
    halign = center
    valign = bottom
}}
input-field {{
    monitor =
    size = 350, 52
    position = 0, 100
    halign = center
    valign = bottom
    outline_thickness = 1
    rounding = 6
    outer_color = rgb({P['accent']})
    inner_color = rgba({P['bg']}f2)
    font_color = rgb({P['ink']})
    font_family = monospace
    dots_center = true
    fade_on_empty = false
    placeholder_text = <span foreground="#{P['muted']}">Password</span>
    check_color = rgb({P['accent']})
    check_text = Checking…
    fail_color = rgb({P['danger']})
    fail_text = Try again
}}
'''

# An original terminal medallion: three pines under a moon. No show emblem.
MEDALLION = r'''$1
$1                        ▄▄▄
$1                       █████
$1                        ▀▀▀
$1         ▄█▄                          ▄█▄
$1        ▄███▄           ▄█▄          ▄███▄
$1       ▄█████▄         ▄███▄        ▄█████▄
$1      ▄███████▄       ▄█████▄      ▄███████▄
$1     ▄█████████▄     ▄███████▄    ▄█████████▄
$1    ▄███████████▄   ▄█████████▄  ▄███████████▄
$1          ██             ██            ██
$1    ════════════════════════════════════════
$1        WKH ZRRGV UHPHPEHU ZKDW WKH
$1                WRZQ IRUJHWV.
'''
MEDALLION_COMPACT = r'''$1
$1                ▄▄
$1               ▀██▀
$1      ▄█▄              ▄█▄
$1     ▄███▄     ▄█▄    ▄███▄
$1    ▄█████▄   ▄███▄  ▄█████▄
$1   ▄███████▄ ▄█████▄▄███████▄
$1       ██       ██      ██
$1   ══════════════════════════
$1      WKH ZRRGV UHPHPEHU
'''


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.write_bytes if isinstance(data, bytes) else path.write_text)(data)


def svg_to_png(svg_text, size):
    from PySide6.QtCore import QByteArray, Qt
    from PySide6.QtGui import QGuiApplication, QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer
    import os
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    QGuiApplication.instance() or QGuiApplication(['build'])
    image = QImage(size, size, QImage.Format_ARGB32)
    image.fill(Qt.transparent)
    painter = QPainter(image)
    QSvgRenderer(QByteArray(svg_text.encode())).render(painter)
    painter.end()
    buffer = io.BytesIO()
    Image.frombytes('RGBA', (size, size), bytes(image.constBits()), 'raw', 'BGRA').save(buffer, 'PNG', optimize=True)
    return buffer.getvalue()


def quote_png(font_path):
    """Palette PNG whose index equals alpha; fastfetch_quotes tints the palette."""
    width, height, size = 1536, 1280, 118
    font = ImageFont.truetype(str(font_path), size)
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    line_height = int(size * 1.25)
    top = (height - line_height * len(CIPHER_LINES)) // 2
    for i, line in enumerate(CIPHER_LINES):
        w = draw.textlength(line, font=font)
        draw.text(((width - w) / 2, top + i * line_height), line, font=font, fill=255)
    image = mask.convert('P') if False else Image.frombytes('P', mask.size, mask.tobytes())
    image.putpalette(bytes(768))
    buffer = io.BytesIO()
    image.save(buffer, 'PNG', transparency=bytes(range(256)), optimize=False)
    return buffer.getvalue(), list(mask.getbbox()), size


def main():
    source_jpeg, regular, bold, license_path = map(Path, sys.argv[1:5])
    frost = ROOT / 'themes/deltarune-snowgrave'
    dest = ROOT / 'themes' / TID
    kept_preview = (dest / 'preview.png').read_bytes() if (dest / 'preview.png').is_file() else None
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(frost, dest)
    if kept_preview is not None:  # keep the real render made by checks/render_theme.py
        write(dest / 'preview.png', kept_preview)
    for name in ('palette.json', 'restoration.json', 'restoration-autumn-0.1.0.json', 'manifest.json'):
        (dest / name).unlink(missing_ok=True)

    # 1. Recolour every Frost text asset; keep structure and behaviour.
    for path in dest.rglob('*'):
        if path.is_file() and path.suffix in ('.qml', '.svg', '.conf', '.ini', '.css', '.colors', '.theme', '.lua'):
            text = path.read_text()
            write(path, remap(text))
    leftovers = []
    for path in dest.rglob('*'):
        if path.is_file() and path.suffix in ('.qml', '.svg', '.conf', '.ini', '.css', '.colors', '.theme', '.lua'):
            if FROST_LEFTOVERS.search(path.read_text()):
                leftovers.append(str(path))
    assert not leftovers, leftovers

    # 2. Theme-specific files.
    ui = dest / 'files/style/shell/ui'
    assets = dest / 'files/style/shell/assets'
    bg = [int(P['bg'][i:i + 2], 16) / 255 for i in (0, 2, 4)]
    write(ui / 'Theme.qml', THEME_QML.format(r=bg[0], g=bg[1], b=bg[2], **P))
    write(ui / 'OrnamentFrame.qml', ORNAMENT_QML)
    write(ui / 'Bar.qml', BAR_QML)
    write(assets / 'tl.svg', tape_svg(P['ink'], 0.55))
    write(assets / 'br.svg', tape_svg(P['ink'], 0.55))
    write(assets / 'tr.svg', EMPTY_SVG)
    write(assets / 'bl.svg', EMPTY_SVG)
    for target in ('courier-prime-regular.ttf', 'courier-prime-bold.ttf'):
        shutil.copy(regular if 'regular' in target else bold, assets / target)
        shutil.copy(regular if 'regular' in target else bold, dest / 'adapters/sddm' / target)
    shutil.copy(license_path, assets / 'courier-prime-license.txt')
    shutil.copy(license_path, dest / 'adapters/sddm/COURIER-PRIME-LICENSE.txt')
    write(dest / 'files/style/kitty/theme.conf', KITTY)
    write(dest / 'files/hypr/appearance.lua', APPEARANCE)
    write(dest / 'files/style/hyprlock/layout.conf', LAYOUT)

    # SDDM: same login controller, dusk colours, typewriter clock, tape corners.
    skin = (dest / 'adapters/sddm/LoginSkin.qml').read_text()
    skin = skin.replace('Qt.resolvedUrl("departure-mono.otf")', 'Qt.resolvedUrl("courier-prime-regular.ttf")')
    skin = skin.replace('readonly property string bodyFont:displayFont', 'readonly property string bodyFont:"sans-serif"')
    skin = skin.replace('readonly property int cornerSize:36', 'readonly property int cornerSize:44')
    write(dest / 'adapters/sddm/LoginSkin.qml', skin)
    (dest / 'adapters/sddm/departure-mono.otf').unlink()
    (dest / 'adapters/sddm/FONT-LICENSE.txt').unlink()
    for corner in ('tl', 'br'):
        write(dest / 'adapters/sddm' / (corner + '.svg'), tape_svg(P['ink'], 0.55))
    for corner in ('tr', 'bl'):
        write(dest / 'adapters/sddm' / (corner + '.svg'), EMPTY_SVG)

    # Dolphin names.
    index = dest / 'adapters/dolphin/icons/index.theme'
    write(index, re.sub(r'(?m)^Name=.*$', 'Name=Gravity Falls Dusk', re.sub(
        r'(?m)^Comment=.*$', 'Comment=Dusk-coloured folders with lamp-orange outlines with inherited application and action icons',
        index.read_text())))
    colors = dest / 'adapters/dolphin/DesktopStyle.colors'
    write(colors, re.sub(r'(?m)^Name=.*$', 'Name=Gravity Falls Dusk', colors.read_text()))
    qt = dest / 'adapters/dolphin/Qt.conf'
    write(qt, re.sub(r'(?m)^Name=.*$', 'Name=Gravity Falls Dusk', qt.read_text()))

    # Hyprlock media buttons from the recoloured SVG sources.
    for name in ('next', 'play', 'pause', 'previous'):
        write(dest / 'files/style/hyprlock' / (name + '.png'), svg_to_png((dest / (name + '.svg')).read_text(), 36))

    # Terminal medallion (text fallback) and its CP437 twin.
    for name, art in (('medallion', MEDALLION), ('medallion-compact', MEDALLION_COMPACT)):
        art = art.lstrip('\n')
        write(dest / 'adapters/terminal' / (name + '.txt'), art)
        write(dest / 'adapters/terminal' / (name + '.cp437'),
              art.replace('$1', '').replace('\n', '\r\n').encode('cp437'))

    # Wallpaper: the user's image, unchanged colours, stored losslessly.
    source = Image.open(source_jpeg).convert('RGB')
    buffer = io.BytesIO()
    source.save(buffer, 'PNG', optimize=True)
    for target in ('files/style/wallpaper.png', 'files/style/shell/assets/wallpaper.png',
                   'files/style/hyprlock/cover.png', 'adapters/sddm/wallpaper.png'):
        write(dest / target, buffer.getvalue())
    shutil.copy(source_jpeg, dest / 'wallpaper-source.jpeg')
    write(dest / 'provenance.json', json.dumps({
        'wallpaper': 'User-supplied image (2026-10-27); third-party fan render, licence unknown, colours unchanged',
        'wallpaperSourceSha256': hashlib.sha256(source_jpeg.read_bytes()).hexdigest(),
        'cipher': {'method': 'Caesar +3', 'plain': PLAIN, 'text': CIPHER},
        'fonts': {'Courier Prime': 'SIL OFL 1.1, The Courier Prime Project Authors (npm @fontsource/courier-prime 5.3.0, latin subset, WOFF2 converted to TTF)'},
    }, indent=2) + '\n')

    # Fastfetch cipher image + manifest row.
    data, bounds, size = quote_png(regular)
    write(ROOT / 'fastfetch-quotes' / (TID + '.png'), data)
    manifest = json.loads((ROOT / 'fastfetch-quotes/manifest.json').read_text())
    manifest['assets'][TID] = {
        'sha256': hashlib.sha256(data).hexdigest(), 'text': CIPHER, 'lines': list(CIPHER_LINES),
        'font': 'Courier Prime', 'fontSha256': hashlib.sha256(regular.read_bytes()).hexdigest(),
        'fontSize': size, 'inkBounds': bounds,
    }
    write(ROOT / 'fastfetch-quotes/manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')

    # Package manifest (preview.png is replaced by a real render afterwards).
    base = json.loads((frost / 'manifest.json').read_text())
    files = [e for e in base['files']]
    for name in ('courier-prime-regular.ttf', 'courier-prime-bold.ttf', 'courier-prime-license.txt'):
        files.append({'source': 'files/style/shell/assets/' + name, 'target': 'style/shell/assets/' + name})
    for entry in files:
        entry['gitBlob'] = git_blob((dest / entry['source']).read_bytes())
    manifest = dict(base, id=TID, name=NAME, version=VERSION, files=files,
                    preview={'source': 'preview.png', 'gitBlob': git_blob((dest / 'preview.png').read_bytes())})
    write(dest / 'manifest.json', json.dumps(manifest, indent=2) + '\n')
    print('built', TID, len(files), 'files; cipher:', CIPHER)


if __name__ == '__main__':
    main()
