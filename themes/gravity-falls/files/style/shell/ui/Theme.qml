pragma Singleton
import QtQuick
import "../logic/Preferences.js" as Preferences
QtObject {
    property var preferences:Preferences.defaults()
    readonly property bool partyStripEnabled:false
    readonly property real fontScale:preferences.fontScale
    readonly property bool reduceMotion:preferences.reduceMotion
    function applicationSymbol(name) {return /kitty|terminal|alacritty/i.test(name) ? "terminal" : /dolphin|files/i.test(name) ? "folder" : /browser|firefox|zen/i.test(name) ? "browser" : /music|spotify/i.test(name) ? "music" : "windows";}
    function fontSize(pixels) {return Math.max(9,Math.round(pixels*fontScale));}
    function duration(milliseconds) {return reduceMotion ? 0 : milliseconds;}
    // Gravity Falls: a dusk forest town. What you point at warms up, as if a
    // lamp or flashlight found it; the accent is the orange of the old sign.
    readonly property color background:Qt.rgba(0.078,0.059,0.071,preferences.surfaceOpacity)
    readonly property color raised:"#2c1f1b"
    readonly property color ink:"#f4e7d0"
    readonly property color muted:"#b39e8c"
    readonly property color brass:"#f0a84a"
    readonly property color line:"#4a3429"
    readonly property color danger:"#e0574a"
    readonly property color selectedSurface:"#3e2a1f"
    readonly property color activeWorkspaceSurface:"#4a3020"
    readonly property color inputSurface:"#0a0709"
    readonly property color panelScrim:"#10140f12"
    readonly property color switcherScrim:"#b0140f12"
    readonly property color previewStatusSurface:"#ed140f12"
    readonly property color partyPink:"#f0a84a"
    readonly property color partyGreen:"#9cc28a"
    // Journal voice: typewriter (clock, headings). System voice: desktop sans-serif.
    readonly property FontLoader loadedFont:FontLoader {source:Qt.resolvedUrl("../assets/courier-prime-regular.ttf")}
    readonly property FontLoader loadedBold:FontLoader {source:Qt.resolvedUrl("../assets/courier-prime-bold.ttf")}
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
    function portraitFor(symbol) {return symbol==="music" || symbol==="power" ? susie : symbol==="search" || symbol==="bell" ? ralsei : kris;}
}
