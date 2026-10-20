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
    readonly property color background:Qt.rgba(0.043,0.078,0.129,preferences.surfaceOpacity)
    readonly property color raised:"#162d45"
    readonly property color ink:"#edf7ff"
    readonly property color muted:"#9fb8d0"
    readonly property color brass:"#9cdfff"
    readonly property color line:"#365873"
    readonly property color danger:"#e68a9d"
    readonly property color selectedSurface:"#224c6b"
    readonly property color activeWorkspaceSurface:"#2c6080"
    readonly property color inputSurface:"#070f1a"
    readonly property color panelScrim:"#100b1421"
    readonly property color switcherScrim:"#b00b1421"
    readonly property color previewStatusSurface:"#ed0b1421"
    readonly property color partyPink:"#9cdfff"
    readonly property color partyGreen:"#b6e9e5"
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
