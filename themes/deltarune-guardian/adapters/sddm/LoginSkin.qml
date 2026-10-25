import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("departure-mono.otf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:displayFont
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:36
    readonly property color c181a18:"#0b1120"
    readonly property color c191a18:"#0b1120"
    readonly property color c252620:"#111a2d"
    readonly property color c35342c:"#252842"
    readonly property color c45473e:"#7c83ac"
    readonly property color c484334:"#303052"
    readonly property color c55564c:"#7c83ac"
    readonly property color c77715e:"#7c83ac"
    readonly property color c777a70:"#939abe"
    readonly property color c888b7d:"#aaaed0"
    readonly property color caaa89b:"#aaaed0"
    readonly property color cb5a37c:"#a7e5f7"
    readonly property color cce9582:"#ee99c3"
    readonly property color cd8d3c5:"#eae5ff"
    readonly property color ce5dcc6:"#eae5ff"
    readonly property color cee191a18:"#ee0b1120"
    readonly property color cffffff:"#ffffff"
}
