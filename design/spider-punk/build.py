#!/usr/bin/env python3
"""Generate the spider-punk theme package (Zine variant) from Snowgrave Frost's structure.

Usage: python3 design/spider-punk/build.py WALLPAPER_JPEG PERMANENT_MARKER_TTF PERMANENT_MARKER_LICENSE
Re-running regenerates the package and its Fastfetch image; a real preview.png is kept.
"""
import hashlib
import io
import json
import os
import re
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from theme_core import git_blob  # noqa: E402

TID = 'spider-punk'
NAME = 'Spider-Punk'
VERSION = '0.1.0'
QUOTE_LINES = ('BREAK THE', 'CANON.')

# Zine palette: photocopy paper, black ink, two misregistered inks (pink, cyan).
P = dict(
    paper='ece8de', paper_deep='e2ddd1', card='e4dfd3', raised='f4dce2', neutral='ddd7ca',
    button='d6cfc0', button2='d0c9b9', selected='f2a9bb', line='b9b3a6', mid='8a857b',
    muted='5c5850', ink='111111', pink='e8285a', pink_light='ff6f91', cyan='2fb3e8',
    danger='c2410c', green='2e7d4f', violet='6b5fa8', input='f7f4ec',
)
# Frost colour -> zine role (Frost is dark; roles flip to paper and ink)
MAP = {
    '0b1421': P['paper'], '091421': P['paper'], '070f1a': P['paper_deep'], '102236': P['card'],
    '162d45': P['neutral'], '19394f': P['button'], '1b3852': P['button2'], '224c6b': P['selected'],
    '2c6080': P['selected'], '365873': P['line'], '6f94b4': P['mid'], '9fb8d0': P['muted'],
    '5a9cc7': P['cyan'], '9cdfff': P['pink'], 'd6f3ff': P['pink_light'], 'edf7ff': P['ink'],
    'd9f0ff': P['ink'], 'e68a9d': P['danger'], 'b6e9e5': P['green'], 'b9d8ef': P['violet'],
    'd4eaff': P['violet'], 'ffffff': P['ink'],
}
# Working apps (Dolphin, Spotify) are black photocopies: white text stays white,
# a project rule for Dolphin, and long sessions are easier on dark surfaces.
XEROX = {
    '0b1421': '111111', '091421': '111111', '070f1a': '0a0a0a', '102236': '1a1a1a',
    '162d45': '262626', '19394f': '2e2e2e', '1b3852': '333333', '224c6b': '4a1a28',
    '2c6080': '4a1a28', '365873': '3a3a3a', '6f94b4': '7a766e', '9fb8d0': 'a09c94',
    '5a9cc7': P['cyan'], '9cdfff': P['pink'], 'd6f3ff': P['pink_light'], 'edf7ff': 'eeeae0',
    'd9f0ff': 'eeeae0', 'e68a9d': 'ffb020', 'b6e9e5': '6cc070', 'b9d8ef': 'a77ad8', 'd4eaff': 'a77ad8',
}
PATTERN = re.compile('|'.join(MAP), re.I)
TRIPLETS = {'205,205,205': '92,88,80'}


def triplet(h):
    return ','.join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def remap(text, table=None):
    table = table or MAP
    pattern = re.compile('|'.join(table), re.I)
    # SDDM skin property names look like colours (e.g. cffffff); never rename them.
    names = {}
    def hide(m):
        names[f'@@{len(names)}@@'] = m.group(0)
        return f'@@{len(names) - 1}@@'
    text = re.sub(r'property color c[0-9a-f]{6,8}\b', hide, text)
    out = pattern.sub(lambda m: table[m.group(0).lower()], text)
    for key, value in names.items():
        out = out.replace(key, value)
    for src, dst in list(table.items()) + [(None, None)]:
        if src is None:
            break
        out = re.sub(r'(?<![\d,])' + re.escape(triplet(src)) + r'(?![\d])', triplet(dst), out)
    for src, dst in (TRIPLETS if table is MAP else {}).items():
        out = re.sub(r'(?<![\d,])' + re.escape(src) + r'(?![\d])', dst, out)
    return out


