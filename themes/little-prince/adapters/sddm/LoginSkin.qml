import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("lora-italic.ttf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:"sans-serif"
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:8
    readonly property color c181a18:"#1e2344"
    readonly property color c191a18:"#1e2344"
    readonly property color c252620:"#232a50"
    readonly property color c35342c:"#2f3762"
    readonly property color c45473e:"#4a5288"
    readonly property color c484334:"#454f8a"
    readonly property color c55564c:"#4a5288"
    readonly property color c77715e:"#4a5288"
    readonly property color c777a70:"#8a8fb8"
    readonly property color c888b7d:"#c3c2dc"
    readonly property color caaa89b:"#c3c2dc"
    readonly property color cb5a37c:"#f2c35a"
    readonly property color cce9582:"#ff8f7c"
    readonly property color cd8d3c5:"#f7eed6"
    readonly property color ce5dcc6:"#f7eed6"
    readonly property color cee191a18:"#ee1e2344"
    readonly property color cffffff:"#ffffff"
}
