import QtQuick
import "../surfaces"
BarSurface {
    clockSize:17;workspaceRadius:1
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:1;color:Theme.line}
    }}
}
