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
    readonly property color background:Qt.rgba(0.043,0.067,0.125,preferences.surfaceOpacity)
    readonly property color raised:"#252842"
    readonly property color ink:"#eae5ff"
    readonly property color muted:"#aaaed0"
    readonly property color brass:"#a7e5f7"
    readonly property color line:"#7c83ac"
    readonly property color danger:"#ee99c3"
    readonly property color selectedSurface:"#303052"
    readonly property color activeWorkspaceSurface:"#5a4d87"
    readonly property color inputSurface:"#080d18"
    readonly property color panelScrim:"#100b1120"
    readonly property color switcherScrim:"#b00b1120"
    readonly property color previewStatusSurface:"#ed0b1120"
    readonly property color partyPink:"#a7e5f7"
    readonly property color partyGreen:"#acbff0"
    readonly property FontLoader loadedFont:FontLoader {source:Qt.resolvedUrl("../assets/departure-mono.otf")}
    readonly property string displayFont:loadedFont.status===FontLoader.Ready ? loadedFont.name : "monospace"
    readonly property string bodyFont:displayFont
    readonly property int quickMotion:130
    readonly property int panelEnterMotion:180
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
