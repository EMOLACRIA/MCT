import QtQuick
QtObject {
    readonly property FontLoader font:FontLoader {source:Qt.resolvedUrl("cinzel.ttf")}
    readonly property string displayFont:font.name || "monospace"
    readonly property string bodyFont:"sans-serif"
    readonly property bool clockPlate:true
    readonly property bool formOnLeft:true
    readonly property int cornerSize:6
    readonly property color c181a18:"#0e2230"
    readonly property color c191a18:"#0e2230"
    readonly property color c252620:"#10283a"
    readonly property color c35342c:"#163246"
    readonly property color c45473e:"#34586a"
    readonly property color c484334:"#23506a"
    readonly property color c55564c:"#34586a"
    readonly property color c77715e:"#34586a"
    readonly property color c777a70:"#6f93a3"
    readonly property color c888b7d:"#a3c2cf"
    readonly property color caaa89b:"#a3c2cf"
    readonly property color cb5a37c:"#7fe3ef"
    readonly property color cce9582:"#ff8a7a"
    readonly property color cd8d3c5:"#eef8ff"
    readonly property color ce5dcc6:"#eef8ff"
    readonly property color cee191a18:"#ee0e2230"
    readonly property color cffffff:"#ffffff"
}
