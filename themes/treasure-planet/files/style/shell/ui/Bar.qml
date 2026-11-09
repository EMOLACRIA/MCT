import QtQuick
import "../surfaces"
// Glass strip with a silver rule and a darker rule beneath, like a ship's rail.
BarSurface {
    clockSize:19;workspaceRadius:2
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:2;color:Theme.frame}
        Rectangle {anchors.bottom:parent.bottom;anchors.bottomMargin:-4;width:parent.width;height:1;color:Theme.brassDark}
    }}
}
