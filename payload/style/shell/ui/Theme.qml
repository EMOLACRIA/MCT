pragma Singleton
import QtQuick
import "../logic/Preferences.js" as Preferences
QtObject {
    property var preferences:Preferences.defaults()
    readonly property real fontScale:preferences.fontScale
    readonly property bool reduceMotion:preferences.reduceMotion
    function fontSize(pixels) {return Math.max(8,Math.round(pixels*fontScale));}
    function duration(milliseconds) {return reduceMotion ? 0 : milliseconds;}
    readonly property color background:Qt.rgba(25/255,26/255,24/255,preferences.surfaceOpacity)
    readonly property color raised: "#282923"
    readonly property color ink: "#d8d3c5"
    readonly property color muted: "#96988c"
    readonly property color brass: "#b5a37c"
    readonly property color line: "#5d5949"
    readonly property color danger: "#ce9582"
    // Semantic surface roles: callers do not choose their own palette literals.
    readonly property color selectedSurface: "#39392f"
    readonly property color activeWorkspaceSurface: "#35362d"
    readonly property color inputSurface: "#242620"
    readonly property color panelScrim: "#55000000"
    readonly property color switcherScrim: "#880c0d0b"
    readonly property color previewStatusSurface: "#e6191a18"
    readonly property string displayFont: "serif"
    readonly property string bodyFont: "sans-serif"
    readonly property int quickMotion:110
    readonly property int panelEnterMotion:140
    readonly property int ornamentSize:20
    readonly property url wallpaper:Qt.resolvedUrl("../assets/wallpaper.png")
    readonly property url cornerTopLeft:Qt.resolvedUrl("../assets/tl.svg")
    readonly property url cornerTopRight:Qt.resolvedUrl("../assets/tr.svg")
    readonly property url cornerBottomLeft:Qt.resolvedUrl("../assets/bl.svg")
    readonly property url cornerBottomRight:Qt.resolvedUrl("../assets/br.svg")
}
