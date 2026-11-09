#!/usr/bin/env python3
"""Generate the treasure-planet theme package (Nebula) from Snowgrave Frost's structure.

Usage: python3 design/treasure-planet/build.py WALLPAPER_JPEG CINZEL_TTF CINZEL_LICENSE
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

TID = 'treasure-planet'
NAME = 'Treasure Planet'
VERSION = '0.1.0'
QUOTE_LINES = ('CHART YOUR', 'OWN COURSE.')

# Nebula palette: deep etherium blue, pale turquoise accent, silver ship fittings.
# No yellow anywhere (user choice). Shell panels 88% opaque; apps opaque.
P = dict(
    bg='0b1d28', app='0e2230', deep='08161f', card='10283a', raised_app='163246', button='1a3a50',
    button2='1e4258', selected_app='23506a', line_app='34586a', mid='6f93a3', muted='a3c2cf',
    ink='eef8ff', accent='7fe3ef', accent_light='c4f6fb', teal='4fb8c8', glow='5cf0b0', silver='b9cdd2',
    rule='34586a', danger='ff8a7a', green='8fe0b8', violet='a9b8f0',
)
ALPHA = 0.88
# Frost colour -> Nebula role (Dolphin keeps white text: project rule)
MAP = {
    '0b1421': P['app'], '091421': P['app'], '070f1a': P['deep'], '102236': P['card'],
    '162d45': P['raised_app'], '19394f': P['button'], '1b3852': P['button2'], '224c6b': P['selected_app'],
    '2c6080': P['selected_app'], '365873': P['line_app'], '6f94b4': P['mid'], '9fb8d0': P['muted'],
    '5a9cc7': P['teal'], '9cdfff': P['accent'], 'd6f3ff': P['accent_light'], 'edf7ff': P['ink'],
    'd9f0ff': P['ink'], 'e68a9d': P['danger'], 'b6e9e5': P['green'], 'b9d8ef': P['violet'], 'd4eaff': P['violet'],
}
PATTERN = re.compile('|'.join(MAP), re.I)
TRIPLETS = {}


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
    // Treasure Planet · Nebula: ship's navigation plates over the etherium. Pale
    // turquoise accent, silver fittings, ion green kept for small highlights.
    readonly property color background:Qt.rgba({r:.3f},{g:.3f},{b:.3f},{alpha}*preferences.surfaceOpacity)
    readonly property color raised:"#801a3646"
    readonly property color ink:"#{ink}"
    readonly property color muted:"#{muted}"
    readonly property color brass:"#{accent}"
    readonly property color line:"#90587f90"
    readonly property color danger:"#{danger}"
    readonly property color selectedSurface:"#b01a4a5e"
    readonly property color activeWorkspaceSurface:"#b01a4a5e"
    readonly property color inputSurface:"#c005121a"
    readonly property color glow:"#{glow}"
    readonly property color frame:"#{silver}"
    readonly property color brassDark:"#{rule}"
    readonly property color panelScrim:"#10{bg}"
    readonly property color switcherScrim:"#b0{app}"
    readonly property color previewStatusSurface:"#ed{app}"
    readonly property color partyPink:"#{accent}"
    readonly property color partyGreen:"#{glow}"
    // Chart lettering for clock and headings (Cinzel); system text stays sans-serif.
    readonly property FontLoader loadedFont:FontLoader {{source:Qt.resolvedUrl("../assets/cinzel.ttf")}}
    readonly property string displayFont:loadedFont.status===FontLoader.Ready ? loadedFont.name : "serif"
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
// Navigation plate: double rule, riveted silver corner brackets and a compass
// tick at the middle of each edge. Static; repaints only on resize.
Item {
    id:root
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    onFillColorChanged:plate.requestPaint()
    Rectangle {anchors.fill:parent;radius:3;color:root.fillColor}
    Canvas {
        id:plate
        anchors.fill:parent;anchors.margins:-3
        antialiasing:true
        onWidthChanged:requestPaint()
        onHeightChanged:requestPaint()
        onPaint: {
            const c=getContext("2d");c.reset();
            const w=width,h=height,o=3;
            c.strokeStyle=Theme.brassDark;c.lineWidth=1;
            c.strokeRect(o+.5,o+.5,w-2*o-1,h-2*o-1);
            c.strokeStyle=Theme.line;c.strokeRect(o+5.5,o+5.5,w-2*o-11,h-2*o-11);
            c.strokeStyle=Theme.frame;c.lineWidth=2;
            const L=22;
            for(const [x,y,dx,dy] of [[o,o,1,1],[w-o,o,-1,1],[o,h-o,1,-1],[w-o,h-o,-1,-1]]) {
                c.beginPath();c.moveTo(x+dx*L,y+dy*1);c.lineTo(x+dx*1,y+dy*1);c.lineTo(x+dx*1,y+dy*L);c.stroke();
                c.beginPath();c.arc(x+dx*7,y+dy*7,2.2,0,Math.PI*2);c.fillStyle=Theme.frame;c.fill();
            }
            c.lineWidth=1.5;
            for(const [x,y,dx,dy] of [[w/2,o,0,1],[w/2,h-o,0,-1],[o,h/2,1,0],[w-o,h/2,-1,0]]) {
                c.beginPath();c.moveTo(x,y);c.lineTo(x+dx*9,y+dy*9);c.stroke();
            }
        }
    }
}
'''

BAR_QML = '''import QtQuick
import "../surfaces"
// Glass strip with a silver rule and a darker rule beneath, like a ship's rail.
BarSurface {
    clockSize:19;workspaceRadius:2
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:2;color:Theme.frame}
        Rectangle {anchors.bottom:parent.bottom;anchors.bottomMargin:-4;width:parent.width;height:1;color:Theme.brassDark}
    }}
}
'''

# Terminal: opaque etherium blue, turquoise cursor; ANSI yellow softened to a pale lime.
KITTY = f'''# Treasure Planet: etherium blue terminal, turquoise cursor; no prompt changes.
foreground #{P['ink']}
background #{P['app']}
selection_foreground #{P['ink']}
selection_background #{P['selected_app']}
cursor #{P['accent']}
url_color #{P['glow']}
active_border_color #{P['accent']}
inactive_border_color #{P['line_app']}
color0 #17303f
color1 #ec6a6a
color2 #5cf0b0
color3 #d6f0a8
color4 #6fa8ef
color5 #b89cf0
color6 #7fe3ef
color7 #dbe8ee
color8 #4d6b7c
color9 #ff8a7a
color10 #9ff7d0
color11 #e8f8c8
color12 #a6c8f8
color13 #d4c4f8
color14 #c4f6fb
color15 #f6fcff
'''

APPEARANCE = f'''hl.config({{
    general = {{
        gaps_in = 5,
        gaps_out = 14,
        border_size = 2,
        col = {{
            active_border = {{ colors = {{ "rgba({P['accent']}ff)", "rgba({P['silver']}ff)" }}, angle = 45 }},
            inactive_border = "rgba({P['line_app']}aa)",
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
            color = 0x66{P['app']},
        }},
        blur = {{ enabled = false, size = 3, passes = 1 }},
    }},
}})
'''

# Clock, date and the line on a navigation plate: silver frame, turquoise rule.
LAYOUT = f'''background {{
    monitor =
    path = @STYLE@/wallpaper.png
    blur_passes = 0
    brightness = 0.85
}}
shape {{
    monitor =
    size = 420, 170
    position = 40, -30
    halign = left
    valign = top
    color = rgba({P['bg']}e6)
    rounding = 4
    border_size = 2
    border_color = rgb({P['silver']})
    zindex = 1
}}
shape {{
    monitor =
    size = 380, 2
    position = 60, -170
    halign = left
    valign = top
    color = rgb({P['accent']})
    rounding = 0
    border_size = 0
    zindex = 2
}}
label {{
    monitor =
    text = $TIME
    color = rgb({P['ink']})
    font_family = serif
    font_size = 42
    position = 62, -44
    halign = left
    valign = top
    zindex = 3
}}
label {{
    monitor =
    text = cmd[update:60000] date '+%d %B %Y'
    color = rgb({P['muted']})
    font_family = sans-serif
    font_size = 10
    position = 64, -108
    halign = left
    valign = top
    zindex = 3
}}
label {{
    monitor =
    text = {' '.join(QUOTE_LINES)}
    color = rgb({P['accent']})
    font_family = serif
    font_size = 14
    position = 64, -134
    halign = left
    valign = top
    zindex = 3
}}
input-field {{
    monitor =
    size = 350, 52
    position = 0, 100
    halign = center
    valign = bottom
    outline_thickness = 2
    rounding = 4
    outer_color = rgb({P['silver']})
    inner_color = rgba({P['bg']}e6)
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

# Original terminal medallion: a ringed planet and a far star. No character or ship design.
MEDALLION = r'''$1
$1                                    *
$1               ▄▄██████▄▄                .
$1         ═══▄██████████████▄════════
$1       ════██████████████████═══════
$1             ▀████████████▀
$1    .           ▀▀▀▀▀▀▀▀              ·
$1         *
$1        C H A R T   Y O U R
$1         O W N   C O U R S E .
'''
MEDALLION_COMPACT = r'''$1
$1             ▄▄████▄▄          *
$1        ══▄████████████▄═══
$1             ▀▀████▀▀
$1     CHART YOUR OWN COURSE.
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
    width, height, size = 1536, 1280, 190
    font = ImageFont.truetype(str(font_path), size)
    probe = ImageDraw.Draw(Image.new('L', (1, 1)))
    while max(probe.textlength(line, font=font) for line in QUOTE_LINES) > 1400:
        size -= 5
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
    source_jpeg, font_path, license_path = map(Path, sys.argv[1:4])
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
            write(path, remap(path.read_text()))
    leftovers = [str(p) for p in dest.rglob('*') if p.is_file() and p.suffix in text_types
                 and re.search('|'.join(MAP), p.read_text(), re.I)]
    assert not leftovers, leftovers

    ui = dest / 'files/style/shell/ui'
    assets = dest / 'files/style/shell/assets'
    bg = [int(P['bg'][i:i + 2], 16) / 255 for i in (0, 2, 4)]
    write(ui / 'Theme.qml', THEME_QML.format(r=bg[0], g=bg[1], b=bg[2], alpha=ALPHA, **P))
    write(ui / 'OrnamentFrame.qml', ORNAMENT_QML)
    write(ui / 'Bar.qml', BAR_QML)
    for corner in ('tl', 'tr', 'bl', 'br'):
        write(assets / (corner + '.svg'), EMPTY_SVG)
        write(dest / 'adapters/sddm' / (corner + '.svg'), EMPTY_SVG)
    shutil.copy(font_path, assets / 'cinzel.ttf')
    shutil.copy(license_path, assets / 'cinzel-license.txt')
    shutil.copy(font_path, dest / 'adapters/sddm/cinzel.ttf')
    shutil.copy(license_path, dest / 'adapters/sddm/CINZEL-LICENSE.txt')
    write(dest / 'files/style/kitty/theme.conf', KITTY)
    write(dest / 'files/hypr/appearance.lua', APPEARANCE)
    write(dest / 'files/style/hyprlock/layout.conf', LAYOUT)

    skin = (dest / 'adapters/sddm/LoginSkin.qml').read_text()
    for old, new in (('Qt.resolvedUrl("departure-mono.otf")', 'Qt.resolvedUrl("cinzel.ttf")'),
                     ('readonly property string bodyFont:displayFont', 'readonly property string bodyFont:"sans-serif"'),
                     ('readonly property int cornerSize:36', 'readonly property int cornerSize:6')):
        assert old in skin, old
        skin = skin.replace(old, new)
    write(dest / 'adapters/sddm/LoginSkin.qml', skin)
    (dest / 'adapters/sddm/departure-mono.otf').unlink()
    (dest / 'adapters/sddm/FONT-LICENSE.txt').unlink()

    index = dest / 'adapters/dolphin/icons/index.theme'
    text = re.sub(r'(?m)^Name=.*$', 'Name=Treasure Planet Nebula', index.read_text())
    text = re.sub(r'(?m)^Comment=.*$', 'Comment=Etherium blue folders with turquoise outlines with inherited application and action icons', text)
    write(index, text)
    colors = dest / 'adapters/dolphin/DesktopStyle.colors'
    write(colors, re.sub(r'(?m)^Name=.*$', 'Name=Treasure Planet Nebula', colors.read_text()))
    qt = dest / 'adapters/dolphin/Qt.conf'
    write(qt, re.sub(r'(?m)^Name=.*$', 'Name=Treasure Planet Nebula', qt.read_text()))

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
        'wallpaper': 'User-supplied image (2026-11-09); third-party signed fan artwork, licence unknown, colours unchanged',
        'wallpaperSourceSha256': hashlib.sha256(source_jpeg.read_bytes()).hexdigest(),
        'quote': {'text': ' '.join(QUOTE_LINES), 'note': 'Original line, not a quotation from the film'},
        'fonts': {'Cinzel': 'SIL OFL 1.1, The Cinzel Project Authors (google/fonts variable TTF, full character set incl. Turkish)'},
    }, indent=2) + '\n')

    data, bounds, size = quote_png(font_path)
    write(ROOT / 'fastfetch-quotes' / (TID + '.png'), data)
    manifest = json.loads((ROOT / 'fastfetch-quotes/manifest.json').read_text())
    manifest['assets'][TID] = {
        'sha256': hashlib.sha256(data).hexdigest(), 'text': ' '.join(QUOTE_LINES), 'lines': list(QUOTE_LINES),
        'font': 'Cinzel', 'fontSha256': hashlib.sha256(font_path.read_bytes()).hexdigest(),
        'fontSize': size, 'inkBounds': bounds,
    }
    write(ROOT / 'fastfetch-quotes/manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')

    base = json.loads((frost / 'manifest.json').read_text())
    files = [dict(e) for e in base['files']]
    for name in ('cinzel.ttf', 'cinzel-license.txt'):
        files.append({'source': 'files/style/shell/assets/' + name, 'target': 'style/shell/assets/' + name})
    for entry in files:
        entry['gitBlob'] = git_blob((dest / entry['source']).read_bytes())
    manifest = dict(base, id=TID, name=NAME, version=VERSION, files=files,
                    preview={'source': 'preview.png', 'gitBlob': git_blob((dest / 'preview.png').read_bytes())})
    write(dest / 'manifest.json', json.dumps(manifest, indent=2) + '\n')
    print('built', TID, len(files), 'files')


if __name__ == '__main__':
    main()
