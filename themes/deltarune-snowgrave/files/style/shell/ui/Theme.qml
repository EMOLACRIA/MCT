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
    readonly property color background:Qt.rgba(0.086,0.055,0.043,preferences.surfaceOpacity)
    readonly property color raised:"#38231b"
    readonly property color ink:"#f4ead8"
    readonly property color muted:"#bda78f"
    readonly property color brass:"#d8b779"
    readonly property color line:"#806044"
    readonly property color danger:"#ef866c"
    readonly property color selectedSurface:"#582c21"
    readonly property color activeWorkspaceSurface:"#633125"
    readonly property color inputSurface:"#100b09"
    readonly property color panelScrim:"#10160e0b"
    readonly property color switcherScrim:"#b0160e0b"
    readonly property color previewStatusSurface:"#ed160e0b"
    readonly property color partyPink:"#d8b779"
    readonly property color partyGreen:"#a8b384"
    readonly property FontLoader loadedFont:FontLoader {source:Qt.resolvedUrl("../assets/departure-mono.otf")}
    readonly property string displayFont:loadedFont.status===FontLoader.Ready ? loadedFont.name : "monospace"
    readonly property string bodyFont:displayFont
    readonly property int quickMotion:110
    readonly property int panelEnterMotion:140
    readonly property int ornamentSize:36
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
