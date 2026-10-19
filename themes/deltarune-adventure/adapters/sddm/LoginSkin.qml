import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("departure-mono.otf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:displayFont
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:36
    readonly property color c181a18:"#251323"
    readonly property color c191a18:"#251323"
    readonly property color c252620:"#321a2d"
    readonly property color c35342c:"#462339"
    readonly property color c45473e:"#a66376"
    readonly property color c484334:"#a83d59"
    readonly property color c55564c:"#a66376"
    readonly property color c77715e:"#a66376"
    readonly property color c777a70:"#bb8293"
    readonly property color c888b7d:"#d7adbd"
    readonly property color caaa89b:"#d7adbd"
    readonly property color cb5a37c:"#ffcf77"
    readonly property color cce9582:"#ff867f"
    readonly property color cd8d3c5:"#fff1e9"
    readonly property color ce5dcc6:"#fff1e9"
    readonly property color cee191a18:"#ee251323"
    readonly property color cffffff:"#ffffff"
}
