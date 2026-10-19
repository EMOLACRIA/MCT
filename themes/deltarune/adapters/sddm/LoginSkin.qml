import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("departure-mono.otf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:displayFont
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:30
    readonly property color c181a18:"#060613"
    readonly property color c191a18:"#060613"
    readonly property color c252620:"#131024"
    readonly property color c35342c:"#211b36"
    readonly property color c45473e:"#69518c"
    readonly property color c484334:"#362342"
    readonly property color c55564c:"#69518c"
    readonly property color c77715e:"#69518c"
    readonly property color c777a70:"#796990"
    readonly property color c888b7d:"#aaa1c4"
    readonly property color caaa89b:"#aaa1c4"
    readonly property color cb5a37c:"#f32baf"
    readonly property color cce9582:"#ff88ad"
    readonly property color cd8d3c5:"#e9ddff"
    readonly property color ce5dcc6:"#e9ddff"
    readonly property color cee191a18:"#ee060613"
    readonly property color cffffff:"#ffffff"
}
