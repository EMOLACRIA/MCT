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
    // Treasure Planet · Nebula: ship's navigation plates over the etherium. Pale
    // turquoise accent, silver fittings, ion green kept for small highlights.
    readonly property color background:Qt.rgba(0.043,0.114,0.157,0.88*preferences.surfaceOpacity)
    readonly property color raised:"#801a3646"
    readonly property color ink:"#eef8ff"
    readonly property color muted:"#a3c2cf"
    readonly property color brass:"#7fe3ef"
    readonly property color line:"#90587f90"
    readonly property color danger:"#ff8a7a"
    readonly property color selectedSurface:"#b01a4a5e"
    readonly property color activeWorkspaceSurface:"#b01a4a5e"
    readonly property color inputSurface:"#c005121a"
    readonly property color glow:"#5cf0b0"
    readonly property color frame:"#b9cdd2"
    readonly property color brassDark:"#34586a"
    readonly property color panelScrim:"#100b1d28"
    readonly property color switcherScrim:"#b00e2230"
    readonly property color previewStatusSurface:"#ed0e2230"
    readonly property color partyPink:"#7fe3ef"
    readonly property color partyGreen:"#5cf0b0"
    // Chart lettering for clock and headings (Cinzel); system text stays sans-serif.
    readonly property FontLoader loadedFont:FontLoader {source:Qt.resolvedUrl("../assets/cinzel.ttf")}
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
