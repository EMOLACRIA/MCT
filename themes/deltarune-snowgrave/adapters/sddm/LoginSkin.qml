import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("departure-mono.otf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:displayFont
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:36
    readonly property color c181a18:"#0b1421"
    readonly property color c191a18:"#0b1421"
    readonly property color c252620:"#102236"
    readonly property color c35342c:"#162d45"
    readonly property color c45473e:"#365873"
    readonly property color c484334:"#224c6b"
    readonly property color c55564c:"#365873"
    readonly property color c77715e:"#365873"
    readonly property color c777a70:"#6f94b4"
    readonly property color c888b7d:"#9fb8d0"
    readonly property color caaa89b:"#9fb8d0"
    readonly property color cb5a37c:"#9cdfff"
    readonly property color cce9582:"#e68a9d"
    readonly property color cd8d3c5:"#edf7ff"
    readonly property color ce5dcc6:"#edf7ff"
    readonly property color cee191a18:"#ee0b1421"
    readonly property color cffffff:"#ffffff"
}
