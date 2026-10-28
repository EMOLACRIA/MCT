import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("permanent-marker.ttf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:"sans-serif"
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:8
    readonly property color c181a18:"#ece8de"
    readonly property color c191a18:"#ece8de"
    readonly property color c252620:"#e4dfd3"
    readonly property color c35342c:"#ddd7ca"
    readonly property color c45473e:"#b9b3a6"
    readonly property color c484334:"#f2a9bb"
    readonly property color c55564c:"#b9b3a6"
    readonly property color c77715e:"#b9b3a6"
    readonly property color c777a70:"#8a857b"
    readonly property color c888b7d:"#5c5850"
    readonly property color caaa89b:"#5c5850"
    readonly property color cb5a37c:"#e8285a"
    readonly property color cce9582:"#c2410c"
    readonly property color cd8d3c5:"#111111"
    readonly property color ce5dcc6:"#111111"
    readonly property color cee191a18:"#eeece8de"
    readonly property color cffffff:"#111111"
}
