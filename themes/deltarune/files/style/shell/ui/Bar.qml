import QtQuick
import "../surfaces"
BarSurface {
    clockSize:18;workspaceRadius:0
    barBackground:Component {Rectangle {
        color:Theme.background
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:1;color:Theme.brass}
    }}
}
