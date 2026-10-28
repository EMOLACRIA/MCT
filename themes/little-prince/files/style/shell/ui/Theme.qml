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
    // Little Prince: translucent dusk-blue paper over a paper diorama, star gold
    // accent, amber and rose sheets cut and stacked behind each panel.
    // Translucency only: blur stays off (stability rule).
    readonly property color background:Qt.rgba(0.169,0.196,0.376,0.8*preferences.surfaceOpacity)
    readonly property color raised:"#704a5290"
    readonly property color ink:"#f7eed6"
    readonly property color muted:"#c3c2dc"
    readonly property color brass:"#f2c35a"
    readonly property color line:"#80525a8c"
    readonly property color danger:"#ff8f7c"
    readonly property color selectedSurface:"#a0505aa0"
    readonly property color activeWorkspaceSurface:"#a0505aa0"
    readonly property color inputSurface:"#c01a1f3a"
    readonly property color offsetInk:"#c94a5a"
    readonly property color paperLayer:"#e39a3a"
    readonly property color panelScrim:"#102b3260"
    readonly property color switcherScrim:"#b01e2344"
    readonly property color previewStatusSurface:"#ed1e2344"
    readonly property color partyPink:"#f2c35a"
    readonly property color partyGreen:"#e39a3a"
    // Storybook voice: Lora italic (clock, headings). System voice: desktop sans-serif.
    readonly property FontLoader loadedFont:FontLoader {source:Qt.resolvedUrl("../assets/lora-italic.ttf")}
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
    function portraitFor(symbol) {return symbol==="music" || symbol==="power" ? susie : symbol==="search" || symbol==="bell" ? ralsei : kris;}
}
