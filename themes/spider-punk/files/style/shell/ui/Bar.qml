import QtQuick
import "../surfaces"
// Paper strip with a pink rule and its cyan misprint underneath.
BarSurface {
    clockSize:19;workspaceRadius:0
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:3;color:Theme.brass}
        Rectangle {anchors.bottom:parent.bottom;anchors.bottomMargin:-3;width:parent.width;height:3;color:Theme.offsetInk}
    }}
}
