import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("departure-mono.otf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:displayFont
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:14
    readonly property color c181a18:"#00060d"
    readonly property color c191a18:"#00060d"
    readonly property color c252620:"#061927"
    readonly property color c35342c:"#062945"
    readonly property color c45473e:"#195a78"
    readonly property color c484334:"#093e61"
    readonly property color c55564c:"#195a78"
    readonly property color c77715e:"#195a78"
    readonly property color c777a70:"#526d88"
    readonly property color c888b7d:"#99bacc"
    readonly property color caaa89b:"#99bacc"
    readonly property color cb5a37c:"#00d9ef"
    readonly property color cce9582:"#ff839e"
    readonly property color cd8d3c5:"#eefaff"
    readonly property color ce5dcc6:"#eefaff"
    readonly property color cee191a18:"#ee00060d"
    readonly property color cffffff:"#ffffff"
}
