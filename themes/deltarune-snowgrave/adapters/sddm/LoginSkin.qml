import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("departure-mono.otf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:displayFont
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:36
    readonly property color c181a18:"#160e0b"
    readonly property color c191a18:"#160e0b"
    readonly property color c252620:"#231710"
    readonly property color c35342c:"#38231b"
    readonly property color c45473e:"#806044"
    readonly property color c484334:"#582c21"
    readonly property color c55564c:"#806044"
    readonly property color c77715e:"#806044"
    readonly property color c777a70:"#96785b"
    readonly property color c888b7d:"#bda78f"
    readonly property color caaa89b:"#bda78f"
    readonly property color cb5a37c:"#d8b779"
    readonly property color cce9582:"#ef866c"
    readonly property color cd8d3c5:"#f4ead8"
    readonly property color ce5dcc6:"#f4ead8"
    readonly property color cee191a18:"#ee160e0b"
    readonly property color cffffff:"#ffffff"
}
