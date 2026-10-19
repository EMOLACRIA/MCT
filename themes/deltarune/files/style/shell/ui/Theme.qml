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
    readonly property color background:Qt.rgba(0.024,0.024,0.075,preferences.surfaceOpacity)
    readonly property color raised:"#211b36"
    readonly property color ink:"#e9ddff"
    readonly property color muted:"#aaa1c4"
    readonly property color brass:"#f32baf"
    readonly property color line:"#69518c"
    readonly property color danger:"#ff88ad"
    readonly property color selectedSurface:"#362342"
    readonly property color activeWorkspaceSurface:"#362342"
    readonly property color inputSurface:"#050511"
    readonly property color panelScrim:"#10040310"
    readonly property color switcherScrim:"#b0060613"
    readonly property color previewStatusSurface:"#ed060613"
    readonly property color partyPink:"#f32baf"
    readonly property color partyGreen:"#71e7a5"
    readonly property FontLoader loadedFont:FontLoader {source:Qt.resolvedUrl("../assets/departure-mono.otf")}
    readonly property string displayFont:loadedFont.status===FontLoader.Ready ? loadedFont.name : "monospace"
    readonly property string bodyFont:displayFont
    readonly property int quickMotion:110
    readonly property int panelEnterMotion:140
    readonly property int ornamentSize:30
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
