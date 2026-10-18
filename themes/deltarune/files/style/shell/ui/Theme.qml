pragma Singleton
import QtQuick
import "../logic/Preferences.js" as Preferences
QtObject {
    property var preferences:Preferences.defaults()
    readonly property bool partyStripEnabled:true
    readonly property real fontScale:preferences.fontScale
    readonly property bool reduceMotion:preferences.reduceMotion
    function fontSize(pixels) {return Math.max(9,Math.round(pixels*fontScale));}
    function duration(milliseconds) {return reduceMotion ? 0 : milliseconds;}
    readonly property color background:Qt.rgba(0,0.012,0.025,preferences.surfaceOpacity)
    readonly property color raised:"#062945"
    readonly property color ink:"#eefaff"
    readonly property color muted:"#99bacc"
    readonly property color brass:"#00d9ef"
    readonly property color line:"#195a78"
    readonly property color danger:"#ff839e"
    readonly property color selectedSurface:"#093e61"
    readonly property color activeWorkspaceSurface:"#062945"
    readonly property color inputSurface:"#01080e"
    readonly property color panelScrim:"#18000000"
    readonly property color switcherScrim:"#b000060d"
    readonly property color previewStatusSurface:"#ed000810"
    readonly property color partyPink:"#ed70df"
    readonly property color partyGreen:"#71e7a5"
    readonly property FontLoader loadedFont:FontLoader {source:Qt.resolvedUrl("../assets/departure-mono.otf")}
    readonly property string displayFont:loadedFont.status===FontLoader.Ready ? loadedFont.name : "monospace"
    readonly property string bodyFont:displayFont
    readonly property int quickMotion:70
    readonly property int panelEnterMotion:90
    readonly property int ornamentSize:14
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
