import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("courier-prime-regular.ttf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:"sans-serif"
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:44
    readonly property color c181a18:"#140f12"
    readonly property color c191a18:"#140f12"
    readonly property color c252620:"#1e1618"
    readonly property color c35342c:"#2c1f1b"
    readonly property color c45473e:"#4a3429"
    readonly property color c484334:"#3e2a1f"
    readonly property color c55564c:"#4a3429"
    readonly property color c77715e:"#4a3429"
    readonly property color c777a70:"#8a7566"
    readonly property color c888b7d:"#b39e8c"
    readonly property color caaa89b:"#b39e8c"
    readonly property color cb5a37c:"#f0a84a"
    readonly property color cce9582:"#e0574a"
    readonly property color cd8d3c5:"#f4e7d0"
    readonly property color ce5dcc6:"#f4e7d0"
    readonly property color cee191a18:"#ee140f12"
    readonly property color cffffff:"#ffffff"
}
