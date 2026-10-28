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
    // Spider-Punk zine: photocopy paper and black ink. Panels are torn paper
    // printed slightly out of register: a cyan layer peeks out behind each one.
    readonly property color background:Qt.rgba(0.925,0.910,0.871,preferences.surfaceOpacity)
    readonly property color raised:"#f4dce2"
    readonly property color ink:"#111111"
    readonly property color muted:"#5c5850"
    readonly property color brass:"#e8285a"
    readonly property color line:"#b9b3a6"
    readonly property color danger:"#c2410c"
    readonly property color selectedSurface:"#f2a9bb"
    readonly property color activeWorkspaceSurface:"#f2a9bb"
    readonly property color inputSurface:"#f7f4ec"
    readonly property color offsetInk:"#2fb3e8"
    readonly property color panelScrim:"#10ece8de"
    readonly property color switcherScrim:"#b0ece8de"
    readonly property color previewStatusSurface:"#edece8de"
    readonly property color partyPink:"#e8285a"
    readonly property color partyGreen:"#2fb3e8"
    // Marker voice: clock and headings. System voice: desktop sans-serif.
    readonly property FontLoader loadedFont:FontLoader {source:Qt.resolvedUrl("../assets/permanent-marker.ttf")}
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
    function portraitFor(symbol) {return symbol==="music" || symbol==="power" ? susie : symbol==="search" || symbol==="bell" ? ralsei : kris;}
}