EMPTY_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 8 8"/>\n'

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
    // Spider-Punk zine: photocopy paper and black ink. Panels are torn paper
    // printed slightly out of register: a cyan layer peeks out behind each one.
    readonly property color background:Qt.rgba({r:.3f},{g:.3f},{b:.3f},preferences.surfaceOpacity)
    readonly property color raised:"#{raised}"
    readonly property color ink:"#{ink}"
    readonly property color muted:"#{muted}"
    readonly property color brass:"#{pink}"
    readonly property color line:"#{line}"
    readonly property color danger:"#{danger}"
    readonly property color selectedSurface:"#{selected}"
    readonly property color activeWorkspaceSurface:"#{selected}"
    readonly property color inputSurface:"#{input}"
    readonly property color offsetInk:"#{cyan}"
    readonly property color panelScrim:"#10{paper}"
    readonly property color switcherScrim:"#b0{paper}"
    readonly property color previewStatusSurface:"#ed{paper}"
    readonly property color partyPink:"#{pink}"
    readonly property color partyGreen:"#{cyan}"
    // Marker voice: clock and headings. System voice: desktop sans-serif.
    readonly property FontLoader loadedFont:FontLoader {{source:Qt.resolvedUrl("../assets/permanent-marker.ttf")}}
    readonly property string displayFont:loadedFont.status===FontLoader.Ready ? loadedFont.name : "sans-serif"
    readonly property string bodyFont:"sans-serif"
    readonly property int quickMotion:110
    readonly property int panelEnterMotion:140
    readonly property int ornamentSize:0
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
// Torn paper panel, printed with a second (cyan) ink layer slightly out of register.
// Static: repaints only when the panel size or colour changes.
Item {
    id:root
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    onFillColorChanged:paper.requestPaint()
    Canvas {
        id:paper
        x:-8;y:-8;width:root.width+16;height:root.height+16
        antialiasing:true
        onWidthChanged:requestPaint()
        onHeightChanged:requestPaint()
        function tear(c,ox,oy,w,h,seed) {
            // deterministic jagged outline: the same panel size tears the same way
            function j(i) {const v=Math.sin(i*12.9898+seed*78.233)*43758.5453;return (v-Math.floor(v))*3.2-1.6;}
            const step=7;let i=0;
            c.beginPath();c.moveTo(ox,oy+j(i++));
            for(let x=step;x<w;x+=step)c.lineTo(ox+x,oy+j(i++));
            c.lineTo(ox+w+j(i++),oy);
            for(let y=step;y<h;y+=step)c.lineTo(ox+w+j(i++),oy+y);
            c.lineTo(ox+w,oy+h+j(i++));
            for(let x=w-step;x>0;x-=step)c.lineTo(ox+x,oy+h+j(i++));
            c.lineTo(ox+j(i++),oy+h);
            for(let y=h-step;y>0;y-=step)c.lineTo(ox+j(i++),oy+y);
            c.closePath();
        }
        onPaint: {
            const c=getContext("2d");c.reset();
            const w=root.width,h=root.height;
            tear(c,8+5,8+5,w,h,7);c.fillStyle=Theme.offsetInk;c.fill();
            tear(c,8,8,w,h,3);c.fillStyle=root.fillColor;c.fill();
        }
    }
}
'''

BAR_QML = '''import QtQuick
import "../surfaces"
// Paper strip with a pink rule and its cyan misprint underneath.
BarSurface {
    clockSize:19;workspaceRadius:0
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:3;color:Theme.brass}
        Rectangle {anchors.bottom:parent.bottom;anchors.bottomMargin:-3;width:parent.width;height:3;color:Theme.offsetInk}
    }}
}
'''

# Terminal stays black photocopy ink: easier on the eyes than a paper terminal.
KITTY = f'''# Spider-Punk: black photocopy terminal with pink/cyan inks; no prompt changes.
foreground #eeeae0
background #111111
selection_foreground #111111
selection_background #{P['pink']}
cursor #{P['pink']}
url_color #{P['cyan']}
active_border_color #{P['pink']}
inactive_border_color #3a3a3a
color0 #1c1c1c
color1 #e8285a
color2 #6cc070
color3 #e6d84a
color4 #2fb3e8
color5 #a77ad8
color6 #4fd1c5
color7 #d8d4ca
color8 #5c5850
color9 #ff6f91
color10 #9be39f
color11 #fff27a
color12 #7fd4f5
color13 #cba6f0
color14 #8ee8df
color15 #ffffff
'''

APPEARANCE = f'''hl.config({{
    general = {{
        gaps_in = 5,
        gaps_out = 14,
        border_size = 2,
        col = {{
            active_border = {{ colors = {{ "rgba({P['pink']}ff)", "rgba({P['cyan']}ff)" }}, angle = 45 }},
            inactive_border = "rgba({P['muted']}aa)",
        }},
        resize_on_border = false,
        allow_tearing = false,
        layout = "dwindle",
    }},
    decoration = {{
        rounding = 2,
        rounding_power = 2,
        active_opacity = 1.0,
        inactive_opacity = 1.0,
        shadow = {{
            enabled = false,
            range = 0,
            render_power = 3,
            color = 0x66111111,
        }},
        blur = {{ enabled = false, size = 3, passes = 1 }},
    }},
}})
'''

# Clock, date and the line sit on a paper plate with a cyan misprint behind it.
LAYOUT = f'''background {{
    monitor =
    path = @STYLE@/wallpaper.png
    blur_passes = 0
    brightness = 0.85
}}
shape {{
    monitor =
    size = 400, 170
    position = 47, -37
    halign = left
    valign = top
    color = rgb({P['cyan']})
    rounding = 0
    border_size = 0
    zindex = 0
}}
shape {{
    monitor =
    size = 400, 170
    position = 40, -30
    halign = left
    valign = top
    color = rgba({P['paper']}f5)
    rounding = 0
    border_size = 0
    zindex = 1
}}
label {{
    monitor =
    text = $TIME
    color = rgb({P['ink']})
    font_family = sans-serif
    font_size = 42
    position = 60, -44
    halign = left
    valign = top
    zindex = 2
}}
label {{
    monitor =
    text = cmd[update:60000] date '+%d %B %Y'
    color = rgb({P['muted']})
    font_family = sans-serif
    font_size = 10
    position = 62, -108
    halign = left
    valign = top
    zindex = 2
}}
label {{
    monitor =
    text = {' '.join(QUOTE_LINES)}
    color = rgb({P['pink']})
    font_family = sans-serif
    font_size = 14
    position = 62, -138
    halign = left
    valign = top
    zindex = 2
}}
input-field {{
    monitor =
    size = 350, 52
    position = 0, 100
    halign = center
    valign = bottom
    outline_thickness = 2
    rounding = 0
    outer_color = rgb({P['pink']})
    inner_color = rgba({P['paper']}f5)
    font_color = rgb({P['ink']})
    font_family = monospace
    dots_center = true
    fade_on_empty = false
    placeholder_text = <span foreground="#{P['muted']}">Password</span>
    check_color = rgb({P['cyan']})
    check_text = Checking…
    fail_color = rgb({P['danger']})
    fail_text = Try again
}}
'''

# Original terminal medallion: a jagged lightning bolt. No character or emblem.
MEDALLION = r'''$1
$1                  ▄▄▄▄▄▄▄▄▄▄
$1                 ██████████▀
$1                ████████▀
$1               ███████▀
$1              ██████▄▄▄▄▄▄▄
$1               ▀▀▀▀████████▀
$1                   ███████▀
$1                  █████▀
$1                 ████▀
$1                ███▀
$1               ██▀
$1              ▀
$1         B R E A K   T H E   C A N O N .
'''
MEDALLION_COMPACT = r'''$1
$1            ▄▄▄▄▄▄▄
$1           ██████▀
$1          █████▀
$1         █████▄▄▄▄
$1          ▀▀▀█████▀
$1             ███▀
$1            ██▀
$1           ▀
$1      BREAK THE CANON.
'''


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.write_bytes if isinstance(data, bytes) else path.write_text)(data)


def svg_to_png(svg_text, size):
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    from PySide6.QtCore import QByteArray, Qt
    from PySide6.QtGui import QGuiApplication, QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer
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
    width, height, size = 1536, 1280, 230
    font = ImageFont.truetype(str(font_path), size)
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    line_height = int(size * 1.15)
    top = (height - line_height * len(QUOTE_LINES)) // 2
    for i, line in enumerate(QUOTE_LINES):
        w = draw.textlength(line, font=font)
        draw.text(((width - w) / 2, top + i * line_height), line, font=font, fill=255)
    image = Image.frombytes('P', mask.size, mask.tobytes())
    image.putpalette(bytes(768))
    buffer = io.BytesIO()
    image.save(buffer, 'PNG', transparency=bytes(range(256)), optimize=False)
    return buffer.getvalue(), list(mask.getbbox()), size


def main():
    source_jpeg, marker, license_path = map(Path, sys.argv[1:4])
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

    text_types = ('.qml', '.svg', '.conf', '.ini', '.css', '.colors', '.theme', '.lua')
    for path in dest.rglob('*'):
        if path.is_file() and path.suffix in text_types:
            dark = any(part in path.parts for part in ('dolphin', 'spotify'))
            write(path, remap(path.read_text(), XEROX if dark else None))
    leftovers = [str(p) for p in dest.rglob('*') if p.is_file() and p.suffix in text_types
                 and re.search('|'.join(k for k in XEROX), p.read_text(), re.I)]
    assert not leftovers, leftovers

    ui = dest / 'files/style/shell/ui'
    assets = dest / 'files/style/shell/assets'
    bg = [int(P['paper'][i:i + 2], 16) / 255 for i in (0, 2, 4)]
    write(ui / 'Theme.qml', THEME_QML.format(r=bg[0], g=bg[1], b=bg[2], **P))
    write(ui / 'OrnamentFrame.qml', ORNAMENT_QML)
    write(ui / 'Bar.qml', BAR_QML)
    for corner in ('tl', 'tr', 'bl', 'br'):
        write(assets / (corner + '.svg'), EMPTY_SVG)
        write(dest / 'adapters/sddm' / (corner + '.svg'), EMPTY_SVG)
    shutil.copy(marker, assets / 'permanent-marker.ttf')
    shutil.copy(license_path, assets / 'permanent-marker-license.txt')
    shutil.copy(marker, dest / 'adapters/sddm/permanent-marker.ttf')
    shutil.copy(license_path, dest / 'adapters/sddm/PERMANENT-MARKER-LICENSE.txt')
    write(dest / 'files/style/kitty/theme.conf', KITTY)
    write(dest / 'files/hypr/appearance.lua', APPEARANCE)
    write(dest / 'files/style/hyprlock/layout.conf', LAYOUT)

    skin = (dest / 'adapters/sddm/LoginSkin.qml').read_text()
    for old, new in (('Qt.resolvedUrl("departure-mono.otf")', 'Qt.resolvedUrl("permanent-marker.ttf")'),
                     ('readonly property string bodyFont:displayFont', 'readonly property string bodyFont:"sans-serif"'),
                     ('readonly property int cornerSize:36', 'readonly property int cornerSize:8')):
        assert old in skin, old
        skin = skin.replace(old, new)
    write(dest / 'adapters/sddm/LoginSkin.qml', skin)
    (dest / 'adapters/sddm/departure-mono.otf').unlink()
    (dest / 'adapters/sddm/FONT-LICENSE.txt').unlink()

    index = dest / 'adapters/dolphin/icons/index.theme'
    text = re.sub(r'(?m)^Name=.*$', 'Name=Spider-Punk Xerox', index.read_text())
    text = re.sub(r'(?m)^Comment=.*$', 'Comment=Black photocopy folders with pink ink outlines with inherited application and action icons', text)
    write(index, text)
    colors = dest / 'adapters/dolphin/DesktopStyle.colors'
    write(colors, re.sub(r'(?m)^Name=.*$', 'Name=Spider-Punk Xerox', colors.read_text()))
    qt = dest / 'adapters/dolphin/Qt.conf'
    write(qt, re.sub(r'(?m)^Name=.*$', 'Name=Spider-Punk Xerox', qt.read_text()))

    for name in ('next', 'play', 'pause', 'previous'):
        write(dest / 'files/style/hyprlock' / (name + '.png'), svg_to_png((dest / (name + '.svg')).read_text(), 36))

    for name, art in (('medallion', MEDALLION), ('medallion-compact', MEDALLION_COMPACT)):
        art = art.lstrip('\n')
        write(dest / 'adapters/terminal' / (name + '.txt'), art)
        write(dest / 'adapters/terminal' / (name + '.cp437'), art.replace('$1', '').replace('\n', '\r\n').encode('cp437'))

    source = Image.open(source_jpeg).convert('RGB')
    buffer = io.BytesIO()
    source.save(buffer, 'PNG', optimize=True)
    for target in ('files/style/wallpaper.png', 'files/style/shell/assets/wallpaper.png',
                   'files/style/hyprlock/cover.png', 'adapters/sddm/wallpaper.png'):
        write(dest / target, buffer.getvalue())
    shutil.copy(source_jpeg, dest / 'wallpaper-source.jpeg')
    write(dest / 'provenance.json', json.dumps({
        'wallpaper': 'User-supplied image (2026-10-28); third-party artwork, licence unknown, colours unchanged',
        'wallpaperSourceSha256': hashlib.sha256(source_jpeg.read_bytes()).hexdigest(),
        'quote': {'text': ' '.join(QUOTE_LINES), 'note': 'Original line, not a film quote'},
        'fonts': {'Permanent Marker': 'Apache License 2.0, Font Diner (npm @fontsource/permanent-marker 5.3.0, latin subset, WOFF2 converted to TTF)'},
    }, indent=2) + '\n')

    data, bounds, size = quote_png(marker)
    write(ROOT / 'fastfetch-quotes' / (TID + '.png'), data)
    manifest = json.loads((ROOT / 'fastfetch-quotes/manifest.json').read_text())
    manifest['assets'][TID] = {
        'sha256': hashlib.sha256(data).hexdigest(), 'text': ' '.join(QUOTE_LINES), 'lines': list(QUOTE_LINES),
        'font': 'Permanent Marker', 'fontSha256': hashlib.sha256(marker.read_bytes()).hexdigest(),
        'fontSize': size, 'inkBounds': bounds,
    }
    write(ROOT / 'fastfetch-quotes/manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')

    base = json.loads((frost / 'manifest.json').read_text())
    files = [dict(e) for e in base['files']]
    for name in ('permanent-marker.ttf', 'permanent-marker-license.txt'):
        files.append({'source': 'files/style/shell/assets/' + name, 'target': 'style/shell/assets/' + name})
    for entry in files:
        entry['gitBlob'] = git_blob((dest / entry['source']).read_bytes())
    manifest = dict(base, id=TID, name=NAME, version=VERSION, files=files,
                    preview={'source': 'preview.png', 'gitBlob': git_blob((dest / 'preview.png').read_bytes())})
    write(dest / 'manifest.json', json.dumps(manifest, indent=2) + '\n')
    print('built', TID, len(files), 'files')


if __name__ == '__main__':
    main()
